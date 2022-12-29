import pygame
import sys
import os

WIDTH, HEIGHT = 640, 480
FPS = 60
clock = pygame.time.Clock()



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

    def update(self):
        if pygame.sprite.spritecollideany(self, horizontal_borders):
            self.vy = -self.vy
        if pygame.sprite.spritecollideany(self, vertical_borders):
            self.vx = -self.vx
        if pygame.sprite.collide_mask(self, plat):
            if pygame.sprite.collide_mask(plat, self)[0] < 70:
                if self.vx > 0:
                    self.vx = -self.vx
            if pygame.sprite.collide_mask(plat, self)[0] > 70:
                if self.vx < 0:
                    self.vx = -self.vx
            self.vy = -self.vy
        self.rect = self.rect.move(self.vx, self.vy)


    def change(self, vx, vy):
        self.vx = vx
        self.vy = vy

class Platphorm(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(main_group, all_sprites)
        self.image = platphorm_image
        self.add(main_group)
        self.add(bouncy)
        self.rect = self.image.get_rect().move(WIDTH / 2 - 100, (8 * HEIGHT) / 10)
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
        if pygame.sprite.collide_mask(self, mball):
            print(pygame.sprite.collide_mask(mball, self))
            if pygame.sprite.collide_mask(mball, self) == (5, 1):
                mball.vy = -mball.vy
            elif pygame.sprite.collide_mask(mball, self) == (1, 5):
                mball.vx = -mball.vx
            else:
                mball.vy = -mball.vy
                mball.vx = -mball.vx
            self.lives -= 1
            self.sprite()
        if self.lives <= 0:
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




def level1():
    brick_one_zero = Brick(1 * 64, 0)
    brick_two_zero = Brick(2 * 64, 0)
    brick_three_zero = Brick(3 * 64, 0)
    brick_four_zero = Brick(4 * 64, 0)
    brick_five_zero = Brick(5 * 64, 0)
    brick_six_zero = Brick(6 * 64, 0)
    brick_seven_zero = Brick(7 * 64, 0)
    brick_eight_zero = Brick(8 * 64, 0)
    brick_one_one = Brick(1 * 64, 1 * 32)
    brick_two_one = Brick(2 * 64, 1 * 32)
    brick_three_one = Brick(3 * 64, 1 * 32)
    brick_four_one = Brick(4 * 64, 1 * 32)
    brick_five_one = Brick(5 * 64, 1 * 32)
    brick_six_one = Brick(6 * 64, 1 * 32)
    brick_seven_one = Brick(7 * 64, 1 * 32)
    brick_eight_one = Brick(8 * 64, 1 * 32)
    brick_one_two = Brick(1 * 64, 2 * 32)
    brick_two_two = Brick(2 * 64, 2 * 32)
    brick_three_two = Brick(3 * 64, 2 * 32)
    brick_four_two = Brick(4 * 64, 2 * 32)
    brick_five_two = Brick(5 * 64, 2 * 32)
    brick_six_two = Brick(6 * 64, 2 * 32)
    brick_seven_two = Brick(7 * 64, 2 * 32)
    brick_eight_two = Brick(8 * 64, 2 * 32)

def level2():
    brick_zero_zero = Brick(0, 0)
    brick_one_zero = Brick(1 * 64, 0)
    brick_two_zero = Brick(2 * 64, 0)
    brick_three_zero = Brick(3 * 64, 0)
    brick_four_zero = Brick(4 * 64, 0)
    brick_five_zero = Brick(5 * 64, 0)
    brick_six_zero = Brick(6 * 64, 0)
    brick_seven_zero = Brick(7 * 64, 0)
    brick_eight_zero = Brick(8 * 64, 0)
    brick_nine_zero = Brick(9 * 64, 0)
    brick_zero_one = Green(0, 1 * 32)
    brick_one_one = Green(1 * 64, 1 * 32)
    brick_two_one = Green(2 * 64, 1 * 32)
    brick_three_one = Green(3 * 64, 1 * 32)
    brick_four_one = Green(4 * 64, 1 * 32)
    brick_five_one = Green(5 * 64, 1 * 32)
    brick_six_one = Green(6 * 64, 1 * 32)
    brick_seven_one = Green(7 * 64, 1 * 32)
    brick_eight_one = Green(8 * 64, 1 * 32)
    brick_nine_one = Green(9 * 64, 1 * 32)
    brick_zero_two = Brown(0, 2 * 32)
    brick_one_two = Brown(1 * 64, 2 * 32)
    brick_two_two = Brown(2 * 64, 2 * 32)
    brick_three_two = Brown(3 * 64, 2 * 32)
    brick_four_two = Brown(4 * 64, 2 * 32)
    brick_five_two = Brown(5 * 64, 2 * 32)
    brick_six_two = Brown(6 * 64, 2 * 32)
    brick_seven_two = Brown(7 * 64, 2 * 32)
    brick_eight_two = Brown(8 * 64, 2 * 32)
    brick_nine_two = Brown(9 * 64, 2 * 32)




all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
main_group = pygame.sprite.Group()
horizontal_borders = pygame.sprite.Group()
vertical_borders = pygame.sprite.Group()
left_borders = pygame.sprite.Group()
right_borders = pygame.sprite.Group()
bouncy = pygame.sprite.Group()
bricks = pygame.sprite.Group()


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    running = True
    started = False
    Border(5, 5, WIDTH - 5, 5)
    Border(5, HEIGHT - 5, WIDTH - 5, HEIGHT - 5)
    Border(5, 5, 5, HEIGHT - 5)
    Border(WIDTH - 5, 5, WIDTH - 5, HEIGHT - 5)
    mball = Ball()
    plat = Platphorm()
    level2()
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONUP and started is False:
                mball.change(5, 5)
                started = True
            if event.type == pygame.KEYDOWN:
                if started is False:
                    mball.change(5, 5)
                    started = True
                if event.key == 1073741904:
                    plat.move('left')
                if event.key == 1073741903:
                    plat.move('right')
            if event.type == pygame.KEYUP:
                plat.move('stop')



        main_group.update()
        main_group.draw(screen)
        pygame.display.flip()
        screen.fill((0, 0, 0))
    pygame.quit()