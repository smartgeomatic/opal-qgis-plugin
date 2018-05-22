import pickle
import os

def save_obj(obj):
    with open(os.path.join(os.path.dirname(__file__), '..', 'db.pkl'), 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)
        return True


def load_obj():
    with open(os.path.join(os.path.dirname(__file__), '..', 'db.pkl'), 'rb') as f:
        try:
            tl = pickle.load(f)
        except:
            tl = {}

        return tl
