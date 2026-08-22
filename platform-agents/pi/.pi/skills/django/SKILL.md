---
name: "django"
description: "Builds full-stack web applications with Django: projects, apps, ORM, admin, auth, migrations, and production deployment."
---

# Django

Builds full-stack web applications with Django: projects, apps, ORM, admin, auth, migrations, and production deployment.

## Instructions

# Django

High-level Python web framework.

## When to Use

- CRUD applications with admin interfaces
- ORM-heavy data models backed by PostgreSQL/MySQL
- Built-in auth, sessions, and class-based views
- Projects needing mature ecosystem (DRF, Celery, channels)

## Commands

```bash
# New project and app
django-admin startproject mysite .
python manage.py startapp polls

# Dev server
python manage.py runserver

# Migrations
python manage.py makemigrations
python manage.py migrate
python manage.py sqlmigrate polls 0001
python manage.py showmigrations

# Shell and superuser
python manage.py shell
python manage.py createsuperuser

# Tests
python manage.py test
python manage.py test --keepdb

# Static files and checks
python manage.py collectstatic
python manage.py check --deploy
```

## Model Example

```python
# polls/models.py
from django.db import models

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.question_text
```

## Best Practices

- Put business logic in models/services, keep views thin
- Use get_object_or_404 and querysets for safety
- Run check --deploy before shipping to catch insecure settings
- Set DEBUG=False, SECURE_SSL_REDIRECT, and proper ALLOWED_HOSTS in prod
- Use collectstatic with a CDN or S3-backed static storage
- Prefer select_related/prefetch_related to avoid N+1 queries

## Capabilities

### django-project
Scaffold projects and apps, run the dev server.

**Commands:**
- `django-admin startproject mysite .`
- `python manage.py startapp polls`
- `python manage.py runserver`
- `python manage.py check`
- `python manage.py collectstatic`

**Examples:**
- django-admin startproject config .
- python manage.py runserver 0.0.0.0:8000
- python manage.py check --deploy

### django-orm
Create and apply migrations, use the ORM shell.

**Commands:**
- `python manage.py makemigrations`
- `python manage.py migrate`
- `python manage.py sqlmigrate polls 0001`
- `python manage.py shell`
- `python manage.py createsuperuser`

**Examples:**
- python manage.py makemigrations polls
- python manage.py migrate --plan
- python manage.py sqlmigrate polls 0001_initial

### django-testing
Run the Django test suite.

**Commands:**
- `python manage.py test`
- `python manage.py test polls.tests.TestQuestion`
- `python manage.py test --keepdb`
- `python manage.py test --parallel`

**Examples:**
- python manage.py test polls --verbosity 2
- python manage.py test --tag=slow
