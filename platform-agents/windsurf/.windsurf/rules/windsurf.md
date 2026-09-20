---
trigger: glob
description: "Operates the Windsurf editor with Cascade AI: global rules, memories, CLI launch flags, and project configuration."
globs: ["**/*.r", "**/*.sh"]
---

# Windsurf

Operates the Windsurf editor with Cascade AI: global rules, memories, CLI launch flags, and project configuration.

## Instructions

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
