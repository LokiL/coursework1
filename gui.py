__author__ = 'Кён'

from coloranalysis import analysis
from tkinter import *
from tkinter.filedialog import askopenfile
from tkinter.ttk import *



def startanalysis(event):
    """
    Эвент, запускающий диалог открытия файла и анализ

    :return:
    """
    fn = askopenfile()
    if fn == '':
        return
    else:
        result = analysis(fn.name)
        txt.insert('1.0', result)
    return None


root = Tk() #инициализация gui


#Настраиваем внешний вид
root.geometry("300x200+40+80") #размер и позиция на экране
root.title("Колориметрический анализ изображения") #заголовок
root.resizable(0,0) #блокируем изменение размера

btn = Button(text="Обработать изображение")
lbl = Label(text = "Внимание, чем больше изображение, \nтем дольше времени займет обработка")
btn.bind("<Button-1>", startanalysis)

txt = Text(root,height=9,width=41,font='Arial 9')

btn.pack(side="top")
lbl.pack(side="top")
txt.pack(side="bottom")

root.mainloop() #запуск Gui