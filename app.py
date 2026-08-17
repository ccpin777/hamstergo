from __future__ import annotations

import functools
import http.server
import json
import os
import platform
import sys
import tempfile
import threading
from pathlib import Path

import webview


_menu_main_thread_target = None


def remove_default_macos_about_menu() -> None:
    """Remove only macOS's standard About action from the application menu."""
    if platform.system() != "Darwin":
        return
    try:
        from AppKit import NSApp

        main_menu = NSApp.mainMenu()
        if main_menu is None or main_menu.numberOfItems() == 0:
            return
        app_menu = main_menu.itemAtIndex_(0).submenu()
        if app_menu is None:
            return
        for index in range(app_menu.numberOfItems() - 1, -1, -1):
            item = app_menu.itemAtIndex_(index)
            if str(item.action()) == "orderFrontStandardAboutPanel:":
                app_menu.removeItemAtIndex_(index)
    except Exception:
        return


class QuietRequestHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format: str, *args: object) -> None:
        return


class PreferencesAPI:
    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._path = Path.home() / "Library" / "Application Support" / "HamsterGo" / "preferences.json"

    def load_preferences(self) -> dict[str, str]:
        try:
            with self._lock, self._path.open("r", encoding="utf-8") as f:
                value = json.load(f)
            return value if isinstance(value, dict) else {}
        except (FileNotFoundError, OSError, json.JSONDecodeError):
            return {}

    def save_preferences(self, preferences: dict[str, str]) -> bool:
        allowed = {"syncEndpoint", "syncKey", "syncEncryptionPassword", "fontScale", "fontFamily"}
        clean = {k: str(v) for k, v in preferences.items() if k in allowed and isinstance(v, (str, int, float))}
        try:
            with self._lock:
                self._path.parent.mkdir(parents=True, exist_ok=True)
                fd, tmp = tempfile.mkstemp(prefix="preferences.", suffix=".tmp", dir=self._path.parent)
                try:
                    with os.fdopen(fd, "w", encoding="utf-8") as f:
                        json.dump(clean, f, ensure_ascii=False, indent=2)
                        f.write("\n")
                    os.chmod(tmp, 0o600)
                    os.replace(tmp, self._path)
                finally:
                    try: os.unlink(tmp)
                    except FileNotFoundError: pass
            return True
        except OSError:
            return False


def app_directory() -> Path:
    source_dir = Path(__file__).resolve().parent
    candidates = [source_dir]
    if getattr(sys, "frozen", False):
        candidates.insert(0, Path(getattr(sys, "_MEIPASS")))
    for candidate in candidates:
        if (candidate / "index.html").exists():
            return candidate
    return candidates[0]


def main() -> None:
    root = app_directory()
    handler = functools.partial(
        QuietRequestHandler,
        directory=str(root),
    )
    server = http.server.ThreadingHTTPServer(("127.0.0.1", 8765), handler)
    server_thread = threading.Thread(target=server.serve_forever, daemon=True)
    server_thread.start()

    url = f"http://127.0.0.1:{server.server_address[1]}/index.html"
    preferences_api = PreferencesAPI()
    window = webview.create_window(
        "HamsterGo",
        url,
        width=520,
        height=860,
        min_size=(360, 600),
        resizable=True,
        text_select=False,
        js_api=preferences_api,
    )

    def schedule_remove_default_macos_about_menu() -> None:
        global _menu_main_thread_target
        if platform.system() != "Darwin":
            return
        from Foundation import NSObject

        if _menu_main_thread_target is None:
            class MenuMainThreadTarget(NSObject):
                def removeDefaultAbout_(self, sender):
                    remove_default_macos_about_menu()

            _menu_main_thread_target = MenuMainThreadTarget.alloc().init()
        _menu_main_thread_target.performSelectorOnMainThread_withObject_waitUntilDone_(
            "removeDefaultAbout:", None, False
        )

    def show_about() -> None:
        schedule_remove_default_macos_about_menu()
        if window is not None:
            window.evaluate_js("if (typeof openAboutModal === 'function') { openAboutModal(); }")

    from webview.menu import Menu, MenuAction
    if platform.system() == "Darwin":
        webview.settings["SHOW_DEFAULT_MENUS"] = False
        app_menu = [Menu("__app__", [MenuAction("關於 HamsterGo", show_about)])]
    else:
        app_menu = [Menu("Help", [MenuAction("About HamsterGo", show_about)])]

    def prepare_window() -> None:
        schedule_remove_default_macos_about_menu()

    window.events.before_show += prepare_window
    window.events.shown += lambda: schedule_remove_default_macos_about_menu()

    try:
        webview.start(menu=app_menu)
    finally:
        server.shutdown()
        server.server_close()


if __name__ == "__main__":
    main()
