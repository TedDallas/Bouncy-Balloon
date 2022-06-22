#include "raylib.h"
#include <math.h>

typedef struct {
    int radius;
    int x_position;
    int y_position;
    Color color;
    bool alive;
 } Enemy;

typedef struct {
    int radius;
    int x_spawn;
    int y_spawn;
    int x_pos;
    int y_pos;
    int jump_speed;
    bool alive;
    int restart_depth;;
    Color color;
 } Player;

int main(void) {
    long frame_counter = 0; 
    const int screen_width = 1920;//GetMonitorHeight(display);
    const int screen_height = 1080;//GetMonitorWidth(display);
    SetConfigFlags(FLAG_VSYNC_HINT);
    InitWindow(screen_width, screen_height, "Bouncy Balloon (c) 2022 - by Ninja's with Guitars");
    int jump_energy = (int)(-1.0/42.0 * screen_height); 
    int player_x_spawn = (int)((float)screen_width / 4.0);
    int player_y_spawn =(int)((float)screen_height * 1.0/2.0);
    int frame_rate = 60;
    int frame_time = 1.0 / frame_rate;
    int ballon_speed = (int)(-(1.0/150.0 * (float)screen_width) * 60.0 / (float)frame_rate);
    int balloons_per_column_count = 100;
    int balloons_count = balloons_per_column_count*5;
    Enemy balloons[balloons_count];
    int hole_height = (int)(2.0/5.0*(float)screen_height);
    int gravity = (int)(1.0 / frame_rate * screen_height / 10.0);
    int score = 0;
    char score_str[10];
    int high_score = 0;
    char high_score_str[10];
    Color sky_color = (Color) { r: 135, g: 206, b: 235, a: 255 }; //Sky Blue
    float default_string_angle = PI * 0.5; 
    float string_angle = default_string_angle;

    int hole_y_pos = 0;
    int counter = 0;
    int distance = 0.0;

    float start_time = 0.0;
    float end_time = 0.0;

    SetWindowSize(screen_width, screen_height);
    //SetWindowState(FLAG_VSYNC_HINT);
    SetTargetFPS(frame_rate);
    ToggleFullscreen();
    HideCursor();
    
    Player player = (Player) {
        .radius = (int)(2.0/75.0 * (float)screen_width),
        .x_spawn = player_x_spawn,
        .y_spawn = player_y_spawn,
        .x_pos = player_x_spawn,
        .y_pos = player_y_spawn,
        .jump_speed = jump_energy,
        .alive = true,
        .restart_depth = 3 * screen_height,
        .color = (Color) { r: 255, g: 128, b: 128, a: 255 }
    };
    
    //populate balloons in the pool
    for (int i = 0; i < balloons_count; i++) 
        balloons[i] = (Enemy) {
            .radius = GetRandomValue((int)(1.0/30.0 * (float)screen_width),(int)(1.0/20.0 * (float)screen_width)),
            .x_position = screen_width+100,
            .y_position = -10,
            .color = (Color) { r: GetRandomValue(0,255), g: GetRandomValue(0,255), b: GetRandomValue(0,255), a: 255 }
        };

    SetTargetFPS(120);

    while (!WindowShouldClose()) {  // Detect window close button or ESC key
        start_time = GetFrameTime();
        
        frame_counter++;

        //capture game input
        if (IsKeyPressed(KEY_SPACE) || IsMouseButtonPressed(MOUSE_BUTTON_LEFT))
            if (player.alive)
                 player.jump_speed += jump_energy;

        //make player go up/down when bouncing up or falling
        player.y_pos += player.jump_speed;
        player.jump_speed += gravity; 
        if (player.y_pos < 0) {
            player.y_pos = 0;
            player.jump_speed = 0;
        }

        //touching the ground kills player
        if (player.y_pos >= screen_height)
            player.alive = false;

        //Make dead player wiggle back and forth because death is pain
        if (!player.alive)
            player.x_pos += GetRandomValue(-(int)(1.0/50.0 * (float)screen_width),(int)(1.0/100.0 * (float)screen_width));

        //spawn evil balloons column
        if (frame_counter % frame_rate  == 0) {
            hole_y_pos = GetRandomValue(1,screen_height-hole_height);
            counter = 0;
            for (int i = 0; i < balloons_count; i++) {
                if (!balloons[i].alive) {
                    balloons[i].radius = GetRandomValue((int)(1.0/30.0 * (float)screen_width),(int)(1.0/20.0 * (float)screen_width));
                    balloons[i].x_position = screen_width +(int)(1.0/6.0*(float)screen_width)+GetRandomValue((int)(-1.0/60.0 * (float)screen_width),(int)(1.0/60.0 * (float)screen_width));
                    if (GetRandomValue(0,2) == 1)
                        balloons[i].y_position = GetRandomValue(0,hole_y_pos);
                    else
                        balloons[i].y_position = GetRandomValue(hole_y_pos+hole_height,screen_height);
                    balloons[i].color.r = GetRandomValue(0,255);
                    balloons[i].color.g = GetRandomValue(0,255);
                    balloons[i].color.b = GetRandomValue(0,255);
                    balloons[i].alive = true;
                    counter++;
                    if (counter >= balloons_per_column_count)
                        break;
                }
            }
        }

        //move the evil balloons and kill player if player touches any balloon
        for (int i = 0; i < balloons_count; i++) {
            if (balloons[i].alive) {
                if (balloons[i].x_position > (int)(-1.0/6.0*(float)screen_width)) {
                    balloons[i].x_position += ballon_speed;
                    distance = hypot(player.x_pos - balloons[i].x_position, player.y_pos - balloons[i].y_position);
                }
                else {
                    balloons[i].alive = false;
                    distance = 100000;
                }

                if (balloons[i].alive) //if enemy is still alive
                    if (distance < player.radius + balloons[i].radius) //and if they are touching then
                        player.alive = false;
            }
        }

        //update player score as they progress, player must be alive and score is incremented every second once game has started running long enough 
        //if player_alive and frame_counter % frame_rate == 0 and frame_counter > (frame_rate * 2) + (balloon_radius * 4):
        if ((frame_counter + (player.radius * 2) ) % frame_rate == 0 && player.alive && frame_counter > frame_rate * 3) 
            score += 1;
        
        //reset game if player died and the player has fallen past the player_restart_depth (which gives us a slight delay)
        if (!player.alive && player.y_pos > screen_height + player.restart_depth) {
            player.alive = true;
            player.x_pos = player_x_spawn;
            player.y_pos = player_y_spawn;
            player.jump_speed = jump_energy;
            score = 0;
            frame_counter = 0;
            for (int i = 0; i < balloons_count; i++) 
                balloons[i].alive = false;
        }

        //reset the high score if player scores higher
        if (!player.alive)
            if (score > high_score)
            {
                high_score = score;
            }

        BeginDrawing();
        ClearBackground(sky_color);
        DrawFPS(screen_width-100,10);

        sprintf(score_str, "%i", score);
        DrawText(score_str, 10, 10, screen_height / 10, YELLOW);

        sprintf(high_score_str, "%i", high_score);
        DrawText(high_score_str, 10, screen_height / 10 + screen_height / 10 / 5, screen_height / 10, PURPLE);

        //draw the player
        string_angle = (player.jump_speed < 0) ? default_string_angle - (player.jump_speed * 0.01) : default_string_angle + (player.jump_speed * 0.01); 
        string_angle += GetRandomValue(-1,1) / 100.0;  
        DrawLine(player.x_pos,
                 player.y_pos+player.radius,
                 (int)(player.x_pos+(player.radius*3.0)*cos(string_angle)),
                 (int)(player.y_pos+(player.radius*3.0)*sin(string_angle)),
                 WHITE);
        
        DrawCircle(player.x_pos, player.y_pos, (float)player.radius, player.color); 

        //Draw evil baloons
        for (int i = 0; i < balloons_count; i++) 
            if (balloons[i].alive)
                 DrawCircle(balloons[i].x_position, balloons[i].y_position, (float)balloons[i].radius, balloons[i].color); 

        EndDrawing();
 
        end_time = start_time + frame_time;
        while (GetTime() < end_time); //hang out
    }

    ShowCursor(); // Show the mouse pointer
    ToggleFullscreen(); // Toggle out of full screen 
    CloseWindow(); // Close window and OpenGL context

    return 0;
}
