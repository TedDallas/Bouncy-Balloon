import pygame, os, time, random, math
from pygame.locals import *

os.environ['SDL_VIDEO_CENTERED'] = '1' #make sure the game window centered. CITATION: https://stackoverflow.com/questions/38703791/how-do-i-place-the-pygame-screen-in-the-middle
pygame.init() # initialize pygame game engine 
frame_counter = 0 # frame counter
screen_height = 360 # screen height for game screen window 
screen_width = 600 # screen width for game screen window
GameScreen = pygame.display.set_mode(size=(screen_width, screen_height)) # create the Game Screen to draw on
jump_energy = -12 #player maximum jump power (always a negative number because y-axis up direction is negative)
player_radius = 16 #used to set set player balloon size
player_x_pos = 200 #current x-position of the player
player_y_pos = 180 #current y-positiocontrols of the player
player_jump_speed = jump_energy #current player jump speed
player_alive = True #boolean variable to tell if the player is alive or not
player_restart_depth = 1500 #game restarts when player falls down to this depth (player_y_pos)
balloon_column_count = 75 #total number of random balloons per column
ballon_speed = -4 #fixed speed of balloons moving accross the screen to the left
balloons = [] #balloons list container
hole_height = 150 #height of the hole in the balloons column that the player must fly through
frame_rate = 60 #frame rate in frames per second

pygame.font.init() #initialize font object
score_font = pygame.font.Font(None, 50) #create font score object for displaying the player score
score = 0 #score is the number of balloon columns the player has gone through
high_score = 0 #the last high score the player achieved

playing = True #boolean used for terminating the main game loop

