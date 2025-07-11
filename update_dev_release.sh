#!/bin/bash

# WhoRang Development Release Update Script
# This script updates the existing v1.1.0-dev release

echo "🔄 Updating WhoRang v1.1.0-dev Development Release"
echo "================================================="

# Check if we're in a git repository
if [ ! -d ".git" ]; then
    echo "❌ Error: Not in a git repository"
    exit 1
fi

# Get description from user
echo "📝 Enter a brief description of the changes:"
read -r description

if [ -z "$description" ]; then
    description="Development updates and improvements"
fi

# Check for uncommitted changes
if [ -n "$(git status --porcelain)" ]; then
    echo "📝 Found uncommitted changes. Adding all files..."
    git add .
else
    echo "✅ No uncommitted changes found"
fi

# Create commit
echo "📦 Creating commit..."
git commit -m "feat: $description

Development update for v1.1.0-dev
- $description

This update maintains the v1.1.0-dev development release.
Users can reinstall the same version to get these updates."

# Update the development tag (force push)
echo "🏷️  Updating v1.1.0-dev tag..."
git tag -f v1.1.0-dev -m "Updated development release: $description

Changes:
- $description

This is a development release update. Users can reinstall 
v1.1.0-dev to get the latest changes."

# Push to remote
echo "⬆️  Pushing to remote repository..."
git push origin main

echo "🏷️  Force pushing updated development tag..."
git push -f origin v1.1.0-dev

echo ""
echo "🎉 SUCCESS! Development release v1.1.0-dev updated!"
echo "================================================="
echo ""
echo "📋 What was updated:"
echo "   ✅ New commit: $description"
echo "   ✅ Updated tag: v1.1.0-dev (force pushed)"
echo "   ✅ Pushed to remote repository"
echo ""
echo "👥 Users can now:"
echo "   1. Reinstall v1.1.0-dev to get updates"
echo "   2. Or wait for automatic HACS updates"
echo ""
echo "🔄 For next update, run this script again!"
