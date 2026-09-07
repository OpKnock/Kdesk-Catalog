---
type: agent_requested
description: "Build Java MQTT clients with Eclipse Paho Java: MqttClient API, callbacks, persistence and Maven setup. Use when working with paho java client, api or when the user mentions paho java client, api."
---

Build Java MQTT clients with Eclipse Paho Java: MqttClient API, callbacks, persistence and Maven setup.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `mvn dependency:tree`
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

# Paho MQTT Java

The Eclipse Paho Java client (org.eclipse.paho.client.mqttv3) is the standard MQTT client for JVM apps.

## What this skill does

- Configures the Maven dependency
- Writes MqttClient publish/subscribe code
- Covers persistent sessions and async callbacks

## When to use

- JVM services publishing events to MQTT
- IoT backends and edge gateways in Java

## Real commands

```bash
# Verify the dependency resolves
mvn dependency:tree -Dincludes=org.eclipse.paho

# Build and run
mvn compile
mvn exec:java -Dexec.mainClass=com.example.Publisher
mvn package
```

## Publish code

```java
MqttClient client = new MqttClient("tcp://localhost:1883", "java-pub");
client.connect();
client.publish("sensors/temp", new MqttMessage("21.5".getBytes()));
client.disconnect();
```

## Callbacks for async

```java
client.setCallback(new MqttCallback() {
    public void messageArrived(String topic, MqttMessage m) { /* handle */ }
    public void connectionLost(Throwable c) { client.reconnect(); }
    public void deliveryComplete(IMqttDeliveryToken t) { }
});
```

## pom.xml dependency

```xml
<dependency>
  <groupId>org.eclipse.paho</groupId>
  <artifactId>org.eclipse.paho.client.mqttv3</artifactId>
  <version>1.2.5</version>
</dependency>
```

## Best practices

- Use `MqttConnectOptions#setCleanSession(false)` for durable subscriptions
- Reconnect with exponential backoff in connectionLost
- Match MQTT QoS with your reliability requirements

## Capabilities

### paho-java-client
Add the paho.mqttv3 dependency, write synchronous/async clients and manage connections in Maven projects.

**Parameters:**
- `version` (string): paho.mqttv3 version, e.g. 1.2.5
- `main_class` (string): Java main class to run via exec plugin
- `broker_url` (string): tcp:// or ssl:// broker URL

**Commands:**
- `mvn dependency:tree`
- `mvn compile`
- `mvn package`
- `mvn exec:java -Dexec.mainClass=com.example.Publisher`
- `curl -s https://repo1.maven.org/maven2/org/eclipse/paho/org.eclipse.paho.client.mqttv3/maven-metadata.xml`

**Examples:**
- mvn dependency:tree -Dincludes=org.eclipse.paho
- mvn package -DskipTests
- mvn exec:java -Dexec.mainClass=com.example.Subscriber

## References
- [Paho Java client page](https://www.eclipse.org/paho/index.php?page=clients/java/index.php)
- [Paho Java GitHub](https://github.com/eclipse/paho.mqtt.java)