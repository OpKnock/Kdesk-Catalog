---
name: "Api Pagination Drf"
description: "Implements pagination in Django REST Framework: PageNumberPagination, LimitOffsetPagination, CursorPagination classes, and OpenAPI schema integration. Use when working with drf pagination, custom pagination or when the user mentions drf pagination, custom pagination."
globs: ["**/*.go", "**/*.py", "**/*.r", "**/*.sh", "**/*.{yaml,yml}"]
alwaysApply: false
---

Implements pagination in Django REST Framework: PageNumberPagination, LimitOffsetPagination, CursorPagination classes, and OpenAPI schema integration.

## Agentic Workflow: Read -> Reason -> Act (api-pagination-drf)

You are **Api Pagination Drf** (backend) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — backend context for `api-pagination-drf`
- Domain: Implements pagination in Django REST Framework: PageNumberPagination, LimitOffsetPagination, CursorPagination classes, and OpenAPI schema integration.
- **drf-pagination**: Configure DRF pagination classes and page metadata — `python manage.py runserver 8000`
- **custom-pagination**: Subclass pagination classes for custom response shapes — `curl -s 'http://localhost:8000/api/users/?ordering=created_at' | jq '.next'`
- Check `knowledge` and `prerequisites: node.js, python, postgresql`

### 2. Reason — think for `api-pagination-drf`
- For `drf-pagination`: Configure DRF pagination classes and page metadata — decide which checks to run
- For `custom-pagination`: Subclass pagination classes for custom response shapes — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `api-pagination-drf` tools
- Tools: `Glob`, `Grep`, `Read`, `Bash` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `api-pagination-drf:e1fc4a77`

# API Pagination v4 - Django REST Framework

Pagination with DRF classes.

## What This Skill Does
- Applies PageNumber, LimitOffset, or Cursor pagination
- Returns count/next/previous metadata
- Documents paging parameters in OpenAPI schemas

## When to Use
- DRF APIs needing standard paging behavior
- Admin list views with moderate data sizes
- APIs where cursor stability matters less than simplicity

## Real Commands

```bash
curl -s 'http://localhost:8000/api/users/?page=2&page_size=10' | jq '.count, .next, .previous'
curl -s 'http://localhost:8000/api/users/?limit=5&offset=10' | jq '.count, .results | length'
```

## Settings

```python
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    'MAX_PAGE_SIZE': 100,
}
```

## Testing
- Verify count stays consistent across pages
- Test negative and oversized page values
- Confirm cursor ordering survives record edits

## Best Practices
- Use CursorPagination for feeds and timelines
- Set MAX_PAGE_SIZE to bound query cost
- Keep pagination metadata in the serializer response

## Capabilities

### drf-pagination
Configure DRF pagination classes and page metadata

**Parameters:**
- `page` (integer): Page number for PageNumberPagination
- `page_size` (integer): Custom page size query param
- `ordering` (string): Ordering field for CursorPagination

**Commands:**
- `python manage.py runserver 8000`
- `curl -s 'http://localhost:8000/api/users/?page=2&page_size=10' | jq '.count, .next, .previous'`
- `curl -s 'http://localhost:8000/api/users/?limit=5&offset=10' | jq '.count, .results | length'`
- `python manage.py shell -c "from rest_framework.pagination import PageNumberPagination; print(PageNumberPagination.page_size)"`
- `curl -s 'http://localhost:8000/api/schema/' -o schema.yaml`

**Examples:**
- ?page=2&page_size=10 returns count/next/previous metadata
- LimitOffsetPagination accepts ?limit=5&offset=10
- CursorPagination keys on ordering fields and returns next cursors

### custom-pagination
Subclass pagination classes for custom response shapes

**Commands:**
- `curl -s 'http://localhost:8000/api/users/?ordering=created_at' | jq '.next'`
- `python manage.py test api.tests.test_pagination -v 2`
- `curl -s 'http://localhost:8000/api/users/?page=-5' -o /dev/null -w '%{http_code}\n'`

**Examples:**
- -cli --help
- -api --help

## References
- [DRF Pagination Guide](https://www.django-rest-framework.org/api-guide/pagination/)
- [DRF Schemas](https://www.django-rest-framework.org/api-guide/schemas/)