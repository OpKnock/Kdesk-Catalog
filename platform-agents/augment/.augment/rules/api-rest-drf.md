---
type: agent_requested
description: "Builds REST APIs with Django REST Framework: models, serializers, viewsets, routers, permissions, and browsable API testing. Use when working with drf setup, viewsets or when the user mentions drf setup, viewsets."
---

Builds REST APIs with Django REST Framework: models, serializers, viewsets, routers, permissions, and browsable API testing.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `pip install django djangorestframework`, `curl -s http://localhost:8000/api/users/ | jq 'length'`
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