import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dashboard.utils import get_preseason_meeting_days, get_maximum_meeting_hours


def create_gos_attendance_plot(student_data: pd.DataFrame) -> go.Figure:
    attendance_count = student_data.groupby(pd.Grouper(key="Date In", freq="D")).count()

    fig = px.bar(attendance_count, y=attendance_count["ID"])

    for meeting_date in get_preseason_meeting_days():
        fig.add_vline(x=meeting_date)

    return fig


def create_gos_hours_per_meeting_plot(student_data: pd.DataFrame) -> go.Figure:
    without_dates = student_data.drop(["Date Out"], axis=1)

    attendance_count = without_dates.groupby(pd.Grouper(key="Date In", freq="D")).sum()

    fig = px.bar(
        attendance_count, x=attendance_count.index, y=attendance_count["Hours Attended"]
    )

    return fig


def create_gos_hours_sum_plot(student_data: pd.DataFrame):
    without_dates = student_data.drop(["Date Out"], axis=1)

    attendance_count = without_dates.groupby(pd.Grouper(key="Date In", freq="D")).sum()
    attendance_count["Cumulative Hours"] = attendance_count["Hours Attended"].cumsum()

    max_meeting_hours = get_maximum_meeting_hours()
    print(max_meeting_hours)

    fig = px.line(
        attendance_count,
        x=attendance_count.index,
        y=attendance_count["Cumulative Hours"],
    )

    fig.add_hline(y=max_meeting_hours * 0.8, annotation_text="80%")
    fig.add_hline(y=max_meeting_hours * 0.6, annotation_text="60%")
    fig.add_hline(y=max_meeting_hours * 0.4, annotation_text="40%")

    return fig
