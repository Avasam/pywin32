from winnt import *

from .commdlg import *
from .consoleapi import *
from .dbt import *
from .imm import *
from .minwindef import *
from .prsht import *
from .richedit import *
from .wincontypes import *
from .wingdi import *
from .winreg import *
from .winuser import *

_NLSCMPERROR = 2147483647  # Included from string.h

# winuser.h line 4601
CUDR_NORMAL = 0
CUDR_NOSNAPTOGRID = 1
CUDR_NORESOLVEPOSITIONS = 2
CUDR_NOCLOSEGAPS = 4
CUDR_NEGATIVECOORDS = 8
CUDR_NOPRIMARY = 16
MFS_MASK = 4235
MFS_HOTTRACKDRAWN = 268435456
MFS_CACHEDBMP = 536870912
MFS_BOTTOMGAPDROP = 1073741824
MFS_TOPGAPDROP = -2147483648
MFS_GAPDROP = -1073741824
IDC_ARROW = 32512
IDC_IBEAM = 32513
IDC_WAIT = 32514
IDC_CROSS = 32515
IDC_UPARROW = 32516
IDC_SIZE = 32640  # OBSOLETE: use IDC_SIZEALL
IDC_ICON = 32641  # OBSOLETE: use IDC_ARROW
IDC_SIZENWSE = 32642
IDC_SIZENESW = 32643
IDC_SIZEWE = 32644
IDC_SIZENS = 32645
IDC_SIZEALL = 32646
IDC_NO = 32648
IDC_HAND = 32649
IDC_APPSTARTING = 32650
IDC_HELP = 32651

# from winuser.h line 153
RT_CURSOR = 1
RT_BITMAP = 2
RT_ICON = 3
RT_MENU = 4
RT_DIALOG = 5
RT_STRING = 6
RT_FONTDIR = 7
RT_FONT = 8
RT_ACCELERATOR = 9
RT_RCDATA = 10
RT_MESSAGETABLE = 11
RT_GROUP_CURSOR = RT_CURSOR + DIFFERENCE
RT_GROUP_ICON = RT_ICON + DIFFERENCE
RT_VERSION = 16
RT_DLGINCLUDE = 17
RT_PLUGPLAY = 19
RT_VXD = 20
RT_ANICURSOR = 21
RT_ANIICON = 22
RT_HTML = 23
ACCESS_STICKYKEYS = 1
ACCESS_FILTERKEYS = 2
ACCESS_MOUSEKEYS = 3
# line 1291
MENULOOP_WINDOW = 0
MENULOOP_POPUP = 1

# These FILE_ATTRIBUTE_* flags  are apparently old definitions from Windows 95
# and conflict with current values above - but they live on for b/w compat...
FILE_ATTRIBUTE_ATOMIC_WRITE = 512
FILE_ATTRIBUTE_XACTION_WRITE = 1024

# Generated by h2py from \msvc20\include\winnt.h
# hacked and split by mhammond.
CONTEXT_PORTABLE_32BIT = 1048576
CONTEXT_ALPHA = 131072
PROCESSOR_INTEL_860 = 860
PROCESSOR_MIPS_R2000 = 2000
PROCESSOR_MIPS_R3000 = 3000
RTL_CRITSECT_TYPE = 0
RTL_RESOURCE_TYPE = 1
IMAGE_SIZEOF_ROM_OPTIONAL_HEADER = 56
IMAGE_SIZEOF_STD_OPTIONAL_HEADER = 28
IMAGE_SIZEOF_NT_OPTIONAL_HEADER = 224
IMAGE_SIZEOF_AUX_SYMBOL = 18
IMAGE_SIZEOF_RELOCATION = 10
IMAGE_SIZEOF_BASE_RELOCATION = 8
IMAGE_SIZEOF_LINENUMBER = 6

# Generated by h2py from \msvcnt\include\wingdi.h
# hacked and split manually by mhammond.
HS_FDIAGONAL1 = 6
HS_BDIAGONAL1 = 7
HS_SOLID = 8
HS_DENSE1 = 9
HS_DENSE2 = 10
HS_DENSE3 = 11
HS_DENSE4 = 12
HS_DENSE5 = 13
HS_DENSE6 = 14
HS_DENSE7 = 15
HS_DENSE8 = 16
HS_NOSHADE = 17
HS_HALFTONE = 18
HS_SOLIDCLR = 19
HS_DITHEREDCLR = 20
HS_SOLIDTEXTCLR = 21
HS_DITHEREDTEXTCLR = 22
HS_SOLIDBKCLR = 23
HS_DITHEREDBKCLR = 24

