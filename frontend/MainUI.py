"""
Bismillahirrahmanirrahim
"""
# PyQt Lib
from PyQt5.QtCore import Qt, QSize, QThread, pyqtSignal, QTime, QDate
from PyQt5 import QtGui, QtCore
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtWidgets import *

# built-ins
import time
import os
import sqlite3
#import psycopg2
import json
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Necessary User Packages
import backend.detectThread as DT
import backend.mainThread as MT
from frontend.ToolUI import ToolWindow
from frontend.UserUI import UserWindow
from backend.databaseManager import DatabaseManager

photo = MT.TakePhoto()
class MainThread(QThread):
    threadSignal = pyqtSignal()
    def run(self):
        while(not photo.terminate):
            photo.endlessLoop()

tool_list_path = "sources/toolList.txt"
        
class CustomDialog(QDialog, DatabaseManager):
    def __init__(self, database, parent = None):
        super(CustomDialog, self).__init__(parent)
        self.database = database

        self.setWindowTitle("Toolbox Login Panel")
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.toolWindow = ToolWindow()
        self.userWindow = UserWindow()	
        self.buttonSize = QSize(160, 160)
        self.setFont((QFont('Roboto', 15)))

        self.toolNotExistBackground = "background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #e63900, stop: 0.3  #ff531a,stop: 0.8  #ff531a, stop: 1.0  #e63900); font: bold;font-size: 58px;border-style: outset; border-width: 3px;border-color: #e63900; border-radius: 35px; "
        self.toolExistsBackground = "background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #85e085, stop: 0.3  #47d147,stop: 0.8  #47d147, stop: 1.0  #70db70); font: bold;font-size: 58px;border-style: outset; border-width: 3px;border-color: #33cc33; border-radius: 35px;"
    
        photo.drawerTrigger.connect(self.toolWindow.updateOpenedDrawer)
        photo.openedDrawersTrigger.connect(self.toolWindow.updateDrawers)

        self.toolWindow.detectSignal.connect(self.setOpenedDrawers)
        self.statusLabel = QLabel(self)
        self.toolStatus = False
        self.missingTools = 0
        self.setFixedSize(1365, 745)
        self.setStyleSheet('font-size: 10pt; background-color: #101010')
        self.layout = QGridLayout()
        self.layout.setSpacing(13)

        # Set components of QDialog
        self.setButtons()
        self.setLastStatus()
        self.setStatusLabel()
        self.addLogo()
        self.shutDownButton.clicked.connect(self.shutDownSystem)
        self.userButton.clicked.connect(self.addUser)
#        self.databaseButton.clicked.connect(self.database.dataMigrate(self))
#        self.loginButton.clicked.connect(self.readCardForLogin)
#        self.rebootButton.clicked.connect(self.rebootSystem)
#        self.toolWindow.disconnectSignal.connect(self.disconnectSensor)
#        self.toolWindow.updateStatusSignal.connect(self.updateStatus)
        self.toolWindowFlag = 1
        self.userWindowFlag = 0
        self.debugLastDistance = 0
        self.completeFlag = False
        
        self.timeLabel = QLabel()
        self.timeLabel.setStyleSheet("font-size: 18pt; background-color: blue")
        self.lastStatusOfTools = [self.toolWindow.lastStatusOfTools_1, 
                                  self.toolWindow.lastStatusOfTools_2,
                                  self.toolWindow.lastStatusOfTools_3,
                                  self.toolWindow.lastStatusOfTools_4,
                                  self.toolWindow.lastStatusOfTools_5,
                                  self.toolWindow.lastStatusOfTools_6]

        self.layout.addWidget(self.taiLogo, 0, 0, 1, 0)
        self.layout.addWidget(self.timeLabel, 0, 3)
        self.layout.addWidget(self.statusLabel,1, 0, 2, 5)
        self.layout.addWidget(self.databaseButton, 3, 0)
        self.layout.addWidget(self.loginButton, 3, 2)
        self.layout.addWidget(self.userButton, 3, 1)
        self.layout.addWidget(self.rebootButton, 3, 3)
        self.layout.addWidget(self.shutDownButton, 3, 4)
        
        self.timeLabel.setStyleSheet("font-size: 15pt; color: white")
        self.timer = QtCore.QTimer(self)
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.displayTime)
        self.timer.start()

        self.debugTimer = QtCore.QTimer(self)
        self.debugTimer.setInterval(100)
