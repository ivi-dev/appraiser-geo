# 1. Empty the output directory
Remove-Item -Path dist\* -Force -Recurse

# 2. Build the app
pyinstaller src/main.py --onedir --noconfirm --name appraiser-geo