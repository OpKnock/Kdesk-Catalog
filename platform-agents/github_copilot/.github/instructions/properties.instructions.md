---
applyTo: "**/*.java **/*.py **/*.r **/*.sh **/*.sql"
---

# Properties

Java properties files: parsing, editing, encoding conversions (native2ascii), and config management in apps.

## Instructions

# Properties

Java .properties files configure JVM apps: key=value pairs with ISO-8859-1 default encoding.

## What this skill does

- Locates and edits keys safely
- Converts encodings with native2ascii
- Parses files for automation

## When to use

- Config changes in Java services
- Localizing message bundles

## Real commands

```bash
# Find keys
 grep -n 'db.url' application.properties
 grep -n -E '^(server|db)\.' application.properties

# Edit in place
 sed -i 's/^db.url=.*/db.url=jdbc:mysql:\/\/localhost:3306\/app/' application.properties
 sed -i 's/^app.mode=dev/app.mode=prod/' application.properties

# Encoding conversion
 native2ascii -encoding UTF-8 messages_zh.properties messages_zh_escaped.properties

# Parse programmatically
 python3 -c "import configparser; c=configparser.ConfigParser(); c.read('application.properties'); print(dict(c['default']))"
```

## Escaping rules

- `\` escapes special characters
- Unicode as \uXXXX sequences
- Continue long values with trailing backslash

## Best practices

- Keep secrets out of properties; use env vars
- Use native2ascii for non-Latin message bundles
- Validate with `java -jar -Dconfig.file=... app.jar` smoke tests

## Capabilities

### properties-management
Inspect, edit and convert Java .properties files including encoding with native2ascii.

**Commands:**
- `grep -n 'db.url' application.properties`
- `sed -i 's/^db.url=.*/db.url=jdbc:mysql://localhost:3306/app/' application.properties`
- `native2ascii -encoding UTF-8 input.properties output.properties`
- `python3 -c "import configparser; c=configparser.ConfigParser(); c.read('application.properties'); print(dict(c['default']))"`
- `java -XshowSettings:properties -version`

**Examples:**
- grep -n -E '^(server|db)\.' application.properties
- sed -i 's/^app.mode=dev/app.mode=prod/' application.properties
- native2ascii -encoding UTF-8 messages_zh.properties messages_zh_escaped.properties
