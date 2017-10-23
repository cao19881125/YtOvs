from PyQt4.QtCore import QString

def to_python_str(from_str):
    if type(from_str) is QString:
        return str(unicode(from_str))
    else:
        return str(from_str)

