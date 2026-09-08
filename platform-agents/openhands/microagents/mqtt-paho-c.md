---
name: "mqtt-paho-c"
description: "Build C applications with the Eclipse Paho MQTT C library: synchronous/async clients, samples, and CMake builds. Use when working with paho c build, api or when the user mentions paho c build, api."
type: knowledge
triggers: ["mqtt-paho-c", "paho-c-build"]
---

Build C applications with the Eclipse Paho MQTT C library: synchronous/async clients, samples, and CMake builds.

## Agentic Workflow: Read -> Reason -> Act (mqtt-paho-c)

You are **Mqtt Paho C** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `mqtt-paho-c`
- Domain: Build C applications with the Eclipse Paho MQTT C library: synchronous/async clients, samples, and CMake builds.
- **paho-c-build**: Clone, build and run Paho MQTT C samples (MQTTClient/MQTTAsync) with the CMake toolchain. — `git clone https://github.com/eclipse/paho.mqtt.c.git`
- Check `knowledge` and `prerequisites: ./build/output/samples/mqttclient_publish, cmake, ctest, git`

### 2. Reason — think for `mqtt-paho-c`
- For `paho-c-build`: Clone, build and run Paho MQTT C samples (MQTTClient/MQTTAsync) with the CMake toolchain. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `mqtt-paho-c` tools
- Tools: `Glob`, `Grep`, `Read`, `Bash`, `Cmake` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `mqtt-paho-c:cea20a88`

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
