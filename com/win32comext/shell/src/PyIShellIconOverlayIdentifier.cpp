// This file implements the IShellIconOverlayIdentifier Interface and Gateway for Python.
// Generated by makegw.py

#include "shell_pch.h"
#include "PyIShellIconOverlayIdentifier.h"

// @doc - This file contains autoduck documentation
// ---------------------------------------------------
//
// Interface Implementation

PyIShellIconOverlayIdentifier::PyIShellIconOverlayIdentifier(IUnknown *pdisp) : PyIUnknown(pdisp) { ob_type = &type; }

PyIShellIconOverlayIdentifier::~PyIShellIconOverlayIdentifier() {}

/* static */ IShellIconOverlayIdentifier *PyIShellIconOverlayIdentifier::GetI(PyObject *self)
{
    return (IShellIconOverlayIdentifier *)PyIUnknown::GetI(self);
}

// @pymethod int|PyIShellIconOverlayIdentifier|IsMemberOf|Determines if a shell object should have an icon overlay
// @rdesc The gateway implementation of this function should return winerror.S_OK to
// display the overlay, S_FALSE if not, or throw a COM exception with E_FAIL on error.
// <nl>The client implementation of this function returns the same values - ie,
// Python's True and False should not be used, as S_OK==0==False.
PyObject *PyIShellIconOverlayIdentifier::IsMemberOf(PyObject *self, PyObject *args)
{
    IShellIconOverlayIdentifier *pISIOI = GetI(self);
    if (pISIOI == NULL)
        return NULL;
    // @pyparm <o PyUnicode>|path||Fully qualified path of the shell object
    // @pyparm int|attrib||Shell attributes, combination of shellcon.SFGAO_* flags
    PyObject *obpath;
    LPWSTR path;
    DWORD attrib;
    if (!PyArg_ParseTuple(args, "Ol:IsMemberOf", &obpath, &attrib))
        return NULL;
    BOOL bPythonIsHappy = TRUE;
    if (bPythonIsHappy && !PyWinObject_AsWCHAR(obpath, &path))
        bPythonIsHappy = FALSE;
    if (!bPythonIsHappy)
        return NULL;
    HRESULT hr;
    PY_INTERFACE_PRECALL;
    hr = pISIOI->IsMemberOf(path, attrib);

    PY_INTERFACE_POSTCALL;
    PyWinObject_FreeWCHAR(path);

    if (FAILED(hr))
        return PyCom_BuildPyException(hr, pISIOI, IID_IShellIconOverlayIdentifier);
    return PyLong_FromLong(hr);
}

// @pymethod (<o PyUnicode>, int, int)|PyIShellIconOverlayIdentifier|GetOverlayInfo|Retrieves the path to the overlay
// icon
// @rdesc Returns the path to the icon file, the index of icon within the file, and Flags containing
//	combination of shellcon.ISIOI_ICON* flags
PyObject *PyIShellIconOverlayIdentifier::GetOverlayInfo(PyObject *self, PyObject *args)
{
    IShellIconOverlayIdentifier *pISIOI = GetI(self);
    if (pISIOI == NULL)
        return NULL;
    WCHAR szIconFile[_MAX_PATH + 1];
    int pIndex;
    DWORD pFlags;
    if (!PyArg_ParseTuple(args, ":GetOverlayInfo"))
        return NULL;
    HRESULT hr;
    PY_INTERFACE_PRECALL;
    hr = pISIOI->GetOverlayInfo(szIconFile, sizeof(szIconFile) / sizeof(szIconFile[0]), &pIndex, &pFlags);
    PY_INTERFACE_POSTCALL;
    if (FAILED(hr))
        return PyCom_BuildPyException(hr, pISIOI, IID_IShellIconOverlayIdentifier);
    PyObject *obiconFile;

    obiconFile = PyWinObject_FromWCHAR(szIconFile);
    PyObject *pyretval = Py_BuildValue("Nii", obiconFile, pIndex, pFlags);
    return pyretval;
}

