#### Datei für Kollision usw.
from __future__ import annotations
import pygame
from abc import ABC
from settings import *
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
            create_button(width/2 -100, 400, 200, 50, 'text', 'Start'),
            create_button(width/2 -150, 500, 300, 50, 'text', 'Settings'),
            create_button(width/2 -100, 600, 200, 50, 'text', 'Exit')
        ]

    def update(self, screen: GameScreen):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in screen.buttons:
                    if button['rect'].collidepoint(event.pos):
                        if button['text'] == 'Start':
                            if screen.story_screen_shown == False:
                                screen.change_state(storyScreen())
                                screen.story_screen_shown = True
                            else:
                                screen.change_state(playScreen())
                        elif button['text'] == 'Settings':
                            screen.change_state(settingsScreen())
                            screen.button_sound.play()
                        elif button['text'] == 'Exit':
                            screen.button_sound.play()
                            pygame.quit()
                            sys.exit()
            if event.type == pygame.QUIT:
                sys.exit()

    def render(self, screen: GameScreen):
        screen.image.render()
        render_button(screen, screen.buttons, 'text')

        self.headline = screen.headline.render(f"Centipede", True, white)
        SCREEN.blit(self.headline, (width/2 -225, 170, 0, 0))

        # Platzieren der Ellipse
        angle = pygame.time.get_ticks() * 0.001
        radius_x = 300
        radius_y = 100
        star_x = int(width / 2 + radius_x * math.cos(angle))
        star_y = int(170 + radius_y * math.sin(angle))

        star_image = pygame.transform.scale(img_dict["star_image"], (60, 60))  # Anpassung der Sternengröße

        # Größe und Position der Ellipse
        ellipse_rect = pygame.Rect(star_x - 25, star_y + 8, 40, 20)

        # Sternbild zeichnen
        SCREEN.blit(star_image, ellipse_rect.topleft)

    def exit(self):
        pass

class storyScreen(screenState):
    def enter(self, screen: GameScreen):
        screen.buttons = [create_button(width/3, 600, 300, 50, 'text', 'Start Game')]
        screen.story = [
            create_text(50, 50, 500, 50, 'text', 'You are the Commander of the'),
            create_text(50, 100, 500, 50, 'text', 'USS Space Splitter. You are on'),
            create_text(50, 150, 500, 50, 'text', 'the mission to hunt and destroy'),
            create_text(50, 200, 500, 50, 'text', 'the Space Centipedes'),
            create_text(50,250, 500, 50, 'text', 'to save our home planet.'),
            create_text(50, 325, 500, 50, 'text', 'Good Luck Commander!'),
            create_text(575, 400, 200, 50, 'text', 'Space Bar'),
            create_text(575, 450, 200, 50, 'text', 'M')]
        
        if isinstance(screen.controller, ArrowKey):
            screen.control_text = [{'text': "Controls:   Up", 'rect': (50, 400, 400, 50)},
                                    {'text': "Left                  Right", 'rect': (150, 450, 500, 50)},
                                    {'text': "Down", 'rect': (325, 500, 500, 50)}
                                    ]
        if isinstance(screen.controller, WASDKey):
            screen.control_text = [{'text': "Controls:      W", 'rect': (50, 400, 400, 50)},
                                    {'text': "A                 D", 'rect': (225, 450, 500, 50)},
                                    {'text': "S", 'rect': (325, 500, 500, 50)}
                                    ]
        screen.control_image = [{'image': ui_img_dict["up"], 'rect': (300, 400, 25, 50)},
                                     {'image': ui_img_dict["left"], 'rect': (250, 450, 25, 50)},
                                     {'image': ui_img_dict["right"], 'rect': (350, 450, 25, 50)},
                                     {'image': ui_img_dict["down"], 'rect': (300, 500, 25, 50)},
                                     {'image': img_dict["bullet"], 'rect': (525, 400, 50, 50)},
                                     {'image': img_dict["Missile"], 'rect': (525, 450, 50, 50)}
                                     ]

    def update(self, screen: GameScreen):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in screen.buttons:
                    if button['rect'].collidepoint(event.pos):
                        if button['text'] == 'Start Game':
                            screen.change_state(playScreen())   
            if event.type == pygame.QUIT:
                sys.exit()  

    def render(self, screen: GameScreen):
        screen.image.render()
        render_button(screen, screen.buttons, 'text')
        render_text(screen.story, 'text', screen.story_font)
        render_text(screen.control_text, 'text', screen.story_font)
        for image in screen.control_image:
            rect = pygame.Rect(image['rect'])
            image = image['image']
            SCREEN.blit(image, rect)
        
