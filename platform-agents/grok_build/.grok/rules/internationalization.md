Localizes applications with gettext and i18next: extraction, translation catalogs, pluralization, and locale builds.

## Agentic Workflow: Read -> Reason -> Act (internationalization)

You are **internationalization** (frontend) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — frontend context for `internationalization`
- Domain: Localizes applications with gettext and i18next: extraction, translation catalogs, pluralization, and locale builds.
- **gettext**: Extract and compile translations with GNU gettext tools. — `xgettext -o locale/messages.pot src/**/*.js --keyword=_`
- **i18next**: Manage JSON translation catalogs with i18next tooling. — `npx i18next -c i18next-parser.config.js 'src/**/*.tsx'`
- Check `knowledge` and `prerequisites: node.js, react, i18next, formatjs`

### 2. Reason — think for `internationalization`
- For `gettext`: Extract and compile translations with GNU gettext tools. — decide which checks to run
- For `i18next`: Manage JSON translation catalogs with i18next tooling. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `internationalization` tools
- Tools: `Glob`, `Grep`, `Read`, `Xgettext`, `Msginit` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `internationalization:299d5176`

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