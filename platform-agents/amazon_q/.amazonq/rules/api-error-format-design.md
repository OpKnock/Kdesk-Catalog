# Api Error Format Design

Designs error formats and schemas: RFC 9457 problem details modeling, status mapping, and OpenAPI error components.

## Instructions

# API Error (Format Design)

Designs the error contract before implementation: formats, status mapping, and reusable schemas.

## When to Use
- Greenfield API error design
- Standardizing across services
- Defining what clients can rely on

## Real Commands

```bash
# Draft the format
node -e "const p={type:'https://api.example/errors',title:'Bad Request',status:400,code:'VALIDATION_1001',instance:'/api/users'};console.log(JSON.stringify(p,null,2))"

# Define status mapping
node -e "const map=[[400,'VALIDATION'],[401,'AUTH'],[403,'FORBIDDEN'],[404,'NOT_FOUND'],[429,'RATE']];console.log(map.map(x=>x.join(' -> ')).join('\n'))"

# Reusable schema
node -e "const s={components:{schemas:{Problem:{type:'object',properties:{title:{type:'string'},status:{type:'integer'},code:{type:'string'}}}}}};console.log(JSON.stringify(s,null,2))"
```

## Design Principles
- Machine-readable `code`, human-readable `title`
- Status codes map to error families
- `instance` points to the failing request

## Testing
Validate the spec with swagger-cli after adding error components.

## Best Practices
- Keep error responses in the spec from day one
- Add examples per status code

## Capabilities

### format-design
Model problem-details schemas and map domain codes to HTTP statuses

**Commands:**
- `node -e "const p={type:'https://api.example/errors',title:'Bad Request',status:400,code:'VALIDATION_1001',instance:'/api/users'};console.log(JSON.stringify(p,null,2))"`
- `python -c "import json;p={'title':'Not Found','status':404,'code':'NOT_FOUND'};print(json.dumps(p))"`
- `node -e "const map=[[400,'VALIDATION'],[401,'AUTH'],[403,'FORBIDDEN'],[404,'NOT_FOUND'],[409,'CONFLICT'],[429,'RATE'],[500,'INTERNAL'],[502,'UPSTREAM']];console.log(map.map(x=>x.join(' -> ')).join('\n'))"`
- `node -e "console.log(['client','server','integration'].map(f=>f+'_errors').join(' '))"`
- `python -c "print({400:'VALIDATION_1XXX',500:'INTERNAL_5XXX'})"`

**Examples:**
- node -e "const map=[[400,'VALIDATION'],[401,'AUTH'],[403,'FORBIDDEN'],[404,'NOT_FOUND'],[429,'RATE']];console.log(map.map(x=>x.join(' -> ')).join('\n'))"
- node -e "const p={title:'Conflict',status:409,code:'CONFLICT_2001'};console.log(JSON.stringify(p))"
- python -c "import json;print(json.dumps({'status':503,'code':'UPSTREAM_9001'}))"

### schema-authoring
Author reusable error schemas in OpenAPI components

**Commands:**
- `node -e "const s={components:{schemas:{Problem:{type:'object',properties:{title:{type:'string'},status:{type:'integer'},code:{type:'string'}}}},required:['title','status','code']}};console.log(JSON.stringify(s,null,2))"`
- `swagger-cli validate openapi.yaml`
- `redocly lint openapi.yaml`
- `npx @stoplight/spectral-cli lint openapi.yaml`
- `node -e "const s={Problem:{type:'object'}};console.log(Object.keys(s)[0]) "`

**Examples:**
- node -e "const s={components:{schemas:{Problem:{type:'object',properties:{title:{type:'string'},status:{type:'integer'},code:{type:'string'}}}}}};console.log(JSON.stringify(s,null,2))"
- swagger-cli validate openapi.yaml && redocly lint openapi.yaml
- npx @stoplight/spectral-cli lint --ruleset error-rules.yaml openapi.yaml