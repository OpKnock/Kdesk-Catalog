Develops iOS and Swift apps: SwiftPM packages, SwiftLint gates, swift-format, and xcodebuild CI builds.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `swift package init --type executable`, `xcodebuild -scheme MyApp -destination 'platform=iOS Simulato`
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

# Swift

Build iOS and Swift packages with SwiftPM and xcodebuild.

## When to Use

- iOS/macOS application development
- Reusable Swift libraries via SwiftPM
- CI builds, tests, and archives

## SwiftPM

```bash
swift package init --type executable
swift build
swift test --filter 'LoginTests'
```

## SwiftLint

```swift
// .swiftlint.yml
disabled_rules:
  - trailing_whitespace
opt_in_rules:
  - empty_count
  - force_unwrapping
```

```bash
swiftlint lint --strict
swiftlint --fix
```

Use `--strict` in CI to treat warnings as errors.

## swift-format

```bash
swift-format lint --strict --recursive Sources/
swift-format format --in-place --recursive Sources/
```

## xcodebuild in CI

```bash
xcodebuild -scheme MyApp -destination 'platform=iOS Simulator,name=iPhone 15' test
xcodebuild -scheme MyApp -archivePath build/MyApp.xcarchive archive
```

Export the archive with an options plist for signing in CI.

## Best practices

- Commit Package.resolved for reproducible builds.
- Gate on swiftlint --strict and swift-format lint.
- Parallelize tests with --parallel on fast machines.
- Use Xcode cloud or runner pools with simulator caching.

## Testing

```bash
swift test --parallel
swiftlint lint --strict
```

Run unit tests and lint in CI on every PR.

## Capabilities

### swiftpm
Create and manage Swift packages.

**Parameters:**
- `type` (string): executable, library, or empty package
- `filter` (string): Test name filter
- `parallel` (string): Run tests in parallel

**Commands:**
- `swift package init --type executable`
- `swift build`
- `swift test --filter 'LoginTests'`
- `swift run my-tool --help`
- `swift package resolve`

**Examples:**
- swift package init --type library
- swift test --parallel
- swift run my-tool config.json

### xcodebuild
Build and test iOS apps in CI.

**Parameters:**
- `scheme` (string): Xcode scheme name
- `destination` (string): Simulator or device destination
- `archivePath` (string): Archive output path

**Commands:**
- `xcodebuild -scheme MyApp -destination 'platform=iOS Simulator,name=iPhone 15' build`
- `xcodebuild test -scheme MyApp -destination 'platform=iOS Simulator,name=iPhone 15'`
- `xcodebuild -scheme MyApp -archivePath build/MyApp.xcarchive archive`
- `xcodebuild -exportArchive -archivePath build/MyApp.xcarchive -exportPath dist -exportOptionsPlist ExportOptions.plist`
- `xcodebuild -list`

**Examples:**
- xcodebuild -scheme MyApp -destination 'platform=iOS Simulator,name=iPhone 15,OS=18.0' test
- xcodebuild -scheme MyApp archive -archivePath build/MyApp.xcarchive
- xcodebuild -project MyApp.xcodeproj -scheme MyApp -showBuildSettings | grep PRODUCT_BUNDLE_IDENTIFIER

## References
- [Swift Docs](https://www.swift.org/documentation/)
- [SwiftLint](https://github.com/realm/SwiftLint)
- [xcodebuild manual](https://manpagez.com/man/1/xcodebuild/)