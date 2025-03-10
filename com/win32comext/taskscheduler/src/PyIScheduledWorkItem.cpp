// This file implements the IScheduledWorkItem Interface for Python.
// Generated by makegw.py

#include "PyIScheduledWorkItem.h"

// @doc - This file contains autoduck documentation
// ---------------------------------------------------
//
// Interface Implementation

PyIScheduledWorkItem::PyIScheduledWorkItem(IUnknown *pdisp) : PyIUnknown(pdisp) { ob_type = &type; }

PyIScheduledWorkItem::~PyIScheduledWorkItem() {}

/* static */ IScheduledWorkItem *PyIScheduledWorkItem::GetI(PyObject *self)
{
    return (IScheduledWorkItem *)PyIUnknown::GetI(self);
}

// @pymethod int,PyITaskTrigger|PyIScheduledWorkItem|CreateTrigger|Creates a new trigger for a task, returns index and
// new ITaskTrigger interface
PyObject *PyIScheduledWorkItem::CreateTrigger(PyObject *self, PyObject *args)
{
    IScheduledWorkItem *pISWI = GetI(self);
    if (pISWI == NULL)
        return NULL;
    ITaskTrigger *pITT;

    WORD trig_ind = 0;
    if (!PyArg_ParseTuple(args, ":PyIScheduledWorkItem::CreateTrigger"))
        return NULL;

    HRESULT hr;
    PY_INTERFACE_PRECALL;
    hr = pISWI->CreateTrigger(&trig_ind, &pITT);
    PY_INTERFACE_POSTCALL;

    if (FAILED(hr))
        return PyCom_BuildPyException(hr, pISWI, IID_IScheduledWorkItem);
    return Py_BuildValue("lN", trig_ind, PyCom_PyObjectFromIUnknown(pITT, IID_ITaskTrigger, FALSE));
}

// @pymethod |PyIScheduledWorkItem|DeleteTrigger|Deletes specified trigger
PyObject *PyIScheduledWorkItem::DeleteTrigger(PyObject *self, PyObject *args)
{
    IScheduledWorkItem *pISWI = GetI(self);
    if (pISWI == NULL)
        return NULL;
    INT iiTrigger;
    WORD iTrigger;
    if (!PyArg_ParseTuple(args, "i:PyIScheduledWorkItem::DeleteTrigger", &iiTrigger))
        return NULL;
    //@pyparm int|Trigger||Index of trigger to delete
    iTrigger = iiTrigger;
    HRESULT hr;
    PY_INTERFACE_PRECALL;
    hr = pISWI->DeleteTrigger(iTrigger);
    PY_INTERFACE_POSTCALL;

    if (FAILED(hr))
        return PyCom_BuildPyException(hr, pISWI, IID_IScheduledWorkItem);
    Py_INCREF(Py_None);
    return Py_None;
}

// @pymethod int|PyIScheduledWorkItem|GetTriggerCount|Returns number of triggers defined for the task
PyObject *PyIScheduledWorkItem::GetTriggerCount(PyObject *self, PyObject *args)
{
    IScheduledWorkItem *pISWI = GetI(self);
    if (pISWI == NULL)
        return NULL;
    WORD wCount = 0;
    if (!PyArg_ParseTuple(args, ":PyIScheduledWorkItem::GetTriggerCount"))
        return NULL;
    HRESULT hr;
    PY_INTERFACE_PRECALL;
    hr = pISWI->GetTriggerCount(&wCount);
    PY_INTERFACE_POSTCALL;

    if (FAILED(hr))
        return PyCom_BuildPyException(hr, pISWI, IID_IScheduledWorkItem);
    else
        return Py_BuildValue("i", wCount);
}

// @pymethod <o PyITaskTrigger>|PyIScheduledWorkItem|GetTrigger|Retrieves ITaskTrigger interface for specified trigger
// index
PyObject *PyIScheduledWorkItem::GetTrigger(PyObject *self, PyObject *args)
{
    IScheduledWorkItem *pISWI = GetI(self);
    if (pISWI == NULL)
        return NULL;
    // @pyparm int|iTrigger||Index of trigger to retrieve
    INT iiTrigger;
    WORD iTrigger;
    ITaskTrigger *pITT;

    if (!PyArg_ParseTuple(args, "i:PyIScheduledWorkItem::GetTrigger", &iiTrigger))
        return NULL;
    iTrigger = iiTrigger;
    HRESULT hr;
    PY_INTERFACE_PRECALL;
    hr = pISWI->GetTrigger(iTrigger, &pITT);
    PY_INTERFACE_POSTCALL;

    if (FAILED(hr))
        return PyCom_BuildPyException(hr, pISWI, IID_IScheduledWorkItem);
    return PyCom_PyObjectFromIUnknown(pITT, IID_ITaskTrigger, FALSE);
}

