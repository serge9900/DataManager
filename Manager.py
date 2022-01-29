# Importing for checking existance of moduls
from email.headerregistry import Group
from imp import find_module
from re import I
from sys import platform
from os import system


# Imoprting for data collecting
from sqlalchemy import  create_engine
import pandas as pd

# Importing for main window setup
from Interface import *

# Importing for interfaces of windows
import icons_rc
from PySide2 import *
from PySide2.QtCore import QPropertyAnimation
from PySide2.QtWidgets import QPushButton, QSizeGrip, QTableWidgetItem, QMessageBox
from PySide2.QtGui import QStandardItemModel, QStandardItem, QFont
from qt_material import *

# Importing for doing validation of changed/added data
import validation

# Importing for connecting to SQL server
from pymysql import connect



### FUNCTION FOR CHECKING EXISTANCE OF
### REQUIRED MODULS AND INSTALLING THEM
def checkIfModulsAreExisting():
    modul = ["pandas", "PySide2", "qt_material", "PyQt5", "sqlalchemy", "pymysql"]

    for name in modul:
        try:
            find_module(name)
            found = True
        except:
            found = False
        if name == "qt_material":
            name = "qt-material"
        if not found:        
            if platform == "win32":
                try:
                    system('cmd /c "pip install {}"'.format(name.lower()))
                except:
                    pass

            elif platform == "linux" or "linux2":
                try:
                    system('pip install {}'.format(name.lower()))
                except:
                    pass

### FUNCTION FOR GETTING DATA FROM SQL SERVER
def GetData():
    TABLES = {
        "student": ["Student_ID", "Name", "Last_Name",
                    "Patronymic", "Birth_Date", "Address",
                    "Phone_Number", "Email", "Passport_ID"],
        "groupp": ["Group_ID", "Title"],
        "student_to_group": ["Date", "Student_ID", "Group_ID"],
        "position": ["Position_ID", "Title", "Salary"],
        "staff": ["Staff_ID", "Name", "Last_Name",
                  "Patronymic", "Education", "Address",
                  "Phone_Number", "Email", "Position_ID"],
        "instructor": ["Instructor_ID", "Staff_ID",
                       "Description", "Teaching_Object"],
        "audience": ["Audience_ID", "Title",
                     "Seat_Count", "Computer_Count"],
        "category": ["Category_ID", "Subject_Category"],
        "subject": ["Subject_ID", "Category_ID",
                    "Title", "Description", "Price"],
        "learningtype": ["Learning_Type_ID", "Title"],
        "schedule": ["Schedule_ID", "Group_ID", "Instructor_ID",
                     "Subject_ID", "Audience_ID", "Learning_Type_ID",
                     "Start_Date", "Finish_Date", "Time_Schedule"]
    }
    connection = create_engine("mysql+pymysql://"+uName+":"+Pass+"@"+Host+"/"+DataBase)
    RES_LIST = list()
    for name, col in TABLES.items():
        result = connection.execute('''SELECT * FROM ''' + name)
        RES_LIST.append(pd.DataFrame(result, columns=col))

    global STUDENTS, GROUPS, S2G, POSITION, STAFF, INSTRUCTOR, AUDIENCE, CATEGORY, SUBJECT, LEARNING_TYPE, SCHEDULE
    STUDENTS, GROUPS, S2G, POSITION, STAFF, INSTRUCTOR, AUDIENCE, CATEGORY, SUBJECT, LEARNING_TYPE, SCHEDULE = RES_LIST

    global student_dict, group_dict, position_dict, staff_dict, instructor_dict, audience_dict, category_dict, subject_dict, lType_dict
    global lType_ID_dict, audience_ID_dict, staff_ID_dict, group_ID_dict, subject_ID_dict, category_ID_dict, position_ID_dict
    student_dict = dict()
    group_dict = dict()
    position_dict = dict()
    staff_dict = dict()
    instructor_dict = dict()
    audience_dict = dict()
    category_dict = dict()
    subject_dict = dict()
    lType_dict = dict()
    lType_ID_dict = dict()
    audience_ID_dict = dict()
    staff_ID_dict = dict()
    group_ID_dict = dict()
    subject_ID_dict = dict()
    category_ID_dict = dict()
    position_ID_dict = dict()

    for x in range(len(STUDENTS)):
        student_dict[str(STUDENTS.Name[x]) + " " + str(STUDENTS.Last_Name[x])] = STUDENTS.Student_ID[x]

    for x in range(len(GROUPS)):
        group_dict[str(GROUPS.Title[x])] = GROUPS.Group_ID[x]

    for x in range(len(POSITION)):
        position_dict[str(POSITION.Title[x])] = POSITION.Position_ID[x]

    for x in range(len(STAFF)):
        staff_dict[str(STAFF.Name[x]) + " " + str(STAFF.Last_Name[x])] = STAFF.Staff_ID[x]

    for x in range(len(INSTRUCTOR)):
        instructor_dict[str(INSTRUCTOR.Teaching_Object[x])] = INSTRUCTOR.Instructor_ID[x]

    for x in range(len(AUDIENCE)):
        audience_dict[str(AUDIENCE.Title[x])] = AUDIENCE.Audience_ID[x]

    for x in range(len(CATEGORY)):
        category_dict[str(CATEGORY.Subject_Category[x])] = CATEGORY.Category_ID[x]

    for x in range(len(SUBJECT)):
        subject_dict[str(SUBJECT.Title[x])] = SUBJECT.Subject_ID[x]

    for x in range(len(LEARNING_TYPE)):
        lType_dict[str(LEARNING_TYPE.Title[x])] = LEARNING_TYPE.Learning_Type_ID[x]

######## New reverse Dicts

    for x in range(len(LEARNING_TYPE)):
        lType_ID_dict[LEARNING_TYPE.Learning_Type_ID[x]] = LEARNING_TYPE.Title[x]

    for x in range(len(AUDIENCE)):
        audience_ID_dict[AUDIENCE.Audience_ID[x]] = AUDIENCE.Title[x]

    for x in range(len(STAFF)):
        staff_ID_dict[STAFF.Staff_ID[x]] = STAFF.Name[x] + " " + STAFF.Last_Name[x]

    for x in range(len(GROUPS)):
        group_ID_dict[GROUPS.Group_ID[x]] = (GROUPS.Title[x])

    for x in range(len(SUBJECT)):
        subject_ID_dict[SUBJECT.Subject_ID[x]] = SUBJECT.Title[x]

    for x in range(len(CATEGORY)):
        category_ID_dict[CATEGORY.Category_ID[x]] = CATEGORY.Subject_Category[x]

    for x in range(len(POSITION)):
        position_ID_dict[POSITION.Position_ID[x]] = POSITION.Title[x]

### REGISTER WINDOW CLASS
class Ui_Form(object):
    def file2(self, Form):
        global uName, Pass, Host, DataBase
        uName = self.user_name.text()
        Pass = self.password.text()
        Host = self.ip_host.text()
        DataBase = self.data_base.text()
        
        #### ERROR WINDOW ####
        # If the input is incorrect, it asks to continue or exit the application #
        try:
            test = connect(host=Host, user=uName, passwd=Pass, db=DataBase)
            Form.close()
            test.close()
            self.test() 
        except:
            msg = QMessageBox.question(None, "Invalid Syntax","The login information is incorrect.\n \tRepeat?",
                                            QMessageBox.Yes | QMessageBox.Close)
            if msg == QMessageBox.Yes:
                pass
            else: 
                Form.close()

    def test(self):
        ui = MainWindow()
        ui.show() 
        
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(475, 640)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.widget = QtWidgets.QWidget(Form)
        self.widget.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.widget.setStyleSheet("background-color: #585858")
        self.widget.setObjectName("widget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setContentsMargins(-1, 15, -1, -1)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.frame = QtWidgets.QFrame(self.widget)
        self.frame.setMinimumSize(QtCore.QSize(0, 100))
        self.frame.setStyleSheet("background-color: rgb(0, 0, 0);")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.gridLayout = QtWidgets.QGridLayout(self.frame)
        self.gridLayout.setObjectName("gridLayout")
        self.pushButton_2 = QtWidgets.QPushButton(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_2.sizePolicy().hasHeightForWidth())
        self.pushButton_2.setSizePolicy(sizePolicy)
        self.pushButton_2.setMinimumSize(QtCore.QSize(100, 100))
        self.pushButton_2.setMaximumSize(QtCore.QSize(100, 16777215))
        self.pushButton_2.setStyleSheet("background-color: #3E3D3E;")
        self.pushButton_2.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icons8-logo-48.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_2.setIcon(icon)
        self.pushButton_2.setIconSize(QtCore.QSize(100, 100))
        self.pushButton_2.setFlat(True)
        self.pushButton_2.setObjectName("pushButton_2")
        self.gridLayout.addWidget(self.pushButton_2, 0, 0, 1, 1)
        self.verticalLayout_3.addWidget(self.frame)
        self.formLayout_2 = QtWidgets.QFormLayout()
        self.formLayout_2.setContentsMargins(50, 35, 59, -1)
        self.formLayout_2.setObjectName("formLayout_2")
        self.pushButton_5 = QtWidgets.QPushButton(self.widget)
        self.pushButton_5.setMaximumSize(QtCore.QSize(100, 100))
        self.pushButton_5.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("icons/Network-Ip-Address-icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_5.setIcon(icon1)
        self.pushButton_5.setIconSize(QtCore.QSize(50, 50))
        self.pushButton_5.setObjectName("pushButton_5")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.pushButton_5)
        self.pushButton_5.setStyleSheet("background-color: #411E8F")
        
     
        self.line = QtWidgets.QFrame(self.widget)
        self.line.setStyleSheet("border: 2px solid white;")
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.formLayout_2.setWidget(2, QtWidgets.QFormLayout.SpanningRole, self.line)
        self.pushButton_6 = QtWidgets.QPushButton(self.widget)
        self.pushButton_6.setMaximumSize(QtCore.QSize(100, 100))
        self.pushButton_6.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("icons/database-reload.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_6.setIcon(icon2)
        self.pushButton_6.setIconSize(QtCore.QSize(50, 50))
        self.pushButton_6.setObjectName("pushButton_6")
        self.formLayout_2.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.pushButton_6)
        self.pushButton_6.setStyleSheet("background-color: #411E8F")
        self.line_2 = QtWidgets.QFrame(self.widget)
        self.line_2.setStyleSheet("border: 2px solid grey;")
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.formLayout_2.setWidget(4, QtWidgets.QFormLayout.SpanningRole, self.line_2)
        self.pushButton_7 = QtWidgets.QPushButton(self.widget)
        self.pushButton_7.setMaximumSize(QtCore.QSize(100, 100))
        self.pushButton_7.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("icons/pngkey.com-avatar-png-3012756.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_7.setIcon(icon3)
        self.pushButton_7.setIconSize(QtCore.QSize(50, 50))
        self.pushButton_7.setObjectName("pushButton_7")
        self.formLayout_2.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.pushButton_7)
        self.pushButton_7.setStyleSheet("background-color: #411E8F")
        self.line_3 = QtWidgets.QFrame(self.widget)
        self.line_3.setStyleSheet("border: 2px solid white;")
        self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.formLayout_2.setWidget(6, QtWidgets.QFormLayout.SpanningRole, self.line_3)
        self.pushButton_8 = QtWidgets.QPushButton(self.widget)
        self.pushButton_8.setMaximumSize(QtCore.QSize(100, 100))
        self.pushButton_8.setText("")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("icons/PinClipart.com_ship-clipart-black-and_1303682.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_8.setIcon(icon4)
        self.pushButton_8.setIconSize(QtCore.QSize(50, 50))
        self.pushButton_8.setObjectName("pushButton_8")
        self.formLayout_2.setWidget(7, QtWidgets.QFormLayout.LabelRole, self.pushButton_8)
        self.pushButton_8.setStyleSheet("background-color: #411E8F")
        self.line_5 = QtWidgets.QFrame(self.widget)
        self.line_5.setStyleSheet("border: 2px solid grey;")
        self.line_5.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_5.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_5.setObjectName("line_5")
        self.formLayout_2.setWidget(8, QtWidgets.QFormLayout.SpanningRole, self.line_5)
        self.line_4 = QtWidgets.QFrame(self.widget)
        self.line_4.setStyleSheet("border: 2px solid orange;")
        self.line_4.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_4.setObjectName("line_4")
        self.formLayout_2.setWidget(9, QtWidgets.QFormLayout.LabelRole, self.line_4)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.formLayout_2.setItem(9, QtWidgets.QFormLayout.FieldRole, spacerItem)
        self.sign_in = QtWidgets.QPushButton(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sign_in.sizePolicy().hasHeightForWidth())
        self.sign_in.setSizePolicy(sizePolicy)
        self.sign_in.setMinimumSize(QtCore.QSize(0, 60))
        self.sign_in.setMouseTracking(False)
        self.sign_in.setAutoFillBackground(False)
        self.sign_in.setStyleSheet("QPushButton{background-color: black;\n"
                                    "selection-color: rgb(84, 64, 206);\n"
                                    "selection-background-color: rgb(81, 64, 201);\n"
                                    "font: 17pt \"Verdana\";\n"
                                    "border: 2px solid grey;\n"
                                    "padding: 5px;\n"
                                    "border-radius: 3px;\n"
                                    "opacity: 200;color: rgb(231, 231, 231);\n"
                                    "selection-color: rgb(84, 64, 206);\n"
                                    "selection-background-color: rgb(81, 64, 201);\n"
                                    "font: 17pt \"Verdana\";\n"
                                    "border: 2px solid grey;\n"
                                    "padding: 5px;\n"
                                    "border-radius: 3px;\n"
                                    "opacity: 200;}\n"
                                    "QPushButton::pressed{\n"
                                    "background-color:  #310A5D}")
        self.sign_in.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.sign_in.setIconSize(QtCore.QSize(16, 16))
        self.sign_in.setAutoDefault(False)
        self.sign_in.setDefault(False)
        self.sign_in.setFlat(False)
        self.sign_in.setObjectName("sign_in")
        self.formLayout_2.setWidget(10, QtWidgets.QFormLayout.SpanningRole, self.sign_in)
        self.ip_host = QtWidgets.QLineEdit(self.widget)
        self.ip_host.setMinimumSize(QtCore.QSize(256, 60))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.ip_host.setFont(font)
        self.ip_host.setText("")
        self.ip_host.setMaxLength(9999999)
        self.ip_host.setObjectName("ip_host")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.ip_host)
        self.ip_host.setStyleSheet("background-color: #A4A4A4;")
        self.data_base = QtWidgets.QLineEdit(self.widget)
        self.data_base.setEchoMode(QtWidgets.QLineEdit.Password)
        self.data_base.setMinimumSize(QtCore.QSize(256, 60))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.data_base.setFont(font)
        self.data_base.setText("")
        self.data_base.setMaxLength(9999999)
        self.data_base.setObjectName("data_base")
        self.formLayout_2.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.data_base)
        self.data_base.setStyleSheet("background-color: #A4A4A4")
        self.password = QtWidgets.QLineEdit(self.widget)
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.password.setMinimumSize(QtCore.QSize(256, 60))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.password.setFont(font)
        self.password.setText("")
        self.password.setMaxLength(9999999)
        self.password.setObjectName("password")
        self.formLayout_2.setWidget(7, QtWidgets.QFormLayout.FieldRole, self.password)
        self.password.setStyleSheet("background-color: #A4A4A4")
        self.user_name = QtWidgets.QLineEdit(self.widget)
        self.user_name.setMinimumSize(QtCore.QSize(256, 60))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.user_name.setFont(font)
        self.user_name.setText("")
        self.user_name.setMaxLength(9999999)
        self.user_name.setPlaceholderText("Username")
        self.user_name.setObjectName("user_name")
        self.formLayout_2.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.user_name)
        self.user_name.setStyleSheet("background-color: #A4A4A4")
        self.verticalLayout_3.addLayout(self.formLayout_2)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem1)
        self.label = QtWidgets.QLabel(self.widget)
        self.label.setTextFormat(QtCore.Qt.PlainText)
        self.label.setObjectName("label")
        self.verticalLayout_3.addWidget(self.label, 0, QtCore.Qt.AlignHCenter)
        self.verticalLayout_2.addLayout(self.verticalLayout_3)
        self.horizontalLayout_3.addWidget(self.widget)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
       

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)
        
        self.sign_in.clicked.connect(lambda: self.file2(Form))


    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.sign_in.setText(_translate("Form", "Sign In"))
        self.ip_host.setPlaceholderText(_translate("Form", "Host"))
        self.data_base.setPlaceholderText(_translate("Form", "Data Base"))
        self.password.setPlaceholderText(_translate("Form", "Password"))
        self.label.setText(_translate("Form", "Powered by ColoAI."))
        
### ENTER/REPLACE WINDOW CLASSES
class Ui_Audience_Enter_Window(object):
    def setupUi(self, Audience_Enter_Window):
        Audience_Enter_Window.setObjectName("Audience_Enter_Window")
        Audience_Enter_Window.resize(400, 205)
        Audience_Enter_Window.setMinimumSize(QtCore.QSize(400, 205))
        Audience_Enter_Window.setMaximumSize(QtCore.QSize(400, 205))
        self.frame = QtWidgets.QFrame(Audience_Enter_Window)
        self.frame.setGeometry(QtCore.QRect(5, 5, 390, 161))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.frame_3 = QtWidgets.QFrame(self.frame)
        self.frame_3.setGeometry(QtCore.QRect(5, 5, 140, 151))
        self.frame_3.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.label = QtWidgets.QLabel(self.frame_3)
        self.label.setGeometry(QtCore.QRect(10, 10, 120, 30))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.frame_3)
        self.label_2.setGeometry(QtCore.QRect(10, 46, 120, 30))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.frame_3)
        self.label_3.setGeometry(QtCore.QRect(10, 82, 120, 30))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.frame_3)
        self.label_4.setGeometry(QtCore.QRect(10, 115, 120, 30))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.frame_4 = QtWidgets.QFrame(self.frame)
        self.frame_4.setGeometry(QtCore.QRect(150, 5, 235, 151))
        self.frame_4.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_4.setObjectName("frame_4")
        self.audience_title_enter_lineEdit = QtWidgets.QLineEdit(self.frame_4)
        self.audience_title_enter_lineEdit.setGeometry(QtCore.QRect(10, 14, 215, 25))
        self.audience_title_enter_lineEdit.setObjectName("audience_title_enter_lineEdit")
        self.audience_seatCount_enter_lineEdit = QtWidgets.QLineEdit(self.frame_4)
        self.audience_seatCount_enter_lineEdit.setGeometry(QtCore.QRect(10, 49, 215, 25))
        self.audience_seatCount_enter_lineEdit.setObjectName("audience_seatCount_enter_lineEdit")
        self.audience_camputer_count_enter_lineEdit = QtWidgets.QLineEdit(self.frame_4)
        self.audience_camputer_count_enter_lineEdit.setGeometry(QtCore.QRect(10, 84, 215, 25))
        self.audience_camputer_count_enter_lineEdit.setObjectName("audience_camputer_count_enter_lineEdit")
        self.audience_ID_enter_lineEdit = QtWidgets.QLineEdit(self.frame_4)
        self.audience_ID_enter_lineEdit.setGeometry(QtCore.QRect(10, 119, 215, 25))
        self.audience_ID_enter_lineEdit.setObjectName("audience_ID_enter_lineEdit")
        self.frame_2 = QtWidgets.QFrame(Audience_Enter_Window)
        self.frame_2.setGeometry(QtCore.QRect(5, 170, 390, 30))
        self.frame_2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.audience_enter_pushButton = QtWidgets.QPushButton(self.frame_2)
        self.audience_enter_pushButton.setGeometry(QtCore.QRect(160, 3, 70, 25))
        font = QtGui.QFont()
        font.setBold(True)
        font.setItalic(False)
        font.setUnderline(True)
        font.setWeight(75)
        font.setStrikeOut(False)
        font.setKerning(True)
        self.audience_enter_pushButton.setFont(font)
        self.audience_enter_pushButton.setObjectName("audience_enter_pushButton")

        self.retranslateUi(Audience_Enter_Window)
        QtCore.QMetaObject.connectSlotsByName(Audience_Enter_Window)

    def retranslateUi(self, Audience_Enter_Window):
        _translate = QtCore.QCoreApplication.translate
        Audience_Enter_Window.setWindowTitle(_translate("Audience_Enter_Window", "Enter"))
        self.label.setText(_translate("Audience_Enter_Window", "Title"))
        self.label_2.setText(_translate("Audience_Enter_Window", "Seat Count"))
        self.label_3.setText(_translate("Audience_Enter_Window", "Camputer Count"))
        self.label_4.setText(_translate("Audience_Enter_Window", "ID"))
        self.audience_enter_pushButton.setText(_translate("Audience_Enter_Window", "OK"))