DIB_PAL_INDICES = 2
DIB_PAL_PHYSINDICES = 2
DIB_PAL_LOGINDICES = 4
CBM_CREATEDIB = 2

# Exception/Status codes from winuser.h and winnt.h

WAIT_FAILED = -1
WAIT_OBJECT_0 = STATUS_WAIT_0 + 0

WAIT_ABANDONED = STATUS_ABANDONED_WAIT_0 + 0
WAIT_ABANDONED_0 = STATUS_ABANDONED_WAIT_0 + 0

WAIT_TIMEOUT = STATUS_TIMEOUT
WAIT_IO_COMPLETION = STATUS_USER_APC
STILL_ACTIVE = STATUS_PENDING
EXCEPTION_ACCESS_VIOLATION = STATUS_ACCESS_VIOLATION
EXCEPTION_DATATYPE_MISALIGNMENT = STATUS_DATATYPE_MISALIGNMENT
EXCEPTION_BREAKPOINT = STATUS_BREAKPOINT
EXCEPTION_SINGLE_STEP = STATUS_SINGLE_STEP
EXCEPTION_ARRAY_BOUNDS_EXCEEDED = STATUS_ARRAY_BOUNDS_EXCEEDED
EXCEPTION_FLT_DENORMAL_OPERAND = STATUS_FLOAT_DENORMAL_OPERAND
EXCEPTION_FLT_DIVIDE_BY_ZERO = STATUS_FLOAT_DIVIDE_BY_ZERO
EXCEPTION_FLT_INEXACT_RESULT = STATUS_FLOAT_INEXACT_RESULT
EXCEPTION_FLT_INVALID_OPERATION = STATUS_FLOAT_INVALID_OPERATION
EXCEPTION_FLT_OVERFLOW = STATUS_FLOAT_OVERFLOW
EXCEPTION_FLT_STACK_CHECK = STATUS_FLOAT_STACK_CHECK
EXCEPTION_FLT_UNDERFLOW = STATUS_FLOAT_UNDERFLOW
EXCEPTION_INT_DIVIDE_BY_ZERO = STATUS_INTEGER_DIVIDE_BY_ZERO
EXCEPTION_INT_OVERFLOW = STATUS_INTEGER_OVERFLOW
EXCEPTION_PRIV_INSTRUCTION = STATUS_PRIVILEGED_INSTRUCTION
EXCEPTION_IN_PAGE_ERROR = STATUS_IN_PAGE_ERROR
EXCEPTION_ILLEGAL_INSTRUCTION = STATUS_ILLEGAL_INSTRUCTION
EXCEPTION_NONCONTINUABLE_EXCEPTION = STATUS_NONCONTINUABLE_EXCEPTION
EXCEPTION_STACK_OVERFLOW = STATUS_STACK_OVERFLOW
EXCEPTION_INVALID_DISPOSITION = STATUS_INVALID_DISPOSITION
EXCEPTION_GUARD_PAGE = STATUS_GUARD_PAGE_VIOLATION
EXCEPTION_INVALID_HANDLE = STATUS_INVALID_HANDLE
CONTROL_C_EXIT = STATUS_CONTROL_C_EXIT

DBWF_LPARAMPOINTER = 32768

