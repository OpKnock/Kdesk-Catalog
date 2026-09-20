---
name: "graphql-graphene"
description: "GraphQL in Python with Graphene: define schema and resolvers with Python classes, integrate with Django/Flask, and run queries."
type: knowledge
triggers: ["graphql-graphene", "graphene-schema"]
---

# Graphql Graphene

GraphQL in Python with Graphene: define schema and resolvers with Python classes, integrate with Django/Flask, and run queries.

## Instructions

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
