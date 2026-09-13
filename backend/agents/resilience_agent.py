"""
GridSwarm resilience agent.

Adds:
- deterministic grid failure risk estimation
- P2P energy coordination
- autonomous recovery planning

The existing CommunityState schema is preserved.
"""

from agents.state import CommunityState
from agents.logger import log_event


def resilience_agent_fn(state: CommunityState) -> CommunityState:
    """Assess grid stress, coordinate local energy, and create a recovery plan."""

    solar = state["solar"]
    battery = state["battery"]
    households = state["households"]
    evs = state["evs"]
    grid = state["grid"]

    total_demand = sum(h["current_demand"] for h in households)
    solar_generation = solar["current_generation"]

    # -----------------------------
    # 1. Calculate resilience risk
    # -----------------------------
    demand_pressure = max(
        0.0,
        total_demand - solar_generation
    ) / max(total_demand, 1.0)

    battery_stress = max(
        0.0,
        1.0 - (battery["soc"] / 100.0)
    )

    charging_evs = [
        ev for ev in evs
        if ev["currently_charging"]
    ]

    ev_pressure = min(
        1.0,
        len(charging_evs) / max(len(evs), 1)
    )

    outage_factor = 1.0 if not grid["availability"] else 0.0

    risk_score = (
        demand_pressure * 0.35
        + battery_stress * 0.20
        + ev_pressure * 0.15
        + outage_factor * 0.30
    )

    risk_score = max(0.0, min(1.0, risk_score))

    if risk_score >= 0.70:
        risk_level = "HIGH"
    elif risk_score >= 0.40:
        risk_level = "MEDIUM"
    else:
        risk_level = "LOW"

    log_event(
        state,
        f"Resilience Agent: risk assessment = "
        f"{risk_level} ({risk_score * 100:.0f}%)."
    )

    # -----------------------------
    # 2. Identify local energy
    # -----------------------------
    solar_surplus = max(
        0.0,
        solar_generation - total_demand
    )

    battery_available = max(
        0.0,
        battery["available_discharge"]
    )

    sellers = []

    if solar_surplus > 0:
        sellers.append(
            {
                "source": "COMMUNITY_SOLAR",
                "available_kwh": round(solar_surplus, 2),
            }
        )

    if battery_available > 0:
        sellers.append(
            {
                "source": "COMMUNITY_BATTERY",
                "available_kwh": round(
                    min(battery_available, battery_available * 0.5),
                    2,
                ),
            }
        )

    # -----------------------------
    # 3. Identify buyers
    # -----------------------------
    buyers = sorted(
        households,
        key=lambda h: (
            0 if h["priority"] == "critical" else
            1 if h["priority"] == "normal" else
            2
        )
    )

    trades = []
    remaining_energy = sum(
        seller["available_kwh"]
        for seller in sellers
    )

    seller_index = 0

    for house in buyers:
        if remaining_energy <= 0:
            break

        demand = max(
            0.0,
            house["current_demand"]
        )

        # Critical and normal loads get priority.
        requested = min(
            demand * 0.25 if house["priority"] != "critical"
            else demand * 0.40,
            remaining_energy,
        )

        if requested <= 0:
            continue

        while (
            seller_index < len(sellers)
            and sellers[seller_index]["available_kwh"] <= 0
        ):
            seller_index += 1

        if seller_index >= len(sellers):
            break

        seller = sellers[seller_index]

        amount = min(
            requested,
            seller["available_kwh"],
        )

        if amount <= 0:
            continue

        trades.append(
            {
                "seller": seller["source"],
                "buyer": house["house_id"],
                "energy_kwh": round(amount, 2),
                "price_inr_per_kwh": 5.0,
            }
        )

        seller["available_kwh"] -= amount
        remaining_energy -= amount

    traded_kwh = round(
        sum(t["energy_kwh"] for t in trades),
        2,
    )

    if trades:
        log_event(
            state,
            f"P2P Agent: matched {len(trades)} local trade(s), "
            f"coordinating {traded_kwh:.1f} kWh."
        )
    else:
        log_event(
            state,
            "P2P Agent: no viable local energy trade found."
        )

    # -----------------------------
    # 4. Autonomous recovery plan
    # -----------------------------
    recovery_actions = []

    if risk_level == "HIGH":
        if traded_kwh > 0:
            recovery_actions.append(
                f"Execute {traded_kwh:.1f} kWh local P2P transfer"
            )

        if battery_available > 0:
            recovery_actions.append(
                "Reserve community battery for critical demand"
            )

        flexible_evs = [
            ev["ev_id"]
            for ev in evs
            if ev["currently_charging"]
            and ev["flex_window_hrs"] > 1.0
        ]

        if flexible_evs:
            recovery_actions.append(
                f"Defer flexible EV charging: {', '.join(flexible_evs[:3])}"
            )

        flexible_houses = [
            h["house_id"]
            for h in households
            if h["priority"] == "flexible"
            and h["flexibility"] >= 0.5
        ]

        if flexible_houses:
            recovery_actions.append(
                f"Shift flexible loads: {', '.join(flexible_houses[:3])}"
            )

        if not grid["availability"]:
            recovery_actions.append(
                "Maintain island mode — grid import unavailable"
            )

        log_event(
            state,
            "Recovery Coordinator: HIGH risk detected — "
            f"{len(recovery_actions)} autonomous action(s) planned."
        )

    elif risk_level == "MEDIUM":
        recovery_actions.extend(
            [
                "Monitor local demand growth",
                "Prioritize local renewable energy",
                "Prepare flexible loads for demand response",
            ]
        )

        log_event(
            state,
            "Recovery Coordinator: medium risk — "
            "preventive actions armed."
        )

    else:
        recovery_actions.extend(
            [
                "Continue continuous grid monitoring",
                "Maintain P2P market readiness",
            ]
        )

    # -----------------------------
    # 5. Persist decisions
    # -----------------------------
    state["decisions"]["resilience"] = {
        "risk_score": round(risk_score, 2),
        "risk_level": risk_level,
        "p2p_trades": trades,
        "local_energy_traded_kwh": traded_kwh,
        "recovery_actions": recovery_actions,
        "autonomous": True,
    }

    return state
