# 이것은 각 상태들을 객체로 구현한 것임.

from pico2d import get_time, load_image, load_font, clamp, SDL_KEYDOWN, SDL_KEYUP, SDLK_SPACE, SDLK_LEFT, SDLK_RIGHT, \
    draw_rectangle, SDLK_w, SDLK_a, SDLK_d, delay

import game_world
import game_framework
import play_mode

sheet_x = 379
sheet_y = 408
def d_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_d


def d_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_d


def a_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_a


def a_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_a


def w_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_w

def time_out(e):
    return e[0] == 'TIME_OUT'

def time_out(e):
    return e[0] == 'TIME_OUT'



# 수정 예정
PIXEL_PER_METER = (1200.0 / 14.0)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 10.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# Boy Action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 3


class Idle:

    @staticmethod
    def enter(player, e):
        if player.face_dir == -1:
            player.action = 2
        elif player.face_dir == 1:
            player.action = 3
        player.dir = 0
        player.frame = 0
        player.wait_time = get_time()  # pico2d import 필요
        pass

    @staticmethod
    def exit(player, e):
        if w_down(e):
            player.attack()
        pass

    @staticmethod
    def do(player):
        pass
        #boy.frame = (boy.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8


    @staticmethod
    def draw(player):
        player.image.clip_composite_draw(0, (sheet_y // 6) * 0 , 60, sheet_y // 6, 0, '',  player.x, player.y, 60 * 2, sheet_y // 6 * 2)


class Run:

    @staticmethod
    def enter(player, e):
        if d_down(e) or a_up(e):  # 오른쪽으로 RUN
            player.dir, player.action, player.face_dir = 1, 1, 1
        elif a_down(e) or d_up(e):  # 왼쪽으로 RUN
            player.dir, player.action, player.face_dir = -1, 0, -1

    @staticmethod
    def exit(player, e):

        pass

    @staticmethod
    def do(player):

        player.x += player.dir * RUN_SPEED_PPS * game_framework.frame_time
        player.x = clamp(50, player.x, 1200 - 50 - 1)


    @staticmethod
    def draw(player):
        player.image.clip_composite_draw(43, (sheet_y // 6) * 5 , 45, sheet_y // 6, 0, '',  player.x, player.y, 45 * 2, sheet_y // 6 * 2)




class StateMachine:
    def __init__(self, player):
        self.player = player
        self.cur_state = Idle
        self.transitions = {
            Idle: {d_down: Run, a_down: Run, a_up: Run, d_up: Run, w_down: Idle},
            Run: {d_down: Idle, a_down: Idle, d_up: Idle, a_up: Idle, w_down: Run},

        }

    def start(self):
        self.cur_state.enter(self.player, ('NONE', 0))

    def update(self):
        self.cur_state.do(self.player)

    def handle_event(self, e):
        for check_event, next_state in self.transitions[self.cur_state].items():
            if check_event(e):
                self.cur_state.exit(self.player, e)
                self.cur_state = next_state
                self.cur_state.enter(self.player, e)
                return True

        return False

    def draw(self):
        self.cur_state.draw(self.player)


class Player:
    def __init__(self):
        self.x, self.y = 150, 140
        self.face_dir = 1
        self.dir = 1
        self.delaytime = 0
        self.image = load_image('character.png')
        self.state_machine = StateMachine(self)
        self.state_machine.start()

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.handle_event(('INPUT', event))

    def draw(self):
        self.state_machine.draw()
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x - 50, self.y - 60, self.x + 10, self.y + 45

    def attack(self):
        print('attack')
        play_mode.sword.x += 20
        play_mode.update()
        play_mode.draw()
        delay(0.35)
        play_mode.sword.x -= 20

    def handle_collision(self, group, other):
        pass
