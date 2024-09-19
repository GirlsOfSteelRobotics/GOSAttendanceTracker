# -----------------------------------------------------------------------
# IMPORTS
# -----------------------------------------------------------------------

import sys

import gspread

from PyQt6.QtWidgets import (
    QMainWindow,
    QApplication,
    QPushButton,
    QWidget,
    QTabWidget,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QLineEdit,
    QLabel,
    QApplication,
)

from PyQt6.QtGui import QPixmap, QFont

from PyQt6.QtCore import Qt

import datetime as dt


# -----------------------------------------------------------------------
# GLOBAL VARIABLES
# -----------------------------------------------------------------------

SPREADSHEET_KEY = "1ztlyayX_A59oDQQsRPfWNKSZ-efkdWKgML-J9WtB66s"
WIDTH = 800
HEIGHT = 400


# -----------------------------------------------------------------------
# USER INTERFACE CODE
# -----------------------------------------------------------------------
class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = "Girls of Steel Meeting Login"
        self.left = 0
        self.top = 0
        self.width = WIDTH
        self.height = HEIGHT
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setStyleSheet("background-color: #ff837a; font-size: 20pt;")
        self.showMaximized()

        self.table_widget = MyTableWidget(self)
        self.setCentralWidget(self.table_widget)

        self.show()


