from pico2d import *
import game_framework

import game_world
import purse_mode
from field import Field
from player1 import Player1
from player2 import Player2
from sword1 import Sword1
from sword2 import Sword2
from background import Background

score1 = 0
score2 = 0


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_SPACE:
            game_framework.push_mode(purse_mode)
        else:
            player1.handle_event(event)
            player2.handle_event(event)
            sword1.handle_event(event)
            sword2.handle_event(event)


def init():
    global player1, player2
    global field
    global sword1, sword2
    global background

    background = Background()
    game_world.add_object(background, 0)

    field = Field()
    game_world.add_object(field, 0)

    player1 = Player1()
    game_world.add_object(player1, 1)

    player2 = Player2()
    game_world.add_object(player2, 1)

    sword1 = Sword1()
    game_world.add_object(sword1, 1)

    sword2 = Sword2()
    game_world.add_object(sword2, 1)

    game_world.add_collision_pair('p1:s2', player1, sword2)
    game_world.add_collision_pair('p2:s1', player2, sword1)


def finish():
    game_world.remove_object(player1)
    game_world.remove_object(player2)
    game_world.remove_object(sword1)
    game_world.remove_object(sword2)
    game_world.clear()
    pass


def update():
    game_world.update()
    game_world.handle_collisions()



def draw():
    global finish_time
    clear_canvas()
    game_world.render()


    update_canvas()


def pause():
    pass


def resume():
    pass


def restart():
    finish()
    init()
