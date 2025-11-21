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

### Troubleshooting

**Port already in use?**
- Make sure no other applications are using ports 8080, 9090, or 3000
- Check: `netstat -ano | findstr :8080`

**Docker not starting?**
- Make sure Docker Desktop is running
- Check: `docker ps`

**Services not responding?**
- Check logs: `docker-compose logs urlshort`
- Restart: `docker-compose restart`

---

## Part 2: Uploading to GitHub

### Option A: Using GitHub Desktop (Easiest)

1. **Install GitHub Desktop**
   - Download from: https://desktop.github.com/
   - Install and sign in with your GitHub account

2. **Add the Repository**
   - Click **File** → **Add Local Repository**
   - Browse to: `C:\Users\andre\Downloads\task`
   - Click **Add Repository**

3. **Create Repository on GitHub**
   - Go to: https://github.com/new
   - Repository name: `DockGuard` (or any name you want)
   - Make it **Public** or **Private**
   - **Don't** initialize with README (we already have one)
   - Click **Create repository**

4. **Publish to GitHub**
   - In GitHub Desktop, click **Publish repository**
   - Select the repository you just created
   - Click **Publish Repository**

### Option B: Using Git Command Line

1. **Install Git** (if not already installed)
   - Download from: https://git-scm.com/download/win
   - Install with default settings

2. **Open PowerShell in Project Folder**
   ```powershell
   cd C:\Users\andre\Downloads\task
   ```

3. **Initialize Git Repository** (if not already done)
   ```powershell
   git init
   ```

4. **Add All Files**
   ```powershell
   git add .
   ```

5. **Create Initial Commit**
   ```powershell
   git commit -m "Initial commit: Complete URL shortener with monitoring"
   ```

6. **Create Repository on GitHub**
   - Go to: https://github.com/new
   - Repository name: `DockGuard`
   - Make it **Public** or **Private**
   - **Don't** initialize with README
   - Click **Create repository**
   - **Copy the repository URL** (e.g., `https://github.com/yourusername/DockGuard.git`)

7. **Connect to GitHub and Push**
   ```powershell
   git remote add origin https://github.com/yourusername/DockGuard.git
   git branch -M main
   git push -u origin main
   ```
   
   Replace `yourusername` with your actual GitHub username.

8. **Enter Credentials**
   - If prompted, use your GitHub username and a **Personal Access Token**
   - To create a token: https://github.com/settings/tokens
   - Select scope: `repo`

### Option C: Using GitHub Web Interface

1. **Create Repository on GitHub**
   - Go to: https://github.com/new
   - Repository name: `DockGuard`
   - Make it **Public** or **Private**
   - **Don't** initialize with README
   - Click **Create repository**

2. **Upload Files**
   - On the repository page, click **uploading an existing file**
   - Drag and drop all files from your project folder
   - Commit message: `Initial commit: Complete URL shortener with monitoring`
   - Click **Commit changes**

### Important: What to Upload

**Upload these files/folders:**
- ✅ `service/` (entire folder)
- ✅ `db/` (entire folder)
- ✅ `prometheus/` (entire folder)
- ✅ `grafana/` (entire folder)
- ✅ `infra/` (entire folder)
- ✅ `docs/` (entire folder)
- ✅ `.github/` (entire folder)
- ✅ `docker-compose.yml`
- ✅ `README.md`
- ✅ `.gitignore`
- ✅ All other `.md` files

**Don't upload:**
- ❌ `app/` folder (old code, not needed)
- ❌ `app.zip`
- ❌ Any `.db` files (database files)
- ❌ `__pycache__/` folders
- ❌ `.venv/` or `venv/` folders

### After Uploading

1. **Verify on GitHub**
   - Go to your repository page
   - Check that all folders are visible
   - Click on `README.md` to see if it displays correctly

2. **Update Repository Description** (optional)
   - Go to repository **Settings** → **General**
   - Add description: "Containerized URL shortener with Prometheus and Grafana monitoring"

3. **Add Topics** (optional)
   - On repository page, click the gear icon next to "About"
   - Add topics: `docker`, `prometheus`, `grafana`, `fastapi`, `monitoring`

---

## Quick Reference Commands

### Running the Project
```powershell
# Start services
docker-compose up --build

# Start in background
docker-compose up -d --build

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Stop and remove volumes
docker-compose down -v
```

### Testing
```powershell
# Create short URL
curl -X POST http://localhost:8080/shorten -H "Content-Type: application/json" -d '{\"url\":\"https://example.com\"}'

# Test redirect
curl -I http://localhost:8080/YOUR_SHORT_CODE

# Check metrics
curl http://localhost:8080/metrics
```

### Git Commands
```powershell
# Check status
git status

# Add changes
git add .

# Commit
git commit -m "Your message"

# Push to GitHub
git push origin main
```

---

## Need Help?

If you encounter any issues:
1. Check the logs: `docker-compose logs`
2. Verify Docker is running: `docker ps`
3. Check the `QUICKSTART.md` file for more details
4. Review the `README.md` for project documentation

