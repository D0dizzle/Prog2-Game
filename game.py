#### Datei für Kollision usw.
from __future__ import annotations
import pygame
from abc import ABC, abstractclassmethod
from settings import *
from sprites import *
from enemy import *
from player import *
import math

#### Interface und Zustand-Klassen für die verschiedenen Spiel-Abschnitte
class screenState(ABC):
    def exit(self):
        pass

    def enter(self):
        pass

    def update(self):
        pass

    def render(self):
        pass

class startScreen(screenState):
    def enter(self, screen: GameScreen):
        screen.buttons = [
            {'rect': pygame.Rect(width/2 -100, 400, 200, 50), 'text': 'Start'}, # beide hinteren Werte für die Größe
            {'rect': pygame.Rect(width/2 -150, 500, 300, 50), 'text': 'Settings'},
            {'rect': pygame.Rect(width/2 -100, 600, 200, 50), 'text': 'Exit'}]
    
    def update(self, screen: GameScreen):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in screen.buttons:
                    if button['rect'].collidepoint(event.pos):
                        if button['text'] == 'Start':
                            screen.change_state(playScreen())
                        if button['text'] == 'Settings':
                            screen.change_state(settingsScreen())
                        if button['text'] == 'Exit':
                            pygame.quit()
                            sys.exit()
            if event.type == pygame.QUIT:
                sys.exit()

    def render(self, screen: GameScreen):
        #SCREEN.blit(screen.image, (0,0))
        screen.image.render()
        for button in screen.buttons:
            rect = pygame.Rect(button['rect'])
            pygame.draw.rect(SCREEN, red, rect, border_radius=10)
            pygame.draw.rect(SCREEN, white, rect, width=2, border_radius=10)
            button_text = screen.font.render(button['text'], True, white)
            text_rect = button_text.get_rect(center=rect.center)
            SCREEN.blit(button_text, text_rect)
        
        self.headline = screen.headline.render(f"Centipede", True, white)
        SCREEN.blit(self.headline, (width/2 -225, 170, 0, 0))

        # Platzieren der Ellipse
        angle = pygame.time.get_ticks() * 0.001
        radius_x = 300
        radius_y = 100
        star_x = int(width / 2 + radius_x * math.cos(angle))
        star_y = int(170 + radius_y * math.sin(angle))

        star_image = pygame.image.load(os.path.join(game_folder, "Assets", "hintergrund", "headline-star.png"))
        star_image = pygame.transform.scale(star_image, (60, 60))  # Anpassung der Sternengröße

        # Größe und Position der Ellipse
        ellipse_rect = pygame.Rect(star_x - 25, star_y + 8, 40, 20)

        # Sternbild zeichnen
        SCREEN.blit(star_image, ellipse_rect.topleft)

        pygame.display.flip()


    def exit(self):
        pass    

class playScreen(screenState):
    def enter(self, screen: GameScreen):
        screen.score.load_highscore()
        screen.buttons = []
        if screen.pause == False:
            del ufo_sprites[0:]
            screen.player1 = Player1(player_img_dict, width /2, height - height /6, screen.shoot_sound, screen.death_sound, screen.missile_sound)
            screen.new_map = ObstacleOnScreen()
            screen.new_map.new(ufo_sprites)
            screen.centipede = Centipede(10)
            screen.centipede.createCentipede()
            screen.collider = Collider()
            screen.asteroids = Asteroid()
        elif screen.pause == True:
            screen.pause = False

    
    def update(self, screen: GameScreen):
        key_pressed = pygame.key.get_pressed()
        exit_game()
        #update der Logik
        screen.player1.update()
        screen.player1.shoot(projectiles)
        screen.asteroids.render()
        screen.collider.collideObstacle(projectiles, ufo_sprites)
        screen.collider.collideCentipede(projectiles, screen.centipede.segments)
        screen.collider.collideWithWall(screen.centipede.segments, ufo_sprites)
        screen.collider.collidePlayer(screen.asteroids.asteroidslist, screen.player1)
        screen.collider.collidePlayer(screen.centipede.segments, screen.player1)
        screen.new_map.delete(ufo_sprites)
        screen.centipede.update()
        screen.timer.count_time()
        screen.score.update_score(screen.new_map, screen.centipede)
        screen.score.update_highscore()
        screen.score.save_highscore()
        if len(screen.centipede.segments) == 0:
            screen.change_state(playScreen())
        if screen.player1.state == "dead":
            screen.change_state(gameOverScreen())

        if key_pressed[pygame.K_ESCAPE]:
            screen.change_state(pauseScreen())

    def render(self, screen: GameScreen):    
        screen.image.render()
        #hier Objekte die ge"draw"ed werden sollen
        sprites = pygame.sprite.Group(screen.player1, projectiles, ufo_sprites, screen.centipede.segments)
        sprites.draw(SCREEN)
        screen.asteroids.update()
        screen.timer.render()
        screen.score.display_scores()

    def exit(self):
        pass

