"""
Ship Class for simulating a ship
"""

# Extended Python
import plotly.graph_objects as go

# Battleship Python
from battleship.params import (
    FULL_FIGURE_HEIGHT,
    FULL_FIGURE_WIDTH
)
from battleship.radar import Radar

# Constants
DEFAULT_LOCATION_Z = 0


class Ship:

    def __init__(self, location_x, location_y, name=""):
        """ Initialize a Ship """
        self.name = name or "ship"
        self.location_x = location_x
        self.location_y = location_y
        self.location_z = DEFAULT_LOCATION_Z

        self.radar = None
    
    def setup_radar(self, range, theta, phi):
        """ """
        self.radar = Radar(
            range=range,
            theta=theta,
            phi=phi,
        )
        
    def plot(self):
        """ Plot the ship and all components of it """
        fig = go.Figure(
            data=go.Scatter3d(x=[0], y=[0], z=[0], marker=dict(color="blue"), name=self.name)
        )

        if self.radar:
            radar_fig = self.radar.plot()
            fig = go.Figure(data=fig.data + radar_fig.data)
        
        fig.update_layout(width=FULL_FIGURE_WIDTH, height=FULL_FIGURE_HEIGHT)
        return fig
