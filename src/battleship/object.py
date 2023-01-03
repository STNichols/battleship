"""
Abstract base class for any objects
"""

# Base Python
from abc import ABC, abstractmethod

class Object(ABC):

    def get_object_id(self):
        return self._object_id

    @abstractmethod
    def update(self):
        pass
