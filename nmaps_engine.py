# -*- coding: utf-8 -*-
"""
/***************************************************************************
 NmapsEngine
                                 A QGIS plugin
 Nmaps engine
                              -------------------
        begin                : 2018-03-11
        git sha              : $Format:%H$
        copyright            : (C) 2018 by WO
        email                : w.oronski@acrux.net.pl
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
import sys
import os
#sys.path.insert(0,os.path.join(os.path.dirname(__file__),"ext-libs/"))
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import QgsMessageLog
from qgis.gui import QgsMessageBar
from qgis.core import QgsMapLayerRegistry
# Initialize Qt resources from file resources.py
import resources
# Import the code for the dialog
from nmaps_engine_dialog import NmapsEngineDialog
import os.path

from nmaps.token import Token
from nmaps.apikey import ApiKey
from nmaps.authentication import Authentication
from nmaps.tilesets import Tilesets
from token_dialog import TokenDialog
from tileset_common_dialog import TilesetCommonDialog
from tileset_create_dialog import TilesetCreateDialog
from tileset_list_item import TilesetListItem
from nmaps import pickle_db

class NmapsEngine:
    """QGIS Plugin Implementation."""
    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgisInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        self.visible = False
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'NmapsEngine_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)


        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&Nmaps Engine')
        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u'NmapsEngine')
        self.toolbar.setObjectName(u'NmapsEngine')

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('NmapsEngine', message)


    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        # Create the dialog (after translation) and keep reference
        self.dlg = NmapsEngineDialog()

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/NmapsEngine/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'NMap'),
            callback=self.run,
            parent=self.iface.mainWindow())

        self.dlg.pushButton.clicked.connect(self.create_nmap)
        self.dlg.listWidget.itemDoubleClicked.connect(self.item_click)
        self.bar = QgsMessageBar(self.dlg)
        QObject.connect(self.iface.mapCanvas(), SIGNAL("layersChanged()"), self.nmap_connect)
        self.bar.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.bar.move(20,1)
        self.bar.setFixedSize(692, 40)


    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&Nmaps Engine'),
                action)
            self.iface.removeToolBarIcon(action)
        # remove the toolbar
        del self.toolbar


    def run(self):
        """Run method that performs all the real work"""
        # show the dialog
        self.iface.mainWindow().statusBar().showMessage("...")
        self.dlg.listWidget.clear()
        self.dlg.show()
        self.visible = True
        #self.bar.pushInfo("Serwer NMap", "Aby pobrać listę tilesetów musisz kliknąć Połącz".decode('utf-8'))
        # Run the dialog event loop
        self.nmap_connect()
        tileset_req = Tilesets(self.nm_token)
        notifications = tileset_req.jobs()
        for notification in notifications:
            if notification.get('status') == 'processing':
                self.bar.pushInfo("Serwer NMap", "Kafelkowanie ".decode('utf-8') + notification.get('originalname'))
            if notification.get('status') == 'success':
                self.bar.pushSuccess("Serwer NMap", "Ukończono ".decode('utf-8') + notification.get('originalname'))
            if notification.get('status') == 'error':
                self.bar.pushCritical("Serwer NMap", "Błąd ".decode('utf-8') + notification.get('originalname'))
            tileset_req.hide(notification.get('job_id'))
        result = self.dlg.exec_()
        # See if OK was pressed
        if result:
            # Do something useful here - delete the line containing pass and
            # substitute with your code.
            self.visible = False
            pass

    def nmap_connect(self):
        if self.visible:
            self.iface.mainWindow().statusBar().clear()
            self.bar.pushInfo("Serwer NMap","Łączenie z serwerem NMap".decode("utf-8"))
            try:
                token = Authentication(ApiKey(), 'qgis-plugin').authenticate()
                self.nm_token = Token(token)
            except:
                self.bar.pushCritical("Serwer NMap", "Nie udało się połączyć".decode("utf-8"))
                tkd = TokenDialog(self)
                tkd.dlg()
                return False

            try:
                tilesets = Tilesets(self.nm_token).list()
            except:
                self.bar.pushCritical("Serwer NMap", "Nie mogę pobrać danych".decode("utf-8"))
                return False

            self.bar.clearWidgets()
            self.bar.pushSuccess("Serwer NMap", "Połączono".decode('utf-8'))
            self.iface.mainWindow().statusBar().showMessage("Połączono".decode("utf-8"))

            tl = pickle_db.load_obj()

            avialble_layers = [layer.name() for layer in self.iface.legendInterface().layers()]

            self.dlg.listWidget.clear()
            for tileset in tilesets:
                tileset_list_item = TilesetListItem()
                tileset_list_item.setTextUp(tileset.get('id'))
                tileset_list_item.setTextDown(tileset.get('name'))
                if tileset.get('name') in tl and tl[tileset.get('name')] in avialble_layers:
                    tileset_list_item.setTextMiddle(tl[tileset.get('name')])
                if tileset.get('id') in tl and tl[tileset.get('id')] in avialble_layers:
                    tileset_list_item.setTextMiddle(tl[tileset.get('id')])
                tileset_list_item.setIcon(None)
                tileset_list_item_widget = QListWidgetItem(self.dlg.listWidget)
                tileset_list_item_widget.setSizeHint(tileset_list_item.sizeHint())
                self.dlg.listWidget.addItem(tileset_list_item_widget)
                self.dlg.listWidget.setItemWidget(tileset_list_item_widget, tileset_list_item)

            self.bar.clearWidgets()
            self.bar.pushSuccess("Serwer NMap", "Połączono i pobrano listę zestawów".decode('utf-8'))

    def item_click(self, item):
        current = item.listWidget().itemWidget(item)
        item_id    = current.getTextUp()
        item_label = current.getTextDown()
        TilesetCommonDialog(item_id, self).dlg(item_label)

    def create_nmap(self):
        TilesetCreateDialog(self).dlg()



