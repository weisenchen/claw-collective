#!/usr/bin/env bash
# octeam bootstrapper: automate setup for OpenClaw agents.
#
# Usage:
#   # For the Lead machine (creates workspace):
#   ./bootstrap.sh --role Leader --name Lead-Agent --workspace ./project-x --remote https://github.com/my-org/project-x.git
#
#   # For Worker machines (joins workspace):
#   ./bootstrap.sh --role Worker --name Worker-01 --remote https://github.com/my-org/project-x.git

set -e

# --- Default Values ---
ROLE="Worker"
NAME="$(hostname)"
WORKSPACE=""
REMOTE=""
INSTALL_DIR="$(pwd)/octeam"

# --- Parse Arguments ---
while [[ "$#" -gt 0 ]]; do
    case $1 in
        --role) ROLE="$2"; shift ;;
        --name) NAME="$2"; shift ;;
        --workspace) WORKSPACE="$2"; shift ;;
        --remote) REMOTE="$2"; shift ;;
        *) echo "Unknown parameter passed: $1"; exit 1 ;;
    esac
    shift
done

echo "🦞 octeam | Starting automated setup for agent: $NAME ($ROLE)"

# 1. Install/Update octeam dependencies
if [ ! -f "pyproject.toml" ]; then
    echo "❌ Error: bootstrap.sh must be run from the octeam project root."
    exit 1
fi

echo "📦 Installing octeam..."
pip3 install -e . --quiet

# 2. Check for octeam command
if ! command -v octeam &> /dev/null; then
    echo "⚠️ Warning: 'octeam' command not found in PATH."
    # Try running via python module as fallback
    COMMAND="python3 -m octeam.cli"
else
    COMMAND="octeam"
fi

# 3. Setup Workspace
if [ "$ROLE" == "Leader" ]; then
    if [ -z "$WORKSPACE" ]; then
        echo "❌ Error: --workspace is required for Leader role."
        exit 1
    fi
    echo "🏗️ Initializing workspace at $WORKSPACE..."
    $COMMAND init "$WORKSPACE" --remote "$REMOTE"
    cd "$WORKSPACE"
else
    if [ -z "$REMOTE" ]; then
        echo "❌ Error: --remote is required for Worker role to join."
        exit 1
    fi
    WS_DIR="$(basename "$REMOTE" .git)"
    if [ ! -d "$WS_DIR" ]; then
        echo "🔗 Joining workspace from $REMOTE..."
        git clone "$REMOTE" "$WS_DIR"
    fi
    cd "$WS_DIR"
fi

# 4. Register
echo "📋 Registering agent..."
$COMMAND register --role "$ROLE" --name "$NAME"

# 5. Final Status
echo "✅ Setup complete for $NAME!"
echo "Status:"
$COMMAND team list || echo "Note: No teams created yet."
