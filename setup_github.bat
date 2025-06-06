@echo off
echo Setting up Git and GitHub...

REM Configure Git
git config --global user.name "Ayan Singha"
git config --global user.email "singhaayanray07@gmail.com"

REM Initialize repository
git init
git add .
git commit -m "Initial commit"
git branch -M main

REM Add remote and push
git remote add origin https://github.com/er-ayan-singha/modern-social-profile.git
git push -u origin main

echo Setup complete! Check your GitHub repository at:
echo https://github.com/er-ayan-singha/modern-social-profile
pause 