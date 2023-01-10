import os
import sys

import pygame
import datetime

pygame.init()
WIDTH, HEIGHT = 640, 480
FPS = 60
clock = pygame.time.Clock()
count = 0
counter, text = 10, '10'.rjust(3)
pygame.time.set_timer(pygame.USEREVENT, 1000)
font = pygame.font.SysFont('Consolas', 30)
FRONT = [(5, 1), (0, 28), (59, 28), (62, 27), (0, 27), (0, 31)]
SIDE = [(1, 5), (2, 11), (2, 4), (0, 10), (69, 3), (0, 10), (0, 14), (0, 5), (0, 23), (0, 22), (0, 27), (0, 15)]
RIGHT = [(5, 13), (1, 8), (2, 4), (1, 9)]
LEFT = [(9, 13), (13, 9), (14, 8), (1, 10)]

def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


def terminate():
    pygame.quit()
    sys.exit()


ball_image = load_image('s_ball.png')
platphorm_image = load_image('s_platphorm.png')


class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(main_group, all_sprites)
        self.image = ball_image
        self.add(main_group)
        self.rect = self.image.get_rect().move(WIDTH / 2 - 16, HEIGHT / 4 - 16 + 32)
        self.vx = 0
        self.vy = 0
        self.count = 1

    def update(self):
        global started, lives, score
        if pygame.sprite.collide_rect(self, death):
            if score >= 500:
                score -= 500
            self.pos()
            self.change(0, 0)
            started = False
            lives -= 1
            print(lives)
        if pygame.sprite.spritecollideany(self, horizontal_borders):
            self.vy = -self.vy
        if pygame.sprite.spritecollideany(self, vertical_borders):
            self.vx = -self.vx
        if pygame.sprite.collide_mask(self, plat):
            if score >= 10:
                score -= 10
            print('Plat ' + str(pygame.sprite.collide_mask(self, plat)))
            if pygame.sprite.collide_mask(self, plat) in RIGHT:
                self.vx = 10
                self.vy = -3
            elif pygame.sprite.collide_mask(self, plat) in LEFT:
                self.vx = -10
                self.vy = -3
            else:
                if self.vx >= 0:
                    self.vx = 5
                elif self.vx < 0:
                    self.vx = -5
                self.vy = -5
        self.rect = self.rect.move(self.vx, self.vy)

    def change(self, vx, vy):
        self.vx = vx
        self.vy = vy

    def pos(self):
        self.rect = self.image.get_rect().move(WIDTH / 2 - 16, HEIGHT / 4 - 16 + 128)


