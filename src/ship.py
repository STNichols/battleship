"""
Ship Class for simulating a ship
"""

# Battleship Python
from radar import Radar

# Constants
DEFAULT_LOCATION_Z = 0


class Ship:

    def __init__(self, location_x, location_y):
        """ Initialize a Ship """
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
        