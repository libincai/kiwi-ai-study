# Local dev at http://localhost:3000/kiwi-ai-study/ (GitHub Pages path parity)
Set-Location $PSScriptRoot\..

$port = 3000
$listeners = @(
    Get-NetTCPConnection -LocalPort $port -State Listen -ErrorAction SilentlyContinue
) | ForEach-Object { $_.OwningProcess } | Select-Object -Unique
foreach ($procId in $listeners) {
    if (-not $procId) { continue }
    $name = (Get-Process -Id $procId -ErrorAction SilentlyContinue).ProcessName
    Write-Host "Stopping $name (PID $procId) on port $port — use this script, not npx serve." -ForegroundColor Yellow
    Stop-Process -Id $procId -Force -ErrorAction SilentlyContinue
    Start-Sleep -Milliseconds 400
}

python local/kiwi_math_catalog.py
python tools/generate-serve-rewrites.py
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
python tools/generate_github_pages_stubs.py
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

python tools/kiwi_dev_server.py