# Klasse für den Zustand des GameScreens -> Spielbildschirm
class playScreen(screenState):
    def enter(self, screen: GameScreen):
        screen.score.load_highscore()
        screen.buttons = []
        if screen.pause == False:
            del ufo_sprites[0:]
            screen.player1 = Player1(player_img_dict, width /2, height - height /6, screen.shoot_sound, screen.death_sound, screen.missile_sound, screen.life_display)
            screen.new_map = ObstacleOnScreen()
            screen.new_map.new(ufo_sprites, screen.style)
            screen.centipede = Centipede()
            screen.centipede.createCentipede(screen.style)
            screen.collider = Collider()
            screen.asteroids = Asteroid()
            screen.controller.set_left_key(PlayerMoveLeft(screen.player1))
            screen.controller.set_right_key(PlayerMoveRight(screen.player1))
            screen.controller.set_up_key(PlayerMoveUp(screen.player1))
            screen.controller.set_down_key(PlayerMoveDown(screen.player1))
            screen.life_display.reset()
            screen.life_display.createLife_Display()
        elif screen.pause == True:
            screen.pause = False

    def update(self, screen: GameScreen):
        exit_game()
        #update der Logik
        # Ausführen der Control-Inputs
        if screen.key_pressed[screen.controller.left_key['button']] and screen.player1.rect.left > 10:
            screen.controller.press_left_key()
        if screen.key_pressed[screen.controller.right_key['button']] and screen.player1.rect.right < width -10:
            screen.controller.press_right_key()
        if screen.key_pressed[screen.controller.up_key['button']] and screen.player1.rect.top > height * 0.75:
            screen.controller.press_up_key()
        if screen.key_pressed[screen.controller.down_key['button']] and screen.player1.rect.bottom < height -10:
            screen.controller.press_down_key()
        screen.player1.update()
        screen.player1.shoot(projectiles)
        screen.asteroids.render()
        screen.collider.collideObstacle(projectiles, ufo_sprites, Missile)
        screen.collider.collideCentipede(projectiles, screen.centipede.segments, screen.centipede_hit_sound)
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
        if screen.key_pressed[pygame.K_ESCAPE]:
            screen.change_state(pauseScreen())
        

    def render(self, screen: GameScreen):    
        screen.image.render()
        sprites = pygame.sprite.Group(screen.player1, projectiles, ufo_sprites, screen.centipede.segments)
        sprites.draw(SCREEN)
        screen.asteroids.update()
        screen.timer.render()
        screen.score.display_scores()
        screen.life_display.render()
        if screen.player1.missile_cd >= 300:
            SCREEN.blit(img_dict['satellite'], (10, 100))

    def exit(self):
        pass


