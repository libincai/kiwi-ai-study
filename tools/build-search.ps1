# Build Pagefind index for GitHub Pages (repo root). Requires Node.js for npx.
$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot\..

python local\kiwi_search_prepare.py
python local\kiwi_inject_search_assets.py
npx --yes pagefind --site .

Write-Host "Search index written to pagefind/ — commit with your HTML changes."