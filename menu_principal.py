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
from tkinter.filedialog import askopenfilename
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

escuderia_file= open("Escuderia.txt","r")
escuderia=escuderia_file.readlines()
escuderia_file.close
#Imagenes en pantalla de inicio
fondo = PhotoImage(file = "Imagenes/fondo1.gif")
#recorte_2 = fondo.subsample(x=2, y=2)
canvas.create_image(0,0, anchor= NW, image= fondo)
logo_esc = PhotoImage(file= escuderia[0][:-1])
logo_canvas=canvas.create_image(10,450, anchor= NW, image= logo_esc)
pat1 = PhotoImage(file = escuderia[1][:-1])
pat1_canvas=canvas.create_image(350, 20, anchor= NW, image= pat1)
pat2 = PhotoImage(file = escuderia[2][:-1])
pat2_canvas=canvas.create_image(350, 20+pat1.height(), anchor= NW, image= pat2)

def leave():
    global animation_Flag
    animation_Flag=False
    canvas.pack_forget()
    principal.quit()
    
def return_principal():
    try:
        principal.title("Inicio")
        principal.minsize(1000,700)
        principal.resizable(width=NO,height=NO)
        canvas.pack()
        escuderia_file= open("Escuderia.txt","r")
        escuderia=escuderia_file.readlines()
        escuderia_file.close
        PA = escuderia[3][:-1]+"\n" +escuderia[4][:-1]
        AH0 = escuderia[5][:-1]
        AH=""
        for modelo in AH0.split("/"):
            AH+=modelo+"\n";
        PD = escuderia[8][:-1]+"\n" +escuderia[9][:-1]
        IGE = str(int(escuderia[6][:-1])*100//int(escuderia[7][:-1]))
        VD= escuderia[10][:-1]+"\n" +escuderia[11][:-1]
        canvas.itemconfig(pa_canvas,text =PA)
        canvas.itemconfig(ah_canvas,text=AH)
        canvas.itemconfig(vd_canvas,text= VD)
        canvas.itemconfig(indices3,text= IGE)
        canvas.itemconfig(pd_canvas, text =PD)
        
       

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

def cambiar_pat1():
    archivo=cambiar_img(1)
    if archivo!="Error":
        global pat1
        pat1 = PhotoImage(file= archivo)
        canvas.itemconfig(pat1_canvas,image=pat1)
        update()
def cambiar_pat2():
    archivo=cambiar_img(2)
    if archivo!="Error":
        global pat2
        pat2 = PhotoImage(file= archivo)
        canvas.itemconfig(pat2_canvas,image=pat2)
        update()

def update():
    canvas.coords(pat2_canvas,350,20+pat1.height())
    canvas.coords(indices1,350,20+pat1.height()+pat2.height())
    canvas.coords(indices2,350,20+pat1.height()+pat2.height()+20)
    canvas.coords(indices3,350,20+pat1.height()+pat2.height()+40)
def cambiar_logo():
    archivo=cambiar_img(0)
    if archivo!="Error":
        global logo_esc
        logo_esc = PhotoImage(file= archivo)
        canvas.itemconfig(logo_canvas,image=logo_esc)

def cambiar_img(valor):
    filename = askopenfilename()
    if filename[-3:]!="gif" and filename[-3:]!="png":
        messagebox.showinfo("Error","La entrada debe ser una imagen en formato gif o png")
        return "Error"
    else:
        img = PhotoImage(file= filename)
        if img.width()>300 or img.height()>300:
            messagebox.showinfo("Error","La imagen es muy grande")
            return "Error"
        else:
            escuderia_file= open("Escuderia.txt","r")
            escuderia=escuderia_file.readlines()
            escuderia[valor]=filename+"\n"
            escuderia_file.close()
            escuderia_file= open("Escuderia.txt","w")
            escuderia_file.writelines(escuderia)
            escuderia_file.close()
            return filename    

#Botones que direccionan a las demas pantallas
about = Button(canvas, font=("Arial", 12), text="About", width=8, bg="grey", fg="Black", command=cambiar_about)#, command=)
about.place(x=650, y=625)
posiciones = Button(canvas, font=("Arial", 12), text="Seleccionar Piloto", bg="grey", fg="Black", command=cambiar_pilotos)#, command=)
posiciones.place(x=300, y=625)

pat1_change = Button(canvas, font=("Arial", 10), text="Cambiar Patrocinador 1", bg="#a3a3a3", fg="Black", command=cambiar_pat1)#, command=)
pat1_change.place(x=10, y=632)
pat2_change = Button(canvas, font=("Arial", 10), text="Cambiar Patrocinador 2", bg="#a3a3a3", fg="Black", command=cambiar_pat2)#, command=)
pat2_change.place(x=10, y=664)
logo = Button(canvas, font=("Arial", 10), text="Cambiar Logo",  bg="#a3a3a3", fg="Black", command=cambiar_logo)#, command=)
logo.place(x=10, y=600)


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
indices1=canvas.create_text(350, 20+pat1.height()+pat2.height(),text="Índices de escudería: ", font=("Montserrat-Regular",14), fill= "White", anchor=NW)
canvas.create_text(735, 50,text="Historico de automóviles: ", font=("Montserrat-Regular",14),fill= "White", anchor=NW)
indices2=canvas.create_text(350, 20+pat1.height()+pat2.height()+20,text="Índice Ganador de Escudería: ", font=("Montserrat-Regular",14), fill= "White", anchor=NW)
canvas.create_text(735, 225,text="Vehículos Disponibles: ", font=("Montserrat-Regular",14), fill= "White", anchor=NW)
img = canvas.create_image(0, 0, image= reduc, anchor= NW)

#Crear líneas
canvas.create_line(345, 45, 345, 600, fill="#000000", dash=(7, 4))
canvas.create_line(650, 45, 650, 600, fill="#000000", dash=(7, 4))

#Creación de archivo de texto para trabajar los datos configurables

PA = escuderia[3][:-1]+"\n" +escuderia[4][:-1]
AH0 = escuderia[5][:-1]
AH=""
for modelo in AH0.split("/"):
    AH+=modelo+"\n";
PD = escuderia[8][:-1]+"\n" +escuderia[9][:-1]
AC = "2019"
IGE = str(int(escuderia[6][:-1])*100//int(escuderia[7][:-1]))
VD= escuderia[10][:-1]+"\n" +escuderia[11][:-1]
indices3=canvas.create_text(350, 20+pat1.height()+pat2.height()+40,text= str(IGE), font=("Montserrat-Regular",14), fill= "Dark Blue", anchor=NW)
canvas.create_text(940, 11, text = str(AC), font=("Montserrat-Regular",14),fill= "Light Green", anchor=NW)
pd_canvas=canvas.create_text(12, 380, text = str(PD), font=("Montserrat-Regular",14),fill= "Dark Blue", anchor=NW)
ah_canvas=canvas.create_text(735, 75, text = str(AH), font=("Montserrat-Regular",14),fill= "Dark Blue", anchor=NW)
pa_canvas=canvas.create_text(10, 200, text = str(PA), font=("Montserrat-Regular",14),fill= "Dark Blue", anchor=NW)
vd_canvas=canvas.create_text(735, 245, text = str(VD), font=("Montserrat-Regular",14),fill= "Dark Blue", anchor=NW)


#Funciones
def musica():
    winsound.PlaySound("8bits.wav", winsound.SND_FILENAME | winsound.SND_ASYNC | winsound.SND_LOOP)

animation_Flag=True
def logo_f1():
    x= 0
    y= 0
    mov_x = 5
    while animation_Flag:
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