class Ui_Audience_Replace_Window(object):
    def setupUi(self, Audience_Replace_Window):
        Audience_Replace_Window.setObjectName("Audience_Replace_Window")
        Audience_Replace_Window.resize(400, 205)
        Audience_Replace_Window.setMinimumSize(QtCore.QSize(400, 205))
        Audience_Replace_Window.setMaximumSize(QtCore.QSize(400, 205))
        self.frame = QtWidgets.QFrame(Audience_Replace_Window)
        self.frame.setGeometry(QtCore.QRect(5, 5, 390, 161))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.frame_3 = QtWidgets.QFrame(self.frame)
        self.frame_3.setGeometry(QtCore.QRect(5, 5, 140, 151))
        self.frame_3.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.label = QtWidgets.QLabel(self.frame_3)
        self.label.setGeometry(QtCore.QRect(10, 10, 120, 30))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.frame_3)
        self.label_2.setGeometry(QtCore.QRect(10, 46, 120, 30))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.frame_3)
        self.label_3.setGeometry(QtCore.QRect(10, 82, 120, 30))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.frame_3)
        self.label_4.setGeometry(QtCore.QRect(10, 115, 120, 30))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.label_4.setStyleSheet("color: red")
        self.frame_4 = QtWidgets.QFrame(self.frame)
        self.frame_4.setGeometry(QtCore.QRect(150, 5, 235, 151))
        self.frame_4.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_4.setObjectName("frame_4")
        self.audience_title_replace_lineEdit = QtWidgets.QLineEdit(self.frame_4)
        self.audience_title_replace_lineEdit.setGeometry(QtCore.QRect(10, 14, 215, 25))
        self.audience_title_replace_lineEdit.setObjectName("audience_title_replace_lineEdit")
        self.audience_seatCount_replace_lineEdit = QtWidgets.QLineEdit(self.frame_4)
        self.audience_seatCount_replace_lineEdit.setGeometry(QtCore.QRect(10, 49, 215, 25))
        self.audience_seatCount_replace_lineEdit.setObjectName("audience_seatCount_replace_lineEdit")
        self.audience_camputer_count_replace_lineEdit = QtWidgets.QLineEdit(self.frame_4)
        self.audience_camputer_count_replace_lineEdit.setGeometry(QtCore.QRect(10, 84, 215, 25))
        self.audience_camputer_count_replace_lineEdit.setObjectName("audience_camputer_count_replace_lineEdit")
        self.audience_ID_replace_comboBox = QtWidgets.QComboBox(self.frame_4)
        self.audience_ID_replace_comboBox.setGeometry(QtCore.QRect(10, 119, 215, 25))
        self.audience_ID_replace_comboBox.setObjectName("audience_ID_replace_comboBox")
        for i in range(len(audience_dict)):
            self.audience_ID_replace_comboBox.addItem("")
        self.frame_2 = QtWidgets.QFrame(Audience_Replace_Window)
        self.frame_2.setGeometry(QtCore.QRect(5, 170, 390, 30))
        self.frame_2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.audience_replace_pushButton = QtWidgets.QPushButton(self.frame_2)
        self.audience_replace_pushButton.setGeometry(QtCore.QRect(160, 3, 70, 25))
        font = QtGui.QFont()
        font.setBold(True)
        font.setItalic(False)
        font.setUnderline(True)
        font.setWeight(75)
        font.setStrikeOut(False)
        font.setKerning(True)
        self.audience_replace_pushButton.setFont(font)
        self.audience_replace_pushButton.setObjectName("audience_replace_pushButton")

        self.retranslateUi(Audience_Replace_Window)
        QtCore.QMetaObject.connectSlotsByName(Audience_Replace_Window)

    def updateCombo(self, index):
        self.audience_title_replace_lineEdit.setText(str(list(AUDIENCE.Title)[index]))
        self.audience_seatCount_replace_lineEdit.setText(str(list(AUDIENCE.Seat_Count)[index]))
        self.audience_camputer_count_replace_lineEdit.setText(str(list(AUDIENCE.Computer_Count)[index]))

    def retranslateUi(self, Audience_Replace_Window):
        _translate = QtCore.QCoreApplication.translate
        Audience_Replace_Window.setWindowTitle(_translate("Audience_Replace_Window", "Update"))
        self.label.setText(_translate("Audience_Replace_Window", "Title"))
        self.label_2.setText(_translate("Audience_Replace_Window", "Seat Count"))
        self.label_3.setText(_translate("Audience_Replace_Window", "Camputer Count"))
        self.label_4.setText(_translate("Audience_Replace_Window", "ID"))
        self.audience_title_replace_lineEdit.setText(str(list(AUDIENCE.Title)[0]))
        self.audience_seatCount_replace_lineEdit.setText(str(list(AUDIENCE.Seat_Count)[0]))
        self.audience_camputer_count_replace_lineEdit.setText(str(list(AUDIENCE.Computer_Count)[0]))
        for value in audience_dict.values():
            self.audience_ID_replace_comboBox.setItemText(list(audience_dict.values()).index(value), _translate("Audience_Replace_Window", str(value)))
        self.audience_replace_pushButton.setText(_translate("Audience_Replace_Window", "OK"))
        self.audience_ID_replace_comboBox.currentIndexChanged.connect(self.updateCombo)
