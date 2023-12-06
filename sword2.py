# 이것은 각 상태들을 객체로 구현한 것임.
import pico2d
from pico2d import get_time, clamp, SDL_KEYDOWN, SDL_KEYUP, draw_rectangle, delay, SDLK_i, SDLK_j, SDLK_l

import game_world
import game_framework
import play_mode


def l_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_l


def l_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_l


def j_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_j


def j_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_j


def i_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_i


def time_out(e):
    return e[0] == 'TIME_OUT'


# 수정 예정
PIXEL_PER_METER = (1200.0 / 14.0)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 5.0  # Km / Hour
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

    @staticmethod
    def exit(sword, e):
        pass

    @staticmethod
    def do(sword):
        sword.x, sword.y = play_mode.player2.x - 30, play_mode.player2.y

    @staticmethod
    def draw(sword):
        pass


class Idle:

    @staticmethod
    def enter(sword, e):
        pass

    @staticmethod
    def exit(sword, e):
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
        # boy.image.clip_draw(int(boy.frame) * 100, boy.action * 100, 95, 85, boy.x, boy.y)


class StateMachine:
    def __init__(self, sword):
        self.sword = sword
        self.cur_state = Idle
        self.transitions = {
            Idle: {l_down: Run, j_down: Run, j_up: Run, l_up: Run, i_down: Idle},
            Run: {l_down: Idle, j_down: Idle, l_up: Idle, j_up: Idle, i_down: Run},

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


class Sword2:
    def __init__(self):
        self.x, self.y = play_mode.player2.x - 30, play_mode.player2.y
        self.dir = 1
        self.state_machine = StateMachine(self)
        self.state_machine.start()

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.handle_event(('INPUT', event))

    def draw(self):
        self.state_machine.draw()
        # draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x - 30, self.y, self.x + 10, self.y + 15

    def handle_collision(self, group, other):
        match group:
            case 'p1:s2':
                print('p2 win')
                play_mode.score2 += 1
                play_mode.restart()
