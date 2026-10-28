import os
import sys
import json
import sqlite3

from PyQt5.QtGui import QFontDatabase, QIcon, QFont
from PyQt5.QtWidgets import QApplication
import browser.main_window


# DB to open
connection = sqlite3.connect("BrowserLocalDB.db", check_same_thread=False)
cursor = connection.cursor()

# Set base UI font with Unicode/Tamil fallback
textFont = QFont("Nirmala UI", 13)
textFont.setStyleHint(QFont.SansSerif)

if os.path.isfile("settings.json"):
    with open("settings.json", "r") as f:
        settings_data = json.load(f)
else:
    json_data = json.loads(
        """
        {
            "defaultSearchEngine": "Google",
            "startupPage": "https://www.google.co.in",
            "newTabPage": "https://www.google.co.in",
            "homeButtonPage": "https://www.google.co.in"
        }
        """
    )
    with open("settings.json", "w") as f:
        json.dump(json_data, f, indent=2)
    with open("settings.json", "r") as f:
        settings_data = json.load(f)


def main():
    gui_app = QApplication(sys.argv)

    # Disable shortcut in context menu
    gui_app.styleHints().setShowShortcutsInContextMenus(False)

    # Set the localized window name
    QApplication.setApplicationName("தமிழ் உலாவி")

    # Set the window icon
    QApplication.setWindowIcon(QIcon(os.path.join("resources", "logos", "browser.png")))

    # App styles
    if os.path.isfile(os.path.join("styles", "styles.css")):
        with open(os.path.join("styles", "styles.css")) as f:
            gui_app.setStyleSheet(f.read())

    QFontDatabase.addApplicationFont(os.path.join("fonts", "fa-solid-900.ttf"))

    window = browser.main_window.mainWindow()

    sys.exit(gui_app.exec_())
