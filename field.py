from pico2d import *

class Field:
    def __init__(self):
        self.image = load_image('field.png')

    def update(self):
        pass

    def draw(self):

        self.image.composite_draw(0, '', 600, 27, 1200, 55)


    def get_bb(self):
        return 0, 0, 1200 - 1, 55
