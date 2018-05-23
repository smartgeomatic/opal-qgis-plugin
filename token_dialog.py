# -*- coding: utf-8 -*-
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import QgsMessageLog
from qgis.gui import QgsMessageBar
from qgis.core import QgsMapLayerRegistry
from nmaps.apikey import ApiKey

class TokenDialog:
    def __init__(self, parent):
        self.parent = parent

    def dlg(self):
        self.parent.bar.clearWidgets()
        self.parent.bar.pushCritical("Serwer NMap",
                              "Błąd połączenia sprawdź poprawność API KEY i spróbuj ponownie".decode('utf-8'))
        self.parent.iface.mainWindow().statusBar().showMessage("Wprowadź klucz API".decode("utf-8"))

        self.d = QDialog()

        b = QPushButton("Zapisz", self.d)
        b.move(10, 160)
        b.clicked.connect(self.close)

        self.c = QPlainTextEdit(self.d)
        self.c.insertPlainText(ApiKey().read())
        self.c.move(10, 1)
        self.c.resize(580, 50)

        self.d.setWindowTitle("Klucz api")
        self.d.setFixedSize(600, 200)
        self.d.setWindowModality(Qt.ApplicationModal)
        self.d.exec_()

    def close(self):
        ApiKey().set(self.c.toPlainText())
        self.parent.nmap_connect()
        self.d.close()
