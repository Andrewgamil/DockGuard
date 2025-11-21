# Quick Start Guide

## Prerequisites

- Docker Desktop installed and running
- Docker Compose installed (usually comes with Docker Desktop)

## Step 1: Start All Services

```bash
docker-compose up --build
```

This will:
- Build the URL shortener service
- Start Prometheus
- Start Grafana
- Create necessary volumes

## Step 2: Verify Services

Wait about 10-15 seconds for services to start, then:

1. **Service API**: http://localhost:8080/metrics
2. **Prometheus**: http://localhost:9090
3. **Grafana**: http://localhost:3000 (login: admin/admin)

## Step 3: Test the Service

### Create a Short URL

```bash
curl -X POST http://localhost:8080/shorten \
  -H "Content-Type: application/json" \
  -d '{"url":"https://example.com"}'
```

Response:
```json
{"short_code": "abc123"}
```

### Use the Short URL

```bash
curl -I http://localhost:8080/abc123
```

You should see a `302 Found` redirect.

## Step 4: View Metrics

1. Open Prometheus: http://localhost:9090
2. Try query: `urlshort_created_total`
3. Open Grafana: http://localhost:3000
4. Login with admin/admin
5. Go to Dashboards → URL Shortener Monitoring

## Step 5: Generate Traffic (Optional)

```bash
cd infra
python3 generate_traffic.py 50 5
```

This will create 50 URLs and access them with 5 threads.

## Step 6: Run Integration Tests

```bash
# On Linux/Mac
chmod +x infra/spinup-and-test.sh
./infra/spinup-and-test.sh

# On Windows (PowerShell)
.\infra\spinup-and-test.sh
```

## Stop Services

```bash
docker-compose down
```

To also remove volumes:

```bash
docker-compose down -v
```

## Troubleshooting

### Port Already in Use

If ports 8080, 9090, or 3000 are in use, you can modify `docker-compose.yml` to use different ports.

### Services Not Starting

Check logs:
```bash
docker-compose logs urlshort
docker-compose logs prometheus
docker-compose logs grafana
```

### Database Issues

The database is stored in a Docker volume. To reset:
```bash
docker-compose down -v
docker-compose up --build
```

