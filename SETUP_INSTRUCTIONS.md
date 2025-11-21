# Setup Instructions

## Part 1: Running the Project on Your Laptop

### Prerequisites

1. **Install Docker Desktop**

   - Download from: https://www.docker.com/products/docker-desktop/
   - Install and restart your computer
   - Make sure Docker Desktop is running (you'll see the Docker icon in your system tray)

2. **Verify Docker is installed**
   - Open PowerShell or Command Prompt
   - Run: `docker --version`
   - Run: `docker-compose --version`
   - Both commands should show version numbers

### Step-by-Step: Running the Project

1. **Open Terminal/PowerShell**

   - Navigate to the project folder:
     ```powershell
     cd C:\Users\andre\Downloads\task
     ```

2. **Start All Services**

   ```powershell
   docker-compose up --build
   ```

   This will:

   - Build the URL shortener service
   - Download Prometheus and Grafana images
   - Start all three services
   - Create necessary volumes for data storage

   **First time will take 5-10 minutes** (downloading images)
   **Subsequent runs will be faster**

3. **Wait for Services to Start**

   - You'll see logs from all services
   - Wait until you see messages like:
     - `urlshort | Application startup complete`
     - `prometheus | Server is ready to receive web requests`
     - `grafana | HTTP Server Listen`

4. **Verify Services are Running**

   - Open your web browser and check:
     - **Service**: http://localhost:8080/metrics
     - **Prometheus**: http://localhost:9090
     - **Grafana**: http://localhost:3000

5. **Test the Service**

   Open a **new** PowerShell window and run:

   ```powershell
   # Create a short URL
   curl -X POST http://localhost:8080/shorten -H "Content-Type: application/json" -d '{\"url\":\"https://example.com\"}'
   ```

   You should get a response like: `{"short_code":"abc123"}`

   Then test the redirect:

   ```powershell
   curl -I http://localhost:8080/abc123
   ```

   You should see `HTTP/1.1 302 Found`

6. **View Grafana Dashboard**

   - Go to: http://localhost:3000
   - Login with:
     - Username: `admin`
     - Password: `admin`
   - Navigate to: **Dashboards** → **URL Shortener Monitoring**

7. **Stop Services** (when done)
   - Press `Ctrl+C` in the terminal where docker-compose is running
   - Or in a new terminal:
     ```powershell
     docker-compose down
     ```
