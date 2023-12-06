from pico2d import *

import game_world
import game_framework
import play_mode


# Game object class here


def handle_events():

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.pop_mode()

def init():
    global helper
    helper = load_image('purse.png')


def finish():
    pass


def update():
    game_world.update()


def draw():
    clear_canvas()
    game_world.render()
    helper.draw(600, 300)
    update_canvas()

def pause():
    pass

def resume():
    pass

