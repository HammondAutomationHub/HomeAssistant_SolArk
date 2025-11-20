# Manual GitHub Deployment Guide

## Quick Method (Using the Script)

If you're in the project directory, just run:

```bash
cd /mnt/user-data/outputs/solark_cloud_integration
./deploy_to_github.sh
```

The script will guide you through the process.

---

## Manual Method (Step-by-Step)

If you prefer to do it manually or the script doesn't work, follow these steps:

### Step 1: Initialize Git Repository

```bash
cd /mnt/user-data/outputs/solark_cloud_integration

# Initialize git
git init
git branch -M main

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: Sol-Ark Cloud Integration v1.0.0"
```

### Step 2: Create GitHub Repository

1. **Go to GitHub**: https://github.com/new
2. **Fill in the form**:
   - **Repository name**: `solark_cloud` (or your preferred name)
   - **Description**: `Home Assistant integration for Sol-Ark Cloud solar monitoring`
   - **Public/Private**: Choose Public (recommended for HACS compatibility)
   - **Important**: Do NOT check "Initialize with README" (we already have one)
3. **Click**: "Create repository"

### Step 3: Connect and Push

GitHub will show you commands on the next page. Use these:

```bash
# Add your GitHub repository as remote
# Replace YOUR_USERNAME and solark_cloud with your actual values
git remote add origin https://github.com/YOUR_USERNAME/solark_cloud.git

# Push to GitHub
git push -u origin main
```

**Example** (if your username is `jsmith`):
```bash
git remote add origin https://github.com/jsmith/solark_cloud.git
git push -u origin main
```

You'll be prompted for your GitHub credentials:
- **Username**: Your GitHub username
- **Password**: Your Personal Access Token (PAT)
  - If you don't have a PAT, create one at: https://github.com/settings/tokens
  - Scopes needed: `repo` (full control of private repositories)

### Step 4: Verify Upload

1. Go to your repository: `https://github.com/YOUR_USERNAME/solark_cloud`
2. You should see all files and folders
3. The README.md should display automatically

---

## Optional: Create a Release (Recommended)

Creating a release makes it easier for users to install:

### Step 1: Create Distribution Packages

```bash
cd /mnt/user-data/outputs/solark_cloud_integration
./package.sh
```

This creates:
- `dist/solark_cloud_v1.0.0.zip` - Full package
- `dist/solark_cloud_hacs_v1.0.0.zip` - HACS package

### Step 2: Create Release on GitHub

1. **Go to**: `https://github.com/YOUR_USERNAME/solark_cloud/releases/new`

2. **Tag version**: `v1.0.0`

3. **Release title**: `Sol-Ark Cloud Integration v1.0.0`

4. **Description**: Copy and paste this:

```markdown
# Sol-Ark Cloud Integration v1.0.0

A production-ready Home Assistant custom integration for Sol-Ark Cloud solar monitoring.

## Features

✅ Full UI configuration (no YAML required)
✅ Easy settings updates via Options Flow
✅ Multi-mode authentication with automatic fallback
✅ 8 comprehensive sensors for complete solar monitoring
✅ HACS compatible
✅ Production-ready code with comprehensive error handling

## Sensors Included

- PV Power (W)
- Load Power (W)
- Grid Import Power (W)
- Grid Export Power (W)
- Battery Power (W)
- Battery State of Charge (%)
- Energy Today (kWh)
- Last Error (diagnostics)

## Installation

### Via HACS (Recommended)

1. Open HACS → Integrations
2. Click ⋮ → Custom repositories
3. Add: `https://github.com/YOUR_USERNAME/solark_cloud`
4. Category: Integration
5. Search "Sol-Ark Cloud" and download
6. Restart Home Assistant
7. Add integration via UI

### Manual Installation

1. Download `solark_cloud_v1.0.0.zip`
2. Extract to `<config>/custom_components/`
3. Restart Home Assistant
4. Add integration via UI

## Documentation

