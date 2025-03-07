"""
Bismillahirrahmanirrahim
"""
from PyQt5.QtCore import *
from PyQt5 import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import sys
import dbConnection as db
from frontend.MainUI import CustomDialog

database = db.DatabaseManager()
database.closeConnection()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = CustomDialog(database) # ?
    win.show()
    sys.exit(app.exec_())
