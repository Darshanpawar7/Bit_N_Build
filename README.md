# ⚡ Bit-N-Build | FlowState ⚡

**An autonomous multi-agent microgrid resilience system for predicting grid stress, coordinating local energy exchange, and protecting communities during peak demand.**

## 🚀 Live Demo

**[bit-n-build-wine.vercel.app](https://bit-n-build-wine.vercel.app/)**

Open the link to explore the FlowState digital twin in the browser. Drag to rotate the
3D community, click any house for its energy telemetry, and use the scenario simulator
to trigger cloud cover, a heatwave, a grid outage, an EV surge or peak demand.

## 📌 Ownership

FlowState was designed and built entirely by the **Bit-N-Build** team for the Bit-N-Build hackathon.

Our team created the multi-agent energy architecture, simulation environment, digital-twin interface, energy optimization components, resilience layer, P2P coordination, autonomous recovery planning, and FlowState visualization.

## 🎯 Challenge Track

> **Decentralised Energy Systems & Micro-Grids**

### Problem

Create agent networks that monitor hyper-local power generation, predict grid failures, and autonomously execute peer-to-peer energy trading during peak demand.

### Our Approach

FlowState extends a multi-agent microgrid foundation with an autonomous resilience layer that:

- detects grid stress and estimates failure risk
- identifies available local energy
- coordinates peer-to-peer energy transfers
- plans autonomous recovery actions
- works alongside deterministic energy optimization

## 🌍 The Vision

Traditional microgrids often react to instability after it occurs.

**FlowState takes a proactive approach.**

Multiple specialized agents continuously evaluate generation, consumption, storage, EV demand, and grid conditions. When the system detects rising instability, it coordinates local energy resources before a failure propagates.

The goal is simple:

> **Predict → Coordinate → Act → Stabilize**

## 🤖 Autonomous Resilience Layer

FlowState introduces a new resilience layer into the existing agent pipeline.

### Resilience Agent

The Resilience Agent evaluates:

- current energy demand
- renewable generation
- battery state of charge
- EV charging pressure
- grid availability

It produces a normalized grid-risk score:

```text
LOW       → stable operation
MEDIUM    → preventive actions armed
HIGH      → autonomous recovery activated
```

### P2P Coordination

When local energy is available, the agent identifies compatible buyers and sellers and creates simulated peer-to-peer energy transfers.

Example:

```text
COMMUNITY SOLAR
      ↓
   2.8 kWh
      ↓
HOUSE H07
```

### Autonomous Recovery

During high-risk conditions, FlowState can recommend:

- local P2P energy transfer
- battery reserve activation
- EV charging deferral
- flexible load shifting
- island-mode operation during grid outages

## 🧠 FlowState Architecture

```text
             Community State
                    │
                    ▼
              Solar Agent
                    │
                    ▼
             Battery Agent
                    │
                    ▼
             House Agents
                    │
                    ▼
                EV Agent
                    │
                    ▼
               Grid Agent
                    │
                    ▼
          ┌──────────────────┐
          │ Resilience Agent │
          └────────┬─────────┘
                   │
          ┌────────┴────────┐
          ▼                 ▼
     P2P Coordination   Risk Assessment
          │                 │
          └────────┬────────┘
                   ▼
        Autonomous Recovery Plan
                   │
                   ▼
              Optimizer
                   │
                   ▼
             Final Dispatch
```

## ⚡ Demo Scenario: Peak Demand

FlowState can simulate a sudden community-wide demand spike.

### Step 1 — Detect

Household demand rises sharply.

### Step 2 — Assess

The Resilience Agent calculates grid instability risk.

### Step 3 — Coordinate

The P2P Agent searches for locally available energy.

### Step 4 — Recover

The system prioritizes:

1. Local renewable energy
2. Peer-to-peer transfers
3. Battery support
4. Flexible EV charging
5. Flexible household loads

### Step 5 — Stabilize

The optimizer calculates the final dispatch and the dashboard reports:

- failure risk
- energy traded locally
- battery support
- deferred loads
- remaining grid import

## 🎮 Digital Twin

The interactive 3D dashboard provides:

- spatial monitoring of houses, EVs, solar, battery, and grid nodes
- animated solar, battery, grid, and P2P energy flows
- selectable peak-demand, heatwave, cloud-cover, outage, and EV-surge scenarios
- live agent negotiation logs and resilience status

## ⚙️ Tech Stack

- **Frontend:** Next.js, React, Tailwind CSS, Three.js / React Three Fiber
- **Backend:** Python, FastAPI, WebSockets
- **Agent Orchestration:** LangGraph
- **LLM Infrastructure:** Groq
- **Energy Optimization:** Deterministic dispatch and load-management logic
- **Simulation:** Synthetic community energy scenarios

## 💻 Get Started Locally

### 1. Clone the repository

```bash
git clone https://github.com/Darshanpawar7/Bit_N_Build.git
cd Bit_N_Build
```

### 2. Backend Setup

```bash
cd backend
python -m venv venv
venv\Scripts\activate  # On Windows
pip install -r requirements.txt

# Create a .env file and add your API keys when using live providers:
# GROQ_API_KEY=your_key
# SARWAM_API_KEY=your_key

uvicorn main:app --reload
```

### 3. Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

Visit `http://localhost:3000` to open the FlowState digital twin.

A hosted build of the frontend is already live at
**[bit-n-build-wine.vercel.app](https://bit-n-build-wine.vercel.app/)**. It runs in mock
mode, so the steps above are only needed to exercise the Python agent backend.

## 👥 Team

**Bit-N-Build — FlowState**

Prithvi S P | Darshan Pawar | Chandan Kumar K |

Designed and built entirely by the **Bit-N-Build** team for the **Bit-N-Build** Hackathon.