FILE_BEGIN = 0
FILE_CURRENT = 1
FILE_END = 2
FILE_FLAG_WRITE_THROUGH = -2147483648
FILE_FLAG_OVERLAPPED = 1073741824
FILE_FLAG_NO_BUFFERING = 536870912
FILE_FLAG_RANDOM_ACCESS = 268435456
FILE_FLAG_SEQUENTIAL_SCAN = 134217728
FILE_FLAG_DELETE_ON_CLOSE = 67108864
FILE_FLAG_BACKUP_SEMANTICS = 33554432
FILE_FLAG_POSIX_SEMANTICS = 16777216
CREATE_NEW = 1
CREATE_ALWAYS = 2
OPEN_EXISTING = 3
OPEN_ALWAYS = 4
TRUNCATE_EXISTING = 5
PIPE_ACCESS_INBOUND = 1
PIPE_ACCESS_OUTBOUND = 2
PIPE_ACCESS_DUPLEX = 3
PIPE_CLIENT_END = 0
PIPE_SERVER_END = 1
PIPE_WAIT = 0
PIPE_NOWAIT = 1
PIPE_READMODE_BYTE = 0
PIPE_READMODE_MESSAGE = 2
PIPE_TYPE_BYTE = 0
PIPE_TYPE_MESSAGE = 4
PIPE_UNLIMITED_INSTANCES = 255
SECURITY_CONTEXT_TRACKING = 262144
SECURITY_EFFECTIVE_ONLY = 524288
SECURITY_SQOS_PRESENT = 1048576
SECURITY_VALID_SQOS_FLAGS = 2031616
DTR_CONTROL_DISABLE = 0
DTR_CONTROL_ENABLE = 1
DTR_CONTROL_HANDSHAKE = 2
RTS_CONTROL_DISABLE = 0
RTS_CONTROL_ENABLE = 1
RTS_CONTROL_HANDSHAKE = 2
RTS_CONTROL_TOGGLE = 3
GMEM_FIXED = 0
GMEM_MOVEABLE = 2
GMEM_NOCOMPACT = 16
GMEM_NODISCARD = 32
GMEM_ZEROINIT = 64
GMEM_MODIFY = 128
GMEM_DISCARDABLE = 256
GMEM_NOT_BANKED = 4096
GMEM_SHARE = 8192
GMEM_DDESHARE = 8192
GMEM_NOTIFY = 16384
GMEM_LOWER = GMEM_NOT_BANKED
GMEM_VALID_FLAGS = 32626
GMEM_INVALID_HANDLE = 32768
GHND = GMEM_MOVEABLE | GMEM_ZEROINIT
GPTR = GMEM_FIXED | GMEM_ZEROINIT
GMEM_DISCARDED = 16384
GMEM_LOCKCOUNT = 255
LMEM_FIXED = 0
LMEM_MOVEABLE = 2
LMEM_NOCOMPACT = 16
LMEM_NODISCARD = 32
LMEM_ZEROINIT = 64
LMEM_MODIFY = 128
LMEM_DISCARDABLE = 3840
LMEM_VALID_FLAGS = 3954
LMEM_INVALID_HANDLE = 32768
LHND = LMEM_MOVEABLE | LMEM_ZEROINIT
LPTR = LMEM_FIXED | LMEM_ZEROINIT
NONZEROLHND = LMEM_MOVEABLE
NONZEROLPTR = LMEM_FIXED
LMEM_DISCARDED = 16384
LMEM_LOCKCOUNT = 255
DEBUG_PROCESS = 1
DEBUG_ONLY_THIS_PROCESS = 2
CREATE_SUSPENDED = 4
DETACHED_PROCESS = 8
CREATE_NEW_CONSOLE = 16
NORMAL_PRIORITY_CLASS = 32
IDLE_PRIORITY_CLASS = 64
HIGH_PRIORITY_CLASS = 128
REALTIME_PRIORITY_CLASS = 256
CREATE_NEW_PROCESS_GROUP = 512
CREATE_UNICODE_ENVIRONMENT = 1024
CREATE_SEPARATE_WOW_VDM = 2048
CREATE_SHARED_WOW_VDM = 4096
CREATE_DEFAULT_ERROR_MODE = 67108864
CREATE_NO_WINDOW = 134217728
PROFILE_USER = 268435456
PROFILE_KERNEL = 536870912
PROFILE_SERVER = 1073741824
THREAD_PRIORITY_LOWEST = THREAD_BASE_PRIORITY_MIN
THREAD_PRIORITY_BELOW_NORMAL = THREAD_PRIORITY_LOWEST + 1
THREAD_PRIORITY_HIGHEST = THREAD_BASE_PRIORITY_MAX
THREAD_PRIORITY_ABOVE_NORMAL = THREAD_PRIORITY_HIGHEST - 1
THREAD_PRIORITY_ERROR_RETURN = MAXLONG
THREAD_PRIORITY_TIME_CRITICAL = THREAD_BASE_PRIORITY_LOWRT
THREAD_PRIORITY_IDLE = THREAD_BASE_PRIORITY_IDLE
THREAD_PRIORITY_NORMAL = 0
THREAD_MODE_BACKGROUND_BEGIN = 0x00010000
THREAD_MODE_BACKGROUND_END = 0x00020000

