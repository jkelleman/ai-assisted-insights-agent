# PowerShell script to update all file path references after reorganization
# Run this AFTER running reorganize_repo.ps1
# Usage: powershell -ExecutionPolicy Bypass -File .\update_references.ps1

Write-Host "Updating file path references..." -ForegroundColor Cyan

# =============================================================================
# README.md updates
# =============================================================================
Write-Host "Updating README.md..." -ForegroundColor Yellow

$readme = Get-Content -Path "README.md" -Raw

# Update badge link
$readme = $readme -replace '\(docs/CONNECTING_TO_DATA\.md', '(01_docs/CONNECTING_TO_DATA.md'

# Update pytest path  
$readme = $readme -replace 'pytest tests/', 'pytest 05_tests/'

# Update example paths
$readme = $readme -replace '\[examples/claude-desktop\]\(examples/claude-desktop\)', '[02_examples/claude-desktop](02_examples/claude-desktop)'
$readme = $readme -replace '\[examples/python-client\]\(examples/python-client\)', '[02_examples/python-client](02_examples/python-client)'
$readme = $readme -replace '\[examples/jupyter\]\(examples/jupyter\)', '[02_examples/jupyter](02_examples/jupyter)'
$readme = $readme -replace '\[examples/USAGE\.md\]\(examples/USAGE\.md\)', '[02_examples/USAGE.md](02_examples/USAGE.md)'
$readme = $readme -replace 'See \[examples/', 'See [02_examples/'
$readme = $readme -replace '\(examples/', '(02_examples/'

# Update data file paths in sample commands
$readme = $readme -replace 'data/ecommerce_sample\.sql', '03_data/ecommerce_sample.sql'
$readme = $readme -replace 'data/financial_sample\.sql', '03_data/financial_sample.sql'
$readme = $readme -replace 'data/hr_sample\.sql', '03_data/hr_sample.sql'
$readme = $readme -replace 'data/streaming', '03_data/streaming'

# Update docs paths
$readme = $readme -replace '\[Connecting to Microsoft Fabric\]\(docs/', '[Connecting to Microsoft Fabric](01_docs/'

Set-Content -Path "README.md" -Value $readme -NoNewline
Write-Host "  README.md updated" -ForegroundColor Green

# =============================================================================
# pyproject.toml - add pytest configuration
# =============================================================================
Write-Host "Updating pyproject.toml..." -ForegroundColor Yellow

$pyproject = Get-Content -Path "pyproject.toml" -Raw

if ($pyproject -notmatch '\[tool\.pytest') {
    $pyproject += @"

[tool.pytest.ini_options]
testpaths = ["05_tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
"@
    Set-Content -Path "pyproject.toml" -Value $pyproject -NoNewline
    Write-Host "  pyproject.toml updated with pytest config" -ForegroundColor Green
} else {
    Write-Host "  pyproject.toml already has pytest config" -ForegroundColor Gray
}

# =============================================================================
# Update CI workflow
# =============================================================================
Write-Host "Updating CI workflow..." -ForegroundColor Yellow

if (Test-Path ".github/workflows/ci.yml") {
    $ci = Get-Content -Path ".github/workflows/ci.yml" -Raw
    $ci = $ci -replace 'pytest tests/', 'pytest 05_tests/'
    Set-Content -Path ".github/workflows/ci.yml" -Value $ci -NoNewline
    Write-Host "  ci.yml updated" -ForegroundColor Green
}

# =============================================================================
# Update USAGE.md
# =============================================================================
Write-Host "Updating 02_examples/USAGE.md..." -ForegroundColor Yellow

if (Test-Path "02_examples/USAGE.md") {
    $usage = Get-Content -Path "02_examples/USAGE.md" -Raw
    $usage = $usage -replace 'docs/', '01_docs/'
    $usage = $usage -replace '`config\.yaml`', '`06_configs/config.yaml`'
    Set-Content -Path "02_examples/USAGE.md" -Value $usage -NoNewline
    Write-Host "  USAGE.md updated" -ForegroundColor Green
}

# =============================================================================
# Update docs in 01_docs/
# =============================================================================
Write-Host "Updating docs in 01_docs/..." -ForegroundColor Yellow

$docFiles = Get-ChildItem -Path "01_docs" -Filter "*.md" -ErrorAction SilentlyContinue

foreach ($doc in $docFiles) {
    $content = Get-Content -Path $doc.FullName -Raw
    $original = $content
    
    $content = $content -replace 'examples/', '02_examples/'
    $content = $content -replace '\.\./examples/', '../02_examples/'
    $content = $content -replace '\.\./data/', '../03_data/'
    $content = $content -replace 'data/', '03_data/'
    
    if ($content -ne $original) {
        Set-Content -Path $doc.FullName -Value $content -NoNewline
        Write-Host "  $($doc.Name) updated" -ForegroundColor Green
    }
}

# =============================================================================
# Update config files with data paths
# =============================================================================
Write-Host "Updating config files in 06_configs/..." -ForegroundColor Yellow

$configFiles = Get-ChildItem -Path "06_configs" -Filter "*.yaml" -ErrorAction SilentlyContinue

foreach ($config in $configFiles) {
    $content = Get-Content -Path $config.FullName -Raw
    $original = $content
    
    $content = $content -replace 'path: data/', 'path: 03_data/'
    
    if ($content -ne $original) {
        Set-Content -Path $config.FullName -Value $content -NoNewline
        Write-Host "  $($config.Name) updated" -ForegroundColor Green
    }
}

# =============================================================================
# Update REAL_DATA_GUIDE.md
# =============================================================================
Write-Host "Updating REAL_DATA_GUIDE.md..." -ForegroundColor Yellow

if (Test-Path "REAL_DATA_GUIDE.md") {
    $guide = Get-Content -Path "REAL_DATA_GUIDE.md" -Raw
    $guide = $guide -replace 'data/', '03_data/'
    $guide = $guide -replace 'config_', '06_configs/config_'
    $guide = $guide -replace '06_configs/06_configs/', '06_configs/'
    Set-Content -Path "REAL_DATA_GUIDE.md" -Value $guide -NoNewline
    Write-Host "  REAL_DATA_GUIDE.md updated" -ForegroundColor Green
}

# =============================================================================
# Commit changes
# =============================================================================
Write-Host "" 
Write-Host "Committing reference updates..." -ForegroundColor Green

git add -A
git commit -m "fix: update all file path references for new folder structure

- README.md: examples, data, docs paths
- pyproject.toml: add pytest testpaths
- CI workflow: update test path
- Config files: update data paths
- Docs: update cross-references
"

Write-Host ""
Write-Host "All references updated!" -ForegroundColor Green
Write-Host ""
Write-Host "New folder structure:" -ForegroundColor Cyan
Write-Host "  01_docs/          - Documentation & guides"
Write-Host "  02_examples/      - Demos & usage examples"
Write-Host "  03_data/          - Sample datasets"
Write-Host "  04_scripts/       - Utility scripts"
Write-Host "  05_tests/         - Test suite"
Write-Host "  06_configs/       - Configuration files"
Write-Host "  insights_agent/   - Python source code"
Write-Host ""
Write-Host "Run 'git push origin main' to push changes" -ForegroundColor Yellow
