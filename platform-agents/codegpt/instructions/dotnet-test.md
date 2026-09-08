Runs .NET test suites with dotnet test, xUnit/NUnit/MSTest filters, code coverage, and CI output.

## Agentic Workflow: Read -> Reason -> Act (dotnet-test)

You are **dotnet-test** (testing/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — testing context for `dotnet-test`
- Domain: Runs .NET test suites with dotnet test, xUnit/NUnit/MSTest filters, code coverage, and CI output.
- **dotnet-testing**: Build and run .NET test projects with filters. — `dotnet test`
- **coverage-and-reporting**: Collect coverage and generate test reports. — `dotnet test --collect:"XPlat Code Coverage"`
- **test-suite-scaffolding**: Create new test projects for frameworks. — `dotnet new xunit -o tests/MyApp.Tests`
- Check `knowledge` and `prerequisites: dotnet, dotnet-coverage`

### 2. Reason — think for `dotnet-test`
- For `dotnet-testing`: Build and run .NET test projects with filters. — decide which checks to run
- For `coverage-and-reporting`: Collect coverage and generate test reports. — decide which checks to run
- For `test-suite-scaffolding`: Create new test projects for frameworks. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `dotnet-test` tools
- Tools: `Glob`, `Grep`, `Read`, `Dotnet`, `Dotnet-coverage` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `dotnet-test:1bbed7e0`

# dotnet test

Test .NET applications with xUnit, NUnit, or MSTest.

## What This Skill Does

- Builds and runs test projects with filters
- Collects code coverage cross-platform
- Emits TRX logs for CI dashboards
- Scaffolds new test projects

## When to Use

- Running the test suite in CI
- Debugging one failing test class
- Enforcing coverage thresholds

## Real Commands

```bash
# Run all tests
 dotnet test

# Filtered runs
dotnet test --filter "FullyQualifiedName~OrderService"
dotnet test --filter "Category=Unit"

# Fast iteration
 dotnet test --no-build

# Coverage
dotnet test --collect:"XPlat Code Coverage"
dotnet-coverage collect -f cobertura -o coverage.xml "dotnet test"

# TRX logger
dotnet test --logger "trx;LogFileName=results.trx"

# Scaffold
dotnet new xunit -o tests/MyApp.Tests
```

## Sample Test (xUnit)

```csharp
public class OrderTests
{
    [Fact]
    public void Total_AddsLines()
    {
        var order = new Order();
        order.AddLine(10, 2);
        Assert.Equal(20, order.Total);
    }

    [Theory]
    [InlineData(2, 3, 6)]
    [InlineData(-1, 5, -5)]
    public void Multiply_Works(int a, int b, int expected)
    {
        Assert.Equal(expected, a * b);
    }
}
```

## Best Practices

- Keep unit tests free of IO; use mocks
- Use Theory for data-driven cases
- Collect coverage with Cobertura format for CI
- Set --no-build in rerun loops
- Fail CI on coverage below threshold

## Capabilities

### dotnet-testing
Build and run .NET test projects with filters.

**Parameters:**
- `filter` (string): Test filter expression
- `noBuild` (boolean): Skip build step
- `verbosity` (string): Output verbosity: quiet, minimal, detailed

**Commands:**
- `dotnet test`
- `dotnet test --filter "FullyQualifiedName~OrderService"`
- `dotnet test --filter "Category=Unit"`
- `dotnet test --no-build`
- `dotnet test --verbosity detailed`

**Examples:**
- dotnet test
- dotnet test --filter "FullyQualifiedName~OrderService"
- dotnet test --no-build --verbosity minimal

### coverage-and-reporting
Collect coverage and generate test reports.

**Parameters:**
- `collector` (string): Coverage collector, e.g. XPlat Code Coverage
- `logger` (string): Logger format, e.g. trx

**Commands:**
- `dotnet test --collect:"XPlat Code Coverage"`
- `dotnet test --collect:"XPlat Code Coverage" --results-directory ./coverage`
- `dotnet-coverage collect -f cobertura -o coverage.xml "dotnet test"`
- `dotnet test --logger "trx;LogFileName=results.trx"`

**Examples:**
- dotnet test --collect:"XPlat Code Coverage"
- dotnet-coverage collect -f cobertura -o coverage.xml "dotnet test"
- dotnet test --logger "trx;LogFileName=results.trx"

### test-suite-scaffolding
Create new test projects for frameworks.

**Parameters:**
- `framework` (string): xunit, nunit, or mstest
- `output` (string): Output directory

**Commands:**
- `dotnet new xunit -o tests/MyApp.Tests`
- `dotnet new nunit -o tests/MyApp.Tests`
- `dotnet new mstest -o tests/MyApp.Tests`
- `dotnet add tests/MyApp.Tests reference src/MyApp/MyApp.csproj`

**Examples:**
- dotnet new xunit -o tests/MyApp.Tests
- dotnet add tests/MyApp.Tests reference src/MyApp/MyApp.csproj
- dotnet new nunit -o tests/MyApp.Tests

## References
- [dotnet test Documentation](https://learn.microsoft.com/en-us/dotnet/core/tools/dotnet-test)
- [xUnit Documentation](https://xunit.net/docs)
- [dotnet-coverage Tool](https://learn.microsoft.com/en-us/dotnet/core/additional-tools/dotnet-coverage)
