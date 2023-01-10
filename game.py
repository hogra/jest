import pygame

from tools import load_image, writescore

pygame.init()
WIDTH, HEIGHT = 640, 480  # устанавливаю размеры экрана
FPS = 60
clock = pygame.time.Clock()
font = pygame.font.SysFont('Consolas', 30)

# загружаю основные спрайты - мячика и платформы
ball_image = load_image('s_ball.png')
platphorm_image = load_image('s_platphorm.png')


class Ball(pygame.sprite.Sprite):  # класс мячика (очевидно)
    def __init__(self):
        super().__init__(main_group, all_sprites)
        self.image = ball_image
        self.add(main_group)
        self.rect = self.image.get_rect().move(WIDTH / 2 - 16, HEIGHT / 4 - 16 + 32)
        # в начале, мячик всегда устанавливается чуть ниже центра экрана
        self.vx = 0  # и стоит неподвижно
        self.vy = 0
        self.count = 1
        # когда мячик рушит кирпичи, он уменьшает свой счет кирпичей на уровне, если их не осталось, загружается
        # следующий уровень

    def update(self):
        global started, lives, score
        if pygame.sprite.collide_rect(self, death):  # если падает вниз,
            if score >= 500:
                score -= 500  # игрок теряет 500 очков
            self.pos()  # мячик возвращается в начальную позицию
            self.change(0, 0)  # становится неподвижным
            started = False  # ждет действий от игрока
            lives -= 1  # и теряет жизнь
        if pygame.sprite.spritecollideany(self, horizontal_borders):
            self.vy = -self.vy  # если мячик сталкивается с горизонтальной стенкой, он меняет скорость по y
        if pygame.sprite.spritecollideany(self, vertical_borders):
            self.vx = -self.vx  # если с вертикальной, соответственно, по x
        if pygame.sprite.collide_mask(self, plat):  # если сталкивается с платформой
            if score >= 10:
                score -= 10  # игрок теряет 10 очков
            print('Plat ' + str(pygame.sprite.collide_mask(self, plat)))
            if pygame.sprite.collide_mask(self, plat)[1] not in [14, 13, 12]:  # если сяч попал не в центр
                if pygame.sprite.collide_mask(self, plat)[0] == 1:  # а в правый край
                    self.vx = 10  # он увеличивает скорость по x
                    self.vy = -3  # и уменьшает по y
                elif pygame.sprite.collide_mask(self, plat)[1] == 1 or pygame.sprite.collide_mask(self, plat)[0] == 9:
                    self.vx = -10  # если в левый край, то же, но в другую сторону
                    self.vy = -3
            else:  # если все-таки в центр,
                if self.vx >= 0:  # возвращает скорость по x
                    self.vx = 5
                elif self.vx < 0:
                    self.vx = -5
                self.vy = -5  # и y к обычной
        self.rect = self.rect.move(self.vx, self.vy)  # и мячик движется по x и y

    def change(self, vx, vy):  # функция для ручной смены скорости
        self.vx = vx
        self.vy = vy

    def pos(self):  # функция для возвращения мячика в начальную позицию
        self.rect = self.image.get_rect().move(WIDTH / 2 - 16, HEIGHT / 4 - 16 + 128)


class Platphorm(pygame.sprite.Sprite):  # класс платформы
    def __init__(self):
        super().__init__(main_group, all_sprites)
        self.image = platphorm_image
        self.add(main_group)
        self.add(bouncy)  # платформа относится к группе bouncy, и мяч от них отскакивает
        self.rect = self.image.get_rect().move(WIDTH / 2 - 100, (8 * HEIGHT) / 10 - 10)
        # платформа начинает в нижней части экрана, выше ui
        self.vx = 0
        self.mask = pygame.mask.from_surface(self.image)

    def move(self, direction):  # управление, тут все просто
        if direction == 'left':  # влево
            self.vx = -5
        if direction == 'right':  # вправо
            self.vx = 5
        if direction == 'stop':  # и в покое
            self.vx = 0

    def update(self):
        if self.vx > 0 and pygame.sprite.spritecollideany(self, right_borders):
            # если платформа сталкивается с правой стенкой, она не может двигаться вправо
            self.vx = 0
        if self.vx < 0 and pygame.sprite.spritecollideany(self, left_borders):  # если с левой, то влево
            self.vx = 0
        self.rect = self.rect.move(self.vx, 0)


class Border(pygame.sprite.Sprite):  # класс стенок
    def __init__(self, x1, y1, x2, y2):
        super().__init__(all_sprites)
        if x1 == x2:
            self.add(vertical_borders)  # стенки есть вертикальные
            self.image = pygame.Surface([1, y2 - y1])
            self.rect = pygame.Rect(x1, y1, 1, y2 - y1)
            if x1 == 5:
                self.add(left_borders)  # левые
            else:
                self.add(right_borders)  # и правые
        else:
            self.add(horizontal_borders)  # либо горизонтальные
            self.image = pygame.Surface([x2 - x1, 1])
            self.rect = pygame.Rect(x1, y1, x2 - x1, 1)


