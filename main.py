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
powerup_message_timer = 0  # Frames to show the power-up message

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
    glClearColor(0.3, 0.5, 0.8, 1.0)
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

def draw_scenery():
    glColor3f(0.3, 0.2, 0.1)
    for z in range(int(ball_z - 100), int(ball_z + 100), 10):
        for x in [-ground_width/2 - 2.5, ground_width/2 + 2.5]:
            glPushMatrix()
            glTranslatef(x, 1, z)
            glScalef(0.2, 2.0, 0.2)
            glutSolidCube(2.0)
            glPopMatrix()
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

    if welcome_screen or game_over:
        glutSwapBuffers()
        return

    gluLookAt(ball_x, 5.0, ball_z - 15.0, ball_x, ball_y + ball_radius, ball_z, 0.0, 1.0, 0.0)

    glPushMatrix()
    glColor3f(0.1, 0.4, 0.1)
    square_size = 2.0
    render_distance = 1000
    glBegin(GL_QUADS)
    for x in range(int(-ground_width/2), int(ground_width/2), int(square_size)):
        for z in range(int(ball_z - render_distance), int(ball_z + render_distance), int(square_size)):
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
    glColor3f(0.0, 0.0, 0.3)  # Deep blue color
    glutSolidSphere(ball_radius, 20, 20)
    glPopMatrix()

    for (ox, oz) in obstacles:
        glPushMatrix()
        glTranslatef(ox, obstacle_size/2, oz)
        glColor3f(1.0, 0.0, 0.0)
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
    if powerup_message_timer > 0:
        draw_text(window_width // 2 - 80, window_height // 2 + 100, "Power-Up Collected!", font=GLUT_BITMAP_TIMES_ROMAN_24, r=1.0, g=1.0, b=0.0)

    draw_text(10, window_height - 20, f"Score: {int(score)}")
    draw_text(10, window_height - 40, f"Health: {health}")
    glutSwapBuffers()

def keyboard(key, x, y):
    global playing, game_over, ball_x, jumping, ball_vel_y, welcome_screen
    if key in (b'\r', b'\n', b'\x0D'):
        if welcome_screen:
            welcome_screen = False
        elif not playing:
            reset_game()
    elif key == b'\x1b':
        glutLeaveMainLoop()
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

def update():
    global ball_x, ball_y, ball_z, ball_vel_y, jumping, score, health, playing, powerup_message_timer
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
                powerup_message_timer = 100  # Show message for 100 frames (~1.5 seconds)

        score += 0.1

    if powerup_message_timer > 0:
        powerup_message_timer -= 1

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

