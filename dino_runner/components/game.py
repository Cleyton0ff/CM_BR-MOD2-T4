
import pygame

from dino_runner.utils.constants import BG, DEAD, ICON, SCREEN_HEIGHT, SCREEN_WIDTH, TITLE, FPS, DEFAULT_TYPE, GAME_OVER
from dino_runner.components.dinosaur import Dinosaur
from dino_runner.components.obstacles.obstacle_manager import ObstacleManager
from dino_runner.components.power_ups.power_up_manager import PowerUpManager

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(TITLE)
        pygame.display.set_icon(ICON)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

        self.player = Dinosaur()
        self.obstacle_manager = ObstacleManager()
        self.power_up_manager = PowerUpManager()

        self.count_death = 0
        self.score = 0
        self.clock = pygame.time.Clock()
        self.playing = False
        self.executing = False
        self.game_speed = 15
        self.x_pos_bg = 0
        self.y_pos_bg = 380

    def run(self):
        # Game loop: events - update - draw
        self.playing = True
        while self.playing:
            self.events()
            self.update()
            self.draw()
        # pygame.quit()

    def execute(self):
        self.executing = True

        while(self.executing): 
            
            self.display_menu()

            # if not self.playing:
                # self.reset()

        pygame.display.quit()
        pygame.quit()

   

    def display_menu(self):
        # print("Displaying menu")
        self.screen.fill((255,255,255))

        font_size = 32
        color = (0,0,0)
        FONT = 'freesansbold.ttf'
        font = pygame.font.Font(FONT, font_size)

        if self.count_death == 0:
            text_to_display = "Press any key to start"
            text = font.render(text_to_display, True, color)
            menu_text_rect = text.get_rect()
            # text_to_display = "Press any key to start again"
            # text = font.render(text_to_display, True, color)
            # menu_text_rect = text.get_rect()

            menu_text_rect.x = (SCREEN_WIDTH //2) - (menu_text_rect.width//2)
            menu_text_rect.y = (SCREEN_HEIGHT //2) - (menu_text_rect.height//2)
            self.screen.blit(text, (menu_text_rect.x, menu_text_rect.y))

        else:
            self.menu_death()


        pygame.display.update()

        self.events_on_menu()


    def menu_death(self):
        self.screen.fill((255,255,255))

        font_size = 32
        color = (0,0,0)
        FONT = 'freesansbold.ttf'
        font = pygame.font.Font(FONT, font_size)        
        dead_text_to_display = "Press any key to start again"
        text = font.render(dead_text_to_display, True, color)


        death_menu_text_rect = text.get_rect()

        
        death_menu_text_rect.x =  (SCREEN_WIDTH //2) - (death_menu_text_rect.width//2)
        death_menu_text_rect.y = (SCREEN_HEIGHT// 1.5) - (death_menu_text_rect.height //2)
        self.screen.blit(text, (death_menu_text_rect.x, death_menu_text_rect.y))

        # tentativa de mostrar o score final

        score_final_text = font.render(f"Final score: {self.score}", True, color)
        score_final_text_rect = text.get_rect()
        score_final_text_rect.x = 400
        score_final_text_rect.y = 120

        self.screen.blit(score_final_text, (score_final_text_rect.x, score_final_text_rect.y))

        # tentativa de mostrar a quantidade de morte

        count_death_text = font.render(f"Number of Deaths: {self.count_death}", True, color)
        count_death_text_rect = text.get_rect()
        count_death_text_rect.x = 375
        count_death_text_rect.y = 170


        self.screen.blit(count_death_text, (count_death_text_rect.x, count_death_text_rect.y))

        dino_dead_image = DEAD
        game_over = GAME_OVER
        # tentar colocar o incone de morte do dino!!!!
        self.screen.blit(game_over, (340, 50))
        self.screen.blit(dino_dead_image, (470, 250))

        pygame.display.update()
        self.events_on_menu()

        
    def events_on_menu(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.executing = False
            if event.type == pygame.KEYDOWN:
                self.reset()
                self.run()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False

    def update(self):
        user_input = pygame.key.get_pressed()
        self.player.update(user_input)
        self.obstacle_manager.update(self)
        self.power_up_manager.update(self)
       

        self.update_score()
        self.update_game_speed()
        # self.update.power_up_time()

    def update_score(self):
        self.score += 1

    def update_game_speed(self):
        if self.score % 100 == 0:
            self.game_speed += 3

    def reset(self):
        self.score = 0
        self.game_speed = 15
        self.obstacle_manager.reset_obstacles()
        self.power_up_manager.reset_power_up()

    def draw(self):
        self.clock.tick(FPS)
        self.screen.fill((255, 255, 255))
        self.draw_background()

        self.player.draw(self.screen)
        self.obstacle_manager.draw(self.screen)
        self.power_up_manager.draw(self.screen)

        #draw score
        self.draw_score()
       
        pygame.display.update()
        pygame.display.flip()

    def draw_score(self):
        #print(self.score)

        font_size = 32
        color = (0,0,0)
        FONT = 'freesansbold.ttf'

        font = pygame.font.Font(FONT, font_size)
        text = font.render(f"Score: {self.score}", True, color)

        score_text_rect = text.get_rect()
        score_text_rect.x = 850
        score_text_rect.y = 30

        self.screen.blit(text, (score_text_rect.x, score_text_rect.y))


    def draw_background(self):
        image_width = BG.get_width()
        self.screen.blit(BG, (self.x_pos_bg, self.y_pos_bg))
        self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
        if self.x_pos_bg <= -image_width:
            self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
            self.x_pos_bg = 0
        self.x_pos_bg -= self.game_speed