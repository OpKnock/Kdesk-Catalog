---
type: agent_requested
description: "Implements the Command pattern in Java with Gradle: encapsulating requests as objects with undo/redo support. Use when working with java gradle, command or when the user mentions java gradle, command."
---

Implements the Command pattern in Java with Gradle: encapsulating requests as objects with undo/redo support.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `gradle init --type java-library --dsl groovy --test-framewor`
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

# Command Pattern

Turn requests into objects: undoable, queueable, loggable.

## When to Use

- Undo/redo in editors
- Queuing or logging operations
- Macro composition of actions

## Example (Java)

```java
public interface Command {
    void execute();
    void undo();
}

public class AddTextCommand implements Command {
    private final StringBuilder doc;
    private final String text;

    public AddTextCommand(StringBuilder doc, String text) {
        this.doc = doc;
        this.text = text;
    }

    public void execute() { doc.append(text); }
    public void undo() {
        int start = doc.length() - text.length();
        doc.delete(start, doc.length());
    }
}

public class History {
    private final Deque<Command> undoStack = new ArrayDeque<>();

    public void push(Command c) { c.execute(); undoStack.push(c); }
    public void undo() { undoStack.pop().undo(); }
}
```

## Test

```java
@Test
void addAndUndo() {
    var doc = new StringBuilder();
    var h = new History();
    h.push(new AddTextCommand(doc, "hello"));
    h.push(new AddTextCommand(doc, " world"));
    assertThat(doc.toString()).isEqualTo("hello world");
    h.undo();
    assertThat(doc.toString()).isEqualTo("hello");
}
```

```bash
./gradlew test --tests 'com.example.command.HistoryTest'
```

## Best practices

- Commands are pure intent; state lives in receivers.
- Make commands serializable for queues and journals.
- Implement undo as inverse ops, not snapshots, for large state.
- Test execute/undo pairs for every command.

## Testing

Verify execute-then-undo returns exact prior state.

## Capabilities

### java-gradle
Implement and test Command pattern examples.

**Parameters:**
- `test-framework` (string): junit-jupiter, spock, or testng
- `tests` (string): Test class filter
- `dsl` (string): groovy or kotlin build DSL

**Commands:**
- `gradle init --type java-library --dsl groovy --test-framework junit-jupiter`
- `gradle wrapper`
- `./gradlew build`
- `./gradlew test --tests 'com.example.command.*'`
- `./gradlew run`

**Examples:**
- gradle init --type java-application --test-framework junit-jupiter
- ./gradlew test --tests 'com.example.command.HistoryTest' --info
- ./gradlew build -x test

## References
- [Refactoring Guru: Command](https://refactoring.guru/design-patterns/command)
- [Gradle Docs](https://docs.gradle.org/current/userguide/java_library_plugin.html)