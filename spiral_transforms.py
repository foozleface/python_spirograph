import numpy as np


def spiral_transform(x, y, theta, spiral_rate, a=1, b=1):
    """
    Transforms the drawing coordinates to create a spiral effect based on an ellipse.
    :param x: Original x coordinates
    :param y: Original y coordinates
    :param theta: Angle values
    :param spiral_rate: Rate at which the spiral grows or shrinks
    :param a: Semi-major axis of the ellipse (default is 1 for a circle)
    :param b: Semi-minor axis of the ellipse (default is 1 for a circle)
    :return: Transformed x and y coordinates
    """

    r = 1 + spiral_rate * theta  # Radial distance grows with theta
    x_transformed = x + a * r * np.cos(theta)
    y_transformed = y + b * r * np.sin(theta)
    return x_transformed, y_transformed

def spiral_oscillator(x, y, theta, spiral_rate, frequency, const=0, a=1, b=1):
    """
    Transforms the drawing coordinates to create a spiral that spirals in and out multiple times.
    Each in-and-out spiral constitutes a single cycle.

    :param x: Original x coordinates (array)
    :param y: Original y coordinates (array)
    :param theta: Angle values (array)
    :param spiral_rate: Base rate at which the spiral grows outward.
                         Determines the average radius of the spiral.
    :param frequency: (cycles/rotations) Number of in-and-out cycles in the spiral.
                   Each cycle consists of one outward spiral and one inward spiral.
                   rotations: Number of full rotations in the spiral.
                      Determines the total angle span of theta.
    :param a: Semi-major axis of the ellipse (default is 1 for a circle).
    :param b: Semi-minor axis of the ellipse (default is 1 for a circle).

    :return: Transformed x and y coordinates (arrays)
    """
    # Calculate the frequency of the oscillation based on cycles and rotations
    # frequency = cycles / rotations  # Oscillations per full rotation

    # Calculate the radial distance with oscillation for in-and-out spiraling
    # r(theta) oscillates between (spiral_rate - amplitude) and (spiral_rate + amplitude)
    # To ensure r remains positive, spiral_rate should be >= amplitude
    amplitude = spiral_rate  # Fixed amplitude for even spiraling
    r = spiral_rate + amplitude * np.sin(frequency * theta)
    # Apply the spiral transformation
    x_transformed = x + a * (r + const) * np.cos(theta)
    y_transformed = y + b * (r + const) * np.sin(theta)

    return x_transformed, y_transformed

def variable_spiral_transform(x, y, theta, start_rate, end_rate, a=1, b=1):
    """
    Transforms the drawing coordinates to create a spiral effect with a variable spiral rate based on an ellipsoid.
    :param x: Original x coordinates
    :param y: Original y coordinates
    :param theta: Angle values
    :param start_rate: Starting rate of the spiral at theta = 0
    :param end_rate: Ending rate of the spiral at theta = theta_max
    :param a: Semi-major axis of the ellipse (default is 1 for a circle)
    :param b: Semi-minor axis of the ellipse (default is 1 for a circle)
    :return: Transformed x and y coordinates
    """
    theta_max = theta[-1]
    delta_rate = end_rate - start_rate
    # Compute the cumulative radial distance r(θ)
    r = start_rate * theta + (delta_rate / (2 * theta_max)) * theta ** 2
    # Update the coordinates with ellipsoidal scaling
    x_transformed = x + a * r * np.cos(theta)
    y_transformed = y + b * r * np.sin(theta)
    return x_transformed, y_transformed


