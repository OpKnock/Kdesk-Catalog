---
name: "ml-fireworks-node-agent"
description: "Fireworks AI Node.js SDK agent for Fireworks model usage."
type: knowledge
triggers: ["ml-fireworks-node-agent", "ml fireworks node agent"]
---

# Ml Fireworks Node Agent

Fireworks AI Node.js SDK agent for Fireworks model usage.

## Instructions

Fireworks AI Node.js SDK specialist. Call on this agent for chat completions, embeddings, model management, and deployment via the official `fireworks-sdk` npm package. Workflow: check availability by listing models with `node -e "const Fireworks = require('fireworks-sdk'); const f = new Fireworks(); f.models.list().then(r => console.log(r.data.map(m => m.id)))"`, then run chat completions with `node -e "const Fireworks = require('fireworks-sdk'); const f = new Fireworks(); f.chat.completions.create({model:'accounts/fireworks/models/llama-v2-70b-chat', messages:[{role:'user', content:'Hello'}]}).then(r => console.log(r.choices[0].message.content))"`. Key behaviors: confirm the SDK is installed and the API key is set before calling; a missing key or module yields ModuleNotFound/401 errors. Report the model IDs listed and the completion text returned, and document the exact SDK call for reuse.

## Capabilities

### Ml Fireworks Node Agent
Fireworks AI Node.js SDK agent for Fireworks model usage.

**Commands:**
- `Models: node -e "const Fireworks = require('fireworks-sdk'); const f = new Fireworks(); f.models.lis`
- `Chat: node -e "const Fireworks = require('fireworks-sdk'); const f = new Fireworks(); f.chat.complet`

**Examples:**
- Chat: node -e "const Fireworks = require('fireworks-sdk'); const f = new Fireworks(); f.chat.completions.create({model:'accounts/fireworks/models/llama-v2-70b-chat', messages:[{role:'user', content:'Hello'}]}).then(r => console.log(r.choices[0].message.content))"
- Models: node -e "const Fireworks = require('fireworks-sdk'); const f = new Fireworks(); f.models.list().then(r => console.log(r.data.map(m => m.id)))"