// @pymethod <o PyUNICODE>|PyIScheduledWorkItem|GetTriggerString|Creates a human-readable summary of specified trigger
PyObject *PyIScheduledWorkItem::GetTriggerString(PyObject *self, PyObject *args)
{
    IScheduledWorkItem *pISWI = GetI(self);
    if (pISWI == NULL)
        return NULL;
    LPWSTR TriggerString;
    PyObject *ret = NULL;
    INT iiTrigger;
    WORD iTrigger;
    if (!PyArg_ParseTuple(args, "i:PyIScheduledWorkItem::GetTriggerString", &iiTrigger))
        return NULL;
    iTrigger = iiTrigger;
    ;
    HRESULT hr;
    PY_INTERFACE_PRECALL;
    hr = pISWI->GetTriggerString(iTrigger, &TriggerString);
    PY_INTERFACE_POSTCALL;

    if (FAILED(hr))
        PyCom_BuildPyException(hr, pISWI, IID_IScheduledWorkItem);
    else
        ret = PyWinObject_FromWCHAR(TriggerString);
    CoTaskMemFree(TriggerString);
    return ret;
}

// @pymethod (<o PyDateTime>,,,)|PyIScheduledWorkItem|GetRunTimes|Return specified number of run times within given time
// frame
PyObject *PyIScheduledWorkItem::GetRunTimes(PyObject *self, PyObject *args)
{
    IScheduledWorkItem *pISWI = GetI(self);
    if (pISWI == NULL)
        return NULL;
    // @pyparm int|Count||Number of run times to retrieve
    // @pyparm <o PyDateTime>|Begin||Start time, defaults to current time if not passed or None
    // @pyparm <o PyDateTime>|End||End time, defaults to unlimited if not passed or None
    WORD wCount = 0, time_ind = 0;
    SYSTEMTIME start_time, end_time;
    LPSYSTEMTIME run_time = NULL, first_run_time = NULL, lpend_time = NULL;

    PyObject *ret = NULL, *run_time_obj = NULL;
    PyObject *obstart_time = NULL, *obend_time = NULL;
    if (!PyArg_ParseTuple(args, "h|OO:GetRunTimes", &wCount, &obstart_time, &obend_time))
        return NULL;
    if ((obstart_time == NULL) || (obstart_time == Py_None))
        GetLocalTime(&start_time);
    else if (!PyWinObject_AsSYSTEMTIME(obstart_time, &start_time))
        return NULL;
    if ((obend_time != NULL) && (obend_time != Py_None)) {
        if (!PyWinObject_AsSYSTEMTIME(obend_time, &end_time))
            return NULL;
        lpend_time = &end_time;
    }
    HRESULT hr;
    PY_INTERFACE_PRECALL;
    hr = pISWI->GetRunTimes(&start_time, lpend_time, &wCount, &first_run_time);
    PY_INTERFACE_POSTCALL;

    if (FAILED(hr))
        return PyCom_BuildPyException(hr, pISWI, IID_IScheduledWorkItem);

    ret = PyTuple_New(wCount);
    run_time = first_run_time;
    for (time_ind = 0; time_ind < wCount; time_ind++) {
        run_time_obj = PyWinObject_FromSYSTEMTIME(*run_time);
        PyTuple_SetItem(ret, time_ind, run_time_obj);
        run_time++;
    }
    CoTaskMemFree(first_run_time);
    return ret;
}

// @pymethod <o PyDateTime>|PyIScheduledWorkItem|GetNextRunTime|Returns next time that task is scheduled to run
PyObject *PyIScheduledWorkItem::GetNextRunTime(PyObject *self, PyObject *args)
{
    IScheduledWorkItem *pISWI = GetI(self);
    if (pISWI == NULL)
        return NULL;
    SYSTEMTIME NextRun;

    if (!PyArg_ParseTuple(args, ":PyIScheduledWorkItem::GetNextRunTime"))
        return NULL;
    HRESULT hr;
    PY_INTERFACE_PRECALL;
    hr = pISWI->GetNextRunTime(&NextRun);
    PY_INTERFACE_POSTCALL;

    if (FAILED(hr))
        return PyCom_BuildPyException(hr, pISWI, IID_IScheduledWorkItem);
    return PyWinObject_FromSYSTEMTIME(NextRun);
}

