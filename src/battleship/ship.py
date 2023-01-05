"""
Ship Class for simulating a ship
"""

# Extended Python
import plotly.graph_objects as go

# Battleship Python
from battleship.object import Object
from battleship.params import (
    FULL_FIGURE_HEIGHT,
    FULL_FIGURE_WIDTH
)
from battleship.radar import Radar

# Constants
DEFAULT_LOCATION_Z = 0


class Ship(Object):

    def __init__(self, location_x, location_y, name=""):
        """ Initialize a Ship """
        super(Ship, self).__init__(pos_x=location_x, pos_y=location_y, pos_z=DEFAULT_LOCATION_Z)

        self.name = name or "ship"
        self.location_x = location_x
        self.location_y = location_y
        self.location_z = DEFAULT_LOCATION_Z

        self.radar = None

    def add_to_environment(self, environment):
        """ Add object within environment """
        object_id = environment.create_new_object(
            self.location_x,
            self.location_y,
            self.location_z
        )
        self.set_object_id(object_id)
    
    def setup_radar(self, range, theta, phi):
        """ Setup the radar on the ship """
        self.radar = Radar(
            range=range,
            theta=theta,
            phi=phi,
        )
        
    def plot(self):
        """ Plot the ship and all components of it """
        x, y, z = self.get_current_position()
        fig = go.Figure(
            data=go.Scatter3d(x=[x], y=[y], z=[z], marker=dict(color="blue"), name=self.name)
        )

        if self.radar:
            radar_fig = self.radar.plot()
            fig = go.Figure(data=fig.data + radar_fig.data)
        
        fig.update_layout(width=FULL_FIGURE_WIDTH, height=FULL_FIGURE_HEIGHT)
        return fig
