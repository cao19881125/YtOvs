from PyQt4.QtGui import QTreeWidgetItem
from PyQt4.QtGui import QIcon
from utils.yt_utils import get_uuid

class DbTreeItem(QTreeWidgetItem):
    def __init__(self, con_name, schema_name, table_names, con_key, label_color):
        QTreeWidgetItem.__init__(self)
        self.__con_name = con_name
        self.__schema_name = schema_name
        self.__table_names = table_names
        self.__con_key = con_key
        self.__label_color = label_color
        self.__uuid = get_uuid()
        self.__setup_ui()


    def __setup_ui(self):
        #self.setText(0, self.__con_name)
        self.setIcon(0,QIcon('./icon/database.png'))


        self.__db_item = QTreeWidgetItem(self)
        self.__db_item.setIcon(0,QIcon('./icon/dir_close.png'))
        self.__db_item.setText(0, self.__schema_name)

        for table in self.__table_names:
            table_item = QTreeWidgetItem(self.__db_item)
            table_item.setIcon(0,QIcon('./icon/table.png'))
            table_item.setText(0, table)

    def get_default_expand_items(self):
        items = []
        items.append(self)
        items.append(self.__db_item)
        return items

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

    def get_uuid(self):
        return self.__uuid

    def get_label_color(self):
        return self.__label_color