// @pymethod |PyIScheduledWorkItem|SetIdleWait|Sets idle parms for task with trigger of type TASK_EVENT_TRIGGER_ON_IDLE
PyObject *PyIScheduledWorkItem::SetIdleWait(PyObject *self, PyObject *args)
{
    IScheduledWorkItem *pISWI = GetI(self);
    if (pISWI == NULL)
        return NULL;
    // @pyparm int|wIdleMinutes||Nbr of minutes computer must be idle before task fires
    // @pyparm int|wDeadlineMinutes||Maximum nbr of minutes task will wait for computer to become idle
    INT iwIdleMinutes;
    INT iwDeadlineMinutes;
    WORD wIdleMinutes;
    WORD wDeadlineMinutes;
    if (!PyArg_ParseTuple(args, "ii:SetIdleWait", &iwIdleMinutes, &iwDeadlineMinutes))
        return NULL;
    BOOL bPythonIsHappy = TRUE;
    wIdleMinutes = iwIdleMinutes;
    wDeadlineMinutes = iwDeadlineMinutes;
    if (!bPythonIsHappy)
        return NULL;
    HRESULT hr;
    PY_INTERFACE_PRECALL;
    hr = pISWI->SetIdleWait(wIdleMinutes, wDeadlineMinutes);

    PY_INTERFACE_POSTCALL;

    if (FAILED(hr))
        return PyCom_BuildPyException(hr, pISWI, IID_IScheduledWorkItem);
    Py_INCREF(Py_None);
    return Py_None;
}

// @pymethod int,int|PyIScheduledWorkItem|GetIdleWait|Gets IdleMinutes and DeadlineMinutes parms for task with trigger
// of type TASK_EVENT_TRIGGER_ON_IDLE
PyObject *PyIScheduledWorkItem::GetIdleWait(PyObject *self, PyObject *args)
{
    IScheduledWorkItem *pISWI = GetI(self);
    if (pISWI == NULL)
        return NULL;
    HRESULT hr;
    WORD IdleMinutes = 0, DeadlineMinutes = 0;
    PyObject *obIdleMinutes = NULL, *obDeadlineMinutes = NULL;
    if (!PyArg_ParseTuple(args, ":PyIScheduledWorkItem::GetIdleWait"))
        return NULL;
    PY_INTERFACE_PRECALL;
    hr = pISWI->GetIdleWait(&IdleMinutes, &DeadlineMinutes);
    PY_INTERFACE_POSTCALL;

    if (FAILED(hr))
        return PyCom_BuildPyException(hr, pISWI, IID_IScheduledWorkItem);
    return Py_BuildValue("ll", IdleMinutes, DeadlineMinutes);
}

// @pymethod |PyIScheduledWorkItem|Run|Starts task
PyObject *PyIScheduledWorkItem::Run(PyObject *self, PyObject *args)
{
    IScheduledWorkItem *pISWI = GetI(self);
    if (pISWI == NULL)
        return NULL;
    if (!PyArg_ParseTuple(args, ":PyIScheduledWorkItem::Run"))
        return NULL;
    HRESULT hr;
    PY_INTERFACE_PRECALL;
    hr = pISWI->Run();

    PY_INTERFACE_POSTCALL;

    if (FAILED(hr))
        return PyCom_BuildPyException(hr, pISWI, IID_IScheduledWorkItem);
    Py_INCREF(Py_None);
    return Py_None;
}

// @pymethod |PyIScheduledWorkItem|Terminate|Terminate process if task is running
PyObject *PyIScheduledWorkItem::Terminate(PyObject *self, PyObject *args)
{
    IScheduledWorkItem *pISWI = GetI(self);
    if (pISWI == NULL)
        return NULL;
    if (!PyArg_ParseTuple(args, ":PyIScheduledWorkItem::Terminate"))
        return NULL;
    HRESULT hr;
    PY_INTERFACE_PRECALL;
    hr = pISWI->Terminate();

    PY_INTERFACE_POSTCALL;

    if (FAILED(hr))
        return PyCom_BuildPyException(hr, pISWI, IID_IScheduledWorkItem);
    Py_INCREF(Py_None);
    return Py_None;
}

// @pymethod |PyIScheduledWorkItem|EditWorkItem|Brings up standard Scheduled Task dialog
PyObject *PyIScheduledWorkItem::EditWorkItem(PyObject *self, PyObject *args)
{
    IScheduledWorkItem *pISWI = GetI(self);
    if (pISWI == NULL)
        return NULL;
    // @pyparm <o PyHANDLE>|hParent||Reserved, use 0 or None if passed
    // @pyparm int|dwReserved||Reserved, use 0 if passed
    HWND hParent = NULL;
    PyObject *obhParent = Py_None;
    DWORD dwReserved = 0;
    if (!PyArg_ParseTuple(args, "|Ol:PyIScheduledWorkItem::EditWorkItem", &obhParent, &dwReserved))
        return NULL;
    if (!PyWinObject_AsHANDLE(obhParent, (HANDLE *)&hParent))
        return NULL;
    HRESULT hr;
    PY_INTERFACE_PRECALL;
    hr = pISWI->EditWorkItem(hParent, dwReserved);

    PY_INTERFACE_POSTCALL;

    if (FAILED(hr))
        return PyCom_BuildPyException(hr, pISWI, IID_IScheduledWorkItem);
    Py_INCREF(Py_None);
    return Py_None;
}

