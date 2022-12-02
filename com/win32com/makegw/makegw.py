"""Utility functions for writing out gateway C++ files

  This module will generate a C++/Python binding for a specific COM
  interface.

  At this stage, no command line interface exists.  You must start Python,
  import this module,  change to the directory where the generated code should
  be written, and run the public function.

  This module is capable of generating both 'Interfaces' (ie, Python
  client side support for the interface) and 'Gateways' (ie, Python
  server side support for the interface).  Many COM interfaces are useful
  both as Client and Server.  Other interfaces, however, really only make
  sense to implement one side or the other.  For example, it would be pointless
  for Python to implement Server side for 'IRunningObjectTable', unless we were
  implementing core COM for an operating system in Python (hey - now there's an idea!)

  Most COM interface code is totally boiler-plate - it consists of
  converting arguments, dispatching the call to Python, and processing
  any result values.

  This module automates the generation of such code.  It has the ability to
  parse a .H file generated by the MIDL tool (ie, almost all COM .h files)
  and build almost totally complete C++ code.

  The module understands some of the well known data types, and how to
  convert them.  There are only a couple of places where hand-editing is
  necessary, as detailed below:

  unsupported types -- If a type is not known, the generator will
  pretty much ignore it, but write a comment to the generated code.  You
  may want to add custom support for this type.  In some cases, C++ compile errors
  will result.  These are intentional - generating code to remove these errors would
  imply a false sense of security that the generator has done the right thing.

  other return policies -- By default, Python never sees the return SCODE from
  a COM function.  The interface usually returns None if OK, else a COM exception
  if "FAILED(scode)" is TRUE.  You may need to change this if:
  * EXCEPINFO is passed to the COM function.  This is not detected and handled
  * For some reason Python should always see the result SCODE, even if it
    did fail or succeed.  For example, some functions return a BOOLEAN result
    in the SCODE, meaning Python should always see it.
  * FAILED(scode) for the interface still has valid data to return (by default,
    the code generated does not process the return values, and raise an exception
    to Python/COM

"""

import re

from . import makegwparse


def make_framework_support(
    header_file_name, interface_name, bMakeInterface=1, bMakeGateway=1
):
    """Generate C++ code for a Python Interface and Gateway

    header_file_name -- The full path to the .H file which defines the interface.
    interface_name -- The name of the interface to search for, and to generate.
    bMakeInterface = 1 -- Should interface (ie, client) support be generated.
    bMakeGatewayInterface = 1 -- Should gateway (ie, server) support be generated.

    This method will write a .cpp and .h file into the current directory,
    (using the name of the interface to build the file name.

    """
    fin = open(header_file_name)
    try:
        interface = makegwparse.parse_interface_info(interface_name, fin)
    finally:
        fin.close()
    assert (
        interface is not None
    ), f"No interface for interface: {interface_name} with header: {header_file_name}"

    if bMakeInterface and bMakeGateway:
        desc = "Interface and Gateway"
    elif bMakeInterface and not bMakeGateway:
        desc = "Interface"
    else:
        desc = "Gateway"
    if interface.name[:5] == "IEnum":  # IEnum - use my really simple template-based one
        import win32com.makegw.makegwenum

        ifc_cpp_writer = win32com.makegw.makegwenum._write_enumifc_cpp
        gw_cpp_writer = win32com.makegw.makegwenum._write_enumgw_cpp
    else:  # Use my harder working ones.
        ifc_cpp_writer = _write_ifc_cpp
        gw_cpp_writer = _write_gw_cpp

    fout = open("Py%s.cpp" % interface.name, "w")
    try:
        fout.write(
            """\
// This file implements the %s %s for Python.
// Generated by makegw.py

#include "shell_pch.h"
"""
            % (interface.name, desc)
        )
        #    if bMakeGateway:
        #      fout.write('#include "PythonCOMServer.h"\n')
        #    if interface.base not in ["IUnknown", "IDispatch"]:
        #      fout.write('#include "Py%s.h"\n' % interface.base)
        fout.write(
            '#include "Py%s.h"\n\n// @doc - This file contains autoduck documentation\n'
            % interface.name
        )
        if bMakeInterface:
            ifc_cpp_writer(fout, interface)
        if bMakeGateway:
            gw_cpp_writer(fout, interface)
    finally:
        fout.close()
    fout = open("Py%s.h" % interface.name, "w")
    try:
        fout.write(
            """\
// This file declares the %s %s for Python.
// Generated by makegw.py
"""
            % (interface.name, desc)
        )

        if bMakeInterface:
            _write_ifc_h(fout, interface)
        if bMakeGateway:
            _write_gw_h(fout, interface)
    finally:
        fout.close()


