######################################################################
# Below are few extra features in this snake game.
#
# I've added a functionaity to keep track of the best score in this py
# file. The score is tracked by using a file named best_score.txt
# The program overwrites this file if the score is greater than any
# privious score.
#
# [1]After the game ends This displays Best score and the user's score
# [2]The Welcome to snake game image displayed in the opening has also
# been modified.
######################################################################

import pygame
import random
import time
pygame.init()

#######################################
######## Initialize the colors#########
white = (255,255,255)
blue = (0,0,255)
green = (0,255,0)
light_green = (0,200,0)
red = (255,0,0)
light_red = (200,0,0)
yellow = (255,255,0)
black = (0,0,0)
snake_color = (109,223,42)
######################################

clock = pygame.time.Clock() 

score_position_in_pixel = [0,0]
window_width_in_pixels = 800
window_height_in_pixels = 600
snake_size = 7
snake_speed = 7

is_game_over = False
can_we_close_game = False
current_snake_pos_xaxis = window_width_in_pixels/2
current_snake_pos_yaxis = window_height_in_pixels/2

##############################################
font_style = pygame.font.SysFont('sarai', 24)
score_font = pygame.font.SysFont('rasa',28)
##############################################

game_window = pygame.display.set_mode((window_width_in_pixels, window_height_in_pixels)) 
pygame.display.set_caption('SNAKE GAME') 

############################## Helper Functions #######################################################
def load_and_show_snake_image(w,l):
    snake_img = pygame.image.load('Welcome.png')
    game_window.blit(snake_img,(w,l))

def show_game_over(w,l):
    game_over_img = pygame.image.load('game_over.png')
    game_window.blit(game_over_img,(w,l))

def show_current_score(score):
    value = score_font.render(f'Your score: {score}', True, yellow)
    game_window.blit(value, score_position_in_pixel)

def display_message(txt,color,w,l):
    mesg = font_style.render(txt,True, color)
    game_window.blit(mesg, [w,l])

def show_snake(snake_size, snake_list):
    global snake_color
    # Initially snake body is represented by a circle
    # as snake eats food its body grows
    # this is acheived by appending the initial body with similar circle
    # based on the number of food the snake has eaten.
    #
    # Here snake_list consists the current position of the snake
    # to draw snake body in each frame
    for x in snake_list:
        #print(x[0], x[1])
        #pygame.draw.rect(game_window, snake_color, [x[0],x[1], snake_size,snake_size])
        pygame.draw.circle(game_window, snake_color,[x[0],x[1]], snake_size)
        
def quit_game():
    pygame.quit()
    quit()

# Button function for display of buttons
def button(msg, btn_xpos, btn_ypos, btn_width, btn_height, inactive_color, active_color, action = None):
    mouse = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.MOUSEBUTTONDOWN:

            if btn_xpos+btn_width > mouse[0] > btn_xpos and btn_ypos+btn_height > mouse[1] > btn_ypos:
                action()

    if btn_xpos+btn_width > mouse[0] > btn_xpos and btn_ypos+btn_height > mouse[1] > btn_ypos:
        pygame.draw.rect(game_window,active_color,[btn_xpos, btn_ypos, btn_width, btn_height])
    else:
        pygame.draw.rect(game_window,inactive_color,[btn_xpos, btn_ypos, btn_width, btn_height])

    display_message(msg,black, btn_xpos, btn_ypos)
    pygame.display.update()

