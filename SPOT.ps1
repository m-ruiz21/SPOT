param(
    [Alias("c")]
    [switch]$CreateEnv,
    [Alias("s")]
    [switch]$StartEnv,
    [Alias("e")]
    [switch]$EndEnv,
    [Alias("i")]
    [switch]$InstallDeps,
    [Alias("b")]
    [switch]$Build,
    [switch]$Setup
)

if ($CreateEnv) {
    py -3.11 -m venv venv
}

if ($StartEnv) {
    venv/Scripts/activate
}

if ($EndEnv) {
    deactivate
} 

if ($InstallDeps) {
    py -m pip install -r .\requirements.txt
}

if ($Build) {
    Set-Location src/lib
    maturin build 
    
    $whl = Get-ChildItem -Path target/wheels -Filter *.whl | ForEach-Object { $_.Name }

    py -m pip install --force-reinstall target/wheels/$whl

    Set-Location ../../
}

if ($Setup) {
    "Setting up virtual environment..." 
    ./SPOT -c
    "Starting Virtual Environment..."
    ./SPOT -s
    "Installing dependencies..."
    ./SPOT -i
    "Building the project..."
    ./SPOT -b
}