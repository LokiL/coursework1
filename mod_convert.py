__author__ = 'Кён'



def rgb_to_xyz(color):
    """
    Перевод sRGB-цвета в систему xyz по стандартам CIE

    Входные данные в sRGB-цвете, стандартная освещенность - D65, угол зрения 2 градуса
    Примечание: Входные данные могут быть при любом стандарте RGB, но нужно будет поменять матрицу перевода.
    :color: список в формате [r,g,b], значения в диапазоне от 0 до 255
    :return: [x,y,z] значения цвета в списке
    """
    r,g,b = color[0], color[1], color[2]
    r, g, b = r/255, g/255, b/255 #можно было воспользоваться и лямбда-функцией, но смысла нет

    correcting_func = lambda x: pow(((x+0.055)/1.055), 2.4) #а тут уже есть. lambda-magic!

    if r > 0.04045:
        r = correcting_func(r)
    else:
        r = r/12.92

    if g > 0.04045:
        g = correcting_func(g)
    else:
        g = g/12.92

    if b > 0.04045:
        b = correcting_func(b)

    else:
        b = b/12.92

    r, g, b = r * 100, g * 100, b * 100

    #Матрица перевода
    x = r*0.4124564 + g*0.3575761 + b*0.1804375
    y = r*0.2126729 + g*0.7151522 + b*0.0721750
    z = r*0.0193339 + g*0.1191920 + b*0.9503041

    return [x,y,z]

def xyz_to_lab(color):
    """Перевод xyz-цвета в L*ab-систему по стандартам CIE

    Перевод согласно стандартам CIE, угол зрения 2 градуса, стандартная освещенность D65
    :param color: список вида [x,y,z]
    :return: список вида [L*,a,b]
    """
    x, y, z = color[0], color[1], color[2]

    white_x, white_y, white_z = 95.047, 100.000, 108.883 #Корректировка стандартной освещенности
    x, y, z = x/white_x, y/white_y, z/white_z

    correcting_func = lambda t: (7.787*t) + (16/116) #lambda-magic!

    #серии if-else, чтобы избавиться от сингулярности
    if x > 0.008856:
        x = pow(x, 1/3)
    else:
        x = correcting_func(x)

    if y > 0.008856:
        y = pow(y, 1/3)
    else:
        y = correcting_func(y)

    if z > 0.008856:
        z = pow(z, 1/3)
    else:
        z = correcting_func(z)

    l = (116*y) - 16
    a = 500*(x-y)
    b = 200*(y-z)

    return [l,a,b]

def rgb_to_lab(color):
    """
    Вспомогательная функция, выполняющая перевод RGB-XYZ-L*ab-LCH

    :param color: [r,g,b]-цвет
    :return: [L*,a,b]-цвет
    """
    return xyz_to_lab(rgb_to_xyz(color))