class Ui_Category_Enter_Window(object):
    def setupUi(self, Category_Enter_Window):
        Category_Enter_Window.setObjectName("Category_Enter_Window")
        Category_Enter_Window.resize(400, 105)
        Category_Enter_Window.setMinimumSize(QtCore.QSize(400, 105))
        Category_Enter_Window.setMaximumSize(QtCore.QSize(400, 105))
        self.frame = QtWidgets.QFrame(Category_Enter_Window)
        self.frame.setGeometry(QtCore.QRect(5, 5, 390, 61))
        self.frame.setFrameShape(QtWidgets.QFrame.Panel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.frame_3 = QtWidgets.QFrame(self.frame)
        self.frame_3.setGeometry(QtCore.QRect(5, 5, 140, 51))
        self.frame_3.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setLineWidth(0)
        self.frame_3.setObjectName("frame_3")
        self.label = QtWidgets.QLabel(self.frame_3)
        self.label.setGeometry(QtCore.QRect(10, 10, 120, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.frame_4 = QtWidgets.QFrame(self.frame)
        self.frame_4.setGeometry(QtCore.QRect(150, 5, 235, 51))
        self.frame_4.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_4.setObjectName("frame_4")
        self.category_subjectCategory_enter_lineEdit = QtWidgets.QLineEdit(self.frame_4)
        self.category_subjectCategory_enter_lineEdit.setGeometry(QtCore.QRect(10, 14, 215, 25))
        self.category_subjectCategory_enter_lineEdit.setObjectName("category_subjectCategory_enter_lineEdit")
        self.frame_2 = QtWidgets.QFrame(Category_Enter_Window)
        self.frame_2.setGeometry(QtCore.QRect(5, 70, 390, 30))
        font = QtGui.QFont()
        font.setKerning(True)
        self.frame_2.setFont(font)
        self.frame_2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.category_enter_pushButton = QtWidgets.QPushButton(self.frame_2)
        self.category_enter_pushButton.setGeometry(QtCore.QRect(160, 3, 70, 25))
        font = QtGui.QFont()
        font.setBold(True)
        font.setUnderline(True)
        font.setWeight(75)
        self.category_enter_pushButton.setFont(font)
        self.category_enter_pushButton.setObjectName("category_enter_pushButton")

        self.retranslateUi(Category_Enter_Window)
        QtCore.QMetaObject.connectSlotsByName(Category_Enter_Window)

    def retranslateUi(self, Category_Enter_Window):
        _translate = QtCore.QCoreApplication.translate
        Category_Enter_Window.setWindowTitle(_translate("Category_Enter_Window", "Enter"))
        self.label.setText(_translate("Category_Enter_Window", "Subject Category"))
        self.category_enter_pushButton.setText(_translate("Category_Enter_Window", "OK"))
class Ui_Category_Replace_Window(object):
    def setupUi(self, Category_Replace_Window):
        Category_Replace_Window.setObjectName("Category_Replace_Window")
        Category_Replace_Window.resize(400, 145)
        Category_Replace_Window.setMinimumSize(QtCore.QSize(400, 145))
        Category_Replace_Window.setMaximumSize(QtCore.QSize(400, 145))
        self.frame = QtWidgets.QFrame(Category_Replace_Window)
        self.frame.setGeometry(QtCore.QRect(5, 5, 390, 101))
        self.frame.setFrameShape(QtWidgets.QFrame.Panel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.frame_3 = QtWidgets.QFrame(self.frame)
        self.frame_3.setGeometry(QtCore.QRect(5, 5, 140, 81))
        self.frame_3.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setLineWidth(0)
        self.frame_3.setObjectName("frame_3")
        self.label = QtWidgets.QLabel(self.frame_3)
        self.label.setGeometry(QtCore.QRect(10, 10, 120, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.frame_3)
        self.label_2.setGeometry(QtCore.QRect(10, 46, 120, 30))
        self.label_2.setStyleSheet("color: red")
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.frame_4 = QtWidgets.QFrame(self.frame)
        self.frame_4.setGeometry(QtCore.QRect(150, 5, 235, 81))
        self.frame_4.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_4.setObjectName("frame_4")
        self.category_subjectCategory_replace_lineEdit = QtWidgets.QLineEdit(self.frame_4)
        self.category_subjectCategory_replace_lineEdit.setGeometry(QtCore.QRect(10, 14, 215, 25))
        self.category_subjectCategory_replace_lineEdit.setObjectName("category_subjectCategory_replace_lineEdit")
        self.category_ID_replace_comboBox = QtWidgets.QComboBox(self.frame_4)
        self.category_ID_replace_comboBox.setGeometry(QtCore.QRect(10, 49, 215, 25))
        self.category_ID_replace_comboBox.setObjectName("category_ID_replace_comboBox")
        for i in range(len(category_dict)):
            self.category_ID_replace_comboBox.addItem("")
        self.frame_2 = QtWidgets.QFrame(Category_Replace_Window)
        self.frame_2.setGeometry(QtCore.QRect(5, 110, 390, 30))
        font = QtGui.QFont()
        font.setKerning(True)
        self.frame_2.setFont(font)
        self.frame_2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.category_replace_pushButton = QtWidgets.QPushButton(self.frame_2)
        self.category_replace_pushButton.setGeometry(QtCore.QRect(160, 3, 70, 25))
        font = QtGui.QFont()
        font.setBold(True)
        font.setUnderline(True)
        font.setWeight(75)
        self.category_replace_pushButton.setFont(font)
        self.category_replace_pushButton.setObjectName("category_replace_pushButton")

        self.retranslateUi(Category_Replace_Window)
        QtCore.QMetaObject.connectSlotsByName(Category_Replace_Window)

    def updateCombo(self, index):
        self.category_subjectCategory_replace_lineEdit.setText(str(list(CATEGORY.Subject_Category)[index]))

    def retranslateUi(self, Category_Replace_Window):
        _translate = QtCore.QCoreApplication.translate
        Category_Replace_Window.setWindowTitle(_translate("Category_Replace_Window", "Update"))
        self.label.setText(_translate("Category_Replace_Window", "Subject Category"))
        self.label_2.setText(_translate("Category_Replace_Window", "ID"))
        self.category_subjectCategory_replace_lineEdit.setText(str(list(CATEGORY.Subject_Category)[0]))
        for i in range(len(category_dict)):
            self.category_ID_replace_comboBox.setItemText(i, _translate("Category_Replace_Window", str(i+1)))
        self.category_replace_pushButton.setText(_translate("Category_Replace_Window", "OK"))
        self.category_ID_replace_comboBox.currentIndexChanged.connect(self.updateCombo)
class Ui_Group_Enter_Window(object):
    def setupUi(self, Group_Enter_Window):
        Group_Enter_Window.setObjectName("Group_Enter_Window")
        Group_Enter_Window.resize(400, 120)
        Group_Enter_Window.setMinimumSize(QtCore.QSize(400, 120))
        Group_Enter_Window.setMaximumSize(QtCore.QSize(400, 120))
        self.frame = QtWidgets.QFrame(Group_Enter_Window)
        self.frame.setGeometry(QtCore.QRect(5, 5, 390, 65))
        self.frame.setFrameShape(QtWidgets.QFrame.Panel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.frame_3 = QtWidgets.QFrame(self.frame)
        self.frame_3.setGeometry(QtCore.QRect(5, 5, 140, 55))
        self.frame_3.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.description_txt = QtWidgets.QLabel(self.frame_3)
        self.description_txt.setGeometry(QtCore.QRect(10, 10, 120, 30))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.description_txt.setFont(font)
        self.description_txt.setObjectName("description_txt")
        self.frame_4 = QtWidgets.QFrame(self.frame)
        self.frame_4.setGeometry(QtCore.QRect(150, 5, 235, 55))
        self.frame_4.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_4.setObjectName("frame_4")
        self.group_enter_title_line = QtWidgets.QLineEdit(self.frame_4)
        self.group_enter_title_line.setGeometry(QtCore.QRect(10, 14, 215, 25))
        self.group_enter_title_line.setObjectName("group_enter_title_line")
        self.frame_2 = QtWidgets.QFrame(Group_Enter_Window)
        self.frame_2.setGeometry(QtCore.QRect(5, 80, 390, 30))
        self.frame_2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.pushButton = QtWidgets.QPushButton(self.frame_2)
        self.pushButton.setGeometry(QtCore.QRect(160, 3, 70, 25))
        self.pushButton.setObjectName("pushButton")

        self.retranslateUi(Group_Enter_Window)
        QtCore.QMetaObject.connectSlotsByName(Group_Enter_Window)

    def retranslateUi(self, Group_Enter_Window):
        _translate = QtCore.QCoreApplication.translate
        Group_Enter_Window.setWindowTitle(_translate("Group_Enter_Window", "Enter"))
        self.description_txt.setText(_translate("Group_Enter_Window", "Title"))
        self.pushButton.setText(_translate("Group_Enter_Window", "OK"))
class Ui_Group_Replace_Window(object):
    def setupUi(self, Group_Replace_Window):
        Group_Replace_Window.setObjectName("Group_Replace_Window")
        Group_Replace_Window.resize(400, 150)
        Group_Replace_Window.setMinimumSize(QtCore.QSize(400, 150))
        Group_Replace_Window.setMaximumSize(QtCore.QSize(400, 150))
        self.frame = QtWidgets.QFrame(Group_Replace_Window)
        self.frame.setGeometry(QtCore.QRect(5, 5, 390, 100))
        self.frame.setFrameShape(QtWidgets.QFrame.Panel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.frame_3 = QtWidgets.QFrame(self.frame)
        self.frame_3.setGeometry(QtCore.QRect(5, 5, 140, 100))
        self.frame_3.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.group_rename_title_txt = QtWidgets.QLabel(self.frame_3)
        self.group_rename_title_txt.setGeometry(QtCore.QRect(10, 10, 120, 30))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.group_rename_title_txt.setFont(font)
        self.group_rename_title_txt.setObjectName("group_rename_title_txt")
        self.group_rename_id_txt = QtWidgets.QLabel(self.frame_3)
        self.group_rename_id_txt.setGeometry(QtCore.QRect(10, 46, 67, 19))
        self.group_rename_id_txt.setStyleSheet("color: red")
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.group_rename_id_txt.setFont(font)
        self.group_rename_id_txt.setObjectName("group_rename_id_txt")
        self.frame_4 = QtWidgets.QFrame(self.frame)
        self.frame_4.setGeometry(QtCore.QRect(150, 5, 235, 100))
        self.frame_4.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_4.setObjectName("frame_4")
        self.group_rename_title_line = QtWidgets.QLineEdit(self.frame_4)
        self.group_rename_title_line.setGeometry(QtCore.QRect(10, 14, 215, 25))
        self.group_rename_title_line.setObjectName("group_rename_title_line")
        self.group_rename_id_combo_box = QtWidgets.QComboBox(self.frame_4)
        self.group_rename_id_combo_box.setGeometry(QtCore.QRect(10, 49, 215, 25))
        self.group_rename_id_combo_box.setObjectName("group_rename_id_combo_box")
        for i in range(len(group_dict)):
            self.group_rename_id_combo_box.addItem("")
        self.frame_2 = QtWidgets.QFrame(Group_Replace_Window)
        self.frame_2.setGeometry(QtCore.QRect(5, 115, 390, 30))
        self.frame_2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.pushButton = QtWidgets.QPushButton(self.frame_2)
        self.pushButton.setGeometry(QtCore.QRect(160, 3, 70, 25))
        font = QtGui.QFont()
        font.setBold(True)
        font.setUnderline(True)
        font.setWeight(75)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")

        self.retranslateUi(Group_Replace_Window)
        QtCore.QMetaObject.connectSlotsByName(Group_Replace_Window)

    def updateCombo(self, index):
        self.group_rename_title_line.setText(str(list(GROUPS.Title)[index]))

    def retranslateUi(self, Group_Replace_Window):
        _translate = QtCore.QCoreApplication.translate
        Group_Replace_Window.setWindowTitle(_translate("Group_Replace_Window", "Update"))
        self.group_rename_title_txt.setText(_translate("Group_Replace_Window", "Title"))
        self.group_rename_id_txt.setText(_translate("Group_Replace_Window", "ID"))
        self.group_rename_title_line.setText(str(list(GROUPS.Title)[0]))
        for i in range(len(group_dict)):
            self.group_rename_id_combo_box.setItemText(i, _translate("Group_Replace_Window", str(i+1)))
        self.pushButton.setText(_translate("Group_Replace_Window", "OK"))
        self.group_rename_id_combo_box.currentIndexChanged.connect(self.updateCombo)
class Ui_Instructor_Enter_Window(object):
    def setupUi(self, Instructor_Enter_Window):
        Instructor_Enter_Window.setObjectName("Instructor_Enter_Window")
        Instructor_Enter_Window.resize(400, 180)
        Instructor_Enter_Window.setMinimumSize(QtCore.QSize(400, 180))
        Instructor_Enter_Window.setMaximumSize(QtCore.QSize(400, 180))
        self.frame = QtWidgets.QFrame(Instructor_Enter_Window)
        self.frame.setGeometry(QtCore.QRect(5, 5, 390, 130))
        self.frame.setFrameShape(QtWidgets.QFrame.Panel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.frame_3 = QtWidgets.QFrame(self.frame)
        self.frame_3.setGeometry(QtCore.QRect(5, 5, 140, 120))
        self.frame_3.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.description_txt = QtWidgets.QLabel(self.frame_3)
        self.description_txt.setGeometry(QtCore.QRect(10, 46, 120, 30))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.description_txt.setFont(font)
        self.description_txt.setObjectName("description_txt")
        self.instructor_enter_staff_id_label = QtWidgets.QLabel(self.frame_3)
        self.instructor_enter_staff_id_label.setGeometry(QtCore.QRect(10, 10, 120, 30))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.instructor_enter_staff_id_label.setFont(font)
        self.instructor_enter_staff_id_label.setObjectName("instructor_enter_staff_id_label")
        self.instructor_enter_teaching_object_txt = QtWidgets.QLabel(self.frame_3)
        self.instructor_enter_teaching_object_txt.setGeometry(QtCore.QRect(10, 82, 120, 30))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.instructor_enter_teaching_object_txt.setFont(font)
        self.instructor_enter_teaching_object_txt.setObjectName("instructor_enter_teaching_object_txt")
        self.frame_4 = QtWidgets.QFrame(self.frame)
        self.frame_4.setGeometry(QtCore.QRect(150, 5, 235, 120))
        self.frame_4.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_4.setObjectName("frame_4")
        self.instructor_enter_description_line = QtWidgets.QLineEdit(self.frame_4)
        self.instructor_enter_description_line.setGeometry(QtCore.QRect(10, 49, 215, 25))
        self.instructor_enter_description_line.setObjectName("instructor_enter_description_line")
        self.instructor_enter_staff_id_combo_box = QtWidgets.QComboBox(self.frame_4)
        self.instructor_enter_staff_id_combo_box.setGeometry(QtCore.QRect(10, 14, 215, 25))
        self.instructor_enter_staff_id_combo_box.setObjectName("instructor_enter_staff_id_combo_box")
        for i in range(len(staff_dict)):
            self.instructor_enter_staff_id_combo_box.addItem("")
        self.instructor_enter_teaching_object_line = QtWidgets.QLineEdit(self.frame_4)
        self.instructor_enter_teaching_object_line.setGeometry(QtCore.QRect(10, 84, 215, 25))
        self.instructor_enter_teaching_object_line.setObjectName("instructor_enter_teaching_object_line")
        self.frame_2 = QtWidgets.QFrame(Instructor_Enter_Window)
        self.frame_2.setGeometry(QtCore.QRect(5, 145, 390, 30))
        self.frame_2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.pushButton = QtWidgets.QPushButton(self.frame_2)
        self.pushButton.setGeometry(QtCore.QRect(160, 3, 70, 25))
        font = QtGui.QFont()
        font.setBold(True)
        font.setUnderline(True)
        font.setWeight(75)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")

        self.retranslateUi(Instructor_Enter_Window)
        QtCore.QMetaObject.connectSlotsByName(Instructor_Enter_Window)

    def retranslateUi(self, Instructor_Enter_Window):
        _translate = QtCore.QCoreApplication.translate
        Instructor_Enter_Window.setWindowTitle(_translate("Instructor_Enter_Window", "Enter"))
        self.description_txt.setText(_translate("Instructor_Enter_Window", "Description"))
        self.instructor_enter_staff_id_label.setText(_translate("Instructor_Enter_Window", "Staff"))
        self.instructor_enter_teaching_object_txt.setText(_translate("Instructor_Enter_Window", "Teaching Object"))
        for key, value in staff_dict.items():
            self.instructor_enter_staff_id_combo_box.setItemText(value-1, _translate("Instructor_Enter_Window", key))
        self.pushButton.setText(_translate("Instructor_Enter_Window", "OK"))
class Ui_Instructor_Replace_Window(object):
    def setupUi(self, Instructor_Replace_Window):
        Instructor_Replace_Window.setObjectName("Instructor_Replace_Window")
        Instructor_Replace_Window.resize(400, 215)
        Instructor_Replace_Window.setMinimumSize(QtCore.QSize(400, 215))
        Instructor_Replace_Window.setMaximumSize(QtCore.QSize(400, 215))
        self.frame = QtWidgets.QFrame(Instructor_Replace_Window)
        self.frame.setGeometry(QtCore.QRect(5, 5, 390, 170))
        self.frame.setFrameShape(QtWidgets.QFrame.Panel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.frame_3 = QtWidgets.QFrame(self.frame)
        self.frame_3.setGeometry(QtCore.QRect(5, 5, 140, 160))
        self.frame_3.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.instructor_rename_description_txt = QtWidgets.QLabel(self.frame_3)
        self.instructor_rename_description_txt.setGeometry(QtCore.QRect(10, 46, 120, 30))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.instructor_rename_description_txt.setFont(font)
        self.instructor_rename_description_txt.setObjectName("instructor_rename_description_txt")
        self.instructor_rename_staff_id_label = QtWidgets.QLabel(self.frame_3)
        self.instructor_rename_staff_id_label.setGeometry(QtCore.QRect(10, 10, 120, 30))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.instructor_rename_staff_id_label.setFont(font)
        self.instructor_rename_staff_id_label.setObjectName("instructor_rename_staff_id_label")
        self.instructor_rename_teaching_object_txt = QtWidgets.QLabel(self.frame_3)
        self.instructor_rename_teaching_object_txt.setGeometry(QtCore.QRect(10, 82, 120, 30))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.instructor_rename_teaching_object_txt.setFont(font)
        self.instructor_rename_teaching_object_txt.setObjectName("instructor_rename_teaching_object_txt")
        self.instructor_rename_id_label = QtWidgets.QLabel(self.frame_3)
        self.instructor_rename_id_label.setGeometry(QtCore.QRect(10, 128, 67, 19))
        self.instructor_rename_id_label.setStyleSheet("color: red")
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.instructor_rename_id_label.setFont(font)
        self.instructor_rename_id_label.setObjectName("instructor_rename_id_label")
        self.frame_4 = QtWidgets.QFrame(self.frame)
        self.frame_4.setGeometry(QtCore.QRect(150, 5, 235, 160))
        self.frame_4.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_4.setObjectName("frame_4")
        self.instructor_rename_description_line = QtWidgets.QLineEdit(self.frame_4)
        self.instructor_rename_description_line.setGeometry(QtCore.QRect(10, 49, 215, 25))
        self.instructor_rename_description_line.setObjectName("instructor_rename_description_line")
        self.instructor_rename_staff_id_combo_box = QtWidgets.QComboBox(self.frame_4)
        self.instructor_rename_staff_id_combo_box.setGeometry(QtCore.QRect(10, 14, 215, 25))
        self.instructor_rename_staff_id_combo_box.setObjectName("instructor_rename_staff_id_combo_box")
        for i in range(len(staff_dict)):
            self.instructor_rename_staff_id_combo_box.addItem("")
        self.instructor_rename_teaching_object_line = QtWidgets.QLineEdit(self.frame_4)
        self.instructor_rename_teaching_object_line.setGeometry(QtCore.QRect(10, 84, 215, 25))
        self.instructor_rename_teaching_object_line.setObjectName("instructor_rename_teaching_object_line")
        self.instructor_rename_id_combo_box = QtWidgets.QComboBox(self.frame_4)
        self.instructor_rename_id_combo_box.setGeometry(QtCore.QRect(10, 126, 215, 25))
        self.instructor_rename_id_combo_box.setObjectName("instructor_rename_id_combo_box")
        for i in range(len(instructor_dict)):
            self.instructor_rename_id_combo_box.addItem("")
        self.frame_2 = QtWidgets.QFrame(Instructor_Replace_Window)
        self.frame_2.setGeometry(QtCore.QRect(5, 180, 390, 30))
        self.frame_2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.pushButton = QtWidgets.QPushButton(self.frame_2)
        self.pushButton.setGeometry(QtCore.QRect(160, 3, 70, 25))
        font = QtGui.QFont()
        font.setBold(True)
        font.setUnderline(True)
        font.setWeight(75)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")

        self.retranslateUi(Instructor_Replace_Window)
        QtCore.QMetaObject.connectSlotsByName(Instructor_Replace_Window)

    def updateCombo(self, index):
        self.instructor_rename_staff_id_combo_box.setCurrentIndex(index)
        self.instructor_rename_description_line.setText(str(INSTRUCTOR.Description[index]))
        self.instructor_rename_teaching_object_line.setText(str(INSTRUCTOR.Teaching_Object[index]))

    def retranslateUi(self, Instructor_Replace_Window):
        _translate = QtCore.QCoreApplication.translate
        Instructor_Replace_Window.setWindowTitle(_translate("Instructor_Replace_Window", "Update"))
        self.instructor_rename_description_txt.setText(_translate("Instructor_Replace_Window", "Description"))
        self.instructor_rename_staff_id_label.setText(_translate("Instructor_Replace_Window", "Staff"))
        self.instructor_rename_teaching_object_txt.setText(_translate("Instructor_Replace_Window", "Teaching Object"))
        self.instructor_rename_id_label.setText(_translate("Instructor_Replace_Window", "ID"))
        self.instructor_rename_description_line.setText(str(INSTRUCTOR.Description[0]))
        self.instructor_rename_teaching_object_line.setText(str(INSTRUCTOR.Teaching_Object[0]))
        for key, value in staff_dict.items():
            self.instructor_rename_staff_id_combo_box.setItemText(value-1, _translate("Instructor_Replace_Window", key))
        for i in range(len(instructor_dict)):
            self.instructor_rename_id_combo_box.setItemText(i, _translate("Instructor_Replace_Window", str(i+1)))
        self.pushButton.setText(_translate("Instructor_Replace_Window", "OK"))
        self.instructor_rename_id_combo_box.currentIndexChanged.connect(self.updateCombo)
class Ui_Schedule_Enter_Window(object):
    def setupUi(self, Schedule_Enter_Window):
        Schedule_Enter_Window.setObjectName("Schedule_Enter_Window")
        Schedule_Enter_Window.resize(400, 355)
        Schedule_Enter_Window.setMinimumSize(QtCore.QSize(400, 355))
        Schedule_Enter_Window.setMaximumSize(QtCore.QSize(400, 355))
        self.frame = QtWidgets.QFrame(Schedule_Enter_Window)
        self.frame.setGeometry(QtCore.QRect(5, 5, 390, 310))
        self.frame.setFrameShape(QtWidgets.QFrame.Panel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.frame_3 = QtWidgets.QFrame(self.frame)
        self.frame_3.setGeometry(QtCore.QRect(5, 5, 140, 300))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_3.sizePolicy().hasHeightForWidth())
        self.frame_3.setSizePolicy(sizePolicy)
        self.frame_3.setMinimumSize(QtCore.QSize(140, 300))
        self.frame_3.setMaximumSize(QtCore.QSize(140, 300))
        self.frame_3.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.frame_3)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.frame_3)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.label_3 = QtWidgets.QLabel(self.frame_3)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.verticalLayout.addWidget(self.label_3)
        self.label_2 = QtWidgets.QLabel(self.frame_3)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.label_4 = QtWidgets.QLabel(self.frame_3)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.verticalLayout.addWidget(self.label_4)
        self.label_5 = QtWidgets.QLabel(self.frame_3)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.verticalLayout.addWidget(self.label_5)
        self.label_6 = QtWidgets.QLabel(self.frame_3)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.verticalLayout.addWidget(self.label_6)
        self.label_7 = QtWidgets.QLabel(self.frame_3)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        self.verticalLayout.addWidget(self.label_7)
        self.label_8 = QtWidgets.QLabel(self.frame_3)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_8.setFont(font)
        self.label_8.setObjectName("label_8")
        self.verticalLayout.addWidget(self.label_8)
        self.frame_4 = QtWidgets.QFrame(self.frame)
        self.frame_4.setGeometry(QtCore.QRect(150, 5, 235, 300))
        self.frame_4.setMinimumSize(QtCore.QSize(235, 300))
        self.frame_4.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_4.setObjectName("frame_4")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.frame_4)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.schedule_group_enter_comboBox = QtWidgets.QComboBox(self.frame_4)
        self.schedule_group_enter_comboBox.setObjectName("schedule_group_enter_comboBox")
        for i in range(len(group_dict)):
            self.schedule_group_enter_comboBox.addItem("")
        self.verticalLayout_2.addWidget(self.schedule_group_enter_comboBox)
        self.schedule_instructor_enter_comboBox = QtWidgets.QComboBox(self.frame_4)
        self.schedule_instructor_enter_comboBox.setObjectName("schedule_instructor_enter_comboBox")
        for i in range(len(staff_dict)):
            self.schedule_instructor_enter_comboBox.addItem("")
        self.verticalLayout_2.addWidget(self.schedule_instructor_enter_comboBox)
        self.schedule_subject_enter_comboBox = QtWidgets.QComboBox(self.frame_4)
        self.schedule_subject_enter_comboBox.setObjectName("schedule_subject_enter_comboBox")
        for i in range(len(subject_dict)):
            self.schedule_subject_enter_comboBox.addItem("")
        self.verticalLayout_2.addWidget(self.schedule_subject_enter_comboBox)
        self.schedule_audience_enter_comboBox = QtWidgets.QComboBox(self.frame_4)
        self.schedule_audience_enter_comboBox.setObjectName("schedule_audience_enter_comboBox")
        for i in range(len(audience_dict)):
            self.schedule_audience_enter_comboBox.addItem("")
        self.verticalLayout_2.addWidget(self.schedule_audience_enter_comboBox)
        self.schedule_learningtype_enter_comboBox = QtWidgets.QComboBox(self.frame_4)
        self.schedule_learningtype_enter_comboBox.setObjectName("schedule_learningtype_enter_comboBox")
        for i in range(len(lType_dict)):
            self.schedule_learningtype_enter_comboBox.addItem("")
        self.verticalLayout_2.addWidget(self.schedule_learningtype_enter_comboBox)
        self.schedule_startdate_enter_lineEdit = QtWidgets.QLineEdit(self.frame_4)
        self.schedule_startdate_enter_lineEdit.setObjectName("schedule_startdate_enter_lineEdit")
        self.verticalLayout_2.addWidget(self.schedule_startdate_enter_lineEdit)
        self.schedule_finishdate_enter_lineEdit = QtWidgets.QLineEdit(self.frame_4)
        self.schedule_finishdate_enter_lineEdit.setObjectName("schedule_finishdate_enter_lineEdit")
        self.verticalLayout_2.addWidget(self.schedule_finishdate_enter_lineEdit)
        self.schedule_timeschedule_enter_lineEdit = QtWidgets.QLineEdit(self.frame_4)
        self.schedule_timeschedule_enter_lineEdit.setObjectName("schedule_timeschedule_enter_lineEdit")
        self.verticalLayout_2.addWidget(self.schedule_timeschedule_enter_lineEdit)
        self.frame_2 = QtWidgets.QFrame(Schedule_Enter_Window)
        self.frame_2.setEnabled(True)
        self.frame_2.setGeometry(QtCore.QRect(5, 320, 390, 30))
        self.frame_2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.Schedule_Enter_pushButton = QtWidgets.QPushButton(self.frame_2)
        self.Schedule_Enter_pushButton.setGeometry(QtCore.QRect(160, 3, 70, 25))
        font = QtGui.QFont()
        font.setBold(True)
        font.setItalic(False)
        font.setUnderline(True)
        font.setWeight(75)
        self.Schedule_Enter_pushButton.setFont(font)
        self.Schedule_Enter_pushButton.setObjectName("Schedule_Enter_pushButton")

        self.retranslateUi(Schedule_Enter_Window)
        QtCore.QMetaObject.connectSlotsByName(Schedule_Enter_Window)

    def retranslateUi(self, Schedule_Enter_Window):
        _translate = QtCore.QCoreApplication.translate
        Schedule_Enter_Window.setWindowTitle(_translate("Schedule_Enter_Window", "Enter"))
        self.label.setText(_translate("Schedule_Enter_Window", "Group "))
        self.label_3.setText(_translate("Schedule_Enter_Window", "Instructor "))
        self.label_2.setText(_translate("Schedule_Enter_Window", "Subject "))
        self.label_4.setText(_translate("Schedule_Enter_Window", "Audience "))
        self.label_5.setText(_translate("Schedule_Enter_Window", "Learning Type "))
        self.label_6.setText(_translate("Schedule_Enter_Window", "Start Date"))
        self.label_7.setText(_translate("Schedule_Enter_Window", "Finish Date"))
        self.label_8.setText(_translate("Schedule_Enter_Window", "Time Schedule"))

        for key,value in group_dict.items():
            self.schedule_group_enter_comboBox.setItemText(value-1, _translate("Schedule_Enter_Window", key))
        for key,value in staff_dict.items():
            self.schedule_instructor_enter_comboBox.setItemText(value-1, _translate("Schedule_Enter_Window", key))
        for key,value in subject_dict.items():
            self.schedule_subject_enter_comboBox.setItemText(value-1, _translate("Schedule_Enter_Window", key))
        for key in audience_dict.keys():
            self.schedule_audience_enter_comboBox.setItemText(list(audience_dict.keys()).index(key), _translate("Audience_Replace_Window", key))
        for key,value in lType_dict.items():
            self.schedule_learningtype_enter_comboBox.setItemText(value-1, _translate("Schedule_Enter_Window", key))
        self.Schedule_Enter_pushButton.setText(_translate("Schedule_Enter_Window", "OK"))
class Ui_Schedule_Replace_Window(object):
    def setupUi(self, Schedule_Replace_Window):
        Schedule_Replace_Window.setObjectName("Schedule_Replace_Window")
        Schedule_Replace_Window.resize(400, 355)
        Schedule_Replace_Window.setMinimumSize(QtCore.QSize(400, 355))
        Schedule_Replace_Window.setMaximumSize(QtCore.QSize(400, 355))
        self.frame = QtWidgets.QFrame(Schedule_Replace_Window)
        self.frame.setGeometry(QtCore.QRect(5, 5, 390, 310))
        self.frame.setFrameShape(QtWidgets.QFrame.Panel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.frame_3 = QtWidgets.QFrame(self.frame)
        self.frame_3.setGeometry(QtCore.QRect(5, 5, 140, 300))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_3.sizePolicy().hasHeightForWidth())
        self.frame_3.setSizePolicy(sizePolicy)
        self.frame_3.setMinimumSize(QtCore.QSize(140, 300))
        self.frame_3.setMaximumSize(QtCore.QSize(140, 300))
        self.frame_3.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.frame_3)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.frame_3)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.label_3 = QtWidgets.QLabel(self.frame_3)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.verticalLayout.addWidget(self.label_3)
        self.label_2 = QtWidgets.QLabel(self.frame_3)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.label_4 = QtWidgets.QLabel(self.frame_3)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.verticalLayout.addWidget(self.label_4)
        self.label_5 = QtWidgets.QLabel(self.frame_3)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.verticalLayout.addWidget(self.label_5)
        self.label_6 = QtWidgets.QLabel(self.frame_3)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.verticalLayout.addWidget(self.label_6)
        self.label_7 = QtWidgets.QLabel(self.frame_3)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        self.verticalLayout.addWidget(self.label_7)
        self.label_8 = QtWidgets.QLabel(self.frame_3)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_8.setFont(font)
        self.label_8.setObjectName("label_8")
        self.verticalLayout.addWidget(self.label_8)
        self.label_9 = QtWidgets.QLabel(self.frame_3)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_9.setFont(font)
        self.label_9.setObjectName("label_9")
        self.label_9.setStyleSheet("color: red")
        self.verticalLayout.addWidget(self.label_9)
        self.frame_4 = QtWidgets.QFrame(self.frame)
        self.frame_4.setGeometry(QtCore.QRect(150, 5, 235, 301))
        self.frame_4.setMinimumSize(QtCore.QSize(235, 300))
        self.frame_4.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_4.setObjectName("frame_4")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.frame_4)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.schedule_group_replace_comboBox = QtWidgets.QComboBox(self.frame_4)
        self.schedule_group_replace_comboBox.setObjectName("schedule_group_replace_comboBox")
        for i in range(len(group_dict)):
            self.schedule_group_replace_comboBox.addItem("")
        self.verticalLayout_2.addWidget(self.schedule_group_replace_comboBox)
        self.schedule_instructor_replace_comboBox = QtWidgets.QComboBox(self.frame_4)
        self.schedule_instructor_replace_comboBox.setObjectName("schedule_instructor_replace_comboBox")
        for i in range(len(instructor_dict)):
            self.schedule_instructor_replace_comboBox.addItem("")
        self.verticalLayout_2.addWidget(self.schedule_instructor_replace_comboBox)
        self.schedule_subject_replace_comboBox = QtWidgets.QComboBox(self.frame_4)
        self.schedule_subject_replace_comboBox.setObjectName("schedule_subject_replace_comboBox")
        for i in range(len(subject_dict)):
            self.schedule_subject_replace_comboBox.addItem("")
        self.verticalLayout_2.addWidget(self.schedule_subject_replace_comboBox)
        self.schedule_audience_replace_comboBox = QtWidgets.QComboBox(self.frame_4)
        self.schedule_audience_replace_comboBox.setObjectName("schedule_audience_replace_comboBox")
        for i in range(len(audience_dict)):
            self.schedule_audience_replace_comboBox.addItem("")
        self.verticalLayout_2.addWidget(self.schedule_audience_replace_comboBox)
        self.schedule_learningtype_replace_comboBox = QtWidgets.QComboBox(self.frame_4)
        self.schedule_learningtype_replace_comboBox.setObjectName("schedule_learningtype_replace_comboBox")
        for i in range(len(lType_dict)):
            self.schedule_learningtype_replace_comboBox.addItem("")
        self.verticalLayout_2.addWidget(self.schedule_learningtype_replace_comboBox)
        self.schedule_startdate_replace_lineEdit = QtWidgets.QLineEdit(self.frame_4)
        self.schedule_startdate_replace_lineEdit.setObjectName("schedule_startdate_replace_lineEdit")
        self.verticalLayout_2.addWidget(self.schedule_startdate_replace_lineEdit)
        self.schedule_finishdate_replace_lineEdit = QtWidgets.QLineEdit(self.frame_4)
        self.schedule_finishdate_replace_lineEdit.setObjectName("schedule_finishdate_replace_lineEdit")
        self.verticalLayout_2.addWidget(self.schedule_finishdate_replace_lineEdit)
        self.schedule_timeschedule_replace_lineEdit = QtWidgets.QLineEdit(self.frame_4)
        self.schedule_timeschedule_replace_lineEdit.setObjectName("schedule_timeschedule_replace_lineEdit")
        self.verticalLayout_2.addWidget(self.schedule_timeschedule_replace_lineEdit)
        self.schedule_learningtype_replace_comboBox_2 = QtWidgets.QComboBox(self.frame_4)
        self.schedule_learningtype_replace_comboBox_2.setObjectName("schedule_learningtype_replace_comboBox_2")
        for i in range(len(SCHEDULE)):
            self.schedule_learningtype_replace_comboBox_2.addItem("")
        self.verticalLayout_2.addWidget(self.schedule_learningtype_replace_comboBox_2)
        self.frame_2 = QtWidgets.QFrame(Schedule_Replace_Window)
        self.frame_2.setEnabled(True)
        self.frame_2.setGeometry(QtCore.QRect(5, 320, 390, 30))
        self.frame_2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.Schedule_Replace_pushButton = QtWidgets.QPushButton(self.frame_2)
        self.Schedule_Replace_pushButton.setGeometry(QtCore.QRect(160, 3, 70, 25))
        font = QtGui.QFont()
        font.setBold(True)
        font.setItalic(False)
        font.setUnderline(True)
        font.setWeight(75)
        self.Schedule_Replace_pushButton.setFont(font)
        self.Schedule_Replace_pushButton.setObjectName("Schedule_Replace_pushButton")

        self.retranslateUi(Schedule_Replace_Window)
        QtCore.QMetaObject.connectSlotsByName(Schedule_Replace_Window)

    def updateCombo(self, index):
        self.schedule_group_replace_comboBox.setCurrentIndex(index)
        self.schedule_instructor_replace_comboBox.setCurrentIndex(index)
        self.schedule_subject_replace_comboBox.setCurrentIndex(index)
        self.schedule_audience_replace_comboBox.setCurrentIndex(index)
        self.schedule_learningtype_replace_comboBox.setCurrentText(str(lType_ID_dict[SCHEDULE.Learning_Type_ID[index]]))
        self.schedule_startdate_replace_lineEdit.setText(str(SCHEDULE.Start_Date[index]))
        self.schedule_finishdate_replace_lineEdit.setText(str(SCHEDULE.Finish_Date[index]))
        self.schedule_timeschedule_replace_lineEdit.setText(str(SCHEDULE.Time_Schedule[index]))

    def retranslateUi(self, Schedule_Replace_Window):
        _translate = QtCore.QCoreApplication.translate
        Schedule_Replace_Window.setWindowTitle(_translate("Schedule_Replace_Window", "Update"))
        self.label.setText(_translate("Schedule_Replace_Window", "Group "))
        self.label_3.setText(_translate("Schedule_Replace_Window", "Instructor "))
        self.label_2.setText(_translate("Schedule_Replace_Window", "Subject "))
        self.label_4.setText(_translate("Schedule_Replace_Window", "Audience "))
        self.label_5.setText(_translate("Schedule_Replace_Window", "Learning Type "))
        self.label_6.setText(_translate("Schedule_Replace_Window", "Start Date"))
        self.label_7.setText(_translate("Schedule_Replace_Window", "Finish Date"))
        self.label_8.setText(_translate("Schedule_Replace_Window", "Time Schedule"))
        self.label_9.setText(_translate("Schedule_Replace_Window", "ID"))
        self.schedule_startdate_replace_lineEdit.setText(str(SCHEDULE.Start_Date[0]))
        self.schedule_finishdate_replace_lineEdit.setText(str(SCHEDULE.Finish_Date[0]))
        self.schedule_timeschedule_replace_lineEdit.setText(str(SCHEDULE.Time_Schedule[0]))
        for key,value in group_dict.items():
            self.schedule_group_replace_comboBox.setItemText(value-1, _translate("Schedule_Enter_Window", key))
        for key,value in staff_dict.items():
            self.schedule_instructor_replace_comboBox.setItemText(value-1, _translate("Schedule_Enter_Window", key))
        for key,value in subject_dict.items():
            self.schedule_subject_replace_comboBox.setItemText(value-1, _translate("Schedule_Enter_Window", key))
        for key in audience_dict.keys():
            self.schedule_audience_replace_comboBox.setItemText(list(audience_dict.keys()).index(key), _translate("Schedule_Enter_Window", key))
        for key,value in lType_dict.items():
            self.schedule_learningtype_replace_comboBox.setItemText(value-1, _translate("Schedule_Enter_Window", key))
        for i in range(len(SCHEDULE)):
            self.schedule_learningtype_replace_comboBox_2.setItemText(i, _translate("Schedule_Enter_Window", str(i+1)))
        self.Schedule_Replace_pushButton.setText(_translate("Schedule_Replace_Window", "OK"))
        self.schedule_learningtype_replace_comboBox_2.currentIndexChanged.connect(self.updateCombo)
class Ui_Staff_Enter_Window(object):
    def setupUi(self, Staff_Enter_Window):
        Staff_Enter_Window.setObjectName("Staff_Enter_Window")
        Staff_Enter_Window.resize(400, 355)
        Staff_Enter_Window.setMinimumSize(QtCore.QSize(400, 355))
        Staff_Enter_Window.setMaximumSize(QtCore.QSize(400, 355))
        self.frame = QtWidgets.QFrame(Staff_Enter_Window)
        self.frame.setGeometry(QtCore.QRect(5, 5, 390, 310))
        self.frame.setFrameShape(QtWidgets.QFrame.Panel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.frame_3 = QtWidgets.QFrame(self.frame)
        self.frame_3.setGeometry(QtCore.QRect(5, 5, 140, 300))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_3.sizePolicy().hasHeightForWidth())
        self.frame_3.setSizePolicy(sizePolicy)
        self.frame_3.setMinimumSize(QtCore.QSize(140, 300))
        self.frame_3.setMaximumSize(QtCore.QSize(140, 300))
        self.frame_3.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.frame_3)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.frame_3)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.label_3 = QtWidgets.QLabel(self.frame_3)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.verticalLayout.addWidget(self.label_3)
        self.label_2 = QtWidgets.QLabel(self.frame_3)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.label_4 = QtWidgets.QLabel(self.frame_3)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.verticalLayout.addWidget(self.label_4)
        self.label_9 = QtWidgets.QLabel(self.frame_3)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_9.setFont(font)
        self.label_9.setObjectName("label_9")
        self.verticalLayout.addWidget(self.label_9)
        self.label_6 = QtWidgets.QLabel(self.frame_3)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.verticalLayout.addWidget(self.label_6)
        self.label_7 = QtWidgets.QLabel(self.frame_3)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        self.verticalLayout.addWidget(self.label_7)
        self.label_8 = QtWidgets.QLabel(self.frame_3)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_8.setFont(font)
        self.label_8.setObjectName("label_8")
        self.verticalLayout.addWidget(self.label_8)
        self.frame_4 = QtWidgets.QFrame(self.frame)
        self.frame_4.setGeometry(QtCore.QRect(150, 5, 235, 311))
        self.frame_4.setMinimumSize(QtCore.QSize(235, 300))
        self.frame_4.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_4.setObjectName("frame_4")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.frame_4)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.staff_name_enter_lineEdit = QtWidgets.QLineEdit(self.frame_4)
        self.staff_name_enter_lineEdit.setObjectName("staff_name_enter_lineEdit")
        self.verticalLayout_2.addWidget(self.staff_name_enter_lineEdit)
        self.staff_lastname_enter_lineEdit = QtWidgets.QLineEdit(self.frame_4)
        self.staff_lastname_enter_lineEdit.setObjectName("staff_lastname_enter_lineEdit")
        self.verticalLayout_2.addWidget(self.staff_lastname_enter_lineEdit)
        self.staff_patronymic_enter_lineEdit = QtWidgets.QLineEdit(self.frame_4)
        self.staff_patronymic_enter_lineEdit.setObjectName("staff_patronymic_enter_lineEdit")
        self.verticalLayout_2.addWidget(self.staff_patronymic_enter_lineEdit)
        self.staff_education_enter_lineEdit = QtWidgets.QLineEdit(self.frame_4)
        self.staff_education_enter_lineEdit.setObjectName("staff_education_enter_lineEdit")
        self.verticalLayout_2.addWidget(self.staff_education_enter_lineEdit)
        self.staff_address_enter_lineEdit = QtWidgets.QLineEdit(self.frame_4)
        self.staff_address_enter_lineEdit.setObjectName("staff_address_enter_lineEdit")
        self.verticalLayout_2.addWidget(self.staff_address_enter_lineEdit)
        self.staff_phonenumber_enter_lineEdit = QtWidgets.QLineEdit(self.frame_4)
        self.staff_phonenumber_enter_lineEdit.setObjectName("staff_phonenumber_enter_lineEdit")
        self.verticalLayout_2.addWidget(self.staff_phonenumber_enter_lineEdit)
        self.staff_email_enter_lineEdit = QtWidgets.QLineEdit(self.frame_4)
        self.staff_email_enter_lineEdit.setObjectName("staff_email_enter_lineEdit")
        self.verticalLayout_2.addWidget(self.staff_email_enter_lineEdit)
        self.staff_position_enter_comboBox = QtWidgets.QComboBox(self.frame_4)
        self.staff_position_enter_comboBox.setObjectName("staff_position_enter_comboBox")
        for i in range(len(position_dict)):
            self.staff_position_enter_comboBox.addItem("")
        self.verticalLayout_2.addWidget(self.staff_position_enter_comboBox)
        self.frame_2 = QtWidgets.QFrame(Staff_Enter_Window)
        self.frame_2.setEnabled(True)
        self.frame_2.setGeometry(QtCore.QRect(5, 320, 390, 30))
        self.frame_2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.Staff_Enter_pushButton = QtWidgets.QPushButton(self.frame_2)
        self.Staff_Enter_pushButton.setGeometry(QtCore.QRect(160, 3, 70, 25))
        font = QtGui.QFont()
        font.setBold(True)
        font.setItalic(False)
        font.setUnderline(True)
        font.setWeight(75)
        self.Staff_Enter_pushButton.setFont(font)
        self.Staff_Enter_pushButton.setObjectName("Staff_Enter_pushButton")

        self.retranslateUi(Staff_Enter_Window)
        QtCore.QMetaObject.connectSlotsByName(Staff_Enter_Window)

    def retranslateUi(self, Staff_Enter_Window):
        _translate = QtCore.QCoreApplication.translate
        Staff_Enter_Window.setWindowTitle(_translate("Staff_Enter_Window", "Enter"))
        self.label.setText(_translate("Staff_Enter_Window", "Name"))
        self.label_3.setText(_translate("Staff_Enter_Window", "Last Name"))
        self.label_2.setText(_translate("Staff_Enter_Window", "Patronymic"))
        self.label_4.setText(_translate("Staff_Enter_Window", "Education"))
        self.label_9.setText(_translate("Staff_Enter_Window", "Address"))
        self.label_6.setText(_translate("Staff_Enter_Window", "Phone Number"))
        self.label_7.setText(_translate("Staff_Enter_Window", "Email"))
        self.label_8.setText(_translate("Staff_Enter_Window", "Position "))
        for key,value in position_dict.items():
            self.staff_position_enter_comboBox.setItemText(value-1, _translate("Staff_Enter_Window", key))
        self.Staff_Enter_pushButton.setText(_translate("Staff_Enter_Window", "OK"))
