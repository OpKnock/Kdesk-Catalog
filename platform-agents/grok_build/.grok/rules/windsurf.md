Operates the Windsurf editor with Cascade AI: global rules, memories, CLI launch flags, and project configuration.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `windsurf .`, `windsurf --rules ~/.windsurf/rules`
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

# Windsurf Editor Operations

Work with the Windsurf editor and its Cascade AI assistant.

## What This Skill Does

- Launches the editor at projects and files
- Opens multifolder workspaces
- Configures Cascade rules and memories
- Manages global vs project rules
- Uses diff/CLI flags for focused sessions

## When to Use

- Setting up Windsurf for a repository
- Configuring Cascade behavior for a team
- CLI-driven editor workflows

## Real Commands

```bash
# Launch
windsurf .
windsurf ~/projects/app
windsurf --multifolder ~/projects/a ~/projects/b
windsurf --diff src/main.ts
windsurf --help

# Cascade config
windsurf --rules ~/.windsurf/rules
windsurf --memories ~/.windsurf/memories
windsurf --global-rules
windsurf --dev
windsurf --no-session-restore
```

## Cascade Rules Layout

```
.windsurf/
  rules/
    global_rules.md      # always-on guidance
    project_rules.md     # repo-specific guidance
  memories/              # persisted context
```

## Best Practices

- Commit .windsurf/rules to the repo for team consistency
- Keep global rules for personal preferences, project rules for standards
- Use memories for frequently reused context
- Pair --diff with staged files for review workflows
- Test rule changes with a fresh session (--no-session-restore)

## Capabilities

### editor-launch
Launch Windsurf with project paths and window options.

**Parameters:**
- `path` (string): Project directory or file
- `multifolder` (boolean): Open multiple folders

**Commands:**
- `windsurf .`
- `windsurf ~/projects/app`
- `windsurf --multifolder ~/projects/a ~/projects/b`
- `windsurf --diff src/main.ts`
- `windsurf --help`

**Examples:**
- windsurf .
- windsurf --diff src/main.ts
- windsurf --multifolder ~/projects/a ~/projects/b

### cascade-configuration
Configure Cascade AI rules, memories, and model settings.

**Parameters:**
- `rules-dir` (string): Directory with Cascade rule files
- `memories-dir` (string): Directory with Cascade memories

**Commands:**
- `windsurf --rules ~/.windsurf/rules`
- `windsurf --memories ~/.windsurf/memories`
- `windsurf --global-rules`
- `windsurf --dev`
- `windsurf --no-session-restore`

**Examples:**
- windsurf --rules ~/.windsurf/rules
- windsurf --memories ~/.windsurf/memories
- windsurf --dev

## References
- [Windsurf Documentation](https://docs.windsurf.com/)
- [Windsurf Blog](https://windsurf.com/blog)