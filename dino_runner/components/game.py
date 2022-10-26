import pygame

from dino_runner.utils.constants import BG, ICON, SCREEN_HEIGHT, SCREEN_WIDTH, TITLE, FPS
from dino_runner.components.dinosaur import Dinosaur
from dino_runner.components.obstacles.obstacle_manager import ObstacleManager

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(TITLE)
        pygame.display.set_icon(ICON)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

        self.player = Dinosaur()
        self.obstacle_manager = ObstacleManager()
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

            if not self.playing:
                self.reset()

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
        else:
            text_to_display = "Press any key to start again"
            text = font.render(text_to_display, True, color)
            menu_text_rect = text.get_rect()

        
        menu_text_rect.x = (SCREEN_WIDTH //2) - (menu_text_rect.width//2)
        menu_text_rect.y = (SCREEN_HEIGHT //2) - (menu_text_rect.height//2)
        self.screen.blit(text, (menu_text_rect.x, menu_text_rect.y))

        pygame.display.update()

        self.events_on_menu()
        
    def events_on_menu(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.executing = False
            if event.type == pygame.KEYDOWN:
              self.run()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False

    def update(self):
        user_input = pygame.key.get_pressed()
        self.player.update(user_input)
        self.obstacle_manager.update(self)

        self.update_score()
        self.update_game_speed()

    def update_score(self):
        self.score += 1

    def update_game_speed(self):
        if self.score % 100 == 0:
            self.game_speed += 3

    def reset(self):
        self.score = 0
        self.game_speed = 15
        self.obstacle_manager.reset_obstacles()

    def draw(self):
        self.clock.tick(FPS)
        self.screen.fill((255, 255, 255))
        self.draw_background()

        self.player.draw(self.screen)
        self.obstacle_manager.draw(self.screen)

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