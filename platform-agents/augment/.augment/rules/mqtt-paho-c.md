---
type: agent_requested
description: "Build C applications with the Eclipse Paho MQTT C library: synchronous/async clients, samples, and CMake builds. Use when working with paho c build, api or when the user mentions paho c build, api."
---

Build C applications with the Eclipse Paho MQTT C library: synchronous/async clients, samples, and CMake builds.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `git clone https://github.com/eclipse/paho.mqtt.c.git`
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

# Paho MQTT C

The Eclipse Paho C library provides synchronous (MQTTClient) and asynchronous (MQTTAsync) MQTT clients.

## What this skill does

- Builds the library and samples from source with CMake
- Runs the provided sample clients
- Links applications against libpaho-mqtt3c / libpaho-mqtt3as

## When to use

- Embedding MQTT into C daemons or embedded devices
- Preferring zero-dependency sync/async C APIs

## Real commands

```bash
# Clone and build
 git clone https://github.com/eclipse/paho.mqtt.c.git
cd paho.mqtt.c
cmake -Bbuild -DPAHO_WITH_SSL=ON -DPAHO_BUILD_SAMPLES=ON
cmake --build build
ctest --test-dir build

# Run samples (needs a broker)
./build/output/samples/MQTTClient_publish -t test/topic -m "hello"
./build/output/samples/MQTTClient_subscribe -t test/topic -q 1

# Compile your own app
 gcc app.c -o app -lpaho-mqtt3c
```

## Minimal sample logic

```c
MQTTClient client;
MQTTClient_create(&client, "tcp://localhost:1883", "client-id", MQTTCLIENT_PERSISTENCE_NONE, NULL);
MQTTClient_connect(client, &conn_opts);
MQTTClient_publishMessage(client, "test/topic", &msg, &token);
MQTTClient_destroy(&client);
```

## Best practices

- Use MQTTAsync for non-blocking event-driven apps
- Enable SSL build if you need TLS (`-DPAHO_WITH_SSL=ON`)
- Always set a client ID; use clean sessions with persistent sessions deliberately

## Capabilities

### paho-c-build
Clone, build and run Paho MQTT C samples (MQTTClient/MQTTAsync) with the CMake toolchain.

**Parameters:**
- `sample` (string): Sample binary: MQTTClient_publish, MQTTClient_subscribe, MQTTAsync_publish
- `topic` (string): Topic to publish/subscribe to
- `qos` (integer): QoS level for the sample

**Commands:**
- `git clone https://github.com/eclipse/paho.mqtt.c.git`
- `cmake -Bbuild -DPAHO_WITH_SSL=ON`
- `cmake --build build`
- `ctest --test-dir build`
- `./build/output/samples/MQTTClient_publish -t test/topic -m "hello"`

**Examples:**
- cmake -Bbuild -DPAHO_BUILD_SAMPLES=ON -DPAHO_WITH_SSL=ON
- ./build/output/samples/MQTTClient_subscribe -t test/topic -q 1
- gcc app.c -o app -lpaho-mqtt3c -lpaho-mqtt3as

## References
- [Paho MQTT C repo](https://github.com/eclipse/paho.mqtt.c)
- [Paho C samples](https://github.com/eclipse/paho.mqtt.c/tree/master/src/samples)