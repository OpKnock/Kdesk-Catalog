---
name: "grpc-web"
description: "gRPC-Web for browser clients: protoc-gen-grpc-web codegen, grpc-web npm client, and Envoy proxy configuration to bridge HTTP/1.1 browsers to HTTP/2 gRPC. Use when working with grpc web bridge, api or when the user mentions grpc web bridge, api."
license: "MIT"
compatibility: "Requires chmod, envoy, npm, protoc. Needs network access."
metadata: {"author": "Kdesk", "version": "2.0.0", "category": "api"}
allowed-tools: "Glob Grep Read Bash(chmod:*) Bash(curl:*) Bash(envoy:*) Bash(npm:*) Bash(protoc:*)"
---

gRPC-Web for browser clients: protoc-gen-grpc-web codegen, grpc-web npm client, and Envoy proxy configuration to bridge HTTP/1.1 browsers to HTTP/2 gRPC.

## Agentic Workflow: Read -> Reason -> Act (grpc-web)

You are **Grpc Web** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `grpc-web`
- Domain: gRPC-Web for browser clients: protoc-gen-grpc-web codegen, grpc-web npm client, and Envoy proxy configuration to bridge HTTP/1.1 browsers to HTTP/2 gRPC.
- **grpc-web-bridge**: Generate grpc-web JS stubs and proxy browser traffic to gRPC backends with Envoy. — `curl -L -o protoc-gen-grpc-web https://github.com/grpc/grpc-web/releases/downloa`
- Check `knowledge` and `prerequisites: chmod, envoy, npm, protoc`

### 2. Reason — think for `grpc-web`
- For `grpc-web-bridge`: Generate grpc-web JS stubs and proxy browser traffic to gRPC backends with Envoy. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `grpc-web` tools
- Tools: `Glob`, `Grep`, `Read`, `Bash`, `Chmod` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `grpc-web:ce543973`

# gRPC-Web

Expose gRPC services to browser clients over gRPC-Web.

## What this skill does

- Generates JS/TS gRPC-Web stubs from proto files.
- Bridges browser HTTP/1.1 calls to gRPC backends with Envoy.
- Explains grpcwebtext vs grpcweb wire modes.
- Debugs the proxy path with curl.

## When to use

- A web frontend must call a gRPC backend directly.
- You want to drop a REST layer between browser and backend.
- Evaluating gRPC-Web vs REST for a new SPA.

## Real commands

```bash
# Install the protoc plugin (pick platform release)
curl -L -o protoc-gen-grpc-web https://github.com/grpc/grpc-web/releases/download/1.5.0/protoc-gen-grpc-web-1.5.0-linux-x86_64
chmod +x protoc-gen-grpc-web

# Generate JS stubs
protoc --plugin=protoc-gen-grpc-web=$(pwd)/protoc-gen-grpc-web \
  --js_out=import_style=commonjs:. \
  --grpc-web_out=import_style=commonjs,mode=grpcwebtext:. helloworld.proto

# Client deps
npm install google-protobuf grpc-web

# Run the Envoy proxy
envoy -c envoy.yaml
```

## Envoy config (minimal)

```yaml
static_resources:
  listeners:
    - name: browser_listener
      address: { socket_address: { address: 0.0.0.0, port_value: 8080 } }
      filter_chains:
        - filters:
            - name: envoy.filters.network.http_connection_manager
              typed_config:
                "@type": type.googleapis.com/envoy.extensions.filters.network.http_connection_manager.v3.HttpConnectionManager
                codec_type: AUTO
                stat_prefix: grpc_web
                route_config:
                  virtual_hosts:
                    - name: grpc
                      domains: ["*"]
                      routes:
                        - match: { prefix: "/" }
                          route:
                            cluster: grpc_backend
                            timeout: 5s
                http_filters:
                  - name: envoy.filters.http.grpc_web
                  - name: envoy.filters.http.router
  clusters:
    - name: grpc_backend
      type: STRICT_DNS
      typed_extension_protocol_options:
        envoy.extensions.upstreams.http.v3.HttpProtocolOptions:
          "@type": type.googleapis.com/envoy.extensions.upstreams.http.v3.HttpProtocolOptions
          explicit_http_config:
            http2_protocol_options: {}
      load_assignment:
        cluster_name: grpc_backend
        endpoints:
          - lb_endpoints:
              - endpoint:
                  address: { socket_address: { address: localhost, port_value: 50051 } }
```

## Browser client

```js
const client = new GreeterClient('http://localhost:8080', null, null);
client.sayHello({ name: 'Web' }, (err, resp) => console.log(resp.message));
```

## Testing

```bash
# The proxy should answer on the browser port (may return 415 for bare GET - that is expected without grpc-accept)
curl -s -X POST -H "Content-Type: application/grpc-web-text" \
  -H "X-Grpc-Web: 1" http://localhost:8080/helloworld.Greeter/SayHello --data-binary @payload
```

## Best practices

- Use mode=grpcwebtext for debuggable base64 traffic; grpcweb binary is smaller.
- Always place the grpc_web filter before the router filter in Envoy.
- Envoy must talk HTTP/2 upstream; gRPC-Web to gRPC needs the grpc-web filter only on the browser side.
- Keep protoc plugin and npm grpc-web versions compatible.

## Example exchange

```
User: Browser requests fail with 405 from the proxy.
Agent: Verify Envoy's grpc_web filter is configured before router and upstream is HTTP/2.
```

## Capabilities

### grpc-web-bridge
Generate grpc-web JS stubs and proxy browser traffic to gRPC backends with Envoy.

**Parameters:**
- `import_style` (string): JS import style: commonjs, commonjs+dts, typescript.
- `mode` (string): Wire format: grpcwebtext (default) or grpcweb (binary).
- `envoy_config` (string): Path to the Envoy config bridging the browser port to the gRPC upstream.

**Commands:**
- `curl -L -o protoc-gen-grpc-web https://github.com/grpc/grpc-web/releases/download/1.5.0/protoc-gen-grpc-web-1.5.0-linux-x86_64`
- `chmod +x protoc-gen-grpc-web`
- `protoc --plugin=protoc-gen-grpc-web=$(pwd)/protoc-gen-grpc-web --js_out=import_style=commonjs:. --grpc-web_out=import_style=commonjs,mode=grpcwebtext:. helloworld.proto`
- `npm install grpc-web`
- `envoy -c envoy.yaml`

**Examples:**
- protoc --plugin=protoc-gen-grpc-web=$(pwd)/protoc-gen-grpc-web --js_out=import_style=commonjs:. --grpc-web_out=import_style=commonjs,mode=grpcwebtext:. helloworld.proto
- npm install google-protobuf grpc-web
- curl -I http://localhost:8080/helloworld.Greeter/SayHello

## References
- [gRPC-Web Basics](https://grpc.io/docs/platforms/web/basics/)
- [grpc-web GitHub](https://github.com/grpc/grpc-web)
