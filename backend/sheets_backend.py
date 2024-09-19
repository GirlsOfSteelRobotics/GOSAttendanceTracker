import gspread
import os
import pandas as pd
import datetime as dt
from backend.backend import Backend
from typing import Union, List

SPREADSHEET_KEY = "1ztlyayX_A59oDQQsRPfWNKSZ-efkdWKgML-J9WtB66s"


class GoogleSheetsBackend(Backend):

    last_names: List[str]
    first_names: List[str]
    ids: List[int]

    def __init__(self):
        print("Connecting to sheets")
        gc = gspread.service_account(filename=os.path.abspath("credentials.json"))
        self.spreadsheet = gc.open_by_key(SPREADSHEET_KEY)
        print("Connected!")

        self.refresh_model()

    def refresh_model(self) -> None:
        wl = self.spreadsheet.worksheet("Member Database")

        self.last_names = wl.col_values(1)[1:]
        self.first_names = wl.col_values(2)[1:]
        self.ids = [int(x) for x in wl.col_values(4)[1:]]

    def log_attendance(self, name: str, fob_id: str) -> None:
        date = dt.datetime.now()
        ds = self.spreadsheet.worksheet("GoS Attendance")
        ds.append_row([date.strftime("%c"), fob_id, name, "General Meeting"])

    def log_visitor(self, name: str, team_number: str) -> None:
        date = dt.datetime.now()
        ds = self.spreadsheet.worksheet("SCRA Visitor Attendance")
        ds.append_row([date.strftime("%c"), team_number, name, "SCRA Open Meeting"])

    def log_field_builder(self, name: str) -> None:
        date = dt.datetime.now()
        ds = self.spreadsheet.worksheet("Field Builder Attendance")
        ds.append_row([date.strftime("%c"), name])

    def name_from_fob_id(self, fob_id: str) -> Union[str, None]:
        for i in range(len(self.ids)):
            if self.ids[i] == fob_id:
                return self.first_names[i] + " " + self.last_names[i]

        return None

    def fob_id_from_name(self, name: str) -> Union[int, None]:
        for i in range(len(self.first_names)):
            if (self.first_names[i] + " " + self.last_names[i]) == name:
                return self.ids[i]

        return None

    def download_local_copy(self) -> None:
        """
        Reaches out to the attendance spreadsheet and downloads a local copy of the relevant sheets. This can be useful
        for local testing, as it is much faster to load from disk than from the internet, and you will not corrupt the
        real data
        """
        def download(sheet_name, output_filename):
            worksheet = self.spreadsheet.worksheet(sheet_name)
            dataframe = pd.DataFrame(worksheet.get_all_records())
            dataframe.to_csv(
                os.path.join("local_model", output_filename), index=False
            )

        download("GoS Attendance", "attendance_gos.csv")
        download("SCRA Visitor Attendance", "attendance_scra.csv")
        download("Field Builder Attendance", "attendance_field_builder.csv")
        download("Member Database", "database_gos.csv")
        download("SCRA Visitor Database", "database_scra.csv")
        download("Field Builder Database", "database_field_builder.csv")