// @pymethod <o PyDateTime>|PyIScheduledWorkItem|GetMostRecentRunTime|Returns last time task ran
PyObject *PyIScheduledWorkItem::GetMostRecentRunTime(PyObject *self, PyObject *args)
{
    IScheduledWorkItem *pISWI = GetI(self);
    if (pISWI == NULL)
        return NULL;
    SYSTEMTIME LastRun;
    if (!PyArg_ParseTuple(args, ":PyIScheduledWorkItem::GetMostRecentRunTime"))
        return NULL;
    HRESULT hr;
    PY_INTERFACE_PRECALL;
    hr = pISWI->GetMostRecentRunTime(&LastRun);
    PY_INTERFACE_POSTCALL;
    if (FAILED(hr))
        return PyCom_BuildPyException(hr, pISWI, IID_IScheduledWorkItem);
    return PyWinObject_FromSYSTEMTIME(LastRun);
}

// @pymethod int|PyIScheduledWorkItem|GetStatus|Returns status (SCHED_S_TASK... constants)
PyObject *PyIScheduledWorkItem::GetStatus(PyObject *self, PyObject *args)
{
    IScheduledWorkItem *pISWI = GetI(self);
    if (pISWI == NULL)
        return NULL;
    HRESULT hr, hrStatus;
    PY_INTERFACE_PRECALL;
    hr = pISWI->GetStatus(&hrStatus);
    PY_INTERFACE_POSTCALL;

    if (FAILED(hr))
        return PyCom_BuildPyException(hr, pISWI, IID_IScheduledWorkItem);
    return Py_BuildValue("l", hrStatus);
}

// @pymethod (int,int)|PyIScheduledWorkItem|GetExitCode|Returns tuple of task's exit code and error returned to Task
// Scheduler if process could not start
PyObject *PyIScheduledWorkItem::GetExitCode(PyObject *self, PyObject *args)
{
    IScheduledWorkItem *pISWI = GetI(self);
    if (pISWI == NULL)
        return NULL;
    HRESULT hr = 0;
    DWORD ExitCode = 0;
    if (!PyArg_ParseTuple(args, ":PyIScheduledWorkItem::GetExitCode"))
        return NULL;
    PY_INTERFACE_PRECALL;
    // this hr receives the startup error code if task could not start
    hr = pISWI->GetExitCode(&ExitCode);
    PY_INTERFACE_POSTCALL;
    return Py_BuildValue("ll", ExitCode, hr);
}

// @pymethod |PyIScheduledWorkItem|SetComment|Set comment string for task
PyObject *PyIScheduledWorkItem::SetComment(PyObject *self, PyObject *args)
{
    IScheduledWorkItem *pISWI = GetI(self);
    if (pISWI == NULL)
        return NULL;
    // @pyparm <o unicode>|Comment||Freeform comment string
    PyObject *obpwszComment;
    LPWSTR pwszComment;
    if (!PyArg_ParseTuple(args, "O:SetComment", &obpwszComment))
        return NULL;

    if (!PyWinObject_AsWCHAR(obpwszComment, &pwszComment))
        return NULL;
    HRESULT hr;
    PY_INTERFACE_PRECALL;
    hr = pISWI->SetComment(pwszComment);
    PY_INTERFACE_POSTCALL;
    PyWinObject_FreeWCHAR(pwszComment);

    if (FAILED(hr))
        return PyCom_BuildPyException(hr, pISWI, IID_IScheduledWorkItem);
    Py_INCREF(Py_None);
    return Py_None;
}

// @pymethod <o PyUnicode>|PyIScheduledWorkItem|GetComment|Return comment string associated with task.
PyObject *PyIScheduledWorkItem::GetComment(PyObject *self, PyObject *args)
{
    IScheduledWorkItem *pISWI = GetI(self);
    if (pISWI == NULL)
        return NULL;
    LPWSTR Comment = NULL;
    PyObject *ret = NULL;
    if (!PyArg_ParseTuple(args, ":PyIScheduledWorkItem::GetComment"))
        return NULL;
    HRESULT hr;
    PY_INTERFACE_PRECALL;
    hr = pISWI->GetComment(&Comment);
    PY_INTERFACE_POSTCALL;
    if (FAILED(hr))
        PyCom_BuildPyException(hr, pISWI, IID_IScheduledWorkItem);
    else
        ret = PyWinObject_FromWCHAR(Comment);
    CoTaskMemFree(Comment);
    return ret;
}

