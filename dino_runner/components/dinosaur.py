
import pygame
from pygame.sprite import Sprite

from dino_runner.utils.constants import DEFAULT_TYPE, SHIELD_TYPE, DUCKING, RUNNING, JUMPING, DUCKING_SHIELD, JUMPING_SHIELD, RUNNING_SHIELD, SHIELD

X_POS = 80
Y_POS = 310
JUMP_VEL = 8.5
Y_POS_DUCK = 340

RUNNING_IMG = {DEFAULT_TYPE:RUNNING, SHIELD_TYPE:RUNNING_SHIELD}
JUMPING_IMG = {DEFAULT_TYPE:JUMPING, SHIELD_TYPE:JUMPING_SHIELD}
DUCKING_IMG = {DEFAULT_TYPE:DUCKING, SHIELD_TYPE:DUCKING_SHIELD}

class Dinosaur(Sprite):
    def __init__(self):
        self.type = DEFAULT_TYPE
        self.image = RUNNING_IMG[DEFAULT_TYPE][0]

        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = X_POS
        self.dino_rect.y = Y_POS

        self.step_index = 0
        self.dino_run = True
        self.dino_jump = False
        self.dino_duck = False
      
        

        self.jump_vel = JUMP_VEL
        self.setup_state()

    def setup_state(self):
        self.has_shield = False
        self.has_power_up = False
        self.power_up_time = 0



    def run(self):
        self.dino_rect.y = Y_POS

        if self.step_index < 5:
             self.image = RUNNING_IMG[self.type][0]
        else:
                self.image = RUNNING_IMG[self.type][1]

        self.step_index += 1
        
    def update(self, user_input):
        if(self.power_up_time > 0):
            self.power_up_time -= 1000
            self.type = SHIELD_TYPE
        else:
            self.type = DEFAULT_TYPE
            self.setup_state()


        if self.dino_run:
            self.run()
        elif self.dino_jump:
            self.jump()
        elif self.dino_duck:
            self.duck()

        if user_input[pygame.K_UP] and not self.dino_jump:
            self.dino_jump = True
            self.dino_run = False
        elif not self.dino_jump:
            self.dino_jump = False
            self.dino_run = True

# tentei mudar o if por elif, no código pra diminuir mas ai não agachava.
        if user_input[pygame.K_DOWN]:
            self.dino_duck = True
            self.dino_run = False
            
       
        if self.step_index >= 10:
            self.step_index = 0

    def jump(self):
        self.image = JUMPING_IMG[self.type]

        if self.dino_jump:
            self.dino_rect.y -= self.jump_vel * 4
            self.jump_vel -= 0.8

        if self.jump_vel < -JUMP_VEL:
            self.dino_rect.y = Y_POS
            self.dino_jump = False
            self.jump_vel = JUMP_VEL

# Tarefa 1
    def duck(self):
        self.image = DUCKING

        if self.step_index < 5:
             self.image = DUCKING_IMG[self.type][0]
        else:
             self.image = DUCKING_IMG[self.type][1]

        self.step_index += 1
       
        self.dino_rect.x = X_POS
        self.dino_rect.y = Y_POS_DUCK
          
        
    def draw(self, screen):

        screen.blit(self.image, ( self.dino_rect.x, self.dino_rect.y))


    



