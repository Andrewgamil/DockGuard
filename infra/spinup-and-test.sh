#!/bin/bash

# Integration test script
# This script starts the services and runs smoke tests

set -e

echo "=========================================="
echo "URL Shortener Integration Test"
echo "=========================================="

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[✓]${NC} $1"
}

print_error() {
    echo -e "${RED}[✗]${NC} $1"
}

print_info() {
    echo -e "${YELLOW}[i]${NC} $1"
}

# Check if docker-compose is available
if ! command -v docker-compose &> /dev/null; then
    print_error "docker-compose not found. Please install Docker Compose."
    exit 1
fi

# Start services
print_info "Starting services with docker-compose..."
docker-compose up -d --build

# Wait for services to be ready
print_info "Waiting for services to be ready..."
sleep 10

# Test 1: Check if service is responding
print_info "Test 1: Checking service health..."
if curl -s -f http://localhost:8080/metrics > /dev/null; then
    print_status "Service is responding"
else
    print_error "Service is not responding"
    docker-compose logs urlshort
    exit 1
fi

# Test 2: Create a short URL
print_info "Test 2: Creating a short URL..."
RESPONSE=$(curl -s -X POST http://localhost:8080/shorten \
    -H "Content-Type: application/json" \
    -d '{"url":"https://example.com"}')

if echo "$RESPONSE" | grep -q "short_code"; then
    SHORT_CODE=$(echo "$RESPONSE" | grep -o '"short_code":"[^"]*"' | cut -d'"' -f4)
    print_status "Short URL created: $SHORT_CODE"
else
    print_error "Failed to create short URL"
    echo "Response: $RESPONSE"
    docker-compose logs urlshort
    exit 1
fi

# Test 3: Follow redirect
print_info "Test 3: Testing redirect..."
REDIRECT_RESPONSE=$(curl -sI http://localhost:8080/$SHORT_CODE)
if echo "$REDIRECT_RESPONSE" | grep -q "302 Found"; then
    print_status "Redirect works correctly"
else
    print_error "Redirect failed"
    echo "Response: $REDIRECT_RESPONSE"
    exit 1
fi

# Test 4: Check metrics endpoint
print_info "Test 4: Checking metrics endpoint..."
METRICS=$(curl -s http://localhost:8080/metrics)
if echo "$METRICS" | grep -q "urlshort_created_total"; then
    print_status "Metrics endpoint is working"
else
    print_error "Metrics endpoint not working correctly"
    exit 1
fi

# Test 5: Check Prometheus
print_info "Test 5: Checking Prometheus..."
sleep 5
PROM_QUERY=$(curl -s 'http://localhost:9090/api/v1/query?query=urlshort_created_total')
if echo "$PROM_QUERY" | grep -q "success"; then
    print_status "Prometheus is scraping metrics"
else
    print_error "Prometheus query failed"
    echo "Response: $PROM_QUERY"
    exit 1
fi

# Test 6: Check Grafana
print_info "Test 6: Checking Grafana..."
if curl -s -f http://localhost:3000/api/health > /dev/null; then
    print_status "Grafana is running"
else
    print_error "Grafana is not responding"
    exit 1
fi

# Test 7: Test 404 handling
print_info "Test 7: Testing 404 handling..."
NOT_FOUND_RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8080/nonexistent123)
if [ "$NOT_FOUND_RESPONSE" == "404" ]; then
    print_status "404 handling works correctly"
else
    print_error "404 handling failed (got $NOT_FOUND_RESPONSE)"
    exit 1
fi

echo ""
echo "=========================================="
print_status "All integration tests passed!"
echo "=========================================="
echo ""
echo "Service URLs:"
echo "  - API: http://localhost:8080"
echo "  - Metrics: http://localhost:8080/metrics"
echo "  - Prometheus: http://localhost:9090"
echo "  - Grafana: http://localhost:3000 (admin/admin)"
echo ""
echo "To stop services, run: docker-compose down"

