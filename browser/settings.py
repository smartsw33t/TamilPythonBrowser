import json
import os
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QWidget

import browser


class UserSettings(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.settings_data = browser.settings_data
        self.default_search_engine = self.settings_data["defaultSearchEngine"]
        self.mainWidget = QWidget(self)

        self.init_ui()
        self.retranslateUi()

    def init_ui(self):
        self.resize(720, 500)
        self.setWindowTitle("அமைப்புகள்")

        # Base Tamil font setup
        tamil_font = QtGui.QFont("Nirmala UI", 10)
        tamil_font.setStyleHint(QtGui.QFont.SansSerif)
        self.setFont(tamil_font)

        self.addDefaultSearchEngineSelector()

        # Settings heading
        self.label_2 = QtWidgets.QLabel(self.mainWidget)
        self.label_2.setGeometry(QtCore.QRect(15, 10, 180, 30))
        header_font = QtGui.QFont("Nirmala UI", 13, QtGui.QFont.Bold)
        header_font.setStyleHint(QtGui.QFont.SansSerif)
        self.label_2.setFont(header_font)
        self.label_2.setObjectName("label_2")

        # 1. Search Engine Section
        self.label = QtWidgets.QLabel(self.mainWidget)
        self.label.setGeometry(QtCore.QRect(15, 60, 300, 24))
        section_font = QtGui.QFont("Nirmala UI", 10, QtGui.QFont.Bold)
        section_font.setStyleHint(QtGui.QFont.SansSerif)
        self.label.setFont(section_font)
        self.label.setObjectName("label")

        self.label_5 = QtWidgets.QLabel(self.mainWidget)
        self.label_5.setGeometry(QtCore.QRect(15, 88, 440, 22))
        self.label_5.setFont(tamil_font)
        self.label_5.setObjectName("label_5")

        # 2. On Startup Section
        self.label_3 = QtWidgets.QLabel(self.mainWidget)
        self.label_3.setGeometry(QtCore.QRect(15, 140, 300, 24))
        self.label_3.setFont(section_font)
        self.label_3.setObjectName("label_3")

        self.label_4 = QtWidgets.QLabel(self.mainWidget)
        self.label_4.setGeometry(QtCore.QRect(15, 168, 440, 22))
        self.label_4.setFont(tamil_font)
        self.label_4.setObjectName("label_4")

        self.startup_page = QtWidgets.QLineEdit(self.mainWidget)
        self.startup_page.setGeometry(QtCore.QRect(470, 155, 230, 33))
        self.startup_page.setFont(tamil_font)
        self.startup_page.setText(self.settings_data["startupPage"])
        self.startup_page.setObjectName("startup_page")

        # 3. Home Button Section
        self.label_7 = QtWidgets.QLabel(self.mainWidget)
        self.label_7.setGeometry(QtCore.QRect(15, 230, 300, 24))
        self.label_7.setFont(section_font)
        self.label_7.setObjectName("label_7")

        self.label_6 = QtWidgets.QLabel(self.mainWidget)
        self.label_6.setGeometry(QtCore.QRect(15, 258, 440, 22))
        self.label_6.setFont(tamil_font)
        self.label_6.setObjectName("label_6")

        self.home_button_page = QtWidgets.QLineEdit(self.mainWidget)
        self.home_button_page.setGeometry(QtCore.QRect(470, 245, 230, 33))
        self.home_button_page.setFont(tamil_font)
        self.home_button_page.setText(self.settings_data["homeButtonPage"])
        self.home_button_page.setObjectName("home_button_page")

        # 4. New Tab Section (சாளரப்பிரிவு)
        self.label_9 = QtWidgets.QLabel(self.mainWidget)
        self.label_9.setGeometry(QtCore.QRect(15, 320, 300, 24))
        self.label_9.setFont(section_font)
        self.label_9.setObjectName("label_9")

        self.label_8 = QtWidgets.QLabel(self.mainWidget)
        self.label_8.setGeometry(QtCore.QRect(15, 348, 440, 22))
        self.label_8.setFont(tamil_font)
        self.label_8.setObjectName("label_8")

        self.new_tab_page = QtWidgets.QLineEdit(self.mainWidget)
        self.new_tab_page.setGeometry(QtCore.QRect(470, 335, 230, 33))
        self.new_tab_page.setFont(tamil_font)
        self.new_tab_page.setText(self.settings_data["newTabPage"])
        self.new_tab_page.setObjectName("new_tab_page")

        # Buttons
        self.discard_changes = QtWidgets.QPushButton(self.mainWidget)
        self.discard_changes.setGeometry(QtCore.QRect(410, 440, 140, 36))
        self.discard_changes.setFont(tamil_font)
        self.discard_changes.setObjectName("discard_changes")
        self.discard_changes.clicked.connect(self.closeWindow)

        self.save_settings = QtWidgets.QPushButton(self.mainWidget)
        self.save_settings.setGeometry(QtCore.QRect(560, 440, 140, 36))
        self.save_settings.setFont(tamil_font)
        self.save_settings.setObjectName("save_settings")
        self.save_settings.clicked.connect(self.saveChangesToJson)

        QtCore.QMetaObject.connectSlotsByName(self.mainWidget)

        if os.path.isfile(os.path.join("styles", "settings_style.css")):
            with open(os.path.join("styles", "settings_style.css")) as f:
                self.setStyleSheet(f.read())

    def addDefaultSearchEngineSelector(self):
        self.searchEngineSelector = QtWidgets.QComboBox(self.mainWidget)
        self.searchEngineSelector.setEnabled(True)
        self.searchEngineSelector.setGeometry(QtCore.QRect(470, 70, 230, 33))
        combo_font = QtGui.QFont("Nirmala UI", 10)
        combo_font.setStyleHint(QtGui.QFont.SansSerif)
        self.searchEngineSelector.setFont(combo_font)

        self.searchEngineSelector.addItem("Google")
        self.searchEngineSelector.addItem("Yahoo")
        self.searchEngineSelector.addItem("Bing")
        self.searchEngineSelector.addItem("DuckDuckGo")
        self.searchEngineSelector.currentTextChanged.connect(self.addDropDownItemToJson)

        if self.default_search_engine == "Google":
            self.searchEngineSelector.setCurrentIndex(0)
        elif self.default_search_engine == "Yahoo":
            self.searchEngineSelector.setCurrentIndex(1)
        elif self.default_search_engine == "Bing":
            self.searchEngineSelector.setCurrentIndex(2)
        elif self.default_search_engine == "DuckDuckGo":
            self.searchEngineSelector.setCurrentIndex(3)

    def saveChangesToJson(self):
        if len(self.startup_page.text()) > 0:
            self.settings_data["startupPage"] = self.startup_page.text()

        if len(self.home_button_page.text()) > 0:
            self.settings_data["homeButtonPage"] = self.home_button_page.text()

        if len(self.new_tab_page.text()) > 0:
            self.settings_data["newTabPage"] = self.new_tab_page.text()

        with open("settings.json", "w") as f:
            json.dump(self.settings_data, f, indent=2)

        self.close()

    def addDropDownItemToJson(self):
        self.settings_data["defaultSearchEngine"] = self.searchEngineSelector.currentText()
        with open("settings.json", "w") as f:
            json.dump(self.settings_data, f, indent=2)

    def closeWindow(self):
        self.close()

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("Form", "அமைப்புகள்"))
        self.label_2.setText(_translate("Form", "அமைப்புகள்"))

        # தேடல் பொறி
        self.label.setText(_translate("Form", "இயல்புநிலைத் தேடல் பொறி"))
        self.label_5.setText(
            _translate("Form", "முகவரிப் பட்டியில் இயல்பாகப் பயன்படுத்த வேண்டிய தேடல் பொறி")
        )

        # தொடக்கம்
        self.label_3.setText(_translate("Form", "தொடக்கத்தில்"))
        self.label_4.setText(
            _translate("Form", "உலாவி தொடங்கும் போது காட்டப்பட வேண்டிய வலைப்பக்கம்")
        )

        # முகப்புப் பொத்தான்
        self.label_7.setText(_translate("Form", "முகப்புப் பொத்தான்"))
        self.label_6.setText(
            _translate("Form", "முகப்புப் பொத்தானை அழுத்தும்போது திறக்க வேண்டிய பக்கம்")
        )

        # சாளரப்பிரிவு
        self.label_9.setText(_translate("Form", "புதிய சாளரப்பிரிவு"))
        self.label_8.setText(
            _translate("Form", "புதிய சாளரப்பிரிவு திறக்கப்படும் போது காட்ட வேண்டிய பக்கம்")
        )

        # பொத்தான்கள்
        self.discard_changes.setText(_translate("Form", "மாற்றங்களை விலக்குக"))
        self.save_settings.setText(_translate("Form", "அமைப்புகளைச் சேமித்திடுக"))
