import struct

import win32wnet

from .netbioscon import *

UCHAR = "B"
WORD = "H"
DWORD = "I"
USHORT = "H"
ULONG = "I"

ADAPTER_STATUS_ITEMS = [
    ("6s", "adapter_address"),
    (UCHAR, "rev_major"),
    (UCHAR, "reserved0"),
    (UCHAR, "adapter_type"),
    (UCHAR, "rev_minor"),
    (WORD, "duration"),
    (WORD, "frmr_recv"),
    (WORD, "frmr_xmit"),
    (WORD, "iframe_recv_err"),
    (WORD, "xmit_aborts"),
    (DWORD, "xmit_success"),
    (DWORD, "recv_success"),
    (WORD, "iframe_xmit_err"),
    (WORD, "recv_buff_unavail"),
    (WORD, "t1_timeouts"),
    (WORD, "ti_timeouts"),
    (DWORD, "reserved1"),
    (WORD, "free_ncbs"),
    (WORD, "max_cfg_ncbs"),
    (WORD, "max_ncbs"),
    (WORD, "xmit_buf_unavail"),
    (WORD, "max_dgram_size"),
    (WORD, "pending_sess"),
    (WORD, "max_cfg_sess"),
    (WORD, "max_sess"),
    (WORD, "max_sess_pkt_size"),
    (WORD, "name_count"),
]

NAME_BUFFER_ITEMS = [
    (str(NCBNAMSZ) + "s", "name"),
    (UCHAR, "name_num"),
    (UCHAR, "name_flags"),
]

SESSION_HEADER_ITEMS = [
    (UCHAR, "sess_name"),
    (UCHAR, "num_sess"),
    (UCHAR, "rcv_dg_outstanding"),
    (UCHAR, "rcv_any_outstanding"),
]

SESSION_BUFFER_ITEMS = [
    (UCHAR, "lsn"),
    (UCHAR, "state"),
    (str(NCBNAMSZ) + "s", "local_name"),
    (str(NCBNAMSZ) + "s", "remote_name"),
    (UCHAR, "rcvs_outstanding"),
    (UCHAR, "sends_outstanding"),
]

LANA_ENUM_ITEMS = [
    ("B", "length"),  # Number of valid entries in lana[]
    (str(MAX_LANA + 1) + "s", "lana"),
]

FIND_NAME_HEADER_ITEMS = [
    (WORD, "node_count"),
    (UCHAR, "reserved"),
    (UCHAR, "unique_group"),
]

FIND_NAME_BUFFER_ITEMS = [
    (UCHAR, "length"),
    (UCHAR, "access_control"),
    (UCHAR, "frame_control"),
    ("6s", "destination_addr"),
    ("6s", "source_addr"),
    ("18s", "routing_info"),
]

ACTION_HEADER_ITEMS = [
    (ULONG, "transport_id"),
    (USHORT, "action_code"),
    (USHORT, "reserved"),
]

del UCHAR, WORD, DWORD, USHORT, ULONG

NCB = win32wnet.NCB


def Netbios(ncb):
    ob = ncb.Buffer
    is_ours = hasattr(ob, "_pack")
    if is_ours:
        ob._pack()
    try:
        return win32wnet.Netbios(ncb)
    finally:
        if is_ours:
            ob._unpack()


class NCBStruct:
    def __init__(self, items):
        self._format = "".join([item[0] for item in items])
        self._items = items
        self._buffer_ = win32wnet.NCBBuffer(struct.calcsize(self._format))

        for format, name in self._items:
            if len(format) == 1:
                if format == "c":
                    val = "\0"
                else:
                    val = 0
            else:
                l = int(format[:-1])
                val = "\0" * l
            self.__dict__[name] = val

    def _pack(self):
        vals = []
        for format, name in self._items:
            try:
                vals.append(self.__dict__[name])
            except KeyError:
                vals.append(None)

        self._buffer_[:] = struct.pack(*(self._format,) + tuple(vals))

    def _unpack(self):
        items = struct.unpack(self._format, self._buffer_)
        assert len(items) == len(self._items), "unexpected number of items to unpack!"
        for (format, name), val in zip(self._items, items):
            self.__dict__[name] = val

    def __setattr__(self, attr, val):
        if attr not in self.__dict__ and attr[0] != "_":
            for format, attr_name in self._items:
                if attr == attr_name:
                    break
            else:
                raise AttributeError(attr)
        self.__dict__[attr] = val


def ADAPTER_STATUS():
    return NCBStruct(ADAPTER_STATUS_ITEMS)


def NAME_BUFFER():
    return NCBStruct(NAME_BUFFER_ITEMS)


def SESSION_HEADER():
    return NCBStruct(SESSION_HEADER_ITEMS)


def SESSION_BUFFER():
    return NCBStruct(SESSION_BUFFER_ITEMS)


def LANA_ENUM():
    return NCBStruct(LANA_ENUM_ITEMS)


def FIND_NAME_HEADER():
    return NCBStruct(FIND_NAME_HEADER_ITEMS)


def FIND_NAME_BUFFER():
    return NCBStruct(FIND_NAME_BUFFER_ITEMS)


def ACTION_HEADER():
    return NCBStruct(ACTION_HEADER_ITEMS)


if __name__ == "__main__":
    # code ported from "HOWTO: Get the MAC Address for an Ethernet Adapter"
    # MS KB ID: Q118623
    ncb = NCB()
    ncb.Command = NCBENUM
    la_enum = LANA_ENUM()
    ncb.Buffer = la_enum
    rc = Netbios(ncb)
    if rc != 0:
        raise RuntimeError("Unexpected result %d" % (rc,))
    for i in range(la_enum.length):
        ncb.Reset()
        ncb.Command = NCBRESET
        ncb.Lana_num = la_enum.lana[i]
        rc = Netbios(ncb)
        if rc != 0:
            raise RuntimeError("Unexpected result %d" % (rc,))
        ncb.Reset()
        ncb.Command = NCBASTAT
        ncb.Lana_num = la_enum.lana[i]
        ncb.Callname = b"*               "
        adapter = ADAPTER_STATUS()
        ncb.Buffer = adapter
        Netbios(ncb)
        print("Adapter address:", end=" ")
        for ch in adapter.adapter_address:
            print(f"{ch:02x}", end=" ")
        print()