def variable_spiral_triangle_transform(x, y, theta, start_rate, end_rate, side1=1, side2=1, side3=1):
    """
    Transforms the drawing coordinates to create a spiral effect with a variable spiral rate inside a triangle.
    :param x: Original x coordinates
    :param y: Original y coordinates
    :param theta: Angle values
    :param start_rate: Starting rate of the spiral at theta = 0
    :param end_rate: Ending rate of the spiral at theta = theta_max
    :param side1: Length of the first side of the triangle (between vertex1 and vertex2)
    :param side2: Length of the second side of the triangle (between vertex2 and vertex3)
    :param side3: Length of the third side of the triangle (between vertex3 and vertex1)
    :return: Transformed x and y coordinates
    """
    # Define the vertices of the triangle based on side lengths
    vertex1 = np.array([0, 1])  # Top vertex, keeping it fixed
    vertex2 = np.array([-side1 * np.sqrt(3)/2, -0.5 * side1])  # Bottom-left vertex
    vertex3 = np.array([side3 * np.sqrt(3)/2, -0.5 * side3])  # Bottom-right vertex

    theta_max = theta[-1]
    delta_rate = end_rate - start_rate

    # Compute the cumulative radial distance r(θ)
    r = start_rate * theta + (delta_rate / (2 * theta_max)) * theta ** 2

    # Initialize transformed coordinates
    x_transformed = np.zeros_like(x)
    y_transformed = np.zeros_like(y)

    for i, angle in enumerate(theta):
        # Normalize the angle to be in the range [0, 2π]
        norm_angle = angle % (2 * np.pi)

        if norm_angle < 2 * np.pi / 3:  # First side of the triangle
            t = norm_angle / (2 * np.pi / 3)
            x_transformed[i] = (1 - t) * vertex1[0] + t * vertex2[0]
            y_transformed[i] = (1 - t) * vertex1[1] + t * vertex2[1]
        elif norm_angle < 4 * np.pi / 3:  # Second side of the triangle
            t = (norm_angle - 2 * np.pi / 3) / (2 * np.pi / 3)
            x_transformed[i] = (1 - t) * vertex2[0] + t * vertex3[0]
            y_transformed[i] = (1 - t) * vertex2[1] + t * vertex3[1]
        else:  # Third side of the triangle
            t = (norm_angle - 4 * np.pi / 3) / (2 * np.pi / 3)
            x_transformed[i] = (1 - t) * vertex3[0] + t * vertex1[0]
            y_transformed[i] = (1 - t) * vertex3[1] + t * vertex1[1]

        # Scale by the radial distance r
        x_transformed[i] = r[i] * x_transformed[i]
        y_transformed[i] = r[i] * y_transformed[i]

    return x_transformed, y_transformed



