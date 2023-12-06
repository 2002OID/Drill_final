from pico2d import get_events, load_image, clear_canvas, update_canvas, get_time
import game_framework
import play_mode


def init():
    global image
    global logo_start_time

    image = load_image('tuk_credit.png')
    logo_start_time = get_time()
    pass

def finish():
    pass

def update():

    global logo_start_time
    if get_time() - logo_start_time >= 2.0:
        game_framework.change_mode(play_mode)
    pass

def draw():
    clear_canvas()
    image.composite_draw(0,'',600,300,1200,600)
    image.draw(600, 300)
    update_canvas()
    pass

def handle_events():
    events = get_events()

def pause():
        pass

def resume():
        pass
