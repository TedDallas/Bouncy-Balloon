import pygame, time, random, math

pygame.init() #initialize the game engine
frame_counter = 0 #frame counter used for timing things
GameScreen = pygame.display.set_mode(size=(0, 0), flags=pygame.HWSURFACE|pygame.FULLSCREEN, vsync=1) # create the Game Screen to draw on
screen_height = GameScreen.get_height()  #Max point for y-axis (min is always 0)
screen_width = GameScreen.get_width() #Max point for x-axis (min is always 0)
jump_energy = -int(1.0/30.0 * screen_height)#player maximum jump power (always a negative number because y-axis up direction is negative)
player_radius = int(2.0/75.0 * screen_width) #radius used when drawing player balloon 
player_x_spawn = screen_width / 4
player_y_spawn = int(screen_height * 1.0/2.0)
player_x_pos = player_x_spawn #current x-position of the player
player_y_pos = player_y_spawn #current y-position of the player
player_jump_speed = jump_energy #current player jump speed
player_alive = True 
player_restart_depth = 3 * screen_height #game restarts when player falls to this depth (player_y_pos)
balloon_column_count = 50 #total number of random balloons per column
ballon_speed = int(-(1.0/150.0 * screen_width)) #fixed speed of balloons moving accross the screen to the left
balloons = [] #balloons list container
hole_height = int(2.0/5.0*screen_height)  #height of the hole in the balloons column that the player must fly through
frame_rate = 60 #frame rate in frames per second
gravity = int(1.0 / frame_rate * screen_height / 6.0)
BALLOON_DEAD_YPOS = -100
pygame.font.init() #initialize font object
score_font = pygame.font.Font(None, int(1.0/12.0 * screen_width)) #create font score object for displaying the player score
score = 0 #score is the number of balloon columns the player has gone through
high_score = 0 #the last high score the player achieved

playing = True #boolean used for terminating the main game loop

#Enemy balloon to be stored in balloons list
class Enemy:
    def __init__(self,Radius,Position,Color,Alive):
        self.radius = Radius
        self.position = Position
        self.color = Color
        self.alive = Alive

pygame.mouse.set_visible(False) #no one wants to see the mouse cursor

