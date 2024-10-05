import numpy as np

def elliptical_spirograph_transform(x, y, theta, R, r, d, a, b, mode):
    """
    Generates a spirograph pattern with an ellipse as the rolling element.
    :param x: Initial x coordinates (starting point array)
    :param y: Initial y coordinates (starting point array)
    :param theta: Array of angle values
    :param R: Radius of the fixed circle
    :param r: Characteristic 'radius' of the ellipse (can be average of a and b)
    :param d: Distance from the center of the rolling ellipse to the drawing point
    :param a: Semi-major axis of the ellipse
    :param b: Semi-minor axis of the ellipse
    :param mode: Type of spirograph ('hypotrochoid' or 'epitrochoid')
    :return: Transformed x and y coordinates (spirograph pattern)
    """
    if mode == 'hypotrochoid':
        x_transformed = x + (R - r) * np.cos(theta) + d * (a / r) * np.cos(((R - r) / r) * theta)
        y_transformed = y + (R - r) * np.sin(theta) - d * (b / r) * np.sin(((R - r) / r) * theta)
    elif mode == 'epitrochoid':
        x_transformed = x + (R + r) * np.cos(theta) - d * (a / r) * np.cos(((R + r) / r) * theta)
        y_transformed = y + (R + r) * np.sin(theta) - d * (b / r) * np.sin(((R + r) / r) * theta)
    else:
        raise ValueError("Invalid mode. Use 'hypotrochoid' or 'epitrochoid'.")
    return x_transformed, y_transformed



def spirograph_transform(x, y, theta, R, r, d, mode):
    """
    Generates spirograph pattern points from an initial point.
    :param x: Initial x coordinate (starting point)
    :param y: Initial y coordinate (starting point)
    :param theta: Array of angle values
    :param R: Radius of the fixed circle
    :param r: Radius of the rolling circle
    :param d: Distance from the center of the rolling circle to the drawing point
    :param mode: Type of spirograph ('hypotrochoid' or 'epitrochoid')
    :return: Transformed x and y coordinates (spirograph pattern)
    """

    if mode == 'hypotrochoid':
        x_transformed = x + (R - r) * np.cos(theta) + d * np.cos(((R - r) / r) * theta)
        y_transformed = y + (R - r) * np.sin(theta) - d * np.sin(((R - r) / r) * theta)
    elif mode == 'epitrochoid':
        x_transformed = x + (R + r) * np.cos(theta) - d * np.cos(((R + r) / r) * theta)
        y_transformed = y + (R + r) * np.sin(theta) - d * np.sin(((R + r) / r) * theta)
    else:
        raise ValueError("Invalid mode. Use 'hypotrochoid' or 'epitrochoid'.")
    return x_transformed, y_transformed





def polygon_spirograph_transform(x, y, theta, R, n, d, mode):
    """
    Generates a spirograph pattern with a regular polygon as the rolling element.
    :param x: Initial x coordinates (starting point array)
    :param y: Initial y coordinates (starting point array)
    :param theta: Array of angle values
    :param R: Radius of the fixed circle
    :param n: Number of sides of the rolling polygon (e.g., n=4 for a square)
    :param d: Distance from the center of the rolling polygon to the drawing point
    :param mode: Type of spirograph ('hypocyclogon' or 'epicyclogon')
    :return: Transformed x and y coordinates (spirograph pattern)
    """
    # Calculate the circumradius of the polygon
    r = R * (np.sin(np.pi / n) / (1 + np.sin(np.pi / n))) if mode == 'hypocyclogon' else R * (
                np.sin(np.pi / n) / (1 - np.sin(np.pi / n)))

    if mode == 'hypocyclogon':
        # Number of rotations the polygon makes
        rotations = (R - r) / r
        # Rotation angle of the polygon
        psi = rotations * theta
        # Angle to account for the orientation of the polygon
        phi = (theta * (R - r) / r) - psi * (2 * np.pi / n)

        # Position of the center of the polygon
        xc = (R - r) * np.cos(theta)
        yc = (R - r) * np.sin(theta)

        # Position of the point on the polygon
        x_transformed = x + xc + d * np.cos(phi)
        y_transformed = y + yc + d * np.sin(phi)

    elif mode == 'epicyclogon':
        # Number of rotations the polygon makes
        rotations = (R + r) / r
        # Rotation angle of the polygon
        psi = rotations * theta
        # Angle to account for the orientation of the polygon
        phi = (theta * (R + r) / r) - psi * (2 * np.pi / n)

        # Position of the center of the polygon
        xc = (R + r) * np.cos(theta)
        yc = (R + r) * np.sin(theta)

        # Position of the point on the polygon
        x_transformed = x + xc + d * np.cos(phi)
        y_transformed = y + yc + d * np.sin(phi)
    else:
        raise ValueError("Invalid mode. Use 'hypocyclogon' or 'epicyclogon'.")

    return x_transformed, y_transformed


