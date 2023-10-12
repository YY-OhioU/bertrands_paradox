import pygame
from solutions import *

WINDOW_BG = (0, 0, 0, 255)
STAGE_BG = (0, 0, 0, 255)
TEXT_BG = (0, 0, 0, 255)

CONTROL_BG = (125, 125, 125, 255)
FRAME_RATE = 60


def draw_text(surface, msg, position, color=(255, 255, 255, 255), size=30):
    font = pygame.font.Font('freesansbold.ttf', size)
    text = font.render(msg, True, color)
    text_rect = text.get_rect()
    text_rect.topleft = position
    surface.blit(text, text_rect)


class MainLoop:
    def __init__(self):
        self.screen = None
        self.stage = None
        self.text_area = None
        self.control = None
        self.clock = pygame.time.Clock()
        self.playing = False
        self.current_play = None
        self.font = None
        self.sol = None
        self.solution_dict = {
            pygame.K_1: Solution1,
            pygame.K_2: Solution2,
            pygame.K_3: Solution3,
        }

    def switch_sol(self, key_id):
        if self.sol:
            self.sol.stop = True
        self.stage.fill(STAGE_BG)
        self.control.fill(CONTROL_BG)
        self.text_area.fill(TEXT_BG)
        cls = self.solution_dict[key_id]
        self.sol = cls(self)
        self.sol.init()

    def welcome(self):
        self.stage.fill(STAGE_BG)
        self.text_area.fill(TEXT_BG)
        self.control.fill(CONTROL_BG)

        msg_l1 = "Keyboard Commands:"
        msg_l2 = "1: Solution 1 (Random endpoints)"
        msg_l3 = "2: Solution 2 (Random midpoint)"
        msg_l4 = "3: Solution 3 (Random radial point)"
        msg_l5 = "Space: pulse and resume"
        msg_l6 = "0: Stop and return to this page"
        msg_l7 = "Escape: Quit"
        msg_l8 = "Press the number button to rerun the test directly"
        if self.sol:
            self.sol.stop = True
            self.sol = None

        draw_text(self.stage, msg_l1, (80, 180))
        draw_text(self.stage, msg_l2, (210, 230))
        draw_text(self.stage, msg_l3, (210, 280))
        draw_text(self.stage, msg_l4, (210, 330))
        draw_text(self.stage, msg_l5, (210, 380))
        draw_text(self.stage, msg_l6, (210, 430))
        draw_text(self.stage, msg_l7, (210, 480))
        draw_text(self.stage, msg_l8, (10, 550), size=30, color=(157, 212, 19, 255))

        self.screen.blit(self.stage, (5, 5))
        self.screen.blit(self.text_area, (5, 600))
        self.screen.blit(self.control, (5, 705))
        pygame.display.flip()

    def _init(self):
        pygame.init()
        pygame.display.set_caption("bertrands paradox")
        self.screen = pygame.display.set_mode((800, 900))
        self.screen.fill(WINDOW_BG)
        self.stage = pygame.Surface((790, 600), flags=pygame.SRCALPHA)
        self.stage.fill(STAGE_BG)
        self.text_area = pygame.Surface((790, 100), flags=pygame.SRCALPHA)
        self.text_area.fill(TEXT_BG)
        self.control = pygame.Surface((790, 190), flags=pygame.SRCALPHA)
        self.control.fill(CONTROL_BG)
        self.screen.blit(self.stage, (5, 5))
        self.screen.blit(self.text_area, (5, 600))
        self.screen.blit(self.control, (5, 705))

        pygame.display.flip()
        self.font = pygame.font.Font('freesansbold.ttf', 32)

    def main_loop(self):
        running = True
        self._init()
        self.sol = None

        self.welcome()
        while running:
            # event handling, gets all event from the event queue
            for event in pygame.event.get():
                # only do something if the event is of type QUIT
                if event.type == pygame.QUIT:
                    # change the value to `False` to exit the main loop
                    running = False
                elif event.type == pygame.KEYDOWN:
                    print(f"key down: {event.key}")
                    if event.key in (pygame.K_1, pygame.K_2, pygame.K_3):
                        self.switch_sol(event.key)
                    elif event.key == pygame.K_SPACE:
                        if self.sol:
                            self.sol.stop = not self.sol.stop
                    elif event.key == pygame.K_0:
                        self.welcome()
                    elif event.key == pygame.K_ESCAPE:
                        running = False
            if self.sol and not self.sol.stop:
                self.sol.update()
                self.screen.blit(self.stage, (5, 5))
                self.screen.blit(self.text_area, (5, 600))
            pygame.display.flip()
            self.clock.tick(60)


if __name__ == "__main__":
    # call the main function
    window = MainLoop()
    window.main_loop()
