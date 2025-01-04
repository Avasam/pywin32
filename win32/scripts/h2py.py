#! /usr/bin/env python3
"""
Vendored from https://github.com/python/cpython/blob/3.8/Tools/scripts/h2py.py

Changes since vendored version:
- Minimal changes to satisfy our checkers.
- Rename `p_hex` to `p_signed_hex` and improve to include lowercase l
- Fixed `pytify` to remove leftover L after numbers and actually compute negative hexadecimal constants
- Added `p_int_cast` and `p_literal_constant`

---

Read #define's and translate to Python code.
Handle #include statements.
Handle #define macros with one argument.
Anything that isn't recognized or doesn't translate into valid
Python is ignored.

Without filename arguments, acts as a filter.
If one or more filenames are given, output is written to corresponding
filenames in the local directory, translated to all uppercase, with
the extension replaced by ".py".

By passing one or more options of the form "-i regular_expression"
you can specify additional strings to be ignored.  This is useful
e.g. to ignore casts to u_long: simply specify "-i '(u_long)'".
"""

# XXX To do:
# - turn trailing C comments into Python comments
# - turn C Boolean operators "&& || !" into Python "and or not"
# - what to do about #if(def)?
# - what to do about macros with multiple parameters?
from __future__ import annotations

import ctypes
import getopt
import os
import re
import sys

p_define = re.compile(r"^[\t ]*#[\t ]*define[\t ]+([a-zA-Z0-9_]+)[\t ]+")

p_macro = re.compile(
    r"^[\t ]*#[\t ]*define[\t ]+" r"([a-zA-Z0-9_]+)\(([_a-zA-Z][_a-zA-Z0-9]*)\)[\t ]+"
)

p_include = re.compile(r"^[\t ]*#[\t ]*include[\t ]+<([^>\n]+)>")

p_comment = re.compile(r"/\*([^*]+|\*+[^/])*(\*+/)?")
p_cpp_comment = re.compile("//.*")
# Maybe we want these to cause integer truncation instead?
p_int_cast = re.compile(r"\((DWORD|HRESULT|SCODE|LONG|HWND|HANDLE|int|HBITMAP)\)")

ignores = [p_comment, p_cpp_comment, p_int_cast]

p_char = re.compile(r"'(\\.[^\\]*|[^\\])'")
p_signed_hex = re.compile(r"0x([0-9a-fA-F]+)[lL]?")
p_literal_constant = re.compile(r"((0x[0-9a-fA-F]+?)|([0-9]+?))[uUlL]")

filedict: dict[str, None] = {}
importable: dict[str, str] = {}

try:
    searchdirs = os.environ["include"].split(";")
except KeyError:
    try:
        searchdirs = os.environ["INCLUDE"].split(";")
    except KeyError:
        searchdirs = ["/usr/include"]
        try:
            searchdirs.insert(0, os.path.join("/usr/include", os.environ["MULTIARCH"]))
        except KeyError:
            pass


def main():
    global filedict
    opts, args = getopt.getopt(sys.argv[1:], "i:")
    for o, a in opts:
        if o == "-i":
            ignores.append(re.compile(a))
    if not args:
        args = ["-"]
    for filename in args:
        if filename == "-":
            sys.stdout.write("# Generated by h2py from stdin\n")
            process(sys.stdin, sys.stdout)
        else:
            with open(filename) as fp:
                outfile = os.path.basename(filename)
                i = outfile.rfind(".")
                if i > 0:
                    outfile = outfile[:i]
                modname = outfile.upper()
                outfile = modname + ".py"
                with open(outfile, "w") as outfp:
                    outfp.write("# Generated by h2py from %s\n" % filename)
                    filedict = {}
                    for dir in searchdirs:
                        if filename[: len(dir)] == dir:
                            filedict[filename[len(dir) + 1 :]] = None  # no '/' trailing
                            importable[filename[len(dir) + 1 :]] = modname
                            break
                    process(fp, outfp)


def pytify(body):
    # replace ignored patterns by spaces
    for p in ignores:
        body = p.sub(" ", body)
    # replace char literals by ord(...)
    body = p_char.sub("ord('\\1')", body)
    # Compute negative hexadecimal constants
    start = 0
    while 1:
        m = p_signed_hex.search(body, start)
        if not m:
            break
        s, e = m.span()
        val = ctypes.c_int32(int(body[slice(*m.span(1))], 16)).value
        if val < 0:
            body = body[:s] + "(" + str(val) + ")" + body[e:]
        start = s + 1
    # remove literal constant indicator (u U l L)
    body = p_literal_constant.sub("\\1", body)
    return body


def process(fp, outfp, env={}):
    lineno = 0
    while 1:
        line = fp.readline()
        if not line:
            break
        lineno = lineno + 1
        match = p_define.match(line)
        if match:
            # gobble up continuation lines
            while line[-2:] == "\\\n":
                nextline = fp.readline()
                if not nextline:
                    break
                lineno = lineno + 1
                line = line + nextline
            name = match.group(1)
            body = line[match.end() :]
            body = pytify(body)
            ok = 0
            stmt = "%s = %s\n" % (name, body.strip())
            try:
                exec(stmt, env)
            except:
                sys.stderr.write("Skipping: %s" % stmt)
            else:
                outfp.write(stmt)
        match = p_macro.match(line)
        if match:
            macro, arg = match.group(1, 2)
            body = line[match.end() :]
            body = pytify(body)
            stmt = "def %s(%s): return %s\n" % (macro, arg, body)
            try:
                exec(stmt, env)
            except:
                sys.stderr.write("Skipping: %s" % stmt)
            else:
                outfp.write(stmt)
        match = p_include.match(line)
        if match:
            regs = match.regs
            a, b = regs[1]
            filename = line[a:b]
            if filename in importable:
                outfp.write("from %s import *\n" % importable[filename])
            elif filename not in filedict:
                filedict[filename] = None
                inclfp = None
                for dir in searchdirs:
                    try:
                        inclfp = open(dir + "/" + filename)
                        break
                    except OSError:
                        pass
                if inclfp:
                    with inclfp:
                        outfp.write("\n# Included from %s\n" % filename)
                        process(inclfp, outfp, env)
                else:
                    sys.stderr.write("Warning - could not find file %s\n" % filename)


if __name__ == "__main__":
    main()