class Brick(pygame.sprite.Sprite):  # класс кирпичей
    def __init__(self, x, y):
        super().__init__(main_group, all_sprites)
        self.lives = 1  # у обычных (синих) кирпичей всего одна жизнь, они ломаются от одного косания мяча
        self.sprite()
        self.add(bouncy)
        self.add(bricks)  # у кирпичей своя группа
        self.rect = self.image.get_rect().move(x, y)
        self.vx = 0
        self.mask = pygame.mask.from_surface(self.image)

    def sprite(self):  # спрайт кирпича зависит от количества его жизней, но пока, что спрайт только один
        if self.lives > 0:
            pic = load_image('bricks/s_blue.png')
            pic = pygame.transform.scale(pic, (64, 32))  # размер всех кирпичей - 64x32
            self.image = pic

    def update(self):
        global score
        if pygame.sprite.collide_mask(self, mball):  # если кирпич сталкивается с мячом
            print('Brick ' + str(pygame.sprite.collide_mask(self, mball)))
            if pygame.sprite.collide_mask(mball, self)[0] == 0 or pygame.sprite.collide_mask(mball, self)[0] == 0:
                # если мяч прилетел в угол кирпича, он (мяч) начинает лететь в противоположную сторону
                mball.vy = -mball.vy
                mball.vx = -mball.vx
            elif pygame.sprite.collide_mask(mball, self)[0] > pygame.sprite.collide_mask(mball, self)[1]:
                # если в горизонтальную часть кирпича - меняет скорость по y
                mball.vy = -mball.vy
            elif pygame.sprite.collide_mask(mball, self)[1] > pygame.sprite.collide_mask(mball, self)[0]:
                # если в вертикальную - по x
                mball.vx = -mball.vx
            else:
                # если что-то пойдет не так, пусть просо летит в другую сторону
                mball.vy = -mball.vy
                mball.vx = -mball.vx
            self.lives -= 1  # при столкновении с мячом, кирпич теряет жизнь
            score += 100  # игрок получает 100 очков
            self.sprite()  # и кирпич меняет спрайт
        if self.lives <= 0:  # если же жизней не осталось
            mball.count -= 1  # мяч получает один кирпич в свой счет
            score += 100  # игрок получает дополнительно 100 очков
            self.kill()  # кирпич уничтожется
            del self  # и его объект удаляется (все равно, они одноразовые)


class Green(Brick):  # есть кирпич попрочнее
    def __init__(self, x, y):
        super(Brick, self).__init__(main_group, all_sprites)
        self.lives = 2  # у зеленых кирпичей 2 жизни и кроме этого ничем от обычных не отличается
        self.sprite()
        self.add(bouncy)
        self.add(bricks)
        self.rect = self.image.get_rect().move(x, y)
        self.vx = 0
        self.mask = pygame.mask.from_surface(self.image)

    def sprite(self):
        if self.lives == 2:  # в зависимости от количества жизней меняется спрайт
            pic = load_image('bricks/s_green.png')
            pic = pygame.transform.scale(pic, (64, 32))
            self.image = pic
        elif self.lives == 1:  # если в кирпич попали, он трескается
            pic = load_image('bricks/s_green_1.png')
            pic = pygame.transform.scale(pic, (64, 32))
            self.image = pic


class Brown(Brick):  # коричнивые кирпичи
    def __init__(self, x, y):
        super(Brick, self).__init__(main_group, all_sprites)
        self.lives = 3  # имеют 3 жизни
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
            pic = load_image('bricks/s_brown_2.png')  # попав в него два раза он трескается сильнее
            pic = pygame.transform.scale(pic, (64, 32))
            self.image = pic


class Purple(Brick):  # фиолетовые кирпичи - самые прочные
    def __init__(self, x, y):
        super(Brick, self).__init__(main_group, all_sprites)
        self.lives = 4  # и имеют 4 жизни
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


def level(num):  # функция загрузки уровня
    filename = "data/lvl" + str(num) + '.txt'
    # карты всех уровней - файлы txt, в которых указано положение и типов кирпичей
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
        max_width = max(map(len, level_map))
    level = list(map(lambda x: x.ljust(max_width, '.'), level_map))
    c = 0
    for i in range(len(level)):
        for j in range(len(level[i])):
            if level[i][j] == '1':  # цифра означает уровень кирпича - количество его жизней
                Brick(int(j) * 64, int(i) * 32)  # кирпичи располагаются в притык друг другу по сетке 64 на 32 пикселя
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
    mball.count = c  # начальное знаечение count у шарика - количество кирпичей на уровне


