import sqlite3 as sql
import psycopg2
import threading
from PyQt5.QtWidgets import QMessageBox

class DatabaseManager():
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(DatabaseManager, cls).__new__(cls, *args, **kwargs)
            print("Database Manager is instantiated.")
            cls._instance.connect_to_database()
        return cls._instance

    def connect_to_database(self):
        try:
            with self._lock:
                self.conn1 = sql.connect("/home/tai-orin/Desktop/ats_new2/database_files/LOGIN.db", check_same_thread=False)
                self.conn2 = sql.connect("/home/tai-orin/Desktop/ats_new2/database_files/ADMIN.db", check_same_thread=False)
            print("Database connection is initialized.")
        except Exception as e:
            raise Exception(f"An error occurred while connecting to the database: {e}")

    def connect_add_user_db(self, password):
        if not hasattr(self, 'conn1') or self.conn1 is None:
            self.conn1 = sql.connect("/home/tai-orin/Desktop/ats_new2/database_files/ADMIN.db", check_same_thread=False)
        admin_cursor = self.conn1.cursor()
        admin_cursor.execute("SELECT USERNAME, LASTNAME, DEPARTMENT, PASSWORD FROM ADMIN WHERE PASSWORD =:password", {"password": password.upper()})
        self.admin_data = admin_cursor.fetchall()

    def insertSQLiteToPostgre(self, completeFlagParam):
        try:
            with self._lock:
                conn = sql.connect("/home/tai-orin/Desktop/ats_new2/database_files/TOOL_USAGE.db", check_same_thread=False)
                cursor = conn.cursor()
                cursor.execute("""SELECT * FROM TOOL_USAGE""")
                data = cursor.fetchall()

            with psycopg2.connect(database="toolboxtakip", user="toctoolbox", password="T*00l@Bax!06", host="pgcons.dmnint.intra", port="54001") as postgresql_conn:
                postgresql_conn.autocommit = True
                postgre_cursor = postgresql_conn.cursor()
                postgre_cursor.executemany("""INSERT INTO TOOLTRACK VALUES(nextval('record_sequence'),%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""", data)

            completeFlagParam = True
        except Exception as e:
            completeFlagParam = False
            print(e)
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("Bağlantı hatası, tekrar deneyiniz.")
            msg.setWindowTitle("Bağlantı Hatası")
            msg.exec_()
