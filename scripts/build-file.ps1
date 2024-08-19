# 1. Empty the output directory
Remove-Item -Path dist\* -Force -Recurse
# 2. Build the app
pyinstaller src/main.py --onefile --noconfirm --name appraiser-geo
# 3. Compress the build output
Compress-Archive -Path dist\appraiser-geo.exe -Destination dist\appraiser-geo -Force