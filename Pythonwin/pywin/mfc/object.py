# MFC base classes.

import win32ui


class Object:
    def __init__(self, initObj=None):
        self._obj_ = initObj
        # 		self._obj_ = initObj
        if initObj is not None:
            initObj.AttachObject(self)

    def __del__(self):
        self.close()

    def __getattr__(
        self, attr
    ):  # Make this object look like the underlying win32ui one.
        # During cleanup __dict__ is not available, causing recursive death.
        if not attr.startswith("__"):
            try:
                if self._obj_ is not None:
                    return getattr(self._obj_, attr)
                # Only raise this error for non "internal" names -
                # Python may be calling __len__, __bool__, etc, so
                # we don't want this exception
                if attr[0] != "_" and attr[-1] != "_":
                    raise win32ui.error("The MFC object has died.")
            except KeyError:
                # No _obj_ at all - don't report MFC object died when there isn't one!
                pass
        raise AttributeError(attr)

    def OnAttachedObjectDeath(self):
        # print("object", self.__class__.__name__, "dieing")
        self._obj_ = None

    def close(self):
        if self._obj_ is not None:
            self._obj_.AttachObject(None)
            self._obj_ = None


class CmdTarget(Object):
    def __init__(self, initObj):
        Object.__init__(self, initObj)

    def HookNotifyRange(self, handler, firstID, lastID):
        oldhandlers = []
        for i in range(firstID, lastID + 1):
            oldhandlers.append(self.HookNotify(handler, i))
        return oldhandlers

    def HookCommandRange(self, handler, firstID, lastID):
        oldhandlers = []
        for i in range(firstID, lastID + 1):
            oldhandlers.append(self.HookCommand(handler, i))
        return oldhandlers

    def HookCommandUpdateRange(self, handler, firstID, lastID):
        oldhandlers = []
        for i in range(firstID, lastID + 1):
            oldhandlers.append(self.HookCommandUpdate(handler, i))
        return oldhandlers
