Use ConnectRPC in browser and TypeScript clients: @connectrpc/connect-web with buf-generated stubs.

## Agentic Workflow: Read -> Reason -> Act (connectrpc-web)

You are **Connectrpc Web** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `connectrpc-web`
- Domain: Use ConnectRPC in browser and TypeScript clients: @connectrpc/connect-web with buf-generated stubs.
- **web-client**: Create a TypeScript ConnectRPC web client and generate stubs with buf — `npm create vite@latest my-app -- --template react-ts`
- **browser-call**: Invoke Connect services from the browser with CORS and unary streaming support — `npm run dev`
- Check `knowledge` and `prerequisites: npm, npx`

### 2. Reason — think for `connectrpc-web`
- For `web-client`: Create a TypeScript ConnectRPC web client and generate stubs with buf — decide which checks to run
- For `browser-call`: Invoke Connect services from the browser with CORS and unary streaming support — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `connectrpc-web` tools
- Tools: `Glob`, `Grep`, `Read`, `Bash`, `Npx` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `connectrpc-web:cf026064`

# ConnectRPC Web

Call ConnectRPC services from browsers and TypeScript apps.

## When to Use

- Building SPAs that talk to Connect/gRPC backends
- Sharing proto-generated types between frontend and backend
- Streaming updates in the browser

## Scaffold

```bash
npm create vite@latest my-app -- --template react-ts
cd my-app
npm install @connectrpc/connect-web @connectrpc/connect
```

## buf.gen.yaml

```yaml
version: v2
plugins:
  - local: protoc-gen-es
    out: src/gen
    opt: target=ts
  - local: protoc-gen-connect-es
    out: src/gen
    opt: target=ts
```

```bash
npx buf generate
```

## Client Code

```ts
import { createClient } from "@connectrpc/connect";
import { createConnectTransport } from "@connectrpc/connect-web";
import { GreetService } from "./gen/greet/v1/greet_connect";

const transport = createConnectTransport({ baseUrl: "http://localhost:8080" });
const client = createClient(GreetService, transport);

const res = await client.greet({ name: "alice" });
console.log(res.greeting);
```

```bash
npm run dev
```

## CORS

The server must send Access-Control-Allow-Origin for the dev origin, or browser calls fail preflight.

## Build

```bash
npm run build
npm run preview
npx tsc --noEmit
```

## Testing

```bash
curl -s -o /dev/null -w "%{http_code}\n" http://localhost:5173
```

## Best Practices

- Generate stubs from the same proto as the backend
- Set up Vite proxy in dev to avoid CORS issues
- Use createGrpcWebTransport for gRPC-Web endpoints
- Enable streaming for long-lived subscriptions
- Pin generated files with buf lock

## Capabilities

### web-client
Create a TypeScript ConnectRPC web client and generate stubs with buf

**Parameters:**
- `app_name` (string): Vite app name
- `template` (string): Vite template such as react-ts, vue-ts

**Commands:**
- `npm create vite@latest my-app -- --template react-ts`
- `npm install @connectrpc/connect-web @connectrpc/connect`
- `npx buf generate`
- `npm run dev -- --host 0.0.0.0`

**Examples:**
- npm create vite@latest my-app -- --template react-ts && npm install @connectrpc/connect-web @connectrpc/connect
- npx buf generate
- npm run build

### browser-call
Invoke Connect services from the browser with CORS and unary streaming support

**Parameters:**
- `dev_port` (string): Vite dev server port, default 5173

**Commands:**
- `npm run dev`
- `npm run build`
- `npm run preview`
- `curl -s -o /dev/null -w "%{http_code}" http://localhost:5173`
- `npx vite --port 5173 --strictPort`

**Examples:**
- npm run dev
- npm run build && npm run preview
- npx tsc --noEmit

## References
- [ConnectRPC Web Getting Started](https://connectrpc.com/docs/web/getting-started)
- [buf es plugin](https://buf.build/docs/ecosystem/es-plugins/)