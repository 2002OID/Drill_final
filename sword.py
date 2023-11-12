# 이것은 각 상태들을 객체로 구현한 것임.

from pico2d import get_time, clamp, SDL_KEYDOWN, SDL_KEYUP, SDLK_SPACE, SDLK_LEFT, SDLK_RIGHT, \
    draw_rectangle

import game_world
import game_framework

def right_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_RIGHT


def right_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_RIGHT


def left_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_LEFT


def left_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_LEFT


def space_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_SPACE

def time_out(e):
    return e[0] == 'TIME_OUT'


# 수정 예정
PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 20.0  # Km / Hour
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
        if right_down(e) or left_up(e):  # 오른쪽으로 RUN
            sword.dir, sword.action, sword.face_dir = 1, 1, 1
        elif left_down(e) or right_up(e):  # 왼쪽으로 RUN
            sword.dir, sword.action, sword.face_dir = -1, 0, -1

    @staticmethod
    def exit(sword, e):

        pass

    @staticmethod
    def do(sword):
        # boy.frame = (boy.frame + 1) % 8
        sword.x += sword.dir * RUN_SPEED_PPS * game_framework.frame_time
        sword.x = clamp(25, sword.x, 1600 - 25)
        #boy.frame = (boy.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8

    @staticmethod
    def draw(sword):
        pass#boy.image.clip_draw(int(boy.frame) * 95, 1040 - 350, 95, 85, boy.x, boy.y)

class Idle:

    @staticmethod
    def enter(sword, e):
        if sword.face_dir == -1:
            sword.action = 2
        elif sword.face_dir == 1:
            sword.action = 3
        sword.dir = 0
        sword.frame = 0
        sword.wait_time = get_time()  # pico2d import 필요
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
        #boy.frame = (boy.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8


    @staticmethod
    def draw(sword):
        pass
        #boy.image.clip_draw(int(boy.frame) * 100, boy.action * 100, 95, 85, boy.x, boy.y)

class Attack:
    @staticmethod
    def enter(sword, e):
        print('attack')
        sword.delaytime = get_time()
        sword.x += 5
        pass

    @staticmethod
    def exit(sword, e):
        sword.x -= 5
        pass

    @staticmethod
    def update(sword, e):
        pass

    @staticmethod
    def do(sword):
        if get_time() - sword.wait_time > 1:
            sword.state_machine.handle_event(('TIME_OUT', 0))
        pass
        # boy.frame = (boy.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8

    @staticmethod
    def draw(sword):
        pass



class StateMachine:
    def __init__(self, boy):
        self.sword = boy
        self.cur_state = Idle
        self.transitions = {
            Idle: {right_down: Run, left_down: Run, left_up: Run, right_up: Run, space_down: Attack},
            Run: {right_down: Idle, left_down: Idle, right_up: Idle, left_up: Idle, space_down: Run},
            Attack: {time_out: Idle}
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
    def __init__(self, manx, many):
        self.x, self.y = manx + 30, many
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
        return self.x - 20, self.y - 10, self.x + 15, self.y + 10

    def handle_collision(self, group, other):
        pass
