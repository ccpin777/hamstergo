from __future__ import annotations

import functools
import http.server
import sys
import threading
from pathlib import Path

import webview


class QuietRequestHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format: str, *args: object) -> None:
        return


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
    window = webview.create_window(
        "HamsterGo · 倉鼠打包小幫手",
        url,
        width=520,
        height=860,
        min_size=(360, 600),
        resizable=True,
        text_select=False,
    )

    try:
        webview.start()
    finally:
        server.shutdown()
        server.server_close()


if __name__ == "__main__":
    main()
