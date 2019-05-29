#Importacion de bibliotecas
from tkinter import*
from threading import Thread
import threading
import os
import time
from tkinter import messagebox

#Biblioteca para el uso del carro


#Ventana principal


def main_about(ventana):
    global root
    root=ventana
    #Configuracion ventana
    root.title('About')
    root.minsize(1000, 800)
    root.resizable(width=NO, height=NO)


    #lienzo
    global Lienzo
    Lienzo=Canvas(root, width=1000, height=800, bg='light blue')
    Lienzo.place(x=-2, y=-2)
    imagen = PhotoImage(file = "f.gif")
    Lienzo.create_image(0,0,anchor=NW,image = imagen)
    imagen2= PhotoImage(file="f2.gif")
    Lienzo.create_image(500,0,anchor=NW,image = imagen2)

    #texto

    Insti = Label(Lienzo,text="Instituto Tecnológico de Costa Rica",font=('Agency FB',25),bg='white',fg='black')
    Autores = Label(Lienzo,text="Programadores:\n\n Juan Pablo Carrillo Salazar/Carnet: 2019380111\n\n Bryan Alfaro González/Carnet: 2019380074\n\n Pablo Rojas Rodríguez/Carnet: 2019173638",font=('Agency FB',18),bg='white',fg='black')
    Carrera = Label(Lienzo,text="Carrera: Ingeniería en Computadores",font=('Agency FB',18),bg='white',fg='black')
    Curso = Label(Lienzo,text="Curso: Taller de Programación" ,font=('Agency FB',18),bg='white',fg='black')
    Grupo = Label(Lienzo,text="Grupo 1",font=('Agency FB',18),bg='white',fg='black')
    Ano = Label(Lienzo,text="Año 2019",font=('Agency FB',18),bg='white',fg='black')
    Profe = Label(Lienzo,text="Profesor: Jeff Schmidt Peralta",font=('Agency FB',18),bg='white',fg='black')
    Pais = Label(Lienzo,text="País de producción: Costa Rica",font=('Agency FB',18),bg='white',fg='black')
    Version = Label(Lienzo,text="Versión del programa 1.0",font=('Agency FB',18),bg='white',fg='black')


    Version.place(x=500-276/2,y=620)
    Autores.place(x=500-529/2,y=100)
    Carrera.place(x=500-405/2,y=320)
    Curso.place(x=500-334/2,y=370)
    Grupo.place(x=500-94/2,y=420)
    Ano.place(x=500-107/2,y=470)
    Profe.place(x=500-327/2,y=520)
    Pais.place(x=500-343/2,y=570)

    Insti.place(x=500-255,y=30)
    root.update()


    boton1= Button(Lienzo, text= "  Volver  ", command=regresar_about, bg='white', fg="black",font=("Arial",14))
    boton1.place(x=460, y=700)
    
    root.protocol("WM_DELETE_WINDOW", _delete_window)
    root.mainloop()
def regresar_about():
    Lienzo.pack_forget()
    root.quit()
    
def _delete_window():
    root.destroy()
