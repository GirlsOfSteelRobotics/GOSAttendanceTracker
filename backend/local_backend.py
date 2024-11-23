import datetime
import os
import logging
from typing import List, Any, Union

import pandas as pd

from backend.backend import Backend


class LocalBackend(Backend):
    GOS_USERS = "database_gos.csv"
    SCRA_USERS = "database_scra.csv"
    FIELD_USERS = "database_field_builder.csv"

    GOS_ATTENDANCE = "attendance_gos.csv"
    SCRA_ATTENDANCE = "attendance_scra.csv"
    FIELD_ATTENDANCE = "attendance_field_builder.csv"

    last_names: List[str]
    first_names: List[str]
    ids: List[int]

    def __init__(self, base_directory="local_model"):
        self.base_directory = os.path.abspath(base_directory)
        logging.info(f"Loading local model from {self.base_directory}")
        self.refresh_model()

    def refresh_model(self) -> None:
        self.__load_gos()

    def __load_gos(self):
        df = pd.read_csv(os.path.join(self.base_directory, LocalBackend.GOS_USERS))
        self.last_names = list(df["Last Name"])
        self.first_names = list(df["First Name"])
        self.ids = [int(x) for x in df["ID Tag Number"]]

    def log_attendance(self, name: str, fob_id: str) -> None:
        self.__log_attendance(
            LocalBackend.GOS_ATTENDANCE, [fob_id, name, "General Meeting"]
        )

    def log_visitor(self, name: str, team_number: str) -> None:
        self.__log_attendance(
            LocalBackend.SCRA_ATTENDANCE, [team_number, name]
        )

    def log_field_builder(self, name: str) -> None:
        self.__log_attendance(LocalBackend.FIELD_ATTENDANCE, [name])

    def __log_attendance(self, attendance_file: str, columns: List[Any]):
        date = datetime.datetime.now()
        date_string = date.strftime("%c")

        with open(os.path.join(self.base_directory, attendance_file), "a") as f:
            f.write(date_string + ",")
            f.write(",".join(str(x) for x in columns))
            f.write("\n")

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

    def load_gos_attendance(self):
        return pd.read_csv(os.path.join(self.base_directory, self.GOS_ATTENDANCE))
