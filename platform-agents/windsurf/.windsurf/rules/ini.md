---
trigger: glob
description: "Parse and modify INI configuration files with Python configparser and shell tools. Covers section lookups, value extraction, validation, and in-place updates."
globs: ["**/*.py", "**/*.r", "**/*.sh"]
---

# INI

Parse and modify INI configuration files with Python configparser and shell tools. Covers section lookups, value extraction, validation, and in-place updates.

## Instructions

# INI Files

Read and modify INI configuration files safely.

## What this skill does
50:   
- Parses sections and options with Python configparser.
- Extracts values with shell one-liners for51:    quick checks.
- Writes back changes preserving structure.
- Detects duplicate keys and malformed52:    lines.

## When to use

- Configuring legacy tools and services that use INI files.
- Auditing53:    which settings an app will load.
- Batch-editing configs across many hosts.

## Real commands
54:   
```bash
# Read one value
python3 -c "import configparser; c=configparser.ConfigParser(); c.read('app.ini');55:    print(c['database']['host'])"

# Validate the file parses
python3 -m configparser app.ini

56:   # List sections
python3 -c "import configparser; c=configparser.ConfigParser(); c.read('app.ini');57:    print(c.sections())"

# Shell one-liner for a section block
grep -A5 '^\[database\]' app.ini
58:   
# Update a value in place
python3 - <<'EOF'
import configparser
c = configparser.ConfigParser()
59:   c.read('app.ini')
c['database']['port'] = '5433'
with open('app.ini', 'w') as f:
    c.write(f)
60:   EOF
```

## Example file

```ini
[server]
host = 0.0.0.0
port = 8080

[database]
host = db.internal
61:   port = 5432
user = app
```

## Testing

```bash
python3 -m configparser app.ini && echo "valid"62:   
```

## Best practices

- Back up the file before in-place writes (`cp app.ini app.ini.bak`).
63:   - Use interpolation-aware escaping when values contain % characters.
- Prefer configparser over regex64:    edits to preserve comments and order.
- Validate with `python3 -m configparser` in CI before deploy.
65:   
## Example exchange

```
User: What port is the app configured to use?
Agent: python3 -c "import66:    configparser; c=configparser.ConfigParser(); c.read('app.ini'); print(c['server']['port'])"
```

## Capabilities

### ini-parsing
Read, validate, and modify INI files with Python and shell tools.

**Commands:**
- `python3 -c "import configparser; c=configparser.ConfigParser(); c.read('app.ini'); print(c['database']['host'])"`
- `python3 -m configparser app.ini`
- `awk -F= '/^\[database\]/{s=1;next} /^\[/{s=0} s && /host/{print $2}' app.ini`
- `grep -A5 '^\[database\]' app.ini`
- `python3 -c "import configparser; c=configparser.ConfigParser(); c.read('app.ini'); c['database']['port']='5433'; with open('app.ini','w') as f: c.write(f)"`

**Examples:**
- awk -F= '/^host=/{print $2}' config.ini
- python3 -c "import configparser; c=configparser.ConfigParser(); c.read('app.ini'); print(c.sections())"
- grep -c '^\[' app.ini
