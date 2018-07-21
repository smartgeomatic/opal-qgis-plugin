from PyQt4.QtCore import QThread

class Notifier(QThread):

    def __init__(self, parentThread):
        QThread.__init__(self, parentThread)
        self.running = False
        self.total = 0
        self.currentCount = 0

    def run(self):
        self.running = True
        self.emit(SIGNAL("changed()"), "aaa")
        self.stop()

    def stop(self):
        self.running = False

