# -*- coding: utf-8 -*-
from PyQt4.QtCore import *
from PyQt4.QtGui import *

class TilesetListItem(QWidget):
    def __init__(self, parent=None):
        super(TilesetListItem, self).__init__(parent)
        self.textQVBoxLayout = QVBoxLayout()
        self.textUpQLabel = QLabel()
        self.textUpQLabel.hide()
        self.textDownQLabel = QLabel()
        self.textMiddleQLabel = QLabel()
        self.textQVBoxLayout.addWidget(self.textUpQLabel)
        self.textQVBoxLayout.addWidget(self.textDownQLabel)
        self.textQVBoxLayout.addWidget(self.textMiddleQLabel)
        self.allQHBoxLayout = QHBoxLayout()
        self.iconQLabel = QLabel()
        self.allQHBoxLayout.addWidget(self.iconQLabel, 0)
        self.allQHBoxLayout.addLayout(self.textQVBoxLayout, 1)
        self.setLayout(self.allQHBoxLayout)

    def setTextUp(self, text):
        self.textUpQLabel.setText(text)

    def setTextMiddle(self, text):
        text = "Warstwa Qgis: " + text
        self.textMiddleQLabel.setText(text)

    def setTextDown(self, text):
        text = "Zestaw kafelków w NMaps: ".decode("utf-8") + text
        self.textDownQLabel.setText(text)

    def getTextDown(self):
        return self.textDownQLabel.text()

    def getTextMiddle(self):
        return self.textMiddleQLabel.text()

    def getTextUp(self):
        return self.textUpQLabel.text()

    def setIcon(self, imagePath):
        self.iconQLabel.setPixmap(QPixmap(imagePath))