- 📖 [Quick Start Guide](QUICKSTART.md)
- 📖 [Installation Guide](INSTALLATION.md)
- 📖 [Configuration Guide](CONFIGURATION.md)
- 📖 [Complete README](README.md)

## Requirements

- Home Assistant 2023.1.0+
- MySolArk account with valid credentials
- Your Sol-Ark Plant ID

## Support

- 🐛 [Report Issues](https://github.com/YOUR_USERNAME/solark_cloud/issues)
- 💬 [Discussions](https://github.com/YOUR_USERNAME/solark_cloud/discussions)
```

5. **Attach files**:
   - Click "Attach binaries by dropping them here or selecting them"
   - Upload: `dist/solark_cloud_v1.0.0.zip`
   - Upload: `dist/solark_cloud_hacs_v1.0.0.zip`

6. **Publish**: Click "Publish release"

---

## Setting Up HACS Compatibility

Your repository is already HACS-compatible. Users can add it as a custom repository:

### For Users to Install via HACS:

1. Open HACS in Home Assistant
2. Go to Integrations
3. Click the three-dot menu (⋮) in top right
4. Select "Custom repositories"
5. Add URL: `https://github.com/YOUR_USERNAME/solark_cloud`
6. Category: Integration
7. Click "Add"
8. Search for "Sol-Ark Cloud"
9. Click "Download"
10. Restart Home Assistant

---

## Updating the Integration Later

When you make changes:

```bash
# Make your changes to the code

# Commit changes
git add .
git commit -m "Description of changes"

# Push to GitHub
git push

# Update version in manifest.json
# Create new release with new version tag (e.g., v1.0.1)
```

---

## Troubleshooting

### Issue: Authentication Failed

**Problem**: Git push asks for password but rejects it

**Solution**: 
1. GitHub no longer accepts passwords for git operations
2. Create a Personal Access Token (PAT):
   - Go to: https://github.com/settings/tokens
   - Click "Generate new token (classic)"
   - Name: "Sol-Ark Cloud Integration"
   - Scopes: Check `repo`
   - Click "Generate token"
   - Copy the token (you won't see it again!)
3. Use the PAT as your password when pushing

### Issue: Repository Already Exists

**Problem**: "Repository already exists" error

**Solution**:
```bash
# Remove existing remote
git remote remove origin

# Add correct remote
git remote add origin https://github.com/YOUR_USERNAME/solark_cloud.git

# Push
git push -u origin main
```

### Issue: Need to Use SSH Instead of HTTPS

**Solution**:
```bash
# Use SSH URL instead
git remote set-url origin git@github.com:YOUR_USERNAME/solark_cloud.git
git push -u origin main
```

---

## Quick Reference Commands

```bash
# Check current status
git status

# See remotes
git remote -v

# Check commit history
git log --oneline

# Create new branch for testing
git checkout -b test-branch

# Return to main branch
git checkout main

# Pull latest changes
git pull origin main
```

---

## What Users Will See

Once published, users will see:

1. **Repository**: All your code and documentation
2. **README**: Displayed on the main page
3. **Releases**: Download links for zip files
4. **HACS**: Can install directly through HACS

---

## Next Steps After Publishing

1. **Test the installation yourself**:
   - Install via HACS custom repository
   - Verify everything works
   - Test with your Sol-Ark system

2. **Share with the community**:
   - Post in Home Assistant forums
   - Share on r/homeassistant
   - Mention in Sol-Ark communities

3. **Maintain the repository**:
   - Respond to issues
   - Accept pull requests
   - Update documentation
   - Release new versions

---

## Need Help?

If you run into issues:
1. Check the error message carefully
2. Ensure you're in the correct directory
3. Verify your GitHub credentials
4. Try the automated script: `./deploy_to_github.sh`
5. Check GitHub documentation: https://docs.github.com/

---

**Remember**: Replace `YOUR_USERNAME` with your actual GitHub username in all commands and URLs!