// @pymethod |PyIScheduledWorkItem|SetCreator|Specify who (or what) created task, can be any string
PyObject *PyIScheduledWorkItem::SetCreator(PyObject *self, PyObject *args)
{
    IScheduledWorkItem *pISWI = GetI(self);
    if (pISWI == NULL)
        return NULL;
    // @pyparm <o unicode>|Creator||Originator of task, does not have to be valid username
    PyObject *obpwszCreator;
    LPWSTR pwszCreator;
    if (!PyArg_ParseTuple(args, "O:SetCreator", &obpwszCreator))
        return NULL;
    if (!PyWinObject_AsWCHAR(obpwszCreator, &pwszCreator))
        return NULL;
    HRESULT hr;
    PY_INTERFACE_PRECALL;
    hr = pISWI->SetCreator(pwszCreator);
    PY_INTERFACE_POSTCALL;
    PyWinObject_FreeWCHAR(pwszCreator);

    if (FAILED(hr))
        return PyCom_BuildPyException(hr, pISWI, IID_IScheduledWorkItem);
    Py_INCREF(Py_None);
    return Py_None;
}

// @pymethod |PyIScheduledWorkItem|GetCreator|Returns creator info, can be any string data
PyObject *PyIScheduledWorkItem::GetCreator(PyObject *self, PyObject *args)
{
    IScheduledWorkItem *pISWI = GetI(self);
    if (pISWI == NULL)
        return NULL;
    LPWSTR Creator;
    PyObject *ret = NULL;
    if (!PyArg_ParseTuple(args, ":PyIScheduledWorkItem::GetCreator"))
        return NULL;
    HRESULT hr;
    PY_INTERFACE_PRECALL;
    hr = pISWI->GetCreator(&Creator);
    PY_INTERFACE_POSTCALL;

    if (FAILED(hr))
        PyCom_BuildPyException(hr, pISWI, IID_IScheduledWorkItem);
    else
        ret = PyWinObject_FromWCHAR(Creator);
    CoTaskMemFree(Creator);
    return ret;
}

// @pymethod |PyIScheduledWorkItem|SetWorkItemData|Set data associated with task (treated as uninterpreted bytes)
PyObject *PyIScheduledWorkItem::SetWorkItemData(PyObject *self, PyObject *args)
{
    IScheduledWorkItem *pISWI = GetI(self);
    if (pISWI == NULL)
        return NULL;
    // @pyparm string|Data||Character data, treated as uninterpreted bytes
    BYTE *workitem_data = NULL;
    Py_ssize_t data_len = 0;
    PyObject *obworkitem_data = NULL;
    if (!PyArg_ParseTuple(args, "O:PyIScheduledWorkItem::SetWorkItemData", &obworkitem_data))
        return NULL;
    if (obworkitem_data != Py_None) {
        if (PyBytes_AsStringAndSize(obworkitem_data, (CHAR **)&workitem_data, &data_len) == -1)
            return NULL;
        else
            // Task Scheduler won't take an empty string for data anymore ??????
            if (data_len == 0)
                workitem_data = NULL;
    }

    HRESULT hr;
    PY_INTERFACE_PRECALL;
    hr = pISWI->SetWorkItemData(PyWin_SAFE_DOWNCAST(data_len, Py_ssize_t, WORD), workitem_data);
    PY_INTERFACE_POSTCALL;

    if (FAILED(hr))
        return PyCom_BuildPyException(hr, pISWI, IID_IScheduledWorkItem);
    Py_INCREF(Py_None);
    return Py_None;
}

// @pymethod string|PyIScheduledWorkItem|GetWorkItemData|Retrieve data associated with task
PyObject *PyIScheduledWorkItem::GetWorkItemData(PyObject *self, PyObject *args)
{
    IScheduledWorkItem *pISWI = GetI(self);
    if (pISWI == NULL)
        return NULL;
    WORD data_len;
    PyObject *ret = NULL;
    BYTE *workitem_data;
    if (!PyArg_ParseTuple(args, ":PyIScheduledWorkItem::GetWorkItemData"))
        return NULL;

    HRESULT hr;
    PY_INTERFACE_PRECALL;
    hr = pISWI->GetWorkItemData(&data_len, &workitem_data);
    PY_INTERFACE_POSTCALL;

    if (FAILED(hr))
        PyCom_BuildPyException(hr, pISWI, IID_IScheduledWorkItem);
    else if (workitem_data != NULL)
        ret = PyBytes_FromStringAndSize((const char *)workitem_data, data_len);
    else {
        Py_INCREF(Py_None);
        ret = Py_None;
    }
    CoTaskMemFree(workitem_data);
    return ret;
}

