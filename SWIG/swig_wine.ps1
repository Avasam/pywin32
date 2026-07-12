#!/usr/bin/env pwsh
exec wine (Join-Path $PSScriptRoot 'swig.exe') @args
