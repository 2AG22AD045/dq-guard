# 🔐 GitHub Authentication Steps

## Step 1: Create Personal Access Token
1. Go to: https://github.com/settings/tokens
2. Click "Generate new token" → "Generate new token (classic)"
3. Give it a name: "DQ-Guard Project"
4. Select scopes: ✅ **repo** (Full control of private repositories)
5. Click "Generate token"
6. **COPY THE TOKEN** (you won't see it again!)

## Step 2: Push with Token
Run this command in the dq-guard folder:

```bash
git push https://2AG22AD045:[YOUR_TOKEN]@github.com/2AG22AD045/dq-guard.git main
```

Replace `[YOUR_TOKEN]` with the token you copied.

## Step 3: Set up for future pushes
```bash
git remote set-url origin https://2AG22AD045:[YOUR_TOKEN]@github.com/2AG22AD045/dq-guard.git
```

## Alternative: Use Git Credential Manager
```bash
git config --global credential.helper manager-core
git push -u origin main
```
Then enter:
- Username: 2AG22AD045
- Password: [YOUR_PERSONAL_ACCESS_TOKEN]