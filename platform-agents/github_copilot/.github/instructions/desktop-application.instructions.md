---
applyTo: "**/*.r **/*.sh **/*.{yaml,yml}"
---

Builds cross-platform desktop apps with Electron and Tauri: scaffolding, dev loops, and packaging.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `npm create electron-vite@latest my-app -- --template react`, `npm create tauri-app@latest`
- Check `knowledge` references and prerequisites before proceeding

### 2. Reason
Analyze and plan:
- Compare current state vs desired state (drift, checksums, policy)
- Evaluate trust, compatibility, and risk: use `kdesk trust` and `kdesk doctor` patterns
- Decide: which capabilities/tools are needed, which can be skipped

### 3. Act
Execute with guards:
- Run only `allowed-tools` (see frontmatter); use `safe_path` for writes
- Prefer `Bash` with explicit binaries (`curl`, `kubectl`, `kdesk`) over generic shell
- Record evidence: file paths, checksums, and tool outputs for verification

# Desktop Application

Builds cross-platform desktop apps: Electron for web-stack teams, Tauri for
small binaries.

## When to Use

- Creating a native-feeling app from web tech
- Packaging installers for Windows/macOS/Linux
- Debugging main/renderer process issues

## Real Commands

```bash
# Electron (electron-vite)
sudo npm create electron-vite@latest my-app -- --template react
sudo npm run dev
sudo npm run build

# Package
sudo npx electron-builder --win nsis
sudo npx electron-builder --mac dmg --arm64
sudo npx electron-builder --linux AppImage

# Tauri
sudo npm create tauri-app@latest
sudo npm run tauri dev
sudo npm run tauri build
sudo npm run tauri build -- --bundles msi
sudo npx tauri info
```

## electron-builder Config (electron-builder.yml)

```yaml
appId: com.example.app
productName: MyApp
files:
  - dist/**/*
win:
  target: nsis
mac:
  target: [dmg]
linux:
  target: [AppImage]
```

## Best Practices

- Keep the main process minimal; heavy work in renderer/workers
- Sign builds for distribution (notarization on macOS)
- Use contextIsolation and no nodeIntegration in renderers
- Set appId and version before first release
- Test installers on clean VMs/containers

## Example Response

Scaffolds the app, runs the dev loop, and packages the installer for the target
platform, reporting artifact paths and sizes.

## Capabilities

### electron-app
Scaffold, run, and package Electron desktop applications

**Parameters:**
- `template` (string): Scaffold template: react, vue, svelte, vanilla
- `config` (string): electron-builder config file
- `platform` (string): Target: --win, --mac, --linux

**Commands:**
- `npm create electron-vite@latest my-app -- --template react`
- `npm run dev`
- `npx electron-builder --win nsis`
- `npx electron-builder --mac dmg --arm64`
- `npm run build && npx electron-builder --linux AppImage`

**Examples:**
- npm run dev -- --host 0.0.0.0
- npx electron-builder --publish never --config electron-builder.yml
- npm run build:win

### tauri-app
Develop and build Tauri apps with a small footprint

**Parameters:**
- `bundles` (string): Installer bundles: msi, nsis, appimage, deb, dmg
- `debug` (boolean): Build debug or release mode
- `runner` (string): Custom runner script for tauri

**Commands:**
- `npm create tauri-app@latest`
- `npm run tauri dev`
- `npm run tauri build`
- `npx tauri info`
- `npm run tauri build -- --bundles msi`

**Examples:**
- npm run tauri dev -- --port 1420
- npm run tauri build -- --bundles nsis
- npx tauri icon app-icon.png

## References
- [Electron docs](https://www.electronjs.org/docs/latest/)
- [Tauri docs](https://tauri.app/)
- [electron-builder docs](https://www.electron.build/)
