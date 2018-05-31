from qgis.core import QgsMessageLog, QgsMapLayerRegistry
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

    def get_layers(self):
        layers = self.parent.iface.legendInterface().layers()
        layer_list = []
        layer_list.append("")
        for layer in layers:
            layer_list.append(layer.name())

        return layer_list

    def upload_tileset(self,tp):
        tus = NmTus(nm_config.tileset_upload_url, tp)
        tus.add_header('X-Auth-Token', self.parent.nm_token.raw())
        tus.upload_callback(self.progress_callback)
        tus.upload()
        return tus

    def send_tileset(self,tmp_path, action):
        tiling = 1
        with open(tmp_path, 'rb') as tp:
            tus = self.upload_tileset(tp)
            til = Tilesets(self.parent.nm_token)
            tmp_file = os.path.basename(tmp_path)

            if action == 'create':
                til.create(tmp_file, tus.file_id())
            elif action == 'replace':
                til.replace(self.item, tmp_file, tus.file_id())

            self.progress_callback(tiling, "Kafelkowanie:".decode("utf-8"))
            time.sleep(self.job_progres_request_iterval)
            while tiling < 100:
                tiling = til.job('progress')
                print tiling
                self.progress_callback(tiling, "Kafelkowanie:".decode("utf-8"))
                time.sleep(self.job_progres_request_iterval)
        self.parent.nmap_connect()
