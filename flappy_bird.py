import pygame
import random
import os


# bird object
class Bird:
    def __init__(self, bird_object):
        self.x = window_width/4         # x-axis of bird
        self.y = 0        # y-axis of bird
        self.vel = 0                    # velocity
        self.gravity = 0.27             # gravity
        self.flapping = -4            # flying speed
        self.bird_surface = bird_object  # bird surface
        self.bird_rect = bird_object.get_rect()      # bird rectangle

    # updates the co-ordinate of bird
    def update(self, flapped=False):
        # bird will fall untill it reaches the ground
        if self.y < window_height - self.bird_surface.get_height():
            self.vel += self.gravity
        else:
            self.vel = 0

        # if bird is flapping, move upward
        if flapped:
            self.vel = self.flapping
        self.y += self.vel
        self.bird_rect.topleft = (self.x, self.y)

    # check if bird collides with something
    def check_colliderect(self, other_rect):
        if self.bird_rect.colliderect(other_rect):
            return True

    def draw(self, window_surface):
        self.bird_rect.topleft = (self.x, self.y)
        window_surface.blit(self.bird_surface, self.bird_rect)


# render any text
def text_render(text, color, font_size, cord, center=False):
    '''
    renders the text in given cordinate.
    params:
        text: actual text
        color: text color
        font_size = font size
        cord: cordinate of font rect (tuple)
    '''
    font_object = pygame.font.Font(None, font_size)
    font_surface = font_object.render(text, True, color)
    font_rect = font_surface.get_rect()
    font_rect.topleft = (cord[0], cord[1])
    if center:
        font_rect.center = (cord[0], cord[1])
    window.blit(font_surface, font_rect)
    return font_rect


# update highscore in score.txt file before closing game
def update_highscore(high_score):
    if not os.path.exists("data"):
        os.mkdir("data")

    myfile = open("data/score.txt", "w")
    myfile.write(f"high_score:{high_score}")
    myfile.close()


# infinite loop of background and pipes
def move_sprite(rect_object, speed):
    x, y = rect_object.topleft
    x -= speed
    rect_object.topleft = (x, y)


# hit once before starting gameloop
def hit_and_play():
    text_render("Tap to Start", black, 30, (window_width/2, window_height/2), True)
    sprite_rect["hit_and_play_button"].center = (window_width/2, (window_height/2)-40)
    window.blit(sprite_surface["hit_and_play_button"], sprite_rect["hit_and_play_button"])
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    return

        clock.tick(fps)


# restart screen if bird collides with something
def restart():
    bird.y = window_height/3
    bird.vel = 0
    sprite_rect["restart_button"].center = (window_width/2, (window_height/2)-60)
    sprite_rect["main_menu_button"].center = (window_width/2, (window_height/2)+20)
    window.blit(sprite_surface["restart_button"], sprite_rect["restart_button"])
    window.blit(sprite_surface["main_menu_button"], sprite_rect["main_menu_button"])
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                x,y = pygame.mouse.get_pos()
                if sprite_rect["restart_button"].collidepoint(x,y) and event.button == 1:
                    sound["click"].play()
                    game_loop()
                
                if sprite_rect["main_menu_button"].collidepoint(x,y) and event.button == 1:
                    sound["click"].play()
                    start()

        clock.tick(fps)


# first screen of game
def start():
    window.blit(sprite_surface["background1"], sprite_rect["background1"])
    sprite_rect["bird_banner"].center = (window_width/2, window_height/5)
    window.blit(sprite_surface["bird_banner"], sprite_rect["bird_banner"])
    bird.y = window_height/3
    bird.draw(window)
    sprite_rect["play_button"].center = (window_width/2, (window_height/2)-35)
    sprite_rect["exit_button"].center = (window_width/2, (window_height/2)+35)
    window.blit(sprite_surface["play_button"], sprite_rect["play_button"])
    window.blit(sprite_surface["exit_button"], sprite_rect["exit_button"])
    text_render("created by Raman Karki", black, 20, (190, 530))
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                x,y = pygame.mouse.get_pos()
                if sprite_rect["play_button"].collidepoint(x,y) and event.button == 1:
                    sound["click"].play()
                    game_loop()
                
                if sprite_rect["exit_button"].collidepoint(x,y) and event.button == 1:
                    sound["click"].play()
                    pygame.quit()
                    exit()

        clock.tick(fps)


