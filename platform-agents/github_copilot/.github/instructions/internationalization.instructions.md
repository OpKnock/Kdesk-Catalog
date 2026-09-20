---
applyTo: "**/*.json **/*.r **/*.sh"
---

Localizes applications with gettext and i18next: extraction, translation catalogs, pluralization, and locale builds.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `xgettext -o locale/messages.pot src/**/*.js --keyword=_`, `npx i18next -c i18next-parser.config.js 'src/**/*.tsx'`
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

# Internationalization

Localize apps with the standard message catalog workflow.

## When to Use

- Shipping a product in multiple languages
- Centralizing user-facing strings for translators
- Handling plurals and dates correctly per locale

## gettext workflow

1. Extract:
```bash
xgettext -o locale/messages.pot src/**/*.js --keyword=_
```

2. Initialize a locale:
```bash
msginit -i locale/messages.pot -o locale/de/LC_MESSAGES/messages.po -l de
```

3. Translate (human or machine) then compile:
```bash
msgfmt -o locale/de/LC_MESSAGES/messages.mo locale/de/LC_MESSAGES/messages.po
```

4. Merge new strings:
```bash
msgmerge --update locale/de/LC_MESSAGES/messages.po locale/messages.pot
```

## Plurals

```po
msgid "%d item"
msgid_plural "%d items"
msgstr[0] "%d Element"
msgstr[1] "%d Elemente"
```

## i18next JSON catalogs

```bash
npx i18next 'src/**/*.tsx' --locales en,de,fr --defaultLocale en
```

Extract keys like `t('checkout.title')` into `locales/en/translation.json`.

## Best practices

- Never concatenate translated strings; use placeholders.
- Keep dates/numbers via Intl APIs, not string formats.
- Key by semantic id (checkout.title) or English source text consistently.
- Run extraction in CI and fail on missing translations for ship locales.

## Testing

```bash
msgfmt --check-format -o de.mo de.po
node -e "const {t}=require('./i18n'); t('checkout.title')" | grep -v checkout.title
```

A missing key must fail the build.

## Capabilities

### gettext
Extract and compile translations with GNU gettext tools.

**Parameters:**
- `keyword` (string): Translation function to extract
- `language` (string): Source language: Python, C, JavaScript
- `locale` (string): Target locale, e.g. de, fr_FR

**Commands:**
- `xgettext -o locale/messages.pot src/**/*.js --keyword=_`
- `msginit -i locale/messages.pot -o locale/de/LC_MESSAGES/messages.po -l de`
- `msgfmt -o locale/de/LC_MESSAGES/messages.mo locale/de/LC_MESSAGES/messages.po`
- `msgmerge --update locale/de/LC_MESSAGES/messages.po locale/messages.pot`
- `msguniq -o deduped.po locale/de/LC_MESSAGES/messages.po`

**Examples:**
- xgettext -o messages.pot src/**/*.py --keyword=_ --language=Python
- msgmerge --backup=off --update de.po messages.pot
- msgfmt --check-format -o de.mo de.po

### i18next
Manage JSON translation catalogs with i18next tooling.

**Parameters:**
- `locales` (string): Locale list to extract catalogs for
- `namespace` (string): i18next namespace name
- `config` (string): Parser config file

**Commands:**
- `npx i18next -c i18next-parser.config.js 'src/**/*.tsx'`
- `npx i18next 'src/**/*.tsx' --locales en,de,fr --defaultLocale en`
- `npm install i18next react-i18next i18next-browser-languagedetector`
- `npx lingui extract`
- `npx lingui compile`

**Examples:**
- npx i18next 'src/**/*.tsx' --locales en,de --output public/locales
- npx lingui extract --clean
- npx i18next --namespace translation --locales en,ja

## References
- [GNU gettext manual](https://www.gnu.org/software/gettext/manual/)
- [i18next](https://www.i18next.com/)
- [Lingui](https://lingui.dev/)
