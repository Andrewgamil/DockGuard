# URL Shortener Runbook

## Service Overview

The URL Shortener service is a containerized application that:
- Shortens long URLs into short codes
- Stores mappings in SQLite database
- Redirects short codes to original URLs
- Exposes Prometheus metrics for monitoring

## Architecture

```
+-----------+      +-------------+      +-----------+
| urlshort  | ---> | Prometheus  | ---> | Grafana   |
| (FastAPI) |      | (scrapes /metrics) | (dashboards)
+-----------+      +-------------+      +-----------+
      |
      v
   SQLite (volume)
```

## Service Endpoints

- `POST /shorten` - Create a short URL
- `GET /{short_code}` - Redirect to original URL
- `GET /metrics` - Prometheus metrics endpoint

## Monitoring

### Prometheus
- URL: http://localhost:9090
- Scrapes: `http://urlshort:8080/metrics` every 15 seconds

### Grafana
- URL: http://localhost:3000
- Default credentials: admin/admin
- Dashboard: "URL Shortener Monitoring"

### Key Metrics

- `urlshort_created_total` - Total URLs shortened
- `urlshort_redirects_total` - Total redirects
- `urlshort_404_total` - Total 404 errors
- `urlshort_request_latency_seconds` - Request latency histogram

## Common Operations

### Start Services

```bash
docker-compose up -d
```

### Stop Services

```bash
docker-compose down
```

### View Logs

```bash
docker-compose logs -f urlshort
docker-compose logs -f prometheus
docker-compose logs -f grafana
```

### Backup Database

```bash
cd db
chmod +x backup.sh
./backup.sh
```

### Restore Database

```bash
cd db
chmod +x restore.sh
./restore.sh <backup_file>
```

### Run Integration Tests

```bash
chmod +x infra/spinup-and-test.sh
./infra/spinup-and-test.sh
```

### Generate Traffic

```bash
cd infra
python3 generate_traffic.py [num_requests] [num_threads]
```

## Troubleshooting

### Service Not Starting

1. Check Docker is running: `docker ps`
2. Check logs: `docker-compose logs urlshort`
3. Verify ports are not in use: `netstat -an | grep 8080`

### Database Issues

1. Check volume exists: `docker volume ls`
2. Verify database file: `docker exec urlshort ls -la /app/data/`
3. Restore from backup if needed

### Metrics Not Appearing

1. Verify service is running: `curl http://localhost:8080/metrics`
2. Check Prometheus targets: http://localhost:9090/targets
3. Verify network connectivity between containers

### High Latency

1. Check Grafana dashboard for latency trends
2. Review service logs for errors
3. Check database size and performance
4. Consider database optimization or migration to PostgreSQL

## Health Checks

### Service Health

```bash
curl http://localhost:8080/metrics
```

### Prometheus Health

```bash
curl http://localhost:9090/-/healthy
```

### Grafana Health

```bash
curl http://localhost:3000/api/health
```

## Scaling Considerations

- Current setup uses SQLite (single instance)
- For production, consider:
  - PostgreSQL for database
  - Multiple service instances behind load balancer
  - Redis for caching frequently accessed URLs
  - CDN for static assets

## Security Notes

- Service runs as non-root user
- Database stored in Docker volume
- No authentication implemented (add for production)
- Consider rate limiting for production use

