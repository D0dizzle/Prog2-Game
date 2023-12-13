#Diese Datei ist für Settings/Einstellungen gedacht!
# Imports:
import pygame
import os
import sys
from random import randint, choice

# Variablen: 
black = (0, 0, 0)
white = (255, 255, 255)
cyan = (100, 100, 255)
red = (205, 51, 51)
green = (0, 255, 0)
dark_green = (100, 255, 100)
height = 700
width = 800
FPS = 60                     #Anzahl FPS
clock = pygame.time.Clock()           #Pygame.time.Clock Objekt
seg_groesse = 25
player_size = 50
player_acc = 1.8 * 60 / FPS
player_friction = -0.2
projectiles = []
ufo_sprites = []
game_folder = os.path.dirname(__file__)
SCREEN = pygame.display.set_mode(size=(width, height))
pygame.display.set_caption("Space Centipede")


## Hintergründe: ##
#vorab PNG's laden, die transformiert werden müssen
#Dictionary mit den Hintergründen
hg_dict = {}
hg_dict["big-planet"] = {"image" : pygame.image.load(os.path.join(game_folder,"Assets","hintergrund", "parallax-space-big-planet.png")).convert_alpha()}
hg_dict["far-planets"] = {"image" : pygame.image.load(os.path.join(game_folder,"Assets","hintergrund", "parallax-space-far-planets.png")).convert_alpha()}
hg_dict["ring-planet"] = {"image" : pygame.image.load(os.path.join(game_folder,"Assets","hintergrund", "parallax-space-ring-planet.png")).convert_alpha()}
# hg_dict keys wird wert image zugewiesen

img_dict = {}
img_dict["bullet"] = pygame.image.load(os.path.join(game_folder,"Assets","ship","Bullet2.png"))
img_dict["satellite"] = pygame.image.load(os.path.join(game_folder, "Assets", "enemies", "Satellite.png"))
img_dict["ufo_gelb"] = pygame.transform.scale(pygame.image.load(os.path.join(game_folder, "Assets", "enemies", "ufo_gelb.png")),(seg_groesse,seg_groesse))
img_dict["asteroid"] = pygame.transform.scale(pygame.image.load(os.path.join(game_folder, "Assets", "enemies", "asteroid.png")),(2*seg_groesse,2*seg_groesse))
img_dict["star_image"] = pygame.image.load(os.path.join(game_folder, "Assets", "hintergrund", "headline-star.png"))
img_dict["Missile"] = pygame.image.load(os.path.join(game_folder,"Assets","ship","Missile.png"))
img_dict["Herz"] = pygame.image.load(os.path.join(game_folder,"Assets","ship","Herz.png"))

tilemap_dict = {}
tilemap_dict["TME"] = os.path.join(game_folder, "Assets","Tilemaps", "TileMapEasy.txt")
tilemap_dict["TMM"] = os.path.join(game_folder, "Assets","Tilemaps", "TileMapMedium.txt")
tilemap_dict["TMH"] = os.path.join(game_folder, "Assets","Tilemaps", "TileMapHard.txt")
tilemap_dict["TMVH"] = os.path.join(game_folder, "Assets","Tilemaps", "TileMapVeryHard.txt")

player_img_dict = {}
player_img_dict["player-5"] = pygame.transform.scale(pygame.image.load(os.path.join(game_folder, "Assets", "ship", "ship-5.png")),(player_size, player_size))
player_img_dict["player-4"] = pygame.transform.scale(pygame.image.load(os.path.join(game_folder, "Assets", "ship", "ship-4.png")),(player_size, player_size))
player_img_dict["player-3"] = pygame.transform.scale(pygame.image.load(os.path.join(game_folder, "Assets", "ship", "ship-3.png")),(player_size, player_size))
player_img_dict["player-2"] = pygame.transform.scale(pygame.image.load(os.path.join(game_folder, "Assets", "ship", "ship-2.png")),(player_size, player_size))
player_img_dict["player-1"] = pygame.transform.scale(pygame.image.load(os.path.join(game_folder, "Assets", "ship", "ship-1.png")),(player_size, player_size))
player_img_dict["player0"] = pygame.transform.scale(pygame.image.load(os.path.join(game_folder, "Assets", "ship", "ship0.png")),(player_size, player_size))
player_img_dict["player1"] = pygame.transform.scale(pygame.image.load(os.path.join(game_folder, "Assets", "ship", "ship1.png")),(player_size, player_size))
player_img_dict["player2"] = pygame.transform.scale(pygame.image.load(os.path.join(game_folder, "Assets", "ship", "ship2.png")),(player_size, player_size))
player_img_dict["player3"] = pygame.transform.scale(pygame.image.load(os.path.join(game_folder, "Assets", "ship", "ship3.png")),(player_size, player_size))
player_img_dict["player4"] = pygame.transform.scale(pygame.image.load(os.path.join(game_folder, "Assets", "ship", "ship4.png")),(player_size, player_size))
player_img_dict["player5"] = pygame.transform.scale(pygame.image.load(os.path.join(game_folder, "Assets", "ship", "ship5.png")),(player_size, player_size))

