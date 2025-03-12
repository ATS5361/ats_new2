import sqlite3 as sql
import psycopg2
from PyQt5.QtWidgets import QMessageBox

class DatabaseManager():
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(DatabaseManager, cls).__new__(cls, *args, **kwargs)
            print("Database Manager is instantiated.")
            cls._instance.connect_to_database()
        return cls._instance

    def connect_to_database(self):
        try:
            self.conn1 = sql.connect("ADD_USER_DATA.db")
            self.conn2 = sql.connect("LOGIN_DATA.db")
            print("Database connection is initialized.")
        except Exception as e:
            raise Exception(f"An error occurred while connecting to the database: {e}")

    def connect_add_user_db(self, password):
        self.conn1 = sql.connect("""C:\\Users\\tai\\Desktop\\ats_new2\\ADD_USER_DATA.db""")
        self.add_user_cursor = self.conn1.cursor()
        self.add_user_cursor.execute("SELECT USERNAME, LASTNAME, DEPARTMENT, PASSWORD FROM LOGIN WHERE PASSWORD =:password",
                          {"password": password.upper()})
        self.add_user_recordroot = self.add_user_cursor.fetchall()

    def connect_login_user_db(self, password):
        self.conn2 = sql.connect("""C:\\Users\\tai\\Desktop\\ats_new2\\database_files\\LOGIN.db""")
        self.login_cursor = self.conn2.cursor()
        self.login_cursor.execute(
            "SELECT USERNAME, LASTNAME, DEPARTMENT, PASSWORD FROM LOGIN WHERE PASSWORD =:password",
            {"password": password.upper()})
        self.login_recordroot = self.login_cursor.fetchall()

    def insertSQLiteToPostgre(self, completeFlagParam):
        try:
            conn = sql.connect("database_files/TOOL_USAGE.db")
            cursor = conn.cursor()
            cursor.execute("""SELECT * FROM TOOL_USAGE""")
            data= cursor.fetchall()

            postgresql_conn = psycopg2.connect(database="toolboxtakip", user="toctoolbox", password="T*00l@Bax!06", host="pgcons.dmnint.intra", port="54001")
            postgre_cursor = postgresql_conn.cursor()
            cursor.executemany(""" INSERT INTO TOOLTRACK VALUES(nextval('record_sequence'),%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",data)

            postgresql_conn.commit()
            postgresql_conn.close()
            conn.commit()
            conn.close()
            completeFlag = True
        except Exception as e:
            completeFlag = False
            print(e)
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("OET-TUSAS ağına bağlanamadığı için \nişlem gerçekleştirilemedi lütfen tekrar deneyiniz.")
            msg.setWindowTitle("Bağlantı Hatası")
            msg.exec_()

    def clearLocalDB(self, completeFlagParam):
        try:
            conn = sql.connect("database_files/TOOL_USAGE.db")
            cursor = conn.cursor()
            cursor.execute("""DELETE FROM TOOL_USAGE WHERE 1=1""")
            conn.commit()
            conn.close()
            completeFlag = False
        except Exception as e:
            print(e)

    def close_connections(self):
        if hasattr(self, 'conn1') and self.conn1:
            self.conn1.close()
            print("Connection to ADD_USER_DATA.db closed.")
        if hasattr(self, 'conn2') and self.conn2:
            self.conn2.close()
            print("Connection to LOGIN_DATA.db closed.")
