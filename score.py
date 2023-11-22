from settings import *

class Score():

    def __init__(self):
        self.score = 0
        self.font = pygame.font.SysFont('Corbel', 35)

    def load_highscore(self):
        try:
            with open("highscore.txt", "r") as file:
                self.highscore= int(file.read())
        except FileNotFoundError:
            return 0

    def save_highscore(self):
        with open("highscore.txt", "w") as file:
            file.write(str(self.highscore))

    def update_highscore(self):
        if self.score > self.highscore:
            self.highscore = self.score

    # Innerhalb der display_scores-Funktion
    def display_scores(self):
        highscore_text = self.font.render(f"Highscore: {self.highscore}", True, white)
        score_text = self.font.render(f"Score: {self.score}", True, white)
        screen.blit(highscore_text, (10, 10))
        screen.blit(score_text, (10, 50))

