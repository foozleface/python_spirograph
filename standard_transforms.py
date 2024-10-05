import numpy as np

def circular_motion(x, y, theta, radius=50, speed=0.01):
    """
    Transforms the drawing coordinates by simulating drawing on a piece of paper
    that is rotating in a circular motion.
    :param x: Original x coordinates
    :param y: Original y coordinates
    :param theta: Angle values
    :param radius: Radius of the circular motion
    :param speed: Speed of the circular motion
    :return: Transformed x and y coordinates
    """
    x_transformed = x + radius * np.cos(speed * theta)
    y_transformed = y + radius * np.sin(speed * theta)
    return x_transformed, y_transformed


def translate_scale_rotate_transform(x, y, theta, x_offset=0, y_offset=0, scale_x=1.0, scale_y=1.0, rotation_angle=0):
    """
    Transforms the drawing coordinates to translate, scale (independently in x and y), and rotate the entire pattern.
    :param x: Original x coordinates
    :param y: Original y coordinates
    :param theta: Angle values (not used in this transform but required for consistency)
    :param x_offset: The distance to move the pattern along the x-axis (positive moves right, negative moves left)
    :param y_offset: The distance to move the pattern along the y-axis (positive moves up, negative moves down)
    :param scale_x: Factor by which to scale the pattern along the x-axis (values > 1 enlarge, < 1 shrink)
    :param scale_y: Factor by which to scale the pattern along the y-axis (values > 1 enlarge, < 1 shrink)
    :param rotation_angle: The angle to rotate the pattern in degrees (counterclockwise)
    :return: Transformed x and y coordinates
    """
    # Scale the pattern independently along x and y axes
    x_transformed = x * scale_x
    y_transformed = y * scale_y

    # Convert the rotation angle to radians
    rotation_radians = np.deg2rad(rotation_angle)

    # Rotate the pattern
    x_rotated = x_transformed * np.cos(rotation_radians) - y_transformed * np.sin(rotation_radians)
    y_rotated = x_transformed * np.sin(rotation_radians) + y_transformed * np.cos(rotation_radians)

    # Translate the pattern
    x_final = x_rotated + x_offset
    y_final = y_rotated + y_offset

    return x_final, y_final



def paper_rotation(x, y, theta, degrees):
    """
    Transforms the drawing coordinates to simulate the paper rotating during the drawing process.
    """
    total_rotation_radians = np.deg2rad(degrees)
    theta_max = theta[-1]
    phi = (theta / theta_max) * total_rotation_radians
    x_transformed = x * np.cos(phi) - y * np.sin(phi)
    y_transformed = x * np.sin(phi) + y * np.cos(phi)
    return x_transformed, y_transformed

def mystery_lines(x,y,theta,spiral_rate, frequency):
    amplitude = spiral_rate  # Fixed amplitude for even spiraling
    r = spiral_rate + amplitude * np.sin(frequency * theta)

    # Apply the spiral transformation
    x_transformed = x + r * np.sin(theta)
    y_transformed = y + r * np.sin(theta)

    return x_transformed, y_transformed



def linear_translation_transform(x, y, theta, total_distance, movement_angle_degrees):
    """
    Transforms the drawing coordinates to move the diagram along a straight line during drawing.
    :param x: Original x coordinates.
    :param y: Original y coordinates.
    :param theta: Array of angle values representing the drawing progression.
    :param total_distance: Total distance to move the diagram during the drawing process.
    :param movement_angle_degrees: Angle (in degrees) along which to move the diagram.
    :return: Transformed x and y coordinates.
    """
    # Convert angle from degrees to radians
    movement_angle = np.deg2rad(movement_angle_degrees)

    # Calculate the maximum value of theta
    theta_max = theta[-1]

    # Compute normalized progression p(theta)
    p = theta / theta_max

    # Compute translation amounts
    delta_x = p * total_distance * np.cos(movement_angle)
    delta_y = p * total_distance * np.sin(movement_angle)

    # Apply translation to x and y
    x_transformed = x + delta_x
    y_transformed = y + delta_y

    return x_transformed, y_transformed



def paper_rotation_transform_non_linear(x, y, theta, degrees, rotation_rate_function):
    """
    Transforms the drawing coordinates to simulate the paper rotating during the drawing process with a non-linear rotation rate.
    :param x: Original x coordinates
    :param y: Original y coordinates
    :param theta: Angle values (progress parameter)
    :param degrees: Total rotation angle of the paper in degrees during the drawing process.
    :param rotation_rate_function: Defines the rotation rate ('linear', 'quadratic', 'sinusoidal', or a custom function).
    :return: Transformed x and y coordinates.
    """
    total_rotation_radians = np.deg2rad(degrees)
    theta_max = theta[-1]
    normalized_theta = theta / theta_max  # Normalize theta to range from 0 to 1

    if rotation_rate_function == 'linear':
        phi = normalized_theta * total_rotation_radians
    elif rotation_rate_function == 'quadratic':
        phi = normalized_theta ** 2 * total_rotation_radians
    elif rotation_rate_function == 'sinusoidal':
        phi = np.sin(normalized_theta * np.pi / 2) * total_rotation_radians
    elif callable(rotation_rate_function):
        phi_normalized = rotation_rate_function(normalized_theta)
        # Ensure phi_normalized is within [0, 1]
        phi_normalized = np.clip(phi_normalized, 0, 1)
        phi = phi_normalized * total_rotation_radians
    else:
        raise ValueError(
            "Invalid rotation_rate_function. Use 'linear', 'quadratic', 'sinusoidal', or provide a function.")

    x_transformed = x * np.cos(phi) - y * np.sin(phi)
    y_transformed = x * np.sin(phi) + y * np.cos(phi)
    return x_transformed, y_transformed


def svg_path_transform(x, y, theta, svg_path, scale=1.0, offset_x=0.0, offset_y=0.0):
    """
    Transforms the drawing coordinates to trace along the SVG path efficiently.
    :param x: Original x coordinates.
    :param y: Original y coordinates.
    :param theta: Array of angle values representing the drawing progression.
    :param svg_path: The SVG Path object to trace along.
    :param scale: Scaling factor for the SVG path.
    :param offset_x: X-axis offset for the SVG path.
    :param offset_y: Y-axis offset for the SVG path.
    :return: Transformed x and y coordinates.
    """
    # Normalize theta to range from 0 to 1
    theta_normalized = theta / theta[-1]

    # Total length of the SVG path
    total_length = svg_path.length()

    # Compute the corresponding distances along the path for each theta
    distances = theta_normalized * total_length

    # Precompute t values and cumulative lengths
    num_samples = 10000  # Adjust based on desired accuracy and performance
    t_vals = np.linspace(0, 1, num_samples)
    cumulative_lengths = np.array([svg_path.length(0, t) for t in t_vals])

    # Ensure cumulative_lengths is strictly increasing for interpolation
    # This avoids potential issues with np.interp
    cumulative_lengths = np.maximum.accumulate(cumulative_lengths)

    # Handle any potential floating-point inaccuracies
    cumulative_lengths[-1] = total_length

    # Interpolate to find t for each desired distance
    t_values = np.interp(distances, cumulative_lengths, t_vals)

    # Get the points on the path at the specified t values using list comprehension
    # This avoids passing an array to svg_path.point, which expects scalar t
    points = [svg_path.point(t) for t in t_values]

    # Extract x and y coordinates from the points
    path_x = np.array([point.real for point in points])
    path_y = np.array([point.imag for point in points])

    # Apply scaling and offset
    path_x = path_x * scale + offset_x
    path_y = path_y * scale + offset_y

    return path_x, path_y

