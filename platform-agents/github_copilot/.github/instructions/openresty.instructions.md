---
applyTo: "**/*.json **/*.r **/*.sh"
---

Writes and tests Lua handlers using the resty CLI, manages lua-resty modules with luarocks, and configures nginx-Lua request processing at the edge.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `openresty -t`
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

# OpenResty

OpenResty bundles nginx with LuaJIT so you can script request handling at the edge.

## What this skill does

- Runs and tests nginx-Lua configs
- Uses the resty CLI for quick Lua experiments
- Installs lua-resty libraries

## When to use

- Edge logic: auth, rate limits, request transforms
- Dynamic routing without full services

## Real commands

```bash
# Validate and reload
openresty -t
openresty -s reload

# Quick Lua experiments
resty -e 'ngx.say(ngx.var.request_uri)'
resty -e 'local cjson = require("cjson"); ngx.say(cjson.encode({a=1}))'

# Libraries
luarocks install lua-resty-http
luarocks install lua-resty-redis
```

## In nginx.conf

```nginx
server {
    listen 8080;
    location /hello {
        content_by_lua_block {
            ngx.say("hello, ", ngx.var.arg_name or "world")
        }
    }
}
```

## Best practices

- Test logic with resty before wiring into nginx
- Use lua-resty modules instead of raw ngx APIs when possible
- Keep Lua code in .lua files loaded with `lua_package_path`

## Capabilities

### openresty-lua
Write and test Lua handlers for OpenResty and manage Lua modules with luarocks.

**Parameters:**
- `lua_code` (string): Inline Lua code to run with resty
- `rock` (string): lua-resty module name for luarocks
- `config` (string): nginx config path

**Commands:**
- `openresty -t`
- `openresty -s reload`
- `resty -e 'ngx.say(ngx.var.request_uri)'`
- `luarocks install lua-resty-http`
- `openresty -p /usr/local/openresty/nginx/ -c nginx.conf`

**Examples:**
- resty -e 'local cjson = require("cjson"); ngx.say(cjson.encode({a=1}))'
- luarocks install lua-resty-redis
- openresty -t && openresty -s reload

## References
- [OpenResty Official Site](https://openresty.org/en/)
- [OpenResty Lua Guide](https://github.com/openresty/lua-nginx-module)
