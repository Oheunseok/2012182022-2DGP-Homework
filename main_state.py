import random
import json
import os

from pico2d import *

import game_framework
import title_state



name = "MainState"
class Grass:
    def __init__(self):
        self.image = load_image('grass.png')

    def draw(self):
        self.image.draw(400, 30)

class Background:
    PIXEL_PER_METER = (10.0 / 0.3)
    SCROLL_SPEED_KMPH = 20.0
    SCROLL_SPEED_MPM = (SCROLL_SPEED_KMPH * 1000.0 / 60.0)
    SCROLL_SPEED_MPS = (SCROLL_SPEED_MPM / 60.0)
    SCROLL_SPEED_PPS = (SCROLL_SPEED_MPS * PIXEL_PER_METER)

    def __init__(self, w, h):
        self.image = load_image('background.png')
        self.speed = 0
        self.left = 0
        self.screen_width = w
        self.screen_height = h

    def draw(self):
        pass

    def update(self, frame_time):
        pass

    def handle_event(self, event):
        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_LEFT: self.speed -= Background.SCROLL_SPEED_PPS
            elif event.key == SDLK_RIGHT: self.speed += Background.SCROLL_SPEED_PPS
        if event.type == SDL_KEYUP:
            if event.key == SDLK_LEFT: self.speed += Background.SCROLL_SPEED_PPS
            elif event.key == SDLK_RIGHT: self.speed -= Background.SCROLL_SPEED_PPS


class TileBackground:

    SCROLL_SPEED_PPS = 1

    def __init__(self, width, height):
        self.tile_map = load_tile_map('field.json')
        self.speed = 0
        self.left = 0
        self.width = width
        self.height = height

    def draw(self):
        x = self.left
        w = min(self.tile_map.map_width - x, self.width)
        self.tile_map.clip_draw_to_origin(x,0,w,self.height,0,0)
        self.tile_map.clip_draw_to_origin(0,0,self.width - w, self.height,w,0)

        pass

    def update(self, frame_time):
        self.left = (self.left + self.speed) % self.tile_map.map_width
        pass

    def handle_event(self, event):
        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_LEFT: self.speed -= TileBackground.SCROLL_SPEED_PPS
            elif event.key == SDLK_RIGHT: self.speed += TileBackground.SCROLL_SPEED_PPS
        if event.type == SDL_KEYUP:
            if event.key == SDLK_LEFT: self.speed += TileBackground.SCROLL_SPEED_PPS
            elif event.key == SDLK_RIGHT: self.speed -= TileBackground.SCROLL_SPEED_PPS

class Boy:
    image = None

    LEFT_RUN, RIGHT_RUN, LEFT_STAND, RIGHT_STAND = 0, 1, 2, 3

    def handle_left_run(self):
        self.x -= 5
        self.run_frames += 1
        if self.x < 0:
            self.state = self.RIGHT_RUN
            self.x = 0

    def handle_left_stand(self):
        self.stand_frames += 1
        if self.stand_frames == 50:
#            self.state = self.LEFT_RUN
            self.run_frames = 0

    def handle_right_run(self):
        self.x += 5
        self.run_frames += 1
        if self.x > 800:
            self.state = self.LEFT_RUN
            self.x = 800

    def handle_right_stand(self):
        self.stand_frames += 1
        if self.stand_frames == 50:
#            self.state = self.RIGHT_RUN
            self.run_frames = 0

    def handle_event(self, event):
        # fill here
        if(event.type, event.key) == (SDL_KEYDOWN, SDLK_LEFT):
            if self.state in (self.RIGHT_STAND, self.LEFT_STAND):
                self.state = self.LEFT_RUN
        elif(event.type, event.key) == (SDL_KEYDOWN, SDLK_RIGHT):
            if self.state in (self.RIGHT_STAND, self.LEFT_STAND):
                self.state = self.RIGHT_RUN
        elif (event.type, event.key) == (SDL_KEYUP, SDLK_LEFT):
            if self.state == self.LEFT_RUN:
                self.state = self.LEFT_STAND
            elif self.state == self.RIGHT_RUN:
                self.state = self.RIGHT_STAND
        elif (event.type, event.key) == (SDL_KEYUP, SDLK_RIGHT):
            if self.state == self.LEFT_RUN:
                self.state = self.LEFT_STAND
            elif self.state == self.RIGHT_RUN:
                self.state = self.RIGHT_STAND

    handle_state = {
                LEFT_RUN: handle_left_run,
                RIGHT_RUN: handle_right_run,
                LEFT_STAND: handle_left_stand,
                RIGHT_STAND: handle_right_stand
    }

    def update(self):
        self.frame = (self.frame + 1) % 8
        self.handle_state[self.state](self)


    def __init__(self):
        self.x, self.y = random.randint(100, 700), 90
        self.frame = random.randint(0, 7)
        self.run_frames = 0
        self.stand_frames = 0
        self.state = self.RIGHT_RUN
        self.name = 'noname'
        if Boy.image == None:
            Boy.image = load_image('animation_sheet.png')

    def draw(self):
        self.image.clip_draw(self.frame * 100, self.state * 100, 100, 100, self.x, self.y)


def handle_events():
    global running
    global boy
    global boyNum
    global team
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_UP and boyNum < 5:
            boyNum += 1
        elif event.type == SDL_KEYDOWN and event.key == SDLK_DOWN and boyNum > 0:
            boyNum -= 1
        elif event.type == SDL_KEYDOWN or event.type == SDL_KEYUP:
            team[boyNum].handle_event(event)




# team FACTORY

def create_team():

    player_state_tabel = {
        "LEFT_RUN" : Boy.LEFT_RUN,
        "RIGHT_RUN" : Boy.RIGHT_RUN,
        "LEFT_STAND" : Boy.LEFT_STAND,
        "RIGHT_STAND" : Boy.RIGHT_STAND
    }

    team_data_file = open('team_data.txt', 'r')
    team_data = json.load(team_data_file)
    team_data_file.close()

    team = []

    for name in team_data:
        player = Boy()
        player.name = name
        player.x = team_data[name]['x']
        player.y = team_data[name]['y']
        player.state = player_state_tabel[team_data[name]['StartState']]
        team.append(player)

    return team

def main():

    open_canvas()

    global boy
    global running
    global team
    global boyNum

    team = create_team()

    boyNum = 0

    grass = Grass()

    running = True
    while running:
        handle_events()

        for player in team:
            player.update()

        clear_canvas()
        grass.draw()
        for player in team:
            player.draw()
        update_canvas()

        delay(0.04)

    close_canvas()


if __name__ == '__main__':
    main()
boy = None
grass = None
font = None
running = None


class Grass:
    def __init__(self):
        self.image = load_image('grass.png')

    def draw(self):
        self.image.draw(400, 30)



class Boy:
    def __init__(self):
        self.x, self.y = 0, 90
        self.frame = 0
        self.image = load_image('run_animation.png')
        self.dir = 1

    def update(self):
        self.frame = (self.frame + 1) % 8
        self.x += self.dir
        if self.x >= 800:
            self.dir = -1
        elif self.x <= 0:
            self.dir = 1

    def draw(self):
        self.image.clip_draw(self.frame * 100, 0, 100, 100, self.x, self.y)


def enter():
    global boy, grass
    boy = Boy()
    grass = Grass()
    pass


def exit():
    global boy, grass
    del(boy)
    del(grass)
    pass


def pause():
    pass


def resume():
    pass


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.change_state(title_state)

    pass


def update():
    boy.update()
    pass


def draw():
    clear_canvas()
    grass.draw()
    boy.draw()
    update_canvas()
    pass





