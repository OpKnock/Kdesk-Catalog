---
name: "webassembly-deployment"
description: "Build, validate, optimize, and run WebAssembly modules and components with wasmtime, wasm-tools, and wasm-opt. Use when working with Run WebAssembly with wasmtime, Validate and inspect modules with wasm tools, Optimize binaries with wasm opt or when the user mentions Run WebAssembly with wasmtime, Validate and inspect modules with wasm tools, Optimize binaries with wasm opt."
globs: ["**/*.go", "**/*.r", "**/*.rs"]
alwaysApply: false
---

Build, validate, optimize, and run WebAssembly modules and components with wasmtime, wasm-tools, and wasm-opt.

## Agentic Workflow: Read -> Reason -> Act (webassembly-deployment)

You are **webassembly-deployment** (backend) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — backend context for `webassembly-deployment`
- Domain: Build, validate, optimize, and run WebAssembly modules and components with wasmtime, wasm-tools, and wasm-opt.
- **Run WebAssembly with wasmtime**: Execute wasm modules and WASI apps locally, serve modules over HTTP, and compile ahead-of-time for f — `wasmtime run hello.wasm`
- **Validate and inspect modules with wasm-tools**: Check wasm binary validity, pretty-print internals, and build components from core modules. — `wasm-tools validate module.wasm`
- **Optimize binaries with wasm-opt**: Shrink and speed up wasm binaries, strip debug info, and produce deployment-ready artifacts. — `wasm-opt -O3 -o app.opt.wasm app.wasm`
- Check `knowledge` and `prerequisites: rust, wasm-pack, wasmtime, emsdk`

### 2. Reason — think for `webassembly-deployment`
- For `Run WebAssembly with wasmtime`: Execute wasm modules and WASI apps locally, serve modules over HTTP, and compile ahead-of-time for fast starts. — decide which checks to run
- For `Validate and inspect modules with wasm-tools`: Check wasm binary validity, pretty-print internals, and build components from core modules. — decide which checks to run
- For `Optimize binaries with wasm-opt`: Shrink and speed up wasm binaries, strip debug info, and produce deployment-ready artifacts. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `webassembly-deployment` tools
- Tools: `Glob`, `Grep`, `Read`, `Wasmtime`, `Wasm-tools` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `webassembly-deployment:5d9a2b7d`

# WebAssembly Deployment

Package, verify, optimize, and operate WebAssembly modules and components in production.

## When to Use

- Edge compute: run untrusted plugins at the edge with sandboxing
- Function-as-a-service runtimes with fast cold starts
- Plugins and extensions compiled once, run anywhere (browser, server, edge)
- Sandboxing third-party code where OS isolation is too heavy

## Build and Sign Pipeline

1. Compile source to wasm (Rust with cargo wasm32-wasip2, C with clang --target=wasm32-wasi).
2. Validate: wasm-tools validate must pass; keep the WAT human-readable copy for reviews.
3. Optimize: wasm-opt with -Os for size or -O3 for speed; strip debug info for prod.
4. Wrap into components when composing interfaces (component model).
5. Sign the artifact and pin the toolchain version in CI for reproducible builds.

## Runtime Policy

- Grant capabilities explicitly: filesystem via --dir, env via --env, network via wasi-http or explicit sockets.
- Deny by default; start with zero capabilities and add only what the module needs.
- Set explicit timeouts and memory limits at the runtime level.

## Serving and Scaling

- wasmtime serve hosts HTTP in-process; scale horizontally behind a load balancer.
- Precompile (.cwasm) at build time to avoid JIT compilation on cold start.
- Cache module artifacts by content hash; invalidate on source change.

## Debugging and Observability

- Enable WASI logging to stdout and forward structured logs.
- Use --wasm-trace or module instrumentation for panic reproduction.
- Compare behavior across runtimes (wasmtime vs wasmer vs browser) before promising portability.

## Common Pitfalls

- Forgetting to adapt WASI preview1 modules to preview2 interfaces.
- Shipping debug symbols to production.
- Over-granting filesystem access with --dir .::.
- Assuming a module is deterministic across runtimes without testing.

## Rollout Checklist

- Module validated and size-bounded
- Capability manifest reviewed
- Cold-start latency measured
- Canary deployed with metrics comparison
- Rollback path: pinned previous artifact hash

## Capabilities

### Run WebAssembly with wasmtime
Execute wasm modules and WASI apps locally, serve modules over HTTP, and compile ahead-of-time for fast starts.

**Parameters:**
- `invoke` (string): Name of the exported function to call (reactor modules).
- `dir` (string): Directory mapping to grant the module filesystem access, e.g. --dir .::.

**Commands:**
- `wasmtime run hello.wasm`
- `wasmtime run --invoke add -- --x 2 --y 3 math.wasm`
- `wasmtime serve --addr 127.0.0.1:8080 --enable-wasi server.wasm`
- `wasmtime compile -o hello.cwasm hello.wasm`
- `wasmtime run --dir .::. --env FOO=bar hello.wasm`

**Examples:**
- wasmtime run --invoke add -- --x 2 --y 3 math.wasm
- wasmtime serve --addr 127.0.0.1:8080 --enable-wasi server.wasm

### Validate and inspect modules with wasm-tools
Check wasm binary validity, pretty-print internals, and build components from core modules.

**Parameters:**
- `adapt` (string): WASI preview1 adapter module used when wrapping a core module into a component.
- `output` (string): Output file path for component wrapping or parse conversion.

**Commands:**
- `wasm-tools validate module.wasm`
- `wasm-tools print module.wasm | head -50`
- `wasm-tools component new module.wasm -o component.wasm --adapt wasi_snapshot_preview1.reactor.wasm`
- `wasm-tools wit component.wasm`
- `wasm-tools parse module.wat -o module.wasm`

**Examples:**
- wasm-tools validate module.wasm
- wasm-tools component new module.wasm -o component.wasm --adapt wasi_snapshot_preview1.reactor.wasm

### Optimize binaries with wasm-opt
Shrink and speed up wasm binaries, strip debug info, and produce deployment-ready artifacts.

**Parameters:**
- `optimization level` (string): -O0 to -O4 or -Os; -O3 maximizes speed, -Os minimizes size.
- `strip-debug` (flag): Remove the debug name section and DWARF info to reduce size.

**Commands:**
- `wasm-opt -O3 -o app.opt.wasm app.wasm`
- `wasm-opt -Os --strip-debug -o app.min.wasm app.wasm`
- `wasm-opt --enable-bulk-memory --enable-mutable-globals -O2 -o app.modern.wasm app.wasm`
- `wasm-opt --metrics app.wasm`

**Examples:**
- wasm-opt -Os --strip-debug -o app.min.wasm app.wasm
- wasm-opt --metrics app.wasm

## References
- [](https://docs.wasmtime.dev/)
- [](https://github.com/bytecodealliance/wasm-tools)
- [](https://github.com/WebAssembly/binaryen)
- [](https://webassembly.org/)