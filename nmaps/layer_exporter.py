# -*- coding: utf-8 -*-
from nm_tus import NmTus
from qgis.core import QgsMessageLog, QgsVectorFileWriter
import os, pprint, re, zipfile, glob

class LayerExporter:

    def __init__(self, layer):
        self.layer = layer

    def export_source(self):

        if "csv" in self.layer.source() and "csv" in self.layer.metadata():

            file_search = re.search('file\:\/\/(.*)\?', self.layer.source(), re.IGNORECASE)
            if file_search:
                path = str(file_search.group(1))
                is_win_path = re.search('\/[A-Z]:', path)
                if is_win_path:
                    return path[1:]
                else:
                    return path
            else:
                return self.layer.source()

        elif "json" in self.layer.source() and "json" in self.layer.metadata():
            return self.layer.source().split("|")[0]

        elif "Shapefile" in self.layer.metadata():
            path = self.layer.source()
            file_template = '*.*'

            if os.path.isfile(path):
                filename_w_ext = os.path.basename(path)
                file_template, file_extension = os.path.splitext(filename_w_ext)
                path = os.path.dirname(path)

            zip_name  = self.layer.name()
            zip_path  = os.path.join(os.path.dirname(__file__), "..", "tmp", zip_name + ".zip")
            abs_src   = os.path.abspath(path)
            zf = zipfile.ZipFile(zip_path, "w")
            for root, dirs, files in os.walk(path):
                for filename in files:
                    absname = os.path.abspath(os.path.join(root, filename))
                    arcname = absname[len(abs_src) + 1:]
                    if file_template is '*.*' or file_template in arcname:
                        zf.write(absname, arcname)

            zf.close()
            return zip_path

        else:
            return False


