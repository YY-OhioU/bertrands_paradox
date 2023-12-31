import pygame
import math
import random
import numpy as np

TAU = 2 * np.pi

pygame.init()


class SolutionBase:
    title_font = pygame.font.Font('freesansbold.ttf', 26)
    body_font = pygame.font.Font('freesansbold.ttf', 20)

    def __init__(self, app, max_count=1000):
        self.app = app
        self.surface = app.stage
        self.stop = False
        self.surface_start = (5, 5)
        self.circle_rad = 250
        self.circle_ori = np.array((int((795 - 5 - 90 - 200) / 2) + 5, 250 + 50))  # 255, 300

        self.mid_circle_rad = 100
        self.mid_circle_ori = self.circle_ori + np.array([400, -100])  # 655, 200

        self.info_msg = ""
        self.desc_title = " "
        self.desc_body = " "
        self.clock = app.clock
        self.prev_time = None

        self.max_line_count = max_count
        self.line_count = 0
        self.target_length = np.sqrt(3)
        self.qualified = 0
        self.unqualified = 0
        self.midpoints = None
        self.midpoints_coord = None
        self.lines = None

        self.solution_idx = 0

        # self.lines = None

    def init(self):
        self.qualified = 0
        self.line_count = 0
        self.unqualified = 0
        self.lines = None
        self.stop = False
        self.app.screen.blit(self.surface, (5, 5))

        # Triangle in circle
        angles = np.array([210, 330, 90])
        angles = np.deg2rad(angles)
        t_v = np.array((np.cos(angles), -1 * np.sin(angles)))
        t_v = np.swapaxes(t_v, 0, 1)
        pygame.draw.circle(self.surface, (255, 255, 255, 255), self.circle_ori, self.circle_rad, 2)
        triangle_v = self.convert_coord(t_v)
        pygame.draw.polygon(self.surface, (0, 255, 0, 255), triangle_v, width=2)
        self.gather_data()

        # Second circle
        pygame.draw.circle(self.surface, (255, 255, 255, 255), self.mid_circle_ori, self.mid_circle_rad, 2)
        self.show_desc()

    def show_desc(self):
        solution_title = f"Solution {self.solution_idx}"
        text = self.title_font.render(solution_title, True, (255, 255, 255, 255))
        text_rect = text.get_rect()
        text_rect.topleft = (5, 15)
        self.app.stage.blit(text, text_rect)

        mid_text = "Middle point of chord"
        font = pygame.font.Font("freesansbold.ttf", 20)
        text = font.render(mid_text, True, (255, 255, 255, 255))
        text_rect = text.get_rect()
        text_rect.center = (655, 320)
        self.app.stage.blit(text, text_rect)


        title = self.desc_title
        text = self.title_font.render(title, True, (0, 0, 0, 255))
        text_rect = text.get_rect()
        text_rect.topleft = (10, 10)
        self.app.control.blit(text, text_rect)

        body = self.desc_body
        start_pos = (10, 50)

        for i, line in enumerate(body):
            text = self.body_font.render(line, True, (0, 0, 0, 255))
            text_rect = text.get_rect()
            text_rect.topleft = (start_pos[0], i * 40 + start_pos[1])
            self.app.control.blit(text, text_rect)


        self.app.screen.blit(self.app.control, (5, 705))

    def convert_coord(self, coord):
        '''

        :param coord: coord (x, y) in ([-1,1], [-1,1]) with origin at circle origin
        :return: coord (x, y) in ([0,max_width_pixel], [0,max_height_pixel]) in pygame coordinate system according
        '''
        return (self.circle_rad * coord) + self.circle_ori

    def convert_mid_coord(self):
        mid_points = self.midpoints.T
        mid_coord = mid_points * self.mid_circle_rad + self.mid_circle_ori
        # mid_coord = mid_points * self.circle_rad + self.circle_ori
        self.midpoints_coord = mid_coord

    def get_points_coord_from_mid(self):
        chords = np.zeros((self.max_line_count, 2, 2))
        for i, (x0, y0) in enumerate(self.midpoints.T):
            m = -x0 / y0
            c = y0 + x0 ** 2 / y0
            # A, B, C = m ** 2 + 1, 2 * m * c, c ** 2 - self.circle_rad ** 2
            A, B, C = m ** 2 + 1, 2 * m * c, c ** 2 - 1
            d = np.sqrt(B ** 2 - 4 * A * C)
            x = np.array(((-B + d), (-B - d))) / 2 / A
            y = m * x + c
            chords[i] = (x, y)
        self.lines = chords

    def gather_data(self):
        ...

    # def
    def update(self):
        if self.line_count >= self.max_line_count:
            # self.stop = True
            # return
            self.gather_data()
            self.line_count = 0
        self.app.text_area.fill((0, 0, 0, 255))
        self.line_count += 1
        chord = self.lines[self.line_count - 1]
        mid = self.midpoints_coord[self.line_count - 1]
        x, y = chord
        if np.hypot(x[0] - x[1], y[0] - y[1]) > self.target_length:
            self.qualified += 1
        else:
            self.unqualified += 1
        info_msg = \
            f"{self.qualified}/({self.qualified}+{self.unqualified}) = {self.qualified / (self.qualified+self.unqualified):.3f}"

        chord = np.swapaxes(chord, 0, 1)
        draw_cord = self.convert_coord(chord)
        pygame.draw.line(self.surface, (227, 134, 154, 3), draw_cord[0], draw_cord[1])
        pygame.draw.circle(self.surface, (162, 160, 235, 2), mid, 3)

        text = self.app.font.render(info_msg, True, (255, 255, 255, 255))
        text_rect = text.get_rect()
        text_rect.center = (500, 50)
        self.app.text_area.blit(text, text_rect)