###########################################################################
#
# INTERNAL FUNCTIONS
#
#


def _write_ifc_h(f, interface):
    f.write(
        """\
// ---------------------------------------------------
//
// Interface Declaration

class Py%s : public Py%s
{
public:
	MAKE_PYCOM_CTOR(Py%s);
	static %s *GetI(PyObject *self);
	static PyComTypeObject type;

	// The Python methods
"""
        % (interface.name, interface.base, interface.name, interface.name)
    )
    for method in interface.methods:
        f.write(
            "\tstatic PyObject *%s(PyObject *self, PyObject *args);\n" % method.name
        )
    f.write(
        """\

protected:
	Py%s(IUnknown *pdisp);
	~Py%s();
};
"""
        % (interface.name, interface.name)
    )


def _write_ifc_cpp(f, interface):
    name = interface.name
    f.write(
        """\
// ---------------------------------------------------
//
// Interface Implementation

Py%(name)s::Py%(name)s(IUnknown *pdisp):
	Py%(base)s(pdisp)
{
	ob_type = &type;
}

Py%(name)s::~Py%(name)s()
{
}

/* static */ %(name)s *Py%(name)s::GetI(PyObject *self)
{
	return (%(name)s *)Py%(base)s::GetI(self);
}

"""
        % (interface.__dict__)
    )

    ptr = re.sub("[a-z]", "", interface.name)
    strdict = {"interfacename": interface.name, "ptr": ptr}
    for method in interface.methods:
        strdict["method"] = method.name
        f.write(
            """\
// @pymethod |Py%(interfacename)s|%(method)s|Description of %(method)s.
PyObject *Py%(interfacename)s::%(method)s(PyObject *self, PyObject *args)
{
	%(interfacename)s *p%(ptr)s = GetI(self);
	if ( p%(ptr)s == NULL )
		return NULL;
"""
            % strdict
        )
        argsParseTuple = (
            argsCOM
        ) = (
            formatChars
        ) = codePost = codePobjects = codeCobjects = cleanup = cleanup_gil = ""
        needConversion = 0
        #    if method.name=="Stat": import win32dbg;win32dbg.brk()
        for arg in method.args:
            try:
                argCvt = makegwparse.make_arg_converter(arg)
                if arg.HasAttribute("in"):
                    val = argCvt.GetFormatChar()
                    if val:
                        f.write("\t" + argCvt.GetAutoduckString() + "\n")
                        formatChars = formatChars + val
                        argsParseTuple = (
                            argsParseTuple + ", " + argCvt.GetParseTupleArg()
                        )
                        codePobjects = (
                            codePobjects + argCvt.DeclareParseArgTupleInputConverter()
                        )
                        codePost = codePost + argCvt.GetParsePostCode()
                        needConversion = needConversion or argCvt.NeedUSES_CONVERSION()
                        cleanup = cleanup + argCvt.GetInterfaceArgCleanup()
                        cleanup_gil = cleanup_gil + argCvt.GetInterfaceArgCleanupGIL()
                comArgName, comArgDeclString = argCvt.GetInterfaceCppObjectInfo()
                if comArgDeclString:  # If we should declare a variable
                    codeCobjects = codeCobjects + "\t%s;\n" % (comArgDeclString)
                argsCOM = argsCOM + ", " + comArgName
            except makegwparse.error_not_supported as why:
                f.write(
                    '// *** The input argument %s of type "%s" was not processed ***\n//     Please check the conversion function is appropriate and exists!\n'
                    % (arg.name, arg.raw_type)
                )

                f.write(
                    "\t%s %s;\n\tPyObject *ob%s;\n" % (arg.type, arg.name, arg.name)
                )
                f.write(
                    "\t// @pyparm <o Py%s>|%s||Description for %s\n"
                    % (arg.type, arg.name, arg.name)
                )
                codePost = (
                    codePost
                    + "\tif (bPythonIsHappy && !PyObject_As%s( ob%s, &%s )) bPythonIsHappy = FALSE;\n"
                    % (arg.type, arg.name, arg.name)
                )

                formatChars = formatChars + "O"
                argsParseTuple = argsParseTuple + ", &ob%s" % (arg.name)

                argsCOM = argsCOM + ", " + arg.name
                cleanup = cleanup + "\tPyObject_Free%s(%s);\n" % (arg.type, arg.name)

        if needConversion:
            f.write("\tUSES_CONVERSION;\n")
        f.write(codePobjects)
        f.write(codeCobjects)
        f.write(
            '\tif ( !PyArg_ParseTuple(args, "%s:%s"%s) )\n\t\treturn NULL;\n'
            % (formatChars, method.name, argsParseTuple)
        )
        if codePost:
            f.write("\tBOOL bPythonIsHappy = TRUE;\n")
            f.write(codePost)
            f.write("\tif (!bPythonIsHappy) return NULL;\n")
        strdict["argsCOM"] = argsCOM[1:]
        strdict["cleanup"] = cleanup
        strdict["cleanup_gil"] = cleanup_gil
        f.write(
            """	HRESULT hr;
	PY_INTERFACE_PRECALL;
	hr = p%(ptr)s->%(method)s(%(argsCOM)s );
%(cleanup)s
	PY_INTERFACE_POSTCALL;
%(cleanup_gil)s
	if ( FAILED(hr) )
		return PyCom_BuildPyException(hr, p%(ptr)s, IID_%(interfacename)s );
"""
            % strdict
        )
        codePre = codePost = formatChars = codeVarsPass = codeDecl = ""
        for arg in method.args:
            if not arg.HasAttribute("out"):
                continue
            try:
                argCvt = makegwparse.make_arg_converter(arg)
                formatChar = argCvt.GetFormatChar()
                if formatChar:
                    formatChars = formatChars + formatChar
                    codePre = codePre + argCvt.GetBuildForInterfacePreCode()
                    codePost = codePost + argCvt.GetBuildForInterfacePostCode()
                    codeVarsPass = codeVarsPass + ", " + argCvt.GetBuildValueArg()
                    codeDecl = codeDecl + argCvt.DeclareParseArgTupleInputConverter()
            except makegwparse.error_not_supported as why:
                f.write(
                    '// *** The output argument %s of type "%s" was not processed ***\n//     %s\n'
                    % (arg.name, arg.raw_type, why)
                )
                continue
        if formatChars:
            f.write(
                '%s\n%s\tPyObject *pyretval = Py_BuildValue("%s"%s);\n%s\treturn pyretval;'
                % (codeDecl, codePre, formatChars, codeVarsPass, codePost)
            )
        else:
            f.write("\tPy_INCREF(Py_None);\n\treturn Py_None;\n")
        f.write("\n}\n\n")

    f.write("// @object Py%s|Description of the interface\n" % (name))
    f.write("static struct PyMethodDef Py%s_methods[] =\n{\n" % name)
    for method in interface.methods:
        f.write(
            '\t{ "%s", Py%s::%s, 1 }, // @pymeth %s|Description of %s\n'
            % (method.name, interface.name, method.name, method.name, method.name)
        )

    interfacebase = interface.base
    f.write(
        """\
	{ NULL }
};

PyComTypeObject Py%(name)s::type("Py%(name)s",
		&Py%(interfacebase)s::type,
		sizeof(Py%(name)s),
		Py%(name)s_methods,
		GET_PYCOM_CTOR(Py%(name)s));
"""
        % locals()
    )


