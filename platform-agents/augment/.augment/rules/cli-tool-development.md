---
type: agent_requested
description: "Develops command-line tools with Commander, Click, and cobra: argument parsing, subcommands, help text, and distribution."
---

# cli-tool-development

Develops command-line tools with Commander, Click, and cobra: argument parsing, subcommands, help text, and distribution.

## Instructions

# CLI Tool Development

Build polished command-line tools.

## When to Use

- Internal developer tooling and automation
- Wrappers around APIs and services
- Scripts that need args, flags, and subcommands
- Tools distributed to other teams or users

## Commands

```bash
# Node with Commander
npm init -y
npm install commander
node bin/mycli.js --help

# Python with Click
pip install click
python -m mycli --help

# Go with Cobra
go install github.com/spf13/cobra-cli@latest
cobra-cli init mycli
cobra-cli add serve
go run ./cmd/mycli --help

# Global install for dev
npm link
```

## Python Click Example

```python
import click

@click.command()
@click.option("--name", default="World", help="Who to greet")
@click.option("--verbose", is_flag=True)
def greet(name, verbose):
    """Greet someone."""
    if verbose:
        click.echo("verbose mode")
    click.echo(f"Hello, {name}!")

if __name__ == "__main__":
    greet()
```

## Best Practices

- Always provide --help and --version
- Exit with non-zero codes and messages on stderr for errors
- Make flags idempotent and composable for piping
- Test with golden fixtures and snapshot tests
- Support CI environments (no TTY, no color when piped)
- Document each flag; the help text is the docs

## Capabilities

### cli-scaffolding
Scaffold CLI tools in Node, Python, and Go.

**Commands:**
- `npm install commander`
- `npm init -y && npm pkg set bin="./bin/mycli.js"`
- `python -m pip install click`
- `go install github.com/spf13/cobra-cli@latest`
- `cobra-cli init mycli`

**Examples:**
- cobra-cli add serve
- npm install oclif
- pip install typer

### cli-verification
Test and verify CLI behavior.

**Commands:**
- `node bin/mycli.js --help`
- `python -m mycli --version`
- `go run ./cmd/mycli --help`
- `npm link`
- `echo "test input" | mycli parse`

**Examples:**
- mycli --help | head -40
- mycli greet --name World
- mycli --version