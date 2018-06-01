# -*- coding: utf-8 -*-
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import QgsMessageLog, QgsMapLayerRegistry
from qgis.gui import QgsMessageBar

from nmaps.layer_exporter import LayerExporter
from nmaps.tilesets import Tilesets
from tileset_dialog_helper import TilesetDialogHelper
from nmaps import pickle_db

import os
import time


class TilesetCreateDialog(QDialog,TilesetDialogHelper):

    def __init__(self, parent):
        super(TilesetCreateDialog, self).__init__()
        self.parent = parent

    def dlg(self):
        self.progress_label = QLabel(self)
        self.progress_label.setText("Wysyłanie pliku:".decode("utf-8"))
        self.progress_label.move(10, 65)
        self.progress_label.hide()

        self.progress = QProgressBar(self)
        self.progress.setGeometry(120, 65, 250, 20)
        self.progress.hide()

        self.completed = 0

        self.button_add = QPushButton("Dodaj do NMap".decode("utf-8"), self)
        self.button_add.move(10, 160)
        self.button_add.clicked.connect(self.create_nmap)

        choose_label = QLabel(self)
        choose_label.setText("Wybierz warstwę qgis:".decode("utf-8"))
        choose_label.move(10, 30)

        self.cb = QComboBox(self)
        self.cb.move(150, 25)

        self.cb.clear()
        self.cb.addItems(self.get_layers())

        self.setWindowTitle("Dodawanie zestawu")
        self.setFixedSize(600, 200)
        self.setWindowModality(Qt.ApplicationModal)
        self.exec_()


    def create_nmap(self):
        self.button_add.setEnabled(False)
        self.button_add.setDisabled(True)
        layer = self.select_layer()
        if not layer:
            self.parent.bar.pushCritical("Serwer NMap", "Proszę wybrać warstwę".decode('utf-8'))
            self.button_add.setDisabled(False)
            self.button_add.setEnabled(True)
            return False
        try:
            tmp_path = LayerExporter(layer).export_source()
        except:
            self.parent.bar.pushCritical("Serwer NMap", "Eksport pliku tymczasowego nie powiódł się".decode('utf-8'))

        try:
            self.send_tileset(tmp_path, 'create')
            self.tileset_to_layer(os.path.basename(tmp_path))
            self.parent.bar.pushSuccess("Serwer NMap", "Eksport pliku powiódł się".decode('utf-8'))
        except:
            self.parent.bar.pushCritical("Serwer NMap", "Eksport pliku nie powiódł się".decode('utf-8'))
        self.close()
        self.button_add.setDisabled(False)
        self.button_add.setEnabled(True)


    def tileset_to_layer(self, tmp_path):
        tl = pickle_db.load_obj()
        layer = self.select_layer()
        if not tl:
            pickle_db.save_obj({tmp_path: layer.name()})
        else:
            tl.update({tmp_path: layer.name()})
            pickle_db.save_obj(tl)
        self.parent.nmap_connect()



