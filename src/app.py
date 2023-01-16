"""
Web App to interact with all battleship components
"""

# Extended Python
import streamlit as st
import plotly.colors as pcolors
import plotly.graph_objects as go

# Battleship Python
from battleship import (
    Environment,
    Missile,
    Ship
)
from battleship.params import (
    FULL_FIGURE_HEIGHT,
    FULL_FIGURE_WIDTH,
)

# Constants
COLORS = pcolors.qualitative.G10

# Streamlit Configuration
st.set_page_config("Battleship", ":ship:", layout="wide")
if "ships" not in st.session_state:
    st.session_state["ships"] = []
if "index" not in st.session_state:
    st.session_state["index"] = 0


def battle(tab):
    """ Setup the battle tab """
    pass


def planner(tab):
    """ Setup the planner tab """
    col_1, col_2 = tab.columns([1, 3])

    fig = go.Figure()
    fig.update_layout(height=FULL_FIGURE_HEIGHT, width=FULL_FIGURE_WIDTH)

    ship = setup_ship(col_1)
    ships = [ship] + st.session_state["ships"]
    for ship in ships:
        ship_fig = ship.plot()
        for trace in ship_fig.data:
            fig.add_trace(trace)
    col_2.plotly_chart(fig)

    if col_1.button("Add another"):
        st.session_state["ships"].append(ship)
        st.session_state["index"] += 1
    if col_1.button("Reset"):
        st.session_state["ships"] = []
        st.session_state["index"] = 0


def setup_ship(column):
    """ Setup a new ship """
    color = COLORS[st.session_state["index"]]

    # Ship Parameters
    column.header("Ship Parameters")
    name = column.text_input("Ship Name:", value="ship")
    location_x = column.number_input("Location X:", value=0)
    location_y = column.number_input("Location Y:", value=0)

    # Radar Parameters
    column.header("Radar Parameters")
    radar_range = column.slider("Range min / max (km):", 10, 500, (50, 100))
    radar_theta = column.slider(f"𝜭 min / max ({chr(176)}):", 0, 360, (0, 30))
    radar_phi = column.slider(f"ϴ min / max ({chr(176)}):", 0, 90, (10, 20))

    ship = Ship(location_x=location_x, location_y=location_y, name=name, color=color)
    ship.setup_radar(radar_range, radar_theta, radar_phi)

    return ship


def run_app():
    """ Run the app """
    st.title("Battleship")
    tab_plan, tab_battle = st.tabs(["Plan", "Battle"])

    planner(tab_plan)
    battle(tab_battle)


if __name__ == "__main__":
    run_app()