class settingsScreen(screenState):
    def enter(self, screen: GameScreen):
        screen.buttons = [{'rect': pygame.Rect(25, 200, 400, 50), 'text': 'Music-Volume:'}, # beide hinteren Werte für die Größe
            {'rect': pygame.Rect(475, 200, 50, 50), 'text': '+'},
            {'rect': pygame.Rect(550, 200, 50, 50), 'text': '-'},
            {'rect': pygame.Rect(625, 200, 150, 50), 'text': 'Mute'},
            {'rect': pygame.Rect(25, 350, 400, 50), 'text': 'Sound-Volume'},
            {'rect': pygame.Rect(475, 350, 50, 50), 'text': '.+'},
            {'rect': pygame.Rect(550, 350, 50, 50), 'text': '.-'},
            {'rect': pygame.Rect(625, 350, 150, 50), 'text': '.Mute'},
            {'rect': pygame.Rect(50, 500, 300, 50), 'text': 'Start Game'},
            {'rect': pygame.Rect(400, 500, 350, 50), 'text': 'Back to Start'},
            {'rect': pygame.Rect(300, 600, 200, 50), 'text': 'Exit'}]
    
    def update(self, screen: GameScreen):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in screen.buttons:
                    if button['rect'].collidepoint(event.pos):
                        if button['text'] == '+':
                            if screen.volume < 2:
                                screen.volume += 0.1
                        if button['text'] == '-':
                            if screen.volume > 0:
                                screen.volume -= 0.1
                        if button['text'] == 'Mute':
                            screen.volume = 0
                        pygame.mixer.music.set_volume(screen.volume)
                        if button['text'] == '.+':
                            screen.sound_volume += 0.1
                        if button['text'] == '.-':
                            screen.sound_volume -= 0.1
                        if button['text'] == '.Mute':
                            screen.sound_volume = 0
                        screen.shoot_sound.set_volume(screen.sound_volume)
                        screen.death_sound.set_volume(screen.sound_volume)
                        if button['text'] == 'Start Game':
                            screen.change_state(playScreen())
                        if button['text'] == 'Back to Start':
                            screen.change_state(startScreen())
                        if button['text'] == 'Exit':
                            pygame.quit()
                            sys.exit()
            if event.type == pygame.QUIT:
                sys.exit()

    def render(self, screen: GameScreen):
        screen.image.render()
        #SCREEN.blit(screen.image, (0,0))
        for button in screen.buttons:
            rect = pygame.Rect(button['rect'])
            pygame.draw.rect(SCREEN, red, rect, border_radius=10)
            pygame.draw.rect(SCREEN, white, rect, width=2, border_radius=10)
            button_text = screen.font.render(button['text'], True, white)
            text_rect = button_text.get_rect(center=rect.center)
            SCREEN.blit(button_text, text_rect)
        

