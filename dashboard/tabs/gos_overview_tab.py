from shiny import Inputs, Outputs, Session, module, reactive, render, ui
from shinywidgets import output_widget, render_widget
from dashboard.data_container import data_container, STRIP_NAMES
import pandas as pd
import plotly.express as px


@module.ui
def gos_overview_tab_ui():
    return ui.page_fluid(
            ui.layout_column_wrap(
                ui.value_box(
                    "Days Attended",
                    ui.output_text("days_attended"),
                ),
                ui.value_box(
                    "Hours Logged",
                    ui.output_text("hours_logged"),
                ),
            ),
            ui.card(
                ui.card_header("Hours"),
                output_widget("hours_plot"),
                full_screen=True,
            ),
            ui.card(
                ui.card_header("Attendance / Day"),
                output_widget("attendance_per_day_plot"),
                full_screen=True,
            ),
            ui.card(
                ui.card_header("Raw Data"),
                ui.output_data_frame("raw_data"),
                full_screen=True,
            ),
        )



@module.server
def gos_overview_tab_server(input: Inputs, output: Outputs, session: Session):
    @render_widget
    def attendance_per_day_plot():
        week_df = data_container.gos_attendance.groupby(data_container.gos_attendance['Date In'].dt.day_name()).count()
        return px.pie(week_df, values="Date In", names=week_df.index, title="Attendance / Day")


    @render_widget
    def hours_plot():
        groupby_key = "ID" if STRIP_NAMES else "Student Name"
        grouped_data = data_container.gos_attendance.groupby(groupby_key).sum(numeric_only=True)
        grouped_data = grouped_data.sort_values("Hours Attended")

        return px.bar(grouped_data, y="Hours Attended", x=[str(x) for x in grouped_data.index])


    @render.text
    def days_attended():
        return f"{data_container.gos_attendance.count(numeric_only=True)['Hours Attended']}"

    @render.text
    def hours_logged():
        return f"{data_container.gos_attendance.sum(numeric_only=True)['Hours Attended']:.2f}"

    @render.data_frame
    def raw_data():
        user_data = pd.DataFrame.copy(data_container.gos_attendance)
        user_data["Date In"] = user_data["Date In"].dt.strftime("%Y-%m-%d %H:%M")
        user_data["Date Out"] = user_data["Date Out"].dt.strftime("%Y-%m-%d %H:%M")
        return render.DataGrid(user_data, filters=True)
