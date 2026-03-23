# 🦞 Claw Collective: Seamless Agent Coordination

### "The definitive solution for scaling OpenClaw teams without the complexity."

In the rapidly evolving landscape of autonomous agents, the biggest bottleneck isn't intelligence—it's **coordination**. 

The OpenClaw community has built incredible agents, but until now, making them work together as a high-performance team was a manual, fragmented, and error-prone process. **`claws` changes that.**

We've consolidated 4 separate, complex repositories into one elegant, high-speed CLI. Whether you're running two agents or twenty, `claws` provides the unified "Command & Control" center your team deserves.

---

## 🔥 Why Claw Collective?

### 🧩 The Fragmentation Pain Point
Most OpenClaw users struggle with scattered state, manual sync scripts, and broken communication channels. Scaling a team often means hours of configuration and debugging.

### ✨ The Claw Collective Solution
*   **One CLI to Rule Them All**: Replace complex setups with a single `pip install`.
*   **The Golden Loop**: Our core innovation. A self-healing sync cycle (**PULL → LOCK → WORK → LOG → PUSH**) that ensures every agent is always on the same page.
*   **Telegram-Powered Orchestration**: The ultimate human-to-agent interface. Command your team and spawn new agents directly from **Telegram**—the natural bridge between human instruction and robotic execution.
*   **Plug-and-Play Orchestration**: Launch fully configured teams in seconds using TOML templates.
*   **Enterprise-Grade Security**: Built-in secret scanning prevents registry leaks before they happen.
*   **Real-time Intelligence**: Live terminal-based Kanban boards and a lightweight web dashboard.

---

## 🚀 Quick Start (From Zero to Team in 2 Minutes)

### 1. Installation
```bash
git clone https://github.com/weisenchen/claw-collective.git
cd claw-collective
pip install .
```

### 2. Launch Your Environment
```bash
claws init my-project
cd my-project
```

### 3. Join the Collective
```bash
export CLAWS_AGENT="Architect"
claws register
```

### 4. Deploy via Telegram
Command your collective from any device using natural language.

**Example Instruction:**
> "Create a new research team for the AI Ethics project. Spawn a Lead Agent and three Security Reviewers."

**Auto-Execution:**
The `claws` bridge automatically parses this and executes:
```bash
claws init ./ai-ethics
claws team create ethics-team --leader "LeadAgent"
claws spawn --team ethics-team --name "LeadAgent" --task "Initial architecture"
# ... spawning SecurityReviewers ...
```

*See also: [**Telegram Orchestration scenarios**](docs/TELEGRAM_ORCHESTRATION.md)*

---

## 📖 The library of Success

*   🤖 [**Agent Self-Setup**](docs/AGENT_SELF_SETUP.md): Empower your agents to join the team autonomously.
*   🔄 [**Workflow Examples**](docs/WORKFLOW_EXAMPLES.md): Master complex coordination patterns.
*   🗺️ [**Getting Started**](docs/GETTING_STARTED.md): The executive roadmap for new installations.
*   📜 [**Command Reference**](docs/COMMAND_REFERENCE.md): The full power of `claws` at your fingertips.

---

## 🛠️ Feature Set

| Feature           | Description                                                 |
| :---------------- | :---------------------------------------------------------- |
| **Telegram Sync** | Direct human-to-agent command pipeline via Telegram.        |
| **Sync Engine**   | Automated git-based shared state with conflict resolution.  |
| **A2A Protocol**  | Machine-to-machine agent communication (aiohttp).           |
| **Task Kanban**   | Full lifecycle task management with dependency tracking.    |
| **Isolation**     | Git worktree and tmux sandboxing for secure execution.      |
| **Registry**      | Auto-detecting agent directory for multi-machine discovery. |

---

> [!IMPORTANT]
> **Claw Collective** is more than a tool; it's a philosophy of collaborative intelligence. Stop managing agents. Start leading teams.

Built with 🦞 by the OpenClaw community.
