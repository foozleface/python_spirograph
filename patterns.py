import spiral_transforms
import standard_transforms
import spirograph_transforms
from svgpathtools import svg2paths

def transform(transform_func, *args, **kwargs):
    return lambda x, y, theta: transform_func(x, y, theta, *args, **kwargs)

class Patterns():

    def __init__(self):
        self.patterns = {
            'croissant': self.create_croissant_pattern(),
            'tube': self.create_tube_pattern(),
            'simple_pent_transform': self.create_simple_pent_transform_pattern(),
            'meta_spiral': self.meta_spiral(),
            'transform_set_2': self.create_transform_set_2(),
            'triangle_test': self.create_triangle_test_pattern(),
            'classic_spirograph': self.create_classic_spirograph_pattern(),
            'rectangle_spirograph': self.create_rectangle_spirograph_pattern(),
            'n_gon_test': self.create_n_gon_test_pattern(),
            'scramble': self.create_scramble_pattern(),
            'x_ray_shell': self.create_x_ray_shell_pattern(),
            'banana': self.create_banana_pattern(),
            'another_simple_shell': self.create_another_simple_snail_pattern(),
            'create_simple_snail_pattern': self.create_simple_snail_pattern(),
            'create_sparse_shell_pattern': self.create_sparse_shell_pattern(),
        }

    def load_svg_path(self, svg_filename):
        """
        Loads the first path from an SVG file and parameterizes it.
        :param svg_filename: Path to the SVG file.
        :return: The path object.
        """
        paths, attributes = svg2paths(svg_filename)
        if not paths:
            raise ValueError("No paths found in the SVG file.")
        svg_path = paths[0]
        return svg_path

    def create_croissant_pattern(self):
        return {
            'transforms': [
                transform(spiral_transforms.spiral_oscillator, spiral_rate=390, frequency=0.00212),
                transform(standard_transforms.circular_motion, radius=1050, speed=0.0016),
                transform(standard_transforms.paper_rotation, degrees=200),
            ],
            'rotations': 235
        }

    def create_tube_pattern(self):
        return {
            'transforms': [
                transform(standard_transforms.mystery_lines, spiral_rate=390, frequency=0.00312),
                transform(standard_transforms.circular_motion, radius=950, speed=0.0046),
            ],
            'rotations': 200
        }

    def create_simple_pent_transform_pattern(self):
        return {
            'transforms': [
                transform(spirograph_transforms.spirograph_transform, R=500, r=200, d=500, mode='hypotrochoid'),
                transform(spiral_transforms.spiral_transform, spiral_rate=0.9),
                transform(standard_transforms.circular_motion, radius=100, speed=0.01),
                transform(standard_transforms.paper_rotation, degrees=30),
            ],
            'rotations': 60
        }

    def meta_spiral(self):
        return {
            'transforms': [
                transform(spiral_transforms.variable_spiral_transform, start_rate=0.01, end_rate=1.1, a=1, b=1),
                transform(standard_transforms.circular_motion, radius=950, speed=0.006),
            ],
            'rotations': 200
        }

    def create_transform_set_2(self):
        path = self.load_svg_path("single_vector.svg")
        return {
            'transforms': [
                transform(standard_transforms.svg_path_transform, path),
                transform(spirograph_transforms.spirograph_transform, R=500, r=200, d=500, mode='hypotrochoid'),
                transform(standard_transforms.circular_motion, radius=100, speed=0.001),
                transform(standard_transforms.linear_translation_transform, 400, 45),
                transform(standard_transforms.paper_rotation_transform_non_linear, degrees=70, rotation_rate_function='quadratic'),
            ],
            'rotations': 130
        }

    def create_triangle_test_pattern(self):
        return {
            'transforms': [
                transform(spiral_transforms.variable_spiral_triangle_transform, 0.9, 0.01, 1, 3, 3),
                transform(standard_transforms.linear_translation_transform, 4000, 45),
                transform(standard_transforms.paper_rotation, degrees=70),
                transform(standard_transforms.circular_motion, radius=100, speed=0.015),
            ],
            'rotations': 230
        }

    def create_classic_spirograph_pattern(self):
        return {
            'transforms': [
                transform(spirograph_transforms.spirograph_transform, R=600, r=171, d=400, mode='hypotrochoid'),
            ],
            'rotations': 30
        }

    def create_rectangle_spirograph_pattern(self):
        return {
            'transforms': [
                transform(spirograph_transforms.spirograph_rectangle_transform, 30, 30, 15, 10),
                transform(standard_transforms.paper_rotation, degrees=70),
                transform(standard_transforms.linear_translation_transform, 3000, 45),
                transform(spiral_transforms.spiral_transform, spiral_rate=0.1),
            ],
            'rotations': 120
        }

    def create_n_gon_test_pattern(self):
        return {
            'transforms': [
                transform(spiral_transforms.variable_spiral_ngon_transform, 0.9, 0.01, [1, 3, 3, 3, 3]),
                transform(standard_transforms.linear_translation_transform, 4000, 45),
                transform(standard_transforms.paper_rotation, degrees=70),
                transform(standard_transforms.circular_motion, radius=100, speed=0.015),
            ],
            'rotations': 230
        }

    def create_scramble_pattern(self):
        path = self.load_svg_path("single_vector.svg")
        return {
            'transforms': [
                transform(standard_transforms.svg_path_transform, path),
                transform(spirograph_transforms.spirograph_transform, R=500, r=200, d=500, mode='hypotrochoid'),
                transform(standard_transforms.circular_motion, radius=100, speed=0.001),
                transform(standard_transforms.linear_translation_transform, 400, 45),
                transform(standard_transforms.paper_rotation_transform_non_linear, degrees=70, rotation_rate_function='quadratic'),
            ],
            'rotations': 130
        }

    def create_x_ray_shell_pattern(self):
        return {
            'transforms': [
                transform(spirograph_transforms.spirograph_transform, R=500, r=200, d=500, mode='hypotrochoid'),
                transform(spiral_transforms.variable_spiral_transform, start_rate=0.01, end_rate=0.9),
                transform(standard_transforms.circular_motion, radius=100, speed=0.001),
                transform(spiral_transforms.spiral_oscillator, spiral_rate=30, frequency=0.035),
                transform(standard_transforms.linear_translation_transform, 700, 45),
                transform(standard_transforms.paper_rotation_transform_non_linear, degrees=90, rotation_rate_function='quadratic'),
            ],
            'rotations': 250
        }

    def create_banana_pattern(self):
        return {
            'transforms': [
                transform(spiral_transforms.spiral_oscillator, spiral_rate=390, frequency=0.00212, const=-300),
                transform(standard_transforms.circular_motion, radius=3050, speed=0.0016),
            ],
            'rotations': 230
        }


    def create_simple_snail_pattern(self):
        return {
            'transforms': [
                transform(spiral_transforms.variable_spiral_transform, start_rate=0.01, end_rate=1.1),
                transform(standard_transforms.circular_motion, radius=950, speed=0.006),
            ],
            'rotations': 200
        }

    def create_another_simple_snail_pattern(self):
        return {
            'transforms': [
                transform(spiral_transforms.spiral_oscillator, spiral_rate=390, frequency=0.00312),
                transform(standard_transforms.circular_motion, radius=950, speed=0.0046),
            ],
            'rotations': 200
        }



    def create_sparse_shell_pattern(self):
        return {
            'transforms': [
                transform(spiral_transforms.spiral_transform, spiral_rate=0.9),
                transform(standard_transforms.linear_translation_transform, 690, 45),
                transform(spirograph_transforms.spirograph_transform, R=500, r=200, d=500, mode='hypotrochoid'),
                transform(standard_transforms.circular_motion, radius=100, speed=0.01),
                transform(standard_transforms.paper_rotation_transform_non_linear, degrees=60,
                          rotation_rate_function='quadratic'),
            ],
            'rotations': 50
        }



    def get_pattern(self, name):
        return self.patterns.get(name)