EXCEPTION_DEBUG_EVENT = 1
CREATE_THREAD_DEBUG_EVENT = 2
CREATE_PROCESS_DEBUG_EVENT = 3
EXIT_THREAD_DEBUG_EVENT = 4
EXIT_PROCESS_DEBUG_EVENT = 5
LOAD_DLL_DEBUG_EVENT = 6
UNLOAD_DLL_DEBUG_EVENT = 7
OUTPUT_DEBUG_STRING_EVENT = 8
RIP_EVENT = 9
DRIVE_UNKNOWN = 0
DRIVE_NO_ROOT_DIR = 1
DRIVE_REMOVABLE = 2
DRIVE_FIXED = 3
DRIVE_REMOTE = 4
DRIVE_CDROM = 5
DRIVE_RAMDISK = 6
FILE_TYPE_UNKNOWN = 0
FILE_TYPE_DISK = 1
FILE_TYPE_CHAR = 2
FILE_TYPE_PIPE = 3
FILE_TYPE_REMOTE = 32768
NOPARITY = 0
ODDPARITY = 1
EVENPARITY = 2
MARKPARITY = 3
SPACEPARITY = 4
ONESTOPBIT = 0
ONE5STOPBITS = 1
TWOSTOPBITS = 2
CBR_110 = 110
CBR_300 = 300
CBR_600 = 600
CBR_1200 = 1200
CBR_2400 = 2400
CBR_4800 = 4800
CBR_9600 = 9600
CBR_14400 = 14400
CBR_19200 = 19200
CBR_38400 = 38400
CBR_56000 = 56000
CBR_57600 = 57600
CBR_115200 = 115200
CBR_128000 = 128000
CBR_256000 = 256000
S_QUEUEEMPTY = 0
S_THRESHOLD = 1
S_ALLTHRESHOLD = 2
S_NORMAL = 0
S_LEGATO = 1
S_STACCATO = 2
NMPWAIT_WAIT_FOREVER = -1
NMPWAIT_NOWAIT = 1
NMPWAIT_USE_DEFAULT_WAIT = 0
OF_READ = 0
OF_WRITE = 1
OF_READWRITE = 2
OF_SHARE_COMPAT = 0
OF_SHARE_EXCLUSIVE = 16
OF_SHARE_DENY_WRITE = 32
OF_SHARE_DENY_READ = 48
OF_SHARE_DENY_NONE = 64
OF_PARSE = 256
OF_DELETE = 512
OF_VERIFY = 1024
OF_CANCEL = 2048
OF_CREATE = 4096
OF_PROMPT = 8192
OF_EXIST = 16384
OF_REOPEN = 32768
OFS_MAXPATHNAME = 128
MAXINTATOM = 49152

# winbase.h
PROCESS_HEAP_REGION = 1
PROCESS_HEAP_UNCOMMITTED_RANGE = 2
PROCESS_HEAP_ENTRY_BUSY = 4
PROCESS_HEAP_ENTRY_MOVEABLE = 16
PROCESS_HEAP_ENTRY_DDESHARE = 32
SCS_32BIT_BINARY = 0
SCS_DOS_BINARY = 1
SCS_WOW_BINARY = 2
SCS_PIF_BINARY = 3
SCS_POSIX_BINARY = 4
SCS_OS216_BINARY = 5
SEM_FAILCRITICALERRORS = 1
SEM_NOGPFAULTERRORBOX = 2
SEM_NOALIGNMENTFAULTEXCEPT = 4
SEM_NOOPENFILEERRORBOX = 32768
LOCKFILE_FAIL_IMMEDIATELY = 1
LOCKFILE_EXCLUSIVE_LOCK = 2
HANDLE_FLAG_INHERIT = 1
HANDLE_FLAG_PROTECT_FROM_CLOSE = 2
HINSTANCE_ERROR = 32
GET_TAPE_MEDIA_INFORMATION = 0
GET_TAPE_DRIVE_INFORMATION = 1
SET_TAPE_MEDIA_INFORMATION = 0
SET_TAPE_DRIVE_INFORMATION = 1
FORMAT_MESSAGE_ALLOCATE_BUFFER = 256
FORMAT_MESSAGE_IGNORE_INSERTS = 512
FORMAT_MESSAGE_FROM_STRING = 1024
FORMAT_MESSAGE_FROM_HMODULE = 2048
FORMAT_MESSAGE_FROM_SYSTEM = 4096
FORMAT_MESSAGE_ARGUMENT_ARRAY = 8192
FORMAT_MESSAGE_MAX_WIDTH_MASK = 255
BACKUP_INVALID = 0
BACKUP_DATA = 1
BACKUP_EA_DATA = 2
BACKUP_SECURITY_DATA = 3
BACKUP_ALTERNATE_DATA = 4
BACKUP_LINK = 5
BACKUP_PROPERTY_DATA = 6
BACKUP_OBJECT_ID = 7
BACKUP_REPARSE_DATA = 8
BACKUP_SPARSE_BLOCK = 9

