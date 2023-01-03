"""
Class representing a 3D enviroment containing various objects
"""

# Base Python
import os

# Extended Python
import numpy as np
import pandas as pd

# Constants
OBJECT_ID_COL = 3
POS_X_COL = 0
POS_Y_COL = 1
POS_Z_COL = 2
STATE_COLUMNS = ["pos_x", "pos_y", "pos_z", "object_id", "time"]
ENVIRONMENT_STATE_NAME = "environment.csv"


class Environment:

    def __init__(self):
        """ Initialize the environment """
        self.current_time = 0
        self.next_object_id = 1

        # Create objest state table
        self.object_states = np.array([np.array([0, 0, 0, 0])])

        object_timeline = self.object_states
        object_timeline = np.hstack([
            object_timeline, 
            np.array([np.array([self.current_time])])
        ])
        self.object_timeline = object_timeline

    def create_new_object(self, pos_x, pos_y, pos_z):
        """ Add a new object to the environment"""
        object_id = self.next_object_id
        self.next_object_id += 1

        # Add new entry to object states
        obj_array = np.array([pos_x, pos_y, pos_z, object_id])
        new_states = np.vstack([self.object_states, obj_array])
        self.object_states = new_states

        return object_id

    def remove_object(self, object):
        """ Remove an object from environment """
        object_id = object.get_object_id()
        is_not_object = self.object_states[:, OBJECT_ID_COL] != object_id
        self.object_states = self.object_states[is_not_object]

    def to_file(self, output):
        """ Save object timeline to file """
        table = pd.DataFrame(
            self.object_timeline,
            columns=STATE_COLUMNS
        )
        name = os.path.join(output, ENVIRONMENT_STATE_NAME)
        print(name)
        table.to_csv(name)

    def update_object_state(self, pos_x, pos_y, pos_z, object_id):
        """ Update the state of an object """
        is_object = self.object_states[:, OBJECT_ID_COL] == object_id
        self.object_states[is_object, :OBJECT_ID_COL] = np.array([pos_x, pos_y, pos_z])

    def update(self):
        """ Add current object states to object timeline """
        obj_states = self.object_states
        obj_times = np.ones((obj_states.shape[0], 1))
        obj_states = np.hstack([obj_states, obj_times])

        self.object_timeline = np.vstack([
            self.object_timeline, 
            obj_states
        ])
