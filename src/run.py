"""
Run the battleship simulation
"""

# Base Python
import os
import pathlib

# Battleship Python
from battleship import Environment
from battleship import Missile
from battleship import Ship

# Constants
HOME = pathlib.Path().home()
OUTPUT = HOME / "battleship_test_run"


def run():
    """ Run the simulation """

    t = 0

    environment = Environment()

    missile = Missile(current_time=t, pos_x=0, pos_y=0, pos_z=0, vel_i=100, theta=45, phi=45)
    missile.add_to_environment(environment)

    dt = 1
    while missile.exists:
        t += dt
        print(t)

        missile.update(environment, t)

        # Last step, update environment
        environment.update()

    environment.remove_object(missile)

    os.makedirs(OUTPUT, exist_ok=True)
    environment.to_file(OUTPUT)


if __name__ == "__main__":
    run()
