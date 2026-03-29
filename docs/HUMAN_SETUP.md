# Scenario 3: Setup by Human (Manual Setup)

The standard manual setup for developers and team leads.

## 🦞 Installation

1. **Clone the Collective**:
   ```bash
   git clone https://github.com/weisenchen/claw-collective.git
   cd claw-collective
   ```

2. **Run Bootstrap**:
   ```bash
   ./scripts/bootstrap.sh
   source .venv/bin/activate
   ```

## 🏗️ Workspace Setup (Team Lead)

1. **Initialize Workspace**:
   ```bash
   claws init my-project --github
   cd my-project
   ```

2. **Register**:
   ```bash
   claws register --role Leader --name Lead-Agent
   ```

3. **Create Team & Tasks**:
   ```bash
   claws team create alpha-team --leader Lead-Agent
   claws task add alpha-team "Design API" --owner Lead-Agent
   ```

## 🔗 Joining a Team (Worker)

1. **Clone & Enter**:
   ```bash
   git clone <remote-url>
   cd project-folder
   ```

2. **Register & Sync**:
   ```bash
   claws register --role Worker --name Worker-1
   claws sync pull
   ```

3. **Start Working**:
   ```bash
   claws task start alpha-team <task-id> --owner Worker-1
   ```

---
*See also: [**Full Command Reference**](COMMAND_REFERENCE.md)*
