# import windows
#
# windows.showUi()

import sys
import threading
import docx
import pyperclip

from PyQt5.QtWidgets import QApplication, QMainWindow,QMessageBox

from openAI import AiThread
from ui import *
from PyQt5.QtCore import Qt, QTimer, QPropertyAnimation
from PyQt5.QtGui import QMouseEvent, QCursor


class MainWindows(QMainWindow, Ui_MainWindow):
    # 创建AI对象
    aiThread = AiThread(1, "AiThread-1", 1)
    # 是否初始化AI对象连接信号槽
    initFinishSignalIf = False

    def __init__(self, parent=None):
        super(MainWindows, self).__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        # 按钮
        self.close_pushButton.clicked.connect(self.close)
        self.hidden_pushButton.clicked.connect(self.showMinimized)
        self.send_pushButton.clicked.connect(self.onSendButtonClick)
        self.pushButton_clear.clicked.connect(self.onClearButtonClick)
        self.pushButton_copy.clicked.connect(self.onCopyButtonClick)
        self.pushButton_toDoc.clicked.connect(self.onToDocButtonClick)


    # 窗口拖动
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

    # 提示框
    def showMsgBox(self,msg):
        TipBox = QMessageBox(self.widget)
        TipBox.setText(msg)
        TipBox.setWindowFlags(TipBox.windowFlags() | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.WindowStaysOnTopHint)
        # TipBox.setStandardButtons(QMessageBox.NoButton)
        TipBox.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        TipBox.show()
        # 创建动画
        animation = QPropertyAnimation(TipBox, b"windowOpacity",self)
        animation.setStartValue(0.5)
        animation.setEndValue(1)
        animation.setDuration(500)

        # 启动动画
        animation.start()

        QTimer.singleShot(800, TipBox.close)
        pass

    # 提问按钮逻辑
    def onSendButtonClick(self):
        thread1 = threading.Thread(target=self.appendUserText(), args=())
        thread1.start()
        thread1.join()

        print("AiThread-1Running")
        # 连接信号槽：等待AI线程结束后添加答案文本
        if not self.initFinishSignalIf:
            self.aiThread.finishSignal.connect(self.appendResText)
            self.initFinishSignalIf = True
        # 添加询问文本到ai对象
        self.aiThread.setMsg(self.sendMsg)
        # 记忆存储询问信息到ai对象
        self.aiThread.appendLocalMsg(self.sendMsg)
        # 启动AI线程
        self.aiThread.start()
        self.send_pushButton.setEnabled(False)

    # 删除按钮逻辑
    def onClearButtonClick(self):
        self.plainTextEdit.document().setPlainText("")
        self.user_lineEdit.setPlaceholderText('')
        self.aiThread.localMsg = ''
        self.aiThread.localRes = ''
        self.showMsgBox("删除成功")
        print("删除按钮：", "成功")
        pass

    # 复制按钮逻辑
    def onCopyButtonClick(self):
        pyperclip.copy(self.aiThread.res)
        self.showMsgBox("复制成功")
        print("复制按钮：", "成功")
        pass

    # 导出doc按钮逻辑
    def onToDocButtonClick(self):
        # 创建一个新的文档
        doc = docx.Document()
        # 在文档中添加一段文本
        doc.add_paragraph(self.aiThread.localRes)
        # 保存文档
        doc.save('out.docx')
        self.showMsgBox("成功导出到软件目录")
        print("导出按钮：", "成功")
        pass


    # 添加文本
    def appendUserText(self):

        print("appendText-1Running")
        self.sendMsg = self.user_lineEdit.text()
        self.user_lineEdit.setText("")
        self.user_lineEdit.setPlaceholderText(self.sendMsg)
        print(self.sendMsg)
        # 创建QTextCharFormat对象
        char_format = QtGui.QTextCharFormat()
        # 设置字体颜色
        char_format.setForeground(QtGui.QColor('red'))

        # 设置设定
        self.plainTextEdit.mergeCurrentCharFormat(char_format)
        # 添加用户提问的文本
        self.plainTextEdit.appendPlainText("您：" + self.sendMsg)
        # 恢复设定
        char_format.setForeground(QtGui.QColor('black'))
        self.plainTextEdit.mergeCurrentCharFormat(char_format)

    # 添加答案文本
    def appendResText(self, msg):
        print("appendResText-1Running")
        self.send_pushButton.setEnabled(True)
        if msg != "失败":
            self.plainTextEdit.appendPlainText("ChatGPT：" + msg)
        else:
            self.plainTextEdit.appendPlainText("ChatGPT：处理失败。")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mywin = MainWindows()
    mywin.show()
    sys.exit(app.exec_())
