---
trigger: glob
description: "Deep expertise in API governance programs: enterprise rulesets, standards publication, and measuring compliance adoption."
globs: ["**/*.go", "**/*.json", "**/*.py", "**/*.r", "**/*.sh", "**/*.{yaml,yml}"]
---

# api-governance-specialist

Deep expertise in API governance programs: enterprise rulesets, standards publication, and measuring compliance adoption.

## Instructions

# API Governance Specialist

Runs governance as a program with measurable adoption.

## When to Use
- Governance across many teams and APIs
- Need to prove standards adoption
- Tiered enforcement (warn vs error)

## Real Commands

```bash
# Aggregate findings
npx @stoplight/spectral-cli lint -r .spectral.yaml --format json specs/**/*.yaml > all.json

# Analyze by rule
node -e "const r=require('./all.json');const byRule={};r.forEach(x=>byRule[x.code]=(byRule[x.code]||0)+1);console.log(JSON.stringify(byRule,null,2))"

# Count specs
node -e "const fs=require('fs');const files=fs.readdirSync('specs').filter(f=>f.endsWith('.yaml'));console.log(files.length+' specs')"
```

## Governance Model
- Recommended tier: everyone
- Org tier: enterprise conventions
- Exception tier: documented waivers

## Testing
Track violations-per-spec quarterly and publish the trend.

## Best Practices
- Severity tiers keep momentum without blocking
- Waivers must be time-boxed

## Capabilities

### enterprise-rulesets
Maintain layered rulesets with severity tiers and exception flows

**Commands:**
- `npx @stoplight/spectral-cli lint -r .spectral.yaml --format json openapi.yaml > report.json`
- `npx @stoplight/spectral-cli lint -r .spectral.yaml --ignore-unknown-formats openapi.yaml`
- `python -c "import json;r=json.load(open('report.json'));print(len(r))"`
- `node -e "const r=require('./report.json');const byRule={};r.forEach(x=>byRule[x.code]=(byRule[x.code]||0)+1);console.log(JSON.stringify(byRule,null,2))"`
- `npx @stoplight/spectral-cli lint -r .spectral.yaml --fail-severity error openapi.yaml`

**Examples:**
- npx @stoplight/spectral-cli lint -r .spectral.yaml --format json openapi.yaml > report.json && node -e "const r=require('./report.json');console.log(r.length+' findings')"
- node -e "const r=require('./report.json');const byRule={};r.forEach(x=>byRule[x.code]=(byRule[x.code]||0)+1);console.log(JSON.stringify(byRule,null,2))"
- npx @stoplight/spectral-cli lint -r .spectral.yaml --fail-severity error openapi.yaml

### adoption-metrics
Measure governance adoption across specs and report trends

**Commands:**
- `npx @stoplight/spectral-cli lint -r .spectral.yaml --format json specs/**/*.yaml > all.json`
- `python -c "import json,glob;r=[];[r.extend(json.load(open(f))) for f in glob.glob('specs/*/*.json')]" 2>/dev/null || echo 'aggregate manually'`
- `node -e "const fs=require('fs');const files=fs.readdirSync('specs').filter(f=>f.endsWith('.yaml'));console.log(files.length+' specs')"`
- `node -e "const fs=require('fs');fs.readdirSync('specs').forEach(f=>{if(f.endsWith('.yaml'))console.log(f)}"`
- `python -c "print('compliance % = 100 - (violations / rules) * 100')"`

**Examples:**
- npx @stoplight/spectral-cli lint -r .spectral.yaml --format json specs/**/*.yaml > all.json
- node -e "const fs=require('fs');const files=fs.readdirSync('specs').filter(f=>f.endsWith('.yaml'));console.log(files.length+' specs')"
- python -c "import json;r=json.load(open('all.json'));print('violations:',len(r))"
