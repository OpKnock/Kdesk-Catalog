---
name: "template"
description: "Implements the Template Method pattern in Java with Maven: fixed algorithm skeletons with overridable steps. Use when working with java maven, template or when the user mentions java maven, template."
license: "MIT"
compatibility: "Requires mvn."
metadata: {"author": "Kdesk", "version": "2.0.0", "category": "patterns"}
allowed-tools: "Glob Grep Read Bash(mvn:*)"
---

Implements the Template Method pattern in Java with Maven: fixed algorithm skeletons with overridable steps.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `mvn archetype:generate -DgroupId=com.example -DartifactId=te`
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

# Template Method Pattern

Define an algorithm skeleton; let subclasses fill the steps.

## When to Use

- Recurring multi-step processes with variant steps
- Pipelines where ordering must be fixed
- Reusing flow while allowing step overrides

## Example (Java)

```java
public abstract class OrderProcessor {
    public final void process() {
        validate();
        charge();
        notifyCustomer();
    }

    protected abstract void validate();
    protected abstract void charge();
    protected void notifyCustomer() { /* default no-op */ }
}

public class CardOrderProcessor extends OrderProcessor {
    protected void validate() { System.out.println("validating card"); }
    protected void charge() { System.out.println("charging card"); }
    protected void notifyCustomer() { System.out.println("emailed receipt"); }
}
```

## Test

```java
@Test
void processesInOrder() {
    new CardOrderProcessor().process();
    // verify order via a recorder
}
```

```bash
mvn -q test
```

## Best practices

- Mark the skeleton `final` to lock step order.
- Provide sensible defaults for optional steps.
- Keep steps cohesive; extract overridable points deliberately.
- Use the pattern sparingly - composition beats inheritance often.

## Testing

Test the skeleton order and each subclass's step overrides.

## Capabilities

### java-maven
Implement and test template method examples.

**Parameters:**
- `test` (string): Test class or method filter
- `archetype` (string): Maven archetype id
- `q` (string): Quiet output

**Commands:**
- `mvn archetype:generate -DgroupId=com.example -DartifactId=template -DarchetypeArtifactId=maven-archetype-quickstart`
- `mvn -q compile`
- `mvn -q test`
- `mvn -q test -Dtest=OrderProcessorTest`
- `mvn -q exec:java`

**Examples:**
- mvn -q test -Dtest='OrderProcessorTest#processOrder'
- mvn -q compile && mvn -q exec:java -Dexec.mainClass=com.example.Main
- mvn -q test -DfailIfNoTests=false

## References
- [Refactoring Guru: Template Method](https://refactoring.guru/design-patterns/template-method)
- [Maven Surefire](https://maven.apache.org/surefire/maven-surefire-plugin/)
