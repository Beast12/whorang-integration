# GitHub Releases Setup Guide

## 🎯 Quick Setup

### 1. Authenticate with GitHub CLI
```bash
gh auth login
```

**Choose the following options:**
- **What account do you want to log into?** → `GitHub.com`
- **What is your preferred protocol for Git operations?** → `HTTPS` or `SSH` (your preference)
- **How would you like to authenticate GitHub CLI?** → `Login with a web browser`

Follow the prompts to complete authentication.

### 2. Verify Authentication
```bash
gh auth status
```

You should see: `✓ Logged in to github.com as [your-username]`

### 3. Create Your First Development Release
```bash
cd /home/koen/Personal/Github/whorang-integration
./create_dev_release.sh
```

This will:
- ✅ Create commit with all intelligent automation features
- ✅ Create `v1.1.0-dev` tag
- ✅ Create GitHub Release (prerelease)
- ✅ Push everything to remote

### 4. For Future Updates
```bash
cd /home/koen/Personal/Github/whorang-integration
./update_dev_release.sh
```

Enter a description when prompted, and it will:
- ✅ Create new commit
- ✅ Update `v1.1.0-dev` tag (force push)
- ✅ Update GitHub Release
- ✅ Push everything to remote

## 🎉 Benefits

### **For You (Developer)**
- ✅ **One Command**: Create/update releases with one script
- ✅ **Consistent**: Professional release notes every time
- ✅ **Automated**: No manual GitHub UI clicking
- ✅ **Safe**: Authentication checks prevent errors

### **For Users**
- ✅ **Easy Installation**: Install `v1.1.0-dev` from GitHub releases
- ✅ **Easy Updates**: Reinstall same version to get updates
- ✅ **Clear Status**: Marked as prerelease for development
- ✅ **Rich Information**: Detailed release notes with features

## 📋 Release Structure

### **Current Setup**
- **v1.0.0** - Stable release (unchanged)
- **v1.1.0-dev** - Development release (continuously updated)

### **User Installation**
Users can install from:
- **HACS**: Repository URL + Version `v1.1.0-dev`
- **GitHub Releases**: Download from releases page
- **Manual**: `git clone` + `git checkout v1.1.0-dev`

## 🔄 Workflow

### **Development Cycle**
1. **Make code changes**
2. **Run update script**: `./update_dev_release.sh`
3. **Users reinstall**: Same version `v1.1.0-dev`
4. **Repeat** as needed

### **Stable Release (Future)**
When ready for stable release:
```bash
git tag -a v1.1.0 -m "Stable release: Intelligent Notification System"
git push origin v1.1.0
gh release create v1.1.0 --title "WhoRang v1.1.0 - Intelligent Notification System" --notes "Stable release notes..."
```

## 🎯 Perfect Solution

This setup gives you exactly what you wanted:
- **Same Version Number**: Users always install `v1.1.0-dev`
- **Continuous Updates**: You can keep updating the same release
- **Professional Releases**: Proper GitHub releases, not just tags
- **Zero Confusion**: Clear development vs stable separation

**Ready to go!** 🚀

Just run `gh auth login` and then `./create_dev_release.sh` to create your first development release!