def spirograph_rectangle_transform(x, y, theta, rect_width, rect_height, gear_radius, tracing_point_dist):
    """
    Transforms the drawing coordinates to create a spirograph-like pattern where a gear rolls along
    the boundary of a skinny rectangle, and its centerpoint traces a rectangular path.

    This version is chainable with other transformations.

    :param x: Original x coordinates (array)
    :param y: Original y coordinates (array)
    :param theta: Angle values (array)
    :param rect_width: Width of the rectangle
    :param rect_height: Height of the rectangle
    :param gear_radius: Radius of the "gear" that is rolling along the rectangle
    :param tracing_point_dist: Distance of the tracing point from the center of the gear
    :return: Transformed x and y coordinates (arrays)
    """

    # Initialize transformed coordinates (make copies of x and y to modify)
    x_transformed = np.copy(x)
    y_transformed = np.copy(y)

    # The total distance the gear's center moves in one full loop around the rectangle
    perimeter = 2 * (rect_width + rect_height)

    # Iterate over theta to generate the spirograph pattern
    for i, angle in enumerate(theta):
        # Calculate how far along the perimeter the gear's center has moved
        distance_along_perimeter = (gear_radius * angle) % perimeter

        # Determine which side of the rectangle the center of the gear is moving along
        if distance_along_perimeter < rect_width:  # Top side
            gear_center_x = -rect_width / 2 + distance_along_perimeter
            gear_center_y = rect_height / 2
        elif distance_along_perimeter < rect_width + rect_height:  # Right side
            gear_center_x = rect_width / 2
            gear_center_y = rect_height / 2 - (distance_along_perimeter - rect_width)
        elif distance_along_perimeter < 2 * rect_width + rect_height:  # Bottom side
            gear_center_x = rect_width / 2 - (distance_along_perimeter - (rect_width + rect_height))
            gear_center_y = -rect_height / 2
        else:  # Left side
            gear_center_x = -rect_width / 2
            gear_center_y = -rect_height / 2 + (distance_along_perimeter - (2 * rect_width + rect_height))

        # Calculate the rotation of the tracing point on the gear
        gear_rotation = angle * (rect_width + rect_height) / gear_radius

        # Update the transformed x and y coordinates with the tracing point, rotating around the gear's center
        x_transformed[i] += gear_center_x + tracing_point_dist * np.cos(gear_rotation)
        y_transformed[i] += gear_center_y + tracing_point_dist * np.sin(gear_rotation)

    return x_transformed, y_transformed


def elliptical_spirograph_transform(x, y, theta, R, r, d, a, b, mode):
    """
    Generates a spirograph pattern with an ellipse as the rolling element.
    :param x: Initial x coordinates (starting point array)
    :param y: Initial y coordinates (starting point array)
    :param theta: Array of angle values
    :param R: Radius of the fixed circle
    :param r: Characteristic 'radius' of the ellipse (can be average of a and b)
    :param d: Distance from the center of the rolling ellipse to the drawing point
    :param a: Semi-major axis of the ellipse
    :param b: Semi-minor axis of the ellipse
    :param mode: Type of spirograph ('hypotrochoid' or 'epitrochoid')
    :return: Transformed x and y coordinates (spirograph pattern)
    """
    if mode == 'hypotrochoid':
        x_transformed = x + (R - r) * np.cos(theta) + d * (a / r) * np.cos(((R - r) / r) * theta)
        y_transformed = y + (R - r) * np.sin(theta) - d * (b / r) * np.sin(((R - r) / r) * theta)
    elif mode == 'epitrochoid':
        x_transformed = x + (R + r) * np.cos(theta) - d * (a / r) * np.cos(((R + r) / r) * theta)
        y_transformed = y + (R + r) * np.sin(theta) - d * (b / r) * np.sin(((R + r) / r) * theta)
    else:
        raise ValueError("Invalid mode. Use 'hypotrochoid' or 'epitrochoid'.")
    return x_transformed, y_transformed



def spirograph_transform(x, y, theta, R, r, d, mode):
    """
    Generates spirograph pattern points from an initial point.
    :param x: Initial x coordinate (starting point)
    :param y: Initial y coordinate (starting point)
    :param theta: Array of angle values
    :param R: Radius of the fixed circle
    :param r: Radius of the rolling circle
    :param d: Distance from the center of the rolling circle to the drawing point
    :param mode: Type of spirograph ('hypotrochoid' or 'epitrochoid')
    :return: Transformed x and y coordinates (spirograph pattern)
    """

    if mode == 'hypotrochoid':
        x_transformed = x + (R - r) * np.cos(theta) + d * np.cos(((R - r) / r) * theta)
        y_transformed = y + (R - r) * np.sin(theta) - d * np.sin(((R - r) / r) * theta)
    elif mode == 'epitrochoid':
        x_transformed = x + (R + r) * np.cos(theta) - d * np.cos(((R + r) / r) * theta)
        y_transformed = y + (R + r) * np.sin(theta) - d * np.sin(((R + r) / r) * theta)
    else:
        raise ValueError("Invalid mode. Use 'hypotrochoid' or 'epitrochoid'.")
    return x_transformed, y_transformed