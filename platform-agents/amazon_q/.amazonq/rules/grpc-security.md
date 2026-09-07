Secure gRPC communication: TLS/mTLS with generated certificates, grpcurl client auth flags, authorization interceptors, and channel credentials in Go.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `openssl req -x509 -newkey rsa:2048 -nodes -keyout ca.key -ou`
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

# gRPC Security

Secure gRPC endpoints with TLS, mutual TLS, and authorization interceptors.

## What this skill does

- Generates CA, server, and client certificates for gRPC TLS.
- Configures server-side TLS and client channel credentials.
- Verifies encrypted gRPC connections with grpcurl and openssl s_client.
- Enforces authz via interceptors on the server.

## When to use

- gRPC traffic crosses network boundaries and must be encrypted.
- Compliance requires mutual TLS between microservices.
- Auditing which services speak TLS (openssl s_client check).

## Real commands

```bash
# Generate a CA and server cert for localhost
openssl req -x509 -newkey rsa:2048 -nodes -keyout ca.key -out ca.crt -days 365 -subj "/CN=my-ca"
openssl req -newkey rsa:2048 -nodes -keyout server.key -out server.csr -subj "/CN=localhost"
openssl x509 -req -in server.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out server.crt -days 365

# Probe a TLS-enabled server
grpcurl -cacert ca.crt -servername localhost localhost:50051 list

# mTLS client
grpcurl -cacert ca.crt -cert client.pem -key client.key -servername localhost localhost:50051 list

# Skip verification (dev only)
grpcurl -insecure localhost:50051 list
```

## Go server TLS

```go
creds, _ := credentials.NewServerTLSFromFile("server.crt", "server.key")
s := grpc.NewServer(grpc.Creds(creds))
```

## Go client TLS

```go
creds, _ := credentials.NewClientTLSFromFile("ca.crt", "localhost")
conn, _ := grpc.NewClient("localhost:50051", grpc.WithTransportCredentials(creds))
```

## Authz interceptor

```go
func authzInterceptor(ctx context.Context, req any, info *grpc.UnaryServerInfo, handler grpc.UnaryHandler) (any, error) {
    md, ok := metadata.FromIncomingContext(ctx)
    if !ok || len(md.Get("authorization")) == 0 {
        return nil, status.Error(codes.Unauthenticated, "missing token")
    }
    return handler(ctx, req)
}
```

## Testing

```bash
# Verify cipher + protocol over the wire
openssl s_client -connect localhost:50051 -servername localhost -tls1_2 2>/dev/null | grep -E "Protocol|Cipher"
```

## Best practices

- Never use `-insecure` or insecure credentials outside dev.
- Set `-servername` to the cert CN to avoid hostname mismatch errors.
- Rotate CA keys and reissue server certs on a schedule.
- Use interceptors for authz, never trust the client to be honest.

## Example exchange

```
User: grpcurl says "certificate signed by unknown authority".
Agent: Pass the CA bundle: grpcurl -cacert ca.crt -servername localhost localhost:50051 list
```

## Capabilities

### grpc-tls-mtls
Configure TLS and mutual TLS for gRPC servers and clients, and verify with grpcurl.

**Parameters:**
- `ca_cert` (string): Path to the CA certificate for server verification.
- `client_cert` (string): Client certificate for mTLS.
- `client_key` (string): Client private key for mTLS.

**Commands:**
- `openssl req -x509 -newkey rsa:2048 -nodes -keyout ca.key -out ca.crt -days 365 -subj "/CN=my-ca"`
- `openssl req -newkey rsa:2048 -nodes -keyout server.key -out server.csr -subj "/CN=localhost"`
- `grpcurl -cacert ca.crt -cert client.pem -key client.key -servername localhost -authority localhost localhost:50051 list`
- `grpcurl -insecure localhost:50051 list`
- `openssl s_client -connect localhost:50051 -servername localhost -tls1_2 2>/dev/null | grep -E "Protocol|Cipher"`

**Examples:**
- grpcurl -cacert ca.crt localhost:50051 helloworld.Greeter/SayHello -d '{"name":"tls"}'
- grpcurl -insecure -plaintext false localhost:50051 list
- openssl x509 -in server.crt -noout -text | grep -A1 "Subject Alternative"

## References
- [gRPC Auth Guide](https://grpc.io/docs/guides/auth/)
- [grpcurl TLS options](https://github.com/fullstorydev/grpcurl#using-grpcurl-with-tls)