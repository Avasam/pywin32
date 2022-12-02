if isinstance(__path__, str):
    # For freeze to work!
    import sys

    try:
        import mapi

        sys.modules["win32com.mapi.mapi"] = mapi
    except ImportError:
        pass
    try:
        import exchange  # pyright: ignore[reportMissingImports]

        sys.modules["win32com.mapi.exchange"] = exchange
    except ImportError:
        pass
    try:
        import exchdapi  # pyright: ignore[reportMissingImports]

        sys.modules["win32com.mapi.exchdapi"] = exchdapi
    except ImportError:
        pass
else:
    import win32com

    # See if we have a special directory for the binaries (for developers)
    win32com.__PackageSupportBuildPath__(__path__)
