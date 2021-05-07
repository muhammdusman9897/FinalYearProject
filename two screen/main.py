import mysql.connector
import cv2
import subprocess
import time
import threading
import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import QSize
from PyQt5.QtGui import * 
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QPropertyAnimation
from PyQt5.QtWidgets import QDialog, QApplication, QMessageBox
import tkinter.messagebox
mydb=mysql.connector.connect(host="localhost",user="root", passwd="1234", database="ser")

mycursor=mydb.cursor()


class SignupScreen(QDialog):
    def __init__(self):
        super(SignupScreen,self).__init__()
        loadUi("Sign-up-screen.ui",self)
        self.SignInBtn.clicked.connect(self.GoBack)
        self.SignupBtn.clicked.connect(self.Signup)
        global fName
        global lName
        global University
        global email
        global pwd
        fName=self.fNameLbl.text()
        lName=self.lNameLbl.text()
        University=self.universityLbl.text()
        email=self.emailLbl.text()
        pwd=self.pwdLbl.text()

    def Signup(self):
       
        try:
            
            query="""INSERT INTO teacher (FirstName,LastName, Institution,Email,UserPwd) VALUES (%s, %s, %s, %s, %s)"""
            values=(self.fNameLbl.text(),self.lNameLbl.text(),self.universityLbl.text(),self.emailLbl.text(),self.pwdLbl.text())
            mycursor.execute(query,values)
            mydb.commit()
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)

            msg.setText("Thankyou For signup")
            # msg.setInformativeText("This is additional information")
            msg.setWindowTitle("Sign up")
            # msg.setDetailedText("The details are as follows:")
            msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            
	
            retval = msg.exec_()
            
        except mysql.connector.Error as error:
            print("Failed to insert into MySQL table {}".format(error))
        
        finally:
            if mydb.is_connected():
                
                print("MySQL connection is closed")    

    def GoBack(self):
        MainWindow2 = MainWindow()
        widget.addWidget(MainWindow2)
        widget.setCurrentIndex(widget.currentIndex()+1)


class HomeScreen(QDialog):
    
    def __init__(self):
        
        super(HomeScreen,self).__init__()
        loadUi("Home2.ui",self)
        
        self.btn_toggle.clicked.connect(lambda: toggleMenu(self, 200, True))
        self.HomeBtn.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.Home_Page))
        self.AddCourseBtn.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.AddCourse_Page))
        self.EditEmotionBtn.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.EditEmotion_Page))
        self.PlayBtn.clicked.connect(self.showPopup)
        self.stopRecordingBtn.clicked.connect(self.stopRecording)
        self.emotionBtn.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.EditEmotion_Page))
        self.MainScreenUpdate.clicked.connect(self.showUpdatePopup)
        self.SearchStdBtn.clicked.connect(self.showSearchStdPopup)
        self.usernameTop.addItem("logout")   
        index=self.usernameTop.findText("UserName",QtCore.Qt.MatchFixedString)
        self.usernameTop.setItemText(0,username)
        self.usernameTop.currentTextChanged.connect(self._pullComboText)

    def _pullComboText(self, text):
        if(text==username):
            print(text)
        elif(text=="logout"):
            SigninScreen = MainWindow()
            widget.addWidget(SigninScreen)
            widget.setCurrentIndex(widget.currentIndex()+1)

      
    def stopRecording(self):
        msgBox=QMessageBox()
        msgBox.setWindowTitle("Stopping Recording")
        msgBox.setText("Are you sure?");
        msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        msgBox.setIcon(QMessageBox.Question)
        msgBox.buttonClicked.connect(self.cancelRecording)
        msgBox.exec();

    def cancelRecording(self):
        recording.terminate()
        cv2.destroyAllWindows()
        self.stopRecordingBtn.setIcon(QIcon("PlayButton.png"))
        self.stopRecordingBtn.setEnabled(False)
        self.stopRecordingBtn.setIconSize(QSize(40, 40));
        timerThread.stop()

    def nothing(self):
        return

    def showSearchStdPopup(self):
        self.dialog=Search_std_Popup()
        self.dialog.show()

       
    def showUpdatePopup(self):
        self.dialog=UpdatePopup()
        self.dialog.show()
    

    def showPopup(self):       
        self.dialog = StartMenu()
        self.dialog.show()
        

