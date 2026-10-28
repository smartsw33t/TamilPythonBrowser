from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QMessageBox


class fileErrorDialog(QMessageBox):
    def __init__(self, *args, **kwargs):
        super(fileErrorDialog, self).__init__(*args, **kwargs)

        tamil_font = QFont("Nirmala UI", 10)
        tamil_font.setStyleHint(QFont.SansSerif)
        self.setFont(tamil_font)

        self.setText("தவறான கோப்பு குறிப்பிடப்பட்டுள்ளது. சரியான கோப்பைக் குறிப்பிட்டு மீண்டும் முயல்க.")
        self.setIcon(QMessageBox.Critical)
        self.setWindowTitle("சரியான கோப்பைக் குறிப்பிடவும்")

        ok_button = self.addButton(QMessageBox.Ok)
        ok_button.setText("சரி")

        self.show()


class errorMsg(QMessageBox):
    def __init__(self, text: str = "உட்புறப் பிழை ஒன்று ஏற்பட்டுள்ளது!"):
        super(errorMsg, self).__init__()

        tamil_font = QFont("Nirmala UI", 10)
        tamil_font.setStyleHint(QFont.SansSerif)
        self.setFont(tamil_font)

        self.setText(text)
        self.setIcon(QMessageBox.Critical)
        self.setWindowTitle("பிழை!")

        ok_button = self.addButton(QMessageBox.Ok)
        ok_button.setText("சரி")

        self.show()
