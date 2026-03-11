# S8.3 — Metrics and Monitoring: Design

## Module: `ops/metrics.py`

### Class: MetricsCollector
- Thread-safe counters and gauges.
- `get_all() -> dict` returns current metrics.
- Middleware for API latency tracking.

### Dependencies
- Standalone; integrated into stream receivers and API middleware.
