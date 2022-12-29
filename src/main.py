

# import windows
#
# windows.showUi()

import sys

from PyQt5.QtWidgets import QApplication,QMainWindow

from openAI import AiThread
from ui import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QMouseEvent, QCursor

class MainWindows(QMainWindow,Ui_MainWindow):
    aiThread = object
    def __init__(self,parent=None):
        super(MainWindows,self).__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        #按钮
        self.close_pushButton.clicked.connect(self.close)
        self.hidden_pushButton.clicked.connect(self.showMinimized)
        self.send_pushButton.clicked.connect(self.onSendButtonClick)


    #窗口拖动
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.m_flag = True
            self.m_Position = event.globalPos() - self.pos()
            event.accept()
            self.setCursor(QCursor(Qt.OpenHandCursor))

    def mouseMoveEvent(self, QMouseEvent):
        if Qt.LeftButton and self.m_flag:
            self.move(QMouseEvent.globalPos() - self.m_Position)
            QMouseEvent.accept()

    def mouseReleaseEvent(self, QMouseEvent):
        self.m_flag = False
        self.setCursor(QCursor(Qt.ArrowCursor))

    def onSendButtonClick(self):
        thread1 = threading.Thread(target=self.appendUserText(), args=())
        thread1.start()
        thread1.join()

        print("AiThread-1Running")
        self.aiThread = AiThread(1, "AiThread-1", 1)
        self.aiThread.setMsg(self.sendMsg)
        self.aiThread.finishSignal.connect(self.appendResText)
        self.aiThread.start()
        self.send_pushButton.setEnabled(False)

    def appendUserText(self):
        # 获取输入框中的文本
        print("appendText-1Running")
        self.sendMsg = self.user_lineEdit.text()
        self.user_lineEdit.setText("")
        self.user_lineEdit.setPlaceholderText(self.sendMsg)
        print(self.sendMsg)
        self.plainTextEdit.appendPlainText("您：" + self.sendMsg)

    def appendResText(self,msg):
        print("appendResText-1Running")
        self.send_pushButton.setEnabled(True)
        if msg != "失败":
            self.plainTextEdit.appendPlainText("ChatGPT：" + msg)
        else:
            self.plainTextEdit.appendPlainText("ChatGPT：处理失败。")



if __name__=="__main__":
    app=QApplication(sys.argv)
    mywin=MainWindows()
    mywin.show()
    sys.exit(app.exec_())



