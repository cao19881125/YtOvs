import hashlib
from yt_db_connection import YtDbConnection
from utils.singleton import singleton

@singleton
class ConnectionManager(object):
    def __init__(self):
        self.__connections = {}

    def connect_to(self, ip, port, schema):
        hash_key = self.__has_code(ip,port)

        if self.__connections.has_key(hash_key):
            print 'already has connect:' + ip + ':' + str(port)
            return False, None
        else:
            con = YtDbConnection(ip, port, schema)
            if not con.connect():
                print 'connect to ' + ip + ':' + str(port) +' ' + schema + ' failed'
                return False, None
            else:
                self.__connections[hash_key] = con
                return True, hash_key


    def get_connection(self, hash_key):
        return self.__connections[hash_key] if self.__connections.has_key(hash_key) else None

    def __has_code(self, ip, port):
        str_key = ip + ':' + str(port)

        return hashlib.new('md5', str_key ).hexdigest()

if __name__ == '__main__':
    ret,con = ConnectionManager().connect_to('192.168.184.128', 6641, 'OVN_Northbound')
    if ret:
        connection = ConnectionManager().get_connection(con)
        print connection.get_table_names()