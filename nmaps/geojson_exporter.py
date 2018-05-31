class LayerExport():

    def __init__(self, layer):
        self._layer = layer

    def get_source(self):
        return self._layer.source().split("|")[0]