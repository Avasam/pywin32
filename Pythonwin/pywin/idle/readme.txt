Pythonwin IDLE directory
------------------------

This directory contains IDLE extensions used by
Pythonwin.  The files in this directory were taken directly from
https://github.com/python/cpython/blob/v3.8.18/Lib/idlelib

If you use IDLE from the same Python version, then the files should be
identical.  If you have a Python version installed that is more recent,
then you may notice differences.  

Pythonwin will look for IDLE extensions first in this directory, then on
the global sys.path.  Thus, if you have IDLE installed and run it from
source, you may remove most of the extensions from this
directory, and the latest versions will then be used.  
