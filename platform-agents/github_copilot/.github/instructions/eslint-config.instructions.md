---
applyTo: "**/*.java **/*.r **/*.sh **/*.{js,ts,jsx,tsx} **/*.{ts,tsx}"
---

# eslint-config

Designs and maintains ESLint flat configs and shareable config packages with rulesets, overrides, and presets.

## Instructions

# ESLint Config

Design and maintain ESLint configuration.

## When to Use

- Setting up linting for new or existing JS/TS projects
- Building shareable config packages
- Migrating .eslintrc to flat config
- Tuning rules for a codebase

## Flat Config Example

```javascript
// eslint.config.js
import js from "@eslint/js";
import tseslint from "typescript-eslint";

export default tseslint.config(
  { ignores: ["dist/**", "coverage/**"] },
  js.configs.recommended,
  ...tseslint.configs.recommended,
  {
    rules: {
      semi: ["error", "always"],
      "@typescript-eslint/no-explicit-any": "warn",
    },
  }
);
```

## Commands

```bash
npm install --save-dev eslint @eslint/js typescript-eslint

# Debug what config applies
npx eslint --print-config src/main.js
npx eslint --debug src/

# Environment info
npx eslint --env-info

# Rule experiments
npx eslint --rule "semi: [error, never]" src/
```

## Best Practices

- Start from recommended presets; add rules deliberately
- Use overrides for test files (globals, rules)
- Keep ignores in config, not scattered .eslintignore
- Test config changes with --print-config in CI
- Ship shareable configs as packages with semver
- Run npx eslint --debug to diagnose config merging

## Capabilities

### eslint-config-authoring
Author flat config and legacy config files.

**Commands:**
- `npm install --save-dev eslint @eslint/js typescript-eslint`
- `npx eslint --init`
- `npx eslint --print-config src/main.js`
- `npx eslint --debug src/`
- `npx eslint --env-info`

**Examples:**
- npx eslint --print-config src/main.js | python -m json.tool | head -60
- npx eslint --config eslint.config.js src/
- npm install --save-dev eslint-plugin-react eslint-plugin-react-hooks

### config-testing
Validate configs and lint output.

**Commands:**
- `npx eslint --rule "semi: [error, never]" src/`
- `npx eslint --rulesdir ./custom-rules src/`
- `npx eslint --no-eslintrc --env browser src/`
- `npx eslint --ext .js,.ts src/`

**Examples:**
- npx eslint --rule "quotes: [error, single]" src/
- npx eslint --no-eslintrc --config base.js src/
