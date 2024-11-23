import pandas as pd
import datetime
from typing import Union, Optional
from dashboard.data_container import DataContainer


def get_meeting_days(start_date, end_date):
    mon = pd.date_range(start_date, end_date, freq='W-MON')
    tue = pd.date_range(start_date, end_date, freq='W-TUE')
    thr = pd.date_range(start_date, end_date, freq='W-THU')
    sat = pd.date_range(start_date, end_date, freq='W-SAT')

    return mon.union(tue).union(thr).union(sat)


def get_preseason_meeting_days():
    start_date = datetime.datetime.strptime("2024-09-01", "%Y-%m-%d")
    # end_date = datetime.datetime.strptime("2025-01-05", "%Y-%m-%d")
    end_date = datetime.datetime.now()
    return get_meeting_days(start_date, end_date)


def get_maximum_meeting_hours() -> float:
    meeting_days = get_preseason_meeting_days()
    return 3 * len(meeting_days)


def get_gos_user_data(data_container : DataContainer, rfid: Union[str, int]) -> Optional[pd.DataFrame]:
    if isinstance(rfid, str):
        try:
            rfid = int(rfid)
        except ValueError:
            return None

    return data_container.gos_attendance[
        data_container.gos_attendance["ID"] == rfid
    ]
