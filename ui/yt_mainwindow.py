from PyQt4.QtGui import QMainWindow
from PyQt4.QtGui import QMenu
from PyQt4.QtGui import QMenuBar
from PyQt4.QtGui import QAction
from PyQt4.QtGui import QToolBar
from PyQt4.QtGui import QIcon
from PyQt4.QtGui import QSplitter
from PyQt4.QtGui import QTableWidget
from PyQt4.QtGui import QMessageBox
from PyQt4.QtCore import Qt
from PyQt4.QtCore import QSize
from PyQt4.QtCore import SIGNAL
from PyQt4.QtCore import SLOT
from PyQt4.QtCore import pyqtSlot
from PyQt4.QtCore import QString
from yt_dialog.new_connection_dlg import NewConnectionDlg
from db_connection.connection_manager import ConnectionManager
from db_tree.yt_tree_widget import YtTreeWidget
from data_widget.data_widget import DataWidget
from utils.yt_utils import *


class YtMainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.__setup_ui()
        self.__connect_slot()

    def __setup_ui(self):
        self.resize(1024,768)
        self.__setup_menu()

        split = QSplitter()
        self.__yt_tree_widget = YtTreeWidget()
        split.addWidget(self.__yt_tree_widget)

        self.__data_widget = DataWidget()
        split.addWidget(self.__data_widget)
        split.setHandleWidth(2)
        split.setStretchFactor(0,1)
        split.setStretchFactor(1,200)


        self.setCentralWidget(split)


    def __setup_menu(self):
        fileMenu = QMenu("Db", self)

        self.menuBar().addMenu(fileMenu)

        self.__new_action = QAction(QIcon('./icon/add_database.png'),"&New", fileMenu)
        fileMenu.addAction(self.__new_action)

        tool_bar = QToolBar()
        tool_bar.setMovable(False)
        tool_bar.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        tool_bar.addAction(self.__new_action)
        tool_bar.setIconSize(QSize(20,20))

        self.addToolBar(tool_bar)


    def __connect_slot(self):
        self.connect(self.__new_action,SIGNAL('triggered()'), self, SLOT('__on_new_action()'))
        self.connect(self.__yt_tree_widget,SIGNAL('table_double_clicked(PyQt_PyObject,PyQt_PyObject)'),
                     self, SLOT('__on_table_double_clicked(PyQt_PyObject,PyQt_PyObject)'))

    @pyqtSlot('PyQt_PyObject','PyQt_PyObject')
    def __on_table_double_clicked(self, table_name, con_key):
        # table_name type is PyQt4.QtCore.QString,con_key type is str

        self.__data_widget.add_tab(to_python_str(con_key), to_python_str(table_name))

    @pyqtSlot()
    def __on_new_action(self):
        new_dlg = NewConnectionDlg()
        if new_dlg.exec_():
            ret,hash_key = ConnectionManager().connect_to(new_dlg.host, new_dlg.port, new_dlg.schema)
            if not ret:
                QMessageBox.critical(self, 'failed', 'connect failed')
                return
            # show db in tree
            con = ConnectionManager().get_connection(hash_key)
            if not con:
                return
            ip, port, schema = con.get_con_info()
            self.__yt_tree_widget.add_connection(ip, port, schema, con.get_table_names(), hash_key)

