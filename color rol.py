from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import sys
import math
import random

# Game state variables
playing = False
game_over = False
score = 0.0
health = 3
welcome_screen = True

# Ball properties
ball_radius = 1.0
ball_x = 0.0
ball_y = 0.0
ball_z = 0.0
ball_speed_z = 0.2
ball_speed_x = 0.6
ball_vel_y = 0.0
jumping = False

# Ground dimensions
ground_width = 20.0
ground_depth = 400.0

# Obstacles and Powerups
obstacles = []
powerups = []
obstacle_size = 2.0
powerup_size = 1.0
last_spawn_z = 0.0
spawn_distance = 50.0
min_spawn_gap = 10.0

# Trail of the ball
trail = []

# Window size
window_width = 800
window_height = 600

def reset_game():
    global score, health, ball_x, ball_y, ball_z, ball_vel_y, jumping
    global obstacles, powerups, last_spawn_z, trail, game_over, playing
    score = 0.0
    health = 3
    ball_x = 0.0
    ball_y = 0.0
    ball_z = 0.0
    ball_vel_y = 0.0
    jumping = False
    obstacles = []
    powerups = []
    trail = []
    last_spawn_z = 0.0
    while last_spawn_z < ball_z + spawn_distance:
        spawn_new_object()
    game_over = False
    playing = True

def spawn_new_object():
    global last_spawn_z, obstacles, powerups
    spawn_z = last_spawn_z + min_spawn_gap + random.uniform(0, 5.0)
    margin = 1.0
    spawn_x = random.uniform(-ground_width/2 + margin, ground_width/2 - margin)
    if random.random() < 0.7:
        obstacles.append((spawn_x, spawn_z))
    else:
        powerups.append((spawn_x, spawn_z))
    last_spawn_z = spawn_z

def init():
    glClearColor(0.3, 0.5, 0.8, 1.0)  # Softer sky tone
    glEnable(GL_DEPTH_TEST)
    glShadeModel(GL_SMOOTH)

def draw_text(x, y, text, font=GLUT_BITMAP_HELVETICA_18, r=1.0, g=1.0, b=1.0):
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, window_width, 0, window_height)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    glColor3f(r, g, b)
    glRasterPos2f(x, y)
    for ch in text:
        glutBitmapCharacter(font, ord(ch))
    glMatrixMode(GL_MODELVIEW)
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

def draw_glow():
    glPushAttrib(GL_ENABLE_BIT)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glColor4f(0.4, 0.4, 1.0, 0.2)
    glutSolidSphere(ball_radius + 0.4, 20, 20)
    glPopAttrib()

def draw_powerup_glow():
    glPushAttrib(GL_ENABLE_BIT)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glColor4f(1.0, 1.0, 0.0, 0.2)
    glutSolidSphere(powerup_size * 0.8, 10, 10)
    glPopAttrib()

def draw_fancy_welcome_screen():
    glDisable(GL_DEPTH_TEST)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, window_width, 0, window_height)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    glBegin(GL_QUADS)
    glColor3f(0.1, 0.1, 0.3)
    glVertex2f(0, 0)
    glVertex2f(window_width, 0)
    glColor3f(0.2, 0.2, 0.5)
    glVertex2f(window_width, window_height)
    glVertex2f(0, window_height)
    glEnd()
    glTranslatef(window_width/2, window_height/2 + 100, 0)
    glColor4f(0.6, 0.6, 1.0, 0.5)
    glutSolidSphere(80, 40, 40)
    glLoadIdentity()
    draw_text(window_width/2 - 200, window_height/2 + 60, "★ WELCOME TO THE 3D BALL GAME ★", GLUT_BITMAP_TIMES_ROMAN_24, 1, 1, 0)
    draw_text(window_width/2 - 180, window_height/2 + 20, "Use A/D or Arrow Keys to Move", GLUT_BITMAP_HELVETICA_18, 1, 1, 1)
    draw_text(window_width/2 - 120, window_height/2 - 10, "Press Space to Jump", GLUT_BITMAP_HELVETICA_18, 1, 1, 1)
    draw_text(window_width/2 - 150, window_height/2 - 40, "Press ENTER to Start Playing", GLUT_BITMAP_HELVETICA_18, 1, 0.9, 0.3)
    draw_text(window_width/2 - 140, window_height/2 - 70, "Press ESC to Exit the Game", GLUT_BITMAP_HELVETICA_18, 1, 0.5, 0.5)
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)
    glEnable(GL_DEPTH_TEST)

