# Upload Project to GitHub Using GitHub Desktop

## Step-by-Step Instructions

### Step 1: Open GitHub Desktop

1. Launch **GitHub Desktop** (you already have it installed)
2. Sign in with your GitHub account if prompted

### Step 2: Add Your Project Folder

1. In GitHub Desktop, click **File** → **Add Local Repository**
2. Click **Choose...** button
3. Navigate to: `C:\Users\andre\Downloads\task`
4. Click **Select Folder**
5. GitHub Desktop will detect it's not a Git repository yet

### Step 3: Initialize Repository (If Needed)

If GitHub Desktop says "This directory does not appear to be a Git repository":

1. Click **"create a repository"** link
2. Name: `DockGuard` (or keep it as `task`)
3. Description: `Monitoring a Containerized URL Shortener Webservice`
4. **DO NOT** check "Initialize this repository with a README" (we already have one)
5. Click **Create Repository**

### Step 4: Review Changes

1. GitHub Desktop will show all your files
2. Review the list - you should see:
   - `service/` folder
   - `db/` folder
   - `prometheus/` folder
   - `grafana/` folder
   - `infra/` folder
   - `docs/` folder
   - `.github/` folder
   - `docker-compose.yml`
   - `README.md`
   - And other files

3. **Important**: Make sure you DON'T see:
   - ❌ `app/` folder (old code, not needed)
   - ❌ `app.zip`
   - ❌ Any `.db` files
   - ❌ `__pycache__/` folders

### Step 5: Create Initial Commit

1. At the bottom left, you'll see a text box for commit message
2. Type: `Initial commit: Complete URL shortener with monitoring stack`
3. Click **Commit to main** (or **Commit to master**)

### Step 6: Create Repository on GitHub

1. Click **Publish repository** button (top right)
2. A dialog will appear:
   - **Name**: `DockGuard` (or your preferred name)
   - **Description**: `Containerized URL shortener with Prometheus and Grafana monitoring`
   - **Keep this code private**: Uncheck if you want it public, check if private
3. Click **Publish Repository**

### Step 7: Wait for Upload

- GitHub Desktop will upload all files
- You'll see a progress bar
- This may take a few minutes depending on your internet speed

### Step 8: Verify on GitHub

1. Once uploaded, click **View on GitHub** button
2. Your browser will open: `https://github.com/YOUR_USERNAME/DockGuard`
3. Verify all folders are there:
   - ✅ service/
   - ✅ db/
   - ✅ prometheus/
   - ✅ grafana/
   - ✅ infra/
   - ✅ docs/
   - ✅ .github/
   - ✅ docker-compose.yml
   - ✅ README.md

### Step 9: Add Repository Description (Optional)

1. On your GitHub repository page
2. Click the **⚙️ Settings** icon next to "About"
3. Add description: `Containerized URL shortener with Prometheus and Grafana monitoring`
4. Add topics: `docker`, `prometheus`, `grafana`, `fastapi`, `monitoring`, `devops`
5. Click **Save changes**

---

## Troubleshooting

### "Repository already exists" Error

If the repository name already exists on GitHub:
- Choose a different name (e.g., `DockGuard-project`, `urlshort-monitoring`)

### Files Not Showing

If some files don't appear:
- Check `.gitignore` - it might be excluding them
- Some files might be too large (GitHub has file size limits)

### Upload Fails

If upload fails:
- Check your internet connection
- Try again (GitHub Desktop will resume)
- Check GitHub status: https://www.githubstatus.com/

### Want to Exclude Files

If you want to exclude certain files:
- Edit `.gitignore` file
- Add patterns for files/folders to ignore
- Commit the changes

---

## After Uploading

### Your Repository URL

Your project will be at:
```
https://github.com/YOUR_USERNAME/DockGuard
```

### Clone It Elsewhere

Others (or you) can clone it with:
```bash
git clone https://github.com/YOUR_USERNAME/DockGuard.git
```

### Update README if Needed

If you want to update the clone URL in README.md:
1. Edit `README.md`
2. Change the clone URL to your actual repository URL
3. Commit and push the changes

---

## Success Checklist

After uploading, verify:

- ✅ All folders visible on GitHub
- ✅ README.md displays correctly
- ✅ docker-compose.yml is there
- ✅ All service files are present
- ✅ No sensitive data (passwords, API keys) in files
- ✅ Repository is accessible

---

## Next Steps

1. **Share the repository** with your team/instructor
2. **Clone on another machine** to test
3. **Create issues** for future improvements
4. **Add collaborators** if working in a team

---

## Quick Reference

**Repository Structure on GitHub:**
```
DockGuard/
├── .github/workflows/    # CI pipeline
├── db/                   # Database scripts
├── docs/                 # Documentation
├── grafana/              # Grafana configs
├── infra/                # Infrastructure scripts
├── prometheus/           # Prometheus config
├── service/              # Application code
├── docker-compose.yml    # Main orchestration
└── README.md            # Project documentation
```

**Your project is now on GitHub! 🎉**

