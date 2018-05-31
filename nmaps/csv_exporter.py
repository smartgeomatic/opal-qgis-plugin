import re
class LayerExport(object):

    def __init__(self, layer):
        self._layer = layer

    def get_source(self):
        layer_source = self._layer.source()
        file_search = re.search('file\:\/\/(.*)\?', layer_source, re.IGNORECASE)
        if not file_search:
            return layer_source
        path = str(file_search.group(1))
        is_win_path = re.search('\/[A-Z]:', path)
        if is_win_path:
            return path[1:]
        else:
            return path
