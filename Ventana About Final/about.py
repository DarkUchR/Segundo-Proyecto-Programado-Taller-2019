#Importacion de bibliotecas
from tkinter import*
from threading import Thread
import threading
import os
import time
from tkinter import messagebox
import tkinter.scrolledtext as tkscrolled

#Biblioteca para el uso del carro


#Ventana principal
root=Tk()

def regresar():
    root.withdraw()

#Configuracion ventana
root.title('About Window')
root.minsize(1000, 800)
root.resizable(width=NO, height=NO)


#lienzo
Lienzo=Canvas(root, width=1000, height=800, bg='light blue')
Lienzo.place(x=-2, y=-2)
imagen = PhotoImage(file = "f.gif")
Lienzo.create_image(0,0,anchor=NW,image = imagen)
imagen2= PhotoImage(file="f2.gif")
Lienzo.create_image(500,0,anchor=NW,image = imagen2)

#texto

Insti = Label(Lienzo,text="Instituto Tecnológico de Costa Rica",font=('Agency FB',25),bg='white',fg='black')
Insti.place(x=325,y=30)
Autores = Label(Lienzo,text="Programadores:\n\n Juan Pablo Carrillo Salazar/Carnet: 2019380111\n\n Bryan Alfaro González/Carnet:2019380074\n\n Pablo Rojas Rodríguez/Carnet: 2019173638",font=('Agency FB',18),bg='white',fg='black')
Autores.place(x=320,y=100)
Carrera = Label(Lienzo,text="Carrera: Ingeniería en Computadores",font=('Agency FB',18),bg='white',fg='black')
Carrera.place(x=358,y=320)
Curso = Label(Lienzo,text="Curso: Taller de Programación" ,font=('Agency FB',18),bg='white',fg='black')
Curso.place(x=385,y=370)
Grupo = Label(Lienzo,text="Grupo 1",font=('Agency FB',18),bg='white',fg='black')
Grupo.place(x=466,y=420)
Año = Label(Lienzo,text="Año 2019",font=('Agency FB',18),bg='white',fg='black')
Año.place(x=458,y=470)
Profe = Label(Lienzo,text="Profesor: Jeff Schmidt Peralta",font=('Agency FB',18),bg='white',fg='black')
Profe.place(x=390,y=520)
Pais = Label(Lienzo,text="País de producción: Costa Rica",font=('Agency FB',18),bg='white',fg='black')
Pais.place(x=386,y=570)
Version = Label(Lienzo,text="Versión del programa 1.0",font=('Agency FB',18),bg='white',fg='black')
Version.place(x=408,y=620)

boton1= Button(Lienzo, text= "  ↶  ", command=regresar, bg='white', fg="black")
boton1.place(x=0, y=0)



root.mainloop()
