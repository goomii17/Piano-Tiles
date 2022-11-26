import os
import sys
import random
import pygame
from pygame.locals import *


class Tile:
    def __init__(self, x, y):
        self.w = WIDTH / 4
        self.h = self.w * 3 / 2
        self.x = x
        self.y = -y * self.h - 2 * self.h
        self.active = True

    def show(self):
        global gameover, delay
        if self.active:
            if self.y >= HEIGHT - 100:
                color = (233, 23, 4)
                delay += 1
                if delay == 25:
                    gameover = True
            else:
                color = (5, 10, 5)
        else:
            color = (55, 55, 55)
            s = pygame.Surface((self.w, self.h))
            s.set_alpha(128)
            s.fill(color)
            screen.blit(s, (self.x * self.w, self.y))
            return
        x, y, w, h = self.x * self.w, self.y, self.w, self.h
        pygame.draw.rect(screen, color, pygame.Rect(x, y - 2, w, h + 2))

    def fall(self, v):
        if delay == -1:
            self.y += v

    def checkClick(self):
        global score
        if self.active:
            if self.x == 0 and keys[K_d]:
                if abs((self.y + self.h / 2) - (HEIGHT - WIDTH * 3 / 8)) < self.h / 2:
                    self.active = False
                    score += 1
            if self.x == 1 and keys[K_f]:
                if abs((self.y + self.h / 2) - (HEIGHT - WIDTH * 3 / 8)) < self.h / 2:
                    self.active = False
                    score += 1
            if self.x == 2 and keys[K_j]:
                if abs((self.y + self.h / 2) - (HEIGHT - WIDTH * 3 / 8)) < self.h / 2:
                    self.active = False
                    score += 1
            if self.x == 3 and keys[K_k]:
                if abs((self.y + self.h / 2) - (HEIGHT - WIDTH * 3 / 8)) < self.h / 2:
                    self.active = False
                    score += 1


def loadNewSong():
    global songs
    ind = random.randint(0, len(songs) - 1)
    pygame.mixer.music.load("./songs/" + songs[ind])


def drawLine():
    color = (255, 255, 255)
    color2 = (50, 200, 50)
    r = 8
    f_s = 24
    x, y, w, h = 0, HEIGHT - WIDTH * 3 / 8, WIDTH, 1
    pygame.draw.rect(screen, color, pygame.Rect(x, y, w, h))
    x = WIDTH / 8
    y = HEIGHT - WIDTH * 3 / 8
    font = pygame.font.SysFont("Arial", f_s, bold=True)
    if keys[K_d]:
        text = font.render("D", True, color2)
    else:
        text = font.render("D", True, color)
    text_rect = text.get_rect(center=(x, y))
    screen.blit(text, text_rect)
    x += WIDTH / 4
    if keys[K_f]:
        text = font.render("F", True, color2)
    else:
        text = font.render("F", True, color)

    text_rect = text.get_rect(center=(x, y))
    screen.blit(text, text_rect)
    x += WIDTH / 4
    if keys[K_j]:
        text = font.render("J", True, color2)
    else:
        text = font.render("J", True, color)
    text_rect = text.get_rect(center=(x, y))
    screen.blit(text, text_rect)
    x += WIDTH / 4
    if keys[K_k]:
        text = font.render("K", True, color2)
    else:
        text = font.render("K", True, color)
    text_rect = text.get_rect(center=(x, y))
    screen.blit(text, text_rect)


def push_Tile():
    global tiles
    ran = random.sample([0, 1, 2, 3], 1)[0]
    tiles.append(Tile(ran, len(tiles)))


def createGame(n):
    global tiles, dificulty
    tiles = []
    i = 0
    i2 = 0
    while i2 < n:
        ran = random.sample([0, 1, 2, 3], 1)
        if i2 != n - 1:
            if dificulty == "normal" and random.random() < 0.2:
                ran = random.sample([[0, 2], [1, 3]], 1)[0]
            elif dificulty == "hard" and random.random() < 0.3:
                ran = random.sample([[0, 2], [1, 3]], 1)[0]
        for j in range(len(ran)):
            tiles.append(Tile(ran[j], i))
            i2 += 1
        i += 1


def restart(full):
    global tiles, start, level, gameover, delay, score, bg
    global starting_speed, music_delay, last_score, best_score, v
    tiles = []
    createGame(n)
    start = False
    level = 0
    gameover = False
    delay = -1
    if full:
        v = starting_speed
        score = 0
        music_delay = 0
        bg = pygame.image.load("./bgs/bg{0}.png".format(random.randint(1, 4)))


def checkMiss():
    global gameover, delay, v, start, dificulty, score
    x = -1
    if keys[K_d]:
        x = 0
    elif keys[K_f]:
        x = 1
    elif keys[K_j]:
        x = 2
    elif keys[K_k]:
        x = 3

    if x != -1:
        touched = False
        for t in tiles:
            if t.x == x:
                if (
                    abs((t.y + t.h / 2) - (HEIGHT - WIDTH * 3 / 8))
                    <= t.h / 2 + 12 + score / 10
                ):
                    touched = True
        if not touched:
            x, y, w, h = (
                WIDTH / 4 * x,
                (HEIGHT - WIDTH * 3 / 8) - tiles[0].h / 2,
                WIDTH / 4,
                tiles[0].h,
            )
            pygame.draw.rect(screen, (123, 4, 66), pygame.Rect(x, y, w, h))
            gameover = True
    if tiles[len(tiles) - 1].y > HEIGHT:
        restart(False)
        start = True
        v += 1
    if dificulty == "speed" and tiles[0].y > HEIGHT + tiles[0].h:
        del tiles[0]
        push_Tile()


