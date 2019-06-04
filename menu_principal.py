"""
Instituto Tecnológico de Costa Rica
Tercer proyecto programado
"""
from tkinter import*
from tkinter import messagebox
from threading import Thread
import winsound
import threading
import time
from about import main_about
from menu_pilotos import main_menu_pilotos

# Importaciones de librerias

principal = Tk()  #Asignacion de pantalla principal

    
#Ventana principal
principal.title("Inicio")
principal.minsize(1000,700)
principal.resizable(width=NO,height=NO)


#Crear Canvas
canvas = Canvas(principal, width=1200, height=900, bg="White")
canvas.place(x=0, y=0)    #Colocar canvas


#Imagenes en pantalla de inicio
fondo = PhotoImage(file = "fondo1.gif")
#recorte_2 = fondo.subsample(x=2, y=2)
canvas.create_image(0,0, anchor= NW, image= fondo)
logo_esc = PhotoImage(file= "BMW.png")
recorte = logo_esc.subsample(x=2, y=2)
canvas.create_image(10,450, anchor= NW, image= recorte)
pat1 = PhotoImage(file = "michelin.png")
rec1 = pat1.subsample(x=3, y=3)
canvas.create_image(350, 20, anchor= NW, image= rec1)
pat2 = PhotoImage(file = "pirelli.gif")
canvas.create_image(350, 145, anchor= NW, image= pat2)


def leave():
    global animation_Flag
    animation_Flag=False
    principal.quit()
    
def return_principal():
    try:
        principal.title("Inicio")
        principal.minsize(1000,700)
        principal.resizable(width=NO,height=NO)    
        principal.protocol("WM_DELETE_WINDOW", _delete_window)
        principal.mainloop()
    except:
        winsound.PlaySound(None, winsound.SND_FILENAME)
        
def cambiar_pilotos():
    leave()
    main_menu_pilotos(principal)
    return_principal()

    

def cambiar_about():
    leave()
    main_about(principal)
    return_principal()
 

#Botones que direccionan a las demas pantallas
about = Button(canvas, font=("Arial", 12), text="About", width=8, bg="grey", fg="Black", command=cambiar_about)#, command=)
about.place(x=650, y=625)
posiciones = Button(canvas, font=("Arial", 12), text="Seleccionar Piloto", bg="grey", fg="Black", command=cambiar_pilotos)#, command=)
posiciones.place(x=300, y=625)



logo_prin = PhotoImage(file= "formula1.png")
reduc = logo_prin.subsample(x=4, y=4)

#Textos en la pantalla de inicio
canvas.create_text(10, 110,text="Escudería", font=("Montserrat-Regular",20), fill= "White", anchor=NW)
canvas.create_text(750, 10,text="Temporada actual: ", font=("Montserrat-Regular", 15), fill= "Light Green", anchor=NW)
canvas.create_text(10, 145,text="Escudería BMW", font=("Montserrat-Regular",14),fill= "White", anchor=NW)
canvas.create_text(12, 175,text="Pilotos Asociados: ", font=("Montserrat-Regular",14),fill= "White", anchor=NW)
canvas.create_text(10, 275,text="Ubicación Geográfica: \nHinwil-Suiza \nMúnich-Alemania", font=("Montserrat-Regular",14),fill= "White", anchor=NW)
canvas.create_text(12, 355,text="Pilotos Disponibles: ", font=("Montserrat-Regular",14),fill= "White", anchor=NW)
canvas.create_text(355, 0,text="Patrocinadores: ", font=("Montserrat-Regular",14),fill= "White", anchor=NW)
canvas.create_text(350, 225,text="Índices de escudería: ", font=("Montserrat-Regular",14), fill= "White", anchor=NW)
canvas.create_text(735, 50,text="Historico de atomóviles: ", font=("Montserrat-Regular",14),fill= "White", anchor=NW)
canvas.create_text(350, 245,text="Índice Ganador de Escudería: ", font=("Montserrat-Regular",14), fill= "White", anchor=NW)
canvas.create_text(735, 225,text="Vehículos Disponibles: ", font=("Montserrat-Regular",14), fill= "White", anchor=NW)
img = canvas.create_image(0, 0, image= reduc, anchor= NW)

#Crear líneas
canvas.create_line(345, 45, 345, 600, fill="#000000", dash=(7, 4))
canvas.create_line(650, 45, 650, 600, fill="#000000", dash=(7, 4))

#Creación de archivo de texto para trabajar los datos configurables
PA = "Franklin Wart \nJhon Sans"
AH = "BT49 \nBT50 \nBMW-269 \nBMW316i"
PD = "Franklin Wart"
AC = "2019"
IGE = "0,89"
archivo = open("configurables.txt","w")
archivo.write(PA)
archivo.write(AH)
archivo.write(PD)
archivo.write(AC)
archivo.write(IGE)
canvas.create_text(350, 265,text= str(IGE), font=("Montserrat-Regular",14), fill= "Dark Blue", anchor=NW)
canvas.create_text(940, 11, text = str(AC), font=("Montserrat-Regular",14),fill= "Light Green", anchor=NW)
canvas.create_text(12, 380, text = str(PD), font=("Montserrat-Regular",14),fill= "Dark Blue", anchor=NW)
canvas.create_text(725, 125, text = str(AH), font=("Montserrat-Regular",14),fill= "Dark Blue", anchor=NW)
canvas.create_text(10, 200, text = str(PA), font=("Montserrat-Regular",14),fill= "Dark Blue", anchor=NW)
archivo.close()


#Funciones
def musica():
    winsound.PlaySound("8bits.wav", winsound.SND_FILENAME | winsound.SND_ASYNC | winsound.SND_LOOP)

animation_Flag=True
def logo_f1():
    x= 0
    y= 0
    mov_x = 5
    while animation_Flag and x>=0:
        x += mov_x
        try:
            canvas.move(img,mov_x,y)
        except:
            pass
        if x>235 or x<0:
            mov_x*=-1                
        time.sleep(0.033)
    try:
        canvas.coords(img, (0,0))
    except:
        pass
    
def inicio():
    global animation_Flag
    animation_Flag=True
    canvas.coords(img, (0,0))
    thread1 = Thread(target=logo_f1, args=())
    thread1.start()
    

def _delete_window():
    global animation_Flag
    animation_Flag=False
    winsound.PlaySound(None, winsound.SND_FILENAME)
    time.sleep(0.5)
    principal.destroy()
         
musica()
inicio()
principal.protocol("WM_DELETE_WINDOW", _delete_window)

principal.mainloop()
