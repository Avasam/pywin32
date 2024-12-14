// This file implements the IFilter Interface for Python.
// Generated by makegw.py

#include "stdafx.h"
#include "PyIFilter.h"
#include "PythonCOMRegister.h"  // For simpler registration of IIDs etc.

// We should not be using this!
#define OleSetOleError PyCom_BuildPyException

// @doc - This file contains autoduck documentation
// ---------------------------------------------------
//
// Interface Implementation

PyIFilter::PyIFilter(IUnknown *pdisp) : PyIUnknown(pdisp) { ob_type = &type; }

PyIFilter::~PyIFilter() {}

/* static */ IFilter *PyIFilter::GetI(PyObject *self) { return (IFilter *)PyIUnknown::GetI(self); }

// @pymethod |PyIFilter|Init|Init an ifilter

//
// TODO: I don't support passing in a FULLPROPSEC array yet
//
PyObject *PyIFilter::Init(PyObject *self, PyObject *args)
{
    IFilter *pIF = GetI(self);
    if (pIF == NULL)
        return NULL;

    const FULLPROPSPEC *aAttributes = NULL;
    ULONG cAttributes = 0;

    ULONG grfFlags = 0;
    ULONG flags = 0;
    if (!PyArg_ParseTuple(args, "l:Init", &grfFlags))
        return NULL;

    HRESULT hr;
    PY_INTERFACE_PRECALL;
    hr = pIF->Init(grfFlags, cAttributes, aAttributes, &flags);
    PY_INTERFACE_POSTCALL;

    if (FAILED(hr))
        return PyCom_BuildPyException(hr, pIF, IID_IFilter);

    return Py_BuildValue("l", flags);
}

// @pymethod |PyIFilter|GetChunk|Description of GetChunk.
PyObject *PyIFilter::GetChunk(PyObject *self, PyObject *args)
{
    IFilter *pIF = GetI(self);
    if (pIF == NULL)
        return NULL;
    if (!PyArg_ParseTuple(args, ":GetChunk"))
        return NULL;

    HRESULT hr;
    STAT_CHUNK stat;
    PY_INTERFACE_PRECALL;
    hr = pIF->GetChunk(&stat);
    PY_INTERFACE_POSTCALL;

    if (FAILED(hr))
        return PyCom_BuildPyException(hr, pIF, IID_IFilter);

    PyObject *obProp;
    if (stat.attribute.psProperty.ulKind == PRSPEC_LPWSTR) {
        obProp = PyWinObject_FromWCHAR(stat.attribute.psProperty.lpwstr);
    }
    else {
        obProp = Py_BuildValue("i", stat.attribute.psProperty.propid);
    }

    PyObject *obAttr = Py_BuildValue("NN", PyWinObject_FromIID(stat.attribute.guidPropSet), obProp);

    return Py_BuildValue("iiiiNiii", stat.idChunk, stat.breakType, stat.flags, stat.locale, obAttr, stat.idChunkSource,
                         stat.cwcStartSource, stat.cwcLenSource);
}

// @pymethod |PyIFilter|GetText|Description of GetText.
PyObject *PyIFilter::GetText(PyObject *self, PyObject *args)
{
    IFilter *pIF = GetI(self);
    if (pIF == NULL)
        return NULL;

    // @pyparm <int>|nBufSize|size of text buffer to create
    ULONG nBufSize = 0;
    if (!PyArg_ParseTuple(args, "|i:GetText", &nBufSize))
        return NULL;

    HRESULT hr;
    if (nBufSize == 0)
        nBufSize = 8192;  // 8k default

    WCHAR *wBuffer = (WCHAR *)PyMem_Malloc((nBufSize + 1) * sizeof(WCHAR));
    if (!wBuffer) {
        PyErr_SetString(PyExc_MemoryError, "getting text");
        return NULL;
    }

    PY_INTERFACE_PRECALL;
    hr = pIF->GetText(&nBufSize, wBuffer);
    PY_INTERFACE_POSTCALL;

    if (FAILED(hr)) {
        PyMem_Free(wBuffer);
        return PyCom_BuildPyException(hr, pIF, IID_IFilter);
    }

    PyObject *obRet = PyWinObject_FromWCHAR(wBuffer, nBufSize);
    PyMem_Free(wBuffer);
    return obRet;
}