def draw_game_over_screen():
    glDisable(GL_DEPTH_TEST)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, window_width, 0, window_height)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    glBegin(GL_QUADS)
    glColor3f(0.3, 0.0, 0.0)
    glVertex2f(0, 0)
    glVertex2f(window_width, 0)
    glColor3f(0.5, 0.1, 0.1)
    glVertex2f(window_width, window_height)
    glVertex2f(0, window_height)
    glEnd()
    glTranslatef(window_width/2, window_height/2 + 100, 0)
    glColor4f(1.0, 0.0, 0.0, 0.5)
    glutSolidSphere(80, 40, 40)
    glLoadIdentity()
    draw_text(window_width/2 - 100, window_height/2 + 60, "GAME OVER", GLUT_BITMAP_TIMES_ROMAN_24, 1, 1, 0)
    draw_text(window_width/2 - 160, window_height/2 + 20, f"Your Score: {int(score)}", GLUT_BITMAP_HELVETICA_18, 1, 1, 1)
    draw_text(window_width/2 - 140, window_height/2 - 10, "Press ENTER to Restart", GLUT_BITMAP_HELVETICA_18, 1, 0.9, 0.3)
    draw_text(window_width/2 - 120, window_height/2 - 40, "Press ESC to Exit", GLUT_BITMAP_HELVETICA_18, 1, 0.5, 0.5)
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)
    glEnable(GL_DEPTH_TEST)

def draw_scenery():
    # Draw trees at intervals along the road sides
    glColor3f(0.3, 0.2, 0.1)  # Trunk color
    for z in range(int(ball_z - 100), int(ball_z + 100), 10):
        for x in [-ground_width/2 - 2.5, ground_width/2 + 2.5]:
            glPushMatrix()
            glTranslatef(x, 1, z)
            glScalef(0.2, 2.0, 0.2)
            glutSolidCube(2.0)
            glPopMatrix()
            # Tree foliage
            glColor3f(0.0, 0.6, 0.0)
            glPushMatrix()
            glTranslatef(x, 3.5, z)
            glutSolidSphere(1.0, 10, 10)
            glPopMatrix()

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    draw_scenery()
    if welcome_screen:
        draw_fancy_welcome_screen()
        glutSwapBuffers()
        return
    if game_over:
        draw_game_over_screen()
        glutSwapBuffers()
        return
    cam_x = ball_x
    cam_y = 5.0
    cam_z = ball_z - 15.0
    gluLookAt(cam_x, cam_y, cam_z, ball_x, ball_y + ball_radius, ball_z, 0.0, 1.0, 0.0)
    glPushMatrix()
    glColor3f(0.1, 0.4, 0.1)
    glTranslatef(ball_x, 0.0, ball_z - ball_z % ground_depth)
    glBegin(GL_QUADS)
    # Infinite moving ground (in Z direction)
    square_size = 2.0
    for x in range(int(-ground_width/2), int(ground_width/2), int(square_size)):
        for z in range(int(ball_z - 200), int(ball_z + 200), int(square_size)):
            if (x + z) % 4 == 0:
                glColor3f(0.2, 0.6, 0.2)
            else:
                glColor3f(0.1, 0.3, 0.1)
            glVertex3f(x, 0.0, z)
            glVertex3f(x + square_size, 0.0, z)
            glVertex3f(x + square_size, 0.0, z + square_size)
            glVertex3f(x, 0.0, z + square_size)
    glEnd()
    glPopMatrix()
    glPushMatrix()
    glTranslatef(ball_x, ball_y + ball_radius, ball_z)
    draw_glow()
    glColor3f(0.2, 0.2, 1.0)
    glutSolidSphere(ball_radius, 20, 20)
    glPopMatrix()
    glColor3f(1.0, 0.0, 0.0)
    for (ox, oz) in obstacles:
        glPushMatrix()
        glTranslatef(ox, obstacle_size/2, oz)
        glutSolidCube(obstacle_size)
        glPopMatrix()
    for (px, pz) in powerups:
        glPushMatrix()
        glTranslatef(px, powerup_size/2, pz)
        draw_powerup_glow()
        glColor3f(1.0, 1.0, 0.0)
        glutSolidSphere(powerup_size/2, 10, 10)
        glPopMatrix()
    if len(trail) > 1:
        glColor3f(1.0, 0.0, 1.0)
        glBegin(GL_LINE_STRIP)
        for (tx, ty, tz) in trail:
            glVertex3f(tx, ty, tz)
        glEnd()
    draw_text(10, window_height - 20, f"Score: {int(score)}")
    draw_text(10, window_height - 40, f"Health: {health}")
    if not playing:
        msg = "Game Over! Press Enter to restart" if game_over else "Press Enter to Start"
        draw_text(window_width/2 - len(msg) * 10 / 2, window_height/2, msg, GLUT_BITMAP_HELVETICA_18, 1, 0, 0)
    glutSwapBuffers()

