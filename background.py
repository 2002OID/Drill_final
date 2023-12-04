from pico2d import *

class Background:
    def __init__(self):
        self.image = load_image('background.png')

    def update(self):
        pass

    def draw(self):

        self.image.composite_draw(0, '', 600, 300, 1200, 600)

    def get_bb(self):
        return 0, 0, 1200 - 1, 600
