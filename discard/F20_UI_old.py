# author:nerako
# This program is used to create a dialog AI form.
# -----------------------2024.2.13-------------------------
import record_wav
import microphone_ASR
import wav_ASR

import thread
import sys
import signal
import time
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTextEdit, QStatusBar, QMainWindow, QInputDialog, \
    QPushButton, QLineEdit, QLabel, QSizePolicy
from PyQt5.QtCore import pyqtSignal, QThread, Qt, QMutex

q_lock_edit = QMutex()
q_lock_ASR = QMutex()

# 继承QThread
class Edit_Thread(QThread):  # 线程1
    def __init__(self,text,parent=None):
        super(Edit_Thread, self).__init__(parent)
        self.ex = parent
        self.text = text

    def run(self):
        q_lock_edit.lock()  # 加锁
        self.ex.textEdit.append(self.text)
        self.ex.textEdit.ensureCursorVisible()
        # time.sleep(1)
        q_lock_edit.unlock()  # 解锁

# 继承QThread
class ASR_Thread(QThread):  # 线程1
    _signal = pyqtSignal(str)

    def __init__(self,):
        super(ASR_Thread, self).__init__()

    def run(self):
        q_lock_ASR.lock()  # 加锁
        ans = "speaker:"+microphone_ASR.set_up()
        self._signal.emit(ans)
        q_lock_ASR.unlock()  # 解锁

class ImageWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.centralWidget = QWidget(self)
        self.setCentralWidget(self.centralWidget)
        layout = QVBoxLayout(self.centralWidget)

class dia_UI(QWidget):
    def __init__(self, parent=None):
        super(dia_UI, self).__init__(parent)
        self.InitUI()
        self.imageWindow = ImageWindow()

    def InitUI(self):
        # self.le = QLineEdit(self)
        # self.le.move(130, 22)

        self.setWindowTitle("F20CA Dialogue System")
        self.layout = QVBoxLayout(self)

        # Create and add a head bar
        self.statusBar_head = QStatusBar(self)
        self.statusBar_head.resize(300, 30)
        self.statusBar_head.setStyleSheet("color:rgb(10,10,10,255);font-size:30px;font-weight:bold;font-family:Roman times;")
        self.layout.addWidget(self.statusBar_head)
        self.statusBar_head.showMessage("Conversational Agents and Spoken Language Processing")


        # Create and add a tip bar
        self.statusBar_wel = QStatusBar(self)
        self.layout.addWidget(self.statusBar_wel)
        self.statusBar_wel.showMessage("You Can Say Whatever You Like:")

        # Create a QTextEdit for displaying text
        self.textEdit = QTextEdit(self)
        self.textEdit.setReadOnly(True)  # Make the QTextEdit read-only
        self.textEdit.setWordWrapMode(True)  # Enable word wrapping
        self.textEdit.move(10, 300)
        self.textEdit.setFixedSize(1270, 300)

        # Create a Real-time conversion text
        self.textEdit_real = QTextEdit(self)
        self.textEdit_real.setReadOnly(True)  # Make the QTextEdit read-only
        self.textEdit_real.setWordWrapMode(True)  # Enable word wrapping
        self.textEdit_real.move(10, 700)
        self.textEdit_real.setFixedSize(1270, 150)
        # self.layout.addWidget(self.textEdit_real)

        # Create and add a status bar
        self.statusBar_sta = QStatusBar(self)
        self.layout.addWidget(self.statusBar_sta)
        self.statusBar_sta.showMessage("I am listening")

        self.btn = QPushButton("speak", self)
        self.btn.move(1180, 955)
        # self.btn.clicked.connect(self.ShowDialog)

        self.setFixedSize(1300, 1000)
        self.show()

    def update_text(self, text):
        self.thread = Edit_Thread(text,self)  # 创建线程
        self.thread.start()  # 开始线程

    # def ASR_start(self):
    #     self.thread = ASR_Thread(self)  # 创建线程
    #     self.thread.start()  # 开始线程

    def update_status(self, message):
        self.statusBar_sta.showMessage(message)

    def Stop(self):
        self.thread.terminate()  # 终止线程

# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     ex = dia_UI()
#     ex.update_text("hello can you hear me")
#     ex.update_text("can you work properly")
#     ex.update_text("can you work properly")
#     ex.update_text("can you work properly")
#     ex.update_status("I'm thinking")
#     sys.exit(app.exec_())