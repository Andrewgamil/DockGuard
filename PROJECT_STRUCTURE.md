# Project Structure

This document outlines the complete project structure and all files created.

## Directory Structure

```
DockGuard/
├── .github/
│   └── workflows/
│       └── ci.yml                    # CI/CD pipeline
├── db/
│   ├── backup.sh                     # Database backup script
│   ├── restore.sh                    # Database restore script
│   └── seed.sql                      # Sample seed data
├── docs/
│   ├── openapi.yaml                  # API documentation (OpenAPI 3.0)
│   └── runbook.md                    # Operations runbook
├── grafana/
│   └── provisioning/
│       ├── dashboards/
│       │   ├── dashboard.yml         # Dashboard provisioning config
│       │   └── urlshort-dashboard.json  # Main Grafana dashboard
│       └── datasources/
│           └── prometheus.yml         # Prometheus datasource config
├── infra/
│   ├── generate_traffic.py           # Traffic generator script
│   └── spinup-and-test.sh            # Integration test script
├── prometheus/
│   └── prometheus.yml                # Prometheus configuration
├── service/
│   ├── Dockerfile                    # Service container definition
│   ├── .dockerignore                 # Docker ignore patterns
│   ├── main.py                       # FastAPI application
│   ├── models.py                     # SQLModel database models
│   ├── requirements.txt              # Python dependencies
│   ├── requirements-test.txt         # Test dependencies
│   └── tests/
│       ├── __init__.py
│       └── test_main.py              # Unit tests
├── .gitignore                        # Git ignore patterns
├── docker-compose.yml                # Docker Compose orchestration
├── README.md                         # Main project documentation
├── QUICKSTART.md                     # Quick start guide
└── PROJECT_STRUCTURE.md              # This file
```

## Key Components

### Service (FastAPI)
- **main.py**: Main application with endpoints:
  - `POST /shorten` - Create short URL
  - `GET /{short_code}` - Redirect to original URL
  - `GET /metrics` - Prometheus metrics
- **models.py**: Database model (Link table)
- **Dockerfile**: Container image definition

### Monitoring
- **Prometheus**: Scrapes metrics from service every 15s
- **Grafana**: Pre-configured dashboard with:
  - URL creation rate
  - Redirect rate
  - 95th percentile latency
  - 404 error rate
  - Total counters
  - Latency distribution heatmap

### Database
- **SQLite**: Stored in Docker volume (`db_data`)
- **Backup/Restore**: Shell scripts for database operations
- **Seed data**: SQL file for sample data

### Testing
- **Unit tests**: pytest-based tests in `service/tests/`
- **Integration tests**: Automated smoke tests in `infra/spinup-and-test.sh`
- **Traffic generator**: Load testing script

### CI/CD
- **GitHub Actions**: Automated build and test pipeline

## Metrics Exposed

All metrics follow the naming convention: `urlshort_*`

- `urlshort_created_total` (Counter) - Total URLs shortened
- `urlshort_redirects_total` (Counter) - Total redirects
- `urlshort_404_total` (Counter) - Total 404 errors
- `urlshort_request_latency_seconds` (Histogram) - Request latency

## Service URLs

When running with `docker-compose up`:

- **Service API**: http://localhost:8080
- **Metrics**: http://localhost:8080/metrics
- **Prometheus**: http://localhost:9090
- **Grafana**: http://localhost:3000 (admin/admin)

## Next Steps

1. Start services: `docker-compose up --build`
2. Run tests: `./infra/spinup-and-test.sh`
3. Generate traffic: `python3 infra/generate_traffic.py`
4. View dashboard: http://localhost:3000

