"""
Resilience + P2P coordination layer for GridSwarm.

Adds:
- deterministic grid failure risk estimation
- local peer-to-peer energy matching

Uses existing CommunityState schema without changing field names.
"""

from agents.state import CommunityState
from agents.logger import log_event


def resilience_agent_fn(state: CommunityState) -> CommunityState:
    """Estimate failure risk and identify simple local P2P trades."""
    solar = state["solar"]
    battery = state["battery"]
    households = state["households"]
    evs = state["evs"]
    grid = state["grid"]

    total_demand = sum(h["current_demand"] for h in households)
    solar_generation = solar["current_generation"]

    # Demand pressure: how much of current demand is not covered by solar.
    demand_pressure = (
        max(0.0, total_demand - solar_generation) / max(total_demand, 1.0)
    )

    # Battery stress: low SoC means less resilience.
    battery_stress = max(0.0, 1.0 - (battery["soc"] / 100.0))

    # EV pressure: active charging increases short-term stress.
    charging_evs = [ev for ev in evs if ev["currently_charging"]]
    ev_pressure = min(1.0, len(charging_evs) / max(len(evs), 1))

    # Grid outage is the strongest signal.
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

    # ---- P2P energy matching ----
    seller_kwh = max(0.0, solar_generation - total_demand)

    # If solar itself is not surplus, allow a portion of battery capacity
    # to act as a local seller.
    if seller_kwh <= 0 and battery["available_discharge"] > 0:
        seller_kwh = min(
            battery["available_discharge"],
            max(0.0, battery["available_discharge"] * 0.5),
        )

    flexible_buyers = sorted(
        households,
        key=lambda h: h["flexibility"],
        reverse=False,
    )

    # Approximate deficit buyers: households under higher demand pressure.
    trades = []

    remaining = round(seller_kwh, 2)

    for house in flexible_buyers:
        if remaining <= 0:
            break

        # Only create a local trade when there is meaningful surplus.
        if seller_kwh > 0:
            trade_kwh = min(remaining, max(
                0.0, house["current_demand"] * 0.25))

            if trade_kwh > 0:
                trades.append(
                    {
                        "seller": "COMMUNITY_SOLAR",
                        "buyer": house["house_id"],
                        "energy_kwh": round(trade_kwh, 2),
                        "price_inr_per_kwh": 5.0,
                    }
                )
                remaining -= trade_kwh

    state["decisions"]["resilience"] = {
        "risk_score": round(risk_score, 2),
        "risk_level": risk_level,
        "p2p_trades": trades,
        "local_energy_traded_kwh": round(
            sum(t["energy_kwh"] for t in trades), 2
        ),
    }

    log_event(
        state,
        f"Resilience Agent: grid risk {risk_level} "
        f"({risk_score * 100:.0f}%)."
    )

    if trades:
        log_event(
            state,
            f"P2P Agent: identified {len(trades)} local energy trade(s), "
            f"moving {sum(t['energy_kwh'] for t in trades):.1f} kWh."
        )
    else:
        log_event(
            state,
            "P2P Agent: no local surplus available for peer-to-peer trading."
        )

    return state
