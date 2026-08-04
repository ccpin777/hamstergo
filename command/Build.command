#!/bin/zsh
# Build HamsterGo.app on macOS.
set -euo pipefail

SCRIPT_DIR=$(cd "$(dirname "$0")" && pwd)
PROJECT_DIR=$(cd "$SCRIPT_DIR/.." && pwd)
cd "$PROJECT_DIR"

pause() {
    if [[ -t 0 ]]; then
        read -r "?Press Return to close..."
    fi
}

fail() {
    echo ""
    echo "Build failed: $1"
    pause
    exit 1
}

cleanup_success() {
    echo "Cleaning successful-build artifacts..."
    rm -rf "$BUILD_VENV" "$BUILD_DIR/pyinstaller" "$ICONSET" "$ICON_ICNS"
    rmdir "$BUILD_DIR" 2>/dev/null || true
}

if [[ "$(uname -s)" != "Darwin" ]]; then
    fail "HamsterGo.app must be built on macOS."
fi

PYTHON_BIN="${PYTHON_BIN:-python3}"
BUILD_VENV="$PROJECT_DIR/BuildVenv"
BUILD_DIR="$PROJECT_DIR/build"
DIST_DIR="$PROJECT_DIR/dist"
ICONSET="$BUILD_DIR/hamstergo.iconset"
ICON_ICNS="$BUILD_DIR/hamstergo.icns"

[[ -f "$PROJECT_DIR/app.py" ]] || fail "Missing app.py"
[[ -f "$PROJECT_DIR/HamsterGo.spec" ]] || fail "Missing HamsterGo.spec"
[[ -f "$PROJECT_DIR/resources/icon-512.png" ]] || fail "Missing resources/icon-512.png"

mkdir -p "$BUILD_DIR" "$DIST_DIR"

echo "Preparing isolated build environment..."
"$PYTHON_BIN" -m venv "$BUILD_VENV"
"$BUILD_VENV/bin/python" -m pip install --upgrade pip setuptools wheel
"$BUILD_VENV/bin/python" -m pip install pywebview pyinstaller

echo "Preparing app icon..."
rm -rf "$ICONSET"
mkdir -p "$ICONSET"
sips -z 16 16 "$PROJECT_DIR/resources/icon-512.png" --out "$ICONSET/icon_16x16.png" >/dev/null
sips -z 32 32 "$PROJECT_DIR/resources/icon-512.png" --out "$ICONSET/icon_16x16@2x.png" >/dev/null
sips -z 32 32 "$PROJECT_DIR/resources/icon-512.png" --out "$ICONSET/icon_32x32.png" >/dev/null
sips -z 64 64 "$PROJECT_DIR/resources/icon-512.png" --out "$ICONSET/icon_32x32@2x.png" >/dev/null
sips -z 128 128 "$PROJECT_DIR/resources/icon-512.png" --out "$ICONSET/icon_128x128.png" >/dev/null
sips -z 256 256 "$PROJECT_DIR/resources/icon-512.png" --out "$ICONSET/icon_128x128@2x.png" >/dev/null
sips -z 256 256 "$PROJECT_DIR/resources/icon-512.png" --out "$ICONSET/icon_256x256.png" >/dev/null
sips -z 512 512 "$PROJECT_DIR/resources/icon-512.png" --out "$ICONSET/icon_256x256@2x.png" >/dev/null
sips -z 512 512 "$PROJECT_DIR/resources/icon-512.png" --out "$ICONSET/icon_512x512.png" >/dev/null
sips -z 1024 1024 "$PROJECT_DIR/resources/icon-512.png" --out "$ICONSET/icon_512x512@2x.png" >/dev/null
iconutil -c icns "$ICONSET" -o "$ICON_ICNS"

echo "Cleaning previous output..."
rm -rf "$BUILD_DIR/pyinstaller" "$DIST_DIR/HamsterGo" "$DIST_DIR/HamsterGo.app"

echo "Building HamsterGo.app..."
"$BUILD_VENV/bin/python" -m PyInstaller     --noconfirm     --clean     --distpath "$DIST_DIR"     --workpath "$BUILD_DIR/pyinstaller"     "$PROJECT_DIR/HamsterGo.spec"

APP_PATH="$DIST_DIR/HamsterGo.app"
[[ -d "$APP_PATH" ]] || fail "PyInstaller did not create $APP_PATH"

find "$APP_PATH" -name ".DS_Store" -delete
find "$APP_PATH" -type d -name "__pycache__" -prune -exec rm -rf {} +

if command -v codesign >/dev/null 2>&1; then
    codesign --force --deep --sign - "$APP_PATH"
fi

echo ""
echo "Built: $APP_PATH"
cleanup_success
pause
