import pygame
from solutions import *

WINDOW_BG = (0, 0, 0, 255)
STAGE_BG = (0, 0, 0, 255)
text_BG = (0, 0, 0, 255)

CONTROL_BG = (125, 125, 125, 255)
FRAME_RATE = 60


class MainLoop:
    def __init__(self):
        self.screen = None
        self.stage = None
        self.control = None
        self.clock = pygame.time.Clock()
        self.playing = False
        self.current_play = None
        self.font = None

    def _init(self):
        pygame.init()
        pygame.display.set_caption("bertrands paradox")
        self.screen = pygame.display.set_mode((800, 900))
        self.screen.fill(WINDOW_BG)
        self.stage = pygame.Surface((790, 600), flags=pygame.SRCALPHA)
        self.stage.fill(STAGE_BG)
        self.text_area = pygame.Surface((790, 200), flags=pygame.SRCALPHA)
        self.text_area.fill(text_BG)
        self.control = pygame.Surface((790, 90))
        self.control.fill(CONTROL_BG)
        self.screen.blit(self.stage, (5, 5))
        self.screen.blit(self.control, (5, 805))
        self.screen.blit(self.text_area, (5, 600))
        pygame.display.flip()
        self.font = pygame.font.Font('freesansbold.ttf', 32)
        # pygame.display.update()

    def main_loop(self):
        running = True
        self._init()
        sol = Solution3(self)
        sol.init()
        # main loop
        # text = self.font.render('test', True, (255, 255, 255, 255))
        # text_rect = text.get_rect()
        # text_rect.center = (50, 50)
        # self.text_area.blit(text, text_rect)
        while running:
            # event handling, gets all event from the event queue
            # self.screen.fill((0, 255, 255, 255))
            # self.text_area.fill(text_BG)
            for event in pygame.event.get():
                # only do something if the event is of type QUIT
                if event.type == pygame.QUIT:
                    # change the value to `False` to exit the main loop
                    running = False
            if sol and sol.stop:
                del sol
                sol = None
            #     self.stage.fill(STAGE_BG)
            if sol:
                sol.update()
                self.screen.blit(self.stage, (5, 5))
                self.screen.blit(self.text_area, (5, 600))
            pygame.display.flip()
            self.clock.tick(60)


# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__ == "__main__":
    # call the main function
    window = MainLoop()
    window.main_loop()
