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
        self.tab_identify_fob = QWidget()
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

        self.input_area_gos_login = QWidget()
        self.input_area_gos_login.layout = QGridLayout(self)
        self.input_area_gos_login.setLayout(self.input_area_gos_login.layout)
        self.tab_log_attendance.layout.addWidget(self.input_area_gos_login, 3, 1)

        self.input_gos_name = QLineEdit()
        self.input_gos_name.setFixedWidth(250)
        self.input_gos_name.setFixedHeight(40)
        self.input_gos_name.setStyleSheet("font-size: 25pt;")
        self.input_gos_name.returnPressed.connect(self.login)
        self.input_gos_name.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.input_area_gos_login.layout.addWidget(self.input_gos_name, 0, 1)

        self.btn_login_gos = QPushButton("Login")
        self.btn_login_gos.setStyleSheet("font-size: 25pt;")
        self.btn_login_gos.clicked.connect(self.login)
        self.input_area_gos_login.layout.addWidget(self.btn_login_gos, 1, 1)

        self.btn_clear_gos_name = QPushButton("Clear")
        self.btn_clear_gos_name.setStyleSheet("font-size: 25pt;")
        self.btn_clear_gos_name.clicked.connect(self.input_gos_name.clear)
        self.btn_clear_gos_name.clicked.connect(lambda: self.message_gos_login.setText(""))
        self.input_area_gos_login.layout.addWidget(self.btn_clear_gos_name, 2, 1)

        self.message_gos_login = QLabel("")
        self.message_gos_login.setStyleSheet("font-size: 25pt;")
        self.message_gos_login.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.tab_log_attendance.layout.addWidget(self.message_gos_login, 4, 1)

        # --------------------
        # Tab 2 Content
        # --------------------

        self.tab_lookup_fob.layout = QGridLayout(self)
        self.tab_lookup_fob.setLayout(self.tab_lookup_fob.layout)
        self.tab_lookup_fob.setStyleSheet("background-color: #bad3fe;")  # ffc3bf;")

        self.header_lookup_fob = QLabel("Forgot your fob? Not a problem!")
        self.header_lookup_fob.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.header_lookup_fob.setFont(headerFont)
        self.header_lookup_fob.setStyleSheet("font-size: 35pt;")
        self.tab_lookup_fob.layout.addWidget(self.header_lookup_fob, 1, 1)

        self.instructions_lookup_fob = QLabel("Type your full name below. (Ex: Rosie Riveter)")
        self.instructions_lookup_fob.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.instructions_lookup_fob.setStyleSheet("font-size: 25pt;")
        self.tab_lookup_fob.layout.addWidget(self.instructions_lookup_fob, 2, 1)

        self.input_area_lookup_fob = QWidget()
        self.input_area_lookup_fob.layout = QGridLayout(self)
        self.input_area_lookup_fob.setLayout(self.input_area_lookup_fob.layout)
        self.tab_lookup_fob.layout.addWidget(self.input_area_lookup_fob, 3, 1)

        self.input_fob_lookup = QLineEdit()
        self.input_fob_lookup.setFixedWidth(250)
        self.input_fob_lookup.setFixedHeight(40)
        self.input_fob_lookup.returnPressed.connect(self.searchID)
        # self.input.setStyleSheet("height: 100px;")
        self.input_fob_lookup.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.input_fob_lookup.setStyleSheet("font-size: 25pt;")
        self.input_area_lookup_fob.layout.addWidget(self.input_fob_lookup, 0, 1)

        self.btn_search_fob = QPushButton("Search")
        self.btn_search_fob.clicked.connect(self.searchID)
        self.btn_search_fob.setStyleSheet("font-size: 25pt;")
        self.input_area_lookup_fob.layout.addWidget(self.btn_search_fob, 1, 1)

        self.btn_clear_lookup_fob = QPushButton("Clear")
        self.btn_clear_lookup_fob.clicked.connect(self.input_fob_lookup.clear)
        self.btn_clear_lookup_fob.clicked.connect(lambda: self.message_fob_lookup.setText(""))
        self.btn_clear_lookup_fob.setStyleSheet("font-size: 25pt;")
        self.input_area_lookup_fob.layout.addWidget(self.btn_clear_lookup_fob, 2, 1)

        self.message_fob_lookup = QLabel("")
        self.message_fob_lookup.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.message_fob_lookup.setStyleSheet("font-size: 25pt;")
        self.message_fob_lookup.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextSelectableByMouse
        )
        self.tab_lookup_fob.layout.addWidget(self.message_fob_lookup, 4, 1)

        # --------------------
        # Tab 3 Content
        # --------------------

        self.tab_identify_fob.layout = QGridLayout(self)
        self.tab_identify_fob.setLayout(self.tab_identify_fob.layout)
        self.tab_identify_fob.setStyleSheet("background-color: #bad3fe;")  # ffffff;")

        self.header_lost_fob = QLabel("Found a lost fob, but don't know whose it is?")
        self.header_lost_fob.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.header_lost_fob.setFont(headerFont)
        self.header_lost_fob.setStyleSheet("font-size: 35pt;")
        self.tab_identify_fob.layout.addWidget(self.header_lost_fob, 1, 1)

        self.instructions_lost_fob = QLabel("Scan the fob and find out who it belongs to!")
        self.instructions_lost_fob.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.instructions_lost_fob.setStyleSheet("font-size: 25pt;")
        self.tab_identify_fob.layout.addWidget(self.instructions_lost_fob, 2, 1)

        self.input_area_search_fob = QWidget()
        self.input_area_search_fob.layout = QGridLayout(self)
        self.input_area_search_fob.setLayout(self.input_area_search_fob.layout)
        self.tab_identify_fob.layout.addWidget(self.input_area_search_fob, 3, 1)

        self.input_identify_fob = QLineEdit()
        self.input_identify_fob.setFixedWidth(250)
        self.input_identify_fob.setFixedHeight(40)
        self.input_identify_fob.setStyleSheet("font-size: 25pt;")
        self.input_identify_fob.returnPressed.connect(self.identifyFob)
        self.input_identify_fob.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.input_area_search_fob.layout.addWidget(self.input_identify_fob, 0, 1)

        self.searchButton3 = QPushButton("Search")
        self.searchButton3.clicked.connect(self.identifyFob)
        self.searchButton3.setStyleSheet("font-size: 25pt;")
        self.input_area_search_fob.layout.addWidget(self.searchButton3, 1, 1)

        self.clearButton3 = QPushButton("Clear")
        self.clearButton3.clicked.connect(self.input_identify_fob.clear)
        self.clearButton3.setStyleSheet("font-size: 25pt;")
        self.input_area_search_fob.layout.addWidget(self.clearButton3, 2, 1)

        self.message_identify_fob = QLabel("")
        self.message_identify_fob.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.message_identify_fob.setStyleSheet("font-size: 25pt;")
        self.tab_identify_fob.layout.addWidget(self.message_identify_fob, 4, 1)

        # --------------------
        # Tab 4 Content
        # --------------------
        self.tab_scra_visitor_log.layout = QHBoxLayout(self)
        self.tab_scra_visitor_log.setLayout(self.tab_scra_visitor_log.layout)
        self.tab_scra_visitor_log.setStyleSheet("background-color: #fceb7c;")

        ##        self.label4 = QLabel("Page Under Construction")
        ##        self.label4.setAlignment(Qt.AlignmentFlag.AlignCenter)
        ##        self.tab4.layout.addWidget(self.label4)

        self.scra_logo = QLabel(self)
        self.scra_pixmap = QPixmap("SCRA2.png")
        self.scra_logo.setPixmap(self.scra_pixmap)
        self.scra_logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.tab_scra_visitor_log.layout.addWidget(self.scra_logo)

        self.signinBox4 = QWidget()
        self.signinBox4.layout = QGridLayout(self)
        self.signinBox4.setLayout(self.signinBox4.layout)
        self.tab_scra_visitor_log.layout.addWidget(self.signinBox4)

        self.header_scra_signin = QLabel("SCRA Open Meeting Sign-In")
        self.header_scra_signin.setAlignment(Qt.AlignmentFlag.AlignCenter)
        headerFont4 = QFont()
        headerFont4.setBold(True)
        self.header_scra_signin.setFont(headerFont)
        self.header_scra_signin.setStyleSheet("font-size: 35pt;")
        self.signinBox4.layout.addWidget(self.header_scra_signin, 0, 0)

        self.inputArea4 = QWidget()
        self.inputArea4.layout = QGridLayout(self)
        self.inputArea4.setLayout(self.inputArea4.layout)
        self.signinBox4.layout.addWidget(self.inputArea4, 1, 0)

        self.lbl_scra_name = QLabel("Name:")
        self.lbl_scra_name.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_scra_name.setStyleSheet("font-size: 25pt;")
        self.inputArea4.layout.addWidget(self.lbl_scra_name, 0, 1)

        self.lbl_scra_team_number = QLabel("Team Number:")
        self.lbl_scra_team_number.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_scra_team_number.setStyleSheet("font-size: 25pt;")
        self.inputArea4.layout.addWidget(self.lbl_scra_team_number, 1, 1)

        self.input_visit_name = QLineEdit()
        self.input_visit_name.setFixedWidth(250)
        self.input_visit_name.setFixedHeight(40)
        self.input_visit_name.setStyleSheet("font-size: 25pt;")
        self.input_visit_name.returnPressed.connect(self.logVisit)
        self.input_visit_name.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.inputArea4.layout.addWidget(self.input_visit_name, 0, 2)

        self.input_visit_team = QLineEdit()
        self.input_visit_team.setFixedWidth(250)
        self.input_visit_team.setFixedHeight(40)
        self.input_visit_team.setStyleSheet("font-size: 25pt;")
        self.input_visit_team.returnPressed.connect(self.logVisit)
        self.input_visit_team.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.inputArea4.layout.addWidget(self.input_visit_team, 1, 2)

        self.btn_scra_login = QPushButton("Submit")
        self.btn_scra_login.setFixedWidth(250)
        self.btn_scra_login.setStyleSheet("font-size: 25pt;")
        self.btn_scra_login.clicked.connect(self.logVisit)
        self.signinBox4.layout.addWidget(self.btn_scra_login, 2, 1)

        self.btn_scra_clear = QPushButton("Clear")
        self.btn_scra_clear.setFixedWidth(250)
        self.btn_scra_clear.setStyleSheet("font-size: 25pt;")
        self.btn_scra_clear.clicked.connect(self.input_gos_name.clear)
        self.btn_scra_clear.clicked.connect(lambda: self.message_visit.setText(""))
        self.signinBox4.layout.addWidget(self.btn_scra_clear, 4, 1)

        self.message_visit = QLabel("")
        self.message_visit.setStyleSheet("font-size: 25pt;")
        self.message_visit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.signinBox4.layout.addWidget(self.message_visit, 5, 0)

        # --------------------
        # Tab 5 Content
        # --------------------
        self.tab_field_builders.layout = QGridLayout(self)
        self.tab_field_builders.setLayout(self.tab_field_builders.layout)
        self.tab_field_builders.setStyleSheet("background-color: #bad3fe;")

        self.game_logo = QLabel(self)
        self.game_pixmap = QPixmap("chargedUp.png")
        self.game_logo.setPixmap(self.game_pixmap)
        self.game_logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.tab_field_builders.layout.addWidget(self.game_logo, 0, 1)

        self.header_field_builder = QLabel("\nWelcome, Practice Field Builder!")
        self.header_field_builder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        headerFont5 = QFont()
        headerFont5.setBold(True)
        self.header_field_builder.setFont(headerFont5)
        self.header_field_builder.setStyleSheet("font-size: 35pt;")
        self.tab_field_builders.layout.addWidget(self.header_field_builder, 1, 1)

        self.instructions_field_builder = QLabel(
            "Type your name below to log your presence here today."
        )
        self.instructions_field_builder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.instructions_field_builder.setStyleSheet("font-size: 25pt;")
        self.tab_field_builders.layout.addWidget(self.instructions_field_builder, 2, 1)

        self.inputArea5 = QWidget()
        self.inputArea5.layout = QGridLayout(self)
        self.inputArea5.setLayout(self.inputArea5.layout)
        self.tab_field_builders.layout.addWidget(self.inputArea5, 3, 1)

        self.input_builder_name = QLineEdit()
        self.input_builder_name.setFixedWidth(250)
        self.input_builder_name.setFixedHeight(40)
        self.input_builder_name.setStyleSheet("font-size: 25pt;")
        self.input_builder_name.returnPressed.connect(self.logBuilder)
        self.input_builder_name.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.inputArea5.layout.addWidget(self.input_builder_name, 0, 1)

        self.loginButton5 = QPushButton("Log Attendance")
        self.loginButton5.setStyleSheet("font-size: 25pt;")
        self.loginButton5.clicked.connect(self.logBuilder)
        self.inputArea5.layout.addWidget(self.loginButton5, 1, 1)

        self.btn_clear_field_builder = QPushButton("Clear")
        self.btn_clear_field_builder.setStyleSheet("font-size: 25pt;")
        self.btn_clear_field_builder.clicked.connect(self.input_gos_name.clear)
        self.btn_clear_field_builder.clicked.connect(lambda: self.message_builder.setText(""))
        self.inputArea5.layout.addWidget(self.btn_clear_gos_name, 2, 1)

        self.message_builder = QLabel("")
        self.message_builder.setStyleSheet("font-size: 25pt;")
        self.message_builder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.tab_field_builders.layout.addWidget(self.message_builder, 4, 1)

        # --------------------
        # Add tabs to widget
        # --------------------
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

        self.input_builder_name.setFocus()
        self.input_visit_name.setFocus()
        self.input_identify_fob.setFocus()
        self.input_fob_lookup.setFocus()
        self.input_gos_name.setFocus()

    def login(self):
        ID = self.input_gos_name.text()

        if ID == "":
            self.message_gos_login.setText("")
            return None

        try:
            ID = int(ID)
        except:
            self.message_gos_login.setText("Make sure the input is a number.")

        name = lookupName(ID)

        if name != None:

            logAttendance(SPREADSHEET_KEY, name, ID)
            self.input_gos_name.clear()
            self.message_gos_login.setText(name + " is logged in.")

        else:
            print("Error! ID number is not associated with a name.")
            self.message_gos_login.setText("Error! Problem logging in.")
            self.input_gos_name.clear()

    def searchID(self):
        # print("HI")
        name = self.input_fob_lookup.text()
        ID = lookupID(name)

        if name == "":
            self.message_fob_lookup.setText("")
            return None

        if ID != None:

            print("Name: " + name)
            self.input_fob_lookup.clear()
            self.message_fob_lookup.setText("ID Number: " + str(ID))
            self.input_fob_lookup.setFocus()

            # Log in the user, then switch back to the main tab
            logAttendance(SPREADSHEET_KEY, name, ID)
            self.tabs.setCurrentIndex(0)
            self.input_gos_name.clear()
            self.message_gos_login.setText(name + " is logged in.")

        else:
            print("Error! ID number is not associated with a name.")
            self.message_fob_lookup.setText("Error! Name not found in database.")
            self.input_fob_lookup.clear()
            self.input_fob_lookup.setFocus()

    def identifyFob(self):
        ID = self.input_identify_fob.text()

        if ID == "":
            self.message_identify_fob.setText("")
            return None

        try:
            ID = int(ID)
        except:
            self.message_identify_fob.setText("Make sure the input is a number.")

        name = lookupName(ID)

        if name != None:

            self.input_identify_fob.clear()
            self.message_identify_fob.setText("Fob " + str(ID) + " belongs to " + name + ".")

        else:
            self.message_identify_fob.setText("Error! ID number is not associated with a name.")
            self.input_identify_fob.clear()

    def logVisit(self):
        team = self.input_visit_team.text()
        name = self.input_visit_name.text()

        if name == "":
            self.message_visit.setText("")
            return None

        if team == "":
            self.message_visit.setText(
                "Please include a team number. If unaffiliated, write n/a."
            )
            return None

        logVisitor(SPREADSHEET_KEY, name, team)
        self.input_visit_name.clear()
        self.input_visit_team.clear()
        self.message_visit.setText("Welcome " + name + "!")
        self.input_visit_name.setFocus()

    def logBuilder(self):
        name = self.input_builder_name.text()

        if name == "":
            self.message_builder.setText("")
            return None

        else:

            logBuilderInSheet(SPREADSHEET_KEY, name)
            self.input_builder_name.clear()
            self.message_builder.setText(name + " is logged in.")
            self.input_builder_name.setFocus()


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
