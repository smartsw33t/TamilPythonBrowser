from PyQt5.QtWebEngineWidgets import (
    QWebEngineDownloadItem,
    QWebEngineSettings,
    QWebEngineView,
)
from PyQt5.QtWidgets import (
    QMainWindow,
    QPushButton,
    QShortcut,
    QToolBar,
    QMenu,
    QAction,
    QFileDialog,
)
from PyQt5.QtCore import QSize, QUrl, Qt
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5 import QtCore
from PyQt5 import QtGui
import browser.widgets
import browser.printer
import browser.errors
import browser.about
import browser.history
import browser.settings
import browser
import sys
import os
import re
import pyperclip as pc
import datetime


# Regular expressions to match urls
pattern = re.compile(
    r"^(http|https)?:?(\/\/)?(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)"
)
without_http_pattern = re.compile(
    r"[\-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)"
)
file_pattern = re.compile(r"^file://")


class mainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(mainWindow, self).__init__(*args, **kwargs)
        self.init_ui()

    def init_ui(self):
        self.tabs = browser.widgets.Tabs()  # create tabs

        # create history table
        browser.cursor.execute(
            """CREATE TABLE IF NOT EXISTS "history" (
                "id"	INTEGER,
                "title"	TEXT,
                "url"	TEXT,
                "date"	TEXT,
                PRIMARY KEY("id")
            )"""
        )

        # Add new tab when tab is doubleclicked
        self.tabs.tabBarDoubleClicked.connect(self.tab_open_doubleclick)

        # Connect to function when current tab changes
        self.tabs.currentChanged.connect(self.tab_changed)

        # Handle tab closing
        self.tabs.tabCloseRequested.connect(self.close_current_tab)

        # open new tab on Ctrl+T
        AddNewTabKeyShortcut = QShortcut("Ctrl+T", self)
        AddNewTabKeyShortcut.activated.connect(
            lambda: self.add_new_tab(
                QtCore.QUrl(browser.settings_data["newTabPage"]), "புதிய பிரிவு"
            )
        )

        # Close current tab on Ctrl+W
        CloseCurrentTabKeyShortcut = QShortcut("Ctrl+W", self)
        CloseCurrentTabKeyShortcut.activated.connect(
            lambda: self.close_current_tab(self.tabs.currentIndex())
        )

        # Exit browser on Ctrl+Shift+W
        ExitBrowserShortcutKey = QShortcut("Ctrl+Shift+W", self)
        ExitBrowserShortcutKey.activated.connect(sys.exit)

        # Navigation bar
        self.navbar = QToolBar()
        self.navbar.setMovable(False)
        self.addToolBar(self.navbar)

        # Back button
        back_btn = QPushButton(self)
        back_btn.setObjectName("back_btn")
        back_btn.setIcon(
            QtGui.QIcon(os.path.join("resources", "icons", "left-arrow.png"))
        )
        back_btn.setToolTip("முந்தைய பக்கத்திற்குச் செல்ல")
        back_btn.setShortcut("Alt+Left")
        back_btn.clicked.connect(self.navigate_back_tab)
        self.navbar.addWidget(back_btn)

        # Forward button
        forward_butn = QPushButton(self)
        forward_butn.setObjectName("forward_butn")
        forward_butn.setIcon(
            QtGui.QIcon(os.path.join("resources", "icons", "right-arrow.png"))
        )
        forward_butn.setToolTip("அடுத்த பக்கத்திற்குச் செல்ல")
        forward_butn.setShortcut("Alt+Right")
        forward_butn.clicked.connect(self.forward_tab)
        self.navbar.addWidget(forward_butn)

        # Refresh button
        self.reload_butn = QPushButton(self)
        self.reload_butn.setObjectName("reload_butn")
        self.reload_butn.setToolTip("பக்கத்தைப் புதுப்பிக்க")
        self.reload_butn.setShortcut("Ctrl+R")
        self.reload_butn.resize(QSize(50, 50))
        self.reload_butn.setIcon(
            QtGui.QIcon(os.path.join("resources", "icons", "refresh.png"))
        )
        self.reload_butn.clicked.connect(self.reload_tab)

        # Stop button
        self.stop_btn = QPushButton(self)
        self.stop_btn.setObjectName("stop_butn")
        self.stop_btn.setToolTip("பக்கம் ஏற்றப்படுவதை நிறுத்த")
        self.stop_btn.setShortcut("Escape")
        self.stop_btn.setIcon(QIcon(os.path.join("resources", "icons", "cross.png")))
        self.stop_btn.clicked.connect(self.stop_loading_tab)

        self.stop_action = self.navbar.addWidget(self.stop_btn)
        self.reload_action = self.navbar.addWidget(self.reload_butn)

        # Home button
        self.home_button = QPushButton(self)
        self.home_button.setObjectName("home_button")
        self.home_button.setToolTip("முகப்புப் பக்கத்திற்குச் செல்ல")
        self.home_button.setIcon(
            QtGui.QIcon(os.path.join("resources", "icons", "home.png"))
        )
        self.home_button.clicked.connect(self.goToHome)
        self.navbar.addWidget(self.home_button)

        # Address bar
        self.url_bar = browser.widgets.AddressBar()
        self.url_bar.initAddressBar()
        self.url_bar.setFrame(False)
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        self.url_bar.setShortcutEnabled(True)
        self.url_bar.setToolTip(self.url_bar.text())

        FocusOnAddressBar = QShortcut("Ctrl+E", self)
        FocusOnAddressBar.activated.connect(self.url_bar.setFocus)

        self.stop_action.setVisible(False)
        self.navbar.addSeparator()

        # SSL status icon
        self.httpsicon = browser.widgets.SSLIcon()
        self.navbar.addWidget(self.httpsicon)
        self.navbar.addWidget(self.url_bar)

        # Context Menu
        context_menu = QMenu(self)
        context_menu.setObjectName("ContextMenu")

        ContextMenuButton = QPushButton(self)
        ContextMenuButton.setObjectName("ContextMenuButton")
        ContextMenuButton.setShortcut("Alt+F")
        ContextMenuButton.setIcon(
            QIcon(os.path.join("resources", "icons", "more.png"))
        )
        ContextMenuButton.setObjectName("ContextMenuTriggerButn")
        ContextMenuButton.setToolTip("மேலும் தேர்வுசெய்யக்கூடியவை")
        ContextMenuButton.setMenu(context_menu)

        # Actions of context menu
        newTabAction = QAction("புதிய சாளரப்பிரிவு", self)
        newTabAction.setIcon(
            QtGui.QIcon(os.path.join("resources", "icons", "newtab.png"))
        )
        newTabAction.triggered.connect(
            lambda: self.add_new_tab(
                QUrl(browser.settings_data["newTabPage"]), "முகப்பு"
            )
        )
        newTabAction.setToolTip("புதிய சாளரப்பிரிவைத் திறந்திடுக")
        context_menu.addAction(newTabAction)

        newWindowAction = QAction("புதிய சாளரம்", self)
        newWindowAction.setIcon(
            QtGui.QIcon(os.path.join("resources", "icons", "app_window_ios.png"))
        )
        newWindowAction.triggered.connect(self.CreateNewWindow)
        context_menu.addAction(newWindowAction)

        CloseTabAction = QAction("சாளரப்பிரிவை மூடுக", self)
        CloseTabAction.setIcon(
            QIcon(os.path.join("resources", "icons", "closetab.png"))
        )
        CloseTabAction.triggered.connect(
            lambda: self.close_current_tab(self.tabs.currentIndex())
        )
        CloseTabAction.setToolTip("நடப்பு சாளரப்பிரிவை மூடுக")
        context_menu.addAction(CloseTabAction)

        context_menu.addSeparator()
        context_menu.addSeparator()

        CopySiteAddress = QAction(
            QtGui.QIcon(os.path.join("resources", "icons", "url.png")),
            "பிணைப்பை நகலெடுத்திடுக",
            self,
        )
        CopySiteAddress.triggered.connect(self.CopySiteLink)
        CopySiteAddress.setToolTip("இந்தத் தளத்தின் பிணைப்பை நகலெடுக்க")
        context_menu.addAction(CopySiteAddress)

        PasteAndGo = QAction(
            QtGui.QIcon(os.path.join("resources", "icons", "paste.png")),
            "ஒட்டிச் செல்க",
            self,
        )
        PasteAndGo.triggered.connect(self.PasteUrlAndGo)
        PasteAndGo.setToolTip("எடுத்துவைத்த பிணைப்பிற்கு நேரடியாகச் செல்ல")
        context_menu.addAction(PasteAndGo)

        context_menu.addSeparator()

        # View History ("இதுவரை")
        ViewHistory = QAction("இதுவரை", self)
        ViewHistory.setIcon(QIcon(os.path.join("resources", "icons", "history.png")))
        ViewHistory.triggered.connect(self.openHistory)
        ViewHistory.setShortcut("Ctrl+h")
        context_menu.addAction(ViewHistory)

        OpenPgAction = QAction("திறந்திடுக", self)
        OpenPgAction.setIcon(
            QtGui.QIcon(os.path.join("resources", "icons", "openclickhtml.png"))
        )
        OpenPgAction.setToolTip("கோப்பை உலாவியில் திறக்க")
        OpenPgAction.setShortcut("Ctrl+O")
        OpenPgAction.triggered.connect(self.open_local_file)
        context_menu.addAction(OpenPgAction)

        SavePageAs = QAction("பக்கத்தைச் சேமித்திடுக", self)
        SavePageAs.setIcon(
            QtGui.QIcon(os.path.join("resources", "icons", "save-disk.png"))
        )
        SavePageAs.setToolTip("நடப்புப் பக்கத்தைச் சாதனத்தில் சேமிக்க")
        SavePageAs.setShortcut("Ctrl+S")
        SavePageAs.triggered.connect(self.save_page)
        context_menu.addAction(SavePageAs)

        PrintThisPageAction = QAction("பக்கத்தை அச்சிடுக", self)
        PrintThisPageAction.setIcon(
            QtGui.QIcon(os.path.join("resources", "icons", "printer.png"))
        )
        PrintThisPageAction.triggered.connect(self.print_this_page)
        PrintThisPageAction.setShortcut("Ctrl+P")
        PrintThisPageAction.setToolTip("நடப்புப் பக்கத்தை அச்சிட")
        context_menu.addAction(PrintThisPageAction)

        PrintPageWithPreview = QAction(
            QtGui.QIcon(os.path.join("resources", "icons", "printerprev.png")),
            "அச்சு முன்னோட்டம்",
            self,
        )
        PrintPageWithPreview.triggered.connect(self.PrintWithPreview)
        PrintPageWithPreview.setShortcut("Ctrl+Shift+P")
        context_menu.addAction(PrintPageWithPreview)

        SavePageAsPDF = QAction(
            QtGui.QIcon(os.path.join("resources", "icons", "adobepdf.png")),
            "பிடிஎஃப் ஆகச் சேமித்திடுக",
            self,
        )
        SavePageAsPDF.triggered.connect(self.save_as_pdf)
        context_menu.addAction(SavePageAsPDF)

        context_menu.addSeparator()

        userSettingsAction = QAction(
            QtGui.QIcon(os.path.join("resources", "icons", "settings.png")),
            "அமைப்புகள்",
            self,
        )
        userSettingsAction.triggered.connect(self.openSettings)
        context_menu.addAction(userSettingsAction)

        # Help Menu ("உதவி")
        HelpMenu = QMenu("உதவி", self)
        HelpMenu.setObjectName("HelpMenu")
        HelpMenu.setIcon(QIcon(os.path.join("resources", "icons", "question.png")))

        AboutAction = QAction("அறிமுகம்", self)
        AboutAction.setIcon(QIcon(os.path.join("resources", "icons", "info.png")))
        AboutAction.triggered.connect(self.about)
        HelpMenu.addAction(AboutAction)

        VisitGithubAction = QAction("திட்டப் பக்கம் செல்ல", self)
        VisitGithubAction.triggered.connect(self.visitGithub)
        HelpMenu.addAction(VisitGithubAction)

        context_menu.addMenu(HelpMenu)
        context_menu.addSeparator()

        CloseBrowser = QAction("உலாவியை மூடுக", self)
        CloseBrowser.triggered.connect(lambda: sys.exit())
        context_menu.addAction(CloseBrowser)

        self.navbar.addWidget(ContextMenuButton)

        # Startup tab
        self.add_new_tab(QUrl(browser.settings_data["startupPage"]), "முகப்பு")

        self.url_bar.setFocus()
        self.setCentralWidget(self.tabs)
        self.showMaximized()
        self.setMinimumWidth(400)

    @QtCore.pyqtSlot(int)
    def loadProgressHandler(self, prog):
        if self.tabs.currentWidget() is not self.sender():
            return

        loading = prog < 100
        self.stop_action.setVisible(loading)
        self.reload_action.setVisible(not loading)

    def goToHome(self):
        self.tabs.currentWidget().setUrl(QUrl(browser.settings_data["homeButtonPage"]))

    def CreateNewWindow(self):
        window = mainWindow()
        window.show()

    def CopySiteLink(self):
        pc.copy(self.tabs.currentWidget().url().toString())

    def PasteUrlAndGo(self):
        self.add_new_tab(QUrl(pc.paste()), self.tabs.currentWidget().title())

    def visitGithub(self):
        self.add_new_tab(
            QUrl("https://github.com/smartsw33t/TamilPythonBrowser"), "கிட்ஹப்"
        )

    def navigate_back_tab(self):
        self.tabs.currentWidget().back()

    def forward_tab(self):
        self.tabs.currentWidget().forward()

    def reload_tab(self):
        self.tabs.currentWidget().reload()

    def stop_loading_tab(self):
        if self.tabs.currentWidget() is None:
            return
        self.tabs.currentWidget().stop()

    def open_local_file(self):
        filename, _ = QFileDialog.getOpenFileName(
            parent=self,
            caption="கோப்பைத் திறந்திடுக",
            directory="",
            filter="வலைப்பக்கக் கோப்புகள் (*.htm *.html *.mhtml);;அனைத்துக் கோப்புகள் (*.*)",
        )
        if filename:
            try:
                with open(filename, "r", encoding="utf8") as f:
                    opened_file = f.read()
                    self.tabs.currentWidget().setHtml(opened_file)

            except:
                dlg = browser.errors.fileErrorDialog()
                dlg.exec_()

        self.url_bar.setText(filename)

    def save_page(self):
        filepath, filter = QFileDialog.getSaveFileName(
            parent=self,
            caption="பக்கத்தைச் சேமித்திடுக",
            directory="",
            filter="முழுமையான வலைப்பக்கம் (*.htm *.html);;வலைப்பக்கக் கோப்புகள் (*.htm *.html);;அனைத்துக் கோப்புகள் (*.*)",
        )
        try:
            if filter == "வலைப்பக்கக் கோப்புகள் (*.htm *.html)":
                self.tabs.currentWidget().page().save(
                    filepath, format=QWebEngineDownloadItem.MimeHtmlSaveFormat
                )

            elif filter == "முழுமையான வலைப்பக்கம் (*.htm *.html)":
                self.tabs.currentWidget().page().save(
                    filepath, format=QWebEngineDownloadItem.CompleteHtmlSaveFormat
                )

        except:
            self.showErrorDlg()

    def print_this_page(self):
        try:
            handler_print = browser.printer.PrintHandler()
            handler_print.setPage(self.tabs.currentWidget().page())
            handler_print.print()

        except:
            self.showErrorDlg()

    def PrintWithPreview(self):
        handler = browser.printer.PrintHandler()
        handler.setPage(self.tabs.currentWidget().page())
        handler.printPreview()

    def save_as_pdf(self):
        filename, filter = QFileDialog.getSaveFileName(
            parent=self,
            caption="பிடிஎஃப் ஆகச் சேமித்திடுக",
            filter="பிடிஎஃப் ஆவணம் (*.pdf);;அனைத்துக் கோப்புகள் (*.*)"
        )

        self.tabs.currentWidget().page().printToPdf(filename)

    def tab_open_doubleclick(self, i):
        if i == -1:
            self.add_new_tab(QUrl(browser.settings_data["newTabPage"]), label="புதிய சாளரப்பிரிவு")

    def tab_changed(self, i):
        qurl = self.tabs.currentWidget().url()
        self.update_urlbar(qurl, self.tabs.currentWidget())
        self.update_title(self.tabs.currentWidget())

    def close_current_tab(self, i):
        if self.tabs.count() < 2:
            self.close()

        self.tabs.removeTab(i)

    def update_title(self, browser_widget):
        if browser_widget != self.tabs.currentWidget():
            return

        title = self.tabs.currentWidget().page().title()

        if len(title) > 0:
            self.setWindowTitle(f"{title} - தமிழ் உலாவி")
        else:
            self.setWindowTitle("தமிழ் உலாவி")

    def add_new_tab(self, qurl=None, label="காலி சாளரப்பிரிவு"):
        if qurl is None:
            qurl = QUrl(browser.settings_data["newTabPage"])

        _browser = QWebEngineView()

        _browser.setPage(browser.widgets.customWebEnginePage(_browser))
        _browser.settings().setAttribute(
            QWebEngineSettings.FullScreenSupportEnabled, True
        )
        _browser.page().fullScreenRequested.connect(lambda request: request.accept())
        _browser.loadProgress.connect(self.loadProgressHandler)
        _browser.page().WebAction()
        _browser.settings().setAttribute(QWebEngineSettings.ScreenCaptureEnabled, True)

        i = self.tabs.addTab(_browser, label)
        self.tabs.setCurrentIndex(i)

        _browser.load(qurl)
        self.url_bar.setFocus()

        _browser.urlChanged.connect(
            lambda qurl, browser=_browser: self.update_urlbar(qurl, browser)
        )

        _browser.loadFinished.connect(
            lambda _, i=i, browser=_browser: self.tabs.setTabText(
                i, browser.page().title()
            )
        )

        _browser.page().loadFinished.connect(self.updateHistory)

    def showErrorDlg(self):
        dlg = browser.errors.errorMsg()
        dlg.exec_()

    def about(self):
        self.AboutDialogue = browser.about.AboutDialog()
        self.AboutDialogue.show()

    def update_urlbar(self, q, _browser=None):
        if _browser != self.tabs.currentWidget():
            return

        if q.toString() == browser.settings_data["newTabPage"]:
            self.httpsicon.setPixmap(
                QPixmap(os.path.join("resources", "icons", "info_24.png"))
            )
            self.httpsicon.setToolTip("இது உலாவியின் புதிய சாளரப்பிரிவு பக்கம்")
            self.url_bar.clear()

        else:
            if q.scheme() == "https":
                self.httpsicon.setPixmap(
                    QPixmap(os.path.join("resources", "icons", "security.png"))
                )
                self.httpsicon.setToolTip(
                    "இத்தளத்துடனான இணைப்பு பாதுகாப்பானது\n\nசெல்லுபடியாகும் சான்றிதழ் உள்ளது"
                )

            elif q.scheme() in ("file", "data"):
                self.httpsicon.setPixmap(
                    QPixmap(os.path.join("resources", "icons", "info_24.png"))
                )
                self.httpsicon.setToolTip("நீங்கள் சாதனத்தினுள் உள்ள அல்லது பகிரப்பட்ட கோப்பைப் பார்க்கிறீர்கள்")

            else:
                self.httpsicon.setPixmap(
                    QPixmap(os.path.join("resources", "icons", "warning.png"))
                )
                self.httpsicon.setToolTip("இத்தளத்துடனான இணைப்பு பாதுகாப்பற்றதாக இருக்கலாம்")

        self.url_bar.setCursorPosition(0)

    def searchWeb(self, text):
        Engine = browser.settings_data["defaultSearchEngine"]
        if text:
            if Engine == "Google":
                return "https://www.google.com/search?q=" + "+".join(text.split())
            elif Engine == "Yahoo":
                return "https://search.yahoo.com/search?q=" + "+".join(text.split())
            elif Engine == "Bing":
                return "https://www.bing.com/search?q=" + "+".join(text.split())
            elif Engine == "DuckDuckGo":
                return "https://duckduckgo.com/?q=" + "+".join(text.split())

    def navigate_to_url(self):
        in_url = self.url_bar.text()
        url = ""

        if len(str(in_url)) < 1:
            return

        if self.tabs.currentWidget() is None:
            return

        if file_pattern.search(in_url):
            file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), in_url))
            local_url = QUrl.fromLocalFile(file_path)
            self.tabs.currentWidget().load(local_url)

        elif without_http_pattern.search(in_url) and any(
            [i in in_url for i in ["http://", "https://"]]
        ):
            url = in_url

        elif pattern.search(in_url) and not any(
            i in in_url for i in ("http://", "https://", "file:///")
        ):
            url = "http://" + in_url

        elif "/" not in in_url:
            url = self.searchWeb(in_url)

        self.tabs.currentWidget().load(QUrl.fromUserInput(url))

    def updateHistory(self):
        title = self.tabs.currentWidget().page().title()
        url = str(self.tabs.currentWidget().page().url())
        url = url[19 : len(url) - 2]
        hour = datetime.datetime.now().strftime("%X")
        day = datetime.datetime.now().strftime("%x")
        date = hour + " - " + day

        data = browser.cursor.execute("SELECT * FROM history")
        siteInfoList = data.fetchall()

        for i in range(len(siteInfoList)):
            if url == siteInfoList[i][2]:
                browser.cursor.execute("DELETE FROM history WHERE url = ?", [url])

        browser.cursor.execute(
            "INSERT INTO history (title,url,date) VALUES (:title,:url,:date)",
            {"title": title, "url": url, "date": date},
        )

        browser.connection.commit()

    def openHistory(self):
        self.historyWindow = browser.history.HistoryWindow()
        self.historyWindow.setWindowFlags(Qt.Popup)
        self.historyWindow.setGeometry(
            int(self.tabs.currentWidget().frameGeometry().width() / 2 + 400),
            70,
            300,
            500,
        )
        self.historyWindow.setContentsMargins(0, 0, 0, 0)
        self.historyWindow.setStyleSheet(
            """
            background-color:#edf4f7;
            """
        )
        self.historyWindow.show()

    def openSiteHistoryClicked(self, url, *args):
        self.tabs.currentWidget().load(url)

    def openSettings(self):
        self.userSettingswindow = browser.settings.UserSettings()
        self.userSettingswindow.setWindowFlag(Qt.MSWindowsFixedSizeDialogHint)
        self.userSettingswindow.show()
