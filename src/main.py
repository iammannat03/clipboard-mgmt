import sys
import os
from PyQt6.QtWidgets import (QApplication, QMainWindow, QSystemTrayIcon,
                           QMenu, QWidget, QVBoxLayout, QListWidget,
                           QLineEdit, QPushButton, QHBoxLayout)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon, QAction, QKeySequence, QShortcut
import pyperclip
from datetime import datetime
from utils.platform_utils import get_icon_path

class ClipboardManager(QMainWindow):
    def __init__(self):
        super().__init__()
        self.clipboard_history = []
        self.max_history = 100
        self.init_ui()
        self.setup_system_tray()
        self.setup_shortcuts()
        
    def init_ui(self):
        self.setWindowTitle('Clipboard Manager')
        self.setGeometry(100, 100, 600, 400)
        
        # Set application icon
        icon_path = get_icon_path()
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        
        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Search bar
        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText('Search clipboard history...')
        self.search_input.textChanged.connect(self.filter_history)
        search_layout.addWidget(self.search_input)
        layout.addLayout(search_layout)
        
        # History list
        self.history_list = QListWidget()
        self.history_list.itemDoubleClicked.connect(self.copy_to_clipboard)
        layout.addWidget(self.history_list)
        
        # Clear button
        clear_button = QPushButton('Clear History')
        clear_button.clicked.connect(self.clear_history)
        layout.addWidget(clear_button)
        
        # Start monitoring clipboard
        QApplication.clipboard().dataChanged.connect(self.on_clipboard_change)
        
    def setup_system_tray(self):
        self.tray_icon = QSystemTrayIcon(self)
        icon_path = get_icon_path()
        if os.path.exists(icon_path):
            self.tray_icon.setIcon(QIcon(icon_path))
        else:
            self.tray_icon.setIcon(QIcon.fromTheme('edit-copy'))
        
        # Create tray menu
        tray_menu = QMenu()
        show_action = QAction('Show', self)
        show_action.triggered.connect(self.show)
        quit_action = QAction('Quit', self)
        quit_action.triggered.connect(self.quit_application)
        
        tray_menu.addAction(show_action)
        tray_menu.addAction(quit_action)
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()
        
    def setup_shortcuts(self):
        # Create a shortcut for showing/hiding the window
        self.shortcut = QShortcut(QKeySequence("Ctrl+Shift+V"), self)
        self.shortcut.activated.connect(self.toggle_window)
        
    def toggle_window(self):
        if self.isVisible():
            self.hide()
        else:
            self.show()
            self.activateWindow()
            
    def on_clipboard_change(self):
        text = QApplication.clipboard().text()
        if text and text not in self.clipboard_history:
            self.clipboard_history.insert(0, text)
            if len(self.clipboard_history) > self.max_history:
                self.clipboard_history.pop()
            self.update_history_display()
            
    def update_history_display(self):
        self.history_list.clear()
        for item in self.clipboard_history:
            self.history_list.addItem(item)
            
    def filter_history(self):
        search_text = self.search_input.text().lower()
        self.history_list.clear()
        for item in self.clipboard_history:
            if search_text in item.lower():
                self.history_list.addItem(item)
                
    def copy_to_clipboard(self, item):
        text = item.text()
        pyperclip.copy(text)
        QApplication.clipboard().setText(text)
        
    def clear_history(self):
        self.clipboard_history.clear()
        self.history_list.clear()
        
    def quit_application(self):
        QApplication.quit()
        
    def closeEvent(self, event):
        event.ignore()
        self.hide()

def main():
    app = QApplication(sys.argv)
    window = ClipboardManager()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main() 