class MyTableWidget(QWidget):

    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)

        # Initialize tab screen
        self.tabs = QTabWidget()
        self.tab_log_attendance = QWidget()
        self.tab_lookup_fob = QWidget()
        self.tab3 = QWidget()
        self.tab_scra_visitor_log = QWidget()
        self.tab_field_builders = QWidget()
        self.tabs.resize(WIDTH, HEIGHT)

        # Add tabs
        self.tabs.addTab(self.tab_log_attendance, "Log Attendance")
        self.tabs.addTab(self.tab_scra_visitor_log, "SCRA Visitor Log")
        self.tabs.addTab(self.tab_field_builders, "Field Builders Login")
        self.tabs.addTab(self.tab_lookup_fob, "Lookup Fob Number")

        # --------------------
        # Tab 1 Content
        # --------------------
        self.tab_log_attendance.layout = QGridLayout(self)
        self.tab_log_attendance.setLayout(self.tab_log_attendance.layout)
        self.tab_log_attendance.setStyleSheet("background-color: #bad3fe;")

        self.logo = QLabel(self)
        self.pixmap = QPixmap("logo3.png")
        self.logo.setPixmap(self.pixmap)
        self.logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.tab_log_attendance.layout.addWidget(self.logo, 0, 1)

        self.header = QLabel("Log your attendance at today's GoS meeting!")
        self.header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        headerFont = QFont()
        headerFont.setBold(True)
        self.header.setFont(headerFont)
        self.header.setStyleSheet("font-size: 35pt;")
        self.tab_log_attendance.layout.addWidget(self.header, 1, 1)

        self.instructions = QLabel(
            "Tap your fob to the reader to log in, or type in the number associated with your fob.\nIt may take a second or two for the log in to process."
        )
        self.instructions.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.instructions.setStyleSheet("font-size: 25pt;")
        self.tab_log_attendance.layout.addWidget(self.instructions, 2, 1)

        self.inputArea = QWidget()
        self.inputArea.layout = QGridLayout(self)
        self.inputArea.setLayout(self.inputArea.layout)
        self.tab_log_attendance.layout.addWidget(self.inputArea, 3, 1)

        self.input = QLineEdit()
        self.input.setFixedWidth(250)
        self.input.setFixedHeight(40)
        self.input.setStyleSheet("font-size: 25pt;")
        self.input.returnPressed.connect(self.login)
        self.input.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.inputArea.layout.addWidget(self.input, 0, 1)

        self.loginButton = QPushButton("Login")
        self.loginButton.setStyleSheet("font-size: 25pt;")
        self.loginButton.clicked.connect(self.login)
        self.inputArea.layout.addWidget(self.loginButton, 1, 1)

        self.clearButton = QPushButton("Clear")
        self.clearButton.setStyleSheet("font-size: 25pt;")
        self.clearButton.clicked.connect(self.input.clear)
        self.clearButton.clicked.connect(lambda: self.message.setText(""))
        self.inputArea.layout.addWidget(self.clearButton, 2, 1)

        self.message = QLabel("")
        self.message.setStyleSheet("font-size: 25pt;")
        self.message.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.tab_log_attendance.layout.addWidget(self.message, 4, 1)

        # --------------------
        # Tab 2 Content
        # --------------------

        self.tab_lookup_fob.layout = QGridLayout(self)
        self.tab_lookup_fob.setLayout(self.tab_lookup_fob.layout)
        self.tab_lookup_fob.setStyleSheet("background-color: #bad3fe;")  # ffc3bf;")

        self.header2 = QLabel("Forgot your fob? Not a problem!")
        self.header2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.header2.setFont(headerFont)
        self.header2.setStyleSheet("font-size: 35pt;")
        self.tab_lookup_fob.layout.addWidget(self.header2, 1, 1)

        self.instructions2 = QLabel("Type your full name below. (Ex: Rosie Riveter)")
        self.instructions2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.instructions2.setStyleSheet("font-size: 25pt;")
        self.tab_lookup_fob.layout.addWidget(self.instructions2, 2, 1)

        self.inputArea2 = QWidget()
        self.inputArea2.layout = QGridLayout(self)
        self.inputArea2.setLayout(self.inputArea2.layout)
        self.tab_lookup_fob.layout.addWidget(self.inputArea2, 3, 1)

        self.input2 = QLineEdit()
        self.input2.setFixedWidth(250)
        self.input2.setFixedHeight(40)
        self.input2.returnPressed.connect(self.searchID)
        # self.input.setStyleSheet("height: 100px;")
        self.input2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.input2.setStyleSheet("font-size: 25pt;")
        self.inputArea2.layout.addWidget(self.input2, 0, 1)

        self.searchButton = QPushButton("Search")
        self.searchButton.clicked.connect(self.searchID)
        self.searchButton.setStyleSheet("font-size: 25pt;")
        self.inputArea2.layout.addWidget(self.searchButton, 1, 1)

        self.clearButton2 = QPushButton("Clear")
        self.clearButton2.clicked.connect(self.input2.clear)
        self.clearButton2.clicked.connect(lambda: self.message2.setText(""))
        self.clearButton2.setStyleSheet("font-size: 25pt;")
        self.inputArea2.layout.addWidget(self.clearButton2, 2, 1)

        self.message2 = QLabel("")
        self.message2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.message2.setStyleSheet("font-size: 25pt;")
        self.message2.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextSelectableByMouse
        )
        self.tab_lookup_fob.layout.addWidget(self.message2, 4, 1)

        # --------------------
        # Tab 3 Content
        # --------------------

        self.tab3.layout = QGridLayout(self)
        self.tab3.setLayout(self.tab3.layout)
        self.tab3.setStyleSheet("background-color: #bad3fe;")  # ffffff;")

        self.header3 = QLabel("Found a lost fob, but don't know whose it is?")
        self.header3.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.header3.setFont(headerFont)
        self.header3.setStyleSheet("font-size: 35pt;")
        self.tab3.layout.addWidget(self.header3, 1, 1)

        self.instructions3 = QLabel("Scan the fob and find out who it belongs to!")
        self.instructions3.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.instructions3.setStyleSheet("font-size: 25pt;")
        self.tab3.layout.addWidget(self.instructions3, 2, 1)

        self.inputArea3 = QWidget()
        self.inputArea3.layout = QGridLayout(self)
        self.inputArea3.setLayout(self.inputArea3.layout)
        self.tab3.layout.addWidget(self.inputArea3, 3, 1)

        self.input3 = QLineEdit()
        self.input3.setFixedWidth(250)
        self.input3.setFixedHeight(40)
        self.input3.setStyleSheet("font-size: 25pt;")
        self.input3.returnPressed.connect(self.identifyFob)
        self.input3.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.inputArea3.layout.addWidget(self.input3, 0, 1)

        self.searchButton3 = QPushButton("Search")
        self.searchButton3.clicked.connect(self.identifyFob)
        self.searchButton3.setStyleSheet("font-size: 25pt;")
        self.inputArea3.layout.addWidget(self.searchButton3, 1, 1)

        self.clearButton3 = QPushButton("Clear")
        self.clearButton3.clicked.connect(self.input3.clear)
        self.clearButton3.setStyleSheet("font-size: 25pt;")
        self.inputArea3.layout.addWidget(self.clearButton3, 2, 1)

        self.message3 = QLabel("")
        self.message3.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.message3.setStyleSheet("font-size: 25pt;")
        self.tab3.layout.addWidget(self.message3, 4, 1)

        # --------------------
        # Tab 4 Content
        # --------------------
        self.tab_scra_visitor_log.layout = QHBoxLayout(self)
        self.tab_scra_visitor_log.setLayout(self.tab_scra_visitor_log.layout)
        self.tab_scra_visitor_log.setStyleSheet("background-color: #fceb7c;")

        ##        self.label4 = QLabel("Page Under Construction")
        ##        self.label4.setAlignment(Qt.AlignmentFlag.AlignCenter)
        ##        self.tab4.layout.addWidget(self.label4)

        self.logo4 = QLabel(self)
        self.pixmap4 = QPixmap("SCRA2.png")
        self.logo4.setPixmap(self.pixmap4)
        self.logo4.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.tab_scra_visitor_log.layout.addWidget(self.logo4)

        self.signinBox4 = QWidget()
        self.signinBox4.layout = QGridLayout(self)
        self.signinBox4.setLayout(self.signinBox4.layout)
        self.tab_scra_visitor_log.layout.addWidget(self.signinBox4)

        self.header4 = QLabel("SCRA Open Meeting Sign-In")
        self.header4.setAlignment(Qt.AlignmentFlag.AlignCenter)
        headerFont4 = QFont()
        headerFont4.setBold(True)
        self.header4.setFont(headerFont)
        self.header4.setStyleSheet("font-size: 35pt;")
        self.signinBox4.layout.addWidget(self.header4, 0, 0)

        self.inputArea4 = QWidget()
        self.inputArea4.layout = QGridLayout(self)
        self.inputArea4.setLayout(self.inputArea4.layout)
        self.signinBox4.layout.addWidget(self.inputArea4, 1, 0)

        self.instructions4a = QLabel("Name:")
        self.instructions4a.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.instructions4a.setStyleSheet("font-size: 25pt;")
        self.inputArea4.layout.addWidget(self.instructions4a, 0, 1)

        self.instructions4b = QLabel("Team Number:")
        self.instructions4b.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.instructions4b.setStyleSheet("font-size: 25pt;")
        self.inputArea4.layout.addWidget(self.instructions4b, 1, 1)

        self.input4a = QLineEdit()
        self.input4a.setFixedWidth(250)
        self.input4a.setFixedHeight(40)
        self.input4a.setStyleSheet("font-size: 25pt;")
        self.input4a.returnPressed.connect(self.logVisit)
        self.input4a.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.inputArea4.layout.addWidget(self.input4a, 0, 2)

        self.input4b = QLineEdit()
        self.input4b.setFixedWidth(250)
        self.input4b.setFixedHeight(40)
        self.input4b.setStyleSheet("font-size: 25pt;")
        self.input4b.returnPressed.connect(self.logVisit)
        self.input4b.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.inputArea4.layout.addWidget(self.input4b, 1, 2)

        self.loginButton4 = QPushButton("Submit")
        self.loginButton4.setFixedWidth(250)
        self.loginButton4.setStyleSheet("font-size: 25pt;")
        self.loginButton4.clicked.connect(self.logVisit)
        self.signinBox4.layout.addWidget(self.loginButton4, 2, 1)

        self.clearButton4 = QPushButton("Clear")
        self.clearButton4.setFixedWidth(250)
        self.clearButton4.setStyleSheet("font-size: 25pt;")
        self.clearButton4.clicked.connect(self.input.clear)
        self.clearButton4.clicked.connect(lambda: self.message4.setText(""))
        self.signinBox4.layout.addWidget(self.clearButton4, 4, 1)

        self.message4 = QLabel("")
        self.message4.setStyleSheet("font-size: 25pt;")
        self.message4.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.signinBox4.layout.addWidget(self.message4, 5, 0)

        # --------------------
        # Tab 5 Content
        # --------------------
        self.tab_field_builders.layout = QGridLayout(self)
        self.tab_field_builders.setLayout(self.tab_field_builders.layout)
        self.tab_field_builders.setStyleSheet("background-color: #bad3fe;")

        self.logo5 = QLabel(self)
        self.pixmap5 = QPixmap("chargedUp.png")
        self.logo5.setPixmap(self.pixmap5)
        self.logo5.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.tab_field_builders.layout.addWidget(self.logo5, 0, 1)

        self.header5 = QLabel("\nWelcome, Practice Field Builder!")
        self.header5.setAlignment(Qt.AlignmentFlag.AlignCenter)
        headerFont5 = QFont()
        headerFont5.setBold(True)
        self.header5.setFont(headerFont5)
        self.header5.setStyleSheet("font-size: 35pt;")
        self.tab_field_builders.layout.addWidget(self.header5, 1, 1)

        self.instructions5 = QLabel(
            "Type your name below to log your presense here today."
        )
        self.instructions5.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.instructions5.setStyleSheet("font-size: 25pt;")
        self.tab_field_builders.layout.addWidget(self.instructions5, 2, 1)

        self.inputArea5 = QWidget()
        self.inputArea5.layout = QGridLayout(self)
        self.inputArea5.setLayout(self.inputArea5.layout)
        self.tab_field_builders.layout.addWidget(self.inputArea5, 3, 1)

        self.input5 = QLineEdit()
        self.input5.setFixedWidth(250)
        self.input5.setFixedHeight(40)
        self.input5.setStyleSheet("font-size: 25pt;")
        self.input5.returnPressed.connect(self.logBuilder)
        self.input5.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.inputArea5.layout.addWidget(self.input5, 0, 1)

        self.loginButton5 = QPushButton("Log Attendance")
        self.loginButton5.setStyleSheet("font-size: 25pt;")
        self.loginButton5.clicked.connect(self.logBuilder)
        self.inputArea5.layout.addWidget(self.loginButton5, 1, 1)

        self.clearButton5 = QPushButton("Clear")
        self.clearButton5.setStyleSheet("font-size: 25pt;")
        self.clearButton5.clicked.connect(self.input.clear)
        self.clearButton5.clicked.connect(lambda: self.message5.setText(""))
        self.inputArea5.layout.addWidget(self.clearButton, 2, 1)

        self.message5 = QLabel("")
        self.message5.setStyleSheet("font-size: 25pt;")
        self.message5.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.tab_field_builders.layout.addWidget(self.message5, 4, 1)

        # --------------------
        # Add tabs to widget
        # --------------------
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

        self.input5.setFocus()
        self.input4a.setFocus()
        self.input3.setFocus()
        self.input2.setFocus()
        self.input.setFocus()

    def login(self):
        ID = self.input.text()

        if ID == "":
            self.message.setText("")
            return None

        try:
            ID = int(ID)
        except:
            self.message.setText("Make sure the input is a number.")

        name = lookupName(ID)

        if name != None:

            logAttendance(SPREADSHEET_KEY, name, ID)
            self.input.clear()
            self.message.setText(name + " is logged in.")

        else:
            print("Error! ID number is not associated with a name.")
            self.message.setText("Error! Problem logging in.")
            self.input.clear()

    def searchID(self):
        # print("HI")
        name = self.input2.text()
        ID = lookupID(name)

        if name == "":
            self.message2.setText("")
            return None

        if ID != None:

            print("Name: " + name)
            self.input2.clear()
            self.message2.setText("ID Number: " + str(ID))
            self.input2.setFocus()

            # Log in the user, then switch back to the main tab
            logAttendance(SPREADSHEET_KEY, name, ID)
            self.tabs.setCurrentIndex(0)
            self.input.clear()
            self.message.setText(name + " is logged in.")

        else:
            print("Error! ID number is not associated with a name.")
            self.message2.setText("Error! Name not found in database.")
            self.input2.clear()
            self.input2.setFocus()

    def identifyFob(self):
        ID = self.input3.text()

        if ID == "":
            self.message3.setText("")
            return None

        try:
            ID = int(ID)
        except:
            self.message3.setText("Make sure the input is a number.")

        name = lookupName(ID)

        if name != None:

            self.input3.clear()
            self.message3.setText("Fob " + str(ID) + " belongs to " + name + ".")

        else:
            self.message3.setText("Error! ID number is not associated with a name.")
            self.input3.clear()

    def logVisit(self):
        team = self.input4b.text()
        name = self.input4a.text()

        if name == "":
            self.message4.setText("")
            return None

        if team == "":
            self.message4.setText(
                "Please include a team number. If unaffiliated, write n/a."
            )
            return None

        logVisitor(SPREADSHEET_KEY, name, team)
        self.input4a.clear()
        self.input4b.clear()
        self.message4.setText("Welcome " + name + "!")
        self.input4a.setFocus()

    def logBuilder(self):
        name = self.input5.text()

        if name == "":
            self.message5.setText("")
            return None

        else:

            logBuilderInSheet(SPREADSHEET_KEY, name)
            self.input5.clear()
            self.message5.setText(name + " is logged in.")
            self.input5.setFocus()


