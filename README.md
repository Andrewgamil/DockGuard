# Monitoring a Containerized URL Shortener Webservice

## Project Name

URL Shortener Monitoring

---

## Project Idea

Build, containerize, and monitor a functional URL shortener webservice. The full stack — application + monitoring (Prometheus, Grafana) — runs locally using Docker.

---

## Table of Contents

* [Project Overview](#project-overview)
* [Team Members](#team-members)
* [Tech Stack](#tech-stack)
* [Architecture](#architecture)
* [Component Ownership (5 equal, independent tasks)](#component-ownership-5-equal-independent-tasks)
* [Repository Layout](#repository-layout)
* [Getting Started (Quickstart)](#getting-started-quickstart)
* [Running Locally (development)](#running-locally-development)
* [Testing & Verification](#testing--verification)
* [Monitoring & Dashboards](#monitoring--dashboards)
* [Development Workflow & PR Checklist](#development-workflow--pr-checklist)
* [Roadmap & Next Steps](#roadmap--next-steps)
* [Contributing](#contributing)
* [License & Contact](#license--contact)

---

## Project Overview

This repository contains a containerized URL shortener service instrumented for monitoring. The service will:

* shorten long URLs,
* persist mappings,
* redirect short codes to long URLs,
* expose Prometheus-compatible metrics,
* be visualized and alerted on via Grafana.

---


## Team Members (pentaRae)

* mohamed yousery 
* mohamed youssef 
* kirolos medhat 
* dania momen 
* andrew gamil 

---

## Instructor

* IslamReda

---

## Project Files

You can find the full project files here:

[https://drive.google.com/drive/folders/1jR7lZjUpiV5e8a4LY72g0HVObMfwfbnY?usp=sharing](https://drive.google.com/drive/folders/1jR7lZjUpiV5e8a4LY72g0HVObMfwfbnY?usp=sharing)

---

## Tech Stack

* Docker & Docker Compose
* Web framework: Flask (Python) **or** Express (Node.js)
* Database: SQLite (local development)
* Monitoring: Prometheus
* Visualization & alerting: Grafana

---

## Architecture

All services run on a local Docker network and communicate over service hostnames.

```
+-----------+      +-------------+      +-----------+
| urlshort  | ---> | Prometheus  | ---> | Grafana   |
| (Flask)   |      | (scrapes /metrics) | (dashboards)
+-----------+      +-------------+      +-----------+
      |
      v
   SQLite (named volume)
```

Prometheus scrapes the service at `http://urlshort:8080/metrics`.

---

## Repository Layout

```
/
├─ service/                # Flask/Express app, Dockerfile, tests
├─ db/                     # migrations, sample.db, backup scripts
├─ prometheus/             # prometheus.yml, mock exporter
├─ grafana/                # provisioning, dashboards, alerts
├─ infra/                  # docker-compose.yml, volumes, scripts
├─ docs/                   # runbook, API contract (openapi.yaml)
└─ .github/workflows/      # CI pipeline
```


## Work Plan

1. Research & Analysis

   * Audience personas
2. Visual Identity

   * Logo design
3. Main Designs

   * Poster
4. Complementary Products
5. Review & Finalization
6. Final Presentation

---

## Roles & Responsibilities

# Component Ownership (5 equal, independent tasks)

Each team member owns one independently testable component. Tasks are balanced so workload is roughly equal.

### 1 — Service Developer (Backend) — mohamed yousery

**Deliverables**

* Service implementation with endpoints:

  * `POST /shorten` → `{ "short_code": "abc123" }`
  * `GET /{short_code}` → 302 redirect or 404
  * `GET /metrics` → Prometheus exposition
* Unit tests, `Dockerfile`, `openapi.yaml`, `seed.sql` (sample data).
  **Branch**: `feature/service-<your-name>`

---

### 2 — Persistence & Database — mohamed youssef

**Deliverables**

* DB schema & migrations
* `backup.sh` / `restore.sh`
* Docker volume mapping recommendations and `sample.db`
* DB helper module for service consumption
  **Branch**: `feature/db-<your-name>`

---

### 3 — Prometheus Integrator (Metrics) — kirolos medhat

**Deliverables**

* `prometheus.yml` config to scrape `urlshort:8080`
* Instrumentation naming conventions:

  * `urlshort_created_total`
  * `urlshort_redirects_total`
  * `urlshort_404_total`
  * `urlshort_request_latency_seconds` (histogram)
* `verify_metrics.sh` and a mock exporter for parallel work
  **Branch**: `feature/prometheus-<your-name>`

---

### 4 — Grafana & Alerts (Dashboards) — dania momen

**Deliverables**

* Grafana provisioning + `dashboard.json` with panels:

  * Creation rate, redirect rate, 95th percentile latency, 404 rate
* Alert rules for latency and error spikes
* `generate_traffic.py` to simulate load
  **Branch**: `feature/grafana-<your-name>`

---

### 5 — Orchestration, CI & Docs (Integration + QA) — andrew gamil

**Deliverables**

* `docker-compose.yml` wiring `urlshort`, `prometheus`, `grafana`, volumes
* `spinup-and-test.sh` integration test script
* CI pipeline (`.github/workflows/ci.yml`)
* Final `README.md`, runbook, PR templates
  **Branch**: `feature/integration-<your-name>`

---

---

## KPIs (Key Performance Indicators)

* Response time (p95, p99)
* System uptime / availability
* Requests per second (throughput)
* Error rate (4xx / 5xx, 404s)
* User adoption rate (number of shortened URLs / active users)

---



---

## License

This project is licensed under the MIT License.


---

---

## Getting Started (Quickstart)

### Prerequisites

* Docker & Docker Compose installed
* (Optional) Python 3.11+ or Node 18+ for local development

### Quickstart

```bash
git clone https://github.com/<your-org>/urlshort-monitoring.git
cd urlshort-monitoring
docker-compose up --build
```

* Service API: `http://localhost:8080`
* Prometheus UI: `http://localhost:9090`
* Grafana UI: `http://localhost:3000`

---

## Running Locally (development)

Build and run the service image:

```bash
docker build -t urlshort ./service
docker run --rm -p 8080:8080 -v "$(pwd)/db:/data" --name urlshort urlshort
```

Start monitoring components:

```bash
docker-compose up -d prometheus grafana
```

---

## Testing & Verification

The Integration owner should automate these checks in `spinup-and-test.sh`.

1. Create a short URL:

```bash
curl -s -X POST http://localhost:8080/shorten \
  -H "Content-Type: application/json" \
  -d '{"url":"https://example.com"}'
# expected: {"short_code":"abc123"}
```

2. Follow redirect:

```bash
curl -sI http://localhost:8080/abc123
# expected: HTTP/1.1 302 Found + Location header
```

3. Metrics present:

```bash
curl http://localhost:8080/metrics | head
# expected: Prometheus exposition lines including custom metrics
```

4. Prometheus query:

```bash
curl 'http://localhost:9090/api/v1/query?query=urlshort_created_total'
```

---

## Monitoring & Dashboards

**Prometheus**

* Scrape target: `urlshort:8080/metrics`
* Example `prometheus.yml` snippet:

```yaml
global:
  scrape_interval: 15s
scrape_configs:
  - job_name: 'urlshort'
    static_configs:
      - targets: ['urlshort:8080']
```

**Grafana**

* Panels to include:

  * `rate(urlshort_created_total[5m])`
  * `rate(urlshort_redirects_total[5m])`
  * `histogram_quantile(0.95, sum(rate(urlshort_request_latency_seconds_bucket[5m])) by (le))`
  * `rate(urlshort_404_total[5m])`
* Alerts:

  * sustained high 95th percentile latency (example threshold: > 1s)
  * sudden spike in 404 rate

---

## Development Workflow & PR Checklist

* Branching: `feature/<component>-<your-name>`
* PR must include:

  * Build proof (`docker build` command output or CI run)
  * Unit tests and results
  * README updates for that component
  * Integration smoke tests (curl commands) and expected output
  * One other teammate assigned to review and sign off

---

## Roadmap & Next Steps

* MVP: Service + Prometheus + Grafana + dashboard + CI integration
* Next: move from SQLite → Postgres (HA), add alert routing (Slack/Email), add auth for Grafana, run e2e load tests, add healthchecks and readiness probes.

---

