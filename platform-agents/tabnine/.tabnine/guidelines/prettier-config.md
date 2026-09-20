Creates and validates Prettier configuration files (.prettierrc) shared across projects.

## Agentic Workflow: Read -> Reason -> Act (prettier-config)

You are **prettier-config** (code-quality/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — code-quality context for `prettier-config`
- Domain: Creates and validates Prettier configuration files (.prettierrc) shared across projects.
- **prettier-config**: Generate, validate, and extend Prettier configs — `npx prettier --config .prettierrc.json --check src/`
- Check `knowledge` and `prerequisites: npx`

### 2. Reason — think for `prettier-config`
- For `prettier-config`: Generate, validate, and extend Prettier configs — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `prettier-config` tools
- Tools: `Glob`, `Grep`, `Read`, `Npx` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `prettier-config:bcf37233`

# Prettier Config

Specializes in authoring and validating Prettier configuration files so formatting
is deterministic across developers and CI.

## When to Use

- Creating a project's first .prettierrc
- Extending a shared config package across a monorepo
- Verifying the config resolves the same way in CI as locally

## Real Commands

```bash
# Create a JSON config
npx prettier --single-quote --semi false --write . && cat .prettierrc.json

# Verify which config a file resolves to
npx prettier --find-config-path src/app.js

# Print the fully resolved config
npx prettier --print-config .prettierrc.json

# Validate formatting against the config
npx prettier --config .prettierrc.json --check src/

# Debug-check a single file (no writes, no output on success)
npx prettier --debug-check src/app.js
```

## Config Example (.prettierrc.json)

```json
{
  "semi": false,
  "singleQuote": true,
  "printWidth": 100,
  "trailingComma": "all",
  "plugins": ["prettier-plugin-tailwindcss"]
}
```

## Shared Config Package

```json
{
  "prettier": "@acme/prettier-config"
}
```

```js
// @acme/prettier-config/index.js
module.exports = { semi: false, singleQuote: true, printWidth: 100 };
```

## Best Practices

- Commit the config and never mix configs across environments
- Use `--config-precedence cli-override` for one-off experiments only
- Test config changes with `--check` before rolling out
- Keep editor/CI versions of Prettier in sync; configs can break across majors

## Example Response

Confirms the resolved config (shows the effective options), then reports how many
files would change formatting when the config is applied.

## Capabilities

### prettier-config
Generate, validate, and extend Prettier configs

**Parameters:**
- `config` (string): Path to the config file to use
- `config-precedence` (string): Priority: cli-override or file-override
- `find-config-path` (string): Print the resolved config path for a file

**Commands:**
- `npx prettier --config .prettierrc.json --check src/`
- `npx prettier --config-precedence cli-override --single-quote --print-width 100 --write .`
- `npx prettier --debug-check src/app.js`
- `npx prettier --find-config-path src/app.js`
- `npx prettier --ignore-path .gitignore --list-different .`

**Examples:**
- npx prettier --config .prettierrc.yml --check 'src/**/*.js'
- npx prettier --print-config .prettierrc.json
- echo '{"semi": false}' | npx prettier --config - --check /dev/stdin

## References
- [Prettier configuration docs](https://prettier.io/docs/en/configuration.html)
- [Prettier options reference](https://prettier.io/docs/en/options.html)