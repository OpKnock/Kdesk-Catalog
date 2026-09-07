---
type: agent_requested
description: "Implements offset/limit pagination with Spring Data JPA and Spring Data REST: Pageable, HAL links, page metadata, and sort parameters. Use when working with spring data paging, pageable repositories or when the user mentions spring data paging, pageable repositories."
---

Implements offset/limit pagination with Spring Data JPA and Spring Data REST: Pageable, HAL links, page metadata, and sort parameters.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `curl -s 'http://localhost:8080/api/users?page=0&size=20' | j`, `curl -s 'http://localhost:8080/api/users?size=0' -o /dev/nul`
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

# API Pagination v2 - Spring Data

Offset pagination with Spring Data.

## What This Skill Does
- Maps Pageable parameters to JPA queries
- Returns HAL links and page metadata
- Enforces page size limits and sort whitelisting

## When to Use
- Spring Boot APIs needing standard page/size paging
- HATEOAS-style clients that follow HAL links
- Admin tables with simple data volumes

## Real Commands

```bash
curl -s 'http://localhost:8080/api/users?page=0&size=20' | jq '.page.totalElements, .page.totalPages'
curl -s -H 'Accept: application/hal+json' 'http://localhost:8080/api/users' | jq '._links.next.href'
```

## Repository Method

```java
@Repository
public interface UserRepository extends JpaRepository<User, Long> {
    Page<User> findByActiveTrue(Pageable pageable);
}
```

## Testing
- Verify totalPages math on boundary sizes
- Confirm size=0 and negative pages are rejected
- Test sort injection attempts do not cause SQL errors

## Best Practices
- Configure spring.data.rest.max-page-size globally
- Whitelist sortable properties to avoid expensive sorts
- Use Page<DTO> projections to avoid N+1 lazy loading

## Capabilities

### spring-data-paging
Use Spring Data Pageable with HAL response metadata

**Parameters:**
- `page` (integer): Zero-based page index
- `size` (integer): Page size, capped by Spring config
- `sort` (string): Comma-separated property,dir pairs

**Commands:**
- `curl -s 'http://localhost:8080/api/users?page=0&size=20' | jq '.page.totalElements, .page.totalPages'`
- `curl -s -H 'Accept: application/hal+json' 'http://localhost:8080/api/users' | jq '._links.next.href'`
- `curl -s 'http://localhost:8080/api/users?sort=name,desc' | jq '._embedded.users[0].name'`
- `./mvnw clean test`

**Examples:**
- page=0&size=20 selects page one with 20 items
- Accept: application/hal+json returns _links with next/prev
- sort=name,desc orders results before paging

### pageable-repositories
Define paging repository methods and custom Pageable defaults

**Commands:**
- `curl -s 'http://localhost:8080/api/users?size=0' -o /dev/null -w '%{http_code}\n'`
- `curl -s 'http://localhost:8080/api/users?page=-1' -o /dev/null -w '%{http_code}\n'`
- `./mvnw spring-boot:run -Dspring-boot.run.arguments=--spring.data.rest.default-page-size=50`

**Examples:**
- -cli --help
- -api --help

## References
- [Spring Data REST Docs](https://docs.spring.io/spring-data/rest/reference/paging-chapter.html)
- [Spring Data JPA Repositories](https://docs.spring.io/spring-data/jpa/reference/repositories/paging-and-sorting.html)