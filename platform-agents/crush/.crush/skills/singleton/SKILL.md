---
name: "singleton"
description: "Implements the Singleton pattern in Java with javac: controlled single instance creation and its thread-safety trade-offs. Use when working with java, singleton or when the user mentions java, singleton."
license: "MIT"
compatibility: "Requires java, javac."
metadata: {"author": "Kdesk", "version": "2.0.0", "category": "patterns"}
allowed-tools: "Glob Grep Read Bash(java:*) Bash(javac:*)"
---

Implements the Singleton pattern in Java with javac: controlled single instance creation and its thread-safety trade-offs.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `javac -d out Singleton.java Main.java`
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

# Singleton Pattern

Ensure one instance and one access point.

## When to Use

- Shared resources: config, connection pools, caches
- Logging and audit infrastructure
- Cross-cutting services with no state needs

## Example (Java)

```java
public final class Config {
    private static final Config INSTANCE = new Config();
    private Config() {}
    public static Config getInstance() { return INSTANCE; }

    private String env = "prod";
    public String env() { return env; }
}
```

Eager init via `static final` is thread-safe without locks.

## Verify

```java
public class Main {
    public static void main(String[] args) {
        Config a = Config.getInstance();
        Config b = Config.getInstance();
        System.out.println(a == b ? "same instance" : "different");
    }
}
```

```bash
javac -d out Singleton.java Main.java
java -cp out Main
```

## When NOT to use

- Global mutable state hides dependencies.
- Testing becomes harder - inject dependencies instead.
- Prefer dependency injection containers over singletons.

## Best practices

- Keep singletons stateless or read-only after init.
- Prefer enum singleton in Java for serialization safety.
- If lazily initialized, guard double-checked locking carefully.
- Limit to genuinely system-wide resources.

## Testing

Test that repeated getInstance returns identical references.

## Capabilities

### java
Implement and verify singleton examples.

**Parameters:**
- `cp` (string): Classpath directory
- `Xlint` (string): Compiler warnings
- `ea` (string): Enable assertions

**Commands:**
- `javac -d out Singleton.java Main.java`
- `java -cp out Main`
- `javac -Xlint:all -d out Singleton.java`
- `java -cp out com.example.singleton.Main`
- `javac -d out SingletonTest.java && java -cp out -ea SingletonTest`

**Examples:**
- javac -d out Singleton.java && java -cp out com.example.Main
- javac -Xlint:all -d out *.java
- java -cp out com.example.Main | grep -c 'same instance'

## References
- [Refactoring Guru: Singleton](https://refactoring.guru/design-patterns/singleton)
- [JLS Enum](https://docs.oracle.com/javase/specs/jls/se17/html/jls-8.html)
