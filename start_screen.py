import pygame
import sys
from settings import *
import subprocess

# Initialisieren von Pygame
pygame.init()

# Definieren von Farbe der Buttons

color_light = (170, 170, 170)

# Schriftart und Text für die Buttons
font = pygame.font.SysFont('Corbel', 35)

# Bildschirmgröße und Bildschirmerstellung
Screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Centipede") # kann angepasst werden, vielleicht "Centipede Hauptmenü"?

# Hintergrundbild laden und Daten aus settings anwenden
Background = pygame.image.load("Assets/hintergrund/parallax-background.png")
Background_scaled = pygame.transform.scale(Background, (width, height))


# Rechtecke und Texte für die Buttons, wenn wir noch weitere hinzufügen möchten, muss die ausrichtung beachtet werden.
buttons = [
    {'rect': pygame.Rect(50, 500, 200, 50), 'text': 'Start'}, # beide hinteren Werte für die Größe
    {'rect': pygame.Rect(300, 500, 200, 50), 'text': 'Button 2'},
    {'rect': pygame.Rect(550, 500, 200, 50), 'text': 'Button 3'}
]

status = True
while status:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            status = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            for button in buttons:
                if button['rect'].collidepoint(event.pos):
                    if button['text'] == 'Start':
                        subprocess.Popen(["python", "Main.py"]) # startet Main.py bzw. das Spiel
                    elif button['text'] == 'Button 2': # gewünschen Namen des Buttons eintragen, muus mit oben übereinstimmen
                        subprocess.Popen(["python", "py"]) # gewünscheten Dateiname eintragen
                    elif button['text'] == 'Button 3':
                        subprocess.Popen(["python", "py"]) # gewünschten Dateiname eintragen

    # Hintergrundbild anzeigen
    Screen.blit(Background_scaled, (0, 0))

    # Buttons erstellen und Text in den Buttons zeichnen
    for button in buttons:
        rect = pygame.Rect(button['rect'])
        pygame.draw.rect(Screen, color_light, rect, border_radius=10)
        pygame.draw.rect(Screen, white, rect, width=2, border_radius=10)
        button_text = font.render(button['text'], True, white)
        text_rect = button_text.get_rect(center=rect.center)
        Screen.blit(button_text, text_rect)

    # Aktualisieren des Bildschirms
    pygame.display.flip()

# Beenden
pygame.quit()
sys.exit()
