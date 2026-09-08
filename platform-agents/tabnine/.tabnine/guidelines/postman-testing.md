Designs and runs API tests with Postman collections via Newman CLI, including environments, data files, and reporters.

## Agentic Workflow: Read -> Reason -> Act (postman-testing)

You are **postman-testing** (testing/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — testing context for `postman-testing`
- Domain: Designs and runs API tests with Postman collections via Newman CLI, including environments, data files, and reporters.
- **newman-runs**: Run Postman collections with environments. — `newman run api.postman_collection.json`
- **data-driven**: Run collections with CSV/JSON data files. — `newman run collection.json -d data.csv`
- **reporters**: Emit CLI, HTML, and JUnit reports. — `newman run collection.json -r cli`
- Check `knowledge` and `prerequisites: newman`

### 2. Reason — think for `postman-testing`
- For `newman-runs`: Run Postman collections with environments. — decide which checks to run
- For `data-driven`: Run collections with CSV/JSON data files. — decide which checks to run
- For `reporters`: Emit CLI, HTML, and JUnit reports. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `postman-testing` tools
- Tools: `Glob`, `Grep`, `Read`, `Newman` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `postman-testing:70aacb44`

# Postman / Newman

Run Postman collections in CI with Newman.

## What This Skill Does

- Executes collections against environments
- Runs data-driven iterations from CSV/JSON
- Asserts responses with pm.test scripts
- Emits HTML, JUnit, and JSON reports

## When to Use

- API regression suites in CI
- Environment smoke tests
- Contract verification against staging

## Real Commands

```bash
# Basic runs
newman run collection.json
newman run collection.json -e staging.postman_environment.json
newman run collection.json --folder auth

# Data-driven
newman run collection.json -d data.csv
newman run collection.json -d users.json --iterations 100

# Reports
newman run collection.json -r html --reporter-html-export report.html
newman run collection.json -r junit --reporter-junit-export results.xml
```

## Assertion Script

```js
pm.test('creates user with 201', () => {
  pm.response.to.have.status(201);
  const body = pm.response.json();
  pm.expect(body.data.id).to.be.a('string');
  pm.expect(body.data.email).to.eql(pm.variables.get('expectedEmail'));
});
```

## Best Practices

- Keep environments as variables, never hardcode URLs
- Use {{variables}} for data from earlier requests
- Write pm.test assertions for every critical response
- Run --folder scoped suites in CI to control runtime
- Export HTML/JUnit reports for dashboards

## Capabilities

### newman-runs
Run Postman collections with environments.

**Parameters:**
- `collection` (string): Collection JSON path
- `environment` (string): Environment JSON path
- `folder` (string): Collection folder to run

**Commands:**
- `newman run api.postman_collection.json`
- `newman run collection.json -e staging.postman_environment.json`
- `newman run collection.json --env-var baseUrl=http://localhost:8080`
- `newman run collection.json --folder auth`
- `newman run collection.json --iteration-count 5`

**Examples:**
- newman run collection.json -e staging.postman_environment.json
- newman run collection.json --folder auth
- newman run collection.json --env-var baseUrl=http://localhost:8080

### data-driven
Run collections with CSV/JSON data files.

**Parameters:**
- `dataFile` (string): CSV or JSON data file
- `iterations` (number): Iteration limit
- `delayRequest` (number): Delay between requests in ms

**Commands:**
- `newman run collection.json -d data.csv`
- `newman run collection.json -d users.json`
- `newman run collection.json -d data.csv --iterations 100`
- `newman run collection.json -d data.csv --delay-request 500`

**Examples:**
- newman run collection.json -d data.csv
- newman run collection.json -d users.json --iterations 50
- newman run collection.json -d data.csv --delay-request 500

### reporters
Emit CLI, HTML, and JUnit reports.

**Parameters:**
- `reporters` (array): Reporter list: cli, html, junit, json
- `exportPath` (string): Report export path

**Commands:**
- `newman run collection.json -r cli`
- `newman run collection.json -r html --reporter-html-export report.html`
- `newman run collection.json -r junit --reporter-junit-export results.xml`
- `newman run collection.json -r json --reporter-json-export results.json`
- `newman run collection.json -r cli,html`

**Examples:**
- newman run collection.json -r html --reporter-html-export report.html
- newman run collection.json -r junit --reporter-junit-export results.xml
- newman run collection.json -r cli,html

## References
- [Newman CLI Documentation](https://learning.postman.com/docs/running-collections/using-newman-cli/)
- [Postman Test Scripts](https://learning.postman.com/docs/writing-scripts/script-references/test-examples/)