$ErrorActionPreference = 'Stop'
# PnP 2.12 works on PS 7.2
Write-Host "Installing PnP.PowerShell 2.12.0 for current user..."
Install-Module PnP.PowerShell -RequiredVersion 2.12.0 -Scope CurrentUser -Force -AllowClobber -SkipPublisherCheck
Import-Module PnP.PowerShell -RequiredVersion 2.12.0 -Force
Get-Module PnP.PowerShell | Format-List Name, Version