// @pymethod int|PyIShellIconOverlayIdentifier|GetPriority|Retrieves the relative priority of the overlay
// @rdesc Implementation of this function should return a number in the range 0-100 (0 is highest priority)
PyObject *PyIShellIconOverlayIdentifier::GetPriority(PyObject *self, PyObject *args)
{
    IShellIconOverlayIdentifier *pISIOI = GetI(self);
    if (pISIOI == NULL)
        return NULL;
    int pri;
    if (!PyArg_ParseTuple(args, ":GetPriority"))
        return NULL;
    HRESULT hr;
    PY_INTERFACE_PRECALL;
    hr = pISIOI->GetPriority(&pri);
    PY_INTERFACE_POSTCALL;

    if (FAILED(hr))
        return PyCom_BuildPyException(hr, pISIOI, IID_IShellIconOverlayIdentifier);

    PyObject *pyretval = Py_BuildValue("i", pri);
    return pyretval;
}

// @object PyIShellIconOverlayIdentifier|Interface that supplies icon overlay information to the shell
static struct PyMethodDef PyIShellIconOverlayIdentifier_methods[] = {
    {"IsMemberOf", PyIShellIconOverlayIdentifier::IsMemberOf,
     1},  // @pymeth IsMemberOf|Determines if a shell object should have an icon overlay
    {"GetOverlayInfo", PyIShellIconOverlayIdentifier::GetOverlayInfo,
     1},  // @pymeth GetOverlayInfo|Retrieves the path to the overlay icon
    {"GetPriority", PyIShellIconOverlayIdentifier::GetPriority,
     1},  // @pymeth GetPriority|Retrieves the relative priority of the overlay
    {NULL}};

PyComTypeObject PyIShellIconOverlayIdentifier::type("PyIShellIconOverlayIdentifier", &PyIUnknown::type,
                                                    sizeof(PyIShellIconOverlayIdentifier),
                                                    PyIShellIconOverlayIdentifier_methods,
                                                    GET_PYCOM_CTOR(PyIShellIconOverlayIdentifier));
// ---------------------------------------------------
//
// Gateway Implementation
STDMETHODIMP PyGShellIconOverlayIdentifier::IsMemberOf(
    /* [unique][in] */ LPCWSTR path,
    /* [unique][in] */ DWORD attrib)
{
    PY_GATEWAY_METHOD;
    PyObject *obpath;
    obpath = PyWinObject_FromWCHAR(path);
    PyObject *ret;
    HRESULT hr = InvokeViaPolicy("IsMemberOf", &ret, "Ol", obpath, attrib);
    if (FAILED(hr))
        return hr;
    if (PyLong_Check(ret))
        hr = PyLong_AsLong(ret);
    Py_XDECREF(ret);
    return hr;
}

STDMETHODIMP PyGShellIconOverlayIdentifier::GetOverlayInfo(LPWSTR iconFile, int maxChars, int __RPC_FAR *pIndex,
                                                           DWORD __RPC_FAR *pFlags)
{
    PY_GATEWAY_METHOD;
    PyObject *result;
    HRESULT hr = InvokeViaPolicy("GetOverlayInfo", &result);
    if (FAILED(hr))
        return hr;
    // Process the Python results, and convert back to the real params
    PyObject *obiconFile;
    if (!PyArg_ParseTuple(result, "Oii", &obiconFile, pIndex, pFlags))
        return PyCom_SetAndLogCOMErrorFromPyException("GetOverlayInfo", GetIID());
    BOOL bPythonIsHappy = TRUE;
    if (bPythonIsHappy) {
        WCHAR *retIconFile;
        if (PyWinObject_AsWCHAR(obiconFile, &retIconFile)) {
            wcsncpy(iconFile, retIconFile, maxChars);
            PyWinObject_FreeWCHAR(retIconFile);
        }
        else
            bPythonIsHappy = FALSE;
    }
    if (!bPythonIsHappy)
        hr = PyCom_SetAndLogCOMErrorFromPyException("GetOverlayInfo", GetIID());
    Py_DECREF(result);
    return hr;
}

STDMETHODIMP PyGShellIconOverlayIdentifier::GetPriority(
    /* [unique][out] */ int __RPC_FAR *pri)
{
    PY_GATEWAY_METHOD;
    PyObject *result;
    HRESULT hr = InvokeViaPolicy("GetPriority", &result);
    if (FAILED(hr))
        return hr;
    // Process the Python results, and convert back to the real params
    if (!PyArg_Parse(result, "i", pri))
        return PyCom_SetAndLogCOMErrorFromPyException("GetPriority", GetIID());
    Py_DECREF(result);
    return hr;
}
