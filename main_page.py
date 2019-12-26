import sys
import os
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtSql import *
from ui_Main import Ui_MainWindow
import pyodbc


class MainWindow(QMainWindow):

    # ------------------- Variable ---------------------- #
    result_database = []

    db = None

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent=parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("NMPSC BRT LIST")

        self.ui.pushButton.setText("ADD ROW")
        self.ui.pushButton_2.setText("DEL ROW")
        self.ui.pushButton_3.setText("REFRESH")
        self.ui.pushButton_4.setText("LOAD DATABASE")

        self.ui.label.setText("Editor BRT")

        self.ui.pushButton_4.clicked.connect(self.Show_Database)
        self.ui.pushButton.clicked.connect(self.add_row)
        self.ui.pushButton_2.clicked.connect(self.del_row)
        self.ui.pushButton_3.clicked.connect(self.refresh_row)
        self.ui.tableView.clicked.connect(self.find_row)

    def database_connect(self):
        cnxn = f'DRIVER={{ODBC Driver 17 for SQL Server}};'\
            f'SERVER=mtl-700-noa55;'\
            f'DATABASE=MT740_LOSSCODE;'\
            f'UID=sa;PWD=qwerty@1'

        self.db = QSqlDatabase.addDatabase('QODBC')
        self.db.setDatabaseName(cnxn)

        if self.db.open():
            print("SQL CONNECTED")
        else:
            print("CAN'T CONNECT SQL")

    def add_row(self):
        print(self.model.rowCount())
        self.model.insertRows(self.model.rowCount(), 1)

    def del_row(self):
        self.model.removeRow(self.ui.tableView.currentIndex().row())

    def refresh_row(self):
        print("Refresh ROW")
        self.model.setFilter("id != '0' ORDER BY convert(int,id) ASC")
        self.model.select()

    def find_row(self, i):
        print(self.ui.tableView.currentIndex().row())

    def show_query(self):
        self.database_connect()

        self.model = QSqlTableModel()
        self.model.setTable("NMPSC_TROUBLE")
        self.model.setEditStrategy(QSqlTableModel.OnFieldChange)
        self.model.setFilter("id != '0' ORDER BY convert(int,id) ASC")
        self.model.select()
        self.model.setHeaderData(1, Qt.Horizontal, ("Block"))
        self.model.setHeaderData(2, Qt.Horizontal, ("Touble"))
        self.model.setHeaderData(3, Qt.Horizontal, ("Cause"))

        print(self.model.rowCount())
        self.ui.tableView.setModel(self.model)

        self.ui.pushButton_4.setEnabled(False)

    def Show_Database(self):
        dataview = self.show_query()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
