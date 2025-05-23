import os
import platform
import subprocess
import shutil
import zipfile
import sys

def run_command(cmd, error_msg="Command failed"):
    """Run a command and handle errors."""
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Error: {error_msg}")
            print(f"Command output: {result.stdout}")
            print(f"Error output: {result.stderr}")
            sys.exit(1)
        return result
    except Exception as e:
        print(f"Error: {error_msg}")
        print(f"Exception: {str(e)}")
        sys.exit(1)

def create_windows_installer():
    """Create a Windows installer using Inno Setup."""
    # Create Inno Setup script
    inno_script = """
[Setup]
AppName=Clipboard Manager
AppVersion=1.0
DefaultDirName={autopf}\\ClipboardManager
DefaultGroupName=Clipboard Manager
OutputDir=build
OutputBaseFilename=ClipboardManager-Setup
Compression=lzma
SolidCompression=yes
PrivilegesRequired=admin

[Files]
Source: "build\\ClipboardManager\\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs

[Icons]
Name: "{group}\\Clipboard Manager"; Filename: "{app}\\ClipboardManager.exe"
Name: "{commondesktop}\\Clipboard Manager"; Filename: "{app}\\ClipboardManager.exe"

[Run]
Filename: "{app}\\ClipboardManager.exe"; Description: "Launch Clipboard Manager"; Flags: postinstall nowait
"""
    
    # Write the script to a file
    with open('installer.iss', 'w') as f:
        f.write(inno_script)
    
    # Run Inno Setup Compiler
    run_command(['iscc', 'installer.iss'], "Failed to create Windows installer")
    
    # Clean up
    os.remove('installer.iss')

def create_portable_zip():
    """Create a portable ZIP package for Windows."""
    zip_path = 'build/ClipboardManager-Portable.zip'
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk('build/ClipboardManager'):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, 'build/ClipboardManager')
                zipf.write(file_path, arcname)

def build_application():
    system = platform.system().lower()
    print(f"Building for platform: {system}")
    
    # Create build directory
    if os.path.exists('build'):
        print("Removing existing build directory...")
        shutil.rmtree('build')
    os.makedirs('build')
    print("Created build directory")
    
    # Install PyInstaller if not already installed
    print("Installing PyInstaller...")
    run_command(['pip', 'install', 'pyinstaller'], "Failed to install PyInstaller")
    
    # Build command based on platform
    if system == 'darwin':
        cmd = [
            'pyinstaller',
            '--windowed',
            '--name=ClipboardManager',
            '--icon=assets/icon.icns',
            '--add-data=assets:assets',
            'src/main.py'
        ]
    elif system == 'windows':
        cmd = [
            'pyinstaller',
            '--windowed',
            '--name=ClipboardManager',
            '--icon=assets/icon.ico',
            '--add-data=assets;assets',
            '--noconfirm',  # Don't ask for confirmation
            '--clean',      # Clean PyInstaller cache
            'src/main.py'
        ]
    else:  # Linux
        cmd = [
            'pyinstaller',
            '--windowed',
            '--name=clipboard-manager',
            '--icon=assets/icon.png',
            '--add-data=assets:assets',
            'src/main.py'
        ]
    
    print("Running PyInstaller...")
    print(f"Command: {' '.join(cmd)}")
    run_command(cmd, "PyInstaller build failed")
    
    # Verify the build output exists
    if system == 'darwin':
        if not os.path.exists('dist/ClipboardManager.app'):
            print("Error: dist/ClipboardManager.app not found")
            sys.exit(1)
        shutil.move('dist/ClipboardManager.app', 'build/')
    elif system == 'windows':
        if not os.path.exists('dist/ClipboardManager'):
            print("Error: dist/ClipboardManager not found")
            sys.exit(1)
        shutil.move('dist/ClipboardManager', 'build/')
        # Create Windows installer and portable package
        try:
            create_windows_installer()
        except FileNotFoundError:
            print("Inno Setup not found. Skipping installer creation.")
            print("To create an installer, install Inno Setup from: https://jrsoftware.org/isdl.php")
        create_portable_zip()
    else:
        if not os.path.exists('dist/clipboard-manager'):
            print("Error: dist/clipboard-manager not found")
            sys.exit(1)
        shutil.move('dist/clipboard-manager', 'build/')
    
    # Clean up PyInstaller files
    print("Cleaning up...")
    shutil.rmtree('dist')
    if os.path.exists('ClipboardManager.spec'):
        os.remove('ClipboardManager.spec')
    
    print(f"Build completed successfully! Output is in the 'build' directory.")
    if system == 'windows':
        print("\nCreated files:")
        print("1. build/ClipboardManager/ClipboardManager.exe (Executable)")
        print("2. build/ClipboardManager-Portable.zip (Portable package)")
        if os.path.exists('build/ClipboardManager-Setup.exe'):
            print("3. build/ClipboardManager-Setup.exe (Installer)")

if __name__ == '__main__':
    build_application() 