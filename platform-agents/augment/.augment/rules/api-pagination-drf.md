---
type: agent_requested
description: "Implements pagination in Django REST Framework: PageNumberPagination, LimitOffsetPagination, CursorPagination classes, and OpenAPI schema integration. Use when working with drf pagination, custom pagination or when the user mentions drf pagination, custom pagination."
---

Implements pagination in Django REST Framework: PageNumberPagination, LimitOffsetPagination, CursorPagination classes, and OpenAPI schema integration.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `python manage.py runserver 8000`, `curl -s 'http://localhost:8000/api/users/?ordering=created_a`
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