
from ctypes.wintypes import *
import ctypes  # py2


HWND_TOPMOST = -1
HWND_NOTOPMOST = -2

SWP_NOMOVE = 1
SWP_NOSIZE = 2

FM_GETFOCUS = 0x600

PM_REMOVE = 0x1

WH_KEYBOARD_LL = 13

WM_COPYDATA = 0x4A
WM_KEYUP = 0x101
WM_SYSKEYUP = 0x105
WM_KEYDOWN = 0x100
WM_SYSKEYDOWN = 0x104

PVOID = ctypes.c_char_p
ULONG_PTR = LPARAM

LRESULT = LPARAM
LPDWORD = PDWORD = ctypes.POINTER(DWORD)
LPWSTR = ctypes.c_wchar_p
LPCWSTR = ctypes.c_wchar_p

HOOKPROC = ctypes.WINFUNCTYPE(LRESULT, ctypes.c_int, WPARAM, LPARAM)
WNDENUMPROC = ctypes.WINFUNCTYPE(BOOL, HWND, LPARAM)

if 'LPMSG' not in dir():  # py2
    LPMSG = ctypes.POINTER(MSG)


class COPYDATA(ctypes.Structure):
    _fields_ = [('dwData', ULONG_PTR),
                ('cbData', DWORD),
                ('lpData', PVOID)]

    @property
    def pointer(self):
        return ctypes.byref(self)


class KBDLLHOOK(ctypes.Structure):
    _fields_ = [('vkCode', DWORD),
                ('scanCode', DWORD),
                ('flags', DWORD),
                ('time', DWORD),
                ('dwExtraInfo', ULONG_PTR)]


CallNextHookEx = ctypes.windll.user32.CallNextHookEx
CallNextHookEx.restype = LRESULT
CallNextHookEx.argtypes = (HHOOK,   # _In_ idHook
                           INT,   # _In_ nCode
                           WPARAM,  # _In_ wParam
                           LPARAM)  # _In_ lParam

DispatchMessage = ctypes.windll.user32.DispatchMessageW
DispatchMessage.restype = LRESULT
DispatchMessage.argtypes = (LPMSG,)  # _In_ lpmsg

EnumWindows = ctypes.windll.user32.EnumWindows
EnumWindows.restype = BOOL
EnumWindows.argtypes = (WNDENUMPROC,  # _In_ lpEnumFunc
                        LPARAM)       # _In_ lParam

FindWindow = ctypes.windll.user32.FindWindowW
FindWindow.restype = HWND
FindWindow.argtypes = (LPCWSTR,  # _In_opt_ lpClassName
                       LPCWSTR)  # _In_opt_ lpWindowName

GetClassName = ctypes.windll.user32.GetClassNameW
GetClassName.restype = INT
GetClassName.argtypes = (HWND,    # _In_ HWND
                         LPWSTR,  # _Out_ lpClassName
                         INT)   # _In_ nMaxCount

GetCurrentProcessId = ctypes.windll.kernel32.GetCurrentProcessId
GetCurrentProcessId.restype = DWORD

GetCurrentThreadId = ctypes.windll.kernel32.GetCurrentThreadId
GetCurrentThreadId.restype = DWORD

GetForegroundWindow = ctypes.windll.user32.GetForegroundWindow
GetForegroundWindow.restype = HWND

GetLastError = ctypes.windll.kernel32.GetLastError
GetLastError.restype = DWORD

GetMessage = ctypes.windll.user32.GetMessageW
GetMessage.restype = BOOL
GetMessage.argtypes = (LPMSG,   # _Out_ lpMsg
                       HWND,    # _In_opt_ hWnd
                       UINT,  # _In_ wMsgFilterMin
                       UINT)  # _In_ wMsgFilterMax

GetModuleHandle = ctypes.windll.kernel32.GetModuleHandleW
GetModuleHandle.restype = HMODULE
GetModuleHandle.argtypes = (LPCWSTR,)  # _In_opt_ lpModuleName

GetWindowThreadProcessId = ctypes.windll.user32.GetWindowThreadProcessId
GetWindowThreadProcessId.restype = DWORD
GetWindowThreadProcessId.argtypes = (HWND,     # _In_ hWnd
                                     LPDWORD)  # _Out_opt_ lpdwProcessId

IsWindowVisible = ctypes.windll.user32.IsWindowVisible
IsWindowVisible.restype = BOOL
IsWindowVisible.argtypes = (HWND,)  # _In_ hWnd

MessageBox = ctypes.windll.user32.MessageBoxW
MessageBox.restype = INT
MessageBox.argtypes = (HWND,     # _In_opt_ hWnd
                       LPCWSTR,  # _In_opt_ lpText
                       LPCWSTR,  # _In_opt_ lpCaption
                       UINT)     # _In_ uType

PeekMessage = ctypes.windll.user32.PeekMessageW
PeekMessage.restype = BOOL
PeekMessage.argtypes = (LPMSG,  # _Out_ lpMsg
                        HWND,   # _In_opt_ hWnd
                        UINT,   # _In_ wMsgFilterMin
                        UINT,   # _In_ wMsgFilterMax
                        UINT)   # _In_ wRemoveMsg

SendMessage = ctypes.windll.user32.SendMessageW
SendMessage.restype = LRESULT
SendMessage.argtypes = (HWND,             # _In_ hWnd
                        UINT,             # _In_ Msg
                        WPARAM,           # _In_ wParam
                        ctypes.c_void_p)  # _In_ lParam

SetLastError = ctypes.windll.kernel32.SetLastError
SetLastError.argtypes = (DWORD,)  # _In_ dwErrCode

SetWindowsHookEx = ctypes.windll.user32.SetWindowsHookExW
SetWindowsHookEx.restype = HHOOK
SetWindowsHookEx.argtpes = (INT,        # _In_ idHook
                            HOOKPROC,   # _In_ lpfn
                            HINSTANCE,  # _In_ hMod
                            DWORD)      # _In_ dwThreadId

SetWindowPos = ctypes.windll.user32.SetWindowPos
SetWindowPos.restype = BOOL
SetWindowPos.argtypes = (HWND,  # _In_ hWnd
                         HWND,  # _In_opt hWndInsertAfter
                         INT,   # _In_ X
                         INT,   # _In_ Y
                         INT,   # _In_ cx
                         INT,   # _In_ cy
                         UINT)  # _In_ uFlags

TranslateMessage = ctypes.windll.user32.TranslateMessage
TranslateMessage.restype = BOOL
TranslateMessage.argtypes = (LPMSG,)  # _In_ lpMsg

UnhookWindowsHookEx = ctypes.windll.user32.UnhookWindowsHookEx
UnhookWindowsHookEx.restype = BOOL
UnhookWindowsHookEx.argtypes = (HHOOK,)  # _In_ hhk
