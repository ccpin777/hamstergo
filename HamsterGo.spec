# -*- mode: python ; coding: utf-8 -*-

from pathlib import Path

from PyInstaller.utils.hooks import collect_all


project_dir = Path.cwd()
webview_datas, webview_binaries, webview_hiddenimports = collect_all("webview")

datas = [
    (str(project_dir / "index.html"), "."),
    (str(project_dir / "manifest.json"), "."),
    (str(project_dir / "service-worker.js"), "."),
    (str(project_dir / "resources"), "resources"),
]
datas += webview_datas

a = Analysis(
    [str(project_dir / "app.py")],
    pathex=[str(project_dir)],
    binaries=webview_binaries,
    datas=datas,
    hiddenimports=webview_hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=["pytest", "IPython", "jupyter", "notebook", "tkinter"],
    noarchive=False,
    optimize=1,
)

pyz = PYZ(a.pure, a.zipped_data)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="HamsterGo",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name="HamsterGo",
)

app = BUNDLE(
    coll,
    name="HamsterGo.app",
    icon=str(project_dir / "build" / "hamstergo.icns"),
    bundle_identifier="com.hamstergo.app",
)
