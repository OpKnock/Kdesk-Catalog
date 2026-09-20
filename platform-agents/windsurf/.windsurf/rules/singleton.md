---
trigger: glob
description: "Implements the Singleton pattern in Java with javac: controlled single instance creation and its thread-safety trade-offs."
globs: ["**/*.java", "**/*.r", "**/*.sh"]
---

# Singleton

Implements the Singleton pattern in Java with javac: controlled single instance creation and its thread-safety trade-offs.

## Instructions

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
