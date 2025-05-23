# Cross-Platform Clipboard Manager

A modern clipboard management application that works across macOS, Windows, and Linux.

## Features

- Global hotkey support for quick access
- History of clipboard entries
- Search through clipboard history
- Cross-platform support (macOS, Windows, Linux)
- System tray integration
- Keyboard shortcuts

## Installation

### macOS

1. Download the latest .dmg file from releases
2. Mount the .dmg file
3. Drag the application to your Applications folder

### Windows

#### **Building on Windows (Recommended)**

1. **Clone the repository** to your Windows machine.
2. **Install Python 3.9+** from [python.org](https://www.python.org/downloads/windows/).
3. **Open Command Prompt** and set up a virtual environment:
   ```sh
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   ```
4. **Run the build script:**
   ```sh
   python build.py
   ```
5. **Find your executable in the `build/ClipboardManager/` folder.**
   - A portable ZIP and installer (if Inno Setup is installed) will also be created.

#### **Creating an Installer (Optional)**

- [Download and install Inno Setup](https://jrsoftware.org/isdl.php)
- The build script will automatically use it if available.

#### **Alternative: GitHub Actions (Cloud Build)**

- You can set up GitHub Actions to build Windows executables in the cloud.
- Example workflow:

```yaml
name: Build Windows Executable
on:
  push:
    branches: [main]
  workflow_dispatch:
jobs:
  build-windows:
    runs-on: windows-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: "3.9"
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          pip install pyinstaller
      - name: Build with PyInstaller
        run: |
          python build.py
      - name: Upload Artifacts
        uses: actions/upload-artifact@v3
        with:
          name: windows-build
          path: build/
```

- After the workflow runs, download the artifacts from the GitHub Actions page.

### Linux

1. Download the latest .deb package from releases
2. Install using: `sudo dpkg -i clipboard-manager.deb`

## Development Setup

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the application:
   ```bash
   python src/main.py
   ```

## Building from Source

### macOS

```bash
pyinstaller --windowed --name "Clipboard Manager" --icon=assets/icon.icns src/main.py
```

### Windows

```bash
pyinstaller --windowed --name "Clipboard Manager" --icon=assets/icon.ico src/main.py
```

### Linux

```bash
pyinstaller --windowed --name "clipboard-manager" --icon=assets/icon.png src/main.py
```

## License

MIT License
