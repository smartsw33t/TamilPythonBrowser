import os
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QDialogButtonBox,
    QDialog,
    QVBoxLayout,
    QLabel
)


class AboutDialog(QDialog):
    def __init__(self, parent=None, *args, **kwargs):
        super(AboutDialog, self).__init__(*args, **kwargs)

        self.layout = QVBoxLayout()

        ok_btn = QDialogButtonBox.Ok
        self.button_box = QDialogButtonBox(ok_btn)

        self.init_ui()

    def init_ui(self):
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        # Set default Tamil text for the OK action
        ok_button = self.button_box.button(QDialogButtonBox.Ok)
        ok_button.setText("சரி")

        if os.path.isfile(os.path.join("styles", "about_style.css")):
            with open(os.path.join("styles", "about_style.css")) as f:
                ok_button.setStyleSheet(f.read())

        # Base Tamil font setup
        tamil_font = QFont("Nirmala UI")
        tamil_font.setStyleHint(QFont.SansSerif)

        logo = QLabel()
        pixmap = QPixmap(os.path.join("resources", "logos", "browser.png"))
        pixmap = pixmap.scaled(80, 80)
        logo.setPixmap(pixmap)
        self.layout.addWidget(logo)

        # Localized Title
        title = QLabel("தமிழ் உலாவி")
        title_font = QFont(tamil_font)
        title_font.setPointSize(18)
        title_font.setBold(True)
        title.setFont(title_font)
        self.layout.addWidget(title)

        # Version & Upstream Attribution
        lbl1 = QLabel(
            '<center>பதிப்பு 1.0.0<br>'
            'ஆரம்ப உருவாக்கம்: <a href="https://github.com/saminsakur/PyQt5BrowserBuild">Samin Sakur</a><br>'
            'தமிழ் உருவாக்கம்: <a href="https://github.com/smartsw33t">Jayaseelan Samuel</a></center>'
        )
        body_font = QFont(tamil_font)
        body_font.setPointSize(11)
        lbl1.setFont(body_font)
        lbl1.setOpenExternalLinks(True)
        self.layout.addWidget(lbl1)

        # Repository / Learn More Link
        github_pg = QLabel(
            '<a href="https://github.com/smartsw33t/TamilPythonBrowser">மேலும் அறிக </a>'
        )
        link_font = QFont("Font Awesome 5 Free Solid", 11)
        github_pg.setFont(link_font)
        github_pg.setOpenExternalLinks(True)
        self.layout.addWidget(github_pg)

        for i in range(0, self.layout.count()):
            self.layout.itemAt(i).setAlignment(Qt.AlignHCenter)

        self.layout.addWidget(self.button_box)

        self.setLayout(self.layout)

        self.setWindowFlags(Qt.MSWindowsFixedSizeDialogHint)
        self.resize(420, 280)
        self.setMaximumHeight(320)
        self.setMaximumWidth(520)
        self.setWindowTitle("அறிமுகம்")
