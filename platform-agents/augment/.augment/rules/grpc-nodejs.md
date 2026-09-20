---
type: agent_requested
description: "gRPC services and clients in Node.js with @grpc/grpc-js and @grpc/proto-loader: dynamic proto loading, streaming RPCs, and grpc_tools_node_protoc codegen."
---

# Grpc Nodejs

gRPC services and clients in Node.js with @grpc/grpc-js and @grpc/proto-loader: dynamic proto loading, streaming RPCs, and grpc_tools_node_protoc codegen.

## Instructions

# gRPC Node.js

gRPC services and clients in Node with @grpc/grpc-js.

## What this skill does

- Loads .proto files at runtime with @grpc/proto-loader (no build step needed).
- Implements unary and streaming RPC handlers.
- Generates static JS stubs with grpc_tools_node_protoc when preferred.
- Configures channels: deadlines, keepalive, and interceptors.

## When to use

- A Node microservice needs internal typed RPC calls.
- Prototype gRPC APIs quickly without a codegen pipeline.
- Building gateway workers that fan out to gRPC services.

## Real commands

```bash
# Install
npm install @grpc/grpc-js @grpc/proto-loader
npm install -D grpc-tools

# Dynamic loading (no codegen) is the default pattern
node server.js &
node client.js

# Optional static codegen
./node_modules/.bin/grpc_tools_node_protoc -I ./proto \
  --js_out=import_style=commonjs:./generated --grpc_out=./generated ./proto/greet.proto
```

## Server skeleton

```js
const grpc = require('@grpc/grpc-js');
const protoLoader = require('@grpc/proto-loader');
const pkgDef = protoLoader.loadSync('./proto/greet.proto');
const greet = grpc.loadPackageDefinition(pkgDef).helloworld;

const server = new grpc.Server();
server.addService(greet.Greeter.service, {
  sayHello: (call, callback) => callback(null, { message: 'Hello ' + call.request.name })
});
server.bindAsync('0.0.0.0:50051', grpc.ServerCredentials.createInsecure(), () => server.start());
```

## Client skeleton

```js
const client = new greet.Greeter('localhost:50051', grpc.credentials.createInsecure(), {
  'grpc.keepalive_time_ms': 10000
});
client.sayHello({ name: 'Node' }, (err, res) => console.log(res.message));
```

## Testing

```bash
node server.js &
grpcurl -plaintext -d '{"name":"Node"}' localhost:50051 helloworld.Greeter/SayHello
node client.js
```

## Best practices

- Use dynamic loading for dev velocity, static stubs for strict typing in TS.
- Always `server.tryShutdown()` on SIGTERM for a clean drain.
- Set `grpc.keepalive_time_ms` on channels behind load balancers.
- Proto-loader `keepCase:false` (default) camelCases field names; keep it consistent client-side.

## Example exchange

```
User: My Node client times out after the server restarts.
Agent: Create a new channel on reconnect and set a deadline per call:
       client.sayHello(req, { deadline: Date.now() + 5000 }, cb)
```

## Capabilities

### nodejs-grpc
Load proto definitions dynamically and implement gRPC servers/clients in Node.js.

**Commands:**
- `npm install @grpc/grpc-js @grpc/proto-loader`
- `npm install -D grpc-tools`
- `./node_modules/.bin/grpc_tools_node_protoc -I ./proto --js_out=import_style=commonjs:./generated --grpc_out=./generated ./proto/greet.proto`
- `node server.js`
- `node client.js`

**Examples:**
- node server.js & node client.js
- npm run proto:gen && node server.js
- node --inspect server.js