# Test Your Running Project

## Your services are running! Here's how to test them:

### 1. Test URL Shortening

Open a **NEW PowerShell window** and run:

```powershell
# Create a short URL
curl -X POST http://localhost:8080/shorten -H "Content-Type: application/json" -d '{\"url\":\"https://example.com\"}'
```

You should get a response like:
```json
{"short_code":"abc123"}
```

### 2. Test the Redirect

Use the short_code from step 1:

```powershell
curl -I http://localhost:8080/YOUR_SHORT_CODE
```

Replace `YOUR_SHORT_CODE` with the code you got (e.g., `abc123`)

You should see: `HTTP/1.1 302 Found`

### 3. Check Metrics

Open in browser: http://localhost:8080/metrics

You should see Prometheus metrics including:
- `urlshort_created_total`
- `urlshort_redirects_total`
- `urlshort_404_total`
- `urlshort_request_latency_seconds`

### 4. View Prometheus

Open in browser: http://localhost:9090

- Click "Status" → "Targets" to see if urlshort is being scraped (should show UP)
- Go to "Graph" tab
- Try query: `urlshort_created_total`
- Click "Execute"

### 5. View Grafana Dashboard

Open in browser: http://localhost:3000

- Login with:
  - Username: `admin`
  - Password: `admin`
- Go to: **Dashboards** → **URL Shortener Monitoring**
- You should see graphs showing your metrics!

### 6. Generate Some Traffic

In PowerShell:

```powershell
cd C:\Users\andre\Downloads\task\infra
python generate_traffic.py 20 5
```

This will create 20 URLs and access them. Then watch the Grafana dashboard update in real-time!

---

## Keep Services Running

The services will keep running in your PowerShell window. You'll see logs scrolling.

**To stop services:**
- Press `Ctrl + C` in the PowerShell window where docker-compose is running

**To stop and remove everything:**
```powershell
docker-compose down
```

**To start again later:**
```powershell
docker-compose up
```

(No need for `--build` unless you changed code)

---

## Success Indicators

✅ All three containers running
✅ Prometheus scraping metrics (you see GET /metrics requests)
✅ Grafana dashboard accessible
✅ Can create and redirect URLs
✅ Metrics visible in Prometheus
✅ Dashboard shows data in Grafana

**Your project is fully functional! 🎉**

