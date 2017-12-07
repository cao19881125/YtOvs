import hashlib
from PyQt4.QtCore import QString
import uuid

def get_uuid():
    return str(uuid.uuid1())


def to_python_str(from_str):
    if type(from_str) is QString:
        return str(unicode(from_str))
    else:
        return str(from_str)




def con_has_code( ip, port, schema):
    str_key = ip + ':' + str(port) + ':' + schema

    return hashlib.new('md5', str_key ).hexdigest()