// @pymethod |PyIFilter|GetValue|Description of GetValue.
PyObject *PyIFilter::GetValue(PyObject *self, PyObject *args)
{
    IFilter *pIF = GetI(self);
    if (pIF == NULL)
        return NULL;

    if (!PyArg_ParseTuple(args, ":GetValue"))
        return NULL;

    HRESULT hr;
    PROPVARIANT *pPropValue = 0;
    PY_INTERFACE_PRECALL;
    hr = pIF->GetValue(&pPropValue);
    PY_INTERFACE_POSTCALL;

    if (FAILED(hr)) {
        return PyCom_BuildPyException(hr, pIF, IID_IFilter);
    }

    if (pPropValue) {
        PyObject *obRet = PyObject_FromPROPVARIANT(pPropValue);
        PropVariantClear(pPropValue);
        CoTaskMemFree(pPropValue);
        return obRet;
    }

    Py_INCREF(Py_None);
    return Py_None;
}

static PyObject *pyLoadIFilter(PyObject *self, PyObject *args)
{
    HRESULT hr;
    IUnknown *pOb = NULL;
    PyObject *obPath;

    PyObject *ret;
    long lres = 0;
    if (!PyArg_ParseTuple(args, "O:LoadIFilter", &obPath))
        return NULL;

    WCHAR *path;
    if (!PyWinObject_AsWCHAR(obPath, &path, FALSE))
        goto done;

    Py_BEGIN_ALLOW_THREADS;
    hr = LoadIFilter(path, NULL, (void **)&pOb);
    Py_END_ALLOW_THREADS;
    if (FAILED(hr))
        ret = OleSetOleError(hr);

    else
        ret = PyCom_PyObjectFromIUnknown(pOb, IID_IFilter, FALSE);
done:
    PyWinObject_FreeWCHAR(path);
    return ret;
}

static PyObject *pyBindIFilterFromStorage(PyObject *self, PyObject *args)
{
    HRESULT hr;
    IUnknown *pOb = NULL;
    PyObject *obStg;

    PyObject *ret;
    long lres = 0;
    if (!PyArg_ParseTuple(args, "O:BindIFilterFromStorage", &obStg))
        return NULL;

    IStorage *pstgDest;
    BOOL bPythonIsHappy = TRUE;
    if (!PyCom_InterfaceFromPyObject(obStg, IID_IStorage, (void **)&pstgDest, FALSE /* bNoneOK */))
        bPythonIsHappy = FALSE;

    if (!bPythonIsHappy)
        return NULL;

    Py_BEGIN_ALLOW_THREADS;
    hr = BindIFilterFromStorage(pstgDest, NULL, (void **)&pOb);
    pstgDest->Release();
    Py_END_ALLOW_THREADS;
    if (FAILED(hr))
        ret = OleSetOleError(hr);

    else
        ret = PyCom_PyObjectFromIUnknown(pOb, IID_IFilter, FALSE);

    return ret;
}

static PyObject *pyBindIFilterFromStream(PyObject *self, PyObject *args)
{
    HRESULT hr;
    IUnknown *pOb = NULL;
    PyObject *obStg;

    PyObject *ret;
    long lres = 0;
    if (!PyArg_ParseTuple(args, "O:BindIFilterFromStream", &obStg))
        return NULL;

    IStream *pstm;
    BOOL bPythonIsHappy = TRUE;
    if (!PyCom_InterfaceFromPyObject(obStg, IID_IStream, (void **)&pstm, FALSE /* bNoneOK */))
        bPythonIsHappy = FALSE;

    if (!bPythonIsHappy)
        return NULL;

    Py_BEGIN_ALLOW_THREADS;
    hr = BindIFilterFromStream(pstm, NULL, (void **)&pOb);
    pstm->Release();
    Py_END_ALLOW_THREADS;
    if (FAILED(hr))
        ret = OleSetOleError(hr);
    else
        ret = PyCom_PyObjectFromIUnknown(pOb, IID_IFilter, FALSE);
    return ret;
}

static int AddConstant(PyObject *dict, const char *key, long value)
{
    PyObject *oval = PyLong_FromLong(value);
    if (!oval) {
        return 1;
    }
    int rc = PyDict_SetItemString(dict, (char *)key, oval);
    Py_DECREF(oval);
    return rc;
}
static int AddIID(PyObject *dict, const char *key, REFGUID guid)
{
    PyObject *obiid = PyWinObject_FromIID(guid);
    if (!obiid)
        return 1;
    int rc = PyDict_SetItemString(dict, (char *)key, obiid);
    Py_DECREF(obiid);
    return rc;
}

