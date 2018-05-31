# -*- coding: utf-8 -*-
import imp, os

class LayerExporter(object):

    def __init__(self, layer):
        self.layer = layer
        self._find_type()

    def _find_type(self):

        if self._source_name("csv") and self._matadata_type("csv"):
            self._exporter = "csv"

        elif self._source_name("json") and self._matadata_type("json"):
            self._exporter = "geojson"

        elif self._matadata_type("Shapefile"):
            self._exporter = "shape"

        else:
            raise Exception("Not a proper layer type")

    def _source_name(self, name):
        return name in self.layer.source()

    def _matadata_type(self, type):
        return type in self.layer.metadata()


    def export_source(self):
        try:
            module = '%s_exporter' % (self._exporter)
            exporter = imp.load_source(module, os.path.join(os.path.dirname(os.path.abspath(__file__)), '%s.py' % (module)))
            exporter_class = getattr(exporter, 'LayerExport')
            exporter_instance = exporter_class(self.layer)
            return exporter_instance.get_source()
        except:
            raise Exception("Can't find exporter")

