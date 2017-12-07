import json
import os
from PyQt4.QtGui import QDialog
from PyQt4.QtGui import QWidget
from PyQt4.QtGui import QVBoxLayout
from PyQt4.QtGui import QHBoxLayout
from PyQt4.QtGui import QTableWidget
from PyQt4.QtGui import QTableWidgetItem
from PyQt4.QtGui import QPushButton
from PyQt4.QtGui import QIcon
from PyQt4.QtGui import QHeaderView
from PyQt4.QtGui import QAbstractItemView
from PyQt4.QtGui import QMessageBox
from PyQt4.QtCore import QStringList
from PyQt4.QtCore import QString
from PyQt4.QtCore import QSize
from PyQt4.QtCore import pyqtSlot
from PyQt4.QtCore import SIGNAL
from PyQt4.QtCore import SLOT
from PyQt4.QtCore import QSettings
from PyQt4.QtCore import Qt
from new_connection_dlg import NewConnectionDlg
from utils.yt_utils import con_has_code
from utils.yt_utils import to_python_str
ICON_IDR = os.path.join(os.path.dirname(__file__),'../../icon/')


class ProfileDlg(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        self.__setup_ui()
        self.__connect_slot()
        self.__settings = QSettings('__cyt', '__yt_ovs')
        #print self.__settings.fileName()
        set_str = to_python_str(self.__settings.value('__profile_record', '').toString())
        set_str = set_str if set_str is not '' else "[]"
        self.__record_list = json.loads(set_str)#[{'ip':'1.1.1.1','port':6641,'schema':'xxxx'},{...}]
        self.__list_to_table_item()
        self.click_ip = ''
        self.click_port = 0
        self.click_schema = ''

    def __setup_ui(self):
        self.setMaximumSize(500, 400)
        self.setMinimumSize(500, 400)

        v_layout = QVBoxLayout()

        #init table widget
        self.__profile_table = QTableWidget()
        self.__profile_table.setColumnCount(3)
        header_list = QStringList()
        header_list << 'ip' << 'port' << 'schema'
        self.__profile_table.setHorizontalHeaderLabels(header_list)
        self.__profile_table.horizontalHeader().setResizeMode(QHeaderView.Stretch)
        self.__profile_table.setSelectionBehavior(QAbstractItemView.SelectRows)

        #init tool widget
        self.__tool_wid = QWidget()
        h_layout = QHBoxLayout()
        h_layout.setContentsMargins(0,0,0,0)

        self.__puls_btn = QPushButton()
        self.__puls_btn.setIcon(QIcon(ICON_IDR + 'arrow_plus.png'))
        self.__puls_btn.setIconSize(QSize(15, 15))
        self.__puls_btn.setMaximumSize(20, 20)

        self.__minus_btn = QPushButton()
        self.__minus_btn.setIcon(QIcon(ICON_IDR + 'arrow_minus.png'))
        self.__minus_btn.setIconSize(QSize(15, 15))
        self.__minus_btn.setMaximumSize(20, 20)

        h_layout.addWidget(self.__puls_btn,0)
        h_layout.addWidget(self.__minus_btn,0)
        h_layout.addStretch(1)
        self.__tool_wid.setLayout(h_layout)


        #v layout
        v_layout.addWidget(self.__profile_table,1)
        v_layout.addWidget(self.__tool_wid,0)

        v_layout.setSpacing(1)

        self.setLayout(v_layout)

    def __connect_slot(self):
        self.connect(self.__puls_btn, SIGNAL('clicked()'), self, SLOT('__on_plus_btn()'))
        self.connect(self.__minus_btn, SIGNAL('clicked()'), self, SLOT('__on_minus_btn()'))
        self.connect(self.__profile_table, SIGNAL('cellDoubleClicked (int,int)'), self, SLOT('__on_profile_double_click(int,int)'))

    def __add_record(self, ip, port, schema):

        count = self.__profile_table.rowCount()
        self.__profile_table.insertRow(count)

        ip_item = QTableWidgetItem(ip)
        ip_item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
        item_font = ip_item.font()
        item_font.setPointSizeF(12)
        ip_item.setFont(item_font)

        port_item = QTableWidgetItem(port)
        port_item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
        port_item.setFont(item_font)

        schema_item = QTableWidgetItem(schema)
        schema_item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
        schema_item.setFont(item_font)



        self.__profile_table.setItem(count, 0, ip_item)
        self.__profile_table.setItem(count, 1, port_item)
        self.__profile_table.setItem(count, 2, schema_item)

    def __clear_table_data(self):
        row_count = self.__profile_table.rowCount()
        rev = [i for i in range(row_count)]
        rev.reverse()
        for i in rev:
            self.__profile_table.removeRow(i)

    def __list_to_table_item(self):
        self.__clear_table_data()
        for record in self.__record_list:
            self.__add_record(record['ip'], str(record['port']), record['schema'])
            #print record

    def __table_item_to_list(self):
        row_count = self.__profile_table.rowCount()
        self.__record_list = []
        for i in range(row_count):
            record = {}
            ip = to_python_str( self.__profile_table.item(i, 0).text() )
            port = int( self.__profile_table.item(i, 1).text() )
            schema = to_python_str(self.__profile_table.item(i, 2).text())
            record["ip"] = ip
            record["port"] = port
            record["schema"] = schema
            self.__record_list.append(record)

        print self.__record_list

    def __check_existed(self, ip, port, schema):
        has_code = con_has_code(ip, port, schema)


        for record in self.__record_list:
            exist_code = con_has_code(record["ip"], record["port"], record["schema"])
            if exist_code == has_code:
                return True

        return False


    def __record_to_settings(self):
        self.__settings.setValue('__profile_record', json.dumps(self.__record_list))


    @pyqtSlot()
    def __on_plus_btn(self):
        new_dlg = NewConnectionDlg()
        if new_dlg.exec_():
            # add to table_widget
            if self.__check_existed(new_dlg.host, new_dlg.port, new_dlg.schema):
                return
            self.__add_record(new_dlg.host, str(new_dlg.port), new_dlg.schema)

        self.__table_item_to_list()
        self.__record_to_settings()


    @pyqtSlot()
    def __on_minus_btn(self):
        select_row = self.__profile_table.currentRow()
        self.__profile_table.removeRow(select_row)

        self.__table_item_to_list()
        self.__record_to_settings()

    @pyqtSlot('int','int')
    def __on_profile_double_click(self, row, column):
        ip_item = self.__profile_table.item(row, 0)
        port_item = self.__profile_table.item(row, 1)
        schema_item = self.__profile_table.item(row, 2)

        self.click_ip = to_python_str(ip_item.text())
        self.click_port = int(port_item.text())
        self.click_schema = to_python_str(schema_item.text())

        self.accept()
