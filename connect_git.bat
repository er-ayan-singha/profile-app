@echo off
echo Connecting to GitHub...

REM Use full path to Git
"C:\Program Files\Git\bin\git.exe" config --global user.name "Ayan Singha"
"C:\Program Files\Git\bin\git.exe" config --global user.email "singhaayanray07@gmail.com"
"C:\Program Files\Git\bin\git.exe" init
"C:\Program Files\Git\bin\git.exe" add .
"C:\Program Files\Git\bin\git.exe" commit -m "Initial commit"
"C:\Program Files\Git\bin\git.exe" branch -M main
"C:\Program Files\Git\bin\git.exe" remote add origin https://github.com/er-ayan-singha/modern-social-profile.git
"C:\Program Files\Git\bin\git.exe" push -u origin main

echo.
echo If successful, check your repository at:
echo https://github.com/er-ayan-singha/modern-social-profile
echo.
pause 