def keyboard(key, x, y):
    global playing, game_over, ball_x, jumping, ball_vel_y, welcome_screen
    if key in (b'\r', b'\n', b'\x0D'): # Enter key compatibility
        if welcome_screen:
            welcome_screen = False
        elif not playing:
            reset_game()
    elif key == b'':  # Escape key
        glutLeaveMainLoop()  # Clean exit from GLUT loop
    elif key == b' ':
        if playing and not jumping:
            jumping = True
            ball_vel_y = 0.3
    elif key in (b'a', b'A'):
        if playing:
            ball_x += ball_speed_x
            ball_x = min(ball_x, ground_width/2 - ball_radius)
    elif key in (b'd', b'D'):
        if playing:
            ball_x -= ball_speed_x
            ball_x = max(ball_x, -ground_width/2 + ball_radius)
# (These are already defined earlier in the script.)

def update():
    global ball_x, ball_y, ball_z, ball_vel_y, jumping, score, health, playing, game_over
    if welcome_screen:
        glutPostRedisplay()
        return
    if playing:
        ball_z += ball_speed_z
        if jumping:
            ball_vel_y -= 0.01
            ball_y += ball_vel_y
            if ball_y <= 0.0:
                ball_y = 0.0
                ball_vel_y = 0.0
                jumping = False
        if ball_z + spawn_distance > last_spawn_z:
            spawn_new_object()
        trail.append((ball_x, ball_y + ball_radius, ball_z))
        while trail and trail[0][2] < ball_z - 50.0:
            trail.pop(0)
        for obs in obstacles[:]:
            ox, oz = obs
            if oz < ball_z - 5:
                obstacles.remove(obs)
                continue
            if abs(ball_x - ox) < (ball_radius + obstacle_size/2) and abs(ball_z - oz) < (ball_radius + obstacle_size/2):
                if ball_y < obstacle_size:
                    health -= 1
                    obstacles.remove(obs)
                    if health <= 0:
                        playing = False
                        game_over = True
                        break
        if not playing:
            glutPostRedisplay()
            return
        for pu in powerups[:]:
            px, pz = pu
            if pz < ball_z - 5:
                powerups.remove(pu)
                continue
            dx = ball_x - px
            dz = ball_z - pz
            dy = (ball_y + ball_radius) - (powerup_size/2)
            dist = math.sqrt(dx*dx + dy*dy + dz*dz)
            if dist < (ball_radius + powerup_size/2):
                score += 10
                powerups.remove(pu)
        score += 0.1
    glutPostRedisplay()

def reshape(width, height):
    global window_width, window_height
    window_width = width
    window_height = height
    if height == 0:
        height = 1
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(60.0, width / float(height), 0.1, 500.0)
    glMatrixMode(GL_MODELVIEW)

def special_keys(key, x, y):
    global ball_x, jumping, ball_vel_y
    if not playing:
        return
    if key == GLUT_KEY_LEFT:
        ball_x += ball_speed_x
        ball_x = min(ball_x, ground_width/2 - ball_radius)
    elif key == GLUT_KEY_RIGHT:
        ball_x -= ball_speed_x
        ball_x = max(ball_x, -ground_width/2 + ball_radius)
    elif key == GLUT_KEY_UP:
        if not jumping:
            jumping = True
            ball_vel_y = 0.3

def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA | GLUT_DEPTH)
    glutInitWindowSize(window_width, window_height)
    glutInitWindowPosition(100, 100)
    glutCreateWindow(b"3D Ball Game")
    init()
    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glutKeyboardFunc(keyboard)
    glutSpecialFunc(special_keys)
    glutIdleFunc(update)
    glutMainLoop()

if __name__ == "__main__":
    main()
