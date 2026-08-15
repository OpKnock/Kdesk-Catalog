# Changelog

All notable changes to kdesk.

## [1.1.0] - 2026-08-14

### Added
- Installer lifecycle CLI commands: `kdesk uninstall`, `kdesk drift`,
  `kdesk status`, `kdesk rollback`.
- `kdesk install --home <dir>` for `~`-prefixed / `--target home` installs.
- Exit-code semantics: `0` success, `1` fatal error, `2` usage error,
  `3` problems found (drift not clean, workflow validation problems,
  audit findings).
- Phase H end-to-end tests: emission -> install -> doctor -> drift ->
  uninstall chain; persisted runtime runs via `RuntimeStore`; approval and
  validation/retry gates; real subagent delegation through a compiled
  `claude.exe` shim plus honest failure when the CLI is missing.
- Phase I CLI tests for the installer lifecycle and exit codes.

### Changed
- `kdesk install` destinations and manifest now use the install-time
  `--base`; manifest keys are install-target-relative posix paths;
  backups keyed by manifest key digest.
- `uninstall` prunes empty directories left behind.
- Audit commands (`security`, `quality`, `license`, `duplicates`,
  `provenance`) and `workflow --validate` now exit `3` when problems are
  found instead of `1`.

### Removed
- None.

## [1.0.0] - Initial release

- Universal agent/skill/workflow registry with stats, graph, resolvers,
  workflow engine, execution layer, runtime, adapters (emission +
  runtime contracts), doctor, transactional installer, and CLI.
