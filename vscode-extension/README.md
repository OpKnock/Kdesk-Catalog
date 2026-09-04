# Kdesk Catalog — VS Code Extension

Browse 3,093 AI agents & skills, diagnose projects, and convert to 45 platforms without leaving VS Code.

## Install (dev)

```bash
cd vscode-extension
npx vsce package   # or: code --install-extension kdesk-catalog-1.1.0.vsix
```

## Setup

1. Set `kdesk.pythonPath` to the Python with Kdesk importable (or install: `pip install -e <repo>[dev]`).
2. Set `kdesk.repoRoot` to your `Kdesk-Catalog` checkout (defaults to the open workspace folder).

## Commands

| Command | What it does |
|---------|--------------|
| Kdesk: Search Agents & Skills | quickpick search over the catalog, inserts a reference |
| Kdesk: Insert Agent Reference at Cursor | search → insert markdown reference |
| Kdesk: Diagnose This Project | `doctor --mode diagnose` on the workspace, report in Output → Kdesk |
| Kdesk: Show Catalog Stats | definition/platform counts |
| Kdesk: Convert Catalog to Platform… | multi-pick platforms → runs the converter |
| Kdesk: Open Dashboard | opens the local web UI (`kdesk serve`) |

The sidebar **Kdesk** view shows live counts plus one-click actions.
