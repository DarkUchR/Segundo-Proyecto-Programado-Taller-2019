#Importacion de bibliotecas
from tkinter import*
from threading import Thread
import threading
import os
import time
from tkinter import messagebox


#E:La ventana de tkinter
#S:-
#R:-
#Cambia a la ventana de about
def main_about(ventana):

    #Se configura la ventana     
    global root
    root=ventana
    root.title('About')
    root.minsize(1000, 800)
    root.resizable(width=NO, height=NO)


    #Se crea y configura el canvas y su fondo
    global canvas_about
    canvas_about=Canvas(root, width=1000, height=800, bg='light blue')
    canvas_about.pack()
    imagen = PhotoImage(file = "Imagenes/f.gif")
    canvas_about.create_image(0,0,anchor=NW,image = imagen)
    imagen2= PhotoImage(file="Imagenes/f2.gif")
    canvas_about.create_image(500,0,anchor=NW,image = imagen2)

    #Se agrega todo el texto necesario
    Insti = Label(canvas_about,text="Instituto Tecnológico de Costa Rica",font=('Agency FB',25),bg='white',fg='black')
    Autores = Label(canvas_about,text="Programadores:\n\n Juan Pablo Carrillo Salazar/Carnet: 2019380111\n\n Bryan Alfaro González/Carnet: 2019380074\n\n Pablo Rojas Rodríguez/Carnet: 2019173638",font=('Agency FB',18),bg='white',fg='black')
    Carrera = Label(canvas_about,text="Carrera: Ingeniería en Computadores",font=('Agency FB',18),bg='white',fg='black')
    Curso = Label(canvas_about,text="Curso: Taller de Programación" ,font=('Agency FB',18),bg='white',fg='black')
    Grupo = Label(canvas_about,text="Grupo 1",font=('Agency FB',18),bg='white',fg='black')
    Ano = Label(canvas_about,text="Año 2019",font=('Agency FB',18),bg='white',fg='black')
    Profe = Label(canvas_about,text="Profesor: Jeff Schmidt Peralta",font=('Agency FB',18),bg='white',fg='black')
    Pais = Label(canvas_about,text="País de producción: Costa Rica",font=('Agency FB',18),bg='white',fg='black')
    Version = Label(canvas_about,text="Versión del programa 1.0",font=('Agency FB',18),bg='white',fg='black')

    #Se centra el texto
    Version.place(x=500-276/2,y=620)
    Autores.place(x=500-529/2,y=100)
    Carrera.place(x=500-405/2,y=320)
    Curso.place(x=500-334/2,y=370)
    Grupo.place(x=500-94/2,y=420)
    Ano.place(x=500-107/2,y=470)
    Profe.place(x=500-327/2,y=520)
    Pais.place(x=500-343/2,y=570)
    Insti.place(x=500-255,y=30)

    #Se crea el boton de volver
    boton1= Button(canvas_about, text= "  Volver  ", command=regresar_about, bg='white', fg="black",font=("Arial",14))
    boton1.place(x=460, y=700)

    #Se reaciona el boton de salir con la funcion de salir
    root.protocol("WM_DELETE_WINDOW", _delete_window)
    root.mainloop()
#E:-
#S:-
#R:-
#Funcion para regresar a la ventana principal
def regresar_about():
    canvas_about.pack_forget()
    root.quit()
#E:-
#S:-
#R:-
#Funcion para salir adecuadamente del programa
def _delete_window():
    root.destroy()
