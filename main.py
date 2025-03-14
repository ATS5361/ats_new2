"""
Bismillahirrahmanirrahim
"""
from PyQt5.QtCore import *
from PyQt5 import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys 
from backend.databaseManager import DatabaseManager
from frontend.mainUI import CustomDialog
import sqlite3 as sql

if __name__ == "__main__":
    app = QApplication(sys.argv)
    db_manager = DatabaseManager()
    window = CustomDialog(database=db_manager)
    window.show()
    def cleanup():
        db_manager.close_connections()
        print("Database connection is closed.")
    app.aboutToQuit.connect(cleanup)
    sys.exit(app.exec_())
