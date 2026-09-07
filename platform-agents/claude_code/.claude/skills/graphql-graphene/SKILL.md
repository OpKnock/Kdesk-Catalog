---
name: "graphql-graphene"
description: "GraphQL in Python with Graphene: define schema and resolvers with Python classes, integrate with Django/Flask, and run queries. Use when working with graphene schema, api or when the user mentions graphene schema, api."
license: "MIT"
compatibility: "Requires pip, python. Needs network access."
metadata: {"author": "Kdesk", "version": "2.0.0", "category": "api"}
allowed-tools: "Glob Grep Read Bash(curl:*) Bash(pip:*) Bash(python:*)"
---

GraphQL in Python with Graphene: define schema and resolvers with Python classes, integrate with Django/Flask, and run queries.

## Agentic Workflow: Read -> Reason -> Act

You are an AI agent that **Reads, Reasons, and Acts** — not a chatbot. Follow this loop for every task:

### 1. Read
Gather context before acting:
- Read relevant files with `Read`, `Glob`, `Grep` (never assume structure)
- Domain context: `pip install graphene django-graphql-graphene`
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

# GraphQL Graphene

## What this skill does

Graphene builds GraphQL schemas in Python with classes: ObjectType for objects, resolvers as methods, and Schema for the root. Graphene-Django adds ORM-friendly fields.

## When to use

- Adding GraphQL to a Python/Django service
- Reusing existing ORM models in a graph
- Python teams that want code-first GraphQL

## Real commands

```bash
# Install
pip install graphene graphene-django

# Inline smoke test
python -c "import graphene; s=graphene.Schema(query=Query); print(s.execute('{ hello }').data)"

# Export SDL for client tooling
python manage.py graphql_schema --schema myapp.schema.schema --out schema.graphql

# Serve and query
python manage.py runserver
curl -s -X POST http://localhost:8000/graphql -H 'Content-Type: application/json' -d '{"query":"{ hello }"}' | jq
```

## Schema example

```python
import graphene

class Order(graphene.ObjectType):
    id = graphene.ID()
    status = graphene.String()

class Query(graphene.ObjectType):
    hello = graphene.String()
    order = graphene.Field(Order, id=graphene.ID(required=True))

    def resolve_hello(self, info):
        return "world"

    def resolve_order(self, info, id):
        return Orders.get(id)  # None -> graphene returns null

schema = graphene.Schema(query=Query)
```

## Testing

```bash
# Execute without HTTP
python -c "from myapp.schema import schema; r=schema.execute('{ order(id: \"1\") { id status } }'); print(r.data, r.errors)"
```

## Best practices

- Code-first: keep schema classes near the models they expose.
- Use graphene-django's DjangoObjectType to avoid hand-written fields.
- Export SDL to schema.graphql for the client pipeline.
- Resolve N+1 queries with select_related/prefetch_related.
- Return errors as GraphQL errors, not Python exceptions leaking.

## Capabilities

### graphene-schema
Define Graphene schemas, wire Django/Flask integration, and test queries.

**Parameters:**
- `schema-module` (string): Python module path to the Schema
- `output-file` (string): SDL export path
- `endpoint` (string): GraphQL HTTP endpoint

**Commands:**
- `pip install graphene django-graphql-graphene`
- `python -c "import graphene; s=graphene.Schema(query=Query); print(s.execute('{ hello }').data)"`
- `python manage.py graphql_schema --schema myapp.schema.schema --out schema.graphql`
- `python manage.py runserver`
- `curl -s -X POST http://localhost:8000/graphql -H 'Content-Type: application/json' -d '{"query":"{ hello }"}' | jq`

**Examples:**
- python -c "import graphene; s=graphene.Schema(query=Query); print(s.execute('{ hello }').data)"
- python manage.py graphql_schema --schema myapp.schema.schema --out schema.graphql
- curl -s -X POST http://localhost:8000/graphql -H 'Content-Type: application/json' -d '{"query":"{ hello }"}' | jq

## References
- [Graphene docs](https://docs.graphene-python.org/)
- [Graphene Django](https://docs.graphene-python.org/projects/django/en/latest/)
