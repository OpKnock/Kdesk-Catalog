---
type: agent_requested
description: "Develops cross-platform mobile apps with Flutter and React Native/Expo: scaffolding, builds, and device deployments. Use when working with flutter, react native or when the user mentions flutter, react native."
---

Develops cross-platform mobile apps with Flutter and React Native/Expo: scaffolding, builds, and device deployments.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `flutter create my_app --org com.example`, `npx create-expo-app@latest my-app --template blank-typescrip`
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

# Mobile App Development

Ship cross-platform apps with Flutter or React Native.

## When to Use

- One codebase for iOS + Android
- Fast prototyping with hot reload
- Teams without deep native specialization

## Flutter

```bash
flutter create my_app --org com.example
flutter pub get
flutter analyze --fatal-infos
flutter test
```

## Flutter builds

```bash
flutter build apk --release
flutter build ipa --release --export-method ad-hoc
```

## Expo (React Native)

```bash
npx create-expo-app@latest my-app --template blank-typescript
npx expo start
npx expo prebuild
```

## EAS builds

```bash
eas build --platform android --profile preview
eas build --platform ios --profile production
```

EAS runs cloud builds with correct signing.

## Framework decision

- Flutter: pixel-consistent UI, strong perf, Dart.
- React Native: JS ecosystem reuse, OTA updates via Expo.
- Evaluate plugin coverage before committing.

## Best practices

- Run flutter analyze and tests in CI.
- Pin SDK versions and lockfiles.
- Test on physical devices before release - emulators miss edge cases.
- Use device farms (Firebase/EAS) for the device matrix.

## Testing

```bash
flutter analyze --fatal-infos && flutter test
```

Both must pass on every merge.

## Capabilities

### flutter
Create, build, and test Flutter applications.

**Parameters:**
- `platforms` (string): Target platforms android,ios,web,linux...
- `fatal-infos` (string): Fail analyze on info-level issues
- `build-mode` (string): debug, profile, or release

**Commands:**
- `flutter create my_app --org com.example`
- `flutter pub get`
- `flutter analyze`
- `flutter test`
- `flutter build apk --release`

**Examples:**
- flutter create my_app --platforms android,ios
- flutter analyze --fatal-infos
- flutter build ipa --release --export-method ad-hoc

### react-native
Scaffold and run React Native apps with Expo.

**Parameters:**
- `template` (string): Expo template name
- `tunnel` (string): Expo dev over the internet
- `profile` (string): EAS build profile: preview, development, production

**Commands:**
- `npx create-expo-app@latest my-app --template blank-typescript`
- `npx expo start`
- `npx expo prebuild`
- `npx expo export --platform android`
- `eas build --platform android --profile preview`

**Examples:**
- npx create-expo-app@latest my-app --template tabs
- npx expo start --tunnel
- eas build --platform ios --profile production

## References
- [Flutter Docs](https://docs.flutter.dev/)
- [Expo Docs](https://docs.expo.dev/)
- [React Native](https://reactnative.dev/docs/getting-started)