// @pymethod |PyIScheduledWorkItem|SetErrorRetryCount|Specify nbr of times to attempt to run task if it can't start (not
// currently implemented)
PyObject *PyIScheduledWorkItem::SetErrorRetryCount(PyObject *self, PyObject *args)
{
    IScheduledWorkItem *pISWI = GetI(self);
    if (pISWI == NULL)
        return NULL;
    // @pyparm int|wRetryCount||Nbr of attemps to start task
    INT iwRetryCount;
    WORD wRetryCount;
    if (!PyArg_ParseTuple(args, "i:SetErrorRetryCount", &iwRetryCount))
        return NULL;
    wRetryCount = iwRetryCount;
    HRESULT hr;
    PY_INTERFACE_PRECALL;
    hr = pISWI->SetErrorRetryCount(wRetryCount);
    PY_INTERFACE_POSTCALL;

    if (FAILED(hr))
        return PyCom_BuildPyException(hr, pISWI, IID_IScheduledWorkItem);
    Py_INCREF(Py_None);
    return Py_None;
}

// @pymethod |PyIScheduledWorkItem|GetErrorRetryCount|Return nbr of times Task scheduler should try to run task (not
// currently implemented)
PyObject *PyIScheduledWorkItem::GetErrorRetryCount(PyObject *self, PyObject *args)
{
    IScheduledWorkItem *pISWI = GetI(self);
    if (pISWI == NULL)
        return NULL;
    WORD wRetryCount;

    if (!PyArg_ParseTuple(args, ":PyIScheduledWorkItem::GetErrorRetryCount"))
        return NULL;
    HRESULT hr;
    PY_INTERFACE_PRECALL;
    hr = pISWI->GetErrorRetryCount(&wRetryCount);
    PY_INTERFACE_POSTCALL;

    if (FAILED(hr))
        return PyCom_BuildPyException(hr, pISWI, IID_IScheduledWorkItem);
    return Py_BuildValue("l", wRetryCount);
}

// @pymethod |PyIScheduledWorkItem|SetErrorRetryInterval|Interval in minutes between attempts to run task. Not
// implemented according to SDK
PyObject *PyIScheduledWorkItem::SetErrorRetryInterval(PyObject *self, PyObject *args)
{
    IScheduledWorkItem *pISWI = GetI(self);
    if (pISWI == NULL)
        return NULL;
    // @pyparm int|RetryInterval||Interval in minutes
    INT iwRetryInterval;
    WORD wRetryInterval;
    if (!PyArg_ParseTuple(args, "i:PyIScheduledWorkItem::SetErrorRetryInterval", &iwRetryInterval))
        return NULL;
    wRetryInterval = iwRetryInterval;
    HRESULT hr;
    PY_INTERFACE_PRECALL;
    hr = pISWI->SetErrorRetryInterval(wRetryInterval);
    PY_INTERFACE_POSTCALL;

    if (FAILED(hr))
        return PyCom_BuildPyException(hr, pISWI, IID_IScheduledWorkItem);
    Py_INCREF(Py_None);
    return Py_None;
}

// @pymethod |PyIScheduledWorkItem|GetErrorRetryInterval|Returns nbr of minutes between attempts to run task. Not
// implemented according to SDK
PyObject *PyIScheduledWorkItem::GetErrorRetryInterval(PyObject *self, PyObject *args)
{
    IScheduledWorkItem *pISWI = GetI(self);
    if (pISWI == NULL)
        return NULL;
    WORD wRetryInterval = 0;
    if (!PyArg_ParseTuple(args, ":PyIScheduledWorkItem::GetErrorRetryInterval"))
        return NULL;
    HRESULT hr;
    PY_INTERFACE_PRECALL;
    hr = pISWI->GetErrorRetryInterval(&wRetryInterval);
    PY_INTERFACE_POSTCALL;

    if (FAILED(hr))
        return PyCom_BuildPyException(hr, pISWI, IID_IScheduledWorkItem);
    return Py_BuildValue("l", wRetryInterval);
}

// @pymethod |PyIScheduledWorkItem|SetFlags|Set flags for task
PyObject *PyIScheduledWorkItem::SetFlags(PyObject *self, PyObject *args)
{
    IScheduledWorkItem *pISWI = GetI(self);
    if (pISWI == NULL)
        return NULL;
    // @pyparm int|dwFlags||Combination of TASK_FLAG_* constants
    DWORD dwFlags;
    if (!PyArg_ParseTuple(args, "l:PyIScheduledWorkItem::SetFlags", &dwFlags))
        return NULL;
    HRESULT hr;
    PY_INTERFACE_PRECALL;
    hr = pISWI->SetFlags(dwFlags);
    PY_INTERFACE_POSTCALL;

    if (FAILED(hr))
        return PyCom_BuildPyException(hr, pISWI, IID_IScheduledWorkItem);
    Py_INCREF(Py_None);
    return Py_None;
}