def _write_gw_h(f, interface):
    if interface.name[0] == "I":
        gname = "PyG" + interface.name[1:]
    else:
        gname = "PyG" + interface.name
    name = interface.name
    if interface.base == "IUnknown" or interface.base == "IDispatch":
        base_name = "PyGatewayBase"
    else:
        if interface.base[0] == "I":
            base_name = "PyG" + interface.base[1:]
        else:
            base_name = "PyG" + interface.base
    f.write(
        """\
// ---------------------------------------------------
//
// Gateway Declaration

class %s : public %s, public %s
{
protected:
	%s(PyObject *instance) : %s(instance) { ; }
	PYGATEWAY_MAKE_SUPPORT2(%s, %s, IID_%s, %s)

"""
        % (gname, base_name, name, gname, base_name, gname, name, name, base_name)
    )
    if interface.base != "IUnknown":
        f.write(
            "\t// %s\n\t// *** Manually add %s method decls here\n\n"
            % (interface.base, interface.base)
        )
    else:
        f.write("\n\n")

    f.write("\t// %s\n" % name)

    for method in interface.methods:
        f.write("\tSTDMETHOD(%s)(\n" % method.name)
        if method.args:
            for arg in method.args[:-1]:
                f.write("\t\t%s,\n" % (arg.GetRawDeclaration()))
            arg = method.args[-1]
            f.write("\t\t%s);\n\n" % (arg.GetRawDeclaration()))
        else:
            f.write("\t\tvoid);\n\n")

    f.write("};\n")
    f.close()


