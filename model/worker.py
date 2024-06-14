from PyQt5.QtCore import QObject, pyqtSignal, QThread


class worker(QThread):
    finished = pyqtSignal()
    result = pyqtSignal(object)

    def __init__(self, method, *args):
        super().__init__()
        self.method = method
        self.args = args

    def run(self):
        result = self.method(*self.args)
        self.result.emit(result)
        self.finished.emit()