#define ADD_CONSTANT(tok)                  \
    if (0 != AddConstant(dict, #tok, tok)) \
        PYWIN_MODULE_INIT_RETURN_ERROR;
#define ADD_IID(tok)                  \
    if (0 != AddIID(dict, #tok, tok)) \
        PYWIN_MODULE_INIT_RETURN_ERROR;

// @object PyIFilter|Wraps the interfaces used with Indexing Service filtering
static struct PyMethodDef PyIFilter_methods[] = {
    {"Init", PyIFilter::Init, 1},          // @pymeth Init|Description of Init
    {"GetChunk", PyIFilter::GetChunk, 1},  // @pymeth GetChunk|Description of GetChunk
    {"GetText", PyIFilter::GetText, 1},    // @pymeth GetText|returns text for the last getChunk
    {"GetValue", PyIFilter::GetValue, 1},  // @pymeth GetValue|returns next property as defined by get check
    {NULL}};

PyComTypeObject PyIFilter::type("PyIFilter", &PyIUnknown::type, sizeof(PyIFilter), PyIFilter_methods,
                                GET_PYCOM_CTOR(PyIFilter));

static struct PyMethodDef ifilter_functions[] = {
    {"LoadIFilter", pyLoadIFilter, 1},                        // @pymeth Init|Description of Init
    {"BindIFilterFromStorage", pyBindIFilterFromStorage, 1},  // @pymeth BindIFilterFromStorage|
    {"BindIFilterFromStream", pyBindIFilterFromStream, 1},    // @pymeth BindIFilterFromStream|
    {NULL}};

static const PyCom_InterfaceSupportInfo g_interfaceSupportData[] = {
    PYCOM_INTERFACE_CLIENT_ONLY(Filter),
};

/* Module initialisation */
PYWIN_MODULE_INIT_FUNC(ifilter)
{
    PYWIN_MODULE_INIT_PREPARE(ifilter, ifilter_functions, "Wraps the interfaces used with Indexing Service filtering");

    // Register all of our interfaces, gateways and IIDs.
    PyCom_RegisterExtensionSupport(dict, g_interfaceSupportData,
                                   sizeof(g_interfaceSupportData) / sizeof(PyCom_InterfaceSupportInfo));

    // Tell pywintypes that IFilter error messages can be extracted from
    // query.dll
    HMODULE hmod = GetModuleHandle(_T("query.dll"));
    if (hmod)
        // According to FiltErr.h, "Codes 0x1700-0x172F are reserved for FILTER"
        PyWin_RegisterErrorMessageModule(0x80041700, 0x8004172F, hmod);

    // NOTE: New constants should go in ifiltercon.py
    // IFilter Init functions
    ADD_CONSTANT(IFILTER_INIT_CANON_PARAGRAPHS);
    ADD_CONSTANT(IFILTER_INIT_HARD_LINE_BREAKS);
    ADD_CONSTANT(IFILTER_INIT_CANON_HYPHENS);
    ADD_CONSTANT(IFILTER_INIT_CANON_SPACES);
    ADD_CONSTANT(IFILTER_INIT_APPLY_INDEX_ATTRIBUTES);
    ADD_CONSTANT(IFILTER_INIT_APPLY_OTHER_ATTRIBUTES);
    ADD_CONSTANT(IFILTER_INIT_INDEXING_ONLY);
    ADD_CONSTANT(IFILTER_INIT_SEARCH_LINKS);

    // IFilter return code
    ADD_CONSTANT(IFILTER_FLAGS_OLE_PROPERTIES);

    // Get Chunk Error codes
    ADD_CONSTANT(FILTER_E_END_OF_CHUNKS);
    ADD_CONSTANT(FILTER_E_EMBEDDING_UNAVAILABLE);
    ADD_CONSTANT(FILTER_E_LINK_UNAVAILABLE);
    ADD_CONSTANT(FILTER_E_PASSWORD);
    ADD_CONSTANT(FILTER_E_ACCESS);

    // Chunk Break (ret item index 1)
    ADD_CONSTANT(CHUNK_NO_BREAK);
    ADD_CONSTANT(CHUNK_EOW);
    ADD_CONSTANT(CHUNK_EOS);
    ADD_CONSTANT(CHUNK_EOP);
    ADD_CONSTANT(CHUNK_EOC);

    // Chunk Flas (ret item index 2)
    ADD_CONSTANT(CHUNK_TEXT);
    ADD_CONSTANT(CHUNK_VALUE);

    // Get Value error codes
    ADD_CONSTANT(FILTER_E_NO_MORE_VALUES);
    ADD_CONSTANT(FILTER_E_NO_VALUES);

    // Get Text error codes
    ADD_CONSTANT(FILTER_E_NO_TEXT);
    ADD_CONSTANT(FILTER_E_NO_MORE_TEXT);
    ADD_CONSTANT(FILTER_S_LAST_TEXT);
    // NOTE: New constants should go in ifiltercon.py

    PYWIN_MODULE_INIT_RETURN_SUCCESS;
}
