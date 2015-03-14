__author__ = 'Арслан Мусин, МГППУ ИТ 4.2'

from mod_color_class import classify_color #Модуль подсчета стандарта
from PIL import Image

def analysis(incoming_image):
    """
    Анализ загруженного изображения.

    :param incoming_image: имя изображения для анализа
    :return: массив из количества пикселей, соответствующих группам цветов
    """
    blue = 0
    green = 0
    red = 0
    yellow = 0
    violet = 0
    brown = 0
    black = 0
    grey = 0

    im = Image.open(incoming_image)
    img = im.load()
    weight, height = im.size[0],im.size[1]
    for i in range(weight):
        print('Обработано: ', i/weight*100, "процентов")
        for k in range(height):
            if classify_color(img[i,k]) == 'blue': #проверяем принадлежность цвета пикселя (i,k) к классу
                blue += 1

            elif classify_color(img[i,k]) == 'green':
                green += 1

            elif classify_color(img[i,k]) == 'red':
                red += 1

            elif classify_color(img[i,k]) == 'yellow':
                yellow += 1

            elif classify_color(img[i,k]) == 'violet':
                violet += 1

            elif classify_color(img[i,k]) == 'brown':
                brown += 1

            elif classify_color(img[i,k]) == 'black':
                black += 1

            elif classify_color(img[i,k]) == 'grey':
                grey += 1

    normalize = lambda x: x/(weight*height)*100 #нормализация вывода

    blue = 'Синие: ' + str(normalize(blue))
    green = '\nЗеленые: ' + str(normalize(green))
    red = '\nКрасные: ' + str(normalize(red))
    yellow = '\nЖелтые: ' + str(normalize(yellow))
    violet = '\nФиолетовые: ' + str(normalize(violet))
    brown = '\nКоричневые: ' + str(normalize(brown))
    black = '\nЧерные: ' + str(normalize(black))
    grey = '\nСерые: ' + str(normalize(grey)) + "\n"
    outputstring = 'Процентное содержание тонов в изображении:\n' + blue + green + red + \
                   yellow + violet + brown + black + grey

    return outputstring




