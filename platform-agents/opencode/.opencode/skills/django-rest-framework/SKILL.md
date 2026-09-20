---
name: "django-rest-framework"
description: "Builds and maintains Django REST Framework APIs: runs the dev server, manages migrations, generates OpenAPI schemas via drf-spectacular, and tests endpoints. Use when working with drf project, api or when the user mentions drf project, api."
---

Builds and maintains Django REST Framework APIs: runs the dev server, manages migrations, generates OpenAPI schemas via drf-spectacular, and tests endpoints.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `python manage.py runserver 0.0.0.0:8000`
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

# Django REST Framework

## What this skill does

Django REST Framework (DRF) turns Django models into JSON APIs with serializers, viewsets, routers, authentication, and throttling. This skill covers project workflow: migrations, servers, schema export, and test runs.

## When to use

- Building a JSON API on top of Django models
- Adding or changing API endpoints, serializers, or permissions
- Generating and validating the OpenAPI schema for the API

## Real commands

```bash
# Run the development server
python manage.py runserver 0.0.0.0:8000

# Schema/model changes
python manage.py makemigrations api
python manage.py migrate

# Generate OpenAPI schema and lint it
python manage.py spectacular --file schema.yml
npx @redocly/cli lint schema.yml

# Run tests
python manage.py test api --keepdb

# Quick data inspection
python manage.py shell -c "from api.models import Order; print(Order.objects.count())"
```

## Example viewset

```python
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Order
from .serializers import OrderSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['status', 'customer']
```

## Testing endpoints

```bash
curl -s http://localhost:8000/api/orders/ -H 'Authorization: Bearer $TOKEN' | jq
curl -s http://localhost:8000/api/schema/ | jq '.paths | keys'
```

## Best practices

- Use viewsets + routers instead of hand-written CRUD functions.
- Set `DEFAULT_PAGINATION_CLASS` with a page size in settings.py.
- Keep business logic in services or models, not in serializers.
- Use drf-spectacular for schema generation; annotate with `@extend_schema` for docstrings.
- Use `--keepdb` in CI to speed up test runs.

## Capabilities

### drf-project
Day-to-day DRF project operations: server, migrations, schema generation, and tests.

**Parameters:**
- `app-name` (string): Django app containing the models/serializers to manage
- `port` (integer): Port for the development server
- `schema-file` (string): Output path for the generated OpenAPI schema

**Commands:**
- `python manage.py runserver 0.0.0.0:8000`
- `python manage.py makemigrations api`
- `python manage.py migrate`
- `python manage.py spectacular --file schema.yml`
- `python manage.py test api`
- `python manage.py shell -c "from api.models import Order; print(Order.objects.count())"`

**Examples:**
- python manage.py makemigrations api && python manage.py migrate
- python manage.py spectacular --file schema.yml && npx @redocly/cli lint schema.yml
- python manage.py test api --keepdb

## References
- [DRF Official Docs](https://www.django-rest-framework.org/)
- [drf-spectacular](https://drf-spectacular.readthedocs.io/)