ufo_img_dict = {}
ufo_img_dict["ufo_gelb"] = pygame.transform.scale(pygame.image.load(os.path.join(game_folder, "Assets", "enemies", "Ufo_gelb.png")),(seg_groesse,seg_groesse))
ufo_img_dict["ufo_lila"] = pygame.transform.scale(pygame.image.load(os.path.join(game_folder, "Assets", "enemies", "Ufo_lila.png")),(seg_groesse,seg_groesse))
ufo_img_dict["ufo_rot"] = pygame.transform.scale(pygame.image.load(os.path.join(game_folder, "Assets", "enemies", "Ufo_rot.png")),(seg_groesse,seg_groesse))

ufo_animation_dict = {}
ufo_animation_dict["ufo3"] = pygame.transform.scale(pygame.image.load(os.path.join(game_folder, "Assets", "enemies", "Ufo_grau.png")),(seg_groesse,seg_groesse))
ufo_animation_dict["ufo2"] = pygame.transform.scale(pygame.image.load(os.path.join(game_folder, "Assets", "enemies", "Ufo_grau2.png")),(seg_groesse,seg_groesse))
ufo_animation_dict["ufo1"] = pygame.transform.scale(pygame.image.load(os.path.join(game_folder, "Assets", "enemies", "Ufo_grau3.png")),(seg_groesse,seg_groesse))
ufo_animation_dict["ufo0"] = pygame.transform.scale(pygame.image.load(os.path.join(game_folder, "Assets", "enemies", "Ufo_grau.png")),(seg_groesse,seg_groesse))

centipede_img_dict = {}
centipede_img_dict["Head"] = pygame.transform.scale(pygame.image.load(os.path.join(game_folder, "Assets", "snake", "snake.blue-head.png")),(seg_groesse,seg_groesse))
centipede_img_dict["Body"] = pygame.transform.scale(pygame.image.load(os.path.join(game_folder, "Assets", "snake", "snake.blue-body part.png")),(seg_groesse,seg_groesse))

pygame.init()
sound_dict = {}
sound_dict["basic_shoot"] = pygame.mixer.Sound(os.path.join(game_folder,"Assets","sounds","shoot.wav"))
sound_dict["missile"] = pygame.mixer.Sound(os.path.join(game_folder,"Assets","sounds","missile.wav"))
sound_dict["death"] = pygame.mixer.Sound(os.path.join(game_folder,"Assets","sounds","death_player.ogg"))
sound_dict["button"] = pygame.mixer.Sound(os.path.join(game_folder, "Assets", "sounds", "menu_select.wav"))

font_dict = {}
font_dict["font_small"] = pygame.font.Font(os.path.join(game_folder, "Assets", "fonts", "Boxy-Bold.ttf"), 35)
font_dict["font_big"] = pygame.font.Font(os.path.join(game_folder, "Assets", "fonts", "Boxy-Bold.ttf"), 65)


#### Funktionen: ####
#Funktion zum Beenden des Spiels durch "x" in der Ecke
def exit_game():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()                       #Quelle für pygame.quit(): coderslegacy.com/python/python-pygame-tutorial
            sys.exit()

