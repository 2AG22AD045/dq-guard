# 📤 Upload DQ-Guard to GitHub - Step by Step

## Method 1: GitHub Web Interface (Easiest)

1. **Go to your repository**: https://github.com/2AG22AD045/dq-guard

2. **Click "uploading an existing file"** or **"Add file" → "Upload files"**

3. **Drag and drop ALL files** from the `dq-guard` folder:
   - backend/ (entire folder)
   - frontend/ (entire folder)
   - tests/ (entire folder)
   - docs/ (entire folder)
   - All CSV files (sample_data.csv, etc.)
   - docker-compose.yml
   - README.md
   - .gitignore

4. **Add commit message**: 
   ```
   Initial commit: Complete DQ-Guard Data Quality Framework
   
   - Full-stack application with Python FastAPI backend and React frontend
   - Professional UI with dark-themed buttons and modern design
   - Comprehensive data validation engine
   - Real-time dashboard with quality metrics
   - Automated scheduling and alerts
   - Docker support and complete documentation
   ```

5. **Click "Commit changes"**

## Method 2: GitHub Desktop (Recommended for future)

1. Download [GitHub Desktop](https://desktop.github.com/)
2. Sign in with account: 2AG22AD045
3. Clone your repository
4. Copy all files to the cloned folder
5. Commit and push

## Method 3: Command Line (if you have Personal Access Token)

```bash
# In the dq-guard folder
git push https://2AG22AD045:[YOUR_TOKEN]@github.com/2AG22AD045/dq-guard.git main
```

Replace [YOUR_TOKEN] with your GitHub Personal Access Token.