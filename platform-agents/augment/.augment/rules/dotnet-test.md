---
type: agent_requested
description: "Runs .NET test suites with dotnet test, xUnit/NUnit/MSTest filters, code coverage, and CI output."
---

# dotnet-test

Runs .NET test suites with dotnet test, xUnit/NUnit/MSTest filters, code coverage, and CI output.

## Instructions

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

**Commands:**
- `dotnet new xunit -o tests/MyApp.Tests`
- `dotnet new nunit -o tests/MyApp.Tests`
- `dotnet new mstest -o tests/MyApp.Tests`
- `dotnet add tests/MyApp.Tests reference src/MyApp/MyApp.csproj`

**Examples:**
- dotnet new xunit -o tests/MyApp.Tests
- dotnet add tests/MyApp.Tests reference src/MyApp/MyApp.csproj
- dotnet new nunit -o tests/MyApp.Tests