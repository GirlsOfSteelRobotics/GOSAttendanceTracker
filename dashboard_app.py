from shiny import App, reactive, render, ui

from dashboard.tabs.gos_overview_tab import gos_overview_tab_ui, gos_overview_tab_server
from dashboard.tabs.gos_student_tab import gos_student_tab_ui, gos_student_tab_server


app_ui = ui.page_navbar(
    ui.nav_panel("GOS Overview", gos_overview_tab_ui("gos_overview_tab")),
    ui.nav_panel("GOS Student", gos_student_tab_ui("gos_student_tab")),

)


def server(input, output, session):
    gos_overview_tab_server("gos_overview_tab")
    gos_student_tab_server("gos_student_tab")


app = App(app_ui, server)
