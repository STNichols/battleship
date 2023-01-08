"""
Missile Class for simulating a missile
"""

# Extended Python
import numpy as np

# Battleship Python
from battleship.object import Object
from battleship.params import ACC_GRAVITY


class Missile(Object):

    def __init__(self, current_time, pos_x, pos_y, pos_z, vel_i, theta, phi):
        """ Initialize a missile object """
        super(Missile, self).__init__(pos_x=pos_x, pos_y=pos_y, pos_z=pos_z)
        self.current_time = current_time

        # Breakdown velocity vector to cartesian components
        self.vel_z = vel_i * np.sin(np.deg2rad(phi))
        vel_xy = vel_i * np.cos(np.deg2rad(phi))
        self.vel_x = vel_xy * np.cos(np.deg2rad(theta))
        self.vel_y = vel_xy * np.sin(np.deg2rad(theta))

    def add_to_environment(self, environment):
        """ Add object within environment """
        object_id = environment.create_new_object(*self.get_current_position())
        self.set_object_id(object_id)

    def propogate(self, time_delta):
        """ Propogate the trajectory for the increment of time passed """
        # Calculate new positions
        self.pos_x = self.pos_x + (self.vel_x * time_delta)  # ignore friction
        self.pos_y = self.pos_y + (self.vel_y * time_delta)  # ignore friction
        self.pos_z = self.pos_z + (self.vel_z * time_delta) + (0.5 * ACC_GRAVITY * time_delta ** 2)

        # Calculate new velocities (ignore friction, only z-component changes)
        self.vel_z = self.vel_z + (ACC_GRAVITY * time_delta)

        if self.pos_z <= 0:
            self._exists = False

    def update(self, environment, new_time):
        """ Update the missile object """
        time_delta = new_time - self.current_time
        self.current_time = new_time

        self.propogate(time_delta)

        environment.update_object_state(*self.get_current_position(), self.get_object_id())