class Platphorm(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(main_group, all_sprites)
        self.image = platphorm_image
        self.add(main_group)
        self.add(bouncy)
        self.rect = self.image.get_rect().move(WIDTH / 2 - 100, (8 * HEIGHT) / 10 - 10)
        self.vx = 0
        self.mask = pygame.mask.from_surface(self.image)

    def move(self, direction):
        if direction == 'left':
            self.vx = -5
        if direction == 'right':
            self.vx = 5
        if direction == 'stop':
            self.vx = 0

    def update(self):
        if self.vx > 0 and pygame.sprite.spritecollideany(self, right_borders):
            self.vx = 0
        if self.vx < 0 and pygame.sprite.spritecollideany(self, left_borders):
            self.vx = 0
        self.rect = self.rect.move(self.vx, 0)


class Border(pygame.sprite.Sprite):
    def __init__(self, x1, y1, x2, y2):
        super().__init__(all_sprites)
        if x1 == x2:
            self.add(vertical_borders)
            self.image = pygame.Surface([1, y2 - y1])
            self.rect = pygame.Rect(x1, y1, 1, y2 - y1)
            if x1 == 5:
                self.add(left_borders)
            else:
                self.add(right_borders)
        else:
            self.add(horizontal_borders)
            self.image = pygame.Surface([x2 - x1, 1])
            self.rect = pygame.Rect(x1, y1, x2 - x1, 1)


class Brick(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(main_group, all_sprites)
        self.lives = 1
        self.sprite()
        self.add(bouncy)
        self.add(bricks)
        self.rect = self.image.get_rect().move(x, y)
        self.vx = 0
        self.mask = pygame.mask.from_surface(self.image)

    def sprite(self):
        if self.lives > 0:
            pic = load_image('bricks/s_blue.png')
            pic = pygame.transform.scale(pic, (64, 32))
            self.image = pic

    def update(self):
        global score
        if pygame.sprite.collide_mask(self, mball):
            print('Brick ' + str(pygame.sprite.collide_mask(self, mball)))
            if pygame.sprite.collide_mask(mball, self) in FRONT:
                mball.vy = -mball.vy
            elif pygame.sprite.collide_mask(mball, self) in SIDE:
                mball.vx = -mball.vx
            else:
                mball.vy = -mball.vy
                mball.vx = -mball.vx
            self.lives -= 1
            score += 100
            self.sprite()
        if self.lives <= 0:
            mball.count -= 1
            score += 100
            self.kill()
            del self


class Green(Brick):
    def __init__(self, x, y):
        super(Brick, self).__init__(main_group, all_sprites)
        self.lives = 2
        self.sprite()
        self.add(bouncy)
        self.add(bricks)
        self.rect = self.image.get_rect().move(x, y)
        self.vx = 0
        self.mask = pygame.mask.from_surface(self.image)

    def sprite(self):
        if self.lives == 2:
            pic = load_image('bricks/s_green.png')
            pic = pygame.transform.scale(pic, (64, 32))
            self.image = pic
        elif self.lives == 1:
            pic = load_image('bricks/s_green_1.png')
            pic = pygame.transform.scale(pic, (64, 32))
            self.image = pic


class Brown(Brick):
    def __init__(self, x, y):
        super(Brick, self).__init__(main_group, all_sprites)
        self.lives = 3
        self.sprite()
        self.add(bouncy)
        self.add(bricks)
        self.rect = self.image.get_rect().move(x, y)
        self.vx = 0
        self.mask = pygame.mask.from_surface(self.image)

    def sprite(self):
        if self.lives == 3:
            pic = load_image('bricks/s_brown.png')
            pic = pygame.transform.scale(pic, (64, 32))
            self.image = pic
        elif self.lives == 2:
            pic = load_image('bricks/s_brown_1.png')
            pic = pygame.transform.scale(pic, (64, 32))
            self.image = pic
        elif self.lives == 1:
            pic = load_image('bricks/s_brown_2.png')
            pic = pygame.transform.scale(pic, (64, 32))
            self.image = pic


class Purple(Brick):
    def __init__(self, x, y):
        super(Brick, self).__init__(main_group, all_sprites)
        self.lives = 4
        self.sprite()
        self.add(bouncy)
        self.add(bricks)
        self.rect = self.image.get_rect().move(x, y)
        self.vx = 0
        self.mask = pygame.mask.from_surface(self.image)

    def sprite(self):
        if self.lives == 4:
            pic = load_image('bricks/s_purple.png')
            pic = pygame.transform.scale(pic, (64, 32))
            self.image = pic
        elif self.lives == 3:
            pic = load_image('bricks/s_purple_1.png')
            pic = pygame.transform.scale(pic, (64, 32))
            self.image = pic
        elif self.lives == 2:
            pic = load_image('bricks/s_purple_2.png')
            pic = pygame.transform.scale(pic, (64, 32))
            self.image = pic
        elif self.lives == 1:
            pic = load_image('bricks/s_purple_3.png')
            pic = pygame.transform.scale(pic, (64, 32))
            self.image = pic


class Ready(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(main_group, all_sprites)
        self.image = load_image('zero.png')
        self.add(ui)
        self.status = 'Ready'
        self.rect = self.image.get_rect().move(128, 128)

    def end(self):
        self.kill()
        del self


def level(num):
    filename = "data/lvl" + str(num) + '.txt'
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    level = list(map(lambda x: x.ljust(max_width, '.'), level_map))
    c = 0
    for i in range(len(level)):
        for j in range(len(level[i])):
            if level[i][j] == '1':
                Brick(int(j) * 64, int(i) * 32)
                c += 1
            if level[i][j] == '2':
                Green(int(j) * 64, int(i) * 32)
                c += 1
            if level[i][j] == '3':
                Brown(int(j) * 64, int(i) * 32)
                c += 1
            if level[i][j] == '4':
                Purple(int(j) * 64, int(i) * 32)
                c += 1
    mball.count = c

class Gui(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(ui, all_sprites)
        self.x_pos = 40
        self.y_pos = 460
        self.font = pygame.font.Font("assets/font.ttf", 30)
        self.base_color, self.hovering_color = (255, 255, 255), (0, 0, 0)
        self.text_input = str(score)
        self.text = self.font.render(self.text_input, True, self.base_color)
        self.image = self.text
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

    def update(self):
        self.text_input = str(score)
        self.text = self.font.render(self.text_input, True, self.base_color)
        self.image = self.text
        screen.blit(self.text, self.text_rect)

def writescore(n):
    f = open('data/score.txt', 'a')
    print(str(datetime.datetime.now().date()))
    f.write('\n' + str(datetime.datetime.now().date()) + ': ' + str(n))


all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
main_group = pygame.sprite.Group()
horizontal_borders = pygame.sprite.Group()
vertical_borders = pygame.sprite.Group()
left_borders = pygame.sprite.Group()
right_borders = pygame.sprite.Group()
bouncy = pygame.sprite.Group()
bricks = pygame.sprite.Group()
ui = pygame.sprite.Group()
for sprite in main_group:
    sprite.kill()
mball = Ball()
death = Border(5, HEIGHT - 5, WIDTH - 5, HEIGHT - 5)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
ended = False
lives = 3
print(lives)
Border(5, 5, WIDTH - 5, 5)
Border(5, 5, 5, HEIGHT - 5)
Border(WIDTH - 5, 5, WIDTH - 5, HEIGHT - 5)
plat = Platphorm()
a = Ready()
score = 0
txt = Gui()
started = False
running = True
started = False
lvl = 1
level(lvl)
first = True





def begin():
    print(all_sprites)


def play():
    global score, screen
    global started, lives, running, lvl, mball, a, plat, first
    pygame.init()
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONUP and started is False:
                if lives == 3:
                    first = False
                a.end()
                mball.change(0, 5)
                started = True
            if event.type == pygame.KEYDOWN:
                if started is False:
                    if lives == 3:
                        first = False
                    a.end()
                    mball.change(0, 5)
                    started = True
                if event.key == 1073741904:
                    plat.move('left')
                if event.key == 1073741903:
                    plat.move('right')
                if event.key == pygame.K_m:
                    for sprite in bricks:
                        sprite.kill()
                    lvl = lvl + 1
                    level(lvl)
            if event.type == pygame.KEYUP:
                plat.move('stop')
        if mball.count == 0:
            mball.pos()
            mball.change(0, 0)
            started = False
            lvl += 1
            level(lvl)
        if lives == 0:
            all_sprites.empty()
            begin()
            lives = 3
            writescore(score)
            score = 0
            first = True
            return True
        if first:
            for sprite in main_group:
                sprite.kill()
            for sprite in ui:
                sprite.kill()
            mball = Ball()
            death = Border(5, HEIGHT - 5, WIDTH - 5, HEIGHT - 5)
            screen = pygame.display.set_mode((WIDTH, HEIGHT))
            ended = False
            lives = 3
            print(lives)
            Border(5, 5, WIDTH - 5, 5)
            Border(5, 5, 5, HEIGHT - 5)
            Border(WIDTH - 5, 5, WIDTH - 5, HEIGHT - 5)
            plat = Platphorm()
            started = False
            running = True
            started = False
            score = 0
            txt = Gui()
            lvl = 1
            level(lvl)
            first = True
        main_group.update()
        main_group.draw(screen)
        ui.update()
        ui.draw(screen)
        pygame.display.flip()
        screen.fill((0, 0, 0))
    pygame.quit()
