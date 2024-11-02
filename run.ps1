# If you get a permission error, you may need to change the PowerShell execution policy.
# Open PowerShell as Administrator and run one of the following commands:
# Option 1: Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
# Option 2: Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope CurrentUser

# Dont worry about the command, it wont affect your system or privacy.
# Then run the script with: .\run.ps1

Write-Host ("-" * 100)
Write-Host "Installing Necessary Packages..."
Write-Host ("-" * 100)
Write-Host ""
python.exe -m pip install --upgrade pip
pip install -r requirements.txt -q
Write-Host ""
Write-Host ("-" * 100)
Write-Host "Necessary Packages Installed"
Write-Host ("-" * 100)
Write-Host ""
Write-Host ("-" * 100)
Write-Host "App is Initializing..."
Write-Host ("-" * 100)
Write-Host ""
python app.py