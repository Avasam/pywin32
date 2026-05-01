// PyMAPIUtil.h

// Must include before MAPIX.h,
// because of casing that header will cause imports of mingw shared headers instead
// Which actually has some differences in param types, causing build failures
#include <MAPIDefS.h>
#include <MAPICode.h>

// HACK/TODO: This is a big copy from com/win32comext/mapi/src/mapiguids.cpp
// Why can't we use that file or deduplicate instead?

// PythonCOM.h includes <initguid.h> which sets INITGUID before PyMAPIUtil.h is
// processed. MAPIGuid.h only declares an IID when (!INITGUID || USES_IID_<name>),
// and its MAPIGUID_H guard fires under INITGUID, blocking later re-inclusion via
// mapiguids.cpp. Define all USES_IID_* here so every IID is declared on first pass.
#define USES_IID_IMAPISession
#define USES_IID_IMAPIStatus
#define USES_IID_IMAPITable
#define USES_IID_IMAPIProp
#define USES_IID_IMAPIFolder
#define USES_IID_IMessage
#define USES_IID_IMsgStore
#define USES_IID_IMAPIContainer
#define USES_IID_IMAPIProgress
#define USES_IID_IAttachment
#define USES_IID_IProfAdmin
#define USES_IID_IMAPIAdviseSink
#define USES_IID_IAddrBook
#define USES_IID_IMAPIPropData
#define USES_IID_IMailUser
#define USES_IID_IDistList
#define USES_IID_IABContainer
#define USES_IID_IProfSect
#define USES_IID_IMsgServiceAdmin
#define USES_IID_IProviderAdmin
#define USES_PS_PUBLIC_STRINGS
#define USES_PS_MAPI
#define USES_PS_ROUTING_EMAIL_ADDRESSES
#define USES_PS_ROUTING_ADDRTYPE
#define USES_PS_ROUTING_DISPLAY_NAME
#define USES_PS_ROUTING_ENTRYID
#define USES_PS_ROUTING_SEARCH_KEY
#include <MAPIGuid.h>

#define USES_IID_IMsgServiceAdmin2
#define USES_IID_IMessageRaw
#include <MAPIAux.h>
#include <MAPITags.h>

#include <MAPIX.h>

// We should not be using this!
#define OleSetOleError PyCom_BuildPyException

PyObject *PyMAPIObject_FromTypedUnknown(ULONG typ, IUnknown *pUnk, BOOL bAddRef);

PyObject *PyObject_FromMAPIERROR(MAPIERROR *e, BOOL bIsUnicode, BOOL free_buffer);

/* Create (and free) a SBinaryArray from a PyObject */
BOOL PyMAPIObject_AsSBinaryArray(PyObject *ob, SBinaryArray *pv);
void PyMAPIObject_FreeSBinaryArray(SBinaryArray *pv);

/* Create (and free) a SPropValue from a PyObject */
BOOL PyMAPIObject_AsSPropValue(PyObject *ob, SPropValue *pv, void *pAllocMoreLinkBlock);
PyObject *PyMAPIObject_FromSPropValue(SPropValue *pv);

/* Create a PyObject to/from a SPropValue Array*/
BOOL PyMAPIObject_AsSPropValueArray(PyObject *ob, SPropValue **ppv, ULONG *pcValues);
PyObject *PyMAPIObject_FromSPropValueArray(SPropValue *pv, ULONG nvalues);

/* Create a PyObject from a SRow/SRowSet */
PyObject *PyMAPIObject_FromSRow(SRow *pr);
PyObject *PyMAPIObject_FromSRowSet(SRowSet *prs);

/* Create (and free) a SRowSet from a PyObject */
BOOL PyMAPIObject_AsSRowSet(PyObject *obSeq, SRowSet **ppResult, BOOL bNoneOK);
void PyMAPIObject_FreeSRowSet(SRowSet *pResult);

/* ADRLIST structures are really just SRowSet */
#define PyMAPIObject_FromADRLIST(prs) PyMAPIObject_FromSRowSet((SRowSet *)(prs))

#define PyMAPIObject_AsADRLIST(obSeq, ppResult, bNoneOK) PyMAPIObject_AsSRowSet(obSeq, (SRowSet **)(ppResult), bNoneOK)
#define PyMAPIObject_FreeADRLIST(p) PyMAPIObject_FreeSRowSet((SRowSet *)(p))

/* Create (and free) a SSortOrderSet from a PyObject */
BOOL PyMAPIObject_AsSSortOrderSet(PyObject *obsos, SSortOrderSet **ppsos, BOOL bNoneOK = TRUE);
void PyMAPIObject_FreeSSortOrderSet(SSortOrderSet *ppsos);

/* Create (and free) a SRestriction from a PyObject */
BOOL PyMAPIObject_AsSRestriction(PyObject *ob, SRestriction **pRest, BOOL bNoneOK = TRUE);
void PyMAPIObject_FreeSRestriction(SRestriction *pr);

/* Create (and free) a SPropTagArray from a PyObject */
BOOL PyMAPIObject_AsSPropTagArray(PyObject *obsos, SPropTagArray **ppta);
void PyMAPIObject_FreeSPropTagArray(SPropTagArray *pta);

/* Create a PyObject from a SPropTagArray */
PyObject *PyMAPIObject_FromSPropTagArray(SPropTagArray *pta);

/* Create (and free) a MAPINAMEID array from a PyObject */
BOOL PyMAPIObject_AsMAPINAMEIDArray(PyObject *ob, MAPINAMEID ***pppNameId, ULONG *pNumIds, BOOL bNoneOK = FALSE);
void PyMAPIObject_FreeMAPINAMEIDArray(MAPINAMEID **pv);

/* Create a PyObject from a MAPINAMEID Array */
PyObject *PyMAPIObject_FromMAPINAMEIDArray(MAPINAMEID **ppNameId, ULONG numIds);

/* Create a PyObject from a SPropProblemArray */
PyObject *PyMAPIObject_FromSPropProblemArray(SPropProblemArray *ppa);

PyObject *PyWinObject_FromMAPIStr(LPTSTR str, BOOL isUnicode);
BOOL PyWinObject_AsMAPIStr(PyObject *stringObject, LPTSTR *pResult, BOOL asUnicode, BOOL bNoneOK = FALSE,
                           DWORD *pResultLen = NULL);
void PyWinObject_FreeMAPIStr(LPTSTR pResult, BOOL wasUnicode);
