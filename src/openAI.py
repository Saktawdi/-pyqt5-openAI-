import threading

import openai
from PyQt5.QtCore import QMutex, pyqtSignal, QThread

qmut_1 = QMutex()


class AiThread(QThread):
    # 记忆存储
    localMsg = ""
    localRes = ""

    msg = ""
    res = ""
    finishSignal = pyqtSignal(str)

    def __init__(self, threadID, name, counter):
        super().__init__()
        self.threadID = threadID
        self.name = name
        self.counter = counter

    def run(self):
        # 在这里定义线程要执行的任务
        if self.msg == "":
            self.res = "错误！参数为空"
            print(self.res)
            self.finishSignal.emit("失败")

        else:
            qmut_1.lock()
            openai.api_key = "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"

            model_engine = "text-davinci-003"
            prompt = self.localMsg

            completion = openai.Completion.create(
                engine=model_engine,
                prompt=prompt,
                max_tokens=1024,
                n=1,
                stop=None,  # 停止符
                # stop=['\n'],
                temperature=0.5,
            )
            self.res = completion.choices[0].text.strip()
            print('AI:', self.res)
            # 存储每次答案
            self.localRes = self.localRes + self.res + '\n'
            # 存储记录
            self.localMsg = self.localMsg + self.res + '\n'
            qmut_1.unlock()
            self.finishSignal.emit(self.res)

    def setMsg(self, msg):
        self.msg = msg

    def appendLocalMsg(self, msg):
        self.localMsg = self.localMsg + msg + '\n'

    def getRes(self):
        return self.res
