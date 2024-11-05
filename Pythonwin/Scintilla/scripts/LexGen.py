#!/usr/bin/env python3
# LexGen.py - implemented 2002 by Neil Hodgson neilh@scintilla.org
# Released to the public domain.

# Regenerate the Scintilla source files that list all the lexers.
# Should be run whenever a new lexer is added or removed.
# Requires Python 3.6 or later
# Files are regenerated in place with templates stored in comments.
# The format of generation comments is documented in FileGenerator.py.
# Also updates version numbers and modification dates.

import os
import pathlib
import sys

import ScintillaData
from FileGenerator import Regenerate

baseDirectory = os.path.dirname(os.path.dirname(ScintillaData.__file__))
sys.path.append(baseDirectory)

import win32.DepGen


def RegenerateAll(rootDirectory):
    root = pathlib.Path(rootDirectory)

    scintillaBase = root.resolve()

    lexfiles = (scintillaBase / "lexers").glob("Lex*.cxx")
    lexerModules = []
    for file in lexfiles:
        for module in ScintillaData.FindModules(file):
            lexerModules.append(module[0])

    Regenerate(scintillaBase / "src/Catalogue.cxx", "//", lexerModules)
    Regenerate(scintillaBase / "win32/scintilla.mak", "#", [f.stem for f in lexfiles])

    startDir = os.getcwd()
    os.chdir(os.path.join(scintillaBase, "win32"))
    win32.DepGen.Generate()
    os.chdir(startDir)


if __name__ == "__main__":
    RegenerateAll(pathlib.Path(__file__).resolve().parent.parent)
