#!/usr/bin/env pwsh
if (-not $IsLinux) {
    Write-Error "Linux required: use MSYS2 on Windows for native MinGW builds"
    exit 1
}

uv pip install build setuptools

$Msys2PythonTmpDir = '/tmp/msys2-python'

if ((Test-Path $Msys2PythonTmpDir) -and (Get-ChildItem -Path $Msys2PythonTmpDir).Count -eq 0) {
    # Find the correct Python package on the MSYS2 repo
    $PythonVer = uv run python -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')"
    $RepoUrl = 'https://repo.msys2.org/mingw/mingw64/'
    $Html = Invoke-WebRequest $RepoUrl -UseBasicParsing
    $PkgName = ($Html.Links.href `
        | Where-Object { $_ -match "mingw-w64-x86_64-python-${PythonVer}\." -and $_ -notmatch 'docs|test|tkinter|pyc|pip|setuptools' } `
        | Select-Object -First 1)

    Write-Host "Downloading $PkgName ..."
    New-Item -ItemType Directory -Force $Msys2PythonTmpDir | Out-Null
    Invoke-WebRequest "${RepoUrl}${PkgName}" -OutFile "$Msys2PythonTmpDir/python.pkg.tar.zst"
    bash -c "cd $Msys2PythonTmpDir && tar -x --zstd -f python.pkg.tar.zst mingw64/lib/libpython${PythonVer}.dll.a mingw64/include/python${PythonVer}/"
}
else {
    Write-Host "$Msys2PythonTmpDir already exists and not empty, skipping download"
}

$WinPythonLib = "$Msys2PythonTmpDir/mingw64/lib"
$WinPythonInclude = "$Msys2PythonTmpDir/mingw64/include/python${PythonVer}"

$Env:CC = 'x86_64-w64-mingw32-gcc'
$Env:CXX = 'x86_64-w64-mingw32-g++'
$Env:AR = 'x86_64-w64-mingw32-ar'
$Env:RANLIB = 'x86_64-w64-mingw32-ranlib'
$Env:LDSHARED = 'x86_64-w64-mingw32-gcc -shared'

$Env:CFLAGS = "-w -I$WinPythonInclude"
$Env:CXXFLAGS = "-w -I$WinPythonInclude"
$Env:WIN_PYTHON_LIB = $WinPythonLib
$Env:LDFLAGS = '-Wl,--allow-shlib-undefined'

$Env:_PYTHON_HOST_PLATFORM = 'win-amd64'

$Env:RC = 'x86_64-w64-mingw32-windres'
$Env:WINDRES = 'x86_64-w64-mingw32-windres'
$Env:WINDMC = 'x86_64-w64-mingw32-windmc'
$Env:SWIG = 'SWIG/swig_wine.ps1' | Resolve-Path

uv run python -m build --wheel --no-isolation --config-setting=--build-option="build_ext --plat-name=win-amd64"
