"""
Ship Class for simulating a ship
"""

# Base Python
import os

# Extended Python
import pandas as pd
import plotly.graph_objects as go

# Battleship Python
from battleship.object import Object
from battleship.params import (
    DEFAULT_LOCATION_Z,
    FULL_FIGURE_HEIGHT,
    FULL_FIGURE_WIDTH
)
from battleship.radar import Radar

# Constants
SHIP_LOCATION_FILE = "ship_location.csv"


class Ship(Object):

    def __init__(self, location_x, location_y, name="", color=None):
        """ Initialize a Ship """
        super(Ship, self).__init__(pos_x=location_x, pos_y=location_y, pos_z=DEFAULT_LOCATION_Z)

        self.name = name or "ship"
        self.set_color(color)
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
            location_x=self.location_x,
            location_y=self.location_y,
            range=range,
            theta=theta,
            phi=phi,
        )
        color = self.get_color()
        if color is not None:
            self.radar.set_color(color)
        
    def plot(self, color="blue"):
        """ Plot the ship and all components of it """
        color = self.get_color() or color
        x, y, z = self.get_current_position()
        fig = go.Figure(
            data=go.Scatter3d(x=[x], y=[y], z=[z], marker=dict(color=color), name=self.name)
        )

        if self.radar:
            radar_fig = self.radar.plot(color=color)
            fig = go.Figure(data=fig.data + radar_fig.data)
        
        fig.update_layout(width=FULL_FIGURE_WIDTH, height=FULL_FIGURE_HEIGHT)
        return fig

    def to_file(self, output):
        """ Save object timeline to file """
        table = pd.DataFrame({
            "name": [self.name],
            "location_x": [self.location_x],
            "location_y": [self.location_y],
            "location_z": [self.location_z],
        })
        name = os.path.join(output, SHIP_LOCATION_FILE)
        table.to_csv(name, index=False)

        if self.radar is not None:
            self.radar.to_file(output)

    def update(self):
        """ Update the ship location (not yet implemented) """
        raise NotImplementedError("The ship is not able to be updated")
