// This file declares the ICustomDestinationList Interface for Python.
// Generated by makegw.py
// ---------------------------------------------------
//
// Interface Declaration

class PyICustomDestinationList : public PyIUnknown {
   public:
    MAKE_PYCOM_CTOR(PyICustomDestinationList);
    static ICustomDestinationList *GetI(PyObject *self);
    static PyComTypeObject type;

    // The Python methods
    static PyObject *SetAppID(PyObject *self, PyObject *args);
    static PyObject *BeginList(PyObject *self, PyObject *args);
    static PyObject *AppendCategory(PyObject *self, PyObject *args);
    static PyObject *AppendKnownCategory(PyObject *self, PyObject *args);
    static PyObject *AddUserTasks(PyObject *self, PyObject *args);
    static PyObject *CommitList(PyObject *self, PyObject *args);
    static PyObject *GetRemovedDestinations(PyObject *self, PyObject *args);
    static PyObject *DeleteList(PyObject *self, PyObject *args);
    static PyObject *AbortList(PyObject *self, PyObject *args);

   protected:
    PyICustomDestinationList(IUnknown *pdisp);
    ~PyICustomDestinationList();
};
