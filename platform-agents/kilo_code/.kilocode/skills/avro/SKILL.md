---
name: "avro"
description: "Works with Apache Avro data serialization: schema authoring, avro-tools conversion, Python avro library usage, and schema evolution."
---

# Avro

Works with Apache Avro data serialization: schema authoring, avro-tools conversion, Python avro library usage, and schema evolution.

## Instructions

# Avro

## What this skill does

Works with Apache Avro serialization: writing schemas, converting data with avro-tools, reading/writing data files in Python, and testing schema evolution (resolution) between writer and reader schemas.

## When to use

- Serializing records for Kafka or data lakes (compact, typed, evolvable)
- Converting JSON lines to Avro for storage efficiency
- Verifying a schema change is backward compatible

## Real commands

```bash
# Inspect metadata
java -jar avro-tools.jar getmeta events.avro

# Convert Avro to JSON
java -jar avro-tools.jar tojson events.avro | head -5

# JSON to Avro
java -jar avro-tools.jar fromjson data.json --schema-file schema.avsc

# Generate sample data
java -jar avro-tools.jar random --schema-file user.avsc --count 100 sample.avro

# Python
pip install avro
python -c "import avro.schema; s=avro.schema.parse(open('user.avsc').read()); print(s.fullname)"
```

## Schema example

```json
{
  "type": "record",
  "name": "User",
  "namespace": "com.example",
  "fields": [
    {"name": "id", "type": "long"},
    {"name": "email", "type": "string"}
  ]
}
```

## Schema evolution

- Adding a field with a default is backward compatible
- Test resolution: `avro-tools tojson --schema-file reader_v2.avsc writer_v1.avro`

## Testing

- Round-trip: fromjson then tojson should reproduce input
- Run evolution checks in CI with both schema versions

## Best practices

- Never remove fields without defaults unless coordinated
- Store the writer schema in the .avro container header
- Use Avro IDs in a schema registry for Kafka payloads

## Capabilities

### avro-tools
Convert, inspect, and manipulate Avro data files.

**Commands:**
- `java -jar avro-tools.jar getmeta file.avro`
- `java -jar avro-tools.jar tojson file.avro`
- `java -jar avro-tools.jar fromjson data.json --schema-file schema.avsc`
- `java -jar avro-tools.jar cat file.avro`
- `java -jar avro-tools.jar random --schema-file schema.avsc --count 10 test.avro`

**Examples:**
- java -jar avro-tools.jar tojson events.avro | head -5
- java -jar avro-tools.jar getmeta events.avro | head -20
- java -jar avro-tools.jar random --schema-file user.avsc --count 100 sample.avro

### python-avro
Serialize and deserialize Avro with the Python library.

**Commands:**
- `pip install avro`
- `python -c "import avro; print(avro.__version__)"`
- `python -c "from avro.datafile import DataFileWriter; from avro.io import DatumWriter; print('ok')"`
- `python -m avro`

**Examples:**
- python -c "import avro.schema; s=avro.schema.parse(open('user.avsc').read()); print(s.fullname)"
- python -c "from avro import schema; print(schema.parse('\"string\"').fullname)"
- python -c "import avro.datafile as d; print([x for x in dir(d) if 'Writer' in x or 'Reader' in x])"

### schema-evolution
Test schema resolution between writer and reader schemas.

**Commands:**
- `java -jar avro-tools.jar --version`
- `java -jar avro-tools.jar tojson --schema-file reader.avsc writer.avro`
- `python -c "import avro.io as io; print([x for x in dir(io) if 'Reader' in x])"`
- `java -jar avro-tools.jar compile schema schema.avsc /tmp/out`

**Examples:**
- java -jar avro-tools.jar tojson --schema-file reader_v2.avsc writer_v1.avro | head -3
- python -c "from avro.io import DatumReader; r=DatumReader(reader_schema, writer_schema); print('resolution ready')"
- java -jar avro-tools.jar compile schema v2.avsc gen/