class Ui_Staff_Replace_Window(object):
    def setupUi(self, Staff_Replace_Window):
        Staff_Replace_Window.setObjectName("Staff_Replace_Window")
        Staff_Replace_Window.resize(400, 355)
        Staff_Replace_Window.setMinimumSize(QtCore.QSize(400, 355))
        Staff_Replace_Window.setMaximumSize(QtCore.QSize(400, 355))
        self.frame = QtWidgets.QFrame(Staff_Replace_Window)
        self.frame.setGeometry(QtCore.QRect(5, 5, 390, 310))
        self.frame.setFrameShape(QtWidgets.QFrame.Panel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.frame_3 = QtWidgets.QFrame(self.frame)
        self.frame_3.setGeometry(QtCore.QRect(10, 10, 140, 300))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_3.sizePolicy().hasHeightForWidth())
        self.frame_3.setSizePolicy(sizePolicy)
        self.frame_3.setMinimumSize(QtCore.QSize(140, 300))
        self.frame_3.setMaximumSize(QtCore.QSize(140, 300))
        self.frame_3.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.frame_3)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.frame_3)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.label_3 = QtWidgets.QLabel(self.frame_3)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.verticalLayout.addWidget(self.label_3)
        self.label_2 = QtWidgets.QLabel(self.frame_3)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.label_4 = QtWidgets.QLabel(self.frame_3)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.verticalLayout.addWidget(self.label_4)
        self.label_9 = QtWidgets.QLabel(self.frame_3)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_9.setFont(font)
        self.label_9.setObjectName("label_9")
        self.verticalLayout.addWidget(self.label_9)
        self.label_6 = QtWidgets.QLabel(self.frame_3)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.verticalLayout.addWidget(self.label_6)
        self.label_7 = QtWidgets.QLabel(self.frame_3)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        self.verticalLayout.addWidget(self.label_7)
        self.label_8 = QtWidgets.QLabel(self.frame_3)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_8.setFont(font)
        self.label_8.setObjectName("label_8")
        self.verticalLayout.addWidget(self.label_8)
        self.label_10 = QtWidgets.QLabel(self.frame_3)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_10.setFont(font)
        self.label_10.setObjectName("label_10")
        self.label_10.setStyleSheet("color: red")
        self.verticalLayout.addWidget(self.label_10)
        self.frame_4 = QtWidgets.QFrame(self.frame)
        self.frame_4.setGeometry(QtCore.QRect(150, 10, 235, 301))
        self.frame_4.setMinimumSize(QtCore.QSize(235, 300))
        self.frame_4.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_4.setObjectName("frame_4")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.frame_4)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.staff_name_replace_lineEdit = QtWidgets.QLineEdit(self.frame_4)
        self.staff_name_replace_lineEdit.setObjectName("staff_name_replace_lineEdit")
        self.verticalLayout_2.addWidget(self.staff_name_replace_lineEdit)
        self.staff_lastname_replace_lineEdit = QtWidgets.QLineEdit(self.frame_4)
        self.staff_lastname_replace_lineEdit.setObjectName("staff_lastname_replace_lineEdit")
        self.verticalLayout_2.addWidget(self.staff_lastname_replace_lineEdit)
        self.staff_patronymic_replace_lineEdit = QtWidgets.QLineEdit(self.frame_4)
        self.staff_patronymic_replace_lineEdit.setObjectName("staff_patronymic_replace_lineEdit")
        self.verticalLayout_2.addWidget(self.staff_patronymic_replace_lineEdit)
        self.staff_education_replace_lineEdit = QtWidgets.QLineEdit(self.frame_4)
        self.staff_education_replace_lineEdit.setObjectName("staff_education_replace_lineEdit")
        self.verticalLayout_2.addWidget(self.staff_education_replace_lineEdit)
        self.staff_address_replace_lineEdit = QtWidgets.QLineEdit(self.frame_4)
        self.staff_address_replace_lineEdit.setObjectName("staff_address_replace_lineEdit")
        self.verticalLayout_2.addWidget(self.staff_address_replace_lineEdit)
        self.staff_phonenumber_replace_lineEdit = QtWidgets.QLineEdit(self.frame_4)
        self.staff_phonenumber_replace_lineEdit.setObjectName("staff_phonenumber_replace_lineEdit")
        self.verticalLayout_2.addWidget(self.staff_phonenumber_replace_lineEdit)
        self.staff_email_replace_lineEdit = QtWidgets.QLineEdit(self.frame_4)
        self.staff_email_replace_lineEdit.setObjectName("staff_email_replace_lineEdit")
        self.verticalLayout_2.addWidget(self.staff_email_replace_lineEdit)
        self.staff_position_replace_comboBox = QtWidgets.QComboBox(self.frame_4)
        self.staff_position_replace_comboBox.setObjectName("staff_position_replace_comboBox")
        for i in range(len(position_dict)):
            self.staff_position_replace_comboBox.addItem("")
        self.verticalLayout_2.addWidget(self.staff_position_replace_comboBox)
        self.staff_id_replace_comboBox = QtWidgets.QComboBox(self.frame_4)
        self.staff_id_replace_comboBox.setObjectName("staff_id_replace_comboBox")
        for i in range(len(staff_dict)):
            self.staff_id_replace_comboBox.addItem("")
        self.verticalLayout_2.addWidget(self.staff_id_replace_comboBox)
        self.frame_2 = QtWidgets.QFrame(Staff_Replace_Window)
        self.frame_2.setEnabled(True)
        self.frame_2.setGeometry(QtCore.QRect(5, 320, 390, 30))
        self.frame_2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.Staff_Replace_pushButton = QtWidgets.QPushButton(self.frame_2)
        self.Staff_Replace_pushButton.setGeometry(QtCore.QRect(160, 3, 70, 25))
        font = QtGui.QFont()
        font.setBold(True)
        font.setItalic(False)
        font.setUnderline(True)
        font.setWeight(75)
        self.Staff_Replace_pushButton.setFont(font)
        self.Staff_Replace_pushButton.setObjectName("Staff_Replace_pushButton")

        self.retranslateUi(Staff_Replace_Window)
        QtCore.QMetaObject.connectSlotsByName(Staff_Replace_Window)

    def updateCombo(self, index):
        self.staff_name_replace_lineEdit.setText(str(STAFF.Name[index]))
        self.staff_lastname_replace_lineEdit.setText(str(STAFF.Last_Name[index]))
        self.staff_patronymic_replace_lineEdit.setText(str(STAFF.Patronymic[index]))
        self.staff_education_replace_lineEdit.setText(str(STAFF.Education[index]))
        self.staff_address_replace_lineEdit.setText(str(STAFF.Address[index]))
        self.staff_phonenumber_replace_lineEdit.setText(str(STAFF.Phone_Number[index]))
        self.staff_email_replace_lineEdit.setText(str(STAFF.Email[index]))
        self.staff_position_replace_comboBox.setCurrentIndex(index)

    def retranslateUi(self, Staff_Replace_Window):
        _translate = QtCore.QCoreApplication.translate
        Staff_Replace_Window.setWindowTitle(_translate("Staff_Replace_Window", "Update"))
        self.label.setText(_translate("Staff_Replace_Window", "Name"))
        self.label_3.setText(_translate("Staff_Replace_Window", "Last Name"))
        self.label_2.setText(_translate("Staff_Replace_Window", "Patronymic"))
        self.label_4.setText(_translate("Staff_Replace_Window", "Education"))
        self.label_9.setText(_translate("Staff_Replace_Window", "Address"))
        self.label_6.setText(_translate("Staff_Replace_Window", "Phone Number"))
        self.label_7.setText(_translate("Staff_Replace_Window", "Email"))
        self.label_8.setText(_translate("Staff_Replace_Window", "Position "))
        self.label_10.setText(_translate("Staff_Replace_Window", "ID"))
        self.staff_name_replace_lineEdit.setText(str(STAFF.Name[0]))
        self.staff_lastname_replace_lineEdit.setText(str(STAFF.Last_Name[0]))
        self.staff_patronymic_replace_lineEdit.setText(str(STAFF.Patronymic[0]))
        self.staff_education_replace_lineEdit.setText(str(STAFF.Education[0]))
        self.staff_address_replace_lineEdit.setText(str(STAFF.Address[0]))
        self.staff_phonenumber_replace_lineEdit.setText(str(STAFF.Phone_Number[0]))
        self.staff_email_replace_lineEdit.setText(str(STAFF.Email[0]))
        for key,value in position_dict.items():
            self.staff_position_replace_comboBox.setItemText(value-1, _translate("Staff_Replace_Window", key))
        for i in range(len(staff_dict)):
            self.staff_id_replace_comboBox.setItemText(i, _translate("Staff_Replace_Window", str(i+1)))
        self.Staff_Replace_pushButton.setText(_translate("Staff_Replace_Window", "OK"))
        self.staff_id_replace_comboBox.currentIndexChanged.connect(self.updateCombo)
class Ui_Student_Enter_window(object):
    def setupUi(self, Student_Enter_window):
        Student_Enter_window.setObjectName("Student_Enter_window")
        Student_Enter_window.resize(400, 354)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Student_Enter_window.sizePolicy().hasHeightForWidth())
        Student_Enter_window.setSizePolicy(sizePolicy)
        Student_Enter_window.setMinimumSize(QtCore.QSize(400, 354))
        Student_Enter_window.setMaximumSize(QtCore.QSize(400, 354))
        self.frame = QtWidgets.QFrame(Student_Enter_window)
        self.frame.setGeometry(QtCore.QRect(5, 5, 390, 310))
        self.frame.setFrameShape(QtWidgets.QFrame.Panel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.frame_3 = QtWidgets.QFrame(self.frame)
        self.frame_3.setGeometry(QtCore.QRect(5, 5, 140, 300))
        self.frame_3.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.frame_3)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_8 = QtWidgets.QLabel(self.frame_3)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_8.setFont(font)
        self.label_8.setObjectName("label_8")
        self.verticalLayout.addWidget(self.label_8)
        self.label = QtWidgets.QLabel(self.frame_3)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.label_3 = QtWidgets.QLabel(self.frame_3)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.verticalLayout.addWidget(self.label_3)
        self.label_2 = QtWidgets.QLabel(self.frame_3)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.label_5 = QtWidgets.QLabel(self.frame_3)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.verticalLayout.addWidget(self.label_5)
        self.label_4 = QtWidgets.QLabel(self.frame_3)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.verticalLayout.addWidget(self.label_4)
        self.label_6 = QtWidgets.QLabel(self.frame_3)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.verticalLayout.addWidget(self.label_6)
        self.label_7 = QtWidgets.QLabel(self.frame_3)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        self.verticalLayout.addWidget(self.label_7)
        self.frame_4 = QtWidgets.QFrame(self.frame)
        self.frame_4.setGeometry(QtCore.QRect(150, 5, 235, 300))
        self.frame_4.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_4.setObjectName("frame_4")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.frame_4)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.student_enter_name_lineEdit = QtWidgets.QLineEdit(self.frame_4)
        self.student_enter_name_lineEdit.setObjectName("student_enter_name_lineEdit")
        self.verticalLayout_2.addWidget(self.student_enter_name_lineEdit)
        self.student_enter_LName_lineEdit = QtWidgets.QLineEdit(self.frame_4)
        self.student_enter_LName_lineEdit.setObjectName("student_enter_LName_lineEdit")
        self.verticalLayout_2.addWidget(self.student_enter_LName_lineEdit)
        self.student_enter_patro_lineEdit = QtWidgets.QLineEdit(self.frame_4)
        self.student_enter_patro_lineEdit.setObjectName("student_enter_patro_lineEdit")
        self.verticalLayout_2.addWidget(self.student_enter_patro_lineEdit)
        self.student_enter_BDate_lineEdit = QtWidgets.QLineEdit(self.frame_4)
        self.student_enter_BDate_lineEdit.setObjectName("student_enter_BDate_lineEdit")
        self.verticalLayout_2.addWidget(self.student_enter_BDate_lineEdit)
        self.student_enter_address_lineEdit = QtWidgets.QLineEdit(self.frame_4)
        self.student_enter_address_lineEdit.setObjectName("student_enter_address_lineEdit")
        self.verticalLayout_2.addWidget(self.student_enter_address_lineEdit)
        self.student_enter_PNumber_lineEdit = QtWidgets.QLineEdit(self.frame_4)
        self.student_enter_PNumber_lineEdit.setObjectName("student_enter_PNumber_lineEdit")
        self.verticalLayout_2.addWidget(self.student_enter_PNumber_lineEdit)
        self.student_enter_email_lineEdit = QtWidgets.QLineEdit(self.frame_4)
        self.student_enter_email_lineEdit.setObjectName("student_enter_email_lineEdit")
        self.verticalLayout_2.addWidget(self.student_enter_email_lineEdit)
        self.student_enter_passportlineEdit = QtWidgets.QLineEdit(self.frame_4)
        self.student_enter_passportlineEdit.setObjectName("student_enter_passportlineEdit")
        self.verticalLayout_2.addWidget(self.student_enter_passportlineEdit)
        self.frame_2 = QtWidgets.QFrame(Student_Enter_window)
        self.frame_2.setGeometry(QtCore.QRect(5, 320, 390, 30))
        self.frame_2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.student_enter_pushButton = QtWidgets.QPushButton(self.frame_2)
        self.student_enter_pushButton.setGeometry(QtCore.QRect(160, 3, 70, 25))
        font = QtGui.QFont()
        font.setBold(True)
        font.setUnderline(True)
        font.setWeight(75)
        self.student_enter_pushButton.setFont(font)
        self.student_enter_pushButton.setObjectName("student_enter_pushButton")

        self.retranslateUi(Student_Enter_window)
        QtCore.QMetaObject.connectSlotsByName(Student_Enter_window)

    def retranslateUi(self, Student_Enter_window):
        _translate = QtCore.QCoreApplication.translate
        Student_Enter_window.setWindowTitle(_translate("Student_Enter_window", "Enter"))
        self.label_8.setText(_translate("Student_Enter_window", "Name"))
        self.label.setText(_translate("Student_Enter_window", "Last Name"))
        self.label_3.setText(_translate("Student_Enter_window", "Patronymic"))
        self.label_2.setText(_translate("Student_Enter_window", "Birth Date"))
        self.label_5.setText(_translate("Student_Enter_window", "Address"))
        self.label_4.setText(_translate("Student_Enter_window", "Phone Number"))
        self.label_6.setText(_translate("Student_Enter_window", "Email"))
        self.label_7.setText(_translate("Student_Enter_window", "Passport ID"))
        self.student_enter_pushButton.setText(_translate("Student_Enter_window", "OK"))