// @pymethod int|PyIScheduledWorkItem|GetFlags|Returns flags for task (TASK_FLAG_* constants)
PyObject *PyIScheduledWorkItem::GetFlags(PyObject *self, PyObject *args)
{
    IScheduledWorkItem *pISWI = GetI(self);
    if (pISWI == NULL)
        return NULL;
    DWORD dwFlags;
    if (!PyArg_ParseTuple(args, ":PyIScheduledWorkItem::GetFlags"))
        return NULL;
    HRESULT hr;
    PY_INTERFACE_PRECALL;
    hr = pISWI->GetFlags(&dwFlags);
    PY_INTERFACE_POSTCALL;

    if (FAILED(hr))
        return PyCom_BuildPyException(hr, pISWI, IID_IScheduledWorkItem);
    return Py_BuildValue("l", dwFlags);
}

// @pymethod |PyIScheduledWorkItem|SetAccountInformation|Set username and password under which task will run
// @comm On some systems, username and password are verified at the time the task is saved, on others when the task
// tries to run
PyObject *PyIScheduledWorkItem::SetAccountInformation(PyObject *self, PyObject *args)
{
    IScheduledWorkItem *pISWI = GetI(self);
    if (pISWI == NULL)
        return NULL;
    // @pyparm <o unicode>|AccountName||AccountName, use "" for local system account (can only be used by
    // Administrators)
    // @pyparm <o unicode>|Password||Password - Can be None for local System account, or if
    // TASK_FLAG_RUN_ONLY_IF_LOGGED_ON is set
    PyObject *obAccountName = NULL, *obPassword = NULL;
    LPWSTR AccountName = NULL, Password = NULL;
    if (!PyArg_ParseTuple(args, "OO:SetAccountInformation", &obAccountName, &obPassword))
        return NULL;
    if (!PyWinObject_AsWCHAR(obAccountName, &AccountName, FALSE))
        return NULL;
    if (!PyWinObject_AsWCHAR(obPassword, &Password, TRUE)) {
        PyWinObject_FreeWCHAR(AccountName);
        return NULL;
    }
    HRESULT hr;
    PY_INTERFACE_PRECALL;
    hr = pISWI->SetAccountInformation(AccountName, Password);
    PY_INTERFACE_POSTCALL;
    PyWinObject_FreeWCHAR(AccountName);
    PyWinObject_FreeWCHAR(Password);

    if (FAILED(hr))
        return PyCom_BuildPyException(hr, pISWI, IID_IScheduledWorkItem);
    Py_INCREF(Py_None);
    return Py_None;
}

// @pymethod <o PyUNICODE>|PyIScheduledWorkItem|GetAccountInformation|Returns username that task will run under
PyObject *PyIScheduledWorkItem::GetAccountInformation(PyObject *self, PyObject *args)
{
    IScheduledWorkItem *pISWI = GetI(self);
    if (pISWI == NULL)
        return NULL;
    LPWSTR AccountName;
    PyObject *ret = NULL;
    if (!PyArg_ParseTuple(args, ":PyIScheduledWorkItem::GetAccountInformation"))
        return NULL;
    HRESULT hr;
    PY_INTERFACE_PRECALL;
    hr = pISWI->GetAccountInformation(&AccountName);
    PY_INTERFACE_POSTCALL;

    if (FAILED(hr))
        PyCom_BuildPyException(hr, pISWI, IID_IScheduledWorkItem);
    else
        ret = PyWinObject_FromWCHAR(AccountName);
    CoTaskMemFree(AccountName);
    return ret;
}