def variable_spiral_regular_ngon_transform(x, y, theta, start_rate, end_rate, side_lengths):
    """
    Transforms the drawing coordinates to create a spiral effect with a variable spiral rate inside an n-gon.

    :param x: Original x coordinates
    :param y: Original y coordinates
    :param theta: Angle values
    :param start_rate: Starting rate of the spiral at theta = 0
    :param end_rate: Ending rate of the spiral at theta = theta_max
    :param side_lengths: List of side lengths for the n-gon
    :return: Transformed x and y coordinates
    """
    n = len(side_lengths)
    theta_max = theta[-1]
    delta_rate = end_rate - start_rate

    # Compute the cumulative radial distance r(θ)
    r = start_rate * theta + (delta_rate / (2 * theta_max)) * theta ** 2

    # Define the vertices of the n-gon based on side lengths and the geometry of the polygon
    vertices = []

    # Place the first vertex at (0, 1)
    current_vertex = np.array([0, 1])
    vertices.append(current_vertex)

    current_angle = np.pi / 2  # Start pointing straight up from (0, 1)

    for i in range(1, n):
        # The previous side length and next side length
        side_a = side_lengths[i - 1]
        side_b = side_lengths[i]
        side_c = side_lengths[(i + 1) % n]  # Closing side

        # Using the law of cosines to calculate the angle between sides
        cos_angle = (side_a ** 2 + side_b ** 2 - side_c ** 2) / (2 * side_a * side_b)
        internal_angle = np.arccos(np.clip(cos_angle, -1, 1))  # Clip to handle floating point errors

        # Update the angle to the new direction
        current_angle -= internal_angle

        # Calculate the next vertex
        next_vertex = current_vertex + side_b * np.array([np.cos(current_angle), np.sin(current_angle)])
        vertices.append(next_vertex)
        current_vertex = next_vertex

    vertices = np.array(vertices)

    # Initialize transformed coordinates
    x_transformed = np.zeros_like(x)
    y_transformed = np.zeros_like(y)

    for i, angle in enumerate(theta):
        # Normalize the angle to be in the range [0, 2π]
        norm_angle = angle % (2 * np.pi)
        segment_angle = 2 * np.pi / n  # Angle per polygon segment

        # Find which side of the n-gon the point is on
        side_index = int(norm_angle // segment_angle)
        t = (norm_angle % segment_angle) / segment_angle

        # Get the start and end points of the current side
        vertex_start = vertices[side_index]
        vertex_end = vertices[(side_index + 1) % n]  # Use modulo n to wrap around

        # Linearly interpolate along the side of the polygon
        x_transformed[i] = (1 - t) * vertex_start[0] + t * vertex_end[0]
        y_transformed[i] = (1 - t) * vertex_start[1] + t * vertex_end[1]

        # Scale by the radial distance r
        x_transformed[i] *= r[i]
        y_transformed[i] *= r[i]

    return x_transformed, y_transformed


#  Not working - it can't calculate side lengths correctly
def variable_spiral_ngon_transform(x, y, theta, start_rate, end_rate, side_lengths):
    """
    Transforms the drawing coordinates to create a spiral effect with a variable spiral rate inside an n-gon.

    :param x: Original x coordinates
    :param y: Original y coordinates
    :param theta: Angle values
    :param start_rate: Starting rate of the spiral at theta = 0
    :param end_rate: Ending rate of the spiral at theta = theta_max
    :param side_lengths: List of side lengths for the n-gon
    :return: Transformed x and y coordinates
    """
    print("WARNING - this isn't working properly, it can't calc side lengths right")
    n = len(side_lengths)
    theta_max = theta[-1]
    delta_rate = end_rate - start_rate

    # Compute the cumulative radial distance r(θ)
    r = start_rate * theta + (delta_rate / (2 * theta_max)) * theta ** 2

    # Define the vertices of the n-gon based on side lengths and the geometry of the polygon
    vertices = []

    # Place the first vertex at (0, 1)
    current_vertex = np.array([0, 1])
    vertices.append(current_vertex)

    current_angle = np.pi / 2  # Start pointing straight up from (0, 1)

    for i in range(1, n):
        # The previous side length and next side length
        side_a = side_lengths[i - 1]
        side_b = side_lengths[i]
        side_c = side_lengths[(i + 1) % n]  # Closing side

        # Using the law of cosines to calculate the angle between sides
        cos_angle = (side_a ** 2 + side_b ** 2 - side_c ** 2) / (2 * side_a * side_b)
        internal_angle = np.arccos(np.clip(cos_angle, -1, 1))  # Clip to handle floating point errors

        # Update the angle to the new direction
        current_angle -= internal_angle

        # Calculate the next vertex
        next_vertex = current_vertex + side_b * np.array([np.cos(current_angle), np.sin(current_angle)])
        vertices.append(next_vertex)
        current_vertex = next_vertex

    vertices = np.array(vertices)

    # Initialize transformed coordinates
    x_transformed = np.zeros_like(x)
    y_transformed = np.zeros_like(y)

    for i, angle in enumerate(theta):
        # Normalize the angle to be in the range [0, 2π]
        norm_angle = angle % (2 * np.pi)
        segment_angle = 2 * np.pi / n  # Angle per polygon segment

        # Find which side of the n-gon the point is on
        side_index = int(norm_angle // segment_angle)
        t = (norm_angle % segment_angle) / segment_angle

        # Get the start and end points of the current side
        vertex_start = vertices[side_index]
        vertex_end = vertices[(side_index + 1) % n]  # Use modulo n to wrap around

        # Linearly interpolate along the side of the polygon
        x_transformed[i] = (1 - t) * vertex_start[0] + t * vertex_end[0]
        y_transformed[i] = (1 - t) * vertex_start[1] + t * vertex_end[1]

        # Scale by the radial distance r
        x_transformed[i] *= r[i]
        y_transformed[i] *= r[i]

    return x_transformed, y_transformed
