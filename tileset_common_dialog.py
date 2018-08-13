# -*- coding: utf-8 -*-
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import QgsMessageLog, QgsMapLayerRegistry
from qgis.gui import QgsMessageBar

from nmaps.layer_exporter import LayerExporter
from nmaps.nm_tus import NmTus
from nmaps.tilesets import Tilesets
from nmaps import pickle_db
from tileset_dialog_helper import TilesetDialogHelper
import nm_config
import os
import time

class TilesetCommonDialog(QDialog,TilesetDialogHelper):


    def __init__(self, item, parent):
        super(TilesetCommonDialog, self).__init__()
        self.item = item
        self.parent = parent

    def dlg(self, item_label):

        self.progress_label = QLabel(self)
        self.progress_label.setText("Wysyłanie pliku:".decode("utf-8"))
        self.progress_label.move(10, 65)
        self.progress_label.hide()

        self.progress = QProgressBar(self)
        self.progress.setGeometry(120, 65, 250, 20)
        self.progress.hide()

        self.completed = 0

        button_save = QPushButton("Zapisz", self)
        button_save.move(10, 160)
        button_save.clicked.connect(self.save)

        button_replace = QPushButton("Zamień w NMap".decode("utf-8"), self)
        button_replace.move(100, 160)
        button_replace.clicked.connect(self.replace_nmap)

        button_remove = QPushButton("Usuń zestaw w NMap".decode("utf-8"), self)
        button_remove.move(215, 160)
        button_remove.clicked.connect(self.remove_nmap)

        item_info = QLabel(self)
        item_info.setText(item_label)
        item_info.move(10, 1)

        connect_label = QLabel(self)
        connect_label.setText("Powiąż z warstwą qgis:".decode("utf-8"))
        connect_label.move(10, 30)

        self.cb = QComboBox(self)
        self.cb.move(150, 25)
        self.cb.clear()
        self.cb.addItems(self.get_layers())
        tl = pickle_db.load_obj()
        item_name = item_label.split(":")[1].strip()
        if item_name in tl:
            layer = tl[item_name]
            index = self.cb.findText(layer, Qt.MatchFixedString)
            if index >= 0:
                self.cb.setCurrentIndex(index)
        if self.item in tl:
            layer = tl[self.item]
            index = self.cb.findText(layer, Qt.MatchFixedString)
            if index >= 0:
                self.cb.setCurrentIndex(index)

        self.setWindowTitle("Konfiguracja powiązania".decode('utf-8'))
        self.setFixedSize(600, 200)
        self.setWindowModality(Qt.ApplicationModal)
        self.exec_()


    def tileset_to_layer(self):
        tl = pickle_db.load_obj()
        layer = self.select_layer()
        if not layer:
            if self.item in tl:
                del tl[self.item]
                pickle_db.save_obj(tl)
        else:
            if not tl:
                pickle_db.save_obj({self.item: layer.name()})
            else:
                tl.update({self.item: layer.name()})
                pickle_db.save_obj(tl)
        self.parent.nmap_connect()

    def save(self):
        self.tileset_to_layer()
        self.close()

    def replace_nmap(self):
        self.parent.bar.pushSuccess("Serwer NMap", "Połączono".decode('utf-8') + " " + self.item + " z " + self.cb.currentText())
        layer = self.select_layer()
        if not layer:
            self.parent.bar.pushCritical("Serwer NMap", "Proszę wybrać warstwę".decode('utf-8'))
            return False

        try:
            tmp_path = LayerExporter(layer).export_source()
        except:
            self.parent.bar.pushCritical("Serwer NMap", "Eksport pliku tymczasowego nie powiódł się".decode('utf-8'))

        try:
            self.send_tileset(tmp_path, 'replace')
            self.parent.bar.pushSuccess("Serwer NMap", "Eksport pliku powiódł się".decode('utf-8'))
        except:
            self.parent.bar.pushCritical("Serwer NMap", "Eksport pliku nie powiódł się".decode('utf-8'))
        self.tileset_to_layer()
        self.close()

    def remove_nmap(self):
        reply = QMessageBox.question(self.parent.iface.mainWindow(), 'Usuwanie zestawu',
                                     "Czy chcesz usunąć zestaw kafelków ? Usunięcie kafelków spowoduje, "
                                     "że Twoje publikacje przestaną działać. "
                                     "Pamiętaj, że akcja nie może być cofnięta!".decode('utf-8'), QMessageBox.Yes, QMessageBox.No)
        if reply == QMessageBox.Yes:
            try:
                til = Tilesets(self.parent.nm_token)
                til.remove(self.item)
                self.parent.bar.pushSuccess("Serwer NMap", "Usunięcie zestawu powiodło się".decode('utf-8'))
            except:
                self.parent.bar.pushCritical("Serwer NMap", "Usunięcie zestawu nie powiodło się".decode('utf-8'))
            self.parent.nmap_connect()
            self.close()
        else:
            self.close()
        self.parent.iface.mainWindow().show()
        self.parent.iface.mainWindow().setWindowState(self.parent.iface.mainWindow().windowState() & ~Qt.WindowMinimized | Qt.WindowActive)
        self.parent.iface.mainWindow().activateWindow()