class Ui_Student_Replace_window(object):
    def setupUi(self, Student_Replace_window):
        Student_Replace_window.setObjectName("Student_Replace_window")
        Student_Replace_window.resize(400, 354)
        Student_Replace_window.setMinimumSize(QtCore.QSize(400, 354))
        Student_Replace_window.setMaximumSize(QtCore.QSize(400, 354))
        self.frame = QtWidgets.QFrame(Student_Replace_window)
        self.frame.setGeometry(QtCore.QRect(5, 5, 390, 310))
        self.frame.setFrameShape(QtWidgets.QFrame.Panel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.frame_3 = QtWidgets.QFrame(self.frame)
        self.frame_3.setGeometry(QtCore.QRect(5, 5, 140, 300))
        self.frame_3.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.frame_3)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_8 = QtWidgets.QLabel(self.frame_3)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_8.setFont(font)
        self.label_8.setObjectName("label_8")
        self.verticalLayout.addWidget(self.label_8)
        self.label = QtWidgets.QLabel(self.frame_3)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.label_3 = QtWidgets.QLabel(self.frame_3)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.verticalLayout.addWidget(self.label_3)
        self.label_2 = QtWidgets.QLabel(self.frame_3)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.label_5 = QtWidgets.QLabel(self.frame_3)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.verticalLayout.addWidget(self.label_5)
        self.label_4 = QtWidgets.QLabel(self.frame_3)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.verticalLayout.addWidget(self.label_4)
        self.label_6 = QtWidgets.QLabel(self.frame_3)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.verticalLayout.addWidget(self.label_6)
        self.label_7 = QtWidgets.QLabel(self.frame_3)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        self.verticalLayout.addWidget(self.label_7)
        self.label_9 = QtWidgets.QLabel(self.frame_3)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_9.setFont(font)
        self.label_9.setObjectName("label_9")
        self.label_9.setStyleSheet("color: red")
        self.verticalLayout.addWidget(self.label_9)
        self.frame_4 = QtWidgets.QFrame(self.frame)
        self.frame_4.setGeometry(QtCore.QRect(150, 5, 235, 301))
        self.frame_4.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_4.setObjectName("frame_4")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.frame_4)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.student_replace_name_lineEdit = QtWidgets.QLineEdit(self.frame_4)
        self.student_replace_name_lineEdit.setObjectName("student_replace_name_lineEdit")
        self.verticalLayout_2.addWidget(self.student_replace_name_lineEdit)
        self.student_replace_LName_lineEdit = QtWidgets.QLineEdit(self.frame_4)
        self.student_replace_LName_lineEdit.setObjectName("student_replace_LName_lineEdit")
        self.verticalLayout_2.addWidget(self.student_replace_LName_lineEdit)
        self.student_replace_patro_lineEdit = QtWidgets.QLineEdit(self.frame_4)
        self.student_replace_patro_lineEdit.setObjectName("student_replace_patro_lineEdit")
        self.verticalLayout_2.addWidget(self.student_replace_patro_lineEdit)
        self.student_replace_BDate_lineEdit = QtWidgets.QLineEdit(self.frame_4)
        self.student_replace_BDate_lineEdit.setObjectName("student_replace_BDate_lineEdit")
        self.verticalLayout_2.addWidget(self.student_replace_BDate_lineEdit)
        self.student_replace_address_lineEdit = QtWidgets.QLineEdit(self.frame_4)
        self.student_replace_address_lineEdit.setObjectName("student_replace_address_lineEdit")
        self.verticalLayout_2.addWidget(self.student_replace_address_lineEdit)
        self.student_replace_PNumber_lineEdit = QtWidgets.QLineEdit(self.frame_4)
        self.student_replace_PNumber_lineEdit.setObjectName("student_replace_PNumber_lineEdit")
        self.verticalLayout_2.addWidget(self.student_replace_PNumber_lineEdit)
        self.student_replace_email_lineEdit = QtWidgets.QLineEdit(self.frame_4)
        self.student_replace_email_lineEdit.setObjectName("student_replace_email_lineEdit")
        self.verticalLayout_2.addWidget(self.student_replace_email_lineEdit)
        self.student_replace_passportlineEdit = QtWidgets.QLineEdit(self.frame_4)
        self.student_replace_passportlineEdit.setObjectName("student_replace_passportlineEdit")
        self.verticalLayout_2.addWidget(self.student_replace_passportlineEdit)
        self.student_replace_ID_comboBox = QtWidgets.QComboBox(self.frame_4)
        self.student_replace_ID_comboBox.setObjectName("student_replace_ID_comboBox")
        for i in range(len(student_dict)):
            self.student_replace_ID_comboBox.addItem("")
        self.verticalLayout_2.addWidget(self.student_replace_ID_comboBox)
        self.frame_2 = QtWidgets.QFrame(Student_Replace_window)
        self.frame_2.setGeometry(QtCore.QRect(5, 320, 390, 30))
        self.frame_2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.student_replace_pushButton = QtWidgets.QPushButton(self.frame_2)
        self.student_replace_pushButton.setGeometry(QtCore.QRect(160, 3, 70, 25))
        font = QtGui.QFont()
        font.setBold(True)
        font.setUnderline(True)
        font.setWeight(75)
        self.student_replace_pushButton.setFont(font)
        self.student_replace_pushButton.setObjectName("student_replace_pushButton")

        self.retranslateUi(Student_Replace_window)
        QtCore.QMetaObject.connectSlotsByName(Student_Replace_window)

    def updateCombo(self, index):
        self.student_replace_name_lineEdit.setText(str(STUDENTS.Name[index]))
        self.student_replace_LName_lineEdit.setText(str(STUDENTS.Last_Name[index]))
        self.student_replace_patro_lineEdit.setText(str(STUDENTS.Patronymic[index]))
        self.student_replace_BDate_lineEdit.setText(str(STUDENTS.Birth_Date[index]))
        self.student_replace_address_lineEdit.setText(str(STUDENTS.Address[index]))
        self.student_replace_PNumber_lineEdit.setText(str(STUDENTS.Phone_Number[index]))
        self.student_replace_email_lineEdit.setText(str(STUDENTS.Email[index]))
        self.student_replace_passportlineEdit.setText(STUDENTS.Passport_ID[index])

    def retranslateUi(self, Student_Replace_window):
        _translate = QtCore.QCoreApplication.translate
        Student_Replace_window.setWindowTitle(_translate("Student_Replace_window", "Update"))
        self.label_8.setText(_translate("Student_Replace_window", "Name"))
        self.label.setText(_translate("Student_Replace_window", "Last Name"))
        self.label_3.setText(_translate("Student_Replace_window", "Patronymic"))
        self.label_2.setText(_translate("Student_Replace_window", "Birth Date"))
        self.label_5.setText(_translate("Student_Replace_window", "Address"))
        self.label_4.setText(_translate("Student_Replace_window", "Phone Number"))
        self.label_6.setText(_translate("Student_Replace_window", "Email"))
        self.label_7.setText(_translate("Student_Replace_window", "Passport ID"))
        self.label_9.setText(_translate("Student_Replace_window", "ID"))
        self.student_replace_name_lineEdit.setText(str(STUDENTS.Name[0]))
        self.student_replace_LName_lineEdit.setText(str(STUDENTS.Last_Name[0]))
        self.student_replace_patro_lineEdit.setText(str(STUDENTS.Patronymic[0]))
        self.student_replace_BDate_lineEdit.setText(str(STUDENTS.Birth_Date[0]))
        self.student_replace_address_lineEdit.setText(str(STUDENTS.Address[0]))
        self.student_replace_PNumber_lineEdit.setText(str(STUDENTS.Phone_Number[0]))
        self.student_replace_email_lineEdit.setText(str(STUDENTS.Email[0]))
        self.student_replace_passportlineEdit.setText(STUDENTS.Passport_ID[0])
        for i in range(len(student_dict)):
            self.student_replace_ID_comboBox.setItemText(i, _translate("Student_Replace_window", str(i+1)))
        self.student_replace_pushButton.setText(_translate("Student_Replace_window", "OK"))
        self.student_replace_ID_comboBox.currentIndexChanged.connect(self.updateCombo)