class Gui(pygame.sprite.Sprite):  # класс интерфейса
    def __init__(self):
        super().__init__(ui, all_sprites)
        self.x_pos = 40
        self.y_pos = 460
        self.font = pygame.font.Font("assets/font.ttf", 30)
        self.base_color, self.hovering_color = (255, 255, 255), (0, 0, 0)
        self.text_input = str(score)
        self.text = self.font.render(self.text_input, True, self.base_color)
        # в интерфейсе отображается счет игрока - справа
        self.image = self.text
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_rect = self.text.get_rect(center=(40, 460))
        self.lives = str(lives)
        self.lind = self.font.render(self.lives, True, self.base_color)  # и его жизни слева
        self.lind_rect = self.lind.get_rect(center=(600, 460))

    def update(self):
        self.text_input = str(score)
        self.lives = str(lives)
        self.text = self.font.render(self.text_input, True, self.base_color)
        self.lind = self.font.render(self.lives, True, self.base_color)
        self.image = self.text
        screen.blit(self.text, self.text_rect)
        screen.blit(self.lind, self.lind_rect)





all_sprites = pygame.sprite.Group()  # все спрайты
main_group = pygame.sprite.Group()  # главные спрайты - шарик и платформа
horizontal_borders = pygame.sprite.Group()  # стенки
vertical_borders = pygame.sprite.Group()
left_borders = pygame.sprite.Group()
right_borders = pygame.sprite.Group()
bouncy = pygame.sprite.Group()  # материалы от которых отскакивает мячик
bricks = pygame.sprite.Group()  # кирпичи
ui = pygame.sprite.Group()  # и интерфейс
for sprite in main_group:  # в начале новоц игры стираются все оставшиеся от прошлой игры объекты
    sprite.kill()
mball = Ball()  # и создаются заново - мячик
death = Border(5, HEIGHT - 5, WIDTH - 5, HEIGHT - 5)
# нижняя стенка, столкновение мячика с которой ознает проигрыш (потерю жизни)
screen = pygame.display.set_mode((WIDTH, HEIGHT))  # сам экран
lives = 3  # у игрока всегда 3 жизни
Border(5, 5, WIDTH - 5, 5)  # три обычные стенки
Border(5, 5, 5, HEIGHT - 5)
Border(WIDTH - 5, 5, WIDTH - 5, HEIGHT - 5)
plat = Platphorm()  # платформа
score = 0  # счет равен нулю
txt = Gui()  # интерфейс
started = False
# флаг озачающий начало игры, не даёт шарику упасть пока игрок не сделает движение платформой или кликнет мышкой
running = True
lvl = 1  # игрок начинает с первого уровня, всего их 5
level(lvl)  # загшрузка уровня
first = True  # флаг указывает, что это первая игра


def play():  # собственно вся игра
    global score, screen
    global started, lives, running, lvl, mball, plat, first
    first = True
    pygame.init()
    while running:  # в цикле
        clock.tick(FPS)  # лочится фпс
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONUP and started is False:
                # при нажатии мыши мячик начинает падать
                if lives == 3:  # если жизней 3, то игра считается первой
                    first = False  # но уже не считается
                mball.change(0, 5)  # мячик падает вертикально вниз
                started = True  # игра началась
            if event.type == pygame.KEYDOWN:
                if started is False:  # то же самое, если была нажата какая-нибудь клавиша
                    if lives == 3:
                        first = False
                    mball.change(0, 5)
                    started = True
                if event.key == 1073741904:  # движение на стрелочках
                    plat.move('left')  # влево
                if event.key == 1073741903:
                    plat.move('right')  # вправо
                if event.key == pygame.K_m:  # супер секретный чит для перехода на следующий урвень (клавиша m)
                    for sprite in bricks:
                        sprite.kill()
                    lvl = lvl + 1
                    try:
                        level(lvl)
                    except FileNotFoundError:
                        return True
            if event.type == pygame.KEYUP:
                # при зажатии клавиши движения платформа движется, если отпустить, она остановится
                plat.move('stop')
        if mball.count == 0:  # если все кирпичи были разбиты
            mball.pos()  # мячик возвращается в начальную позицию
            mball.change(0, 0)  # останавливается
            started = False  # игра останавливается
            lvl += 1  # и загружается следующий уровень
            try:
                level(lvl)
            except FileNotFoundError:  # если это последний уровень, игра завершается и выврдится экран game over
                return True
        if lives == 0:  # если жизней не осталось
            all_sprites.empty()
            lives = 3  # у игрока снова 3 жизни
            writescore(score)  # его счет записываются в хронику
            score = 0  # счет сбрасывается
            first = True
            return True  # игра завершается, выводится экран game over
        if first:  # если это первая игра
            for sprite in main_group:  # все спрайты удаляются
                sprite.kill()
            for sprite in ui:
                sprite.kill()
            mball = Ball()  # и создаются новые
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
