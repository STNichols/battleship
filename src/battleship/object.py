"""
Abstract base class for any objects
"""

# Base Python
from abc import ABC, abstractmethod

# Constants
ORIGIN = 0

class Object(ABC):

    def __init__(self, pos_x=ORIGIN, pos_y=ORIGIN, pos_z=ORIGIN):
        self._object_id = None
        self._exists = True

        self.pos_x = pos_x
        self.pos_y = pos_y
        self.pos_z = pos_z

        self.color = None

    @property
    def exists(self):
        """ If the object still exists """
        return self._exists

    def get_color(self):
        """ Get the objects color """
        return self.color

    def get_current_position(self):
        """ Return the current position of the object """
        return self.pos_x, self.pos_y, self.pos_z

    def get_object_id(self):
        """ Getter for object's id """
        return self._object_id

    def set_color(self, color):
        """ Set color for object """
        self.color = color

    def set_object_id(self, object_id):
        """ Setter for object's id """
        self._object_id = object_id

    @abstractmethod
    def update(self):
        pass