while playing: # main game loop
    start_time = time.time_ns() #capture frame start time
    frame_counter += 1 #Increment frame counter
    GameScreen.fill([135,206,235]) #fill screen with sky blue color

    # capture game input events
    for event in pygame.event.get(): # get pygame events for user input
        if event.type == pygame.KEYDOWN: # if the user pressed a key
            if event.key == pygame.K_ESCAPE: # if the user pressed the escape key
                playing = False #set the playing variable to False so that the game loop ends and the program ends
            if event.key == pygame.K_SPACE: #if the user pressed the space bar
                if player_alive: #if the player is still alive
                    player_jump_speed += jump_energy #make the player bounce higher by adding to the players jump speed
        if event.type == pygame.QUIT: # if user closed the window to end the game instead of pressing the escape key
            playing = False #set the playing variable to False so that the game-loop ends and the program ends

    #make player go up/down when bouncing up or falling
    if frame_counter % 2 == 0: #doing this for every other frame (so the player bounces and falls slower)
        player_y_pos += player_jump_speed #add the current jump speed to the player's y-position to move the player
        player_jump_speed += 1 #add 1 to the jump speed, since jump speed is negative based the player will change direction at 0 and start falling
        if player_y_pos < 0: #if the player trys to jump too high past the top of the screen, stop the player
            player_y_pos = 0 #force the player to be at the top of the screen
            player_jump_speed = 0 #set the player jump speed at 0 so the player will start to fall 
    
    #touching the ground kills player
    if player_y_pos >= screen_height: #player has either touched the bottom or has gone past the bottom of the screen 
        player_alive = False #player is in dead state when they touch the bottom or go lower

    #Make dead player wiggle back and forth
    if not player_alive: #if the player is now dead
        player_x_pos += random.randrange(-6,8) #randomly change the player x-position so the player wiggles back and forth as they fall

    #draw the player
    pygame.draw.line(GameScreen, (255,255,255),(player_x_pos, player_y_pos),(player_x_pos-16, player_y_pos+32),2) #draw the player balloon string
    pygame.draw.circle(GameScreen, (255,128,128), (player_x_pos, player_y_pos), 16) #draw the player balloon 

    #spawn balloons column
    if frame_counter % frame_rate == 0: #add a new balloon column once every second
        hole_y_pos = random.randrange(1,screen_height-hole_height) # randomly select top of balloon hole position
        for i in range(balloon_column_count): #create and add all balloons in the baloo20n column (limited by the balloon_column_count) 
            balloon_radius = random.randrange(10,30) #pick a random size for the balloon
            balloon_color = (random.randrange(0,255),random.randrange(0,255),random.randrange(0,255))
            balloon_x_position = screen_width+100+random.randrange(-10,10)
            if random.randrange(0,2) == 1: #if random number is 1 then ballon must be above the hole
                balloon_y_position = random.randrange(0,hole_y_pos)
            else: #else the random number is not 1, so place the balloon below the hole
                balloon_y_position = random.randrange(hole_y_pos+hole_height,screen_height)
            balloons.append({"radius"   : balloon_radius, #the balloon's size radius
                             "position" : (balloon_x_position,balloon_y_position), #randomly place balloon on the right side, but not in the hole
                             "color"    : balloon_color}) #a random balloon color
    
    #move the balloons and kill player if player touches any balloon
    last_balloon_x = 0
    for balloon in balloons:
        #move the ballon if not off the screen
        if balloon["position"][0] > -100:
            balloon["position"] = (balloon["position"][0]+ballon_speed,balloon["position"][1]) #move the baloon
            pygame.draw.circle(GameScreen, balloon["color"], balloon["position"], balloon["radius"]) #draw the balloon
            #get player disance from balloon    
            distance = math.dist([player_x_pos,player_y_pos],[balloon["position"][0],balloon["position"][1]])
            #kill player if player touches balloon
            if distance < player_radius + balloon["radius"]:
                player_alive = False
            else:
                last_balloon_x = balloon["position"][0]
    
    #update player score as they progress, player must be alive and score is incremented every second once game has started running long enough 
    if player_alive and frame_counter % frame_rate == 0 and frame_counter > frame_rate * 2:
        score += 1
    
    #reset game if player died and the player has fallen past the player_restart_depth (which gives us a slight delay)
    if not player_alive and player_y_pos > screen_height + player_restart_depth:
        player_alive = True #player is back alive
        player_x_pos = 150 #reset player x-position
        player_y_pos = 180 #reset player y-position
        player_jump_speed = jump_energy #reset jump energy, so player does not start falling at the begining
        balloons = [] #clear the balloons list
        score = 0 #reset the score to 0
        frame_counter = 0 #reset the frame counter to 0

    #reset the high score if player scores higher
    if not player_alive:
        if isinstance(score, int):
            if score > high_score:
                high_score = score 
                score = "NEW HIGH SCORE !!!"

    #show the score and high score on the screen
    high_score_text = score_font.render(str(high_score), True, (128,128,255)) #create high score text object with high score value set
    text_width, text_height = score_font.size(str(high_score)) #get the score text size so we can center it
    GameScreen.blit(high_score_text, (screen_width/2-text_width/2, 10)) #draw score text
    score_text = score_font.render(str(score), True, (255,255,128)) #create score text object with score value set
    text_width, text_height = score_font.size(str(score)) #get the high score text size so we can center it
    GameScreen.blit(score_text, (screen_width/2-text_width/2, 10 + text_height)) #draw score text
    
    #update screen 
    pygame.display.flip()

    end_time = time.time_ns() #capture end frame end time
    elapsed_time = float(end_time - start_time) # calculate time elapsed = Start Time - End Time (in nanoseconds) 
    
    # calculate sleep time = 1/60 - time elapsed since frame start (converted from nanoseconds to seconds)
    sleep_time = 1.0/60.0 - elapsed_time/1000000000.0 #sleep_time is a fraction of 1 second (Ex. 0.5 = 1/2 second)
    
    #Limit frame rate by waiting until total elapsed time equals the frame rate duration 
    if sleep_time > 0.0: # if sleep time > 0 then go to sleep until a full 1/60th of second has elapsed 
        time.sleep(sleep_time) #wait for sleep time to even out the frame rate to 1/60th of a second

# Clean up section ----------------------------------------------------------------------------------------------------------
pygame.quit() #shut down pygame