from pico2d import *

import game_framework
import play_mode


class Background:
    def __init__(self):
        self.image = load_image('background.png')
        self.font = load_font('ENCR10B.TTF', 44)


    def update(self):

        pass

    def draw(self):
        self.image.composite_draw(0, '', 600, 300, 1200, 600)
        self.font.draw(500, 500, f'{play_mode.score1} : {play_mode.score2}', (0, 0, 0))
        if play_mode.score1 >= 15:
            self.font.draw(400, 300, 'player1 win', (0, 0, 0))
        elif play_mode.score2 >= 15:
            self.font.draw(400, 300, 'player2 win', (0, 0, 0))

    def get_bb(self):
        return 0, 0, 1200 - 1, 600