def game_loop():
    global high_score
    score = 0

    # set sprites values
    hit = True
    sprite_rect["base"].topleft = (0, window_height-sprite_surface["base"].get_height())
    pipe_distance = 0
    for upper_pipe, lower_pipe in [["upper_pipe1", "lower_pipe1"], ["upper_pipe2", "lower_pipe2"], ["upper_pipe3", "lower_pipe3"]]:
        sprite_rect[upper_pipe].bottomleft = (window_width+pipe_distance, random.randint(80, 272))
        sprite_rect[lower_pipe].topleft = (sprite_rect[upper_pipe].bottomleft[0], sprite_rect[upper_pipe].bottomleft[1]+100)
        pipe_distance += 170

    while True:
        # check if bird collided with something
        for danger_zone in ["upper_pipe1", "lower_pipe1", "upper_pipe2", "lower_pipe2", "upper_pipe3", "lower_pipe3"]:
            if bird.check_colliderect(sprite_rect[danger_zone]) or bird.y <= 0 or bird.y > window_height-sprite_surface["base"].get_height()-bird.bird_surface.get_height()+6:
                sound["hit"].play()
                if score > high_score:
                    high_score = score
                bird.y = window_height/3
                bird.vel = 0
                restart()

        # event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                update_highscore(high_score)
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    sound["wing"].play()
                    bird.update(True)

        # draw and update
        window.blit(sprite_surface["background1"], sprite_rect["background1"])
        window.blit(sprite_surface["background2"], sprite_rect["background2"])
        bird.draw(window)
        for upper_pipe, lower_pipe in [["upper_pipe1", "lower_pipe1"], ["upper_pipe2", "lower_pipe2"], ["upper_pipe3", "lower_pipe3"]]:
            window.blit(sprite_surface[upper_pipe], sprite_rect[upper_pipe])
            window.blit(sprite_surface[lower_pipe], sprite_rect[lower_pipe])
        window.blit(sprite_surface["base"], sprite_rect["base"])
        text_render(f"High Score: {high_score}", black, 30, (10,10))
        text_render(f"{score}", black, 60, (window_width/2,window_height/4), True)
        pygame.display.update()
        clock.tick(fps)

        # first hit to start game
        if hit:
            hit_and_play()
            hit = False

        # move sprites
        move_sprite(sprite_rect["background1"], 1)
        move_sprite(sprite_rect["background2"], 1)
        bird.update()
        for upper_pipe, lower_pipe in [["upper_pipe1", "lower_pipe1"], ["upper_pipe2", "lower_pipe2"], ["upper_pipe3", "lower_pipe3"]]:
            move_sprite(sprite_rect[upper_pipe], 2)
            move_sprite(sprite_rect[lower_pipe], 2)

        # update score
        for u_pipe in ["upper_pipe1", "upper_pipe2", "upper_pipe3"]:
            if sprite_rect[u_pipe].bottomright[0] == 87 or sprite_rect[u_pipe].bottomright[0] == 86:
                sound["point"].play()
                score += 1

        # infinite sprite loop
        if sprite_rect["background1"].topright[0] == window_width:
            sprite_rect["background2"].topleft = (window_width, 0)
        elif sprite_rect["background2"].topright[0] == window_width:
            sprite_rect["background1"].topleft = (window_width, 0)
        
        for upper_pipe, lower_pipe in [["upper_pipe1", "lower_pipe1"], ["upper_pipe2", "lower_pipe2"], ["upper_pipe3", "lower_pipe3"]]:
            if sprite_rect[upper_pipe].topright[0] <= 0:
                sprite_rect[upper_pipe].bottomleft = (465, random.randint(80, 272))
                sprite_rect[lower_pipe].topleft = (sprite_rect[upper_pipe].bottomleft[0], sprite_rect[upper_pipe].bottomleft[1]+100)


if __name__ == "__main__":

    # initialize pygame
    pygame.mixer.pre_init(22050, -16, 2, 1024)
    pygame.init()
    pygame.mixer.quit()
    pygame.mixer.init(22050, -16, 2, 1024)

    # setup colors
    black = (0,0,0)

    # setup window
    window_width = 350
    window_height = 550
    window = pygame.display.set_mode((window_width, window_height))
    pygame.display.set_caption("Flappy Bird")
    clock = pygame.time.Clock()
    fps = 70

    # load sprites
    sprite_surface = {
        "background1" : pygame.image.load("image/background.png").convert_alpha(),
        "background2" : pygame.image.load("image/background.png").convert_alpha(),
        "upper_pipe1" : pygame.transform.rotate(pygame.image.load("image/pipe.png").convert_alpha(), 180),
        "upper_pipe2" : pygame.transform.rotate(pygame.image.load("image/pipe.png").convert_alpha(), 180),
        "upper_pipe3" : pygame.transform.rotate(pygame.image.load("image/pipe.png").convert_alpha(), 180),
        "lower_pipe1" : pygame.image.load("image/pipe.png").convert_alpha(),
        "lower_pipe2" : pygame.image.load("image/pipe.png").convert_alpha(),
        "lower_pipe3" : pygame.image.load("image/pipe.png").convert_alpha(),
        "base" : pygame.image.load("image/base.png").convert_alpha(),
        "bird_banner" : pygame.image.load("image/flappy_bird_logo.png").convert_alpha(),
        "play_button" : pygame.image.load("image/play_button.png").convert_alpha(),
        "exit_button" : pygame.image.load("image/exit_button.png").convert_alpha(),
        "hit_and_play_button" : pygame.image.load("image/hit.png").convert_alpha(),
        "restart_button" : pygame.image.load("image/restart.png").convert_alpha(),
        "main_menu_button" : pygame.image.load("image/main_menu.png").convert_alpha(),
    }
    bird = Bird(pygame.image.load("image/bird.png").convert_alpha())

    # sprite rect
    sprite_rect = dict()
    for sprites in sprite_surface:
        sprite_rect[sprites] = sprite_surface[sprites].get_rect()

    # load sounds
    sound = {
        "click" : pygame.mixer.Sound('audio/click.wav'),
        "hit" : pygame.mixer.Sound('audio/hit.wav'),
        "point" : pygame.mixer.Sound('audio/point.wav'),
        "wing" : pygame.mixer.Sound('audio/wing.wav')
    }

    # open score file for high_score data
    try:
        file = open("data/score.txt", "r")
        data = file.read()
        h_score = data.split(":")
        high_score = int(h_score[1])
    except:
        high_score = 0
    
    # start game
    start()
    game_loop()

