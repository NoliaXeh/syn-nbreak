import pygame
import time
from pygame.locals import *

global win, font


def render_cell(x, y, value):
    global win, font
    x *= 25
    y *= 25
    g = 255 - abs((value - 127))
    g /= 255
    g *= 200
    g = int(g)
    pygame.draw.rect(win, (value, g, 255 - value), Rect(x, y, 24, 24))
    s = str(value)
    if len(s) < 3:
        s = ' ' + s
    lbl = font.render(str(value), 1, (255, 255, 255))
    win.blit(lbl, (x + 3, y + 7))

def render_all(mat):
    for y in range(len(mat)):
        for x in range(len(mat[y])):
            if mat[y][x]:
                render_cell(x, y, mat[y][x])

def render_ball(x, y):
    global win
    pygame.draw.circle(win, (255, 255, 255), (int(x), int(y)), 2)

def move_ball(x, y, dx, dy, mat):
    if ball_on_cell(x + dx, y, mat):
        return x - dx, y, -dx, dy
    if ball_on_cell(x, y + dy, mat):
        return x, y - dy, dx, -dy
    if x < 0:
        return 0, y, -dx, dy
    if x > 25 * 20:
        return 25 * 20, y, -dx, dy
    if y < 0:
        return x, 0, dx, -dy
    if y > 480:
        return x, 480, dx, -dy
    return x + dx, y + dy, dx, dy

def ball_on_cell(x, y, mat):
    try:
        x = int(x)
        y = int(y)
        if mat[y // 25][x // 25]:
            mat[y // 25][x // 25] -= 1
            if mat[y // 25][x // 25] < 0:
                mat[y // 25][x // 25] = 0
            return x // 25, y // 25
        return None
    except Exception as e:
        return None

if __name__ == '__main__':
    pygame.init()
    
    win = pygame.display.set_mode((640, 480))
    font = pygame.font.SysFont("monospace", 10)

    mat = [[255  for i in range(20)] for i in range(10)]
    #x, y, dx, dy = 320, 450, 1, 1
    nb_ball = 100
    next_loader = [(320, 450, 5, -5) for _ in range(nb_ball)]
    balls = []
    i = 0
    in_game = True
    cd = 0.05
    last = 2 * cd
    loader = []
    speed = 0
    start_speed = 1
    while in_game:
        win.fill((0, 0, 0))
        render_all(mat)
        for e in pygame.event.get():
            if e.type == QUIT:
                quit()
        for j in range(len(balls)):
            if balls[j] == None:
                continue
            ox, oy, odx, ody = balls[j]
            x, y, dx, dy = move_ball(ox, oy, odx, ody, mat)
            render_ball(x, y)
            if (y > 475):
                next_loader.append((320, 450, 5, -5))
                balls[j] = None
            else:
                #dx = ((dx > 0) - 0.5) * 2 * speed
                #dy = ((dy > 0) - 0.5) * 2 * speed
                balls[j] = x, y, dx, dy
        k = pygame.key.get_pressed()
        if k[pygame.K_SPACE]:
            for i in range(len(balls)):
                if balls[i]:
                    next_loader.append(balls[i])
                    balls[i] = None
            next_loader = loader + next_loader
            i = len(loader)
        launch, mx, my = False, 0, 0
        launch = pygame.mouse.get_pressed()[0]
        mx, my = pygame.mouse.get_pos()
        if time.time() - last > cd and i < len(loader):
            balls.append(loader[i])
            i += 1
            last = time.time()
        if i >= len(loader) and balls.count(None) == len(balls):
            dx, dy = next_loader[0][:2]
            if my > 420:
                my = 420
            dx -= mx
            dy -= my
            dx *= 1000
            dy *= 1000
            pygame.draw.line(win, (255, 0, 0), (next_loader[0][:2]), (mx - dx, my - dy))
        speed += 0.005
        if launch and i >= len(loader) and balls.count(None) == len(balls):
            balls = []
            loader = next_loader
            next_loader = []
            for j in range(len(loader)):
                x, y, dx, dy = loader[j]
                dx = mx - x
                dy = my - y
                n = (dx ** 2 + dy ** 2) ** 0.5
                dx /= n
                dy /= n
                dx *= speed
                dy *= speed
                loader[j] = x, y, dx, dy
            i = 0
            speed = start_speed
        pygame.display.flip()