#        self.debugTimer.timeout.connect(self.debugCam)
        self.debugTimer.start()
        self.passwordEntry = QLineEdit(self)
        self.passwordEntry.setFixedWidth(0)
        self.passwordEntry.move(100, 100)
#        self.passwordEntry.textChanged.connect(self.passCheck)
        self.passwordEntry.hide()

        self.isForLogin = False

        self.setLayout(self.layout)
        self.readCard()
#        DT.runMain()

    def keyPressEvent(self, event):
        """ Press Space key to pass to an instance of ToolUI. """
        if event.key() == Qt.Key_Escape:
            print("Kapatılıyor...")
            QApplication.instance().quit()

        elif event.key() == Qt.Key_Space:
            self.hide()
            self.toolWindow.show()
            self.toolWindow.setFocus()  # ToolWindow'a odaklanır
            event.accept()

    def setLastStatus(self):
        with open(tool_list_path, "r") as dosya:
            i = 0
            total_dif = 0

            for satir in dosya:
                if i != 6:
                    self.toolWindow.lastStatusOfDrawers[i] = json.loads(satir)
                    missing_counter = 0
                    for index in self.toolWindow.lastStatusOfDrawers[i]:
                        if index == 0:
                            total_dif += 1
                            missing_counter += 1
                    self.toolWindow.toolLabels[i].setText(str(missing_counter))
                    i += 1

            self.missingTools = total_dif
            if total_dif > 0:
                self.toolStatus = False
            else:
                self.toolStatus = True
        
        self.toolWindow.drawLastStatus()
            
    def setOpenedDrawers(self):
        self.changeDrawerList(photo.openedDrawerList)

    def passCheck(self):
        password = self.passwordEntry.text()
        if len(password) == 8:
            try:
                database = DatabaseManager()
                database.connect_add_user_db(password)
                database.connect_login_user_db(password)
                database.close_connections()

                if len(database.add_user_recordroot) == 1 and self.isForLogin == False:
                    self.showButtons()
                elif len(database.login_recordroot) == 1:
                    if self.toolWindowFlag:
                        sqlConnection = self.database.conn1
                        cursor = database.add_user_cursor
                    elif self.userWindowFlag:
                        sqlConnection = self.database.conn2
                        cursor = database.login_cursor
                    else:
                        print("HATA!!! db bağlantısı için gerekli ayarlamalar(flagler) eksik yapılmış.")
                    cursor.execute("SELECT USERNAME, LASTNAME, DEPARTMENT, PASSWORD FROM login_data WHERE PASSWORD =:password", {"password":password.upper()})
                    record = cursor.fetchall()
                    database.clos
                    if len(record) == 0:
                        print("HATA!!! Veri Tabanında böyle bir kullanıcı bulunamadı...")
                        self.statusLabel.setText("KULLANICI BULUNAMADI.\nLÜTFEN TEKRAR OKUTUNUZ")
                        self.statusLabel.repaint()
                    elif len(record) == 1:
                        if self.toolWindowFlag == 1:
                            self.statusLabel.setText("LÜTFEN BEKLEYİNİZ...")
                            self.statusLabel.repaint()
                            app.processEvents()
                            self.openToolWindow()
                            self.toolWindow.activePassword = record[0][3].upper()
                            # self.toolWindowFlag = 0
                        elif self.userWindowFlag == 1:
                            self.userWindow.show()
                            self.userWindowFlag = 0
                            self.toolWindowFlag = 1
                        self.passwordEntry.hide()
                        self.passwordEntry.setFocus(False)
                        self.toolWindow.nameLabel_entry.setText(record[0][0])
                        self.toolWindow.surnameLabel_entry.setText(record[0][1])
                        self.toolWindow.departmanLabel_entry.setText(record[0][2])
                        self.isForLogin = False
                        
                    else:
                        print("Hata: Veri tabanında duplike kayıt bulunmakta!!!")
                elif(len(self.database.login_recordroot) == 0 and len(self.database.add_user_recordroot) == 0):
                    print("HATA!!! Veri Tabanında böyle bir kullanıcı bulunamadı...")
                    self.statusLabel.setText("KULLANICI BULUNAMADI.\nLÜTFEN TEKRAR OKUTUNUZ")
                    self.statusLabel.repaint()

            except sqlite3.Error as err:
                print("Veri tabanı bağlantısı hatası:", err)

            finally:
                self.passwordEntry.clear()

    """
        def openToolWindow(self):
            photo.mainThreadFunction()
            photo.terminate = False
            self.workerThread = MainThread()
            self.workerThread.start()

            self.toolWindow.show()
            time.sleep(2)
            photo.sensor.setToolboxOn()
            self.toolWindow.passwordEntry.show()
            self.toolWindow.passwordEntry.setFocus(True)
            self.toolWindow.autoCloseTimer.start()
            #os.system("python3 _main.py &")

        def debugCam(self):
            if self.toolWindow.isVisible():
                if self.toolWindow.drawerIsOpen and self.debugLastDistance == photo.sensor.avgDistance and photo.sensor.avgDistance > 160:
                    self.debugCnt +=1
                else:
                    self.debugCnt = 0

                if self.debugCnt >= 5:
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Information)
                    msg.setText("Beklenmedik bir hata ile karşılaşıldı. Tüm çekmecelerin kapalı olduğundan emin olun ve 'OK' butonuna tıklayarak\ntekrar giriş yapın.")
                    msg.setWindowTitle("HATA")
                    retunVal = msg.exec_()
                    if (retunVal == QMessageBox.Ok):
                        self.toolWindow.closeWindow()
                    self.debugCnt = 0
                self.debugLastDistance = photo.sensor.avgDistance

        def disconnectSensor(self):
            photo.sensor.setToolboxOff()
            self.toolWindow.triggerDetectSignal()
            photo.terminate = True
            time.sleep(0.1)
            del photo.sensor
            time.sleep(0.1)
            photo.txtWriteArr = [0]*6
            photo.openedDrawerList = []
            self.toolWindow.updateDrawers(photo.openedDrawerList)
            self.workerThread.quit()
            self.workerThread.exit()
            del self.workerThread
            time.sleep(0.1)
            photo.video_capture_2.release()
            photo.video_capture.release()
            self.setLastStatus()
            self.setStatusLabel()
    """
    def dataMigrate(self):
        """Helps transfer data from SQLite to PostgreSQL."""
        self.database.insertSQLiteToPostgre(completeFlagParam = self.completeFlag)
        if self.completeFlag:
            self.database.clearLocalDB(completeFlagParam= self.completeFlag)
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("Veri tabanı aktarımı tamamlandı.")
            msg.setWindowTitle("İşlem Tamamlandı")
            msg.exec_()

    def addUser(self):
        self.statusLabel.setText("YETKİLİ KİŞİ GİRİŞİ")
        self.statusLabel.repaint()
        self.userWindowFlag = 1
        self.toolWindowFlag = 0
        self.isForLogin = True
        self.passwordEntry.show()
        self.passwordEntry.setFocus(True)
        self.hideButtons()

    def readCard(self):
        self.passwordEntry.setFocus(True)

    def readCardForLogin(self):
        self.statusLabel.setText("LÜTFEN KARTINIZI OKUTUN")
        self.statusLabel.repaint()
        self.toolWindowFlag = 1
        self.userWindowFlag = 0
        self.passwordEntry.show()
        self.passwordEntry.setFocus(True)
        self.isForLogin = True
        self.hideButtons()

    def showButtons(self):
        self.databaseButton.show()
        self.userButton.show()
        self.loginButton.show()
        self.rebootButton.show()
        self.shutDownButton.show()

    def hideButtons(self):
        self.databaseButton.hide()
        self.userButton.hide()
        self.loginButton.hide()
        self.rebootButton.hide()
        self.shutDownButton.hide()

    def updateStatus(self):
        pass

    def rebootSystem(self):
        #self.workerThread.quit()
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("Sistemi yeniden başlatmak istediğinize emin misiniz?")
        msg.setWindowTitle("Sistemi Yeniden Başlat")
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        ret = msg.exec_()
        if ret == QMessageBox.Ok:
            os.system("reboot")
        #os.system("sudo pkill -f _main.py")
        #self.close()

    def shutDownSystem(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("Sistemi kapatmak istediğinize emin misiniz?")
        msg.setWindowTitle("Sistemi Kapat")
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        ret = msg.exec_()
        if ret == QMessageBox.Ok:
            os.system("shutdown -h now")

    def addLogo(self):
        self.taiLogo = QLabel()
        self.taiLogo.setPixmap(QtGui.QPixmap("C:\\Users\\stand-alone1\\Desktop\\ats_new\\images\\tai-logo.png"))
        #self.taiLogo.setGeometry(QtCore.QRect(0, 0, 20, 20))
        self.taiLogo.setScaledContents(True)
        self.taiLogo.setMaximumSize(160,84)
        self.taiLogo.setAlignment(Qt.AlignRight | Qt.AlignCenter)
    
    def displayTime(self):
        current_time = QTime.currentTime()
        label_time = current_time.toString('hh:mm:ss')
        now = QDate.currentDate()
        self.timeLabel.setText(now.toString(Qt.ISODate) + "\n" + label_time)
        self.timeLabel.setAlignment(Qt.AlignRight)
        self.readCard()

    def setButtons(self):
        self.loginButton = QPushButton(self) # type: ignore
        self.loginButton.setIcon(QIcon("images/login-icon.png"))
        self.loginButton.setIconSize(self.buttonSize)
        self.loginButton.setStyleSheet("background-color: rgba(0, 153, 255, 30);border-width: 3px;border-color: #33cc33; border-radius: 25px")
        self.loginButton.hide()

        self.rebootButton = QPushButton(self)
        self.rebootButton.setIcon(QIcon("images/close-icon.png"))
        self.rebootButton.setIconSize(self.buttonSize)
        self.rebootButton.setStyleSheet("background-color: rgba(0, 153, 255, 30);border-width: 3px;border-color: #33cc33; border-radius: 25px;")
        self.rebootButton.hide()

        self.shutDownButton = QPushButton(self)
        self.shutDownButton.setIcon(QIcon("images/shutDown.png"))
        self.shutDownButton.setIconSize(self.buttonSize)
        self.shutDownButton.setStyleSheet("background-color: rgba(0, 153, 255, 30);border-width: 3px;border-color: #33cc33; border-radius: 25px;")
        self.shutDownButton.hide()
        
        self.userButton = QPushButton(self)
        self.userButton.setIcon(QIcon("images/user-icon.png"))
        self.userButton.setIconSize(self.buttonSize)
        self.userButton.setStyleSheet("background-color: rgba(0, 153, 255, 30);border-width: 3px;border-color: #33cc33; border-radius: 25px;")
        self.userButton.hide()

        self.databaseButton = QPushButton(self)
        self.databaseButton.setIcon(QIcon("images/database-icon.png"))
        self.databaseButton.setIconSize(self.buttonSize)
        self.databaseButton.setStyleSheet("background-color: rgba(0, 153, 255, 30);border-width: 3px;border-color: #33cc33; border-radius: 25px;")
        self.databaseButton.hide()

    def setStatusLabel(self):
        if (self.toolStatus == False):
            self.statusLabel.setText("EKSİK ALET BULUNMAKTADIR. (" + str(self.missingTools) + ")" + "\n GÖRMEK İÇİN GİRİŞ YAPINIZ.")
            self.statusLabel.repaint()
            self.statusLabel.setStyleSheet(self.toolNotExistBackground)
        else:
            self.statusLabel.setText("TÜM ALETLER YERİNDEDİR.")
            self.statusLabel.repaint()
            self.statusLabel.setStyleSheet(self.toolExistsBackground)

        font = self.statusLabel.font()
        font.setLetterSpacing(QFont.AbsoluteSpacing, 8)
        self.statusLabel.setAlignment(Qt.AlignCenter)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = CustomDialog()
    win.show()
    sys.exit(app.exec_())