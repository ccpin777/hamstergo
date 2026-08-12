from __future__ import annotations

import functools
import http.server
import json
import os
import sys
import tempfile
import threading
from pathlib import Path

import webview


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
        "",
        url,
        width=520,
        height=860,
        min_size=(360, 600),
        resizable=True,
        text_select=False,
        js_api=preferences_api,
    )

    try:
        webview.start()
    finally:
        server.shutdown()
        server.server_close()


if __name__ == "__main__":
    main()