# -----------------------------------------------------------------------
# GOOGLE SPREADSHEET CODE
# -----------------------------------------------------------------------

##def lookupID(fname, lname):
##    pass
##


def lookupName(idNumber):
    # print(ids)
    for i in range(len(ids)):
        # print (ids[i])
        if ids[i] == idNumber:
            return firstNames[i] + " " + lastNames[i]

    return None


def lookupID(name):
    for i in range(len(firstNames)):
        if (firstNames[i] + " " + lastNames[i]) == name:
            return ids[i]

    return None


def updateIDData(SK):
    sh = gc.open_by_key(SK)

    wl = sh.worksheet("Member Database")
    # print(wl)

    # print(ds)
    ln = wl.col_values(1)[1:]
    fn = wl.col_values(2)[1:]
    newIDs = wl.col_values(4)[1:]
    # print(newIDs)

    for i in range(len(newIDs)):
        newIDs[i] = int(newIDs[i])

    return ln, fn, newIDs


def logAttendance(SK, name, ID):
    sh = gc.open_by_key(SK)
    date = dt.datetime.now()
    ds = sh.worksheet("GoS Attendance")
    ds.append_row([date.strftime("%c"), ID, name, "General Meeting"])


def logVisitor(SK, name, team):
    sh = gc.open_by_key(SK)
    date = dt.datetime.now()
    ds = sh.worksheet("SCRA Visitor Attendance")
    ds.append_row([date.strftime("%c"), team, name, "SCRA Open Meeting"])


def logBuilderInSheet(SK, name):
    sh = gc.open_by_key(SK)
    date = dt.datetime.now()
    ds = sh.worksheet("Field Builder Attendance")
    ds.append_row([date.strftime("%c"), name])


# -----------------------------------------------------------------------
# MAIN
# -----------------------------------------------------------------------
if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = App()

    gc = gspread.service_account(filename="credentials.json")

    lastNames, firstNames, ids = updateIDData(SPREADSHEET_KEY)

    sys.exit(app.exec())
