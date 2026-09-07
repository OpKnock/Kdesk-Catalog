---
name: "mobile-testing"
description: "Tests mobile apps with Maestro flows, Appium, Detox, adb, and simctl across iOS and Android devices. Use when working with maestro, device tools, mobile or when the user mentions maestro, device tools, mobile."
license: "MIT"
compatibility: "Requires adb, maestro, xcrun."
metadata: {"author": "Kdesk", "version": "2.0.0", "category": "mobile"}
allowed-tools: "Glob Grep Read Bash(adb:*) Bash(maestro:*) Bash(xcrun:*)"
---

Tests mobile apps with Maestro flows, Appium, Detox, adb, and simctl across iOS and Android devices.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `maestro test flows/smoke.yaml`, `adb devices`
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

# Mobile Testing

Test real user journeys on devices and simulators.

## When to Use

- E2E coverage for critical mobile flows
- Regression testing across device sizes/OS versions
- Reproducing reported crashes

## Maestro flows

```yaml
appId: com.example.app
---
- launchApp
- tapOn: "Login"
- inputText: "user@example.com"
- tapOn: "Continue"
- assertVisible: "Orders"
```

```bash
maestro record login.yaml
maestro test flows/smoke.yaml
```

Flows are YAML - readable by QA and engineers alike.

## Emulator/simulator control

```bash
adb devices
adb shell input tap 540 960
xcrun simctl list devices available
xcrun simctl boot 'iPhone 15'
```

## Logs on failure

```bash
adb logcat -s TestRunner -v brief
xcrun simctl io 'iPhone 15' screenshot screen.png
```

Capture screenshots automatically in the failure handler.

## Strategy

- Smoke: launch + login + core journey per release.
- Critical: checkout, sync, auth - every PR.
- Full suite: nightly on the device matrix.

## Best practices

- Tag flows: critical, slow, broken-on-device.
- Use env vars for endpoints; never hardcode staging URLs.
- Keep flows idempotent (reset state first).
- Test on real devices weekly; simulators miss GPS/perf quirks.

## Testing

```bash
maestro test flows/ --include-tags=critical
```

Run the critical set in CI for every merge.

## Capabilities

### maestro
Author and run declarative mobile UI flows.

**Parameters:**
- `device` (string): Target device id
- `include-tags` (string): Only run flows with these tags
- `env` (string): Environment variables for flows

**Commands:**
- `maestro test flows/smoke.yaml`
- `maestro record flow.yaml`
- `maestro test --device 2 flows/checkout.yaml`
- `maestro studio`
- `maestro test flows/ --exclude-tags=slow`

**Examples:**
- maestro record --device=emulator-5554 login.yaml
- maestro test --include-tags=critical flows/
- maestro test --env APP_URL=https://staging.example.com flows/checkout.yaml

### device-tools
Control emulators and simulators with adb and simctl.

**Parameters:**
- `device` (string): Device or simulator name/id
- `command` (string): adb shell or simctl command
- `package` (string): Android package name

**Commands:**
- `adb devices`
- `adb shell input tap 540 960`
- `adb shell am start -n com.example.app/.MainActivity`
- `xcrun simctl list devices available`
- `xcrun simctl boot 'iPhone 15' && open -a Simulator`

**Examples:**
- adb install -r app-debug.apk
- adb logcat -s TestRunner -v brief
- xcrun simctl io 'iPhone 15' screenshot screen.png

## References
- [Maestro](https://maestro.mobile.dev/)
- [Appium](https://appium.io/docs/en/2.0/)
- [Detox](https://wix.github.io/Detox/)
