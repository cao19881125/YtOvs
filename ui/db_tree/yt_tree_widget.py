import sys
from PyQt4.QtGui import QApplication
from PyQt4.QtGui import QTreeWidget
from PyQt4.QtGui import QPushButton
from PyQt4.QtGui import QWidget
from PyQt4.QtGui import QLabel
from PyQt4.QtGui import QHBoxLayout
from PyQt4.QtGui import QVBoxLayout
from PyQt4.QtGui import QMessageBox
from PyQt4.QtCore import Qt
from PyQt4.QtCore import QSize
from PyQt4.QtCore import pyqtSlot
from PyQt4.QtCore import SIGNAL
from PyQt4.QtCore import SLOT
from db_tree_item import DbTreeItem
from db_tree_header_widget import DbTreeHeaderWidget
from db_connection.connection_manager import ConnectionManager

class YtTreeWidget(QTreeWidget):
    def __init__(self):
        QTreeWidget.__init__(self)
        self.__setup_ui()
        self.__connect_slot()
        self.__label_color = ['red','orange','yellow','green','blue','purple']
        self.__current_label_count = 0

    def __setup_ui(self):
        self.setColumnCount(1)

        self.header().close()
        self.setIconSize(QSize(20,20))
        self.setAttribute(Qt.WA_MacShowFocusRect, False)
        self.setIndentation(12)

    def add_connection(self, ip, port ,schema, tables, con_key):


        item = DbTreeItem(ip + ':' + str(port), schema, tables, con_key, self.__label_color[self.__current_label_count])
        self.addTopLevelItem(item)

        header_widget = DbTreeHeaderWidget(ip + ':' + str(port), item, con_key, self.__label_color[self.__current_label_count])
        self.setItemWidget(item,0,header_widget)
        self.connect(header_widget,SIGNAL('close_btn_clickd(PyQt_PyObject,PyQt_PyObject)'),self,SLOT('__on_header_close_btn(PyQt_PyObject,PyQt_PyObject)'))

        default_expand_items = item.get_default_expand_items()
        for ex_item in default_expand_items:
            self.expandItem(ex_item)

        self.__current_label_count += 1
        if self.__current_label_count >= len(self.__label_color):
            self.__current_label_count = 0

    def __connect_slot(self):
        self.connect(self,SIGNAL('itemExpanded(QTreeWidgetItem*)'),self,SLOT('__on_item_expand(QTreeWidgetItem*)'))
        self.connect(self,SIGNAL('itemCollapsed(QTreeWidgetItem*)'),self,SLOT('__on_item_collapsed(QTreeWidgetItem*)'))
        self.connect(self,SIGNAL('itemDoubleClicked(QTreeWidgetItem*,int)'),self,SLOT('__on_item_double_click(QTreeWidgetItem*,int)'))

    def __get_root_parent(self, item):
        if item.parent():
            return self.__get_root_parent(item.parent())
        else:
            return item

    @pyqtSlot('QTreeWidgetItem*')
    def __on_item_expand(self,item):
        root_item = self.__get_root_parent(item)
        root_item.item_expand(item)

    @pyqtSlot('QTreeWidgetItem*')
    def __on_item_collapsed(self, item):
        root_item = self.__get_root_parent(item)
        root_item.item_collapsed(item)

    @pyqtSlot('QTreeWidgetItem*','int')
    def __on_item_double_click(self, item, colume):
        root_item = self.__get_root_parent(item)
        table_name,con_key = root_item.item_double_click(item)
        if not table_name or not con_key:
            return
        label_color = root_item.get_label_color()
        self.emit(SIGNAL('table_double_clicked(PyQt_PyObject,PyQt_PyObject,PyQt_PyObject)'), table_name, con_key,label_color)

    @pyqtSlot('PyQt_PyObject','PyQt_PyObject')
    def __on_header_close_btn(self, item, con_key):
        top_count = self.topLevelItemCount()
        for i in range(top_count):
            top_item = self.topLevelItem(i)
            if item is top_item:
                self.takeTopLevelItem(i)
                ConnectionManager().del_connection(con_key)
                return

if __name__== '__main__':
    app = QApplication(sys.argv)

    test_widget = YtTreeWidget()
    item = DbTreeItem('tcp:192.168.184.128:6641','OVN_Northbound',['Load_Balancer', 'Logical_Switch_Port', 'Address_Set'])
    test_widget.addTopLevelItem(item)

    test_widget.show()
    sys.exit(app.exec_())
