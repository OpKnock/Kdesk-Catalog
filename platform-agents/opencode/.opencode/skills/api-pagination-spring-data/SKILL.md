---
name: "api-pagination-spring-data"
description: "Implements offset/limit pagination with Spring Data JPA and Spring Data REST: Pageable, HAL links, page metadata, and sort parameters. Use when working with spring data paging, pageable repositories or when the user mentions spring data paging, pageable repositories."
---

Implements offset/limit pagination with Spring Data JPA and Spring Data REST: Pageable, HAL links, page metadata, and sort parameters.

## Agentic Workflow: Read -> Reason -> Act (api-pagination-spring-data)

You are **Api Pagination Spring Data** (backend) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — backend context for `api-pagination-spring-data`
- Domain: Implements offset/limit pagination with Spring Data JPA and Spring Data REST: Pageable, HAL links, page metadata, and sort parameters.
- **spring-data-paging**: Use Spring Data Pageable with HAL response metadata — `curl -s 'http://localhost:8080/api/users?page=0&size=20' | jq '.page.totalElemen`
- **pageable-repositories**: Define paging repository methods and custom Pageable defaults — `curl -s 'http://localhost:8080/api/users?size=0' -o /dev/null -w '%{http_code}\n`
- Check `knowledge` and `prerequisites: node.js, python, postgresql`

### 2. Reason — think for `api-pagination-spring-data`
- For `spring-data-paging`: Use Spring Data Pageable with HAL response metadata — decide which checks to run
- For `pageable-repositories`: Define paging repository methods and custom Pageable defaults — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `api-pagination-spring-data` tools
- Tools: `Glob`, `Grep`, `Read`, `Bash`, `./mvnw` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `api-pagination-spring-data:1228bdee`

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
