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
            self.conn1 = sql.connect("/home/tai-orin/Desktop/ats_new2/database_files/LOGIN.db")
            self.conn2 = sql.connect("/home/tai-orin/Desktop/ats_new2/database_files/ADMIN.db")
            print("Database connection is initialized.")
        except Exception as e:
            raise Exception(f"An error occurred while connecting to the database: {e}")

    def execute_query(self, cursor, query):
        cursor.execute(query)
        recordroot = cursor.fetchall()

    def create_cursors(self):
        self.login_cursor = self.conn1.cursor()
        self.add_user_cursor = self.conn2.cursor()
        return self.login_cursor, self.add_user_cursor

    def connect_add_user_db(self, password):
        self.conn1 = sql.connect('home/tai-orin/Desktop/ats_new2/database_files/ADMIN.db')
        admin_cursor = self.conn1.cursor()
        admin_cursor.execute("SELECT USERNAME, LASTNAME, DEPARTMENT, PASSWORD FROM ADMIN WHERE PASSWORD =:password", {"password":password.upper()})
        self.admin_data = admin_cursor.fetchall()

    def connect_login_user_db(self, password):
        self.conn2 = sql.connect('home/tai-orin/Desktop/ats_new2/database_files/LOGIN.db')
        login_cursor = self.conn1.cursor()
        login_cursor.execute("SELECT USERNAME, LASTNAME, DEPARTMENT, PASSWORD FROM LOGIN WHERE PASSWORD =:password", {"password":password.upper()})
        self.user_data = login_cursor.fetchall()

    def fetch_admin_data(self):
        return self.admin_data
    
    def fetch_user_data(self):
        return self.user_data

    def fetch_one_user(self, password):
        self.conn1 = sql.connect("""/home/tai-orin/Desktop/ats_new2/database_files/ADMIN.db""")
        self.add_user_cursor = self.conn1.cursor()
        self.add_user_cursor.execute("SELECT USERNAME, LASTNAME, DEPARTMENT, PASSWORD FROM LOGIN WHERE PASSWORD =:password",
                          {"password": password.upper()})
        self.add_user_recordroot = self.add_user_cursor.fetchall()
        return self.add_user_recordroot

    def insertSQLiteToPostgre(self, completeFlagParam):
        try:
            conn = sql.connect("/home/tai-orin/Desktop/ats_new2/database_files/TOOL_USAGE.db")
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
            conn = sql.connect("/home/tai-orin/Desktop/ats_new2/database_files/TOOL_USAGE.db")
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
            print("Connection to ADMIN.db closed.")
        if hasattr(self, 'conn2') and self.conn2:
            self.conn2.close()
            print("Connection to LOGIN.db closed.")
