# GitHub Deployment - Quick Commands

## 🚀 Fastest Method: Use the Script

```bash
cd /mnt/user-data/outputs/solark_cloud_integration
./deploy_to_github.sh
```

Then follow the prompts!

---

## ⚡ Manual Quick Deploy

Replace `YOUR_USERNAME` with your GitHub username:

```bash
# 1. Navigate to project
cd /mnt/user-data/outputs/solark_cloud_integration

# 2. Initialize git (if not already done)
git init
git branch -M main

# 3. Add and commit files
git add .
git commit -m "Initial commit: Sol-Ark Cloud Integration v1.0.0"

# 4. Add remote (replace YOUR_USERNAME!)
git remote add origin https://github.com/YOUR_USERNAME/solark_cloud.git

# 5. Push to GitHub
git push -u origin main
```

**⚠️ IMPORTANT**: Create the repository on GitHub first at https://github.com/new

---

## 📦 Create Release Package

```bash
cd /mnt/user-data/outputs/solark_cloud_integration
./package.sh
```

Files created in `dist/` folder.

---

## 🔑 Need a GitHub Personal Access Token?

1. Go to: https://github.com/settings/tokens
2. Click: "Generate new token (classic)"
3. Name: "Home Assistant Integration"
4. Scopes: Check `repo`
5. Click: "Generate token"
6. Copy: Save it somewhere safe!
7. Use: As password when git asks

---

## ✅ Verification Checklist

After pushing:

- [ ] Go to `https://github.com/YOUR_USERNAME/solark_cloud`
- [ ] See all files listed?
- [ ] README displays on main page?
- [ ] All folders present (custom_components, etc.)?
- [ ] Can read documentation files?

If yes to all, you're done! ✨

---

## 📋 What to Do After Pushing

1. **Test it yourself**:
   - Add as HACS custom repository
   - Install in your Home Assistant
   - Verify it works

2. **Create a release** (optional but recommended):
   - Go to: `https://github.com/YOUR_USERNAME/solark_cloud/releases/new`
   - Tag: `v1.0.0`
   - Title: `Sol-Ark Cloud Integration v1.0.0`
   - Upload: zips from `./package.sh`
   - Publish!

3. **Share** (when ready):
   - Home Assistant Community Forum
   - r/homeassistant subreddit
   - Sol-Ark communities

---

## 🆘 Quick Troubleshooting

### Push rejected?
```bash
git pull origin main --allow-unrelated-histories
git push -u origin main
```

### Wrong remote?
```bash
git remote remove origin
git remote add origin https://github.com/YOUR_USERNAME/solark_cloud.git
git push -u origin main
```

### Authentication failed?
- Use Personal Access Token instead of password
- See section above for creating one

---

## 🎯 One-Liner Summary

```bash
cd /mnt/user-data/outputs/solark_cloud_integration && \
git init && git branch -M main && git add . && \
git commit -m "Initial commit: Sol-Ark Cloud Integration v1.0.0" && \
echo "Now run: git remote add origin https://github.com/YOUR_USERNAME/solark_cloud.git" && \
echo "Then run: git push -u origin main"
```

---

## 📱 For Quick Reference

**Project Location**: `/mnt/user-data/outputs/solark_cloud_integration`

**GitHub Repo URL**: `https://github.com/YOUR_USERNAME/solark_cloud`

**HACS Install URL**: Same as repo URL

---

Need more details? See [GITHUB_DEPLOYMENT.md](GITHUB_DEPLOYMENT.md)
