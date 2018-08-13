from qgis.core import QgsMessageLog, QgsMapLayerRegistry, QgsMapLayer
from nmaps.nm_tus import NmTus
from nmaps.tilesets import Tilesets
import nm_config
import os
import time

class TilesetDialogHelper:

    job_progres_request_iterval = 2

    def progress_callback(self, value, label=None):
        self.progress_label.show()
        self.progress.show()
        self.progress_label.setText(label)
        self.progress.setValue(value)

    def select_layer(self):
        layer = None
        for lyr in QgsMapLayerRegistry.instance().mapLayers().values():
            if lyr.name() == self.cb.currentText():
                layer = lyr
                break

        return layer

    def _is_valid_layer(self, layer):
        if layer.type() == QgsMapLayer.VectorLayer:
            return True
        else:
            return False

    def get_layers(self):
        layers = self.parent.iface.legendInterface().layers()
        layer_list = []
        layer_list.append("")
        for layer in layers:
            if self._is_valid_layer(layer):
                layer_list.append(layer.name())

        return layer_list

    def upload_tileset(self,tp):
        tus = NmTus(nm_config.tileset_upload_url, tp)
        tus.add_header('X-Auth-Token', self.parent.nm_token.raw())
        tus.upload_callback(self.progress_callback)
        tus.upload()
        return tus

    def send_tileset(self,tmp_path, action):
        with open(tmp_path, 'rb') as tp:
            tus = self.upload_tileset(tp)
            til = Tilesets(self.parent.nm_token)
            tmp_file = os.path.basename(tmp_path)

            if action == 'create':
                til.create(tmp_file, tus.file_id())
            elif action == 'replace':
                til.replace(self.item, tmp_file, tus.file_id())

        self.parent.nmap_connect()