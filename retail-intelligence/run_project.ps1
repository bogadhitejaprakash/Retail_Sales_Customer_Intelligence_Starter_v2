# Retail Sales & Customer Intelligence — Windows PowerShell launcher
# Run from VS Code terminal: .\run_project.ps1
# Run only Lesson 1:       .\run_project.ps1 -LessonOnly

param(
    [switch]$LessonOnly
)

$ErrorActionPreference = 'Stop'
$projectFolder = $PSScriptRoot
$pythonInVenv = Join-Path $projectFolder '.venv\Scripts\python.exe'

function Run-Python {
    param([string[]]$Arguments)
    & $pythonInVenv @Arguments
    if ($LASTEXITCODE -ne 0) {
        throw "Python command failed with exit code $LASTEXITCODE. Check the error above."
    }
}

Push-Location $projectFolder
try {
    Write-Host '=========================================' -ForegroundColor Cyan
    Write-Host 'Retail Sales & Customer Intelligence' -ForegroundColor Cyan
    Write-Host '=========================================' -ForegroundColor Cyan

    if (-not (Test-Path $pythonInVenv)) {
        Write-Host '[1/3] Creating a Python virtual environment...'
        if (Get-Command py -ErrorAction SilentlyContinue) {
            & py -m venv .venv
        }
        elseif (Get-Command python -ErrorAction SilentlyContinue) {
            & python -m venv .venv
        }
        else {
            throw 'Python not found. Install Python from python.org and reopen PowerShell.'
        }
        if ($LASTEXITCODE -ne 0 -or -not (Test-Path $pythonInVenv)) {
            throw 'Could not create the Python environment.'
        }
    }
    else {
        Write-Host '[1/3] Python environment already exists.'
    }

    Write-Host '[2/3] Installing project packages (first run may take a few minutes)...'
    Run-Python -Arguments @('-m', 'pip', 'install', '-r', 'requirements.txt')

    Write-Host '[3/3] Running Lesson 1 with the practice dataset...' -ForegroundColor Green
    Run-Python -Arguments @('lessons\01_first_analysis.py')

    if (-not $LessonOnly) {
        Write-Host ''
        Write-Host 'Starting your Streamlit dashboard...' -ForegroundColor Green
        Write-Host 'Open the Local URL displayed below. Press Ctrl+C to stop.'
        Run-Python -Arguments @('-m', 'streamlit', 'run', 'app.py')
    }
    else {
        Write-Host 'Lesson 1 finished. Run without -LessonOnly to open the dashboard.' -ForegroundColor Green
    }
}
catch {
    Write-Host "Problem: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}
finally {
    Pop-Location
}
