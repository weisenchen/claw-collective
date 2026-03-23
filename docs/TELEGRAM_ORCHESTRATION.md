# Telegram-Powered Orchestration scenarios

This guide outlines several scenarios for how `claws` can be integrated with a Telegram bot or an agent-bridge that monitors Telegram channels. In these scenarios, the Telegram bot acts as the "Leader's Voice" or the "Human Proxy," translating natural language instructions into `claws` CLI commands.

---

## 🚀 Getting Started (Initial Setup)

Before you can orchestrate your collective via Telegram, the **Bridge Agent** (running on your Lead machine) must have the `claws` tool installed:

```bash
# 1. Clone the repository
git clone https://github.com/weisenchen/claw-collective.git

# 2. Enter and install
cd claw-collective
pip install .

# 3. Initialize your first workspace
claws init ./my-orchestra
```

---

## 🏗️ Scenario 1: Natural Language Team Creation

**User Instruction (in Telegram):**
> "Hey bot, set up a new research team for the 'Quantum Algorithms' project. We need a Lead researcher and two security reviewers."

**Telegram Bridge Action:**
The bridge (an agent running on the Leader machine) parses the intent and executes the following:

1.  **Initialize local workspace (if needed):**
    ```bash
    claws init ./quantum-research
    ```
2.  **Create the team:**
    ```bash
    claws team create quantum-team --description "Quantum Algorithm Research Team" --leader "LeadResearcher"
    ```
3.  **Spawn the Lead agent:**
    ```bash
    claws spawn --team quantum-team --name "LeadResearcher" --task "Initial architecture and roadmap"
    ```
4.  **Confirm to Telegram:**
    > "✅ Team 'quantum-team' created! Spawning LeadResearcher..."

---

## 🛰️ Scenario 2: Multi-Machine Registration (Leader & Worker Setup)

`claws` is designed for multi-machine coordination. You can register machines as **Leaders** (owning the workspace) or **Workers** (joining the workspace) via Telegram.

### A. Registering the Leader
**User Instruction (on Lead Machine):**
> "Bot, register this machine as the Leader for the 'Stealth-Project' workspace."

**Telegram Bridge Action:**
The bridge on the Lead machine executes:
```bash
claws register --role Leader --name Lead-Machine-01 --workspace ./stealth-project
```

### B. Registering a Worker
**User Instruction (on Worker Machine 1):**
> "Bot, join the 'Stealth-Project' at 'https://github.com/org/stealth.git' as a Worker."

**Telegram Bridge Action:**
The bridge on the Worker machine executes:
```bash
# 1. Joins the workspace
git clone https://github.com/org/stealth.git .
# 2. Registers as worker
claws register --role Worker --name Worker-Node-01
```

**Result:**
The Leader can now see both machines in the `agent_directory.md` and assign tasks via Telegram.

---

## 🚀 Scenario 3: Launching from a Predefined Template

**User Instruction (in Telegram):**
> "Launch the standard 'Development-Trio' team template."

**Telegram Bridge Action:**
The bridge searches for the `development-trio.toml` file and executes:
```bash
claws launch development-trio.toml
```

**Result:**
`claws` automatically creates the team and spawns all agents defined in the TOML file (e.g., Frontend, Backend, and Tester).

---

## 🧩 Scenario 4: Ad-hoc Agent Spawning

**User Instruction (in Telegram):**
> "We're hitting a bottleneck in the database. Add a database expert named 'QueryOptimizer' to the Ethics project to help with indexing."

**Telegram Bridge Action:**
The bridge executes:
```bash
claws spawn --team ethics-project --name "QueryOptimizer" --task "Fix database indexing issues and optimize queries"
```

**Result:**
A new agent is spawned in a separate `tmux` window and joins the `ethics-project` team workspace.

---

## 📊 Scenario 5: Real-time Status Monitoring

**User Instruction (in Telegram):**
> "Give me a quick status update on the Web3 project. Who is blocked?"

**Telegram Bridge Action:**
The bridge runs:
```bash
claws task list web3-project --status blocked
```

**Bot Response:**
> "🔔 **Status for 'web3-project'**:
> - **Blocked Tasks**: 2
> - **Agent 'BlockWatcher'**: Currently waiting on the Smart Contract review."

---

## ✉️ Scenario 6: Proxy Messaging

**User Instruction (in Telegram):**
> "Tell the Lead Agent in the AI-ethics team to prioritize the 'Bias Detection' module."

**Telegram Bridge Action:**
The bridge translates this into an inbox message:
```bash
claws inbox send ai-ethics LeadAgent "Instruction from Human: Prioritize Bias Detection module" --from HumanCommander
```

---

## ⚙️ How it works under the hood

The `claws` Telegram orchestration relies on a **Bridge Agent** running a continuous loop that polls the Telegram Bot API or listens via a Webhook. 

1.  **Input**: The bot receives a message from an authorized user.
2.  **Parsing**: The message is passed to an LLM (running via OpenClaw) to extract the **Team**, **Action**, **Agent Name**, and **Task**.
3.  **Execution**: The bridge executes the appropriate `claws` command via a subprocess.
4.  **Feedback**: The `claws` CLI output is returned to the bot and posted back to the Telegram channel.

---

> [!TIP]
> Use the `.toml` templates for complex team setups. Tell the bot "Load template [filename]" for the most reliable results.
