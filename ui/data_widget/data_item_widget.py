import sys
from PyQt4.QtGui import QApplication
from PyQt4.QtGui import QWidget
from PyQt4.QtGui import QTableWidget
from PyQt4.QtGui import QVBoxLayout
from PyQt4.QtGui import QHBoxLayout
from PyQt4.QtGui import QHeaderView
from PyQt4.QtGui import QTableWidgetItem
from PyQt4.QtCore import QStringList
from PyQt4.QtCore import Qt
from db_connection.connection_manager import ConnectionManager

class DataItemWidget(QWidget):
    def __init__(self, con_key, table_name):
        QWidget.__init__(self)
        self.__con_key = con_key
        self.__table_name = table_name
        self.__setup_ui()
        self.__init_data()


    def __setup_ui(self):


        v_layout = QVBoxLayout()

        self.__tool_widget = QWidget()

        h_layout = QHBoxLayout()
        self.__data_table_widget = QTableWidget()
        self.__data_table_widget.horizontalHeader().setStretchLastSection(True)
        self.__data_table_widget.horizontalHeader().setResizeMode(0,QHeaderView.Fixed)

        h_layout.addWidget(self.__data_table_widget)


        #v_layout.addWidget(self.__tool_widget)
        v_layout.addLayout(h_layout)
        self.setLayout(v_layout)


    def __init_data(self):


        yt_connection = ConnectionManager().get_connection(self.__con_key)
        if not yt_connection:
            print 'DataItemWidget:get con failed'
            return
        result = yt_connection.get_table_data(self.__table_name)

        self.__data_table_widget.clearContents()

        # init header
        self.__colume_names = yt_connection.get_table_colume_names(self.__table_name)
        self.__colume_names.insert(0,'uuid')

        print self.__colume_names

        self.__data_table_widget.setColumnCount(len(self.__colume_names))
        head_list = QStringList()
        for colume in self.__colume_names:
            head_list << colume

        self.__data_table_widget.setHorizontalHeaderLabels(head_list)


        #self.__data_table_widget.horizontalHeader().setResizeMode(QHeaderView.Stretch)

        # init data
        data = yt_connection.get_table_data(self.__table_name)

        self.__update_table(data)
        self.__data_table_widget.resizeColumnsToContents()

    '''
    data like this
    [
    {u'direction': 'to-lport', 
    u'name': '[]', 
    u'priority': '100', 
    u'log': 'true', 
    u'action': 'drop', 
    u'external_ids': '{"neutron:lport"="5fb77332-2035-4f72-8e57-7415b02489c9"}', 
    u'match': '"outport==\\"inside-vm2\\""', 
    u'severity': '[]',
    'uuid': '2890a832-1c83-4b8e-8b40-2928817012cc'}
    ]

    '''
    def __update_table(self,data):
        self.__data_table_widget.clearContents()

        row_num = 0
        for row in data:
            self.__data_table_widget.insertRow(row_num)
            colume_num = 0
            for colume in self.__colume_names:
                item_str = row[colume]
                table_wid_item = QTableWidgetItem(item_str)
                table_wid_item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
                self.__data_table_widget.setItem(row_num,colume_num,table_wid_item)
                colume_num += 1
            row_num += 1



if __name__ == '__main__':
    ret,con = ConnectionManager().connect_to('192.168.184.128', 6641, 'OVN_Northbound')

    app = QApplication(sys.argv)

    test_widget = DataItemWidget(con, 'ACL')

    test_widget.show()
    sys.exit(app.exec_())
