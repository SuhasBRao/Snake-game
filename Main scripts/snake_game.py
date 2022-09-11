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
try:
    import sys
    import pygame
    import random
    from os.path import exists
except ModuleNotFoundError as e:
    print()
    print("Please make sure you have installed necessary modules!!")
    print("Below module was not found")
    print(e.name)
    sys.exit()

pygame.init()

########################################
######## Initialize the colors #########
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

game_over = False
can_we_stop_game = False
current_snake_pos_xaxis = window_width_in_pixels/2
current_snake_pos_yaxis = window_height_in_pixels/2

##############################################
font_style = pygame.font.SysFont('sarai', 24)
score_font = pygame.font.SysFont('rasa',28)
##############################################

game_window = pygame.display.set_mode((window_width_in_pixels, window_height_in_pixels)) 
pygame.display.set_caption('SNAKE GAME') 
        
#########################################################################################################
def main(): 
 
    global can_we_stop_game, game_over 
    
    global  current_snake_pos_xaxis, current_snake_pos_yaxis 
    
    x_change = 0
    y_change = 0
    
    snake_list = []
    length_of_snake = 1 #initial length of snake , it increases as it eats food

    food_position_x = round(random.randrange(0, window_width_in_pixels - snake_size) /10.0 )* 10.0
    food_position_y = round(random.randrange(0, window_height_in_pixels - snake_size) / 10.0 ) *10.0

    while not game_over:         #While loop for the screen to get displayed continuously

        pygame.display.update()
        game_window.fill(black)
        
        # Here we handle movement of the snake using arrow keys
        for event in pygame.event.get():
            # if event is quit / if exit button is pressed it exits from the screen
            if event.type == pygame.QUIT:
                game_over = True
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
            or (current_snake_pos_yaxis not in range(0, window_height_in_pixels) ):
            can_we_stop_game = True

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

        # if snake collides itself then game is over
        for x in snake_list[:-1]:
            if x == snake_head:
                can_we_stop_game = True  

        show_snake(snake_size,snake_list)
        show_current_score(length_of_snake -1) 
        
        # The snake eats food if it is near the food and 
        # length_of_snake is updated everytime the snake eats
        
        if abs(current_snake_pos_xaxis - int(food_position_x)) <= 5 \
                and abs(current_snake_pos_yaxis - int(food_position_y)) <= 5:
                    
            food_position_x = round(random.randrange(0, window_width_in_pixels - snake_size) / 10.0) * 10.0
            food_position_y = round(random.randrange(0, window_height_in_pixels - snake_size) / 10.0) * 10.0
            length_of_snake += 1   # increases the food eaten depending
                                    #on the lenght of the snake
        
        clock.tick(snake_speed)
        
        _cnt = 0
        # Game closes if either snake touches the borders of game window or it 
        # touches itself. Correspondingly can_we_stop_game is set to TRUE.
        while can_we_stop_game:
            
            _cnt += 1
        
            show_game_over(window_width_in_pixels*.4, window_height_in_pixels*.3)
            
            # introduce a delay to display game over image
            if _cnt == 1:
                clock.tick(0.25)
            
            current_score = length_of_snake - 1
            
            check_best_score_to_overwrite(current_score)

            display_message('Do you want to play again?', green, 0, 100)
            
            # shows two buttons to either continue to play or opt for exit
            show_buttons('YES', main)
            show_buttons('NO', quit_game)

            show_current_score(current_score)

    ####################################################################
    #### If game is over just exit and stop showing the game window ####
    
    quit_game()

##############################################################################
def show_game_over(w,l):
    game_over_img = pygame.image.load('game_over.png')
    game_window.blit(game_over_img,(w,l))
    pygame.display.update()
    
    
def check_best_score_to_overwrite(current_score):
    best_score_file = open('best_score.txt', 'r+')
    best_score = int(best_score_file.read())
    best_score_file.seek(0)

    if current_score > best_score:
        #best_score_file = open('best_score.txt', 'w+')
        best_score_file.write(str(current_score))
        display_message(f'Best-score:{current_score}', white,0,70)
    else:
        display_message(f'Best-score:{best_score}', blue,0,70)
        

def display_message(txt,color,w,l):
    mesg = font_style.render(txt,True, color)
    game_window.blit(mesg, [w,l])
    

def show_buttons(msg, action = None):
    btn_xpos, btn_ypos, btn_width, btn_height, btn_color = grab_values_for_button(msg)
    inactive_color, active_color = btn_color
    
    mouse_pos = pygame.mouse.get_pos()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if mouse_pos[0] in range(btn_xpos, btn_xpos + btn_width) \
            and mouse_pos[1] in range(btn_ypos, btn_ypos + btn_height):
                action()

    if mouse_pos[0] in range(btn_xpos, btn_xpos + btn_width) \
        and mouse_pos[1] in range(btn_ypos, btn_ypos + btn_height):
        pygame.draw.rect(game_window, active_color, [btn_xpos, btn_ypos, btn_width, btn_height])
    else:
        pygame.draw.rect(game_window, inactive_color, [btn_xpos, btn_ypos, btn_width, btn_height])

    display_message(msg,black, btn_xpos, btn_ypos)
    pygame.display.update()


def grab_values_for_button(txt_on_button):
    if txt_on_button == 'YES':
        return 10,131, 80,40, (light_green,green)
    if txt_on_button == 'NO':
        return 100,130, 80,40 , (light_red, red)
 

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
        #pygame.draw.rect(game_window, snake_color, [x[0],x[1], snake_size,snake_size])
        pygame.draw.circle(game_window, snake_color,[x[0],x[1]], snake_size)


def show_current_score(score):
    value = score_font.render(f'Your score: {score}', True, yellow)
    game_window.blit(value, score_position_in_pixel)
    pygame.display.update()


def quit_game():
    pygame.quit()
    quit() 


def load_and_show_snake_image(w,l):
    snake_img = pygame.image.load('Welcome.png')
    game_window.blit(snake_img,(w,l))
    
def check_if_all_files_exist(files_list):
    for file_name in files_list:
        file_exists = exists(file_name)
        if not file_exists:
            raise FileNotFoundError(file_name)
    return True

########################################################################################################


# {
# Driver Code starts
if __name__ == "__main__":
    

    # Ensure all the necessary files are present before running the main() function
    try:
        files_to_check = ["best_score.txt", "Welcome.png", "game_over.png"]
        check_if_all_files_exist(files_to_check)
        
    except FileNotFoundError as e:
        print()
        print(e)
        print("File not found. Please ensure the above file is the same directory !!")
        sys.exit()
        
    else:
        load_and_show_snake_image(window_width_in_pixels*.4,window_height_in_pixels*.3)

        display_message('SNAKE GAME',green,window_width_in_pixels/3 + 50,window_height_in_pixels/1.8)
        
        display_message('Feed the snakes', white, window_width_in_pixels/3 + 53, window_height_in_pixels/1.8 + 30)
        
        pygame.display.update()
        
        clock.tick(.25)
        
        main()

# } Driver Code ends