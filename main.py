import matplotlib.pyplot as plt
from patterns import Patterns
import numpy as np
from standard_transforms import translate_scale_rotate_transform
def draw_pattern(patterns_meta, filename=None):
    """
    Draws multiple patterns on the same canvas after applying different sets of transformations.
    :param patterns_meta: List of dictionaries, where each dictionary contains:
                          - 'pattern': A dictionary with 'transforms' (list of transformation functions)
                                       and 'rotations' (number of rotations for the pattern).
                          - 'translations': Optional dictionary with 'x_offset', 'y_offset', 'scale_x', 'scale_y', 'rotation_angle'.
    :param filename: Optional. If provided, saves the plot to the specified filename as an SVG.
    """
    plt.figure(figsize=(8, 8))

    for meta in patterns_meta:
        pattern = meta['pattern']
        transforms = pattern['transforms']
        rotations = pattern['rotations']

        # Optional translation parameters
        translations = meta.get('translations', {})
        x_offset = translations.get('x_offset', 0)
        y_offset = translations.get('y_offset', 0)
        scale_x = translations.get('scale_x', 1.0)
        scale_y = translations.get('scale_y', 1.0)
        rotation_angle = translations.get('rotation_angle', 0)

        theta = np.linspace(0, 2 * np.pi * rotations, 50000)  # Increased resolution
        x = np.zeros_like(theta)
        y = np.zeros_like(theta)

        # Apply transformations for each set interleaved with optional translations
        for transform_func in transforms:
            # Apply the current pattern-specific transformation
            x, y = transform_func(x, y, theta)

            # Apply translation, scaling, and rotation
        x, y = translate_scale_rotate_transform(
            x, y, theta,
            x_offset=x_offset,
            y_offset=y_offset,
            scale_x=scale_x,
            scale_y=scale_y,
            rotation_angle=rotation_angle
        )

        # Plot the pattern on the same canvas
        plt.plot(x, y, lw=0.5, color='black')

    # Set plot settings
    plt.axis('equal')
    plt.axis('off')
    plt.tight_layout()

    # Save the figure as an SVG file if a filename is provided
    if filename:
        plt.savefig(filename, format='svg')

    # Display the plot
    plt.show()


def generate_pattern():
    patterns = Patterns()
    patterns_meta = [
        {
            'pattern': patterns.get_pattern('banana'),
            'translations': {
                'x_offset': 1000,
                'y_offset': 0,
                'scale_x': 1.2,
                'scale_y': 1.2,
                'rotation_angle': 15
            }
        },
        {
            'pattern': patterns.get_pattern('triangle_test'),
            # No translations (this pattern stays in its default position and size)
        },
        {
            'pattern': patterns.get_pattern('meta_spiral'),
            'translations': {
                'x_offset': 2900,

            }
        },
        {
            'pattern': patterns.get_pattern('x_ray_shell'),
            'translations': {
                'x_offset': -4900,
                'scale_x': 3,
                'scale_y': 3,
            }
        }
    ]

    draw_pattern(patterns_meta, filename="foo.svg")


def main():
    generate_pattern()


if __name__ == "__main__":
    main()
#
#
