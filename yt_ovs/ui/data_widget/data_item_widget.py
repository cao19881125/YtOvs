import sys
from PyQt4.QtGui import QApplication
from PyQt4.QtGui import QWidget
from PyQt4.QtGui import QTableWidget
from PyQt4.QtGui import QVBoxLayout
from PyQt4.QtGui import QHeaderView
from PyQt4.QtGui import QTableWidgetItem
from PyQt4.QtCore import QStringList
from PyQt4.QtCore import Qt
from PyQt4.QtCore import pyqtSlot
from PyQt4.QtCore import SIGNAL
from PyQt4.QtCore import SLOT
from db_connection.connection_manager import ConnectionManager
from tool_widget import ToolWidget

class DataItemWidget(QWidget):
    __EXTRA_COLUMN_WIDTH = 20
    def __init__(self, con_key, table_name):
        QWidget.__init__(self)
        self.__con_key = con_key
        self.__table_name = table_name
        self.__setup_ui()
        self.__init_data()
        self.__connect_slot()


    def __setup_ui(self):


        v_layout = QVBoxLayout()

        self.__tool_widget = ToolWidget()

        self.__tool_widget.setMaximumHeight(40)

        self.__data_table_widget = QTableWidget()
        self.__data_table_widget.horizontalHeader().setStretchLastSection(True)
        self.__data_table_widget.horizontalHeader().setResizeMode(0,QHeaderView.Fixed)


        v_layout.setSpacing(0)
        v_layout.setContentsMargins(0,0,0,0)
        v_layout.addWidget(self.__tool_widget,0)
        v_layout.addWidget(self.__data_table_widget,1)
        self.setLayout(v_layout)

    def __connect_slot(self):
        self.connect(self.__tool_widget,SIGNAL('refresh_btn_clicked()'), self ,SLOT('__on_refresh_signal()'))

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

        #print self.__colume_names

        self.__data_table_widget.setColumnCount(len(self.__colume_names))
        head_list = QStringList()
        for colume in self.__colume_names:
            head_list << colume

        self.__data_table_widget.setHorizontalHeaderLabels(head_list)

        # default the header column both sides are coverd, these codes add __EXTRA_COLUMN_WIDTH to the header column width
        # and reise column width in function self.__adjust_table_colume()
        self.__data_table_widget.horizontalHeader().setResizeMode(QHeaderView.ResizeToContents)
        self.__record_colume_header_width()
        self.__data_table_widget.horizontalHeader().setResizeMode(QHeaderView.Interactive)

        self.__record_colume_header_width()



        # init data
        data = yt_connection.get_table_data(self.__table_name)

        self.__update_table(data)
        self.__adjust_table_colume()

    def __record_colume_header_width(self):
        count = self.__data_table_widget.columnCount()
        self.__column_widths = []
        for i in range(count):
            self.__column_widths.append(self.__data_table_widget.columnWidth(i) + self.__EXTRA_COLUMN_WIDTH)

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

    def __clear_table_data(self):
        row_count = self.__data_table_widget.rowCount()
        rev = [i for i in range(row_count)]
        rev.reverse()
        for i in rev:
            self.__data_table_widget.removeRow(i)

    def __adjust_table_colume(self):
        self.__data_table_widget.resizeColumnsToContents()
        count = self.__data_table_widget.columnCount()
        for i in range(count):
            col_wid = self.__data_table_widget.columnWidth(i)
            if col_wid < self.__column_widths[i]:
                self.__data_table_widget.setColumnWidth(i, self.__column_widths[i])

    @pyqtSlot()
    def __on_refresh_signal(self):
        yt_connection = ConnectionManager().get_connection(self.__con_key)
        if not yt_connection:
            print 'DataItemWidget:get con failed'
            return
        #self.__data_table_widget.clearContents()
        self.__clear_table_data()

        data = yt_connection.get_table_data(self.__table_name)

        self.__update_table(data)
        self.__adjust_table_colume()


if __name__ == '__main__':
    ret,con = ConnectionManager().connect_to('192.168.184.128', 6641, 'OVN_Northbound')

    app = QApplication(sys.argv)

    test_widget = DataItemWidget(con, 'ACL')

    test_widget.show()
    sys.exit(app.exec_())
