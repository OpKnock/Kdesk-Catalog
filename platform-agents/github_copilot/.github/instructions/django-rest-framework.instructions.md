---
applyTo: "**/*.go **/*.json **/*.py **/*.r **/*.sh"
---

Builds and maintains Django REST Framework APIs: runs the dev server, manages migrations, generates OpenAPI schemas via drf-spectacular, and tests endpoints.

## Agentic Workflow: Read -> Reason -> Act (django-rest-framework)

You are **Django Rest Framework** (api/general) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — api context for `django-rest-framework`
- Domain: Builds and maintains Django REST Framework APIs: runs the dev server, manages migrations, generates OpenAPI schemas via drf-spectacular, and tests endpoints.
- **drf-project**: Day-to-day DRF project operations: server, migrations, schema generation, and tests. — `python manage.py runserver 0.0.0.0:8000`
- Check `knowledge` and `prerequisites: python`

### 2. Reason — think for `django-rest-framework`
- For `drf-project`: Day-to-day DRF project operations: server, migrations, schema generation, and tests. — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `django-rest-framework` tools
- Tools: `Glob`, `Grep`, `Read`, `Bash` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `django-rest-framework:5dbfca21`

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
