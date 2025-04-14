// This file implements the IQueryAssociations Interface and Gateway for Python.
// Generated by makegw.py

#include "shell_pch.h"
#include "PyIQueryAssociations.h"

// @doc - This file contains autoduck documentation
// ---------------------------------------------------
//
// Interface Implementation

PyIQueryAssociations::PyIQueryAssociations(IUnknown *pdisp) : PyIUnknown(pdisp) { ob_type = &type; }

PyIQueryAssociations::~PyIQueryAssociations() {}

/* static */ IQueryAssociations *PyIQueryAssociations::GetI(PyObject *self)
{
    return (IQueryAssociations *)PyIUnknown::GetI(self);
}

// @pymethod |PyIQueryAssociations|Init|Initializes the IQueryAssociations interface and sets the root key to the
// appropriate ProgID.
PyObject *PyIQueryAssociations::Init(PyObject *self, PyObject *args)
{
    IQueryAssociations *pIQA = GetI(self);
    if (pIQA == NULL)
        return NULL;
    // @pyparm int|flags||One of shellcon.ASSOCF_* flags
    // @pyparm string|assoc||The string data (ie, extension, prog-id, etc)
    // @pyparm <o PyHKEY>|hkeyProgId|None|Root registry key, can be None
    // @pyparm <o PyHANDLE>|hwnd|None|Reserved, must be 0 or None
    int flags;
    HWND hwnd;
    HKEY hkProgid;
    PyObject *obAssoc, *obhwnd = Py_None, *obhkProgid = Py_None;
    WCHAR *pszAssoc = NULL;
    if (!PyArg_ParseTuple(args, "lO|OO:Init", &flags, &obAssoc, &obhkProgid, &obhwnd))
        return NULL;
    if (!PyWinObject_AsWCHAR(obAssoc, &pszAssoc, TRUE))
        return NULL;
    if (!PyWinObject_AsHKEY(obhkProgid, &hkProgid))
        return NULL;
    if (!PyWinObject_AsHANDLE(obhwnd, (HANDLE *)&hwnd))
        return NULL;
    HRESULT hr;
    PY_INTERFACE_PRECALL;
    hr = pIQA->Init(flags, pszAssoc, hkProgid, hwnd);
    PY_INTERFACE_POSTCALL;
    PyWinObject_FreeWCHAR(pszAssoc);

    if (FAILED(hr))
        return PyCom_BuildPyException(hr, pIQA, IID_IQueryAssociations);
    Py_INCREF(Py_None);
    return Py_None;
}

// XXX - GetData not implemented - memory management unclear - XXX

// @pymethod int|PyIQueryAssociations|GetKey|Searches for and retrieves a file association-related key from the
// registry.
PyObject *PyIQueryAssociations::GetKey(PyObject *self, PyObject *args)
{
    IQueryAssociations *pIQA = GetI(self);
    if (pIQA == NULL)
        return NULL;
    // @pyparm int|flags||Used to control the search.
    // @pyparm int|assocKey||Specifies the type of key that is to be returned.
    // @pyparm string||extra|Optional string with information about the location of the key.
    // It is normally set to a shell verb such as 'open'. Set this parameter to None if it is not used.
    int flags, assoc;
    PyObject *obExtra = Py_None;
    HKEY ret = NULL;
    WCHAR *pszExtra = NULL;
    if (!PyArg_ParseTuple(args, "ii|O:GetKey", &flags, &assoc, &obExtra))
        return NULL;
    if (!PyWinObject_AsWCHAR(obExtra, &pszExtra, TRUE))
        return NULL;
    HRESULT hr;
    PY_INTERFACE_PRECALL;
    hr = pIQA->GetKey(flags, (ASSOCKEY)assoc, pszExtra, &ret);
    PY_INTERFACE_POSTCALL;
    PyWinObject_FreeWCHAR(pszExtra);
    if (FAILED(hr))
        return PyCom_BuildPyException(hr, pIQA, IID_IQueryAssociations);
    // observation of the "open handles" count in task-manager indicates
    // this key needs to be closed!
    return PyWinObject_FromHKEY(ret);
}

// @pymethod int|PyIQueryAssociations|GetString|Searches for and retrieves a file association-related string from the
// registry.
PyObject *PyIQueryAssociations::GetString(PyObject *self, PyObject *args)
{
    IQueryAssociations *pIQA = GetI(self);
    if (pIQA == NULL)
        return NULL;
    // @pyparm int|flags||Used to control the search.
    // @pyparm int|assocStr||Specifies the type of string that is to be returned.
    // @pyparm string||extra|Optional string with information about the location of the key.
    // It is normally set to a shell verb such as 'open'. Set this parameter to None if it is not used.
    int flags, assoc;
    PyObject *obExtra = Py_None;
    HKEY *ret = NULL;
    WCHAR *pszExtra = NULL;
    if (!PyArg_ParseTuple(args, "ll|O:GetString", &flags, &assoc, &obExtra))
        return NULL;
    // @comm Note that ASSOCF_NOTRUNCATE semantics are currently not supported -
    // the buffer passed is 2048 bytes long, and will be truncated by the
    // shell if too small.
    WCHAR result_buf[2048];
    DWORD result_size = sizeof(result_buf) / sizeof(result_buf[0]);
    if (flags & ASSOCF_NOTRUNCATE)
        return PyErr_Format(PyExc_ValueError, "Can not set ASSOCF_NOTRUNCATE - these semantics are not supported");
    if (!PyWinObject_AsWCHAR(obExtra, &pszExtra, TRUE))
        return NULL;

    HRESULT hr;
    PY_INTERFACE_PRECALL;
    hr = pIQA->GetString(flags, (ASSOCSTR)assoc, pszExtra, result_buf, &result_size);
    PY_INTERFACE_POSTCALL;
    PyWinObject_FreeWCHAR(pszExtra);
    if (FAILED(hr))
        return PyCom_BuildPyException(hr, pIQA, IID_IQueryAssociations);
    // docs don't explicitly say if result_size includes NULL.  It says:
    // "will be set to the number of characters actually placed in the buffer"
    return PyWinObject_FromWCHAR(result_buf, result_size - 1);
}

// @object PyIQueryAssociations|Description of the interface
static struct PyMethodDef PyIQueryAssociations_methods[] = {
    {"Init", PyIQueryAssociations::Init,
     1},  // @pymeth Init|Initializes the IQueryAssociations interface and sets the root key to the appropriate ProgID.
    {"GetKey", PyIQueryAssociations::GetKey,
     1},  // @pymeth GetKey|Searches for and retrieves a file association-related key from the registry.
    {"GetString", PyIQueryAssociations::GetString,
     1},  // @pymeth GetString|Searches for and retrieves a file association-related string from the registry.
    {NULL}};

PyComTypeObject PyIQueryAssociations::type("PyIQueryAssociations", &PyIUnknown::type, sizeof(PyIQueryAssociations),
                                           PyIQueryAssociations_methods, GET_PYCOM_CTOR(PyIQueryAssociations));
