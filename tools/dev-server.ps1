# Local dev with clean URLs (e.g. /math-foundations -> math/math-foundations.html)
Set-Location $PSScriptRoot\..

python tools/generate-serve-rewrites.py
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

npx --yes serve . -l 3000