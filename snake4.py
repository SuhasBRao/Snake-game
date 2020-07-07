import pygame
import random
import time
pygame.init()

white = (255,255,255)
blue = (0,0,255)
green = (0,255,0)
light_green = (0,200,0)

red = (255,0,0)
light_red = (200,0,0)

yellow = (255,255,0)

black = (0,0,0)

clock = pygame.time.Clock()

score_pos = [0,0]
display_width = 800
display_height = 600
snake_block = 10
snake_speed = 7
snake_img = pygame.image.load('snake_img.png')

font_style = pygame.font.SysFont('comicsansms', 24)
score_font = pygame.font.SysFont('nakula',20)

d = pygame.display.set_mode((display_width,display_height)) # for layout where d stands for the 
                                                            # display surface
pygame.display.set_caption('SNAKE GAME') # sets the tile of the project

# The Snake_Img function displays 
#the starting snake image
def Snake_Img(w,l):

    d.blit(snake_img,(w,l))

# Your_score funciton keeps track of the current score
def Your_score(score):
    value = score_font.render(f'Your score:{score}', True, yellow)
    d.blit(value, score_pos)
   
def message(txt,color,w,l):
    mesg = font_style.render(txt,True, color)
    d.blit(mesg, [w,l])

# our_snake function display the snake 
# after each food
def our_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(d, red, [x[0],x[1], snake_block,snake_block])

def quit_game():
        pygame.quit()
        quit()

# Button function for display of buttons
def button(msg,x,y,w,h,ic,ac, action = None):
    mouse = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            
            if x+w > mouse[0] > x and y+h > mouse[1] > y:
                action()
           
    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(d,ac,[x,y,w,h])
    else:
        pygame.draw.rect(d,ic,[x,y,w,h])

    message(msg,black, x, y)
    pygame.display.update()

def game_loop(): # main GAME LOOP
    
    game_over = False
    game_close = False

    x1 = display_width/2
    y1 = display_height/2
    x_change = 0
    y_change = 0
    
    snake_list = []
    length_of_snake = 1


    foodx = round(random.randrange(0,display_width - snake_block) /10.0 )* 10.0
    foody = round(random.randrange(0, display_height - snake_block) / 10.0 ) *10.0
    
    while not game_over:						#While loop for the screen to get displayed 
       
        pygame.display.update()
        d.fill(black)
# This below works only after the game 
# is over  
        while game_close == True:
            
            mouse = pygame.mouse.get_pos()
            message('You lost, Do you want to play again?',green,0,100) 
# This function crestes the exit and replay buttons

            button('YES',display_width/4, display_height/2.5, 80,40,light_green,green,game_loop)
            button('NO',display_width/2.5, display_height/2.5, 80,40,light_red,red,quit_game)
            
            Your_score(length_of_snake -1)
# This part of the code is there to check if the current
# best score (it checks for the file named best_score.txt)
# in the current directory
            myfile = open('best_score.txt')
            best_score = int(myfile.read())
            myfile.seek(0)

            if length_of_snake-1 > best_score:
                myfile = open('best_score.txt', 'w+')
                myfile.write(str(length_of_snake - 1))
                message(f'Best-score:{length_of_snake-1}', white,0,130)
            else:
                message(f'Best-score:{best_score}', blue,0,130)
            pygame.display.update()

# The below loop is responsible for movements of the snake            
        for event in pygame.event.get():# until quit button is pressed
        	
        	if event.type == pygame.QUIT:
        		game_over = True     # if event is quit / if exit button is
                                     # pressed it exits from the screen
        	if event.type == pygame.KEYDOWN:
        		if event.key == pygame.K_LEFT:
        			x_change = -snake_block
        			y_change = 0
        		elif event.key == pygame.K_RIGHT:
        			x_change = snake_block
        			y_change = 0
        		elif event.key == pygame.K_UP:
        			x_change = 0
        			y_change = -snake_block
        		elif event.key == pygame.K_DOWN:
        			x_change = 0
        			y_change = snake_block

        x1 += x_change
        y1 += y_change 
     # IF YOU DONT WANT END THE GAME IF SNAKE TOUCHES THE BORDER REMOVE THE BELOW COMMENTS 
     #   if x1 > display_width:
     #       x1 = 0
     #   elif x1 < 0:
     #       x1 = display_width
     #   elif y1 > display_height:
     #      y1 = 0
     #   elif y1 < 0:
     #       y1 = display_height
        if x1 >= display_width or x1 <= 0 or y1 >= display_height or y1<=0:
            game_close = True

        d.fill(black)
        pygame.draw.rect(d,green, [int(foodx), int(foody), snake_block- 5,snake_block - 5])
        snake_head =[]
        snake_head.append(x1)
        snake_head.append(y1)

        snake_list.append(snake_head)
        
        if len(snake_list) > length_of_snake:
            del snake_list[0]

        for x in snake_list[:-1]:
            if x == snake_head:
                game_close = True  # if snake collides itself then game is over

        our_snake(snake_block,snake_list)
        Your_score(length_of_snake -1) # Displays current score

        pygame.display.update()
        
        if x1 == int(foodx) and y1 == int(foody):
            foodx = round(random.randrange(0, display_width - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, display_height - snake_block) / 10.0) * 10.0
            length_of_snake += 1   # increases the food eaten depending 
                                    #on the lenght of the snake
        clock.tick(snake_speed)
    
    pygame.quit()
    quit()

Snake_Img(display_width*.32,display_height*.07)
message('WELCOME TO SNAKE GAME',green,display_width/3,display_height/1.8)
pygame.display.update()
clock.tick(.25)
game_loop()