class Ui_Subject_Enter_Window(object):
    def setupUi(self, Subject_Enter_Window):
        Subject_Enter_Window.setObjectName("Subject_Enter_Window")
        Subject_Enter_Window.resize(400, 215)
        Subject_Enter_Window.setMinimumSize(QtCore.QSize(400, 215))
        Subject_Enter_Window.setMaximumSize(QtCore.QSize(400, 215))
        self.frame = QtWidgets.QFrame(Subject_Enter_Window)
        self.frame.setGeometry(QtCore.QRect(5, 5, 390, 160))
        self.frame.setFrameShape(QtWidgets.QFrame.Panel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.frame_3 = QtWidgets.QFrame(self.frame)
        self.frame_3.setGeometry(QtCore.QRect(5, 5, 140, 200))
        self.frame_3.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.subjects_enter_title_txt = QtWidgets.QLabel(self.frame_3)
        self.subjects_enter_title_txt.setGeometry(QtCore.QRect(10, 46, 120, 30))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.subjects_enter_title_txt.setFont(font)
        self.subjects_enter_title_txt.setObjectName("subjects_enter_title_txt")
        self.subjects_enter_category_id_label_txt = QtWidgets.QLabel(self.frame_3)
        self.subjects_enter_category_id_label_txt.setGeometry(QtCore.QRect(10, 10, 120, 30))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.subjects_enter_category_id_label_txt.setFont(font)
        self.subjects_enter_category_id_label_txt.setObjectName("subjects_enter_category_id_label_txt")
        self.subjects_enter_description_txt = QtWidgets.QLabel(self.frame_3)
        self.subjects_enter_description_txt.setGeometry(QtCore.QRect(10, 82, 120, 30))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.subjects_enter_description_txt.setFont(font)
        self.subjects_enter_description_txt.setObjectName("subjects_enter_description_txt")
        self.subjects_enter_price_txt = QtWidgets.QLabel(self.frame_3)
        self.subjects_enter_price_txt.setGeometry(QtCore.QRect(10, 118, 120, 30))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.subjects_enter_price_txt.setFont(font)
        self.subjects_enter_price_txt.setObjectName("subjects_enter_price_txt")
        self.frame_4 = QtWidgets.QFrame(self.frame)
        self.frame_4.setGeometry(QtCore.QRect(150, 5, 235, 160))
        self.frame_4.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_4.setObjectName("frame_4")
        self.subjects_enter_title_line = QtWidgets.QLineEdit(self.frame_4)
        self.subjects_enter_title_line.setGeometry(QtCore.QRect(10, 49, 215, 25))
        self.subjects_enter_title_line.setObjectName("subjects_enter_title_line")
        self.subjects_enter_category_id_combo_box = QtWidgets.QComboBox(self.frame_4)
        self.subjects_enter_category_id_combo_box.setGeometry(QtCore.QRect(10, 14, 215, 25))
        self.subjects_enter_category_id_combo_box.setObjectName("subjects_enter_category_id_combo_box")
        for i in range(len(category_dict)):
            self.subjects_enter_category_id_combo_box.addItem("")
        self.subjects_enter_description_line = QtWidgets.QLineEdit(self.frame_4)
        self.subjects_enter_description_line.setGeometry(QtCore.QRect(10, 84, 215, 25))
        self.subjects_enter_description_line.setObjectName("subjects_enter_description_line")
        self.subjects_enter_price_line = QtWidgets.QLineEdit(self.frame_4)
        self.subjects_enter_price_line.setGeometry(QtCore.QRect(10, 119, 215, 25))
        self.subjects_enter_price_line.setObjectName("subjects_enter_price_line")
        self.frame_2 = QtWidgets.QFrame(Subject_Enter_Window)
        self.frame_2.setGeometry(QtCore.QRect(5, 175, 390, 30))
        self.frame_2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.pushButton = QtWidgets.QPushButton(self.frame_2)
        self.pushButton.setGeometry(QtCore.QRect(160, 3, 70, 25))
        font = QtGui.QFont()
        font.setBold(True)
        font.setUnderline(True)
        font.setWeight(75)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")

        self.retranslateUi(Subject_Enter_Window)
        QtCore.QMetaObject.connectSlotsByName(Subject_Enter_Window)

    def retranslateUi(self, Subject_Enter_Window):
        _translate = QtCore.QCoreApplication.translate
        Subject_Enter_Window.setWindowTitle(_translate("Subject_Enter_Window", "Enter"))
        self.subjects_enter_title_txt.setText(_translate("Subject_Enter_Window", "Title"))
        self.subjects_enter_category_id_label_txt.setText(_translate("Subject_Enter_Window", "Category"))
        self.subjects_enter_description_txt.setText(_translate("Subject_Enter_Window", "Description"))
        self.subjects_enter_price_txt.setText(_translate("Subject_Enter_Window", "Price"))
        for key, value in category_dict.items():
            self.subjects_enter_category_id_combo_box.setItemText(value-1, _translate("Subject_Enter_Window", key))
        self.pushButton.setText(_translate("Subject_Enter_Window", "OK"))
class Ui_Subject_Replace_Window(object):
    def setupUi(self, Subject_Replace_Window):
        Subject_Replace_Window.setObjectName("Subject_Replace_Window")
        Subject_Replace_Window.resize(400, 245)
        Subject_Replace_Window.setMinimumSize(QtCore.QSize(400, 245))
        Subject_Replace_Window.setMaximumSize(QtCore.QSize(400, 245))
        self.frame = QtWidgets.QFrame(Subject_Replace_Window)
        self.frame.setGeometry(QtCore.QRect(5, 5, 390, 200))
        self.frame.setFrameShape(QtWidgets.QFrame.Panel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.frame_3 = QtWidgets.QFrame(self.frame)
        self.frame_3.setGeometry(QtCore.QRect(5, 5, 140, 190))
        self.frame_3.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.subjects_rename_title_txt = QtWidgets.QLabel(self.frame_3)
        self.subjects_rename_title_txt.setGeometry(QtCore.QRect(10, 46, 120, 30))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.subjects_rename_title_txt.setFont(font)
        self.subjects_rename_title_txt.setObjectName("subjects_rename_title_txt")
        self.subjects_enter_category_id_label_txt = QtWidgets.QLabel(self.frame_3)
        self.subjects_enter_category_id_label_txt.setGeometry(QtCore.QRect(10, 10, 120, 30))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.subjects_enter_category_id_label_txt.setFont(font)
        self.subjects_enter_category_id_label_txt.setObjectName("subjects_enter_category_id_label_txt")
        self.subjects_rename_description_txt = QtWidgets.QLabel(self.frame_3)
        self.subjects_rename_description_txt.setGeometry(QtCore.QRect(10, 82, 120, 30))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.subjects_rename_description_txt.setFont(font)
        self.subjects_rename_description_txt.setObjectName("subjects_rename_description_txt")
        self.subjects_rename_price_txt = QtWidgets.QLabel(self.frame_3)
        self.subjects_rename_price_txt.setGeometry(QtCore.QRect(10, 118, 120, 30))
        font = QtGui.QFont()
        font.setPointSize(13)
        font.setBold(True)
        font.setWeight(75)
        self.subjects_rename_price_txt.setFont(font)
        self.subjects_rename_price_txt.setObjectName("subjects_rename_price_txt")
        self.subjects_rename_id_label_txt = QtWidgets.QLabel(self.frame_3)
        self.subjects_rename_id_label_txt.setGeometry(QtCore.QRect(10, 154, 120, 30))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.subjects_rename_id_label_txt.setFont(font)
        self.subjects_rename_id_label_txt.setObjectName("subjects_rename_id_label_txt")
        self.subjects_rename_id_label_txt.setStyleSheet("color: red")
        self.frame_4 = QtWidgets.QFrame(self.frame)
        self.frame_4.setGeometry(QtCore.QRect(150, 5, 235, 190))
        self.frame_4.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_4.setObjectName("frame_4")
        self.subject_rename_title_line = QtWidgets.QLineEdit(self.frame_4)
        self.subject_rename_title_line.setGeometry(QtCore.QRect(10, 49, 215, 25))
        self.subject_rename_title_line.setObjectName("subject_rename_title_line")
        self.subjects_rename_category_id_combo_box = QtWidgets.QComboBox(self.frame_4)
        self.subjects_rename_category_id_combo_box.setGeometry(QtCore.QRect(10, 14, 215, 25))
        self.subjects_rename_category_id_combo_box.setObjectName("subjects_rename_category_id_combo_box")
        for i in range(len(category_dict)):
            self.subjects_rename_category_id_combo_box.addItem("")
        self.subjects_rename_description_line = QtWidgets.QLineEdit(self.frame_4)
        self.subjects_rename_description_line.setGeometry(QtCore.QRect(10, 84, 215, 25))
        self.subjects_rename_description_line.setObjectName("subjects_rename_description_line")
        self.subject_rename_price_line = QtWidgets.QLineEdit(self.frame_4)
        self.subject_rename_price_line.setGeometry(QtCore.QRect(10, 119, 215, 25))
        self.subject_rename_price_line.setObjectName("subject_rename_price_line")
        self.subject_rename_id_combo_box = QtWidgets.QComboBox(self.frame_4)
        self.subject_rename_id_combo_box.setGeometry(QtCore.QRect(10, 154, 215, 25))
        self.subject_rename_id_combo_box.setObjectName("subject_rename_id_combo_box")
        for i in range(len(subject_dict)):
            self.subject_rename_id_combo_box.addItem("")
        self.frame_2 = QtWidgets.QFrame(Subject_Replace_Window)
        self.frame_2.setGeometry(QtCore.QRect(5, 210, 390, 30))
        self.frame_2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.pushButton = QtWidgets.QPushButton(self.frame_2)
        self.pushButton.setGeometry(QtCore.QRect(160, 3, 70, 25))
        font = QtGui.QFont()
        font.setBold(True)
        font.setUnderline(True)
        font.setWeight(75)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")

        self.retranslateUi(Subject_Replace_Window)
        QtCore.QMetaObject.connectSlotsByName(Subject_Replace_Window)

    def updateCombo(self, index):
        self.subjects_rename_category_id_combo_box.setCurrentIndex(index)
        self.subject_rename_title_line.setText(str(SUBJECT.Title[index]))
        self.subjects_rename_description_line.setText(str(SUBJECT.Description[index]))
        self.subject_rename_price_line.setText(str(SUBJECT.Price[index]))

    def retranslateUi(self, Subject_Replace_Window):
        _translate = QtCore.QCoreApplication.translate
        Subject_Replace_Window.setWindowTitle(_translate("Subject_Replace_Window", "Update"))
        self.subjects_rename_title_txt.setText(_translate("Subject_Replace_Window", "Title"))
        self.subjects_enter_category_id_label_txt.setText(_translate("Subject_Replace_Window", "Category"))
        self.subjects_rename_description_txt.setText(_translate("Subject_Replace_Window", "Description"))
        self.subjects_rename_price_txt.setText(_translate("Subject_Replace_Window", "Price"))
        self.subjects_rename_id_label_txt.setText(_translate("Subject_Replace_Window", "ID"))
        self.subject_rename_title_line.setText(str(SUBJECT.Title[0]))
        self.subjects_rename_description_line.setText(str(SUBJECT.Description[0]))
        self.subject_rename_price_line.setText(str(SUBJECT.Price[0]))
        for key, value in category_dict.items():
            self.subjects_rename_category_id_combo_box.setItemText(value-1, _translate("Subject_Replace_Window", key))
        for i in range(len(subject_dict)):
            self.subject_rename_id_combo_box.setItemText(i, _translate("Subject_Replace_Window", str(i+1)))
        self.pushButton.setText(_translate("Subject_Replace_Window", "OK"))
        self.subject_rename_id_combo_box.currentIndexChanged.connect(self.updateCombo)

### MAIN WINDOW CLASS
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.ui  = Ui_MainWindow()
        self.ui.setupUi(self)

        ### this will overide fonts selected in qt designer
        apply_stylesheet(app, theme='dark_cyan.xml')

        ### Remove window title bar
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)

        ### Set main background to transparent
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        ### Shadow effect style
        self.shadow = QtWidgets.QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(50)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QColor(0, 92, 157, 550))

        ### Help button
        self.ui.help_button.setToolTip('''\n\tClick on the left menu bar features to see data tables.\t
        \tUse <ADD>  and  <REPLACE> buttons to make changes on data.\t
        \tOn the right side of window you can see our Links.\t\n''')

        ### Apply shadow to central widget
        self.ui.centralwidget.setGraphicsEffect(self.shadow)

        ### Set window Icon
        self.setWindowIcon(QtGui.QIcon("./icons/icons8-logo-48.png"))

        ### Set window title
        self.setWindowTitle("Data Manager")

        ### Window Size grip to resize window
        QSizeGrip(self.ui.size_grip)

        ### Minimize window
        self.ui.window_minimize_button.clicked.connect(lambda: self.showMinimized())

        ### Close window
        self.ui.window_close_button.clicked.connect(lambda: self.close())

        ### Restore/Maximize window
        self.ui.window_restore_button.clicked.connect(lambda: self.restore_or_maximize_window())

        ### STACKED PAGES NAVIGATION, Using side menu button
        # navigate to Students page
        self.ui.student_button.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.students))
        # navigate to Groups page
        self.ui.group_button.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.groups))
        # navigate to Staff page
        self.ui.staff_button.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.staff))
        # navigate to instructors page
        self.ui.instructor_button.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.instructors))
        # navigate to audiences page
        self.ui.audienc_button.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.audiences))
        # navigate to categories page
        self.ui.category_button.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.categories))
        # navigate to subjects page
        self.ui.subject_button.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.subjects))
        # navigate to schedules page
        self.ui.schedule_button.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.schedule))

        ### Function to move window on mouse drag event on the title bar
        def moveWindow(e):
            # Detect if the window is in normal size
            if self.isMaximized() == False:
                # Accept only left mouse clicks
                if e.buttons() == Qt.LeftButton:
                    self.move(self.pos() + e.globalPos() - self.clickPosition)
                    self.clickPosition = e.globalPos()
                    e.accept()
     
        ### Add click event/Mouse move event/drag event to the top header to move the window
        self.ui.header_frame.mouseMoveEvent = moveWindow

        ### Left Menu toggle button (Show hidden menu labels)
        self.ui.menu_button.clicked.connect(lambda: self.slideLeftMenu())

        ### Style clicked menu button
        for w in self.ui.menu_frame.findChildren(QPushButton):
            # Add click event listener
            w.clicked.connect(self.applyButtonStyle)

        GetData()
        self.show()
        self.show_students()
        self.show_groups()
        self.show_staff()
        self.show_instructor()
        self.show_audience()
        self.show_category()
        self.show_subject()
        self.show_schedule()

    
    ### A function that creates table widget
    def create_table_widget(self, rowPosition, columnPosition, text, tableName):
        qtablewidgetitem = QTableWidgetItem()
        getattr(self.ui, tableName).setItem(rowPosition, columnPosition, qtablewidgetitem)
        qtablewidgetitem = getattr(self.ui, tableName).item(rowPosition, columnPosition)
        qtablewidgetitem.setText(text)


    ### add new row 
    def addrow(self,name):
        
        if name == "Student":

            # Calling entry window
            self.window = QtWidgets.QMainWindow()
            self.w = Ui_Student_Enter_window()
            self.w.setupUi(self.window)
            self.window.show()


            def OkClicked():
                #Dictionary for key(nameerror):value(True or false)
                errorDict = dict()
                # Reading data from line and doing validation
                readName = self.w.student_enter_name_lineEdit.text()
                if validation.isValidName(readName):
                    errorDict["NameError"] = True
                else:
                    errorDict["NameError"] = False
                  
                readLast_name = self.w.student_enter_LName_lineEdit.text()
                if validation.isValidName(readLast_name):
                    errorDict["LastNameError"] = True
                else:
                    errorDict["LastNameError"] = False

                readPatronymic = self.w.student_enter_patro_lineEdit.text()
                if validation.isValidName(readPatronymic):
                    errorDict["PatronymicError"] = True
                else:
                    errorDict["PatronymicError"] = False

                readBirthDate = self.w.student_enter_BDate_lineEdit.text()
                if validation.isValidBirthDate(readBirthDate):
                    errorDict["BirthDayError"] = True
                else:
                    errorDict["BirthDayError"] = False

                readAddress = self.w.student_enter_address_lineEdit.text()

                readPhone_number = self.w.student_enter_PNumber_lineEdit.text()
                if validation.isValidPhoneNumber(readPhone_number):
                    errorDict["PhoneNumberError"] = True
                else:
                    errorDict["PhoneNumberError"] = False

                readEmail = self.w.student_enter_email_lineEdit.text()
                if validation.isValidEmail(readEmail):
                    errorDict["EmailError"] = True
                else:
                    errorDict["EmailError"] = False

                readPassport_ID = self.w.student_enter_passportlineEdit.text()

                #List for show errors
                showError = []
                #through this cikle we add errors name into our list(showError)
                for item in errorDict:
                    if errorDict[item] == True:
                        pass
                    else:
                        showError.append(item)

                #if our showError list has one or more items` we can know that we have error and we can use MessageBox
                #else we can know that everything is fine and we can add our data
                if len(showError) >= 1:
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Critical)
                    msg.setText(str(showError))
                    msg.setInformativeText('More information')
                    msg.setWindowTitle("Invalid Syntax")
                    msg.exec_()
                else:
                    #            #"student" : ["Name", "Last_Name", "Patronymic", "Birth_Date", "Address", "Phone_Number", "Email", "Passport_ID"],

                    # Adding new empty row
                    rowPosition = self.ui.student_tableWidget.rowCount()
                    self.ui.student_tableWidget.insertRow(rowPosition)
                    # Connecting to server 
                    con = connect(host=Host, user=uName, passwd=Pass, db=DataBase)
                    myCursor = con.cursor()
                    # Transfer data to server
                    myCursor.execute("INSERT INTO student(student_ID,name, last_name, patronymic, birth_date, address, phone_number, email, passport_ID) VALUES({},'{}','{}','{}','{}','{}','{}','{}','{}')".format(rowPosition+1, readName, readLast_name, readPatronymic, readBirthDate, readAddress, readPhone_number, readEmail, readPassport_ID))
                    # Confirming new changes in server
                    con.commit()
                    # Closing connection
                    con.close()
                    # Adding new row information
                    self.create_table_widget(rowPosition, 0, str(rowPosition+1), "student_tableWidget")
                    self.create_table_widget(rowPosition, 1, str(readName), "student_tableWidget")
                    self.create_table_widget(rowPosition, 2, str(readLast_name), "student_tableWidget") 
                    self.create_table_widget(rowPosition, 3, str(readPatronymic), "student_tableWidget")
                    self.create_table_widget(rowPosition, 4, str(readBirthDate), "student_tableWidget")
                    self.create_table_widget(rowPosition, 5, str(readAddress), "student_tableWidget")
                    self.create_table_widget(rowPosition, 6, str(readPhone_number), "student_tableWidget")              
                    self.create_table_widget(rowPosition, 7, str(readEmail), "student_tableWidget")
                    self.create_table_widget(rowPosition, 8, str(readPassport_ID), "student_tableWidget")
                    # Closing entry window
                    self.window.close()
                    # Updating data in program
                    GetData()

            #Navigate  ok button   
            self.w.student_enter_pushButton.clicked.connect(lambda: OkClicked())



       
        elif name == "Group":
            
            # Calling entry window
            self.window = QtWidgets.QMainWindow()
            self.w = Ui_Group_Enter_Window()
            self.w.setupUi(self.window)
            self.window.show()


            def OkClicked():
                #Dictionary for key(nameerror):value(True or false)
                errorDict = dict()
                # Reading data from line and doing validation
                readData = self.w.group_enter_title_line.text()
                if readData:
                    if readData.isdigit():
                        errorDict["TitleError"] = False
                    else:
                        errorDict["TitleError"] = True
                else:
                    errorDict["TitleError"] = False

                #List for show errors
                showError = []
                #through this cikle we add errors name into our list(showError)
                for item in errorDict:
                    if errorDict[item] == True:
                        pass
                    else:
                        showError.append(item)

                #if our showError list has one or more items` we can know that we have error and we can use MessageBox
                #else we can know that everything is fine and we can add our data
                if len(showError) >= 1:
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Critical)
                    msg.setText(str(showError))
                    msg.setInformativeText('More information')
                    msg.setWindowTitle("Invalid Syntax")
                    msg.exec_()
                else:
                    # Adding new empty row
                    rowPosition = self.ui.group_tableWidget.rowCount()
                    self.ui.group_tableWidget.insertRow(rowPosition)
                    # Connecting to server
                    con = connect(host=Host, user=uName, passwd=Pass, db=DataBase)
                    myCursor = con.cursor()
                    # Transfer data to server
                    myCursor.execute("INSERT INTO groupp(group_ID, title) VALUES({line},'{txt}')".format(line = rowPosition+1, txt=readData))
                    # Confirming new changes in server
                    con.commit()
                    # Closing connection
                    con.close()
                    # Adding new row information
                    self.create_table_widget(rowPosition, 0, str(rowPosition+1), "group_tableWidget")
                    self.create_table_widget(rowPosition, 1, str(readData), "group_tableWidget")
                    # Closing entry window
                    self.window.close()
                    # Updating data in program
                    GetData()
                    
            # Calling function when <OK> is clicked
            self.w.pushButton.clicked.connect(lambda: OkClicked())

        
        elif name == "Staff":

            # Calling entry window
            self.window = QtWidgets.QMainWindow()
            self.w = Ui_Staff_Enter_Window()
            self.w.setupUi(self.window)
            self.window.show()

            
            def OkClicked():
                #Dictionary for key(nameerror):value(True or false)
                errorDict = dict()
                # Reading data from line and doing validation
                readName = self.w.staff_name_enter_lineEdit.text()
                
                if validation.isValidName(readName):
                    errorDict["NameError"] = True
                else:
                    errorDict["NameError"] = False
                  
                readLast_name = self.w.staff_lastname_enter_lineEdit.text()
                if validation.isValidName(readLast_name):
                    errorDict["LastNameError"] = True
                else:
                    errorDict["LastNameError"] = False

                readPatronymic = self.w.staff_patronymic_enter_lineEdit.text()
                if validation.isValidName(readPatronymic):
                    errorDict["PatronymicError"] = True
                else:
                    errorDict["PatronymicError"] = False

                readEducation = self.w.staff_education_enter_lineEdit.text()
            
                readAddress = self.w.staff_address_enter_lineEdit.text()

                readPhone_number = self.w.staff_phonenumber_enter_lineEdit.text()
                if validation.isValidPhoneNumber(readPhone_number):
                    errorDict["PhoneNumberError"] = True
                else:
                    errorDict["PhoneNumberError"] = False

                readEmail = self.w.staff_email_enter_lineEdit.text()
                if validation.isValidEmail(readEmail):
                    errorDict["EmailError"] = True
                else:
                    errorDict["EmailError"] = False

                readPosition_ID = self.w.staff_position_enter_comboBox.currentText()

                #List for show errors
                showError = []
                #through this cikle we add errors name into our list(showError)
                for item in errorDict:
                    if errorDict[item] == True:
                        pass
                    else:
                        showError.append(item)

                #if our showError list has one or more items` we can know that we have error and we can use MessageBox
                #else we can know that everything is fine and we can add our data
                if len(showError) >= 1:
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Critical)
                    msg.setText(str(showError))
                    msg.setInformativeText('More information')
                    msg.setWindowTitle("Invalid Syntax")
                    msg.exec_()
                else:
                    # Adding new empty row
                    rowPosition = self.ui.staff_tableWidget.rowCount()
                    self.ui.staff_tableWidget.insertRow(rowPosition)
                    # Connecting to server
                    con = connect(host=Host, user=uName, passwd=Pass, db=DataBase)
                    myCursor = con.cursor()
                    # Transfer data to server
                    myCursor.execute("INSERT INTO staff(staff_ID, name, last_name, patronymic, education, address, phone_number, email, position_ID) VALUES({},'{}','{}','{}','{}','{}','{}','{}',{})".format(rowPosition+1, readName, readLast_name, readPatronymic, readEducation, readAddress, readPhone_number, readEmail, position_dict[readPosition_ID]))
                    # Confirming new changes in server
                    con.commit()
                    # Closing connection
                    con.close()
                    # Adding new row information
                    self.create_table_widget(rowPosition, 0, str(rowPosition+1), "staff_tableWidget")
                    self.create_table_widget(rowPosition, 1, str(readName), "staff_tableWidget")
                    self.create_table_widget(rowPosition, 2, str(readLast_name), "staff_tableWidget") 
                    self.create_table_widget(rowPosition, 3, str(readPatronymic), "staff_tableWidget")
                    self.create_table_widget(rowPosition, 4, str(readEducation), "staff_tableWidget")
                    self.create_table_widget(rowPosition, 5, str(readAddress), "staff_tableWidget")
                    self.create_table_widget(rowPosition, 6, str(readPhone_number), "staff_tableWidget")              
                    self.create_table_widget(rowPosition, 7, str(readEmail), "staff_tableWidget")
                    self.create_table_widget(rowPosition, 8, str(readPosition_ID), "staff_tableWidget")
                    # Closing entry window
                    self.window.close()
                    # Updating data in program
                    GetData()

            #Navigate  ok button   
            self.w.Staff_Enter_pushButton.clicked.connect(lambda: OkClicked())


       
        elif name == "Instructor":
         
            # Calling entry window
            self.window = QtWidgets.QMainWindow()
            self.w = Ui_Instructor_Enter_Window()
            self.w.setupUi(self.window)
            self.window.show()

            
            def OkClicked():
                
                #Dictionary for key(nameerror):value(True or false)
                errorDict = dict()
                # Reading data from line and doing validation
                readStaff_ID = self.w.instructor_enter_staff_id_combo_box.currentText()
                  
                readDescription = self.w.instructor_enter_description_line.text()
                if readDescription:
                    errorDict["DescriptionError"] = True
                else:
                    errorDict["DescriptionError"] = False

                readTeaching_object = self.w.instructor_enter_teaching_object_line.text()
                if readTeaching_object:
                    errorDict["TeachingObjectError"] = True
                else:
                    errorDict["TeachingObjectError"] = False

                #List for show errors
                showError = []
                #through this cikle we add errors name into our list(showError)
                for item in errorDict:
                    if errorDict[item] == True:
                        pass
                    else:
                        showError.append(item)

                #if our showError list has one or more items` we can know that we have error and we can use MessageBox
                #else we can know that everything is fine and we can add our data
                if len(showError) >= 1:
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Critical)
                    msg.setText(str(showError))
                    msg.setInformativeText('More information')
                    msg.setWindowTitle("Invalid Syntax")
                    msg.exec_() 
                else:
                    # Adding new empty row
                    rowPosition = self.ui.instructor_tableWidget.rowCount()
                    self.ui.instructor_tableWidget.insertRow(rowPosition)
                    # Connecting to server
                    con = connect(host=Host, user=uName, passwd=Pass, db=DataBase)
                    myCursor = con.cursor()
                    # Transfer data to server
                    myCursor.execute("INSERT INTO instructor(instructor_ID, staff_ID, description, teaching_object) VALUES({},{},'{}','{}')".format(rowPosition+1, staff_dict[readStaff_ID], readDescription, readTeaching_object))
                    # Confirming new changes in server
                    con.commit()
                    # Closing connection
                    con.close()
                    # Adding new row information
                  
                    self.create_table_widget(rowPosition, 0, str(rowPosition+1), "instructor_tableWidget")
                    self.create_table_widget(rowPosition, 1, str(readStaff_ID), "instructor_tableWidget")
                    self.create_table_widget(rowPosition, 2, str(readDescription), "instructor_tableWidget") 
                    self.create_table_widget(rowPosition, 3, str(readTeaching_object), "instructor_tableWidget") 

                    # Closing entry window
                    self.window.close()
                    # Updating data in program
                    GetData()

            self.w.pushButton.clicked.connect(lambda: OkClicked())

        
        elif name == "Audience":
       
            # Calling entry window
            self.window = QtWidgets.QMainWindow()
            self.w = Ui_Audience_Enter_Window()
            self.w.setupUi(self.window)
            self.window.show()


            def OkClicked():    

                #Dictionary for key(nameerror):value(True or false)
                errorDict = dict()
                # Reading data from line and doing validation
                readTitle = self.w.audience_title_enter_lineEdit.text()
                if readTitle:
                    errorDict["TitleError"] = True
                else:
                    errorDict["TitleError"] = False
                
                readSeatcount = self.w.audience_seatCount_enter_lineEdit.text()
                if readSeatcount.isdigit():
                    errorDict["SeatCountError"] = True
                else:
                    errorDict["SeatCountError"] = False

                readCamputercount = self.w.audience_camputer_count_enter_lineEdit.text()
                if readCamputercount.isdigit():
                    errorDict["CamputerCountError"] = True
                else:
                    errorDict["CamputerCountError"] = False

                readID = self.w.audience_ID_enter_lineEdit.text()

                audienceList = list()
                audienceList += audience_dict.values()
               
                if readID in audienceList:
                    errorDict["This ID already Exist"] = False
                elif readID.isdigit():
                    errorDict["IDError"] = True
                else:
                    errorDict["IDError"] = False

                #List for show errors
                showError = []
                #through this cikle we add errors name into our list(showError)
                for item in errorDict:
                    if errorDict[item] == True:
                        pass
                    else:
                        showError.append(item)

                #if our showError list has one or more items` we can know that we have error and we can use MessageBox
                #else we can know that everything is fine and we can add our data
                if len(showError) >= 1:
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Critical)
                    msg.setText(str(showError))
                    msg.setInformativeText('More information')
                    msg.setWindowTitle("Invalid Syntax")
                    msg.exec_() 
                else:
                     #Audience_ID", "Title", "Seat_Count", "Computer_Count
                    # Adding new empty row
                    rowPosition = self.ui.audience_tableWidget.rowCount()
                    self.ui.audience_tableWidget.insertRow(rowPosition)
                    # Connecting to server
                    con = connect(host=Host, user=uName, passwd=Pass, db=DataBase)
                    myCursor = con.cursor()
                    # Transfer data to server
                    myCursor.execute("INSERT INTO audience(audience_ID, title, seat_count, computer_count) VALUES('{}','{}','{}','{}')".format(readID, readTitle, readSeatcount, readCamputercount))
                    # Confirming new changes in server
                    con.commit()
                    # Closing connection
                    con.close()
                    # Adding new row information
                    self.create_table_widget(rowPosition, 0, str(readID), "audience_tableWidget")
                    self.create_table_widget(rowPosition, 1, str(readTitle), "audience_tableWidget")
                    self.create_table_widget(rowPosition, 2, str(readSeatcount), "audience_tableWidget") 
                    self.create_table_widget(rowPosition, 3, str(readCamputercount), "audience_tableWidget") 

                    # Closing entry window
                    self.window.close()
                    # Updating data in program
                    GetData()

            self.w.audience_enter_pushButton.clicked.connect(lambda: OkClicked())


        elif name == "Category":
            
            # Calling entry window
            self.window = QtWidgets.QMainWindow()
            self.w = Ui_Category_Enter_Window()
            self.w.setupUi(self.window)
            self.window.show()

            def OkClicked():
                #Dictionary for key(nameerror):value(True or false)
                errorDict = dict()
                # Reading data from line and doing validation
                readData = self.w.category_subjectCategory_enter_lineEdit.text()
                if readData:
                    if readData.isdigit():
                        errorDict["TitleError"] = False
                    else:
                        errorDict["TitleError"] = True
                else:
                    errorDict["TitleError"] = False

                #List for show errors
                showError = []
                #through this cikle we add errors name into our list(showError)
                for item in errorDict:
                    if errorDict[item] == True:
                        pass
                    else:
                        showError.append(item)

                #if our showError list has one or more items` we can know that we have error and we can use MessageBox
                #else we can know that everything is fine and we can add our data
                if len(showError) >= 1:
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Critical)
                    msg.setText(str(showError))
                    msg.setInformativeText('More information')
                    msg.setWindowTitle("Invalid Syntax")
                    msg.exec_()
                else:
                    # Adding new empty row
                    rowPosition = self.ui.category_tableWidget.rowCount()
                    self.ui.category_tableWidget.insertRow(rowPosition)
                    # Connecting to server
                    con = connect(host=Host, user=uName, passwd=Pass, db=DataBase)
                    myCursor = con.cursor()
                    # Transfer data to server
                    myCursor.execute("INSERT INTO category(category_ID, subject_category) VALUES({},'{}')".format(rowPosition+1, readData))
                    # Confirming new changes in server
                    con.commit()
                    # Closing connection
                    con.close()
                    # Adding new row information
                    self.create_table_widget(rowPosition, 0, str(rowPosition+1), "category_tableWidget")
                    self.create_table_widget(rowPosition, 1, str(readData), "category_tableWidget")
                    # Closing entry window
                    self.window.close()
                    # Updating data in program
                    GetData()
                    
            # Calling function when <OK> is clicked
            self.w.category_enter_pushButton.clicked.connect(lambda: OkClicked())

        
        elif name == "Subject":

            # Calling entry window
            self.window = QtWidgets.QMainWindow()
            self.w = Ui_Subject_Enter_Window()
            self.w.setupUi(self.window)
            self.window.show()
            

            def OkClicked():
                
                #Dictionary for key(nameerror):value(True or false)
                errorDict = dict()
                # Reading data from line and doing validation
                readCategory_ID = self.w.subjects_enter_category_id_combo_box.currentText()
                  
                readTitle = self.w.subjects_enter_title_line.text()
                if readTitle:
                    errorDict["DescriptionError"] = True
                else:
                    errorDict["DescriptionError"] = False

                readDescription = self.w.subjects_enter_description_line.text()
                if readDescription:
                    errorDict["TeachingObjectError"] = True
                else:
                    errorDict["TeachingObjectError"] = False

                readPrice = self.w.subjects_enter_price_line.text()
                if validation.isValidPrice(readPrice):
                    errorDict["PriceError"] = True
                else:
                    errorDict["PriceError"] = False


                #List for show errors
                showError = []
                #through this cikle we add errors name into our list(showError)
                for item in errorDict:
                    if errorDict[item] == True:
                        pass
                    else:
                        showError.append(item)

                #if our showError list has one or more items` we can know that we have error and we can use MessageBox
                #else we can know that everything is fine and we can add our data
                if len(showError) >= 1:
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Critical)
                    msg.setText(str(showError))
                    msg.setInformativeText('More information')
                    msg.setWindowTitle("Invalid Syntax")
                    msg.exec_() 
                else:
                    #"subject" : ["Subject_ID", "Category_ID", "Title", "Description", "Price"],
                    # Adding new empty row
                    rowPosition = self.ui.subject_tableWidget.rowCount()
                    self.ui.subject_tableWidget.insertRow(rowPosition)
                    # Connecting to server
                    con = connect(host=Host, user=uName, passwd=Pass, db=DataBase)
                    myCursor = con.cursor()
                    # Transfer data to server
                    myCursor.execute("INSERT INTO subject(subject_ID, category_ID, title, description, price) VALUES({},{},'{}','{}','{}')".format(rowPosition+1, category_dict[readCategory_ID], readTitle, readDescription, readPrice))
                    # Confirming new changes in server
                    con.commit()
                    # Closing connection
                    con.close()
                    # Adding new row information
            
                    self.create_table_widget(rowPosition, 0, str(rowPosition+1), "subject_tableWidget")
                    self.create_table_widget(rowPosition, 1, str(readCategory_ID), "subject_tableWidget")
                    self.create_table_widget(rowPosition, 2, str(readTitle), "subject_tableWidget") 
                    self.create_table_widget(rowPosition, 3, str(readDescription), "subject_tableWidget") 
                    self.create_table_widget(rowPosition, 4, str(readPrice), "subject_tableWidget")


                    # Closing entry window
                    self.window.close()
                    # Updating data in program
                    GetData()

            self.w.pushButton.clicked.connect(lambda: OkClicked())


        elif name == "Schedule":
            
            # Calling entry window
            self.window = QtWidgets.QMainWindow()
            self.w = Ui_Schedule_Enter_Window()
            self.w.setupUi(self.window)
            self.window.show()

            def OkClicked():
                
                #Dictionary for key(nameerror):value(True or false)
                errorDict = dict()
                # Reading data from line and doing validation
                readGroup = self.w.schedule_group_enter_comboBox.currentText()
                  
                readInstructor = self.w.schedule_instructor_enter_comboBox.currentText()
                
                readSubject = self.w.schedule_subject_enter_comboBox.currentText()

                readAudience = self.w.schedule_audience_enter_comboBox.currentText()

                readLearningtype = self.w.schedule_learningtype_enter_comboBox.currentText()
                
                readStartdate = self.w.schedule_startdate_enter_lineEdit.text()
                if validation.isValidBirthDate(readStartdate):
                    errorDict["StartDateError"] = True
                else:
                    errorDict["StartDateError"] = False

                readFinishdate = self.w.schedule_finishdate_enter_lineEdit.text()
                if validation.isValidBirthDate(readFinishdate):
                    errorDict["FinishDateError"] = True
                else:
                    errorDict["FinishDateError"] = False

                readTimeschedule = self.w.schedule_timeschedule_enter_lineEdit.text()
                if readTimeschedule:
                    errorDict["TimeScheduleError"] = True
                else:
                    errorDict["TimeScheduleError"] = False

                #list for show errors
                showError = []
                #through this cikle we add errors name into our list(showError)
                for item in errorDict:
                    if errorDict[item] == True:
                        pass
                    else:
                        showError.append(item)

                #if our showError list has one or more items` we can know that we have error and we can use MessageBox
                #else we can know that everything is fine and we can add our data
                if len(showError) >= 1:
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Critical)
                    msg.setText(str(showError))
                    msg.setInformativeText('More information')
                    msg.setWindowTitle("Invalid Syntax")
                    msg.exec_() 
                else:
                   

                    # Adding new empty row
                    rowPosition = self.ui.schedule_tableWidget.rowCount()
                    self.ui.schedule_tableWidget.insertRow(rowPosition)
                    # Connecting to server
                    con = connect(host=Host, user=uName, passwd=Pass, db=DataBase)
                    myCursor = con.cursor()
                    # Transfer data to server
                    
                    myCursor.execute("INSERT INTO schedule(schedule_ID, group_ID, instructor_ID, Subject_ID, audience_ID, learning_type_ID, start_date, finish_date, time_schedule) VALUES({},{},{},{},{},{},'{}','{}','{}')".format(rowPosition+1, group_dict[readGroup], staff_dict[readInstructor], subject_dict[readSubject],  audience_dict[readAudience], lType_dict[readLearningtype], readStartdate, readFinishdate, readTimeschedule))
                    # Confirming new changes in server
                    con.commit()
                    # Closing connection
                    con.close()
                    # Adding new row information
                    self.create_table_widget(rowPosition, 0, str(rowPosition+1), "schedule_tableWidget")
                    self.create_table_widget(rowPosition, 1, str(readGroup), "schedule_tableWidget")
                    self.create_table_widget(rowPosition, 2, str(readInstructor), "schedule_tableWidget") 
                    self.create_table_widget(rowPosition, 3, str(readSubject), "schedule_tableWidget") 
                    self.create_table_widget(rowPosition, 4, str(readAudience), "schedule_tableWidget")
                    self.create_table_widget(rowPosition, 5, str(readLearningtype), "schedule_tableWidget")
                    self.create_table_widget(rowPosition, 6, str(readStartdate), "schedule_tableWidget")
                    self.create_table_widget(rowPosition, 7, str(readFinishdate), "schedule_tableWidget")
                    self.create_table_widget(rowPosition, 8, str(readTimeschedule), "schedule_tableWidget")


                    # Closing entry window
                    self.window.close()
                    # Updating data in program
                    GetData()

            self.w.Schedule_Enter_pushButton.clicked.connect(lambda: OkClicked())


    ### STUDENTS
    def show_students(self):
        for x in range(len(STUDENTS)):
            # Create new row
            rowPosition = self.ui.student_tableWidget.rowCount()
            self.ui.student_tableWidget.insertRow(rowPosition)
            # Create widget

            self.create_table_widget(rowPosition, 0, str(STUDENTS.Student_ID[x]), "student_tableWidget")
            self.create_table_widget(rowPosition, 1, str(STUDENTS.Name[x]), "student_tableWidget")
            self.create_table_widget(rowPosition, 2, str(STUDENTS.Last_Name[x]), "student_tableWidget")
            self.create_table_widget(rowPosition, 3, str(STUDENTS.Patronymic[x]), "student_tableWidget")
            self.create_table_widget(rowPosition, 4, str(STUDENTS.Birth_Date[x]), "student_tableWidget")
            self.create_table_widget(rowPosition, 5, str(STUDENTS.Address[x]), "student_tableWidget")
            self.create_table_widget(rowPosition, 6, str(STUDENTS.Phone_Number[x]), "student_tableWidget")
            self.create_table_widget(rowPosition, 7, str(STUDENTS.Email[x]), "student_tableWidget")
            self.create_table_widget(rowPosition, 8, str(STUDENTS.Passport_ID[x]), "student_tableWidget")
            
        self.ui.student_lineEdit.textChanged.connect(self.findStudent)
        self.ui.student_add_button.clicked.connect(lambda: self.addrow("Student"))
        self.ui.student_replace_button.clicked.connect(lambda: self.Replace("Student"))
        

    ### GROUPS
    def show_groups(self):
        for x in range(len(GROUPS)):
            # Create new row
            rowPosition = self.ui.group_tableWidget.rowCount()
            self.ui.group_tableWidget.insertRow(rowPosition)
            # Create widget
            self.create_table_widget(rowPosition, 0, str(GROUPS.Group_ID[x]), "group_tableWidget")
            self.create_table_widget(rowPosition, 1, str(GROUPS.Title[x]), "group_tableWidget")

        self.ui.group_lineEdit.textChanged.connect(self.findGroup)  
        self.ui.group_add_button.clicked.connect(lambda: self.addrow("Group"))
        self.ui.group_replace_button.clicked.connect(lambda: self.Replace("Group"))


    ### STAFF
    def show_staff(self):
        for x in range(len(STAFF)):
            # Create new row
            rowPosition = self.ui.staff_tableWidget.rowCount()
            self.ui.staff_tableWidget.insertRow(rowPosition)
            # Create widget

            self.create_table_widget(rowPosition, 0, str(STAFF.Staff_ID[x]), "staff_tableWidget")
            self.create_table_widget(rowPosition, 1, str(STAFF.Name[x]), "staff_tableWidget")
            self.create_table_widget(rowPosition, 2, str(STAFF.Last_Name[x]), "staff_tableWidget")
            self.create_table_widget(rowPosition, 3, str(STAFF.Patronymic[x]), "staff_tableWidget")
            self.create_table_widget(rowPosition, 4, str(STAFF.Education[x]), "staff_tableWidget")
            self.create_table_widget(rowPosition, 5, str(STAFF.Address[x]), "staff_tableWidget")
            self.create_table_widget(rowPosition, 6, str(STAFF.Phone_Number[x]), "staff_tableWidget")
            self.create_table_widget(rowPosition, 7, str(STAFF.Email[x]), "staff_tableWidget")
            self.create_table_widget(rowPosition, 8, str(position_ID_dict[STAFF.Position_ID[x]]), "staff_tableWidget")
        
        self.ui.staff_lineEdit.textChanged.connect(self.findStaff)
        self.ui.staff_add_button.clicked.connect(lambda: self.addrow("Staff"))
        self.ui.staff_replace_button.clicked.connect(lambda: self.Replace("Staff"))
        

    ### INSTRUCTOR
    def show_instructor(self):
        for x in range(len(INSTRUCTOR)):
            # Create new row
            rowPosition = self.ui.instructor_tableWidget.rowCount()
            self.ui.instructor_tableWidget.insertRow(rowPosition)
            # Create widget

            self.create_table_widget(rowPosition, 0, str(INSTRUCTOR.Instructor_ID[x]), "instructor_tableWidget")
            self.create_table_widget(rowPosition, 1, str(staff_ID_dict[INSTRUCTOR.Staff_ID[x]]), "instructor_tableWidget")
            self.create_table_widget(rowPosition, 2, str(INSTRUCTOR.Description[x]), "instructor_tableWidget")
            self.create_table_widget(rowPosition, 3, str(INSTRUCTOR.Teaching_Object[x]), "instructor_tableWidget")
        
        self.ui.instructor_lineEdit.textChanged.connect(self.findInstructor)
        self.ui.instructor_add_button.clicked.connect(lambda: self.addrow("Instructor"))
        self.ui.instructor_replace_button.clicked.connect(lambda: self.Replace("Instructor"))


    ### AUDIENCE
    def show_audience(self):
        for x in range(len(AUDIENCE)):
            # Create new row
            rowPosition = self.ui.audience_tableWidget.rowCount()
            self.ui.audience_tableWidget.insertRow(rowPosition)
            # Create widget
            self.create_table_widget(rowPosition, 0, str(AUDIENCE.Audience_ID[x]), "audience_tableWidget")
            self.create_table_widget(rowPosition, 1, str(AUDIENCE.Title[x]), "audience_tableWidget")
            self.create_table_widget(rowPosition, 2, str(AUDIENCE.Seat_Count[x]), "audience_tableWidget")
            self.create_table_widget(rowPosition, 3, str(AUDIENCE.Computer_Count[x]), "audience_tableWidget")
        
        self.ui.audience_lineEdit.textChanged.connect(self.findAudience) 
        self.ui.audience_add_button.clicked.connect(lambda: self.addrow("Audience"))
        self.ui.audience_replace_button.clicked.connect(lambda: self.Replace("Audience"))


    ### CATEGORY
    def show_category(self):
        for x in range(len(CATEGORY)):
            # Create new row
            rowPosition = self.ui.category_tableWidget.rowCount()
            self.ui.category_tableWidget.insertRow(rowPosition)
            # Create widget
            self.create_table_widget(rowPosition, 0, str(CATEGORY.Category_ID[x]), "category_tableWidget")
            self.create_table_widget(rowPosition, 1, str(CATEGORY.Subject_Category[x]), "category_tableWidget")
            
        self.ui.category_lineEdit.textChanged.connect(self.findCategory)
        self.ui.category_add_button.clicked.connect(lambda: self.addrow("Category"))
        self.ui.category_replace_button.clicked.connect(lambda: self.Replace("Category"))
   
   
    ### SUBJECT
    def show_subject(self):
        for x in range(len(SUBJECT)):
            # Create new row
            rowPosition = self.ui.subject_tableWidget.rowCount()
            self.ui.subject_tableWidget.insertRow(rowPosition)
            # Create widget

            self.create_table_widget(rowPosition, 0, str(SUBJECT.Subject_ID[x]), "subject_tableWidget")
            self.create_table_widget(rowPosition, 1, str(category_ID_dict[SUBJECT.Category_ID[x]]), "subject_tableWidget")
            self.create_table_widget(rowPosition, 2, str(SUBJECT.Title[x]), "subject_tableWidget")
            self.create_table_widget(rowPosition, 3, str(SUBJECT.Description[x]), "subject_tableWidget")
            self.create_table_widget(rowPosition, 4, str(SUBJECT.Price[x]), "subject_tableWidget")
            
        self.ui.subject_lineEdit.textChanged.connect(self.findSubject)
        self.ui.subject_add_button.clicked.connect(lambda: self.addrow("Subject"))
        self.ui.subject_replace_button.clicked.connect(lambda: self.Replace("Subject"))

   
    ### SCHEDULE
    def show_schedule(self):
        for x in range(len(SCHEDULE)):
            # Create new row
            rowPosition = self.ui.schedule_tableWidget.rowCount()
            self.ui.schedule_tableWidget.insertRow(rowPosition)
            # Create widget

            self.create_table_widget(rowPosition, 0, str(SCHEDULE.Schedule_ID[x]), "schedule_tableWidget")
            self.create_table_widget(rowPosition, 1, str(group_ID_dict[SCHEDULE.Group_ID[x]]), "schedule_tableWidget")
            self.create_table_widget(rowPosition, 2, str(staff_ID_dict[SCHEDULE.Instructor_ID[x]]), "schedule_tableWidget")
            self.create_table_widget(rowPosition, 3, str(subject_ID_dict[SCHEDULE.Subject_ID[x]]), "schedule_tableWidget")
            self.create_table_widget(rowPosition, 4, str(SCHEDULE.Audience_ID[x]), "schedule_tableWidget")
            self.create_table_widget(rowPosition, 5, str(lType_ID_dict[SCHEDULE.Learning_Type_ID[x]]), "schedule_tableWidget")
            self.create_table_widget(rowPosition, 6, str(SCHEDULE.Start_Date[x]), "schedule_tableWidget")
            self.create_table_widget(rowPosition, 7, str(SCHEDULE.Finish_Date[x]), "schedule_tableWidget")
            self.create_table_widget(rowPosition, 8, str(SCHEDULE.Time_Schedule[x]), "schedule_tableWidget")
            

        self.ui.schedule_lineEdit.textChanged.connect(self.findSchedule)
        self.ui.schedule_add_button.clicked.connect(lambda: self.addrow("Schedule"))
        self.ui.schedule_replace_button.clicked.connect(lambda: self.Replace("Schedule"))


    ### Search function for Student 
    def findStudent(self):
        name = self.ui.student_lineEdit.text().lower()
        for row in range(self.ui.student_tableWidget.rowCount()):
            item = self.ui.student_tableWidget.item(row, 1)
            # if the search i not in the item's text hide the row
            self.ui.student_tableWidget.setRowHidden(row, name not in item.text().lower())


    ### Search function for Group    
    def findGroup(self):
        name = self.ui.group_lineEdit.text().lower()
        for row in range(self.ui.group_tableWidget.rowCount()):
            item = self.ui.group_tableWidget.item(row, 1)
            # if the search i not in the item's text hide the row
            self.ui.group_tableWidget.setRowHidden(row, name not in item.text().lower())


    ### Search function for Staff
    def findStaff(self):
        name = self.ui.staff_lineEdit.text().lower()
        for row in range(self.ui.staff_tableWidget.rowCount()):
            item = self.ui.staff_tableWidget.item(row, 1)
            # if the search i not in the item's text hide the row
            self.ui.staff_tableWidget.setRowHidden(row, name not in item.text().lower())


    ### Search function for Instructor    
    def findInstructor(self):
        name = self.ui.instructor_lineEdit.text().lower()
        for row in range(self.ui.instructor_tableWidget.rowCount()):
            item = self.ui.instructor_tableWidget.item(row, 1)
            # if the search i not in the item's text hide the row
            self.ui.instructor_tableWidget.setRowHidden(row, name not in item.text().lower())


    ### Search function for Audience
    def findAudience(self):
        name = self.ui.audience_lineEdit.text().lower()
        for row in range(self.ui.audience_tableWidget.rowCount()):
            item = self.ui.audience_tableWidget.item(row, 1)
            # if the search i not in the item's text hide the row
            self.ui.audience_tableWidget.setRowHidden(row, name not in item.text().lower())


    ### Search function for Category 
    def findCategory(self):
        name = self.ui.category_lineEdit.text().lower()
        for row in range(self.ui.category_tableWidget.rowCount()):
            item = self.ui.category_tableWidget.item(row, 1)
            # if the search i not in the item's text hide the row
            self.ui.category_tableWidget.setRowHidden(row, name not in item.text().lower())


    ### Search function for Subject 
    def findSubject(self):
        name = self.ui.subject_lineEdit.text().lower()
        for row in range(self.ui.subject_tableWidget.rowCount()):
            item = self.ui.subject_tableWidget.item(row, 2)
            # if the search i not in the item's text hide the row
            self.ui.subject_tableWidget.setRowHidden(row, name not in item.text().lower())


    ### Search function for Schedule
    def findSchedule(self):
        name = self.ui.schedule_lineEdit.text().lower()
        for row in range(self.ui.schedule_tableWidget.rowCount()):
            item = self.ui.schedule_tableWidget.item(row, 1)
            # if the search i not in the item's text hide the row
            self.ui.schedule_tableWidget.setRowHidden(row, name not in item.text().lower())


    ### Side menu buttons styling function
    def applyButtonStyle(self):
        # Reset style for other buttons
        for w in self.ui.menu_frame.findChildren(QPushButton):
            # If button name is not equl to clicked button name
            if w.objectName() != self.sender().objectName():
                # Apply the default style
                w.setStyleSheet("border-bottom: none;")
        # Apply new style to clicked button
        self.sender().setStyleSheet("border-bottom: 2px solid")


    ### Slide left menu function
    def slideLeftMenu(self):
        # Get current left menu width
        width = self.ui.left_menu_content_frame.width()
        # if minimized expand menu
        if width == 50:
            newWidth = 200
        # if maximized restore menu
        else:
            newWidth = 50
        # Animate the transition
        self.animation = QPropertyAnimation(self.ui.left_menu_content_frame, b"minimumWidth") # Animate minimumWidth
        self.animation.setDuration(250)
        self.animation.setStartValue(width) # Start value is the current menu width
        self.animation.setEndValue(newWidth) # End value is the new menu width
        self.animation.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
        self.animation.start()


    ### Add mouse events to the window
    def mousePressEvent(self, event):
        # Get current position of the mouse
        # This value will be used to move the window
        self.clickPosition = event.globalPos()


    ### Update restore button icon on maximizing or restoring
    def restore_or_maximize_window(self):
        if self.isMaximized():
            self.showNormal()
            self.ui.window_restore_button.setIcon(QtGui.QIcon(u"./icons/icons8-maximize-button-32.png"))
        else:
            self.showMaximized()
            self.ui.window_restore_button.setIcon(QtGui.QIcon(u"./icons/icons8-restore-down-48.png"))


  ### add new row 
    def Replace(self,name):
        if name == "Student":            
            # Calling replace window
            self.window = QtWidgets.QMainWindow()
            self.w = Ui_Student_Replace_window()
            self.w.setupUi(self.window)
            self.window.show()

            def OkClicked():
                #Dictionary for key(nameerror):value(True or false)
                errorDict = dict()
                # Reading data from line and doing validation
                readName = self.w.student_replace_name_lineEdit.text()
                if validation.isValidName(readName):
                    errorDict["NameError"] = True
                else:
                    errorDict["NameError"] = False
                  
                readLast_name = self.w.student_replace_LName_lineEdit.text()
                if validation.isValidName(readLast_name):
                    errorDict["LastNameError"] = True
                else:
                    errorDict["LastNameError"] = False

                readPatronymic = self.w.student_replace_patro_lineEdit.text()
                if validation.isValidName(readPatronymic):
                    errorDict["PatronymicError"] = True
                else:
                    errorDict["PatronymicError"] = False

                readBirthDate = self.w.student_replace_BDate_lineEdit.text()
                if validation.isValidBirthDate(readBirthDate):
                    errorDict["BirthDayError"] = True
                else:
                    errorDict["BirthDayError"] = False

                readAddress = self.w.student_replace_address_lineEdit.text()

                readPhone_number = self.w.student_replace_PNumber_lineEdit.text()
                if validation.isValidPhoneNumber(readPhone_number):
                    errorDict["PhoneNumberError"] = True
                else:
                    errorDict["PhoneNumberError"] = False

                readEmail = self.w.student_replace_email_lineEdit.text()
                if validation.isValidEmail(readEmail):
                    errorDict["EmailError"] = True
                else:
                    errorDict["EmailError"] = False

                readPassport_ID = self.w.student_replace_passportlineEdit.text()
                readStudent_ID = self.w.student_replace_ID_comboBox.currentText()
                #List for show errors
                showError = []
                #through this cikle we add errors name into our list(showError)
                for item in errorDict:
                    if errorDict[item] == True:
                        pass
                    else:
                        showError.append(item)

                #if our showError list has one or more items` we can know that we have error and we can use MessageBox
                #else we can know that everything is fine and we can add our data
                if len(showError) >= 1:
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Critical)
                    msg.setText(str(showError))
                    msg.setWindowTitle("Invalid Syntax")
                    msg.exec_()
                else:
                    # Connecting to server
                    con = connect(host=Host, user=uName, passwd=Pass, db=DataBase)
                    myCursor = con.cursor()
                    # Transfer data to server
                    myCursor.execute(f"UPDATE  student SET name='{readName}', last_name='{readLast_name}', patronymic='{readPatronymic}',"
                                     f" birth_date='{readBirthDate}', address='{readAddress}', phone_number='{readPhone_number}',"
                                     f" email='{readEmail}',passport_ID='{readPassport_ID}' where student_ID='{readStudent_ID}'")
                    # Confirming new changes in server
                    con.commit()
                    # Closing connection
                    con.close()
                    self.window.close()
                    # Updating data in program
                    rowPosition=self.w.student_replace_ID_comboBox.currentText() 
                    rowPosition=int(rowPosition) 
                    self.create_table_widget(rowPosition-1, 0, str(rowPosition), "student_tableWidget")
                    self.create_table_widget(rowPosition-1, 1, str(readName), "student_tableWidget")
                    self.create_table_widget(rowPosition-1, 2, str(readLast_name), "student_tableWidget") 
                    self.create_table_widget(rowPosition-1, 3, str(readPatronymic), "student_tableWidget")
                    self.create_table_widget(rowPosition-1, 4, str(readBirthDate), "student_tableWidget")
                    self.create_table_widget(rowPosition-1, 5, str(readAddress), "student_tableWidget")
                    self.create_table_widget(rowPosition-1, 6, str(readPhone_number), "student_tableWidget")              
                    self.create_table_widget(rowPosition-1, 7, str(readEmail), "student_tableWidget")
                    self.create_table_widget(rowPosition-1, 8, str(readPassport_ID), "student_tableWidget")
                    #self.window.close()
                    GetData()

            #Navigate  ok button
            self.w.student_replace_pushButton.clicked.connect(lambda: OkClicked())

        elif name == "Group":
            # Calling replace window
            self.window = QtWidgets.QMainWindow()
            self.w = Ui_Group_Replace_Window()
            self.w.setupUi(self.window)
            self.window.show()

            def OkClicked():
                # Dictionary for key(nameerror):value(True or false)
                errorDict = dict()
                # Reading data from line and doing validation
                readData = self.w.group_rename_title_line.text()
                readGroup_ID = self.w.group_rename_id_combo_box.currentText()
                if readData:
                    if readData.isdigit():
                        errorDict["TitleError"] = False
                    else:
                        errorDict["TitleError"] = True
                else:
                    errorDict["TitleError"] = False

                # List for show errors
                showError = []
                # through this cikle we add errors name into our list(showError)
                for item in errorDict:
                    if errorDict[item] == True:
                        pass
                    else:
                        showError.append(item)

                # if our showError list has one or more items` we can know that we have error and we can use MessageBox
                # else we can know that everything is fine and we can add our data
                if len(showError) >= 1:
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Critical)
                    msg.setText(str(showError))
                    msg.setInformativeText('More information')
                    msg.setWindowTitle("Invalid Syntax")
                    msg.exec_()
                else:
                    # Connecting to server
                    con = connect(host=Host, user=uName, passwd=Pass, db=DataBase)
                    myCursor = con.cursor()
                    # Transfer data to server
                    myCursor.execute(f"UPDATE  groupp SET title='{readData}' where group_ID='{readGroup_ID}'")
                    # Confirming new changes in server
                    con.commit()
                    # Closing connection
                    con.close()
                    self.window.close()
                    # Updating data in program
                    rowPosition = self.w.group_rename_id_combo_box.currentText()
                    rowPosition = int(rowPosition)
                    self.create_table_widget(rowPosition-1, 0, str(rowPosition), "group_tableWidget")
                    self.create_table_widget(rowPosition-1, 1, str(readData), "group_tableWidget")
                    # Updating data in program
                    GetData()

                # Navigate  ok button
            self.w.pushButton.clicked.connect(lambda: OkClicked())

        elif name == "Staff":
            # Calling replace window
            self.window = QtWidgets.QMainWindow()
            self.w = Ui_Staff_Replace_Window()
            self.w.setupUi(self.window)
            self.window.show()

            def OkClicked():
                    # Dictionary for key(nameerror):value(True or false)
                    errorDict = dict()
                    # Reading data from line and doing validation
                    readName = self.w.staff_name_replace_lineEdit.text()

                    if validation.isValidName(readName):
                        errorDict["NameError"] = True
                    else:
                        errorDict["NameError"] = False

                    readLast_name = self.w.staff_lastname_replace_lineEdit.text()
                    if validation.isValidName(readLast_name):
                        errorDict["LastNameError"] = True
                    else:
                        errorDict["LastNameError"] = False

                    readPatronymic = self.w.staff_patronymic_replace_lineEdit.text()
                    if validation.isValidName(readPatronymic):
                        errorDict["PatronymicError"] = True
                    else:
                        errorDict["PatronymicError"] = False

                    readEducation = self.w.staff_education_replace_lineEdit.text()

                    readAddress = self.w.staff_address_replace_lineEdit.text()

                    readPhone_number = self.w.staff_phonenumber_replace_lineEdit.text()
                    if validation.isValidPhoneNumber(readPhone_number):
                        errorDict["PhoneNumberError"] = True
                    else:
                        errorDict["PhoneNumberError"] = False

                    readEmail = self.w.staff_email_entstaff_address_replace_lineEditer_lineEdit.text()
                    if validation.isValidEmail(readEmail):
                        errorDict["EmailError"] = True
                    else:
                        errorDict["EmailError"] = False

                    readPosition_ID = self.w.staff_position_replace_comboBox.currentText()
                    readStaff_ID = self.w.staff_id_replace_comboBox.currentText()
                    # List for show errors
                    showError = []
                    # through this cikle we add errors name into our list(showError)
                    for item in errorDict:
                        if errorDict[item] == True:
                            pass
                        else:
                            showError.append(item)

                    # if our showError list has one or more items` we can know that we have error and we can use MessageBox
                    # else we can know that everything is fine and we can add our data
                    if len(showError) >= 1:
                        msg = QMessageBox()
                        msg.setIcon(QMessageBox.Critical)
                        msg.setText(str(showError))
                        msg.setInformativeText('More information')
                        msg.setWindowTitle("Invalid Syntax")
                        msg.exec_()
                    else:
                        # Connecting to server
                        con = connect(host=Host, user=uName, passwd=Pass, db=DataBase)
                        myCursor = con.cursor()
                        # Transfer data to server
                        myCursor.execute(f"UPDATE  staff SET name='{readName}', last_name='{readLast_name}',"
                                         f" patronymic='{readPatronymic}', education='{readEducation}',"
                                         f" address='{readAddress}', phone_number='{readPhone_number}', email='{readEmail}',"
                                         f" position_ID='{position_dict[readPosition_ID]}' where staff_ID='{readStaff_ID}'")
                        # Confirming new changes in server
                        con.commit()
                        # Closing connection
                        con.close()
                        # Closing entry window
                        self.window.close()
                        # Updating data in program
                        rowPosition = self.w.staff_id_replace_comboBox.currentText()
                        rowPosition = int(rowPosition)
                        self.create_table_widget(rowPosition-1, 0, str(rowPosition), "staff_tableWidget")
                        self.create_table_widget(rowPosition-1, 1, str(readName), "staff_tableWidget")
                        self.create_table_widget(rowPosition-1, 2, str(readLast_name), "staff_tableWidget") 
                        self.create_table_widget(rowPosition-1, 3, str(readPatronymic), "staff_tableWidget")
                        self.create_table_widget(rowPosition-1, 4, str(readEducation), "staff_tableWidget")
                        self.create_table_widget(rowPosition-1, 5, str(readAddress), "staff_tableWidget")
                        self.create_table_widget(rowPosition-1, 6, str(readPhone_number), "staff_tableWidget")              
                        self.create_table_widget(rowPosition-1, 7, str(readEmail), "staff_tableWidget")
                        self.create_table_widget(rowPosition-1, 8, str(position_dict[readPosition_ID]), "staff_tableWidget")
                        # Updating data in program
                        GetData()

                # Navigate  ok button
            self.w.Staff_Replace_pushButton.clicked.connect(lambda: OkClicked())

        elif name == "Instructor":
            # Calling replace window
            self.window = QtWidgets.QMainWindow()
            self.w = Ui_Instructor_Replace_Window()
            self.w.setupUi(self.window)
            self.window.show()


            def OkClicked():
                # Reading data from line
                readStaff_ID = self.w.instructor_rename_staff_id_combo_box.currentText()
                readDescription = self.w.instructor_rename_description_line.text()
                readTeaching_object = self.w.instructor_rename_teaching_object_line.text()
                readInstructor_ID = self.w.instructor_rename_id_combo_box.currentText()
                # Connecting to server
                con = connect(host=Host, user=uName, passwd=Pass, db=DataBase)
                myCursor = con.cursor()
                # Transfer data to server
                myCursor.execute(f"UPDATE  instructor SET staff_ID={staff_dict[readStaff_ID]},"
                                 f" description='{readDescription}',"
                                 f" teaching_object='{readTeaching_object}' where instructor_ID={readInstructor_ID}")
                # Confirming new changes in server
                con.commit()
                # Closing connection
                con.close()
                # Closing entry window
                self.window.close()
                # Updating data in program
                rowPosition = self.w.instructor_rename_id_combo_box.currentText()
                rowPosition = int(rowPosition)
                self.create_table_widget(rowPosition-1, 0, str(rowPosition), "instructor_tableWidget")
                self.create_table_widget(rowPosition-1, 1, str(staff_dict[readStaff_ID]), "instructor_tableWidget")
                self.create_table_widget(rowPosition-1, 2, str(readDescription), "instructor_tableWidget") 
                self.create_table_widget(rowPosition-1, 3, str(readTeaching_object), "instructor_tableWidget") 
                # Updating data in program
                GetData()
                
            # Navigate  ok button
            self.w.pushButton.clicked.connect(lambda: OkClicked())

        elif name == "Audience":
            # Calling replace window
            self.window = QtWidgets.QMainWindow()
            self.w = Ui_Audience_Replace_Window()
            self.w.setupUi(self.window)
            self.window.show()

            def OkClicked():
                #Dictionary for key(nameerror):value(True or false)
                errorDict = dict()
                # Reading data from line and doing validation
                readTitle = self.w.audience_title_replace_lineEdit.text()
                if readTitle:
                    errorDict["TitleError"] = True
                else:
                    errorDict["TitleError"] = False
                  
                readSeatCount = self.w.audience_seatCount_replace_lineEdit.text()
                if readSeatCount.isnumeric and "." not in readSeatCount:
                    errorDict["SeatCountError"] = True
                else:
                    errorDict["SeatCountError"] = False

                readCompCount = self.w.audience_camputer_count_replace_lineEdit.text()
                if readCompCount.isnumeric and "." not in readCompCount:
                    errorDict["ComputerCountError"] = True
                else:
                    errorDict["ComputerCountError"] = False

                readAudience_ID = self.w.audience_ID_replace_comboBox.currentText()
                #List for show errors
                showError = []
                #through this cikle we add errors name into our list(showError)
                for item in errorDict:
                    if errorDict[item] == True:
                        pass
                    else:
                        showError.append(item)

                #if our showError list has one or more items` we can know that we have error and we can use MessageBox
                #else we can know that everything is fine and we can add our data
                if len(showError) >= 1:
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Critical)
                    msg.setText(str(showError))
                    msg.setWindowTitle("Invalid Syntax")
                    msg.exec_()
                else:
                    # Connecting to server
                    con = connect(host=Host, user=uName, passwd=Pass, db=DataBase)
                    myCursor = con.cursor()
                    # Transfer data to server
                    myCursor.execute(f"UPDATE audience SET  title='{readTitle}', seat_count='{readSeatCount}',"
                                     f" computer_count='{readCompCount}' WHERE audience_ID={readAudience_ID}")
                    # Confirming new changes in server
                    con.commit()
                    # Closing connection
                    con.close()
                    self.window.close()
                    # Finding position of changed data
                    for i in range(len(audience_dict)):
                        if AUDIENCE.Audience_ID[i] == int(readAudience_ID):
                            rowPosition = i
                            break
                        
                    # Updating data in program
                    self.create_table_widget(rowPosition, 0, str(readAudience_ID), "audience_tableWidget")
                    self.create_table_widget(rowPosition, 1, str(readTitle), "audience_tableWidget")
                    self.create_table_widget(rowPosition, 2, str(readSeatCount), "audience_tableWidget") 
                    self.create_table_widget(rowPosition, 3, str(readCompCount), "audience_tableWidget")
                    #self.window.close()
                    GetData()

            #Navigate  ok button
            self.w.audience_replace_pushButton.clicked.connect(lambda: OkClicked())

        elif name == "Category":
            # Calling replace window
            self.window = QtWidgets.QMainWindow()
            self.w = Ui_Category_Replace_Window()
            self.w.setupUi(self.window)
            self.window.show()

            def OkClicked():
                #Dictionary for key(nameerror):value(True or false)
                errorDict = dict()
                # Reading data from line and doing validation
                readSubjectCategory = self.w.category_subjectCategory_replace_lineEdit.text()
                if readSubjectCategory.isalpha and readSubjectCategory:
                    errorDict["SubjectCategoryError"] = True
                else:
                    errorDict["SubjectCategoryError"] = False

                readCategory_ID = self.w.category_ID_replace_comboBox.currentText()
                #List for show errors
                showError = []
                #through this cikle we add errors name into our list(showError)
                for item in errorDict:
                    if errorDict[item] == True:
                        pass
                    else:
                        showError.append(item)

                #if our showError list has one or more items` we can know that we have error and we can use MessageBox
                #else we can know that everything is fine and we can add our data
                if len(showError) >= 1:
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Critical)
                    msg.setText(str(showError))
                    msg.setWindowTitle("Invalid Syntax")
                    msg.exec_()
                else:
                    # Connecting to server
                    con = connect(host=Host, user=uName, passwd=Pass, db=DataBase)
                    myCursor = con.cursor()
                    # Transfer data to server
                    myCursor.execute(f"UPDATE category SET  subject_category='{readSubjectCategory}' WHERE category_ID={readCategory_ID}")
                    # Confirming new changes in server
                    con.commit()
                    # Closing connection
                    con.close()
                    self.window.close()                        
                    # Updating data in program
                    self.create_table_widget(int(readCategory_ID) - 1, 1, str(readSubjectCategory), "category_tableWidget")
                    #self.window.close()
                    GetData()

            #Navigate  ok button
            self.w.category_replace_pushButton.clicked.connect(lambda: OkClicked())
            
        elif name == "Subject":
            # Calling replace window
            self.window = QtWidgets.QMainWindow()
            self.w = Ui_Subject_Replace_Window()
            self.w.setupUi(self.window)
            self.window.show()

            def OkClicked():
                #Dictionary for key(nameerror):value(True or false)
                errorDict = dict()
                # Reading data from line and doing validation
                readCategoryTitle = self.w.subjects_rename_category_id_combo_box.currentText()

                readTitle = self.w.subject_rename_title_line.text()
                if readTitle:
                    errorDict["TitleError"] = True
                else:
                    errorDict["TitleError"] = False
                
                readDescription = self.w.subjects_rename_description_line.text()
                if readDescription:
                    errorDict["DescriptionError"] = True
                else:
                    errorDict["DescriptionError"] = False

                readPrice = self.w.subject_rename_price_line.text()
                if validation.isValidPrice(readPrice):
                    errorDict["PriceError"] = True
                else:
                    errorDict["PriceError"] = False

                readSubject_ID = self.w.subject_rename_id_combo_box.currentText()
                #List for show errors
                showError = []
                #through this cikle we add errors name into our list(showError)
                for item in errorDict:
                    if errorDict[item] == True:
                        pass
                    else:
                        showError.append(item)

                #if our showError list has one or more items` we can know that we have error and we can use MessageBox
                #else we can know that everything is fine and we can add our data
                if len(showError) >= 1:
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Critical)
                    msg.setText(str(showError))
                    msg.setWindowTitle("Invalid Syntax")
                    msg.exec_()
                else:
                    # Connecting to server
                    con = connect(host=Host, user=uName, passwd=Pass, db=DataBase)
                    myCursor = con.cursor()
                    # Transfer data to server
                    myCursor.execute(f"UPDATE subject SET  category_ID={category_dict[readCategoryTitle]},"
                                     f" title='{readTitle}', description='{readDescription}',"
                                     f" price={readPrice} WHERE subject_ID={readSubject_ID}")
                    # Confirming new changes in server
                    con.commit()
                    # Closing connection
                    con.close()
                    self.window.close()
                        
                    # Updating data in program
                    self.create_table_widget(int(readSubject_ID) - 1, 1, str(readCategoryTitle), "subject_tableWidget")
                    self.create_table_widget(int(readSubject_ID) - 1, 2, str(readTitle), "subject_tableWidget")
                    self.create_table_widget(int(readSubject_ID) - 1, 3, str(readDescription), "subject_tableWidget")
                    self.create_table_widget(int(readSubject_ID) - 1, 4, str(readPrice), "subject_tableWidget")
                    #self.window.close()
                    GetData()

            #Navigate  ok button
            self.w.pushButton.clicked.connect(lambda: OkClicked())

        elif name == "Schedule":
            # Calling replace window
            self.window = QtWidgets.QMainWindow()
            self.w = Ui_Schedule_Replace_Window()
            self.w.setupUi(self.window)
            self.window.show()

            def OkClicked():
                #Dictionary for key(nameerror):value(True or false)
                errorDict = dict()
                # Reading data from line and doing validation
                readGroupTitle = self.w.schedule_group_replace_comboBox.currentText()
                readInstructorTitle = self.w.schedule_instructor_replace_comboBox.currentText()
                readSubjectTitle = self.w.schedule_subject_replace_comboBox.currentText()
                readAudienceTitle = self.w.schedule_audience_replace_comboBox.currentText()
                readLType = self.w.schedule_learningtype_replace_comboBox.currentText()

                readStartDate = self.w.schedule_startdate_replace_lineEdit.text()
                if validation.isValidBirthDate(readStartDate):
                    errorDict["StartDateError"] = True
                else:
                    errorDict["StartDateError"] = False
                
                readFinishDate = self.w.schedule_finishdate_replace_lineEdit.text()
                if validation.isValidBirthDate(readFinishDate):
                    errorDict["FinishDateError"] = True
                else:
                    errorDict["FinishDateError"] = False

                readTimeSchdule = self.w.schedule_timeschedule_replace_lineEdit.text()
                if readTimeSchdule:
                    errorDict["TimeScheduleError"] = True
                else:
                    errorDict["TimeScheduleError"] = False

                readSchedule_ID = self.w.schedule_learningtype_replace_comboBox_2.currentText()
                #List for show errors
                showError = []
                #through this cikle we add errors name into our list(showError)
                for item in errorDict:
                    if errorDict[item] == True:
                        pass
                    else:
                        showError.append(item)

                #if our showError list has one or more items` we can know that we have error and we can use MessageBox
                #else we can know that everything is fine and we can add our data
                if len(showError) >= 1:
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Critical)
                    msg.setText(str(showError))
                    msg.setWindowTitle("Invalid Syntax")
                    msg.exec_()
                else:
                    # Connecting to server
                    con = connect(host=Host, user=uName, passwd=Pass, db=DataBase)
                    myCursor = con.cursor()
                    # Transfer data to server
                    myCursor.execute(f"UPDATE schedule SET group_ID={group_dict[readGroupTitle]},"
                                     f" instructor_ID={staff_dict[readInstructorTitle]},"
                                     f" subject_ID={subject_dict[readSubjectTitle]},"
                                     f" audience_ID={audience_dict[readAudienceTitle]},"
                                     f" learning_type_ID={lType_dict[readLType]},"
                                     f" start_date='{readStartDate}', finish_date='{readFinishDate}',"
                                     f" time_schedule='{readTimeSchdule}' WHERE schedule_ID={readSchedule_ID}")
                    # Confirming new changes in server
                    con.commit()
                    # Closing connection
                    con.close()
                    self.window.close()
                        
                    # Updating data in program
                    self.create_table_widget(int(readSchedule_ID) - 1, 1, str(readGroupTitle), "schedule_tableWidget")
                    self.create_table_widget(int(readSchedule_ID) - 1, 2, str(readInstructorTitle), "schedule_tableWidget")
                    self.create_table_widget(int(readSchedule_ID) - 1, 3, str(readSubjectTitle), "schedule_tableWidget")
                    self.create_table_widget(int(readSchedule_ID) - 1, 4, str(audience_dict[readAudienceTitle]), "schedule_tableWidget")
                    self.create_table_widget(int(readSchedule_ID) - 1, 5, str(readLType), "schedule_tableWidget")
                    self.create_table_widget(int(readSchedule_ID) - 1, 6, str(readStartDate), "schedule_tableWidget")
                    self.create_table_widget(int(readSchedule_ID) - 1, 7, str(readFinishDate), "schedule_tableWidget")
                    self.create_table_widget(int(readSchedule_ID) - 1, 8, str(readTimeSchdule), "schedule_tableWidget")
                    #self.window.close()
                    GetData()

            #Navigate  ok button
            self.w.Schedule_Replace_pushButton.clicked.connect(lambda: OkClicked())


#####################################################
##                 EXECUTE APP                     ##
#####################################################
if __name__ == "__main__":
    checkIfModulsAreExisting()
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    LogIn = Ui_Form()
    LogIn.setupUi(Form)
    Form.setWindowIcon(QtGui.QIcon("./icons/icons8-logo-48.png"))
    Form.show()
    sys.exit(app.exec_())
