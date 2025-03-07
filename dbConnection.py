from PyQt5.QtWidgets import *
import sqlite3
import psycopg2

class DatabaseManager():
    def __init__():
        print("DB Manager is initialized")

    def connect_TOOLS():
        conn = sqlite3.connect("database_files/TOOLS.db")
    
    def connect_LOGIN():
        conn = sqlite3.connect("database_files/LOGIN.db")

    def connect_ADD_USER():
        conn = sqlite3.connect("database_files/ADD_USER.db")
        imlec = conn.cursor()
        imlec.execute("")
        conn.commit()
        conn.close()

    

    def dataMigrate(class_param):
        class_param.insertSQLiteToPostgre()
        if class_param.completeFlag:
            try:
                class_param.clear_local_db("tools_data")
                class_param.completeFlag = False
            except Exception as e:
                print(e)
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("Veri tabanı aktarımı tamamlandı.")
            msg.setWindowTitle("İşlem Tamamlandı")
            msg.exec_()

    def insertSQLiteToPostgre(self):
        try:
            sqlConnection = sqlite3.connect('database_files/TOOL_TIME.db')
            cursorSqlite = sqlConnection.cursor()
            cursorSqlite.execute("""SELECT * FROM TOOL_TIME""")
            sqLiteData = cursorSqlite.fetchall()
            #print(sqLiteData)
            conn = psycopg2.connect(database="toolboxtakip", user="toctoolbox", password="T*00l@Bax!06", host="pgcons.dmnint.intra", port="54001")
            cursor = conn.cursor()
            cursor.executemany(""" INSERT INTO TOOLTRACK VALUES(nextval('record_sequence'),%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",sqLiteData)
            
            conn.commit()
            conn.close()
        except Exception as e:
            self.completeFlag = False
            print(e)
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("OET-TUSAS ağına bağlanamadığı için \nişlem gerçekleştirilemedi lütfen tekrar deneyiniz.")
            msg.setWindowTitle("Bağlantı Hatası")
            msg.exec_()