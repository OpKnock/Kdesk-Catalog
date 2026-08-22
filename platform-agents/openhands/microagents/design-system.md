---
name: "design-system"
description: "Builds design systems: Storybook components, design tokens, Chromatic visual tests, and docs."
type: knowledge
triggers: ["design-system", "storybook-workflow"]
---

# design-system

Builds design systems: Storybook components, design tokens, Chromatic visual tests, and docs.

## Instructions

# Design System

Builds a component library with Storybook: stories, design tokens, visual
regression tests, and published docs.

## When to Use

- Establishing a shared component library
- Visual regression testing UI
- Distributing design tokens across platforms

## Real Commands

```bash
# Init Storybook in an existing project
sudo npx storybook@latest init --yes

# Dev server
sudo npm run storybook -- --port 6006

# Static build for publishing
sudo npm run build-storybook

# Visual tests with Chromatic
sudo npx chromatic --project-token=$CHROMATIC_TOKEN
sudo npx chromatic --exit-zero-on-changes --auto-accept-changes

# Accessibility addon
sudo npx storybook addon install @storybook/addon-a11y

# Tokens: transform to platforms
sudo npx style-dictionary build
```

## Story Example (Button.stories.tsx)

```tsx
export const Primary: Story = {
  args: { label: 'Click me', variant: 'primary' },
};
```

## Token Pipeline (tokens.json -> style-dictionary)

```json
{
  "color": { "primary": { "value": "#4f46e5" } },
  "spacing": { "md": { "value": "16px" } }
}
```

## Best Practices

- One story per component state; use args tables
- Add a11y checks to every story
- Keep tokens the single source of truth for colors/spacing
- Run Chromatic on every PR; review diffs visually
- Version the design system package and document migrations

## Example Response

Scaffolds the library, authors stories, runs Chromatic, and reports the visual
change set with links for review.

## Capabilities

### storybook-workflow
Create, test, and publish component libraries with Storybook

**Commands:**
- `npx storybook@latest init --yes`
- `npm run storybook -- --port 6006`
- `npm run build-storybook`
- `npx chromatic --project-token=$CHROMATIC_TOKEN --exit-zero-on-changes`
- `npx style-dictionary build`

**Examples:**
- npx storybook addon install @storybook/addon-a11y
- npx chromatic --auto-accept-changes
- npx tokens-transformer tokens.json tokens/