class Solution1(SolutionBase):
    def __init__(self, app, *args, **kwargs):
        super().__init__(app, *args, **kwargs)
        self.desc_title = 'The "random endpoints" method'
        self.desc_body = [
            "Choose two random points on the circumference of the circle and draw",
            "the chord joining them.",
            "Expected prob: 1/3"
        ]
        self.solution_idx = 1

    def gather_data(self):
        angles = np.random.random((self.max_line_count, 2)) * TAU
        chords = np.array((np.cos(angles), np.sin(angles)))
        chords = np.swapaxes(chords, 0, 1)
        self.lines = chords
        self.app.screen.blit(self.surface, (5, 5))
        self.midpoints = np.mean(chords, axis=2).T
        self.convert_mid_coord()





class Solution2(SolutionBase):
    def __init__(self, app, *args, **kwargs):
        super().__init__(app, *args, **kwargs)
        self.desc_title = 'The "random midpoint" method'
        self.desc_body = [
            "Choose a point anywhere within the circle and construct a chord with the",
            "chosen point as its midpoint.",
            "Expected prob: 1/4"
        ]
        self.solution_idx = 2

    def gather_data(self):
        angles = np.random.random(self.max_line_count) * TAU

        # sqrt because it is the area that is being randomized
        # Basically, this means we choose the area value first, and go back to radius.
        radii = np.sqrt(np.random.random(self.max_line_count))

        midpoints = np.array((radii * np.cos(angles), radii * np.sin(angles)))
        self.midpoints = midpoints
        self.convert_mid_coord()
        self.get_points_coord_from_mid()


class Solution3(SolutionBase):
    def __init__(self, app, *args, **kwargs):
        super().__init__(app, *args, **kwargs)
        self.desc_title = 'The "random radial point" method:'
        self.desc_body = [
            "Choose a radius of the circle, choose a point on the radius and construct",
            "the chord through this point and perpendicular to the radius.",
            "Expected prob: 1/2"
        ]
        self.solution_idx = 3

    def gather_data(self):
        angles = np.random.random(self.max_line_count) * TAU
        radii = np.random.random(self.max_line_count)
        midpoints = np.array((radii * np.cos(angles), radii * np.sin(angles)))
        self.midpoints = midpoints
        self.convert_mid_coord()
        self.get_points_coord_from_mid()

    # def convert_mid_coord(self):
    #     mid_points = self.midpoints.T
    #     mid_coord = mid_points * self.mid_circle_rad + self.mid_circle_ori
    #     self.midpoints_coord = mid_coord


__all__ = [
    'Solution3',
    'Solution1',
    'Solution2'
]
