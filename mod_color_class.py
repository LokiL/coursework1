__author__ = 'Кён'

from mod_convert import rgb_to_lab#Модуль конвертации цвета
from random import normalvariate #Из библиотеки random импортируем функцию нормального распределения
from math import sqrt #Из библиотеки math импортируем функцию извлечения квадратного корня и арктангенса

def rand_number(mu):
    """
    Генерация случайного числа

    Генерация идет по нормальному распределению с заданным математическим ожиданием и жестко заданными
    границами генерации случайного числа в пределах от 0 до 255, так как этого требует задача

    Используемые глобальные переменные: sigma

    :param mu: математическое ожидание случайной величины
    """

    result = -1
    while 0>result or result>255: #если число не входит в границу - пересчитываем, иначе выходим из цикла
        result = normalvariate(mu, sigma)

    return result

def get_three_coord(x,y,z):
    """
    Генерация случайных координат точки

    Используется функция генерации случайного, объявленная в rand_number. Возвращает список из трех координат,
    представляющих собой случайные значения с математическим ожиданием равным численному значению исходной координаты
    и стандартным отклонением sigma

    :param x: математическое ожидание x
    :param y: математическое ожидание y
    :param z: математическое ожидание z

    :return: Список из трех координат, без округления
    """

    coord = []
    coord.append(rand_number(x))
    coord.append(rand_number(y))
    coord.append(rand_number(z))

    return coord

def get_random_coord_list(dot):
    """
    Генерация списка координат

    Каждый элемент списка представляет собой список из трех элементов, сгенерированный функцией get_three_coord.

    Используемые глобальные переменные: number_of_dots_for_standart

    :dot: список из координат исходной точки, dot[0] - x, dot[1] - y, dot[2] - z-координата.
    :return: Список списков координат
    """

    coord_list = []

    for i in range(number_of_dots_for_standart):
        coord_list.append(get_three_coord(dot[0], dot[1], dot[2]))
    return coord_list

def calc_standart_for_dot(dot):
    """
    Считаем эталон для одной точки.

    Подсчет эталона осуществляется путем подсчета среднего арифметического для каждой из координат
    на основе полученного облака точек

    :param dot: список координат исходной точки
    :return: координаты эталона на основе исходной точки
    """

    standart_dot = [0,0,0]

    cloud = get_random_coord_list(dot) #получение облака соседей для заданной
    for i in cloud: #в цикле прибавляем значения координат соседей к соответствующим
        standart_dot[0] += i[0]
        standart_dot[1] += i[1]
        standart_dot[2] += i[2]

    #среднее арифметическое, округляем до 3 знаков после запятой
    standart_dot[0] = round(standart_dot[0] / len(cloud), 3)
    standart_dot[1] = round(standart_dot[1] / len(cloud), 3)
    standart_dot[2] = round(standart_dot[2] / len(cloud), 3)

    return standart_dot

def select_dot_coords_from_color_base(color_base):
    """
    Используется для извлечения координат цветов из базы-словаря

    Используемые глобальные переменные:  list_of_colors

    :color_base: используемая база
    :return: возвращает список координат цветов
    """

    dot_dist_list = []
    for color in list_of_colors:
        dot_dist_list.append(color_base[color])



    return dot_dist_list

def get_standart_color_base():
    """
    Генерация базы эталонов для цветов

    Используемые глобальные переменные: raw_color_base

    :return: словарь с ключами-именами цветов и значениями - координатами эталонов
    """

    #инициализируем словарь с будущими эталонами
    standart_color_base = {'blue': [],
              'green': [],
              'red': [],
              'yellow': [],
              'violet': [],
              'brown': [],
              'black': [],
              'grey': []}


    #Для каждого цвета считаем эталон
    for color in list_of_colors:
        standart_color_base[color] =  calc_standart_for_dot(raw_color_base[color])
    return standart_color_base

def get_dots_distance(fst_dot, sec_dot):
    """
    Получаем расстояние между двумя точками

    Расстояние считается по формуле цветового различия CIE76 для пространства Lab
    :param fst_dot: [r,g,b]-координаты первой точки
    :param sec_dot: [r,g,b]-координаты второй точки
    :return: расстояние, число с плавающей точкой
    """


    fst_dot = rgb_to_lab(fst_dot)
    sec_dot = rgb_to_lab(sec_dot)
    distance = sqrt(pow((float(sec_dot[0]) - float(fst_dot[0])), 2) +
                    pow((float(sec_dot[1]) - float(fst_dot[1])), 2) +
                    pow((float(sec_dot[2]) - float(fst_dot[2])), 2))
    return distance

def classify_color(color):
    """
    Относит заданный цвет в один из восьми классов.

    Используемые глобальные переменные: list_of_colors

    :param color: заданный цвет в виде списка rgb-координат цвета
    :return: возвращает название класса и близость к эталону
    """
    color_class = ''

    if -3 < rgb_to_lab(color)[1] < 3 and -3 < rgb_to_lab(color)[2] < 3 and rgb_to_lab(color)[0] > 10: # проверка на серый цвет
        return 'grey'
    elif rgb_to_lab(color)[0]<10: # проверка на черный
        return 'black'

    else: #цвет не серый, значит продолжаем классификацию
        distance_base = []
        #Считаем расстояния до каждого эталона и заносим в словарь {название:расстояние}
        for i in range(len(standart_coord_list)):
            distance_base.append([list_of_colors[i], get_dots_distance(standart_coord_list[i], color)])

        list_of_distances = []
        #Выделяем расстояния в отдельный список
        for i in range(len(distance_base)):
            list_of_distances.append(distance_base[i][1])

        #Проводим поиск искомого минимального расстояния в словаре расстояний,
        #используя в качестве итератора индекс словаря, при совпадении выводим индекс в
        #отдельную переменную как название класса
        for i in range(len(distance_base)):
            if distance_base[i][1] == min(list_of_distances):
                color_class = distance_base[i][0]

        return color_class

number_of_dots_for_standart = 64 #Количество точек для генерации эталона
sigma = 4 #Задаем среднеквадратичное отклонение

#Хардкодим основные цвета, на основе которых будут создаваться эталоны.
#Формат записи - словарь с названием цвета-ключом и координатами [x,y,z] - значением
raw_color_base = {'blue': [0, 0, 255],
              'green': [0, 255, 0],
              'red': [255, 0, 0],
              'yellow': [255, 255, 0],
              'violet': [139, 0, 255],
              'brown': [150, 75, 0],
#              'black': [0, 0, 0], #оставлены для порядка, считаются отдельно
#              'grey': [128, 128, 128]
}

#Извлекаем список индексов цветов, так как словарь - неупорядоченная структура и невозможно использование
#ключей как итераторов, что понадобится в дальнейшем.
#Каждый раз при вызове функции порядок значений в списке изменяется, но сами значения неизменны.
get_list_of_keys = lambda color_base: list(color_base.keys()) #лямбда-функция не особо нужна, но пусть будет

list_of_colors = get_list_of_keys(raw_color_base)

standart_color_base = get_standart_color_base() #Создаем словарь эталонов цветов

standart_coord_list = select_dot_coords_from_color_base(standart_color_base) #Создаем список из координат эталонов