while playing: # main game loop
    start_time = time.time_ns() #capture frame start time, used for pegging frame rate which is less jumpy than clock.tick()
    frame_counter += 1 #Increment frame counter
    GameScreen.fill([135,206,235]) #fill screen with sky blue color

    # capture game input events
    for event in pygame.event.get(): # get pygame events for user input
        if event.type == pygame.KEYDOWN: # if the user pressed a key
            if event.key == pygame.K_ESCAPE: # if the user pressed the escape key
                playing = False #set the playing variable to False so that the game loop ends and the program ends
            elif player_alive: #if the player is still alive
                player_jump_speed += jump_energy #make the player bounce higher by adding to the players jump speed
        if event.type == pygame.QUIT: # if user closed the window to end the game instead of pressing the escape key
            playing = False #set the playing variable to False so that the game-loop ends and the program ends

    #make player go up/down when bouncing up or falling
    if frame_counter % 2 == 0: #doing this for every other frame (so the player bounces and falls slower)
        player_y_pos += player_jump_speed #add the current jump speed to the player's y-position to move the player
        player_jump_speed += gravity #add gravity to the jump speed, since jump speed is negative based the player will change direction at 0 and start falling
        if player_y_pos < 0: #if the player trys to jump too high past the top of the screen, stop the player
            player_y_pos = 0 #force the player to be at the top of the screen
            player_jump_speed = 0 #set the player jump speed at 0 so the player will start to fall 
    
    #touching the ground kills player
    if player_y_pos >= screen_height: #player has either touched the bottom or has gone past the bottom of the screen 
        player_alive = False #player is in dead state when they touch the bottom or go lower

    #Make dead player wiggle back and forth because death is pain
    if not player_alive: #if the player is now dead
        player_x_pos += random.randrange(-int(1.0/100.0 * screen_width),int(1.0/75.0 * screen_width)) #randomly change the player x-position so the player wiggles back and forth as they fall

    #draw the player
    pygame.draw.arc(GameScreen, (255,255,255), [player_x_pos-player_radius,player_y_pos,player_radius,player_radius*2], 3*math.pi/2, 2*math.pi, 2)
    pygame.draw.circle(GameScreen, (255,128,128), (player_x_pos, player_y_pos), player_radius) #draw the player balloon 

    #populate balloons pool
    if len(balloons) == 0: #add balloons
        for i in range(balloon_column_count * 5): #(limited by the balloon_column_count time 6
            balloons.append(Enemy(Radius = random.randrange(int(1.0/30.0 * screen_width),int(1.0/20.0 * screen_width)), 
                                  Position = (screen_width+100,-10), 
                                  Color = (random.randrange(128,255),random.randrange(128,255),random.randrange(128,255)),
                                  Alive = False))

    #spawn evil balloons column
    if frame_counter % frame_rate == 0: #add a new balloon column once every second
        hole_y_pos = random.randrange(1,screen_height-hole_height) # randomly select top of balloon hole position
        counter = 0
        for balloon in balloons: #create and add all balloons in the baloon column (limited by the balloon_column_count) 
            if not balloon.alive:
                balloon_x_position = screen_width+(1.0/6.0*screen_width)+random.randrange(-int(1.0/60.0 * screen_width),int(1.0/60.0 * screen_width))
                if random.randrange(0,2) == 1: #if random number is 1 then ballon must be above the hole
                    balloon_y_position = random.randrange(0,hole_y_pos)
                else: #else the random number is not 1, so place the balloon below the hole
                    balloon_y_position = random.randrange(hole_y_pos+hole_height,screen_height)
                balloon.radius = random.randrange(int(1.0/30.0 * screen_width),int(1.0/20.0 * screen_width)) #pick a random size for the balloon
                balloon.position = (balloon_x_position,balloon_y_position)
                balloon.color = (random.randrange(0,255),random.randrange(0,255),random.randrange(0,255))
                balloon.alive = True
                counter += 1
                if counter >= balloon_column_count:
                    break

    #move the evil balloons and kill player if player touches any balloon
    for balloon in balloons:
        #move the ballon if not off the screen
        if balloon.alive:
            if balloon.position[0] > -int(1.0/6.0*screen_width):
                balloon.position = (balloon.position[0]+ballon_speed,balloon.position[1]) #move the baloon
                pygame.draw.circle(GameScreen, balloon.color, balloon.position, balloon.radius) #draw the balloon
                #get player disance from balloon    
                distance = math.dist([player_x_pos,player_y_pos],[balloon.position[0],balloon.position[1]])
                #kill player if player touches balloon
                if distance < player_radius + balloon.radius:
                    player_alive = False
            else:
                balloon.alive = False
    
    #update player score as they progress, player must be alive and score is incremented every second once game has started running long enough 
    #if player_alive and frame_counter % frame_rate == 0 and frame_counter > (frame_rate * 2) + (balloon_radius * 4):
    if (frame_counter + (player_radius * 2) ) % frame_rate == 0 and player_alive and frame_counter > frame_rate * 3: 
        score += 1
    
    #reset game if player died and the player has fallen past the player_restart_depth (which gives us a slight delay)
    if not player_alive and player_y_pos > screen_height + player_restart_depth:
        player_alive = True #player is back alive
        player_x_pos = player_x_spawn #reset player x-position
        player_y_pos = player_y_spawn #reset player y-position
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

    #show high score on the screen
    high_score_text = score_font.render(str(high_score), True, (128,128,255)) #create high score text object with high score value set
    text_width, text_height = score_font.size(str(high_score)) #get the score text size so we can center it
    GameScreen.blit(high_score_text, (screen_width/2-text_width/2, 10)) #draw score text

    #show score on the screen
    score_text = score_font.render(str(score), True, (255,255,128)) #create score text object with score value set
    text_width, text_height = score_font.size(str(score)) #get the high score text size so we can center it
    GameScreen.blit(score_text, (screen_width/2-text_width/2, 10 + text_height)) #draw score text
     
    pygame.display.flip() #update screen 

    time.sleep(max(0.0,1.0/60.0 - float(time.time_ns() - start_time)/1000000000.0)) #sleep for time remaining before 1/60th of one second has elapsed. Smooth got to be. 

pygame.mouse.set_visible(True)
pygame.quit() #shut down