pygame.init()
WIDTH = 342
HEIGHT = 600
pygame.display.list_modes()
screen = pygame.display.set_mode([WIDTH, HEIGHT])
FPS = 60
fpsClock = pygame.time.Clock()
pygame.font.init()
mouse = []
keys = []
pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.mixer.init()
songs = os.listdir("songs")
loadNewSong()
bg = pygame.image.load("bgs/bg{0}.png".format(random.randint(1, 4)))

dificulty = (sys.argv[1]) if len(sys.argv) > 1 else "easy"
dificulty = dificulty if dificulty in ["easy", "normal", "hard", "speed"] else "easy"
n = int(sys.argv[2]) if len(sys.argv) > 2 else 50
starting_speed = int(sys.argv[3]) if len(sys.argv) > 3 else 5
aceleration = 0.0001  # float(sys.argv[4]) if len(sys.argv) > 4 else 0.0001
if dificulty == "normal":
    aceleration *= 10
if dificulty == "hard":
    aceleration *= 75
if dificulty == "speed":
    aceleration *= 100
    n = 100
tiles = []
createGame(n)
start = False
level = 0
gameover = False
delay = -1
v = 5
score = 0
size = 16
size_v = 1
my_time = 0

if not os.path.exists("records/"):
    os.mkdir("records/")

if os.path.exists("records/record_" + dificulty + ".txt"):
    with open("records/record_" + dificulty + ".txt", "r") as f:
        best_score = int(f.readline().strip())
        last_score = int(f.readline().strip())
else:
    best_score = 0
    last_score = 0

music_delay = 0

while True:
    mouse = pygame.mouse.get_pressed()
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit(0)
    screen.blit(bg, (0, 0))
    if gameover:
        FPS = 20
        best_score = max(best_score, score)
        last_score = score
        pygame.mixer.music.stop()
        loadNewSong()
        txt = "GAME OVER"
        myfont = pygame.font.SysFont("Arial", 48, bold=True)
        textsurface = myfont.render(txt, False, (0, 0, 0))
        text_rect = textsurface.get_rect(center=(WIDTH / 2, HEIGHT / 5))
        screen.blit(textsurface, text_rect)
        txt = "Last Score: " + str(last_score)
        myfont = pygame.font.SysFont("Arial", 28, bold=True)
        textsurface = myfont.render(txt, False, (0, 0, 0))
        text_rect = textsurface.get_rect(center=(WIDTH / 2, HEIGHT / 3))
        screen.blit(textsurface, text_rect)
        txt = "Best Score: " + str(best_score)
        myfont = pygame.font.SysFont("Arial", 28, bold=True)
        textsurface = myfont.render(txt, False, (0, 0, 0))
        text_rect = textsurface.get_rect(center=(WIDTH / 2, HEIGHT / 3 + 35))
        screen.blit(textsurface, text_rect)
        txt = "Press r to restart"
        myfont = pygame.font.SysFont("Arial", int(size), bold=True)
        textsurface = myfont.render(txt, False, (0, 0, 0))
        text_rect = textsurface.get_rect(center=(WIDTH / 2, HEIGHT / 2))
        screen.blit(textsurface, text_rect)
        size += size_v
        if size == 16 or size == 24:
            size_v *= -1
        with open("records/record_" + dificulty + ".txt", "w") as f:
            f.write(str(best_score) + "\n")
            f.write(str(last_score) + "\n")
        if keys[K_r]:
            restart(True)
            start = True
        my_time += 1
    elif start:
        FPS = 60
        if music_delay < 100:
            music_delay += 1
        elif music_delay == 100:
            pygame.mixer.music.play(loops=-1)
            music_delay += 1
        for t in tiles:
            t.show()
            t.checkClick()
            if not keys[K_p]:
                t.fall(v)
        txt = "Score: " + str(score)
        myfont = pygame.font.SysFont("Arial", 24, bold=True)
        textsurface = myfont.render(txt, False, (255, 255, 255))
        screen.blit(textsurface, (15, WIDTH / 16))
        checkMiss()
        v += aceleration
    else:
        FPS = 20
        txt = "PIANO TILES"
        myfont = pygame.font.SysFont("Algerian", 46, bold=True)
        textsurface = myfont.render(txt, False, (0, 0, 0))
        text_rect = textsurface.get_rect(center=(WIDTH / 2, HEIGHT / 8))
        screen.blit(textsurface, text_rect)
        txt = "Last Score: " + str(last_score)
        myfont = pygame.font.SysFont("Arial", 28, bold=True)
        textsurface = myfont.render(txt, False, (0, 0, 0))
        text_rect = textsurface.get_rect(center=(WIDTH / 2, HEIGHT / 3))
        screen.blit(textsurface, text_rect)
        txt = "Best Score: " + str(best_score)
        myfont = pygame.font.SysFont("Arial", 28, bold=True)
        textsurface = myfont.render(txt, False, (0, 0, 0))
        text_rect = textsurface.get_rect(center=(WIDTH / 2, HEIGHT / 3 + 35))
        screen.blit(textsurface, text_rect)
        txt = "Press s to start"
        myfont = pygame.font.SysFont("Arial", int(size), bold=True)
        textsurface = myfont.render(txt, False, (0, 0, 0))
        text_rect = textsurface.get_rect(center=(WIDTH / 2, HEIGHT / 2))
        screen.blit(textsurface, text_rect)
        size += size_v
        if size == 16 or size == 24:
            size_v *= -1
        my_time += 1
        if keys[K_s]:
            start = True
    drawLine()
    pygame.display.flip()
    fpsClock.tick(FPS)
