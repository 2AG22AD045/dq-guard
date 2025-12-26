@echo off
echo ========================================
echo   DQ-Guard GitHub Setup and Push
echo ========================================
echo.

echo Setting up Git configuration...
git config user.name "2AG22AD045"
git config user.email "gadamphallisaniya@gmail.com"

echo.
echo Cleared old credentials. You will be prompted for new ones.
echo.
echo When prompted, enter:
echo Username: 2AG22AD045
echo Password: [Your GitHub Personal Access Token]
echo.
echo If you don't have a token, create one at:
echo https://github.com/settings/tokens
echo Select 'repo' permissions when creating the token.
echo.

pause

echo Pushing to GitHub...
git push -u origin main

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ✅ SUCCESS! DQ-Guard has been pushed to GitHub!
    echo 🌐 Repository URL: https://github.com/2AG22AD045/dq-guard
    echo.
    echo Your repository is now live and public!
    echo.
    echo 🚀 Features uploaded:
    echo ✅ Complete full-stack application
    echo ✅ Professional UI with dark theme
    echo ✅ Comprehensive documentation
    echo ✅ Docker support
    echo ✅ Test suite
    echo ✅ Sample datasets
    echo.
) else (
    echo.
    echo ❌ Push failed. Please check your credentials.
    echo Make sure you're using your Personal Access Token as password.
    echo.
)

pause