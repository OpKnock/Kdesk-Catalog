---
name: "Api Rest Drf"
description: "Builds REST APIs with Django REST Framework: models, serializers, viewsets, routers, permissions, and browsable API testing. Use when working with drf setup, viewsets or when the user mentions drf setup, viewsets."
globs: ["**/*.go", "**/*.json", "**/*.py", "**/*.r", "**/*.sh"]
alwaysApply: false
---

Builds REST APIs with Django REST Framework: models, serializers, viewsets, routers, permissions, and browsable API testing.

## Agentic Workflow: Read -> Reason -> Act (api-rest-drf)

You are **Api Rest Drf** (backend) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — backend context for `api-rest-drf`
- Domain: Builds REST APIs with Django REST Framework: models, serializers, viewsets, routers, permissions, and browsable API testing.
- **drf-setup**: Scaffold a Django project with DRF — `pip install django djangorestframework`
- **viewsets**: Expose CRUD via viewsets and routers — `curl -s http://localhost:8000/api/users/ | jq 'length'`
- Check `knowledge` and `prerequisites: node.js, python, express, fastapi`

### 2. Reason — think for `api-rest-drf`
- For `drf-setup`: Scaffold a Django project with DRF — decide which checks to run
- For `viewsets`: Expose CRUD via viewsets and routers — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `api-rest-drf` tools
- Tools: `Glob`, `Grep`, `Read`, `Bash`, `Django-admin` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `api-rest-drf:737dd577`

# API REST v4 - Django REST Framework

REST APIs with DRF.

## What This Skill Does
- Exposes models as REST resources with viewsets
- Validates and serializes with serializers
- Handles auth with permission classes

## When to Use
- Python/Django teams
- Rapid CRUD APIs with admin UIs
- Standardized DRF projects

## Real Commands

```bash
pip install django djangorestframework
django-admin startproject config .
python manage.py startapp api
python manage.py migrate
python manage.py runserver
```

## ViewSet Example

```python
from rest_framework import viewsets
from .models import User
from .serializers import UserSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
```

## Testing
- Verify browsable API at /api/users/
- Test validation and permissions with APIClient
- Confirm 401/403 for anonymous writes

## Best Practices
- Use routers to wire URLs consistently
- Add filtering and ordering mixins
- Document with drf-spectacular OpenAPI generation

## Capabilities

### drf-setup
Scaffold a Django project with DRF

**Parameters:**
- `app` (string): Django app name
- `model` (string): Model to expose via the API
- `serializer` (string): DRF serializer class

**Commands:**
- `pip install django djangorestframework`
- `django-admin startproject config .`
- `python manage.py startapp api`
- `python manage.py migrate`
- `python manage.py runserver`

**Examples:**
- django-admin startproject scaffolds the project
- python manage.py migrate applies schema
- python manage.py runserver serves the browsable API

### viewsets
Expose CRUD via viewsets and routers

**Commands:**
- `curl -s http://localhost:8000/api/users/ | jq 'length'`
- `curl -s -X POST http://localhost:8000/api/users/ -H 'Content-Type: application/json' -d '{"name":"alice","email":"a@localhost"}' -w '\n%{http_code}\n'`
- `curl -s -o /dev/null -w '%{http_code}\n' -X POST http://localhost:8000/api/users/ -H 'Content-Type: application/json' -d '{"name":"x"}'`
- `python manage.py test api -v 2`

**Examples:**
- -cli --help
- -api --help

## References
- [DRF Quickstart](https://www.django-rest-framework.org/tutorial/quickstart/)
- [DRF Viewsets](https://www.django-rest-framework.org/api-guide/viewsets/)