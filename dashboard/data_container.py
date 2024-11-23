import logging

from backend.local_backend import LocalBackend
from backend.sheets_backend import GoogleSheetsBackend
import pandas as pd
import datetime


STRIP_NAMES = True
NO_LOGOUT_HOURS_ASSUMPTION = 2


class DataContainer:
    def __init__(self):
        # backend = LocalBackend()
        backend = GoogleSheetsBackend()

        self.gos_attendance = backend.load_gos_attendance()

        self.__annotate_gos_attendance()

        if STRIP_NAMES:
            self.__strip_names()

    def __annotate_gos_attendance(self):

        self.gos_attendance["Missing Logout"] = self.gos_attendance[
            "Date Out"
        ].isnull() | (self.gos_attendance["Date Out"] == "")

        self.gos_attendance["Date In"] = pd.to_datetime(
            self.gos_attendance["Date In"], format="%m/%d/%y %I:%M %p"
        )

        no_logout = self.gos_attendance["Missing Logout"]
        self.gos_attendance.loc[no_logout, "Date Out"] = self.gos_attendance["Date In"][
            no_logout
        ] + datetime.timedelta(hours=NO_LOGOUT_HOURS_ASSUMPTION)

        self.gos_attendance["Date Out"] = pd.to_datetime(
            self.gos_attendance["Date Out"], format="%m/%d/%y %I:%M %p"
        )
        self.gos_attendance["Hours Attended"] = (
            self.gos_attendance["Date Out"] - self.gos_attendance["Date In"]
        ).dt.total_seconds() / (60 * 60)

    def __strip_names(self):
        self.gos_attendance = self.gos_attendance.drop("Student Name", axis=1)


data_container = DataContainer()
