import os
import sys
import pygame
import datetime


def load_image(name, colorkey=None):  # функция загрузки изображения спрайта
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image

def terminate(): # функция аварийного завершения
    pygame.quit()
    sys.exit()

def writescore(n):  # функция записи счета для таблицы рекордов
    f = open('data/levels/score.txt', 'a')  # в файле score.txt записаны все итоги игры
    print(str(datetime.datetime.now().date()))  # дата игры
    f.write('\n' + str(datetime.datetime.now().date()) + ': ' + str(n))  # и финальный счет