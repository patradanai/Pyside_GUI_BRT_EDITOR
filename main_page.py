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
        self.resize(800, 600)
        self.setWindowTitle("NMPSC BRTLIST")

        # ------- Set Text ------
        self.ui.pushButton.setText("ADD ROW")
        self.ui.pushButton_2.setText("DEL ROW")
        self.ui.pushButton_3.setText("REFRESH")
        self.ui.pushButton_4.setText("LOAD DATABASE")
        self.ui.pushButton_5.setText("EXIT")

        self.ui.label.setText("Editor BRT")

        # ------- Signal and Slot -------
        self.ui.pushButton_4.clicked.connect(self.show_query)
        self.ui.pushButton.clicked.connect(self.add_row)
        self.ui.pushButton_2.clicked.connect(self.del_row)
        self.ui.pushButton_3.clicked.connect(self.refresh_row)
        self.ui.pushButton_5.clicked.connect(sys.exit)
        self.ui.tableView.clicked.connect(self.find_row)

        self.ui.lineEdit.textChanged.connect(
            self.fillter_model)

        self.ui.lineEdit_2.textChanged.connect(self.fillter_model_trouble)

        self.ui.lineEdit_3.textChanged.connect(self.fillter_model_cause)

    def database_connect(self):
        cnxn = f'DRIVER={{SQL Server}};'\
            f'SERVER=mt700svr;'\
            f'DATABASE=MT700PDDB;'\
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
        choice = QMessageBox.question(self, 'Confirm Deleting',
                                      "ต้องที่จะลบ ข้อมูลใช่ไหม",
                                      QMessageBox.Yes | QMessageBox.No)
        if choice == QMessageBox.Yes:
            print("Deleted Now")
            self.model.removeRow(self.ui.tableView.currentIndex().row())

    def refresh_row(self):
        print("Refresh ROW")
        self.model.setFilter("No != '0' ORDER BY convert(int,No) ASC")
        self.model.select()

    def find_row(self, i):
        print(self.ui.tableView.currentIndex().row())

    def show_query(self):

        # Connect DataBase
        self.database_connect()

        # Initial QSQLTableModel
        self.model = QSqlTableModel()
        self.model.setTable("NMPSC_TROUBLE")
        self.model.setEditStrategy(QSqlTableModel.OnFieldChange)
        self.model.setFilter("No != '0' ORDER BY convert(int,No) ASC")
        self.model.select()
        self.model.setHeaderData(1, Qt.Horizontal, ("Block"))
        self.model.setHeaderData(2, Qt.Horizontal, ("Trouble"))
        self.model.setHeaderData(3, Qt.Horizontal, ("Cause"))

        self.ui.tableView.setModel(self.model)      # Print model on Tableview

        # Initial FillterProxyModel Block
        self.fillter_proxymodel = QSortFilterProxyModel()
        self.fillter_proxymodel.setSourceModel(self.model)
        self.fillter_proxymodel.setFilterKeyColumn(1)

        # Initial FillterProxyModel Trouble
        self.fillter_proxymodel_trouble = QSortFilterProxyModel()
        self.fillter_proxymodel_trouble.setSourceModel(self.fillter_proxymodel)
        self.fillter_proxymodel_trouble.setFilterKeyColumn(2)

        # Initial FillterProxyModel Cause
        self.fillter_proxymodel_cause = QSortFilterProxyModel()
        self.fillter_proxymodel_cause.setSourceModel(
            self.fillter_proxymodel_trouble)
        self.fillter_proxymodel_cause.setFilterKeyColumn(3)

        self.ui.pushButton_4.setEnabled(False)      # Disable Buttom

    @pyqtSlot(str)
    def fillter_model(self, x):
        self.fillter_proxymodel.setFilterRegExp(x)
        self.ui.tableView.setModel(self.fillter_proxymodel)

    @pyqtSlot(str)
    def fillter_model_trouble(self, x):
        self.fillter_proxymodel_trouble.setFilterRegExp(x)
        self.ui.tableView.setModel(self.fillter_proxymodel_trouble)

    @pyqtSlot(str)
    def fillter_model_cause(self, x):
        self.fillter_proxymodel_cause.setFilterRegExp(x)
        self.ui.tableView.setModel(self.fillter_proxymodel_cause)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
