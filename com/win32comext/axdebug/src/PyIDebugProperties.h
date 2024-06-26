// This file declares the IDebugProperty Interface and Gateway for Python.
// Generated by makegw.py
// ---------------------------------------------------
//
// Interface Declaration

class PyIDebugProperty : public PyIUnknown {
   public:
    MAKE_PYCOM_CTOR(PyIDebugProperty);
    static IDebugProperty *GetI(PyObject *self);
    static PyComTypeObject type;

    // The Python methods
    static PyObject *GetPropertyInfo(PyObject *self, PyObject *args);
    static PyObject *GetExtendedInfo(PyObject *self, PyObject *args);
    static PyObject *SetValueAsString(PyObject *self, PyObject *args);
    static PyObject *EnumMembers(PyObject *self, PyObject *args);
    static PyObject *GetParent(PyObject *self, PyObject *args);

   protected:
    PyIDebugProperty(IUnknown *pdisp);
    ~PyIDebugProperty();
};
// ---------------------------------------------------
//
// Gateway Declaration

class PyGDebugProperty : public PyGatewayBase, public IDebugProperty {
   protected:
    PyGDebugProperty(PyObject *instance) : PyGatewayBase(instance) { ; }
    PYGATEWAY_MAKE_SUPPORT(PyGDebugProperty, IDebugProperty, IID_IDebugProperty)

    // IDebugProperty
    STDMETHOD(GetPropertyInfo)(DWORD dwFieldSpec, UINT nRadix, DebugPropertyInfo __RPC_FAR *pPropertyInfo);

    STDMETHOD(GetExtendedInfo)(ULONG cInfos, GUID __RPC_FAR *rgguidExtendedInfo, VARIANT __RPC_FAR *rgvar);

    STDMETHOD(SetValueAsString)(LPCOLESTR pszValue, UINT nRadix);

    STDMETHOD(EnumMembers)
    (DWORD dwFieldSpec, UINT nRadix, REFIID refiid, IEnumDebugPropertyInfo __RPC_FAR *__RPC_FAR *ppepi);

    STDMETHOD(GetParent)(IDebugProperty __RPC_FAR *__RPC_FAR *ppDebugProp);
};
