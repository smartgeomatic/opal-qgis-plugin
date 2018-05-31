import os, re, zipfile, glob


class LayerExport(object):

    def __init__(self, layer):
        self._layer = layer

    def get_source(self):
        path = self._layer.source()
        file_template = '*.*'

        if os.path.isfile(path):
            filename_w_ext = os.path.basename(path)
            file_template, file_extension = os.path.splitext(filename_w_ext)
            path = os.path.dirname(path)

        zip_name = self._layer.name()
        zip_path = os.path.join(os.path.dirname(__file__), "..", "tmp", zip_name + ".zip")
        abs_src = os.path.abspath(path)
        zf = zipfile.ZipFile(zip_path, "w")
        for root, dirs, files in os.walk(path):
            for filename in files:
                absname = os.path.abspath(os.path.join(root, filename))
                arcname = absname[len(abs_src) + 1:]
                if file_template is '*.*' or file_template in arcname:
                    zf.write(absname, arcname)

        zf.close()
        return zip_path