class settingsScreen(screenState):
    def enter(self, screen: GameScreen):
        screen.text = [
            create_text(25, 100, 400, 50, 'text', 'Music-Volume:'),
            create_text(25, 200, 400, 50, 'text', 'Sound-Volume:'),
            create_text(25, 300, 275, 50, 'text', 'Controls:'),
            create_text(350, 603, 200, 50, 'text', 'Secret:')
        ]
        screen.buttons = [
            create_button(450, 100, 50, 50, 'text', '+'),
            create_button(525, 100, 50, 50, 'text', '-'),
            create_button(600, 100, 150, 50, 'text', 'Mute'),
            create_button(400, 300, 325, 50, 'text', 'Arrow Keys'),
            create_button(400, 375, 350, 50, 'text', 'W A S D Keys'),
            create_button(25, 500, 300, 50, 'text', 'Start Game'),
            create_button(400, 500, 350, 50, 'text', 'Back to Start'),
            create_button(100, 600, 200, 50, 'text', 'Exit'),
            create_button(550, 600, 75, 50, 'text', 'ON'),
            create_button(650, 600, 100, 50, 'text', 'OFF')
        ]
        screen.buttons2 = [
            create_button(450, 200, 50, 50, 'text', '+'),
            create_button(525, 200, 50, 50, 'text', '-'),
            create_button(600, 200, 150, 50, 'text', 'Mute')
        ]

    #anpassbare Einstellungen
    def update(self, screen: GameScreen):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in screen.buttons:
                    if button['rect'].collidepoint(event.pos):
                        if button['text'] == '+':
                            if screen.volume < 2:
                                screen.volume += 0.2
                        if button['text'] == '-':
                            if screen.volume > 0:
                                screen.volume -= 0.2
                        if button['text'] == 'Mute':
                            screen.button_sound.play()
                            screen.volume = 0
                        pygame.mixer.music.set_volume(screen.volume)
                        if button['text'] == 'Arrow Keys':
                            screen.controller = screen.controllerCreator.createController("arrow")
                            screen.button_sound.play()
                        if button['text'] == 'W A S D Keys':
                            screen.controller = screen.controllerCreator.createController("wasd")
                            screen.button_sound.play()
                        if button['text'] == 'Start Game':
                            screen.score.points = 0
                            screen.timer.time = 0
                            screen.button_sound.play()
                            if screen.story_screen_shown == False:
                                screen.change_state(storyScreen())
                                screen.story_screen_shown = True
                            else:
                                screen.change_state(playScreen())
                        if button['text'] == 'Back to Start':
                            screen.button_sound.play()
                            screen.change_state(startScreen())
                        if button['text'] == 'Exit':
                            screen.button_sound.play()
                            pygame.quit()
                            sys.exit()
                        if button['text'] == 'ON':
                            screen.button_sound.play()
                            screen.style = "Tree"
                        if button['text'] == 'OFF':
                            screen.button_sound.play()
                            screen.style = "Ufo"
                for button in screen.buttons2:
                    if button['rect'].collidepoint(event.pos):
                        if button['text'] == '+':
                            screen.sound_volume += 0.2
                            screen.shoot_sound.play()
                        if button['text'] == '-':
                            screen.sound_volume -= 0.2
                            screen.shoot_sound.play()
                        if button['text'] == 'Mute':
                            screen.button_sound.play()
                            screen.sound_volume = 0
                        for sound in screen.sound_list:
                            sound.set_volume(screen.sound_volume)
            if event.type == pygame.QUIT:
                sys.exit()

    def render(self, screen: GameScreen):
        screen.image.render()
        render_button(screen, screen.buttons, 'text')
        render_button(screen, screen.buttons2, 'text')
        render_text(screen.text, 'text', screen.font)
        
class pauseScreen(screenState):
    def enter(self, screen: GameScreen):
        screen.buttons = [
            create_button(width/2 -125, 200, 250, 50, 'text', 'Continue'),
            create_button(width/2 -125, 300, 250, 50, 'text', 'Settings'),
            create_button(width/2 -125, 400, 250, 50, 'text', 'Restart'),
            create_button(width/2 -175, 500, 350, 50, 'text', 'Back to Start'),
            create_button(width/2 -125, 600, 250, 50, 'text', 'Exit Game')
        ]

        screen.pause = True
        self.timer = 0
    
    def update(self, screen: GameScreen):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in screen.buttons:
                    if button['rect'].collidepoint(event.pos):
                        if button['text'] == 'Continue':
                            screen.change_state(playScreen())
                            screen.button_sound.play()
                        if button['text'] == 'Settings':
                            screen.change_state(settingsScreen())
                            screen.pause = False
                            screen.button_sound.play()
                        if button['text'] == 'Restart':
                            screen.score.points = 0
                            screen.timer.time = 0
                            screen.pause = False
                            screen.button_sound.play()
                            screen.change_state(playScreen())
                        if button['text'] == 'Back to Start':
                            screen.score.points = 0
                            screen.timer.time = 0
                            screen.button_sound.play()
                            screen.change_state(startScreen())
                        if button['text'] == 'Exit Game':
                            pygame.quit()
                            sys.exit()
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def render(self, screen: GameScreen):
        screen.image.render()
        render_button(screen, screen.buttons, 'text')

