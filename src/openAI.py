import threading

import openai
from PyQt5.QtCore import QMutex, pyqtSignal, QThread

qmut_1 = QMutex()


class AiThread(QThread):
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

            model_engine = "text-davinci-002"
            prompt = self.msg

            completion = openai.Completion.create(
                engine=model_engine,
                prompt=prompt,
                max_tokens=1024,
                n=1,
                stop=None,
                temperature=0.5,
            )
            self.res = completion.choices[0].text.strip()
            print(self.res)
            qmut_1.unlock()
            self.finishSignal.emit(self.res)

    def setMsg(self, msg):
        self.msg = msg

    def getRes(self):
        return self.res
