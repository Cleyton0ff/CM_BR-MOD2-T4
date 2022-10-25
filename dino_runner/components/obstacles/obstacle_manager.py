import pygame
import random 

from dino_runner.components.obstacles.cactus import Cactus
from dino_runner.components.obstacles.large_cactus import LargeCactus
from dino_runner.components.obstacles.bird import Bird
from dino_runner.utils.constants import LARGE_CACTUS, SMALL_CACTUS, BIRD

class ObstacleManager:
    def __init__(self):
        self.obstacles  = []

    def update(self, game):
        if len(self.obstacles) == 0:

            obs_type = random.randint(0, 2)

            if obs_type == 0:
                self.obstacles.append(Cactus(SMALL_CACTUS))
            elif obs_type == 1:
                self.obstacles.append(LargeCactus(LARGE_CACTUS))
            elif obs_type == 2:
                self.obstacles.append(Bird(BIRD))
                
        # if len(self.obstacles) == 0:
            # if random.randint(0, 2) == 0:
                # self.obstacles.append(Cactus(SMALL_CACTUS))
            # elif random.randint(0, 2) == 1:
                # self.obstacles.append(LargeCactus(LARGE_CACTUS))

            # if random.randint(0, 2) == 2:
                # self.obstacles.append(Bird(BIRD))

        for obstacle in self.obstacles:
            obstacle.update(game.game_speed, self.obstacles)

            #manege the collision
            if game.player.dino_rect.colliderect(obstacle.rect):
                game.playing = False
                pygame.time.delay(500)
                break


    def draw(self, screen):
        for obstacle in self.obstacles:
            obstacle.draw(screen)
    











