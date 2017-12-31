import sys
import random
from pico2d import *


def Setstate(i):
    for boy in team:
        boy.state = 0
    team[i].state = 1


class Grass:
    def __init__(self):
        self.image = load_image('grass.png')

    def draw(self):
        self.image.draw(400, 30)


class Boy:
    image = None

    PIXEL_PER_METER = (10.0 / 0.3)
    RUN_SPEED_KMPH = 20.0
    RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
    RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

    TIME_PER_ACTION = 0.5
    ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
    FRAMES_PER_ACTION = 8

    LEFT_RUN, RIGHT_RUN, LEFT_STAND, RIGHT_STAND = 0, 1, 2, 3

    def handle_left_run(self, frame_time):
        distance = Boy.RUN_SPEED_PPS * frame_time
        self.x -= (1 * distance)
        self.total_frame += Boy.FRAMES_PER_ACTION * Boy.ACTION_PER_TIME * frame_time
        self.run_frames = int(self.total_frame) % 8
        if self.x < 0:
            self.state = self.RIGHT_RUN
            self.x = 0
        if self.run_frames >= 100:
            self.state = self.LEFT_STAND
            self.stand_frames = 0

        pass  # fill here

    def handle_left_stand(self, frame_time):
        self.total_frame += Boy.FRAMES_PER_ACTION * Boy.ACTION_PER_TIME * frame_time
        self.stand_frames = int(self.total_frame) % 8
        if self.stand_frames >= 50:
            self.state = self.LEFT_RUN
            self.run_frames = 0
        pass  # fill here

    def handle_right_run(self, frame_time):
        distance = Boy.RUN_SPEED_PPS * frame_time
        self.x += (1 * distance)
        self.total_frame += Boy.FRAMES_PER_ACTION * Boy.ACTION_PER_TIME * frame_time
        self.run_frames = int(self.total_frame) % 8
        if self.x > 800:
            self.state = self.LEFT_RUN
            self.x = 800
        if self.run_frames >= 100:
            self.state = self.RIGHT_STAND
            self.stand_frames = 0
        pass  # fill here

    def handle_right_stand(self, frame_time):
        self.total_frame += Boy.FRAMES_PER_ACTION * Boy.ACTION_PER_TIME * frame_time
        self.stand_frames = int(self.total_frame) % 8
        if self.stand_frames >= 50:
            self.state = self.RIGHT_RUN
            self.run_frames = 0
        pass  # fill here

    handle_state = {
        LEFT_RUN: handle_left_run,
        RIGHT_RUN: handle_right_run,
        LEFT_STAND: handle_left_stand,
        RIGHT_STAND: handle_right_stand
    }

    def update(self, frame_time):
        self.frame = (self.frame + 1) % 8
        self.handle_state[self.state](self, frame_time)

    def __init__(self):
        self.x, self.y = random.randint(100, 700), 90
        self.frame = random.randint(0, 7)
        self.run_frames = 0
        self.stand_frames = 0
        self.total_frame = 0.0
        self.state = self.RIGHT_RUN
        if Boy.image == None:
            Boy.image = load_image('animation_sheet.png')

    def draw(self):
        self.image.clip_draw(self.frame * 100, self.state * 100, 100, 100, self.x, self.y)


def handle_events():
    global running
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False
        elif event.type == SDL_MOUSEMOTION:
            for boy in team:
                if boy.state == 1:
                    boy.x, boy.y = event.x, 600 - event.y


def handle_events():
    global running
    global boyNum
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_DOWN and boyNum > 0:
            boyNum -= 1
        elif event.type == SDL_KEYDOWN and event.key == SDLK_UP and boyNum < 1000:
            boyNum += 1
        elif event.type == SDL_MOUSEMOTION:
            team[boyNum].x, team[boyNum].y = event.x, 600 - event.y


current_time = 0.0


def get_frame_time():
    global current_time

    frame_time = get_time() - current_time
    current_time += frame_time
    return frame_time


open_canvas()

team = [Boy() for i in range(1000)]

grass = Grass()

running = True
boyNum = 0
while running:
    frame_time = get_frame_time()

    handle_events()
    clear_canvas()
    grass.draw()
    for boy in team:
        boy.update(frame_time)
        boy.draw()
    update_canvas()

    delay(0.05)

close_canvas()