class gameOverScreen(screenState):
    def enter(self, screen: GameScreen):
        screen.buttons = [
            create_button(50, 500, 200, 50, 'text', 'Restart'),
            create_button(550, 500, 200, 50, 'text', 'Exit')
        ]
    
    def update(self, screen: GameScreen):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in screen.buttons:
                    if button['rect'].collidepoint(event.pos):
                        if button['text'] == 'Restart':
                            screen.score.points = 0
                            screen.timer.time = 0
                            del projectiles[:0]
                            screen.button_sound.play()
                            screen.change_state(playScreen())
                        if button['text'] == 'Exit':
                            pygame.quit()
                            sys.exit()

    def render(self, screen: GameScreen):
        screen.image.render()
        self.gameovertext = screen.headline.render("Game Over", True, white)
        SCREEN.blit(self.gameovertext, (175, 100))
        render_button(screen, screen.buttons, 'text')

class GameScreen:
    def __init__(self):
        self.controllerCreator = ControllerCreator()
        pygame.init()
        pygame.mixer.init()
        self.volume = 0.5
        self.sound_volume = 0.5
        self.timer = Time()
        self.score = Score()
        self.pause = False
        self.controller = self.controllerCreator.createController("arrow")
        pygame.mixer.music.load(os.path.join(game_folder,"Assets","sounds","BGM.wav"))
        pygame.mixer.music.play(-1, 0)
        pygame.mixer.music.set_volume(self.volume)
        self.shoot_sound = sound_dict["basic_shoot"] 
        self.death_sound = sound_dict["death"] 
        self.centipede_hit_sound = sound_dict["centipede"] 
        self.missile_sound = sound_dict["missile"]
        self.button_sound = sound_dict["button"]
        self.sound_list = [self.shoot_sound, self.death_sound, self.centipede_hit_sound, self.missile_sound, self.button_sound]
        background = Hintergrund(hg_dict)
        self.image = background
        self.screen_state = startScreen()
        self.buttons = []
        self.screen_state.enter(self)
        self.font = font_dict["font_small"]
        self.headline = font_dict["font_big"]
        self.story_font = font_dict["font_tiny"]
        self.life_display = Life_Display()
        self.style = "Ufo"
        self.story_screen_shown = False

    def change_state(self, newState: screenState):
        if (self.screen_state != None):
            self.screen_state.exit()
        self.screen_state = newState
        self.screen_state.enter(self)
    
    def render(self):
        self.screen_state.render(self)

    def update(self):
        self.key_pressed = pygame.key.get_pressed()
        self.screen_state.update(self)

# Player-Lebensanzeige mit Aktualisierung    
class Life_Display:
    def __init__(self):
        self.lives = []
        self.length = 50
        self.x = 10
        self.y = 55

    def createLife_Display(self):
        if len(self.lives) == 0:
            heart_image = pygame.transform.scale(img_dict["Herz"], (30, 30))
            for i in range(3):
                self.lives.append((heart_image, (self.x + i * 40, self.y)))
                
    def render(self):
        for lives in self.lives:
            SCREEN.blit(lives[0], lives[1])

    def loseLife(self):
        if self.lives:
            self.lives.pop()
    
    def reset(self):
        self.lives = []