def _write_gw_cpp(f, interface):
    if interface.name[0] == "I":
        gname = "PyG" + interface.name[1:]
    else:
        gname = "PyG" + interface.name
    name = interface.name
    if interface.base == "IUnknown" or interface.base == "IDispatch":
        base_name = "PyGatewayBase"
    else:
        if interface.base[0] == "I":
            base_name = "PyG" + interface.base[1:]
        else:
            base_name = "PyG" + interface.base
    f.write(
        """\
// ---------------------------------------------------
//
// Gateway Implementation
"""
        % {"name": name, "gname": gname, "base_name": base_name}
    )

    for method in interface.methods:
        f.write(
            """\
STDMETHODIMP %s::%s(
"""
            % (gname, method.name)
        )

        if method.args:
            for arg in method.args[:-1]:
                inoutstr = "][".join(arg.inout)
                f.write("\t\t/* [%s] */ %s,\n" % (inoutstr, arg.GetRawDeclaration()))

            arg = method.args[-1]
            inoutstr = "][".join(arg.inout)
            f.write("\t\t/* [%s] */ %s)\n" % (inoutstr, arg.GetRawDeclaration()))
        else:
            f.write("\t\tvoid)\n")

        f.write("{\n\tPY_GATEWAY_METHOD;\n")
        cout = 0
        codePre = codePost = codeVars = ""
        argStr = ""
        needConversion = 0
        formatChars = ""
        if method.args:
            for arg in method.args:
                if arg.HasAttribute("out"):
                    cout = cout + 1
                    if arg.indirectionLevel == 2:
                        f.write("\tif (%s==NULL) return E_POINTER;\n" % arg.name)
                if arg.HasAttribute("in"):
                    try:
                        argCvt = makegwparse.make_arg_converter(arg)
                        argCvt.SetGatewayMode()
                        formatchar = argCvt.GetFormatChar()
                        needConversion = needConversion or argCvt.NeedUSES_CONVERSION()

                        if formatchar:
                            formatChars = formatChars + formatchar
                            codeVars = (
                                codeVars + argCvt.DeclareParseArgTupleInputConverter()
                            )
                            argStr = argStr + ", " + argCvt.GetBuildValueArg()
                        codePre = codePre + argCvt.GetBuildForGatewayPreCode()
                        codePost = codePost + argCvt.GetBuildForGatewayPostCode()
                    except makegwparse.error_not_supported as why:
                        f.write(
                            '// *** The input argument %s of type "%s" was not processed ***\n//   - Please ensure this conversion function exists, and is appropriate\n//   - %s\n'
                            % (arg.name, arg.raw_type, why)
                        )
                        f.write(
                            "\tPyObject *ob%s = PyObject_From%s(%s);\n"
                            % (arg.name, arg.type, arg.name)
                        )
                        f.write(
                            '\tif (ob%s==NULL) return MAKE_PYCOM_GATEWAY_FAILURE_CODE("%s");\n'
                            % (arg.name, method.name)
                        )
                        codePost = codePost + "\tPy_DECREF(ob%s);\n" % arg.name
                        formatChars = formatChars + "O"
                        argStr = argStr + ", ob%s" % (arg.name)

        if needConversion:
            f.write("\tUSES_CONVERSION;\n")
        f.write(codeVars)
        f.write(codePre)
        if cout:
            f.write("\tPyObject *result;\n")
            resStr = "&result"
        else:
            resStr = "NULL"

        if formatChars:
            fullArgStr = '%s, "%s"%s' % (resStr, formatChars, argStr)
        else:
            fullArgStr = resStr

        f.write('\tHRESULT hr=InvokeViaPolicy("%s", %s);\n' % (method.name, fullArgStr))
        f.write(codePost)
        if cout:
            f.write("\tif (FAILED(hr)) return hr;\n")
            f.write(
                "\t// Process the Python results, and convert back to the real params\n"
            )
            # process the output arguments.
            formatChars = codePobjects = codePost = argsParseTuple = ""
            needConversion = 0
            for arg in method.args:
                if not arg.HasAttribute("out"):
                    continue
                try:
                    argCvt = makegwparse.make_arg_converter(arg)
                    argCvt.SetGatewayMode()
                    val = argCvt.GetFormatChar()
                    if val:
                        formatChars = formatChars + val
                        argsParseTuple = (
                            argsParseTuple + ", " + argCvt.GetParseTupleArg()
                        )
                        codePobjects = (
                            codePobjects + argCvt.DeclareParseArgTupleInputConverter()
                        )
                        codePost = codePost + argCvt.GetParsePostCode()
                        needConversion = needConversion or argCvt.NeedUSES_CONVERSION()
                except makegwparse.error_not_supported as why:
                    f.write(
                        '// *** The output argument %s of type "%s" was not processed ***\n//     %s\n'
                        % (arg.name, arg.raw_type, why)
                    )

            if formatChars:  # If I have any to actually process.
                if len(formatChars) == 1:
                    parseFn = "PyArg_Parse"
                else:
                    parseFn = "PyArg_ParseTuple"
                if codePobjects:
                    f.write(codePobjects)
                f.write(
                    '\tif (!%s(result, "%s" %s))\n\t\treturn MAKE_PYCOM_GATEWAY_FAILURE_CODE("%s");\n'
                    % (parseFn, formatChars, argsParseTuple, method.name)
                )
            if codePost:
                f.write("\tBOOL bPythonIsHappy = TRUE;\n")
                f.write(codePost)
                f.write(
                    '\tif (!bPythonIsHappy) hr = MAKE_PYCOM_GATEWAY_FAILURE_CODE("%s");\n'
                    % method.name
                )
            f.write("\tPy_DECREF(result);\n")
        f.write("\treturn hr;\n}\n\n")


def test():
    # 	make_framework_support("d:\\msdev\\include\\objidl.h", "ILockBytes")
    make_framework_support("d:\\msdev\\include\\objidl.h", "IStorage")


# 	make_framework_support("d:\\msdev\\include\\objidl.h", "IEnumSTATSTG")