# elements/examples
# lambda x, y, theta: elliptical_spirograph_transform(x, y, theta,
#                                                     R=100,
#                                                     r=r_elliptical,
#                                                     d=60,
#                                                     a=a_elliptical,
#                                                     b=b_elliptical,
#                                                     mode='epitrochoid'),
# lambda x, y, theta: svg_path_transform(x, y, theta, path),
# lambda x, y, theta: spirograph_transform(x, y, theta, R=500, r=200, d=500, mode='hypotrochoid'),  # penta figure
#
# lambda x, y, theta: variable_spiral_transform(x, y, theta, start_rate=0.01, end_rate=0.9),
#  R=700, r=100, d=700, mode='hypotrochoid'),
# lambda x, y, theta: spirograph_transform(x, y, theta, R=700, r=100, d=700, mode='hypotrochoid'),  # septa figure
#
# lambda x, y, theta: variable_spiral_transform(x, y, theta,start_rate=0.01, end_rate=0.9),
# lambda x, y, theta: circular_motion_transform(x, y, theta, radius=100, speed=0.001),
# # lambda x, y, theta: spiral_transform(x, y, theta, spiral_rate=0.9),
# lambda x, y, theta: spiral_oscillator(x, y, theta, spiral_rate=30, frequency=0.035),
#
# lambda x, y, theta: linear_translation_transform(x, y, theta, 700,45),
# # # lambda x, y, theta: spirograph_transform(x, y, theta, R=100, r=31, d=90, mode='epitrochoid'),
# #
#
# lambda x, y, theta: paper_rotation_transform_non_linear(x, y, theta, degrees=90,rotation_rate_function='quadratic'),
# # lambda x, y, theta: paper_rotation_transform(x, y, theta, degrees=200),