class pauseScreen(screenState):
    def enter(self, screen: GameScreen):
        #screen.image = pygame.transform.scale(pygame.image.load(os.path.join(game_folder, "Assets", "hintergrund", "parallax-background.png")).convert(),(width, height))
        screen.buttons = [
            {'rect': pygame.Rect(width/2 -125, 200, 250, 50), 'text': 'Continue'},
            {'rect': pygame.Rect(width/ 2 -125, 300, 250, 50), 'text': 'Settings'},
            {'rect': pygame.Rect(width/ 2 -125, 400, 250, 50), 'text': 'Restart'},
            {'rect': pygame.Rect(width / 2 -175, 500, 350, 50), 'text': 'Back to Start'},
            {'rect': pygame.Rect(width / 2 -125, 600, 250, 50), 'text': 'Exit Game'}
        ]
        screen.pause = True
    
    def update(self, screen: GameScreen):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in screen.buttons:
                    if button['rect'].collidepoint(event.pos):
                        if button['text'] == 'Continue':
                            screen.change_state(playScreen())
                        if button['text'] == 'Settings':
                            screen.change_state(settingsScreen())
                        if button['text'] == 'Restart':
                            screen.score.points = 0
                            screen.timer.time = 0
                            screen.change_state(playScreen())
                        if button['text'] == 'Back to Start':
                            screen.score.points = 0
                            screen.timer.time = 0
                            screen.change_state(startScreen())
                        if button['text'] == 'Exit Game':
                            exit_game()
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def render(self, screen: GameScreen):
        screen.image.render()
        for button in screen.buttons:
            rect = pygame.Rect(button['rect'])
            pygame.draw.rect(SCREEN, red, rect, border_radius=10)
            pygame.draw.rect(SCREEN, white, rect, width=2, border_radius=10)
            button_text = screen.font.render(button['text'], True, white)
            text_rect = button_text.get_rect(center=rect.center)
            SCREEN.blit(button_text, text_rect)


class gameOverScreen(screenState):

    def enter(self, screen: GameScreen):

        screen.buttons = [{'rect': pygame.Rect(50, 500, 200, 50), 'text': 'Restart'},
        {'rect': pygame.Rect(550, 500, 200, 50), 'text': 'Exit'}]
        #screen.image = pygame.transform.scale(pygame.image.load(os.path.join(game_folder, "Assets", "hintergrund", "parallax-background.png")).convert(),(width, height))
    
    def update(self, screen: GameScreen):

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in screen.buttons:
                    if button['rect'].collidepoint(event.pos):
                        if button['text'] == 'Restart':
                            screen.score.points = 0
                            screen.timer.time = 0
                            screen.change_state(playScreen())
                        if button['text'] == 'Exit':
                            pygame.quit()
                            sys.exit()

    def render(self, screen: GameScreen):
        screen.image.render()
        self.gameovertext = screen.headline.render("Game Over", True, white)
        SCREEN.blit(self.gameovertext, (175, 100))
        
        for button in screen.buttons:
            rect = pygame.Rect(button['rect'])
            pygame.draw.rect(SCREEN, red, rect, border_radius=10)
            pygame.draw.rect(SCREEN, white, rect, width=2, border_radius=10)
            button_text = screen.font.render(button['text'], True, white)
            text_rect = button_text.get_rect(center=rect.center)
            SCREEN.blit(button_text, text_rect)

class GameScreen:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.volume = 0.5
        self.sound_volume = 0.5
        self.timer = Time()
        self.score = Score()
        self.pause = False
        pygame.mixer.music.load(os.path.join(game_folder,"Assets","sounds","BGM.wav"))
        pygame.mixer.music.play(-1, 0)
        pygame.mixer.music.set_volume(self.volume)
        self.shoot_sound = pygame.mixer.Sound(os.path.join(game_folder,"Assets","sounds","shoot.wav"))
        self.death_sound = pygame.mixer.Sound(os.path.join(game_folder,"Assets","sounds","death_player.ogg"))
        self.missile_sound = print("Hier kommt ein Sound")
        background = Hintergrund(hg_dict)
        self.image = background
        self.screen_state = startScreen()
        self.buttons = []
        self.screen_state.enter(self)
        self.font = pygame.font.Font(os.path.join(game_folder, "Assets", "fonts", "Boxy-Bold.ttf"), 35)
        self.headline = pygame.font.Font(os.path.join(game_folder, "Assets", "fonts", "Boxy-Bold.ttf"), 65)

    def change_state(self, newState: screenState):
        if (self.screen_state != None):
            self.screen_state.exit()
        self.screen_state = newState
        self.screen_state.enter(self)
    
    def render(self):
        self.screen_state.render(self)

    def update(self):
        self.screen_state.update(self)
        
