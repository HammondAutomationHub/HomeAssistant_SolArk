# Quick Deployment to HammondAutomationHub/HomeAssistant_SolArk

## 🚀 Fastest Way to Deploy

Your repository is pre-configured! Just run:

```bash
cd /mnt/user-data/outputs/solark_cloud_integration
./deploy_hammond.sh
```

Then:
```bash
git push -u origin main
```

---

## 📋 Your Repository Details

- **GitHub Organization**: HammondAutomationHub
- **Repository Name**: HomeAssistant_SolArk
- **Full URL**: https://github.com/HammondAutomationHub/HomeAssistant_SolArk
- **Clone URL**: https://github.com/HammondAutomationHub/HomeAssistant_SolArk.git

---

## ✅ Pre-Configured Files

All files have been updated with your repository information:

- ✅ `manifest.json` - Points to your repo
- ✅ `README.md` - All links updated
- ✅ `INSTALLATION.md` - HACS instructions updated
- ✅ All documentation files - Correct URLs
- ✅ `deploy_hammond.sh` - Pre-configured deployment script

---

## 🔑 Authentication

When you push to GitHub, you'll need a Personal Access Token:

### Create Token:
1. Go to: https://github.com/settings/tokens
2. Click: "Generate new token (classic)"
3. Name: "Home Assistant Integration"
4. Scopes: Check `repo` (full control of private repositories)
5. Click: "Generate token"
6. **COPY IT NOW** - You won't see it again!

### Use Token:
When `git push` asks for password, paste your token (not your GitHub password)

---

## 📝 Step-by-Step Commands

```bash
# Navigate to project
cd /mnt/user-data/outputs/solark_cloud_integration

# Run deployment script (initializes git, creates commit)
./deploy_hammond.sh

# Push to GitHub (you'll be asked for credentials)
git push -u origin main
```

**Username**: Your GitHub username  
**Password**: Your Personal Access Token (from above)

---

## 🌐 After Pushing

### Verify Upload
1. Go to: https://github.com/HammondAutomationHub/HomeAssistant_SolArk
2. Check all files are there
3. README should display on main page

### Create Release (Recommended)
1. Create distribution packages:
   ```bash
   ./package.sh
   ```

2. Go to: https://github.com/HammondAutomationHub/HomeAssistant_SolArk/releases/new

3. Fill in:
   - **Tag**: `v1.0.0`
   - **Title**: `Sol-Ark Cloud Integration v1.0.0`
   - **Description**: Copy from DEPLOYMENT_SUMMARY.md
   - **Attach files**: Upload zips from `dist/` folder

4. Click: "Publish release"

---

## 👥 HACS Installation (For Users)

Once published, users can install via HACS:

1. Open HACS in Home Assistant
2. Go to Integrations
3. Click three-dot menu → Custom repositories
4. Add: `https://github.com/HammondAutomationHub/HomeAssistant_SolArk`
5. Category: Integration
6. Search "Sol-Ark Cloud" and install

---

## 🔄 Making Updates Later

```bash
# Make your changes to files

# Commit changes
git add .
git commit -m "Description of changes"

# Push to GitHub
git push

# Create new release with new version tag
```

---

## ❓ Troubleshooting

### Authentication Failed
- Use Personal Access Token, not password
- Token needs `repo` scope
- Generate new token if lost

### Repository Already Exists
```bash
git remote remove origin
git remote add origin https://github.com/HammondAutomationHub/HomeAssistant_SolArk.git
git push -u origin main
```

### Push Rejected
```bash
git pull origin main --allow-unrelated-histories
git push -u origin main
```

---

## 📍 Quick Links

- **Your Repository**: https://github.com/HammondAutomationHub/HomeAssistant_SolArk
- **Issues**: https://github.com/HammondAutomationHub/HomeAssistant_SolArk/issues
- **Releases**: https://github.com/HammondAutomationHub/HomeAssistant_SolArk/releases
- **Token Settings**: https://github.com/settings/tokens

---

## ✨ Ready to Deploy!

Everything is configured for your repository. Just run:

```bash
./deploy_hammond.sh
git push -u origin main
```

That's it! 🎉
