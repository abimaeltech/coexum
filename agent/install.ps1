# PowerShell installer para Windows
Set-ExecutionPolicy Bypass -Scope Process -Force
choco install python3 docker-desktop git -y
pip install -e .
Add-Content -Path $PROFILE -Value "Set-Alias coexum python -m coexum"
