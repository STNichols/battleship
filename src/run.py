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

    # Create a ship
    ship = Ship(0, 0, "USS Cortado")
    ship.add_to_environment(environment)

    # Create radar
    ship.setup_radar([100, 150], [40, 60], phi=[20, 30])

    # Create a missile
    missile = Missile(current_time=t, pos_x=0, pos_y=0, pos_z=0, vel_i=200, theta=45, phi=45)
    missile.add_to_environment(environment)

    dt = 1
    while missile.exists:
        # Increment time
        t += dt
        # Update missile
        missile.update(environment, t)
        # Last step, update environment
        environment.update(t)

    # Remove missile from environment
    environment.remove_object(missile)

    print(f"\nTotal time: {t}s\n")

    # Save run logs
    os.makedirs(OUTPUT, exist_ok=True)
    environment.to_file(OUTPUT)
    ship.to_file(OUTPUT)


if __name__ == "__main__":
    run()
