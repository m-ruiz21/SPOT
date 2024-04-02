param(
    [Alias("c")]
    [switch]$CreateEnv,
    [Alias("s")]
    [switch]$StartEnv,
    [Alias("e")]
    [switch]$EndEnv,
    [Alias("i")]
    [switch]$InstallDeps
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
