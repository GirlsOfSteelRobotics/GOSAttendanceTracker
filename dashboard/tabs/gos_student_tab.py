from shiny import Inputs, Outputs, Session, module, reactive, render, ui
from shinywidgets import output_widget, render_widget
from dashboard.data_container import data_container
import pandas as pd


from dashboard.plotting import create_gos_attendance_plot, create_gos_hours_per_meeting_plot, create_gos_hours_sum_plot
from dashboard.utils import get_gos_user_data


@module.ui
def gos_student_tab_ui():
    return ui.page_sidebar(
        ui.sidebar(
            ui.input_text("rfid_input", "RFID"),
            title="ID Number",
        ),
        ui.page_fluid(
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
                ui.card_header("Attendance"),
                output_widget("attendance_plot"),
                full_screen=True,
            ),
            ui.card(
                ui.card_header("Hours / Meeting"),
                output_widget("hours_per_meeting_plot"),
                full_screen=True,
            ),
            ui.card(
                ui.card_header("Cumulative Hours"),
                output_widget("cumulative_hours_plot"),
                full_screen=True,
            ),
            ui.card(
                ui.card_header("Raw Data"),
                ui.output_data_frame("raw_data"),
                full_screen=True,
            ),
        ),
    )


@module.server
def gos_student_tab_server(input: Inputs, output: Outputs, session: Session):
    @reactive.calc
    def filter_by_user() -> pd.DataFrame:
        return get_gos_user_data(data_container, input.rfid_input())

    @render_widget
    def attendance_plot():
        user_data = filter_by_user()
        if user_data is None:
            return None
        return create_gos_attendance_plot(user_data)

    @render_widget
    def cumulative_hours_plot():
        user_data = filter_by_user()
        if user_data is None:
            return None
        return create_gos_hours_sum_plot(user_data)

    @render_widget
    def hours_per_meeting_plot():
        user_data = filter_by_user()
        if user_data is None:
            return None
        return create_gos_hours_per_meeting_plot(user_data)

    @render.data_frame
    def raw_data():
        user_data = filter_by_user()
        if user_data is None:
            return None
        user_data = pd.DataFrame.copy(user_data)
        user_data["Date In"] = user_data["Date In"].dt.strftime("%Y-%m-%d %H:%M")
        user_data["Date Out"] = user_data["Date Out"].dt.strftime("%Y-%m-%d %H:%M")
        return render.DataGrid(user_data, filters=True)

    @render.text
    def days_attended():
        user_data = filter_by_user()
        if user_data is None:
            return "Select Student"
        return f"{user_data.count(numeric_only=True)['Hours Attended']}"

    @render.text
    def hours_logged():
        user_data = filter_by_user()
        if user_data is None:
            return "Select Student"
        return f"{user_data.sum(numeric_only=True)['Hours Attended']:.2f}"
