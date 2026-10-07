#!/usr/bin/env pwsh
if (-not $IsLinux) {
    Write-Error "Linux required: use MSYS2 on Windows for native MinGW builds"
    exit 1
}

uv pip install build setuptools

$Msys2PythonTmpDir = '/tmp/msys2-python'
$PythonVer = uv run python -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')"
$WinPythonLib = "$Msys2PythonTmpDir/mingw64/lib"
$WinPythonInclude = "$Msys2PythonTmpDir/mingw64/include/python${PythonVer}"

if (-not (Test-Path "$WinPythonInclude/Python.h")) {
    # Find the correct Python package on the MSYS2 repo
    $RepoUrl = 'https://repo.msys2.org/mingw/mingw64/'
    $Html = Invoke-WebRequest $RepoUrl -UseBasicParsing
    $PkgName = ([regex]::Matches($Html.Content, 'href="([^"]*python-' + [regex]::Escape($PythonVer) + '\.[^"]*)"')
        | Where-Object { $_.Groups[1].Value -notmatch 'docs|test|tkinter|pyc|pip|setuptools' }
        | Select-Object -First 1).Groups[1].Value

    if (-not $PkgName) {
        Write-Error "No MSYS2 package found for Python $PythonVer at ${RepoUrl}. Run 'uv python pin <ver>' to match an available MSYS2 Python version."
        exit 1
    }

    Write-Host "Downloading $PkgName ..."
    New-Item -ItemType Directory -Force $Msys2PythonTmpDir | Out-Null
    Invoke-WebRequest "${RepoUrl}${PkgName}" -OutFile "$Msys2PythonTmpDir/python.pkg.tar.zst"
    bash -c "cd $Msys2PythonTmpDir && tar -x --zstd -f python.pkg.tar.zst mingw64/lib/libpython${PythonVer}.dll.a mingw64/include/python${PythonVer}/"
}
else {
    Write-Host "$WinPythonInclude already extracted, skipping download"
}

# $WinProgramFilesSearchRoots = @($Env:HOME, '/mnt', '/media', '/run/media') | Where-Object { Test-Path $_ }

$Env:CC = 'x86_64-w64-mingw32-gcc'
$Env:CXX = 'x86_64-w64-mingw32-g++'
$Env:AR = 'x86_64-w64-mingw32-ar'
$Env:RANLIB = 'x86_64-w64-mingw32-ranlib'
$Env:LDSHARED = 'x86_64-w64-mingw32-gcc -shared'

$Env:CFLAGS = "-w -I$WinPythonInclude"
$Env:CXXFLAGS = "-w -I$WinPythonInclude"
$Env:WIN_PYTHON_LIB = $WinPythonLib
$Env:WIN_PYTHON_INC = $WinPythonInclude
$Env:LDFLAGS = '-Wl,--allow-shlib-undefined'

$Env:_PYTHON_HOST_PLATFORM = 'win-amd64'

$Env:RC = 'x86_64-w64-mingw32-windres'
$Env:WINDRES = 'x86_64-w64-mingw32-windres'
$Env:WINDMC = 'x86_64-w64-mingw32-windmc'
$Env:SWIG = 'SWIG/swig_wine.ps1' | Resolve-Path
# $Env:MFC_INCLUDE_PATH = Get-ChildItem -Path $WinProgramFilesSearchRoots -Recurse -Directory -Filter 'Program Files (x86)' -ErrorAction SilentlyContinue |
#     ForEach-Object { Get-Item "$($_.FullName)/Microsoft Visual Studio/*/BuildTools/VC/Tools/MSVC/*/atlmfc/include" -ErrorAction SilentlyContinue } |
#     Select-Object -First 1 -ExpandProperty FullName

uv run python -m build --wheel --no-isolation --config-setting=--build-option="build_ext --plat-name=win-amd64"
