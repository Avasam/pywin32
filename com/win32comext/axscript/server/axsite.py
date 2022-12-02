from __future__ import annotations

from typing import TYPE_CHECKING, Any, cast

import pythoncom
import winerror
from win32com.axscript import axscript
from win32com.server import exception, util
from win32comext.axscript.client.framework import COMScript

if TYPE_CHECKING:
    from _win32typing import PyIUnknown
else:
    PyIUnknown: Any


class AXEngine:
    def __init__(self, site, engine: str | PyIUnknown):
        engine = (
            pythoncom.CoCreateInstance(
                engine, None, pythoncom.CLSCTX_SERVER, pythoncom.IID_IUnknown
            )
            if isinstance(engine, str)
            else engine
        )

        self.eScript: COMScript = cast(
            COMScript, engine.QueryInterface(axscript.IID_IActiveScript)
        )
        self.eParse: COMScript = cast(
            COMScript, engine.QueryInterface(axscript.IID_IActiveScriptParse)
        )
        self.eSafety: PyIUnknown = engine.QueryInterface(axscript.IID_IObjectSafety)

        self.eScript.SetScriptSite(site)
        self.eParse.InitNew()

    def __del__(self):
        self.Close()

    def GetScriptDispatch(self, name=None):
        return self.eScript.GetScriptDispatch(name)

    def AddNamedItem(self, item, flags):
        return self.eScript.AddNamedItem(item, flags)

    # Some helpers.
    def AddCode(self, code, flags=0):
        self.eParse.ParseScriptText(code, None, None, None, 0, 0, flags)

    def EvalCode(self, code):
        return self.eParse.ParseScriptText(
            code, None, None, None, 0, 0, axscript.SCRIPTTEXT_ISEXPRESSION
        )

    def Start(self):
        # Should maybe check state?
        # Do I need to transition through?
        self.eScript.SetScriptState(axscript.SCRIPTSTATE_STARTED)

    #    self.eScript.SetScriptState(axscript.SCRIPTSTATE_CONNECTED)

    def Close(self):
        if self.eScript:
            self.eScript.Close()
        self.eScript = self.eParse = self.eSafety = None

    def SetScriptState(self, state):
        self.eScript.SetScriptState(state)


IActiveScriptSite_methods = [
    "GetLCID",
    "GetItemInfo",
    "GetDocVersionString",
    "OnScriptTerminate",
    "OnStateChange",
    "OnScriptError",
    "OnEnterScript",
    "OnLeaveScript",
]


class AXSite:
    """An Active Scripting site.  A Site can have exactly one engine."""

    _public_methods_ = IActiveScriptSite_methods
    _com_interfaces_ = [axscript.IID_IActiveScriptSite]

    def __init__(self, objModel={}, engine: AXEngine | None = None, lcid=0):
        self.lcid = lcid
        self.objModel = {}
        for name, object in objModel.items():
            # Gregs code did string.lower this - I think that is callers job if he wants!
            self.objModel[name] = object
        self.engine = self.AddEngine(engine) if engine else None

    def AddEngine(self, engine: AXEngine | str):
        """Adds a new engine to the site.
        engine can be a string, or a fully wrapped engine object.
        """
        if isinstance(engine, str):
            newEngine = AXEngine(util.wrap(self), engine)
        else:
            newEngine = engine
        flags = (
            axscript.SCRIPTITEM_ISVISIBLE
            | axscript.SCRIPTITEM_NOCODE
            | axscript.SCRIPTITEM_GLOBALMEMBERS
            | axscript.SCRIPTITEM_ISPERSISTENT
        )
        for name in self.objModel.keys():
            newEngine.AddNamedItem(name, flags)
            newEngine.SetScriptState(axscript.SCRIPTSTATE_INITIALIZED)
        return newEngine

    # B/W compat
    _AddEngine = AddEngine

    def _Close(self):
        if self.engine:
            self.engine.Close()
        self.objModel = {}

    def GetLCID(self):
        return self.lcid

    def GetItemInfo(self, name, returnMask):
        if name not in self.objModel:
            raise exception.Exception(
                scode=winerror.TYPE_E_ELEMENTNOTFOUND, desc="item not found"
            )

        ### for now, we don't have any type information

        if returnMask & axscript.SCRIPTINFO_IUNKNOWN:
            return (self.objModel[name], None)

        return (None, None)

    def GetDocVersionString(self):
        return "Python AXHost version 1.0"

    def OnScriptTerminate(self, result, excepInfo):
        pass

    def OnStateChange(self, state):
        pass

    def OnScriptError(self, errorInterface):
        return winerror.S_FALSE

    def OnEnterScript(self):
        pass

    def OnLeaveScript(self):
        pass