#########################################################################################################
def main(): # main GAME LOOP
 
    global can_we_close_game, is_game_over 
    
    global  current_snake_pos_xaxis, current_snake_pos_yaxis 
    
    x_change = 0
    y_change = 0
    
    snake_list = []
    length_of_snake = 1

    food_position_x = round(random.randrange(0,window_width_in_pixels - snake_size) /10.0 )* 10.0
    food_position_y = round(random.randrange(0, window_height_in_pixels - snake_size) / 10.0 ) *10.0

    while is_game_over != True:         #While loop for the screen to get displayed continuously

        pygame.display.update()
        game_window.fill(black)
        # This below works only after the game
        # is over
        cnt = 0
        
        # Game closes if either snake touches the borders of game window or it 
        # touches itself. Correspondingly can_we_close_game is set to TRUE.
        while can_we_close_game == True:
            cnt += 1
            mouse = pygame.mouse.get_pos()

            show_game_over(window_width_in_pixels*.4,window_height_in_pixels*.3)
            pygame.display.update()
            # introduce a delay to display game over image
            if cnt == 1:
                clock.tick(0.25)
            
            # Here we check if the current score > best score
            # If so, rewrites the best score.
            # best score (it checks for the file named best_score.txt)
            # in the current directory
            
            current_score = length_of_snake - 1
            
            best_score_file = open('best_score.txt')
            best_score = int(best_score_file.read())
            best_score_file.seek(0)

            if current_score > best_score:
                best_score_file = open('best_score.txt', 'w+')
                best_score_file.write(str(length_of_snake - 1))
                display_message(f'Best-score:{length_of_snake-1}', white,0,70)
            else:
                display_message(f'Best-score:{best_score}', blue,0,70)

            display_message('Do you want to play again?',green,0,100)
            button('YES',10,131, 80,40,light_green,green,main)
            button('NO',100,130, 80,40,light_red,red,quit_game)

            show_current_score(current_score)

            pygame.display.update()

        # Here we handle movement of the snake using arrow keys
        for event in pygame.event.get():
            # if event is quit / if exit button is pressed it exits from the screen
            if event.type == pygame.QUIT:
                is_game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -snake_size
                    y_change = 0
                elif event.key == pygame.K_RIGHT:
                    x_change = snake_size
                    y_change = 0
                elif event.key == pygame.K_UP:
                    x_change = 0
                    y_change = -snake_size
                elif event.key == pygame.K_DOWN:
                    x_change = 0
                    y_change = snake_size
        
        current_snake_pos_xaxis += x_change
        current_snake_pos_yaxis += y_change
     ######################################################################################   
     # IF YOU DONT WANT END THE GAME IF SNAKE TOUCHES THE BORDER REMOVE THE BELOW COMMENTS
     #   if current_snake_pos_xaxis > window_width_in_pixels:
     #       current_snake_pos_xaxis = 0
     #   elif current_snake_pos_xaxis < 0:
     #       current_snake_pos_xaxis = window_width_in_pixels
     #   elif current_snake_pos_yaxis > window_height_in_pixels:
     #      current_snake_pos_yaxis = 0
     #   elif current_snake_pos_yaxis < 0:
     #       current_snake_pos_yaxis = window_height_in_pixels
     ######################################################################################
     
        if (current_snake_pos_xaxis not in range(0, window_width_in_pixels) ) \
            or (current_snake_pos_yaxis not in range(0,window_height_in_pixels) ):
            can_we_close_game = True

        game_window.fill(black)
        pygame.draw.rect(game_window,red, [int(food_position_x), int(food_position_y), snake_size,snake_size])
        #pygame.draw.circle(game_window,red,[int(food_position_x), int(food_position_y)], 5)
        
        snake_head =[]
        snake_head.append(current_snake_pos_xaxis)
        snake_head.append(current_snake_pos_yaxis)

        # snake list holds the current position of the snake to draw snake body 
        # in each frame
        snake_list.append(snake_head)
        
        # snake list is altered to ensure number of elements in snake_list
        # to be equal to food eaten by snake i.e: length_of_snake
        if len(snake_list) > length_of_snake:
            del snake_list[0]

        for x in snake_list[:-1]:
            if x == snake_head:
                can_we_close_game = True  # if snake collides itself then game is over

        show_snake(snake_size,snake_list)
        show_current_score(length_of_snake -1) # Displays current score

        pygame.display.update()
        
        
        if abs(current_snake_pos_xaxis - int(food_position_x)) <= 5 \
            and abs(current_snake_pos_yaxis == int(food_position_y)) <= 5:
            food_position_x = round(random.randrange(0, window_width_in_pixels - snake_size) / 10.0) * 10.0
            food_position_y = round(random.randrange(0, window_height_in_pixels - snake_size) / 10.0) * 10.0
            length_of_snake += 1   # increases the food eaten depending
                                    #on the lenght of the snake
        clock.tick(snake_speed)
        
    ####################################################################
    #### If game is over just exit and stop showing the game window ####
    pygame.quit()
    quit()
    ####################################################################
    
####################################################################################################


# {
# Driver Code starts
if __name__ == "__main__":
    # write your code here
    
    load_and_show_snake_image(window_width_in_pixels*.4,window_height_in_pixels*.3)
    
    display_message('SNAKE GAME',green,window_width_in_pixels/3 + 50,window_height_in_pixels/1.8)
    
    #display_message('Feed the snakes',white,window_width_in_pixels/3 + 50,window_height_in_pixels/1.8 + 30)
    
    display_message('Feed the snakes', white, window_width_in_pixels/3 + 53, window_height_in_pixels/1.8 + 30)
    
    pygame.display.update()
    
    clock.tick(.25)
    
    main()

# } Driver Code ends

