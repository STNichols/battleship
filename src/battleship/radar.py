"""
Radar Class for simulating a radar
"""

# Extended Python
import matplotlib.colors as mcolors
import numpy as np
import pandas as pd
import plotly.figure_factory as ff
import plotly.graph_objects as go

# Battleship Python
from battleship.object import Object
from battleship.params import (
    FULL_FIGURE_HEIGHT,
    FULL_FIGURE_WIDTH
)
from battleship.utils import (
    generate_polar_simplices,
    polar_to_cartesian
)

# Constants
MIN_RANGE = 0
MIN_PHI = 0
MAX_PHI = 90
MIN_THETA = 0
MAX_THETA = 360
N_IN_SECTOR = 10


class Radar(Object):

    def __init__(self, range, theta, phi, name=""):
        """ Initialize the radar and check inputs """
        self._name = name or "radar"
        self.check_radar_inputs(range, theta, phi)
        self.generate_sector()

    def check_radar_inputs(self, range, theta, phi):
        """ Check validity of radar inputs """

        if not isinstance(range, list) and len(range) != 2:
            raise Exception("Range provided to radar must be a list of length 2")
        if range[0] < MIN_RANGE:
            raise Exception(f"Invalid minimum range: {range[0]}")
        if range[1] <= range[0]:
            raise Exception("Invalid ranges provided, must be [min, max]")
        self.min_range = range[0]
        self.max_range = range[1]

        if not isinstance(theta, list) and len(theta) != 2:
            raise Exception("Theta provided to radar must be a list of length 2")
        if theta[0] < MIN_THETA or theta[0] > MAX_THETA:
            raise Exception(f"Invalid min theta: {theta[0]}, must be [{MIN_THETA}, {MAX_THETA}]")
        if theta[1] < MIN_THETA or theta[1] > MAX_THETA:
            raise Exception(f"Invalid max theta: {theta[0]}, must be [{MIN_THETA}, {MAX_THETA}]")
        if theta[1] <= theta[0]:
            raise Exception("Invalid theta provided, must be [min, max]")
        self.min_theta = theta[0]
        self.max_theta = theta[1]

        if not isinstance(phi, list) and len(phi) != 2:
            raise Exception("Phi provided to radar must be a list of length 2")
        if phi[0] < 0 or phi[0] > MAX_PHI:
            raise Exception(f"Invalid min phi: {phi[0]}, must be [{MIN_PHI}, {MAX_PHI}]")
        if phi[1] < 0 or phi[1] > MAX_PHI:
            raise Exception(f"Invalid max phi: {phi[0]}, must be [{MIN_PHI}, {MAX_PHI}]")
        if phi[1] <= phi[0]:
            raise Exception("Invalid phi provided, must be [min, max]")
        self.min_phi = phi[0]
        self.max_phi = phi[1]

    def generate_sector(self, n=N_IN_SECTOR):
        """ 
        Generate sector representing a 3D slice in a polar coordinate frame.
        Convert to cartesian.
        Calculate simplices for triangulation.
        """
        r_mesh = np.array([])
        theta_mesh = np.array([])
        phi_mesh = np.array([])

        r = np.linspace(self.min_range, self.max_range, n)
        theta = np.linspace(self.min_theta, self.max_theta, n)
        phi = np.linspace(self.min_phi, self.max_phi, n)

        # Mesh theta phi with r min
        r_temp, theta_temp, phi_temp = np.meshgrid(
            np.array([self.min_range]),
            theta,
            phi
        )
        r_mesh = np.append(r_mesh, r_temp.flatten())
        theta_mesh = np.append(theta_mesh, theta_temp.flatten())
        phi_mesh = np.append(phi_mesh, phi_temp.flatten())

        # Mesh theta phi with r max
        r_temp, theta_temp, phi_temp = np.meshgrid(
            np.array([self.max_range]),
            theta,
            phi
        )
        r_mesh = np.append(r_mesh, r_temp.flatten())
        theta_mesh = np.append(theta_mesh, theta_temp.flatten())
        phi_mesh = np.append(phi_mesh, phi_temp.flatten())

        # Create a dataframe of catersian coordinates
        x, y, z = polar_to_cartesian(r_mesh, theta_mesh, phi_mesh)
        sector = pd.DataFrame({
            "x": x,
            "y": y,
            "z": z
        })

        # Generate simplicies
        simplices = generate_polar_simplices(n)

        self.sector = sector
        self.simplices = simplices

    def plot(self):
        """ Plot the radar 3D volume """
        fig = ff.create_trisurf(
            x=self.sector['x'].values, 
            y=self.sector['y'].values,
            z=self.sector['z'].values,
            simplices=self.simplices,
            colormap=[mcolors.to_hex('green')] * 2,
            show_colorbar=False
        )
        fig['data'][0].update(opacity=0.5)

        fig.update_layout(title="Searching", width=FULL_FIGURE_WIDTH, height=FULL_FIGURE_HEIGHT)
        return fig
