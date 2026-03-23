# Implementation Plan: Rebranding to Claw Collective

Total transformation of the project from `octeam` to **Claw Collective**, including a new CLI command `claws`.

## Proposed Changes

### Core Package
- **[MODIFY] [Rename Folder]** `octeam/` -> `claws/`
- **[MODIFY] All Python Files**: Update `import octeam` to `import claws`.
- **[MODIFY] [pyproject.toml](file:///home/wei/projects/openclaw-team-workspace/workspace/code/octeam/pyproject.toml)**: Update name and script entry point to `claws`.

### Branding & Documentation
- **[MODIFY] [README.md](file:///home/wei/projects/openclaw-team-workspace/workspace/code/octeam/README.md)**: Replace all "octeam" mentions with "Claw Collective" and the `claws` command.
- **[MODIFY] All Docs**: Update `docs/*.md` to reflect the new branding.
- **[NEW] [Banner]**: Regenerate the project banner with "Claw Collective" text.

### Infrastructure
- **[MODIFY] [bootstrap.sh](file:///home/wei/projects/openclaw-team-workspace/workspace/code/octeam/scripts/bootstrap.sh)**: Update to use `claws` command.

## Verification Plan
- Run `claws --help` to verify CLI registration.
- Verify all documentation links are functional.
- Ensure all imports are correctly updated.
