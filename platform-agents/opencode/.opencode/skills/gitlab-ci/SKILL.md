---
name: "gitlab-ci"
description: "CI/CD pipelines with GitLab CI: validate pipeline YAML, run jobs via the API, manage runners, and debug job failures. Use when working with gitlab pipelines, api or when the user mentions gitlab pipelines, api."
---

CI/CD pipelines with GitLab CI: validate pipeline YAML, run jobs via the API, manage runners, and debug job failures.

## Agentic Workflow: Read -> Reason -> Act (gitlab-ci)

You are **Gitlab Ci** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `gitlab-ci`
- Domain: CI/CD pipelines with GitLab CI: validate pipeline YAML, run jobs via the API, manage runners, and debug job failures.
- **gitlab-pipelines**: Validate, run, and inspect GitLab CI pipelines and runners. — `curl -s -X POST --header 'Content-Type: application/json' --header "PRIVATE-TOKE`
- Check `knowledge` and `prerequisites: gitlab-runner`

### 2. Reason — think for `gitlab-ci`
- For `gitlab-pipelines`: Validate, run, and inspect GitLab CI pipelines and runners. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `gitlab-ci` tools
- Tools: `Glob`, `Grep`, `Read`, `Bash`, `Gitlab-runner` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `gitlab-ci:d83552bf`

# GitLab CI

## What this skill does

GitLab CI defines pipelines in .gitlab-ci.yml with stages, jobs, and rules. The REST API validates config, lists pipelines/jobs, and the gitlab-runner CLI manages executors.

## When to use

- Validating .gitlab-ci.yml before pushing
- Inspecting failing jobs via API
- Registering runners for new projects

## Real commands

```bash
# Lint the config via API
curl -s -X POST --header 'Content-Type: application/json' --header "PRIVATE-TOKEN: $GITLAB_TOKEN" https://gitlab.example.com/api/v4/projects/$PROJECT_ID/ci/lint -d '{"content": "$(cat .gitlab-ci.yml | python -c "import sys,json;print(json.dumps(sys.stdin.read()))")"}' | jq '.errors'

# Latest pipelines on main
curl -s --header "PRIVATE-TOKEN: $GITLAB_TOKEN" https://gitlab.example.com/api/v4/projects/$PROJECT_ID/pipelines?ref=main | jq '.[0] | {id, status}'

# Job statuses for a pipeline
curl -s --header "PRIVATE-TOKEN: $GITLAB_TOKEN" https://gitlab.example.com/api/v4/projects/$PROJECT_ID/pipelines/$PIPE_ID/jobs | jq '.[] | {name, status}'

# Runner management
gitlab-runner list
gitlab-runner register --url https://gitlab.example.com --token $RUNNER_TOKEN --executor docker --docker-image alpine:latest
```

## .gitlab-ci.yml example

```yaml
stages: [test, deploy]

test:
  stage: test
  image: node:20
  script:
    - npm ci
    - npm test
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"

deploy:
  stage: deploy
  script:
    - echo "deploying"
  only:
    - main
```

## Testing

```bash
# Retry a failed job via API
curl -s -X POST --header "PRIVATE-TOKEN: $GITLAB_TOKEN" https://gitlab.example.com/api/v4/projects/$PROJECT_ID/jobs/$JOB_ID/retry | jq '.status'
```

## Best practices

- Lint config in pre-commit or MR CI so invalid YAML never merges.
- Use `rules:` instead of deprecated only/except.
- Cache dependencies per branch and key on lockfiles.
- Scope runner registration tokens to one project.
- Poll job status with the API, don't scrape the UI.

## Capabilities

### gitlab-pipelines
Validate, run, and inspect GitLab CI pipelines and runners.

**Parameters:**
- `project-id` (string): GitLab project id or URL-encoded path
- `pipeline-id` (integer): Pipeline to inspect
- `runner-token` (string): Runner registration token

**Commands:**
- `curl -s -X POST --header 'Content-Type: application/json' --header "PRIVATE-TOKEN: $GITLAB_TOKEN" https://gitlab.example.com/api/v4/projects/$PROJECT_ID/ci/lint -d '{"content": "$(cat .gitlab-ci.yml | python -c "import sys,json;print(json.dumps(sys.stdin.read()))")"}' | jq '.errors'`
- `curl -s --header "PRIVATE-TOKEN: $GITLAB_TOKEN" http://localhost:8080/api/v4/projects/$PROJECT_ID/pipelines?ref=main | jq '.[0] | {id, status}'`
- `curl -s --header "PRIVATE-TOKEN: $GITLAB_TOKEN" http://localhost:8080/api/v4/projects/$PROJECT_ID/pipelines/$PIPE_ID/jobs | jq '.[] | {name, status}'`
- `gitlab-runner list`
- `gitlab-runner register --url http://localhost:8080 --token $RUNNER_TOKEN --executor docker --docker-image alpine:latest`
- `curl -s --header "PRIVATE-TOKEN: $GITLAB_TOKEN" http://localhost:8080/api/v4/projects/$PROJECT_ID/pipelines/$PIPE_ID | jq '{status, duration, created_at}'`

**Examples:**
- curl -s -X POST --header 'Content-Type: application/json' --header "PRIVATE-TOKEN: $GITLAB_TOKEN" https://gitlab.example.com/api/v4/projects/$PROJECT_ID/ci/lint -d '{"content": "$(cat .gitlab-ci.yml | python -c "import sys,json;print(json.dumps(sys.stdin.read()))")"}' | jq '.errors'
- curl -s --header "PRIVATE-TOKEN: $GITLAB_TOKEN" http://localhost:8080/api/v4/projects/$PROJECT_ID/pipelines?ref=main | jq '.[0] | {id, status}'
- gitlab-runner list

## References
- [GitLab CI/CD docs](https://docs.gitlab.com/ee/ci/)
- [GitLab REST API pipelines](https://docs.gitlab.com/ee/api/pipelines.html)
