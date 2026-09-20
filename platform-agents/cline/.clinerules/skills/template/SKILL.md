---
name: "template"
description: "Implements the Template Method pattern in Java with Maven: fixed algorithm skeletons with overridable steps."
---

# Template

Implements the Template Method pattern in Java with Maven: fixed algorithm skeletons with overridable steps.

## Instructions

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
