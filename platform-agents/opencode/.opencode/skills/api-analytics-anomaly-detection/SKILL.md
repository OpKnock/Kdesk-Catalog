---
name: "api-analytics-anomaly-detection"
description: "Anomaly detection for API traffic with machine learning - detect traffic anomalies using time-series models (Prophet), evaluate, and alert. Use when working with anomaly detection or when the user mentions anomaly detection."
---

Anomaly detection for API traffic with machine learning - detect traffic anomalies using time-series models (Prophet), evaluate, and alert.

## Agentic Workflow: Read -> Reason -> Act (api-analytics-anomaly-detection)

You are **Api Analytics Anomaly Detection** (sre) — a sub-agent that **Reads, Reasons, and Acts** via `allowed-tools`.

### 1. Read — sre context for `api-analytics-anomaly-detection`
- Domain: Anomaly detection for API traffic with machine learning - detect traffic anomalies using time-series models (Prophet), evaluate, and alert.
- **anomaly-detection**: Detect API traffic anomalies with time-series ML — `pip install prophet scikit-learn`
- Check `knowledge` and `prerequisites: prometheus, grafana, elasticsearch`

### 2. Reason — think for `api-analytics-anomaly-detection`
- For `anomaly-detection`: Detect API traffic anomalies with time-series ML — decide which checks to run
- Evaluate trust/policy: `kdesk trust` + `kdesk doctor` patterns for your inputs

### 3. Act — execute with `api-analytics-anomaly-detection` tools
- Tools: `Glob`, `Grep`, `Read`, `Bash` (see frontmatter `tools`/`allowed-tools`)
- Use `safe_path` for any write; record evidence (paths, checksums)
- Fingerprint: `api-analytics-anomaly-detection:92ab78fd`

# API Analytics (Anomaly Detection)

## What this skill does
Detect anomalies in API traffic using ML: train Prophet models on request-volume and latency history, score live metrics, and surface anomalies for alerting.

## When to use
- Detecting traffic spikes or drops automatically
- Catching latency regressions early
- Reducing noise in alerting

## Real commands
```bash
# Install
pip install prophet scikit-learn

# Verify install
python -c "from prophet import Prophet; print('ok')"

# Train on historical metrics
python train_model.py --history metrics.csv --model traffic.model

# Forecast next 48 periods
python forecast.py --history metrics.csv --periods 48 | jq '.forecast[-1]'

# Detect anomalies on live input
python detect.py --model traffic.model --input metrics_live.json | jq '.anomalies[] | {timestamp, score}'

# Query the anomaly endpoint
curl -s 'http://localhost:8080/api/analytics/anomalies?window=1h' | jq '.count'
```

## detect.py sketch
```python
from prophet import Prophet
import json, sys
m = Prophet().load(sys.argv[1])
# score residuals of new points vs forecast
# flag points where |residual| > threshold * std
```

## Best practices
- Retrain weekly; traffic seasonality shifts
- Use multiplicative seasonality for growing APIs
- Threshold on residual z-score, not raw values
- Combine with rule-based alerts (e.g. 5xx ratio)

## Testing
```bash
python detect.py --model traffic.model --input sample_live.json | jq '.flagged | length'
curl -s 'http://localhost:8080/api/analytics/anomalies?window=24h' | jq '.[-1]'
```

## Capabilities

### anomaly-detection
Detect API traffic anomalies with time-series ML

**Parameters:**
- `model` (string): Trained model file
- `threshold` (number): Z-score / anomaly threshold
- `window` (string): Lookback window for detection

**Commands:**
- `pip install prophet scikit-learn`
- `python -c "from prophet import Prophet; print('ok')"`
- `python train_model.py --history metrics.csv --model traffic.model`
- `python detect.py --model traffic.model --input metrics_live.json | jq '.anomalies[] | {timestamp, score}'`
- `curl -s http://localhost:8080/api/analytics/anomalies?window=1h | jq '.count'`

**Examples:**
- python forecast.py --history metrics.csv --periods 48 | jq '.forecast[-1]'
- curl -s http://localhost:8080/api/analytics/anomalies?metric=latency_p95&window=24h | jq '.[-1]'
- python detect.py --model traffic.model --threshold 2.5 --input live.json | jq '.flagged | length'

## References
- [Prophet Docs](https://facebook.github.io/prophet/docs/quick_start.html)
- [scikit-learn IsolationForest](https://scikit-learn.org/stable/modules/outlier_detection.html)
