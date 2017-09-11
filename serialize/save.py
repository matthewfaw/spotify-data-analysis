import pickle
from datetime import datetime

def _uniquifiy(name):
    return "%s_%s"%(name,datetime.now())

def _get_filename(obj_name, op):
    return "data/%s.pickle"%(op(obj_name))

def save(obj, obj_name):
    filename = _get_filename(obj_name, _uniquifiy)
    with open(filename,'wb') as f:
        pickle.dump(obj,f)
    return filename

def load(obj_name):
    filename = _get_filename(obj_name, lambda x: x)
    with open(filename,'rb') as f:
        return pickle.load(f)
