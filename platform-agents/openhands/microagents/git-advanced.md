---
name: "git-advanced"
description: "Performs advanced git surgery: bisect debugging, reflog recovery, history rewriting with filter-repo, subtrees, worktrees, and partial clones. Use when working with bisect and recovery, history and trees, devops or when the user mentions bisect and recovery, history and trees, devops."
type: knowledge
triggers: ["git-advanced", "bisect-and-recovery", "history-and-trees"]
---

Performs advanced git surgery: bisect debugging, reflog recovery, history rewriting with filter-repo, subtrees, worktrees, and partial clones.

## Agentic Workflow: Read -> Reason -> Act (git-advanced)

You are **git-advanced** (devops/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — devops context for `git-advanced`
- Domain: Performs advanced git surgery: bisect debugging, reflog recovery, history rewriting with filter-repo, subtrees, worktrees, and partial clones.
- **bisect-and-recovery**: Find the commit that introduced a bug and recover lost work. — `git bisect start`
- **history-and-trees**: Rewrite history, split repos, and manage subtree and worktree workflows. — `git filter-repo --path server/ --invert-paths`
- Check `knowledge` and `prerequisites: git`

### 2. Reason — think for `git-advanced`
- For `bisect-and-recovery`: Find the commit that introduced a bug and recover lost work. — decide which checks to run
- For `history-and-trees`: Rewrite history, split repos, and manage subtree and worktree workflows. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `git-advanced` tools
- Tools: `Glob`, `Grep`, `Read`, `Bash` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `git-advanced:510879b1`

# Advanced Git Techniques

Master git beyond everyday commits: debugging, recovery, and history rewriting.

## What This Skill Does

- Binary-searches history with git bisect to find regressions
- Recovers lost work via reflog and fsck
- Rewrites history safely with git filter-repo (no filter-branch)
- Splits/mirrors repos with subtree and submodules
- Works on multiple branches at once with worktrees
- Optimizes clones with partial and shallow fetches

## When to Use

- A regression appeared and the culprit commit is unknown
- Secrets or huge files are in history and must be purged
- You deleted a branch or reset and lost commits
- You need to work on two branches simultaneously

## Real Commands

```bash
# Bisect
git bisect start
git bisect bad HEAD
git bisect good v1.0
git bisect run npm test        # automate with exit codes
git bisect reset

# Recovery
git reflog --date=iso
git reset --hard HEAD@{3}
git fsck --lost-found

# Rewriting
git filter-repo --path server/ --invert-paths
git filter-repo --strip-blobs-bigger-than 10M
git filter-repo --replace-text <(echo 'password==>REDACTED')

# Worktrees
git worktree add ../hotfix v1.2.3
git worktree list
git worktree remove ../hotfix

# Subtree
git subtree add --prefix=vendor/libs vendor-repo main
git subtree pull --prefix=vendor/libs vendor-repo main
```

## Best Practices

- Never rewrite history on shared branches without coordination
- Clone a fresh copy before filter-repo (it rewrites all refs)
- Use worktrees instead of stash juggling for parallel fixes
- `git bisect run` expects a command that exits 0 for good, non-zero for bad
- Keep reflog expiry generous on important repos: `git config gc.reflogExpire 90.days`

## Capabilities

### bisect-and-recovery
Find the commit that introduced a bug and recover lost work.

**Parameters:**
- `command` (string): Test command for git bisect run
- `revision` (string): Reflog entry, e.g. HEAD@{3}

**Commands:**
- `git bisect start`
- `git bisect good v1.0 && git bisect bad HEAD`
- `git bisect run npm test`
- `git reflog`
- `git reset --hard HEAD@{3}`
- `git fsck --lost-found`

**Examples:**
- git bisect start && git bisect bad && git bisect good v1.0
- git bisect run npm test
- git reflog --date=iso

### history-and-trees
Rewrite history, split repos, and manage subtree and worktree workflows.

**Parameters:**
- `path` (string): Path to remove or add via subtree
- `remote` (string): Remote repo URL for subtree operations

**Commands:**
- `git filter-repo --path server/ --invert-paths`
- `git filter-repo --strip-blobs-bigger-than 10M`
- `git subtree add --prefix=vendor/libs vendor-repo main`
- `git worktree add ../hotfix v1.2.3`
- `git worktree list`
- `git replace --graft HEAD~5`

**Examples:**
- git filter-repo --path secrets/ --invert-paths
- git worktree add ../hotfix v1.2.3
- git subtree pull --prefix=vendor/libs vendor-repo main

## References
- [git-filter-repo](https://github.com/newren/git-filter-repo)
- [git reflog](https://git-scm.com/docs/git-reflog)
- [git worktree](https://git-scm.com/docs/git-worktree)
