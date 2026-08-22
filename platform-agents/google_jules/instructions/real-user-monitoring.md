# Real User Monitoring

Capture real-user Core Web Vitals with Grafana Faro, run Lighthouse lab audits, and correlate field versus lab performance signals.

## Instructions

# Real User Monitoring

RUM captures how actual browsers experience your app: LCP, CLS, INP, errors and page loads.

## What this skill does

- Instruments web apps with Faro SDK
- Tracks Core Web Vitals
- Runs lighthouse as a lab baseline

## When to use

- Performance budgets and alerting
- Comparing lab vs field data

## Real commands

```bash
# Instrument
npm install @grafana/faro-web-sdk @grafana/faro-web-tracing
npm install web-vitals

# Lab check
npx lighthouse https://staging.your-app.test --output=json --output-path=report.json
npx lighthouse https://staging.your-app.test --preset=desktop --quiet
```

## Faro init

```js
import { initializeFaro } from '@grafana/faro-web-sdk';
import { TracingInstrumentation } from '@grafana/faro-web-tracing';

initializeFaro({
  url: 'https://faro-collector.staging.your-app.test/collect',
  app: { name: 'shop-web', version: '1.2.0' },
  instrumentations: [new TracingInstrumentation()],
});
```

## Reading vitals

- LCP under 2.5s, CLS under 0.1, INP under 200ms

## Best practices

- Sample field data at scale (5-10%)
- Correlate lab (lighthouse) and field (RUM) numbers
- Alert on LCP regressions from releases

## Capabilities

### rum-instrumentation
Instrument web apps for RUM with Faro, measure Core Web Vitals, and run lighthouse audits.

**Commands:**
- `npm install @grafana/faro-web-sdk @grafana/faro-web-tracing`
- `npx lighthouse https://staging.your-app.test --output=json --output-path=report.json`
- `npx lighthouse https://staging.your-app.test --preset=desktop --quiet --output=json`
- `curl -s https://cdn.jsdelivr.net/npm/@grafana/faro-web-sdk/dist/core/index.js -o /dev/null -w "%{http_code}\n"`
- `npm install web-vitals`

**Examples:**
- npx lighthouse https://staging.your-app.test --output=json --output-path=report.json | jq '.categories.performance.score'
- npm install web-vitals
- npx lighthouse https://staging.your-app.test --preset=desktop
