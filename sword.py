# 이것은 각 상태들을 객체로 구현한 것임.
import pico2d
from pico2d import get_time, clamp, SDL_KEYDOWN, SDL_KEYUP, draw_rectangle, delay, SDLK_w, SDLK_a, SDLK_d

import game_world
import game_framework
import play_mode


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


# 수정 예정
PIXEL_PER_METER = (1200.0 / 14.0)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 10.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# Boy Action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 6

class Run:

    @staticmethod
    def enter(sword, e):
        pass
        # if d_down(e) or a_up(e):  # 오른쪽으로 RUN
        #     sword.dir, sword.action, sword.face_dir = 1, 1, 1
        # elif a_down(e) or d_up(e):  # 왼쪽으로 RUN
        #     sword.dir, sword.action, sword.face_dir = -1, 0, -1

    @staticmethod
    def exit(sword, e):

        pass

    @staticmethod
    def do(sword):
        sword.x, sword.y = play_mode.player1.x + 30, play_mode.player1.y
        # boy.frame = (boy.frame + 1) % 8
        # sword.x += sword.dir * RUN_SPEED_PPS * game_framework.frame_time
        # sword.x = clamp(25, sword.x, 1600 - 25)


    @staticmethod
    def draw(sword):
        pass

class Idle:

    @staticmethod
    def enter(sword, e):

        pass

    @staticmethod
    def exit(sword, e):
        if w_down(e):
            sword.attack()

        pass

    @staticmethod
    def update(sword, e):

        pass

    @staticmethod
    def do(sword):
        pass



    @staticmethod
    def draw(sword):
        pass
        #boy.image.clip_draw(int(boy.frame) * 100, boy.action * 100, 95, 85, boy.x, boy.y)


class StateMachine:
    def __init__(self, sword):
        self.sword = sword
        self.cur_state = Idle
        self.transitions = {
            Idle: {d_down: Run, a_down: Run, a_up: Run, d_up: Run, w_down: Idle},
            Run: {d_down: Idle, a_down: Idle, d_up: Idle, a_up: Idle, w_down: Run},

        }

    def start(self):
        self.cur_state.enter(self.sword, ('NONE', 0))

    def update(self):
        self.cur_state.do(self.sword)

    def handle_event(self, e):
        for check_event, next_state in self.transitions[self.cur_state].items():
            if check_event(e):
                self.cur_state.exit(self.sword, e)
                self.cur_state = next_state
                self.cur_state.enter(self.sword, e)
                return True

        return False

    def draw(self):
        self.cur_state.draw(self.sword)


class Sword:
    def __init__(self):
        self.x, self.y = play_mode.player1.x + 30, play_mode.player1.y
        self.frame = 0
        # self.action = 3
        self.face_dir = 1
        self.dir = 1
        self.delaytime = 0
        #self.image = load_image('character.png')
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
        return self.x - 10, self.y - 10, self.x + 60, self.y + 20

    def attack(self):
        print('attack')
        self.x += 20
        play_mode.update()
        play_mode.draw()
        delay(0.35)
        self.x -= 20

    def handle_collision(self, group, other):
        pass
