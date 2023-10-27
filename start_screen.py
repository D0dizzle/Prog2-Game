import pygame
import sys
from settings import *
pygame.init()

# light shade of the button 
color_light = (170,170,170) 
  
# dark shade of the button 
color_dark = (100,100,100)

font = pygame.font.SysFont('Corbel',35) 
  
# rendering a text written in 
# this font 
text = font.render('quit' , True , white) 


Screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Centipede")

Background = pygame.image.load("/Users/justusraabe/Documents/Fortgeschrittene Programmierung/Prog2-Game/Assets/hintergrund/parallax-background.png")


Background_scaled= pygame.transform.scale(Background,(width, height))
# Using blit to copy content from one surface to other
Screen.blit(Background_scaled, (0, 0))
 
# paint screen one time
pygame.display.flip()
status = True
while (status):
 
  # iterate over the list of Event objects
  # that was returned by pygame.event.get() method.
    for ev in pygame.event.get():  

        #checks if a mouse is clicked 
        if ev.type == pygame.MOUSEBUTTONDOWN: 
              
            #if the mouse is clicked on the 
            # button the game is terminated 
            if width/2 <= mouse[0] <= height/2+140 and height/2 <= mouse[1] <= height/2+40: 
                exit_game() 
      
    # stores the (x,y) coordinates into 
    # the variable as a tuple 
    mouse = pygame.mouse.get_pos() 
      
    # if mouse is hovered on a button it 
    # changes to lighter shade  
    if width/2 <= mouse[0] <= width/2+140 and height/2 <= mouse[1] <= height/2+40: 
        pygame.draw.rect(screen,color_light,[width/2,height/2,140,40]) 
          
    else: 
        pygame.draw.rect(screen,color_dark,[width/2,height/2,140,40]) 
      
    # superimposing the text onto our button 
    screen.blit(text , (width/2+50,height/2))
    screen.blit(Background_scaled, (height, width))

    pygame.display.flip()





import pygame 
import sys


# initializing the constructor 
pygame.init() 

# screen resolution 
res = (720,720) 

# opens up a window 
screen = pygame.display.set_mode(res) 

# white color 
color = (255,255,255) 

# light shade of the button 
color_light = (170,170,170) 

# dark shade of the button 
color_dark = (100,100,100) 

# stores the width of the 
# screen into a variable 
width = screen.get_width() 

# stores the height of the 
# screen into a variable 
height = screen.get_height() 

# defining a font 
smallfont = pygame.font.SysFont('Corbel',35) 

# rendering a text written in 
# this font 
text = smallfont.render('quit' , True , color) 

while True: 
	
	for ev in pygame.event.get(): 

		if ev.type == pygame.QUIT: 
			pygame.quit() 
			
		#checks if a mouse is clicked 
		if ev.type == pygame.MOUSEBUTTONDOWN: 
			
			#if the mouse is clicked on the 
			# button the game is terminated 
			if width/2 <= mouse[0] <= width/2+140 and height/2 <= mouse[1] <= height/2+40: 
				pygame.quit() 
				
	# fills the screen with a color 
	screen.fill((60,25,60)) 
	
	# stores the (x,y) coordinates into 
	# the variable as a tuple 
	mouse = pygame.mouse.get_pos() 
	
	# if mouse is hovered on a button it 
	# changes to lighter shade 
	if width/2 <= mouse[0] <= width/2+140 and height/2 <= mouse[1] <= height/2+40: 
		pygame.draw.rect(screen,color_light,[width/2,height/2,140,40]) 
		
	else: 
		pygame.draw.rect(screen,color_dark,[width/2,height/2,140,40]) 
	
	# superimposing the text onto our button 
	screen.blit(text , (width/2+50,height/2)) 
	
	# updates the frames of the game 
	pygame.display.update() 
