import platform
import os
import sys

def get_platform():
    """Returns the current platform name."""
    return platform.system().lower()

def get_config_dir():
    """Returns the appropriate configuration directory for the current platform."""
    system = get_platform()
    
    if system == 'darwin':  # macOS
        return os.path.expanduser('~/Library/Application Support/ClipboardManager')
    elif system == 'windows':
        return os.path.join(os.environ['APPDATA'], 'ClipboardManager')
    else:  # Linux and others
        return os.path.expanduser('~/.config/clipboard-manager')

def get_icon_path():
    """Returns the appropriate icon path based on the platform."""
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    assets_dir = os.path.join(base_dir, 'assets')
    
    if sys.platform == 'darwin':  # macOS
        return os.path.join(assets_dir, 'icon.icns')
    elif sys.platform == 'win32':  # Windows
        return os.path.join(assets_dir, 'icon.ico')
    else:  # Linux and others
        return os.path.join(assets_dir, 'icon.png')

def get_hotkey():
    """Returns the appropriate hotkey combination for the current platform."""
    system = get_platform()
    
    if system == 'darwin':
        return 'command+shift+v'
    else:
        return 'ctrl+shift+v' 