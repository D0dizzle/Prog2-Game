#Pseudocode

# Prüfung auf Kollision mit Screen-Begrenzeung
#def collision_with_screen():
   #if snake_head_x >= screen_width or snake_head_x < 0 or snake_head_y >= screen_height or snake_head_y < 0:
        #go_down()  # Hier sollte die entsprechende Reaktion auf die Kollision erfolgen, in dem Fall eine Zeile nach unten gehen

# Prüfung auf Kollision mit Pilzen
#for pilz in pilze:
    #if collision(snake_head, pilz):
        #go_down()  # Hier sollte die entsprechende Reaktion auf die Kollision mit einem Pilz erfolgen, in dem Fall eine Zeile nach unten gehen
#kann man bestimmt auch auf den Gegner anwenden. Dann mit game_over()

# Wenn die Schlange größer als 1 ist, muss sie sich teilen; wenn genau 1 soll der Kopf verschwinden.
    #if len(snake) == 1:
        #snake.pop()
    
    #if len(snake) < 1
        #snake.split()

#def go_down(snake, screen_widht, screen_ height):
    # hier kann auch die kollision-funktion stehen dann:
#else:
    #new_head = (new_head_x, new_head_y)
    #snake.insert(0, new_head)