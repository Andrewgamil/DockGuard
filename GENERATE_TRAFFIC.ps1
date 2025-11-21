# Traffic Generator Script for PowerShell
# This will create URLs and access them to generate metrics

Write-Host " Generating traffic to URL Shortener..." -ForegroundColor Cyan
Write-Host ""

$baseUrl = "http://localhost:8080"
$numRequests = 20
$shortCodes = @()


Write-Host "Phase 1: Creating $numRequests short URLs..." -ForegroundColor Yellow
for ($i = 1; $i -le $numRequests; $i++) {
    $url = "https://example.com/page$i"
    $body = @{url=$url} | ConvertTo-Json
    
    try {
        $response = Invoke-RestMethod -Uri "$baseUrl/shorten" -Method POST -ContentType "application/json" -Body $body
        $shortCodes += $response.short_code
        Write-Host "  Created URL $i/$numRequests : $($response.short_code)" -ForegroundColor Green
    } catch {
        Write-Host "  Failed to create URL $i" -ForegroundColor Red
    }
    
    Start-Sleep -Milliseconds 200
}

Write-Host ""
Write-Host " Created $($shortCodes.Count) short URLs" -ForegroundColor Green
Write-Host ""


Write-Host "Phase 2: Accessing short URLs..." -ForegroundColor Yellow
$accessCount = 0
foreach ($code in $shortCodes) {
    try {
        $response = Invoke-WebRequest -Uri "$baseUrl/$code" -MaximumRedirection 0 -ErrorAction Stop
        $accessCount++
    } catch {
        if ($_.Exception.Response.StatusCode -eq 302) {
            $accessCount++
        }
    }
    Start-Sleep -Milliseconds 100
}

Write-Host " Accessed $accessCount URLs" -ForegroundColor Green
Write-Host ""


Write-Host "Phase 3: Testing 404 handling..." -ForegroundColor Yellow
$fakeCodes = @("fake123", "nonexistent", "invalid999")
foreach ($code in $fakeCodes) {
    try {
        Invoke-WebRequest -Uri "$baseUrl/$code" -MaximumRedirection 0 -ErrorAction Stop
    } catch {
        if ($_.Exception.Response.StatusCode -eq 404) {
            Write-Host "   404 handled correctly for: $code" -ForegroundColor Green
        }
    }
}


Write-Host " Traffic generation complete!" -ForegroundColor Cyan


