"""
Various utilities for spatial operations
"""

# Extended Python
import numpy as np


def generate_polar_simplices(n):
	"""
	-- FOR TOP AND BOTTOM FACES --

	near bottom: i * n for i in [0, n - 1]
	far bottom:  i * n for i in [n, 2n - 1]

	near top: i * n - 1 for i in [1, n + 1]
	far top:  i * n - 1 for i in [n + 1, 2n + 1]

	-- FOR LEFT AND RIGHT SIDE FACES --

	near left: [0, n-1]
	far left: [n^2, n^2 + n - 1]

	near right: [n^2 - n, n^2 - 1]
	far right: [2n^2 -n , 2n^2 - 1]

	Then, given any two arrays x and y:

	[ x[i], x[i + 1], y[i + 1] ]  <- first half of triangles
	[ y[i], y[i + 1], x[i]     ]  <- second half of triangles
	"""
	# Bottom and top rows
	near_bottom = [i * n for i in range(n)]
	far_bottom = [i * n for i in range(n, 2 * n)]
	near_top = [i * n - 1 for i in range(1, n + 1)]
	far_top = [i * n - 1 for i in range(n + 1, 2 * n + 1)]

	# Left and right rows
	near_right = [i for i in range(n)]
	far_right = [i for i in range(n ** 2, n ** 2 + n)]
	near_left = [i for i in range(n ** 2 - n, n ** 2)]
	far_left = [i for i in range(2 * n ** 2 - n, 2 * n ** 2)]

	simplices = []
	simplices.extend(make_face_simplices(near_right, far_right, n))    # Right face
	simplices.extend(make_face_simplices(near_left, far_left, n))      # Left face
	simplices.extend(make_face_simplices(near_top, far_top, n))        # Top face
	simplices.extend(make_face_simplices(near_bottom, far_bottom, n))  # Bottom face
	simplices.extend(make_face_simplices(near_bottom, near_top, n))    # Top face
	simplices.extend(make_face_simplices(far_bottom, far_top, n))      # Bottom face

	# Stack in N x 3 matrix
	simplices = np.vstack(simplices)

	return simplices


def make_face_simplices(array_a, array_b, n):
    """
    Create all triagulations of a face between two arrays

    A-------B---o ...
    |\      |
    | \  1  |     
    |  \    |
    |   \   |     ...
    | 2  \  |
    |     \ |
    C-------D---o ...

    (A, B, D) creates triangle 1
    (A, C, D) creates triangle 2
    
    ... repeat for face between full arrays

    """
    simplices = []
    # First Half
    for i in range(n - 1):
        s = np.array([array_a[i], array_a[i + 1], array_b[i]])
        simplices.append(s)

    # Second Half
    for i in range(n - 1):
        s = np.array([array_b[i], array_b[i + 1], array_a[i + 1]])
        simplices.append(s)
    
    return simplices


def polar_to_cartesian(r, theta, phi):
    """ Convert polar coordinates to cartesian """
    theta_rad = np.deg2rad(theta)
    phi_rad = np.deg2rad(phi)

    x = r * np.cos(phi_rad) * np.cos(theta_rad)
    y = r * np.cos(phi_rad) * np.sin(theta_rad)
    z = r * np.sin(phi_rad)

    return x, y, z
