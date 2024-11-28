# If you get a permission error, you may need to change the PowerShell execution policy.
# Open PowerShell as Administrator and run one of the following commands:
# Option 1: Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
# Option 2: Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope CurrentUser

# Dont worry about the command, it wont affect your system or privacy.
# Then run the script with: .\run.ps1

if (-not (Get-Command ffmpeg -ErrorAction SilentlyContinue)) {
    Write-Host ("-" * 100)
    Write-Host "FFmpeg is not installed or not found in PATH"
    Write-Host "FFmpeg is required to run ytgrabber"
    Write-Host "Please download and install FFmpeg, then add it to your system PATH"
    Write-Host "Download FFmpeg from: https://drive.google.com/file/d/1dUmR4yQwsSH_h2bSUYTa9NOjui8g3zgQ/view?usp=drive_link"
    Write-Host ("-" * 100)
    exit 1
}

Write-Host ("-" * 100)
# Check if all required packages installed
$needsInstall = $false
$requirements = Get-Content "requirements.txt"
foreach ($req in $requirements) {
    if ($req -match '^\s*#' -or $req -match '^\s*$') { continue }  # Skip comments and empty lines
    $package = ($req -split '==|>=|<=|~=|!=|<|>')[0].Trim()
    $checkPackage = python -c "import pkg_resources; print('$package' in {pkg.key for pkg in pkg_resources.working_set})" 2>$null
    if ($checkPackage -eq "False") {
        $needsInstall = $true
        break
    }
}

if ($needsInstall) {
    Write-Host "Installing Necessary Packages..."
    Write-Host ("-" * 100)
    Write-Host ""
    python.exe -m pip install --upgrade pip
    pip install -r requirements.txt -q
} else {
    Write-Host "Necessary packages already installed."
    Write-Host ("-" * 100)
    Write-Host ""
}

Write-Host ("-" * 100)
Write-Host "App is Initializing..."
Write-Host ("-" * 100)
Write-Host ""
python app.py