#### Klassen für Settings: ####
class Hintergrund():     
    def __init__(self, dict):
        self.background = pygame.transform.scale(pygame.image.load(os.path.join(game_folder, "Assets", "hintergrund", "parallax-background.png")).convert(),(width, height))
        self.space_stars = pygame.transform.scale(pygame.image.load(os.path.join(game_folder,"Assets","hintergrund" ,"parallax-space-stars.png")).convert_alpha(),(width, height))
        self.dict = dict
        self.max_particles = 50
        self.current_particles = 0
        self.last_particles = 0
        self.particles = []
        self.animated_background = [pygame.image.load(os.path.join(game_folder,"Assets","enemies" ,"particle.png")).convert_alpha(), pygame.image.load(os.path.join(game_folder,"Assets","enemies" ,"particle2.png")).convert_alpha()]
        self.cooldown = 1

        for i in self.dict:
            x = randint(50,(width-50))
            y = randint(50,(height-200))
            dict[i]["x"] = x
            dict[i]["y"] = y
            #verschachtes dict: jedem background asset key wird ein weiteres dict hinzugefügt für die werte image, x und y
            # sieht so aus: 
            # {'big-planet': {'image': <Surface(88x87x32 SW)>, 'x': 268, 'y': 124},
            #  'far-planets': {'image': <Surface(272x160x32 SW)>, 'x': 592, 'y': 387},
            #  'ring-planet': {'image': <Surface(51x115x32 SW)>, 'x': 337, 'y': 68}}

    def render(self):
        SCREEN.blit(self.background,(0,0))
        SCREEN.blit(self.space_stars,(0,0))

        for i in self.dict:
            SCREEN.blit(self.dict[i]["image"], (self.dict[i]["x"],self.dict[i]["y"]))

        current_time = pygame.time.get_ticks()
        if current_time - self.last_particles > self.cooldown and self.current_particles < self.max_particles:
            self.last_particles = current_time                 
            self.particles.append(Particles(randint(0,width),-80, randint(2,10),choice(self.animated_background)))
            self.current_particles += 1
            self.cooldown = randint(0,60)

        for particle in self.particles:
            particle.update()

class Particles(pygame.sprite.Sprite):
    def __init__(self, x, y, vy, img):
        super().__init__()
        self.image = img
        self.x = x
        self.y = y
        self.vy = vy
    
    def update(self):
        SCREEN.blit(self.image, (self.x, self.y))
        self.y += self.vy
        if self.y  > height+50:
                self.y = -10


class TileMap:
    def __init__(self, filename):
        self.data = []
        with open(filename, 'r') as f:
            for line in f:
                self.data.append(line.strip())
        self.width = len(self.data[0])
        self.height = len(self.data)

class Collider():

    def collideObstacle(self, projectiles, enemysprites):
        for enemy in enemysprites:
            index = enemy.rect.collidelist(projectiles)
            if index != -1:    #-1 bedeutet keine Kollision deswegen muss es exkludiert werden
                enemy.status("hit")
                projectiles.pop(index)

    def collidePlayer(self, sprite, player1):
        index = player1.rect.collidelist(sprite)
        if index != -1:
            sprite.pop(index)
            player1.status("hit")        
        
    def collideCentipede(self, projectiles, enemysprites):
        for enemy in enemysprites:
            index = enemy.rect.collidelist(projectiles)
            if index != -1:    #-1 bedeutet keine Kollision deswegen muss es exkludiert werden
                enemy.status("hit", ufo_sprites)
                projectiles.pop(index)

    def collideWithWall(self, centipede, obstacles):
        for segment in centipede:
            if segment.rect.collidelist(obstacles) != -1:
                segment.status("collideWithWall", ufo_sprites)

class Time:
    def __init__(self):
        pygame.init()
        self.time = 0
        self.time_counter = 0
        self.font = pygame.font.Font(os.path.join(game_folder, "Assets", "fonts", "Boxy-Bold.ttf"), 14)

    def count_time(self):
        if self.time_counter == FPS:
            self.time += 1
            self.time_counter = 0
        elif self.time_counter < FPS:
            self.time_counter += 1
    
    def render(self):
        self.time_on_screen = self.font.render(f"Time:  {self.time}", True, white)
        SCREEN.blit(self.time_on_screen, (680, 10))

class Score:
    def __init__(self):
        pygame.init()
        self.points = 0
        self.font = pygame.font.Font(os.path.join(game_folder, "Assets", "fonts", "Boxy-Bold.ttf"), 14)

    def load_highscore(self):
        try:
            with open(os.path.join(game_folder, "Assets", "highscore.txt"), "r") as file:
                self.highscore = int(file.read())
        except FileNotFoundError:
            return 0

    def save_highscore(self):
        with open(os.path.join(game_folder,"Assets", "highscore.txt"), "w") as file:
            file.write(str(self.highscore))

    def update_highscore(self):
        if self.points > self.highscore:
            self.highscore = self.points

    def display_scores(self):
        highscore_text = self.font.render(f"Highscore: {self.highscore}", True, white)
        score_text = self.font.render(f"Score: {self.points}", True, white)
        SCREEN.blit(highscore_text, (10, 10))
        SCREEN.blit(score_text, (10, 35))

    def update_score(self, enemy1, enemy2):
        self.points += enemy1.score
        self.points += enemy2.score