def toggleMenu(self, maxWidth, enable):
    
    if enable:
        width = self.frame_left_menu.width()
        maxEntend = maxWidth
        standard = 0

        if width == 0:
            widthExtended = maxEntend
        else:
            widthExtended = standard
        #animation
        self.animation = QPropertyAnimation(self.frame_left_menu, b"minimumWidth")
        self.animation.setDuration(400)
        self.animation.setStartValue(width) 
        self.animation.setEndValue(widthExtended)
        self.animation.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
      
        self.animation.start()  

class Search_std_Popup(QDialog):
    def __init__(self):
        super(Search_std_Popup,self).__init__()
        loadUi("Search-std-popup.ui",self)
        self.setWindowIcon(QIcon("SER-LOGO.png"))

class UpdatePopup(QDialog):
    def __init__(self):
        super(UpdatePopup,self).__init__()
        loadUi("update-popup.ui",self)
        self.setWindowIcon(QIcon("SER-LOGO.png"))
    def GoToMain(self):
        self.close()
        MHomeScreen.stackedWidget.setCurrentWidget(MHomeScreen.MainScreen_Page)

class MyThread(threading.Thread): 
    
    def __init__(self, *args, **kwargs): 
        super(MyThread, self).__init__(*args, **kwargs) 
        self._stop = threading.Event() 
  
    
    def stop(self): 
        self._stop.set() 
  
    def stopped(self): 
        return self._stop.isSet() 
  
    def run(self): 
        second = 0 
        minute = 0
        hours = 0
        while True: 
            if self.stopped(): 
                return
            time.sleep(1)    
            second+=1    
            if second == 60:    
                second = 0    
                minute += 1    
            if minute == 60:    
                minute = 0    
                hours += 1;  
            MHomeScreen.timerLbl.setText("{}:{}:{}".format(hours, minute, second))
          

class StartMenu(QDialog):
    
    def __init__(self):
        super(StartMenu,self).__init__()
        loadUi("Start-Menu.ui",self)
        self.DialogStartBtn.clicked.connect(self.GoToMain)
        self.setWindowIcon(QIcon("SER-LOGO.png"))
        self.setWindowTitle("startMenu")
    
    def GoToMain(self):
        self.close()
        global recording
        global timerThread
        recording = subprocess.Popen([sys.executable, './ScreenRecordingwithFaceRecognition.py'])
        MHomeScreen.stackedWidget.setCurrentWidget(MHomeScreen.MainScreen_Page)
        timerThread = MyThread()
        timerThread.start() 

  
class MainWindow(QDialog):
   
    def __init__(self):
        super(MainWindow,self).__init__() 
        
        loadUi("screen-1.ui",self)
        self.S1.clicked.connect(self.MoveToHome)
        self.SignupBtn.clicked.connect(self.MoveToSignUp)
  
    def MoveToSignUp(self):
        SignupScreen2 = SignupScreen()
        widget.addWidget(SignupScreen2)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def MoveToHome(self):
        email=self.EmailLbl.text()
        email2="muhammadusman9897@gmail.com"
        pwd=self.PwdLbl.text()
        result = False
        mycursor.execute("select * from teacher where Email=%s and UserPwd =%s " , (email,pwd))
        myresult = mycursor.fetchall()
        
        for x in myresult:
            global username
            username =(x[0]+" "+x[1])
            if(x):
                print(x)
                    
                result=True
            else:
                result=False
        


        if email == "" or pwd == "":
            msgBox=QMessageBox()
            msgBox.setWindowTitle("Error")
            msgBox.setText("Un No! you forget to fill all the fields");
            msgBox.setIcon(QMessageBox.Critical)
            msgBox.exec();

        elif result == True:
            global MHomeScreen
            global Currentind
            currentind = 0
            
            MHomeScreen = HomeScreen()
            MHomeScreen.setWindowIcon(QIcon("SER-LOGO.png"))
            screenObj=MHomeScreen
            widget.addWidget(MHomeScreen)
            widget.setCurrentIndex(widget.currentIndex()+1)
            print(result)
           
        else:
            print(result)
            msgBox=QMessageBox()
            msgBox.setWindowTitle("Error")
            msgBox.setText("Sorry Email or Password is incorrect");
            msgBox.setIcon(QMessageBox.Critical)
            msgBox.exec();
          





app=QApplication(sys.argv)
widget=QtWidgets.QStackedWidget()
mainwindow=MainWindow()

widget.addWidget(mainwindow)

widget.setFixedWidth(800)
widget.setFixedHeight(600)
widget.setWindowIcon(QIcon("SER-LOGO.png"))
widget.setWindowTitle("Student Engagement Recognizer - SER")

widget.show()

try:
    sys.exit(app.exec_())
except:
    print("Exiting")
