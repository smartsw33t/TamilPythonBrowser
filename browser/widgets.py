import os

from PyQt5.QtWebEngineWidgets import QWebEnginePage
from PyQt5.QtWidgets import QLabel, QLineEdit, QTabWidget
from PyQt5.QtGui import QPixmap, QFont
from PyQt5 import QtCore


class AddressBar(QLineEdit):
    def __init__(self):
        super().__init__()
        self.setFocus()

    def mousePressEvent(self, e):
        self.selectAll()

    def initAddressBar(self):
        # Set localized font and placeholder
        tamil_font = QFont("Nirmala UI", 10)
        tamil_font.setStyleHint(QFont.SansSerif)
        self.setFont(tamil_font)

        self.setPlaceholderText("தேடுக அல்லது வலை முகவரியை நிரப்புக")

        # Set focus to the address bar
        self.setFocus()
        if os.path.isfile(os.path.join("styles", "addr_bar.css")):
            with open(os.path.join("styles", "addr_bar.css")) as f:
                self.setStyleSheet(f.read())


class SSLIcon(QLabel):
    def __init__(self):
        super().__init__()
        self.InitSSLIcon()

    def InitSSLIcon(self):
        self.setObjectName("SSLIcon")
        icon_path = os.path.join("resources", "lock-icon.png")
        if os.path.isfile(icon_path):
            icon = QPixmap(icon_path)
            self.setPixmap(icon)


class Tabs(QTabWidget):
    def __init__(self):
        super().__init__()
        self.setDocumentMode(True)

        # Set the tabs closable & movable
        self.setTabsClosable(True)
        self.setMovable(True)

        # Localized font for tab headers
        tab_font = QFont("Nirmala UI", 9)
        tab_font.setStyleHint(QFont.SansSerif)
        self.setFont(tab_font)

        # Add styles to tabs
        tab_style_path = os.path.join("styles", "tab_style.css")
        if os.path.isfile(tab_style_path):
            with open(tab_style_path) as f:
                self.setStyleSheet(f.read())


class customWebEnginePage(QWebEnginePage):
    def createWindow(self, _type):
        page = customWebEnginePage(self)
        page.urlChanged.connect(self.on_url_changed)
        return page

    @QtCore.pyqtSlot(QtCore.QUrl)
    def on_url_changed(self, url):
        page = self.sender()
        self.setUrl(url)
        page.deleteLater()
