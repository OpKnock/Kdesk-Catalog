---
applyTo: "**/*.java **/*.json **/*.r **/*.sh **/*.sql"
---

# Api Pagination Spring Data

Implements offset/limit pagination with Spring Data JPA and Spring Data REST: Pageable, HAL links, page metadata, and sort parameters.

## Instructions

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
