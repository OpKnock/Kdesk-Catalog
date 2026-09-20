---
name: "game-development"
description: "Builds games with Godot and Unity headless pipelines: project export, automated builds, and CI artifact generation. Use when working with godot, unity or when the user mentions godot, unity."
license: "MIT"
compatibility: "Requires unity, unreal, godot, phaser, pixi."
metadata: {"author": "Kdesk", "version": "2.0.0", "category": "gaming"}
allowed-tools: "Glob Grep Read Bash(godot:*) Bash(unity-editor:*)"
---

Builds games with Godot and Unity headless pipelines: project export, automated builds, and CI artifact generation.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `godot --headless --path project/ --import`, `unity-editor -batchmode -quit -projectPath . -executeMethod `
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

# Game Development

Automate Godot and Unity game builds with headless CLI pipelines.

## When to Use

- Setting up CI builds for game projects
- Running automated tests without an editor session
- Producing release artifacts for multiple platforms

## Godot headless

First, import assets so the export cache is warm:

```bash
godot --headless --path project/ --import
```

Run GDScript tests:

```bash
godot --headless --path project/ --script res://tests/run_tests.gd
```

Export for platforms:

```bash
godot --headless --path project/ --export-release 'Windows Desktop' build/game.exe
godot --headless --path project/ --export-release 'Web' dist/index.html
```

## Unity batch mode

```bash
unity-editor -batchmode -quit -projectPath . -executeMethod BuildScript.PerformBuild -logFile build.log
unity-editor -batchmode -quit -runTests -testPlatform PlayMode -testResults results.xml
```

Sample BuildScript:

```csharp
public static class BuildScript
{
    public static void PerformBuild()
    {
        BuildPipeline.BuildPlayer(new[] { "Assets/Scenes/Main.unity" },
            "build/game.exe", BuildTarget.StandaloneWindows64, BuildOptions.None);
    }
}
```

## CI considerations

- Use a license-free batch mode on Linux agents with the nographics flag.
- Cache Godot import files and Unity Library/ folders between runs.
- Store signed keystores in CI secrets, never in the repo.

## Best practices

- Version export presets in the repo.
- Test on the platform you ship: mobile builds need device smoke tests.
- Keep scene asset import deterministic by running --import first.

## Testing

Run unit (GDScript / EditMode) and PlayMode suites in CI and gate merges on results.

## Capabilities

### godot
Run Godot headless for imports, tests, and exports.

**Parameters:**
- `headless` (string): Run without a window (CI mode)
- `export-release` (string): Export preset name and output path
- `script` (string): GDScript entry point to run

**Commands:**
- `godot --headless --path project/ --import`
- `godot --headless --path project/ --script res://tests/run_tests.gd`
- `godot --headless --path project/ --export-release 'Windows Desktop' build/game.exe`
- `godot --headless --path project/ --export-pack 'Linux' build/game.pck`
- `godot --headless --path project/ --quit-after 5`

**Examples:**
- godot --headless --path ./game --import && godot --headless --path ./game --export-release 'Web' dist/index.html
- godot --headless --path ./game --script res://tests/run_tests.gd --verbose
- godot --headless --path ./game --export-debug 'Linux' build/game.x86_64

### unity
Drive Unity builds and test runs from the command line.

**Parameters:**
- `batchmode` (string): Run without editor UI for CI
- `buildTarget` (string): Android, WebGL, StandaloneWindows64, etc.
- `executeMethod` (string): Static build method to invoke

**Commands:**
- `unity-editor -batchmode -quit -projectPath . -executeMethod BuildScript.PerformBuild`
- `unity-editor -batchmode -quit -runTests -testPlatform PlayMode -testResults results.xml`
- `unity-editor -batchmode -quit -projectPath . -buildTarget Android -outputPath build/app.apk`
- `unity-editor -batchmode -quit -logFile build.log -executeMethod BuildScript.AndroidBuild`
- `unity-editor -batchmode -quit -projectPath . -deleteLibrary`

**Examples:**
- unity-editor -batchmode -quit -projectPath . -buildTarget WebGL -outputPath build/web
- unity-editor -batchmode -quit -runTests -testPlatform EditMode -testResults edit.xml
- unity-editor -batchmode -quit -projectPath . -executeMethod BuildScript.PerformBuild -nographics

## References
- [Godot Docs](https://docs.godotengine.org/en/stable/tutorials/editor/command_line_tutorial.html)
- [Unity command line arguments](https://docs.unity3d.com/Manual/CommandLineArguments.html)
- [Godot Export](https://docs.godotengine.org/en/stable/tutorials/export/exporting_projects.html)
