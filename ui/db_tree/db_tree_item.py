import sys
from PyQt4.QtGui import QTreeWidget
from PyQt4.QtGui import QTreeWidgetItem
from PyQt4.QtGui import QApplication
from PyQt4.QtGui import QIcon
from PyQt4.QtCore import QSize

class DbTreeItem(QTreeWidgetItem):
    def __init__(self, con_name, schema_name, table_names, con_key):
        QTreeWidgetItem.__init__(self)
        self.__con_name = con_name
        self.__schema_name = schema_name
        self.__table_names = table_names
        self.__con_key = con_key
        self.__setup_ui()


    def __setup_ui(self):
        self.setText(0, self.__con_name)

        self.setIcon(0,QIcon('./icon/database.png'))

        db_item = QTreeWidgetItem(self)
        db_item.setIcon(0,QIcon('./icon/dir_close.png'))
        db_item.setText(0, self.__schema_name)


        for table in self.__table_names:
            table_item = QTreeWidgetItem(db_item)
            table_item.setIcon(0,QIcon('./icon/table.png'))
            table_item.setText(0, table)

    def item_expand(self,item):
        if item is self:
            # do nothing
            return

        for i in range(self.childCount()):
            if item is self.child(i):
                item.setIcon(0,QIcon('./icon/dir_open.png'))
    def item_collapsed(self, item):
        if item is self:
            # do nothing
            return

        for i in range(self.childCount()):
            if item is self.child(i):
                item.setIcon(0,QIcon('./icon/dir_close.png'))

    def item_double_click(self, item):
        if item is self:
            # do nothing
            return None, None

        for i in range(self.childCount()):
            # database layer
            if item is self.child(i):
                return None, None
            child_item = self.child(i)
            for d in range(child_item.childCount()):
                if item is child_item.child(d):
                    return item.text(0), self.__con_key