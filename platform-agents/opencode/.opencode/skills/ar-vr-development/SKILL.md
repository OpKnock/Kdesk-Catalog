---
name: "ar-vr-development"
description: "Develops AR/VR experiences: Three.js scene building with Vite, glTF asset optimization with gltf-transform, Blender headless rendering, and WebXR deployment. Use when working with threejs setup, asset pipeline or when the user mentions threejs setup, asset pipeline."
---

Develops AR/VR experiences: Three.js scene building with Vite, glTF asset optimization with gltf-transform, Blender headless rendering, and WebXR deployment.

## Agentic Workflow: Read -> Reason -> Act (ar-vr-development)

You are **ar-vr-development** (emerging) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — emerging context for `ar-vr-development`
- Domain: Develops AR/VR experiences: Three.js scene building with Vite, glTF asset optimization with gltf-transform, Blender headless rendering, and WebXR deployment.
- **threejs-setup**: Scaffold and build Three.js scenes — `npm create vite@latest my-scene -- --template vanilla`
- **asset-pipeline**: Optimize 3D assets for the web — `npm install -g @gltf-transform/cli`
- Check `knowledge` and `prerequisites: unity, unreal, blender, three-js`

### 2. Reason — think for `ar-vr-development`
- For `threejs-setup`: Scaffold and build Three.js scenes — decide which checks to run
- For `asset-pipeline`: Optimize 3D assets for the web — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `ar-vr-development` tools
- Tools: `Glob`, `Grep`, `Read`, `Bash`, `Npx` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `ar-vr-development:b474403f`

# AR/VR Development

Web-based AR/VR with Three.js.

## What This Skill Does
- Builds 3D scenes with Three.js
- Optimizes glTF assets for performance
- Deploys WebXR experiences

## When to Use
- Web AR/VR prototypes
- 3D product visualization
- Immersive training demos

## Real Commands

```bash
npm create vite@latest my-scene -- --template vanilla
npm install three @types/three
npx vite build
npm install -g @gltf-transform/cli
gltf-transform optimize model.glb -o model-optimized.glb
```

## Scene Example

```js
import * as THREE from 'three';
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(75, innerWidth / innerHeight, 0.1, 1000);
const renderer = new THREE.WebGLRenderer();
renderer.setSize(innerWidth, innerHeight);
document.body.appendChild(renderer.domElement);
```

## Testing
- Inspect asset sizes before deploy
- Verify Draco decoding at runtime
- Test with WebXR device emulation


## Best Practices
- Compress glTF with draco
- Use LODs for complex scenes
- Keep framerates above 60fps on target devices

## Capabilities

### threejs-setup
Scaffold and build Three.js scenes

**Parameters:**
- `template` (string): Vite template name
- `asset` (string): 3D asset file to load
- `output-dir` (string): Build output directory

**Commands:**
- `npm create vite@latest my-scene -- --template vanilla`
- `npm install three @types/three`
- `npm install vite`
- `npx vite build`
- `npx vite preview`

**Examples:**
- vite scaffold starts a vanilla JS project
- npm install three adds the 3D engine
- vite build bundles the scene for production

### asset-pipeline
Optimize 3D assets for the web

**Parameters:**
- `input` (string): Input glTF file
- `output` (string): Optimized output file
- `compression` (string): draco, meshopt

**Commands:**
- `npm install -g @gltf-transform/cli`
- `gltf-transform optimize model.glb -o model-optimized.glb`
- `gltf-transform draco model.glb model-draco.glb`
- `gltf-transform inspect model.glb`
- `blender -b scene.blend -o //render -E CYCLES -f 1`

**Examples:**
- gltf-transform optimize reduces file size
- gltf-transform draco compresses geometry
- blender -b renders headlessly

## References
- [Three.js Docs](https://threejs.org/docs/)
- [gltf-transform Docs](https://gltf-transform.dev/)