STREAM_NORMAL_ATTRIBUTE = 0
STREAM_MODIFIED_WHEN_READ = 1
STREAM_CONTAINS_SECURITY = 2
STREAM_CONTAINS_PROPERTIES = 4
STARTF_USESHOWWINDOW = 1
STARTF_USESIZE = 2
STARTF_USEPOSITION = 4
STARTF_USECOUNTCHARS = 8
STARTF_USEFILLATTRIBUTE = 16
STARTF_FORCEONFEEDBACK = 64
STARTF_FORCEOFFFEEDBACK = 128
STARTF_USESTDHANDLES = 256
STARTF_USEHOTKEY = 512
SHUTDOWN_NORETRY = 1
DONT_RESOLVE_DLL_REFERENCES = 1
LOAD_LIBRARY_AS_DATAFILE = 2
LOAD_WITH_ALTERED_SEARCH_PATH = 8
DDD_RAW_TARGET_PATH = 1
DDD_REMOVE_DEFINITION = 2
DDD_EXACT_MATCH_ON_REMOVE = 4
MOVEFILE_REPLACE_EXISTING = 1
MOVEFILE_COPY_ALLOWED = 2
MOVEFILE_DELAY_UNTIL_REBOOT = 4
MAX_COMPUTERNAME_LENGTH = 15
LOGON32_LOGON_INTERACTIVE = 2
LOGON32_LOGON_NETWORK = 3
LOGON32_LOGON_BATCH = 4
LOGON32_LOGON_SERVICE = 5
LOGON32_LOGON_UNLOCK = 7
LOGON32_LOGON_NETWORK_CLEARTEXT = 8
LOGON32_LOGON_NEW_CREDENTIALS = 9
LOGON32_PROVIDER_DEFAULT = 0
LOGON32_PROVIDER_WINNT35 = 1
LOGON32_PROVIDER_WINNT40 = 2
LOGON32_PROVIDER_WINNT50 = 3
TC_NORMAL = 0
TC_HARDERR = 1
TC_GP_TRAP = 2
TC_SIGNAL = 3
AC_LINE_OFFLINE = 0
AC_LINE_ONLINE = 1
AC_LINE_BACKUP_POWER = 2
AC_LINE_UNKNOWN = 255
BATTERY_FLAG_HIGH = 1
BATTERY_FLAG_LOW = 2
BATTERY_FLAG_CRITICAL = 4
BATTERY_FLAG_CHARGING = 8
BATTERY_FLAG_NO_BATTERY = 128
BATTERY_FLAG_UNKNOWN = 255
BATTERY_PERCENTAGE_UNKNOWN = 255
BATTERY_LIFE_UNKNOWN = -1

# GetUserNameEx/GetComputerNameEx
NameUnknown = 0
NameFullyQualifiedDN = 1
NameSamCompatible = 2
NameDisplay = 3
NameUniqueId = 6
NameCanonical = 7
NameUserPrincipal = 8
NameCanonicalEx = 9
NameServicePrincipal = 10
NameDnsDomain = 12

ComputerNameNetBIOS = 0
ComputerNameDnsHostname = 1
ComputerNameDnsDomain = 2
ComputerNameDnsFullyQualified = 3
ComputerNamePhysicalNetBIOS = 4
ComputerNamePhysicalDnsHostname = 5
ComputerNamePhysicalDnsDomain = 6
ComputerNamePhysicalDnsFullyQualified = 7

## flags used with Get/SetSystemFileCacheSize
MM_WORKING_SET_MAX_HARD_ENABLE = 1
MM_WORKING_SET_MAX_HARD_DISABLE = 2
MM_WORKING_SET_MIN_HARD_ENABLE = 4
MM_WORKING_SET_MIN_HARD_DISABLE = 8

## Flags for GetFinalPathNameByHandle
VOLUME_NAME_DOS = 0
VOLUME_NAME_GUID = 1
VOLUME_NAME_NT = 2
VOLUME_NAME_NONE = 4
FILE_NAME_NORMALIZED = 0
FILE_NAME_OPENED = 8
