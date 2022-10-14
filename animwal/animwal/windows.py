# coding: utf-8

from ctypes import (
    windll, wintypes,
    POINTER, WINFUNCTYPE
)

user32 = windll.user32
wintypes.PDWORD_PTR = POINTER(wintypes.DWORD)

WNDENUMPROC = WINFUNCTYPE(
    wintypes.BOOL,
    wintypes.HWND,        # _In_ hWnd
    wintypes.LPARAM,)     # _In_ lParam

user32.EnumWindows.argtypes = (
   WNDENUMPROC,           # _In_ lpEnumFunc
   wintypes.LPARAM,)      # _In_ lParam

user32.FindWindowW.argtypes = (
    wintypes.LPCWSTR,     # _In_ lpClassName
    wintypes.LPCWSTR,)    # _In_ lpWindowName

user32.FindWindowExW.argtypes = (
    wintypes.HWND,        # _In_ hWndParent
    wintypes.HWND,        # _In_ hWndChildAfter
    wintypes.LPCWSTR,     # _In_ lpszClass
    wintypes.LPCWSTR,)    # _In_ lpszWindow

user32.SendMessageTimeoutW.argtypes = (
    wintypes.HWND,        # _In_ hWnd
    wintypes.UINT,        # _In_ Msg
    wintypes.WPARAM,      # _In_ wParam
    wintypes.LPARAM,      # _In_ lParam
    wintypes.UINT,        # _In_ fuFlags
    wintypes.UINT,        # _In_ uTimeout
    wintypes.PDWORD_PTR,) # _In_ lpdwResult

def get_handle():
    ret_hwnd = None

    user32.SendMessageTimeoutW(
        user32.FindWindowW('Progman', None),
        0x052C, 0, 0,
        0, # SMTO_NORMAL
        1000, POINTER(wintypes.DWORD)()
    ) # directs Progman to spawn a WorkerW

    @WNDENUMPROC
    def callback(hwnd, lParam):
        if user32.FindWindowExW(hwnd, None, 'SHELLDLL_DefView', None):
            nonlocal ret_hwnd
            ret_hwnd = user32.FindWindowExW(None, hwnd, 'WorkerW', None)

        return True

    user32.EnumWindows(callback, 0)
    return ret_hwnd