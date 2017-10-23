import connection
from command.list_table_cmd import ListTableCmd
from command.dump_table_cmd import DumpTableCmd
from command.get_table_structure_cmd import GetTableStructureCmd

class YtDbConnection(object):
    def __init__(self, ip, port, db_schema):
        self.__ip = ip
        self.__port = port
        self.__con_str = 'tcp:' + ip + ':' + str(port)
        self.__db_schema = db_schema
        self.__connection = connection.Connection(self.__con_str, 180, self.__db_schema)
        self.__table_names = []
        self.__connected = False

    def connect(self):
        if self.__connected:
            return
        try:
            self.__connection.start()
        except Exception:
            return False
        self.__get_tables_names_from_db()
        self.__connected = True
        return True

    def __get_tables_names_from_db(self):
        list_cmd = ListTableCmd(self.__connection)
        self.__connection.queue_txn(list_cmd)
        result = list_cmd.get_result(5)
        self.__table_names = result

    def get_table_names(self):
        return self.__table_names

    def get_table_data(self, table_name):
        dump_table_cmd = DumpTableCmd(self.__connection, table_name)
        self.__connection.queue_txn(dump_table_cmd)
        result = dump_table_cmd.get_result(5)
        return result

    def get_table_colume_names(self, table_name):
        get_colume_names_cmd = GetTableStructureCmd(self.__connection, table_name)
        self.__connection.queue_txn(get_colume_names_cmd)
        result_struct = get_colume_names_cmd.get_result(5)
        result = []

        for colume in result_struct:
            result.append(colume)

        return result

    def get_con_info(self):
        return self.__ip,self.__port,self.__db_schema


if __name__ == '__main__':
    #yt_con = YtDbConnection('tcp:192.168.184.128:6641', 'OVN_Northbound')
    yt_con = YtDbConnection('192.168.184.128', 6641, 'OVN_Northbound')
    if yt_con.connect():
        #print str(yt_con.get_table_names())
        print str(yt_con.get_table_data('ACL'))
        #print str(yt_con.get_table_colume_names('ACL'))
    else:
        print 'con failed'
