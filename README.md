# pywin32

[![CI](https://github.com/mhammond/pywin32/workflows/CI/badge.svg)](https://github.com/mhammond/pywin32/actions?query=workflow%3ACI)
[![PyPI - Version](https://img.shields.io/pypi/v/pywin32.svg)](https://pypi.org/project/pywin32)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pywin32.svg)](https://pypi.org/project/pywin32)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/pywin32.svg)](https://pypi.org/project/pywin32)
[![License - PSF-2.0](https://img.shields.io/badge/license-PSF--2.0-9400d3.svg)](https://spdx.org/licenses/PSF-2.0.html)

-----

This is the readme for the Python for Win32 (pywin32) extensions, which provides access to many of the Windows APIs from Python, including COM support.

See [CHANGES.txt](https://github.com/mhammond/pywin32/blob/main/CHANGES.txt) for recent notable changes.

adodbapi's documentation can be found in: [adodbapi/readme.txt](https://github.com/mhammond/pywin32/blob/main/adodbapi/readme.txt)

isapi's documentation can be found in: [isapi/README.txt](https://github.com/mhammond/pywin32/blob/main/isapi/README.txt)

## Docs

The docs are a long and sad story, but [there's now an online version](https://mhammond.github.io/pywin32/)
of the `PyWin32.chm` helpfile (thanks [@ofek](https://github.com/mhammond/pywin32/pull/1774)!).
Lots of that is very old, but some is auto-generated and current. Would love help untangling the docs!

## Support

Feel free to [open issues](https://github.com/mhammond/pywin32/issues) for
all bugs (or suspected bugs) in pywin32. [pull-requests](https://github.com/mhammond/pywin32/pulls)
for all bugs or features are also welcome.

However, please **do not open github issues for general support requests**, or
for problems or questions using the modules in this package - they will be
closed. For such issues, please email the
[python-win32 mailing list](https://mail.python.org/mailman/listinfo/python-win32) -
note that you must be subscribed to the list before posting.

## Binaries

[Binary releases are no longer supported.](https://mhammond.github.io/pywin32_installers.html)

Build 306 was the last with .exe installers. You really shouldn't use them, but if you really need them,
[find them here](https://github.com/mhammond/pywin32/releases/tag/b306)

## Installing via PIP

You should install pywin32 via pip - eg,

```shell
python -m pip install --upgrade pywin32
```

There is a post-install script (see below) which should *not* be run inside virtual environments;
it should only be run in "global" installs.

For unreleased changes, you can download builds made by [github actions](https://github.com/mhammond/pywin32/actions/) -
choose any "workflow" from the `main` branch and download its "artifacts")

### Installing globally

Outside of a virtual environment you might want to install COM objects, services, etc. You can do
this by executing:

```shell
python Scripts/pywin32_postinstall.py -install
```

From the root of your Python installation.

If you do this with normal permissions it will be global for your user (a few files will be
copied to the root of your Python install and some changes made to HKCU). If you execute this from
an elevated process, it will be global for the machine (files will be copied to System32, HKLM
will be changed, etc)

### Installing for MingGW/msys2

The folks at <https://github.com/msys2/MINGW-packages/tree/master/mingw-w64-python-pywin32> are graciously keeping an updated set of patches to install pywin32 for MingGW/msys2.

We'd suggest installing from <https://packages.msys2.org/base/mingw-w64-python-pywin32> `pacman -S mingw-w64-python-pywin32`.

We're open to seeing these patches be upstreamed in pywin32 if they can be tested automatically on the CI.

### Running as a Windows Service

To run as a service, you probably want to install pywin32 globally from an elevated
command prompt - see above.

You also need to ensure Python is installed in a location where the user running
the service has access to the installation and is able to load `pywintypesXX.dll` and `pythonXX.dll`.
In particular, the `LocalSystem` account typically will not have access to your local `%USER%` directory structure.

## Troubleshooting

If you encounter any problems when upgrading like the following:

```text
The specified procedure could not be found
Entry-point not found
```

It usually means one of 2 things:

* You've upgraded an install where the post-install script has previously run.
So you should run it again:

    ```shell
    python Scripts/pywin32_postinstall.py -install
    ```

    This will make some small attempts to cleanup older conflicting installs.

* There are other pywin32 DLLs installed in your system,
but in a different location than the new ones. This sometimes happens in environments that
come with pywin32 pre-shipped (eg, anaconda?).

  The possible solutions here are:

  * Run the "post_install" script documented above.
  * Otherwise, find and remove all other copies of `pywintypesXX.dll` and `pythoncomXX.dll`
  (where `XX` is the Python version - eg, "39")

## Building from source

Install Visual Studio 2019 (later probably works, but options might be different),
follow the instructions in [Build environment](/build_env.md#build-environment)
for the version you install.

Then follow the [Build](/build_env.md#build) instructions for the build itself (including ARM64 cross-compilation).

## Release process

The following steps are performed when making a new release - this is mainly
to form a checklist so @mhammond doesn't forget what to do :)

Since build 307 the release process is based on the artifacts created by Github actions.

* Ensure CHANGES.txt has everything worth noting. Update the header to reflect
  the about-to-be released build and date, commit it.

* Update setup.py with the new build number. Update CHANGES.txt to have a new heading
  section for the next unreleased version. (ie, a new, empty "Coming in build XXX, as yet unreleased"
  section)

* Push these changes to github, wait for the actions to complete, then
  download the artifacts from that run.

* Upload `.whl` artifacts to pypi - we do this before pushing the tag because they might be
  rejected for an invalid `README.md`. Done via `py -3.? -m twine upload dist/*XXX*.whl`.

* Create a new git tag for the release.

* Update setup.py with the new build number + ".1" (eg, 123.1), to ensure
  future test builds aren't mistaken for the real release.

* Make sure everything is pushed to github, including the tag (ie,
  `git push --tags`)

* Send mail to python-win32

### Older Manual Release Process

This is the old process used when a local dev environment was used to create
the builds. Build 306 was the last released with this process.

* Ensure CHANGES.txt has everything worth noting. Update the header to reflect
  the about-to-be released build and date, commit it.

* Update setup.py with the new build number.

* Execute `make_all.bat`, wait forever, test the artifacts.

* Upload .whl artifacts to pypi - we do this before pushing the tag because they might be
  rejected for an invalid `README.md`. Done via `py -3.? -m twine upload dist/*XXX*.whl`.

* Commit setup.py (so the new build number is in the repo), create a new git tag

* Upload the .exe installers to github.

* Update setup.py with the new build number + ".1" (eg, 123.1), to ensure
  future test builds aren't mistaken for the real release.

* Make sure everything is pushed to github, including the tag (ie,
  `git push --tags`)

* Send mail to python-win32
