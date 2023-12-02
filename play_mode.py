import random

from pico2d import *
import game_framework

import game_world
from field import Field
from player import Player
from sword import Sword


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        else:
            player1.handle_event(event)
            sword.handle_event(event)

def init():
    global player1
    global field
    global sword

    field = Field()
    game_world.add_object(field, 0)

    player1 = Player()
    game_world.add_object(player1, 1)



    sword = Sword()
    game_world.add_object(sword, 1)


def finish():
    game_world.clear()
    pass


def update():
    game_world.update()
    game_world.handle_collisions()


def draw():
    clear_canvas()
    game_world.render()
    update_canvas()

def pause():
    pass

def resume():
    pass

