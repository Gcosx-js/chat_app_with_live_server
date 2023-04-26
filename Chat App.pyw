import socket as skt
from PyQt5.QtWidgets import *
from second import second_ui
from PyQt5 import *
from first import first_ui
from PyQt5.QtCore import Qt, QThread, pyqtSignal

class Birinci_ekran(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.app1 = first_ui()
        self.app1.setupUi(self)
        self.username = ""
        self.app1.username_input.textChanged.connect(self.update_username)
        self.app1.baglan_button.clicked.connect(self.baglan)

    def update_username(self, text):
        self.username = text

    def baglan(self):
        self.goster = Ikinci_ekran(self.username)
        self.close()
        self.goster.show()


class Ikinci_ekran(QWidget):
    def __init__(self, username) -> None:
        super().__init__()
        self.username = username
        self.app2 = second_ui()
        self.app2.setupUi(self)
        self.layout = QVBoxLayout(self.app2.scrollAreaWidgetContents)
        self.layout.setAlignment(Qt.AlignTop)
        self.app2.gonder.clicked.connect(self.gonder)
        self.scroll = self.app2.scrollArea.verticalScrollBar()
        self.lineedit = self.app2.user2_mesaj
        self.app2.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        HOST = '127.0.0.1'
        PORT = 23847
        self.s = skt.socket(skt.AF_INET, skt.SOCK_STREAM)
        self.s.connect((HOST, PORT))
        self.thread = MesajAlThread(self.s)
        self.thread.start()
        self.thread.gelen_mesaj_signal.connect(self.gelen_mesaj)
        msg2 = "{} Kanala uğurla bağlandınız!".format(self.username)
        self.s.send(msg2.encode("utf-8"))
        self.gelen_mesaj(msg2)

    def gelen_mesaj(self, msg):
        label = QLabel(msg)
        font = QtGui.QFont()                                                                            
        font.setPointSize(20)
        label.setFont(font)
        self.layout.addWidget(label)
        self.scroll.setValue(self.scroll.maximum())

    def gonder(self):
        msg = "{} : {}".format(self.username, self.lineedit.text())
        self.s.send(msg.encode("utf-8"))
        msg00 = "[Siz] : {}".format(self.lineedit.text())
        self.gelen_mesaj(msg00)
        self.lineedit.clear()

class MesajAlThread(QThread):
    gelen_mesaj_signal = pyqtSignal(str)

    def __init__(self, soket) -> None:
        super().__init__()
        self.soket = soket
        

    def run(self):
        BUFFERSIZE = 1024
        while True:
            try:
                msg = self.soket.recv(BUFFERSIZE).decode("utf-8")
                self.gelen_mesaj_signal.emit(msg)
            except OSError:
                break

app2 = QApplication([])
ekran = Birinci_ekran()
ekran.show()
app2.exec_()
