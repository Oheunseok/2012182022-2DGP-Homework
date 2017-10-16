# json_players.py : load player data from .json file

import random
import json
from pico2d import *

running = None

class Grass:
    def __init__(self):
        self.image = load_image('grass.png')

    def draw(self):
        self.image.draw(400, 30)


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