// @object PyIScheduledWorkItem|Python object that encapsulates the IScheduledWorkItem interface
static struct PyMethodDef PyIScheduledWorkItem_methods[] = {
    {"CreateTrigger", PyIScheduledWorkItem::CreateTrigger,
     1},  // @pymeth CreateTrigger|Creates a new trigger for a task, returns index and new ITaskTrigger interface
    {"DeleteTrigger", PyIScheduledWorkItem::DeleteTrigger, 1},  // @pymeth DeleteTrigger|Deletes specified trigger
    {"GetTriggerCount", PyIScheduledWorkItem::GetTriggerCount,
     1},  // @pymeth GetTriggerCount|Returns number of triggers defined for the task
    {"GetTrigger", PyIScheduledWorkItem::GetTrigger,
     1},  // @pymeth GetTrigger|Retrieves ITaskTrigger interface for specified trigger index
    {"GetTriggerString", PyIScheduledWorkItem::GetTriggerString,
     1},  // @pymeth GetTriggerString|Creates a human-readable summary of specified trigger
    {"GetRunTimes", PyIScheduledWorkItem::GetRunTimes,
     1},  // @pymeth GetRunTimes|Return specified number of run times within given time frame
    {"GetNextRunTime", PyIScheduledWorkItem::GetNextRunTime,
     1},  // @pymeth GetNextRunTime|Returns next time that task is scheduled to run
    {"SetIdleWait", PyIScheduledWorkItem::SetIdleWait,
     1},  // @pymeth SetIdleWait|Sets idle parms for task with trigger of type TASK_EVENT_TRIGGER_ON_IDLE
    {"GetIdleWait", PyIScheduledWorkItem::GetIdleWait,
     1},  // @pymeth GetIdleWait|Gets idle parms for task with trigger of type TASK_EVENT_TRIGGER_ON_IDLE
    {"Run", PyIScheduledWorkItem::Run, 1},              // @pymeth Run|Starts task
    {"Terminate", PyIScheduledWorkItem::Terminate, 1},  // @pymeth Terminate|Terminate process if task is running
    {"EditWorkItem", PyIScheduledWorkItem::EditWorkItem,
     1},  // @pymeth EditWorkItem|Brings up standard Scheduled Task dialog
    {"GetMostRecentRunTime", PyIScheduledWorkItem::GetMostRecentRunTime,
     1},                                                // @pymeth GetMostRecentRunTime|Returns last time task ran
    {"GetStatus", PyIScheduledWorkItem::GetStatus, 1},  // @pymeth GetStatus|Returns status (SCHED_S_TASK... constants)
    {"GetExitCode", PyIScheduledWorkItem::GetExitCode,
     1},  // @pymeth GetExitCode|Returns tuple of task's exit code and error returned to Task Scheduler if process could
          // not start
    {"SetComment", PyIScheduledWorkItem::SetComment, 1},  // @pymeth SetComment|Set comment string for task
    {"GetComment", PyIScheduledWorkItem::GetComment,
     1},  // @pymeth GetComment|Return comment string associated with task.
    {"SetCreator", PyIScheduledWorkItem::SetCreator,
     1},  // @pymeth SetCreator|Specify who (or what) created task, can be any string
    {"GetCreator", PyIScheduledWorkItem::GetCreator,
     1},  // @pymeth GetCreator|Returns creator info, can be any string data
    {"SetWorkItemData", PyIScheduledWorkItem::SetWorkItemData,
     1},  // @pymeth SetWorkItemData|Set data associated with task (treated as uninterpreted bytes)
    {"GetWorkItemData", PyIScheduledWorkItem::GetWorkItemData,
     1},  // @pymeth GetWorkItemData|Retrieve data associated with task
    {"SetErrorRetryCount", PyIScheduledWorkItem::SetErrorRetryCount,
     1},  // @pymeth SetErrorRetryCount|Specify nbr of times to attempt to run task if it can't start (not currently
          // implemented)
    {"GetErrorRetryCount", PyIScheduledWorkItem::GetErrorRetryCount,
     1},  // @pymeth GetErrorRetryCount|Return nbr of times Task scheduler should try to run task (not currently
          // implemented)
    {"SetErrorRetryInterval", PyIScheduledWorkItem::SetErrorRetryInterval,
     1},  // @pymeth SetErrorRetryInterval|Interval in minutes between attempts to run task. Not implemented according
          // to SDK
    {"GetErrorRetryInterval", PyIScheduledWorkItem::GetErrorRetryInterval,
     1},  // @pymeth GetErrorRetryInterval|Returns nbr of minutes between attempts to run task. Not implemented
          // according to SDK
    {"SetFlags", PyIScheduledWorkItem::SetFlags, 1},  // @pymeth SetFlags|Set flags for task
    {"GetFlags", PyIScheduledWorkItem::GetFlags, 1},  // @pymeth GetFlags|Returns flags for task (TASK_FLAG_* constants)
    {"SetAccountInformation", PyIScheduledWorkItem::SetAccountInformation,
     1},  // @pymeth SetAccountInformation|Set username and password under which task will run
    {"GetAccountInformation", PyIScheduledWorkItem::GetAccountInformation,
     1},  // @pymeth GetAccountInformation|Returns username that task will run under
    {NULL}};

PyComTypeObject PyIScheduledWorkItem::type("PyIScheduledWorkItem", &PyIUnknown::type, sizeof(PyIScheduledWorkItem),
                                           PyIScheduledWorkItem_methods, GET_PYCOM_CTOR(PyIScheduledWorkItem));
