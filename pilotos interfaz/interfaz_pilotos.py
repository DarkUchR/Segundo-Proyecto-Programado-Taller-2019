from tkinter import *
from threading import Thread
import threading 
import os
import time
from tkinter import messagebox

#Se crea la ventana y se configura
ventana1 = Tk()
ventana1.title("Brayan Alfaro");
ventana1.minsize(1000,800)
ventana1.maxsize(1000,800)
ventana1.resizable(width=NO,height=NO)
scrollbar=Scrollbar(ventana1)
scrollbar.pack( side = RIGHT, fill=Y )

#Se crea el canvas y se configura
canvas_ventana1 = Canvas(ventana1,width= 1000,height = 800, bg = "white",scrollregion=(0, 0, 1000, 1800) , yscrollcommand = scrollbar.set)
canvas_ventana1.place(x=0, y=0)
canvas_ventana1.pack()


def cargar_imagen(nombre):
    direccion= os.path.join('Imagenes',nombre)
    imagen= PhotoImage(file=direccion)
    return imagen

def calcular_estadisticas(piloto):
    victorias=int(piloto[6])
    cuasivictorias=int(piloto[7])
    abandonos=int(piloto[8])
    competencias=int(piloto[5])
    if competencias-abandonos!=0:
        rgp= str((victorias+cuasivictorias)*100//(competencias-abandonos))+" "
        rep= str((victorias)*100//(competencias-abandonos))+ " "
    else:
        rgp= "0 "
        rep= "0 "
    return [rgp,rep]

pilotos_archivo= open("Pilotos.txt","r")
info_pilotos=pilotos_archivo.readlines()

pilotos=[]
for i in range(len(info_pilotos)//9):

    piloto_simple= info_pilotos[9*i:9*(i+1)]
    piloto_simple+=calcular_estadisticas(piloto_simple)
    pilotos.append(piloto_simple)

bar= cargar_imagen("bar.png")
titulos= Label(canvas_ventana1,font=("Arial",13),bg="#0059A6",fg ="white",borderwidth=2, relief="groove", text="               Piloto                                 Edad      Nacionalidad               Carro                 Competencias           RGP          REP                ")
titulos.place(x=1,y=1)
rectangulos=[]
paises=[]    
caras=[]
carros=[]
indice= cargar_imagen("position.png")
for i in range(len(pilotos)):

    piloto=pilotos[i]

    rectangulos.append(canvas_ventana1.create_rectangle(1, 40+78*i, 920, 32+78*(i+1), fill='white',outline="white"))
    canvas_ventana1.tag_lower(rectangulos[-1])
    
    imagen_indice=canvas_ventana1.create_image(1,40+78*i,image = indice ,anchor = NW)
    
    carros= [cargar_imagen(piloto[4][:-1]+".png")]+carros
    imagen_carro=canvas_ventana1.create_image(480,55+78*i,image = carros[0] ,anchor = NW)
    caras= [cargar_imagen(piloto[1][:-1]+".png")]+caras
    imagen_cara = canvas_ventana1.create_image(70,40+78*i,image = caras[0] ,anchor = NW)
    paises= [cargar_imagen(piloto[3][:-1]+".png")]+paises
    imagen_pais = canvas_ventana1.create_image(370,55+78*i,image = paises[0] ,anchor = NW)
    imagen_bar = canvas_ventana1.create_image(30,110+78*i,image = bar ,anchor = NW)
    
    imagen_edad= canvas_ventana1.create_text((295,65+78*i),font=("Arial",15), text=piloto[2],anchor = NW)
    imagen_nombre= canvas_ventana1.create_text((150,65+78*i),font=("Arial",15),text=piloto[0],anchor = NW)
    imagen_competencias= canvas_ventana1.create_text((680,65+78*i),font=("Arial",15), text=piloto[5],anchor = NW)
    imagen_rgp= canvas_ventana1.create_text((805,65+78*i),font=("Arial",15),text=piloto[9],anchor = NW)
    imagen_rep= canvas_ventana1.create_text((890,65+78*i),font=("Arial",15), text=piloto[10],anchor = NW)

    piloto+=[imagen_carro,imagen_cara,imagen_pais,imagen_edad, imagen_nombre, imagen_competencias,imagen_rgp, imagen_rep]

def actualizar():
    global paises
    paises=[]
    for i in range(len(pilotos)):
        canvas_ventana1.coords(pilotos[i][11],480,55+78*i)
        canvas_ventana1.coords(pilotos[i][12],70,40+78*i)
        canvas_ventana1.coords(pilotos[i][13],370,55+78*i)
        paises= [cargar_imagen(pilotos[i][3][:-1]+".png")]+paises
        canvas_ventana1.itemconfig(pilotos[i][13],image=paises[0])
        canvas_ventana1.coords(pilotos[i][14],295,65+78*i)
        canvas_ventana1.itemconfig(pilotos[i][14],text=pilotos[i][2])
        canvas_ventana1.coords(pilotos[i][15],150,65+78*i)
        canvas_ventana1.itemconfig(pilotos[i][15],text=pilotos[i][0])
        canvas_ventana1.coords(pilotos[i][16],680,65+78*i)
        canvas_ventana1.itemconfig(pilotos[i][16],text=pilotos[i][5])
        canvas_ventana1.coords(pilotos[i][17],805,65+78*i)
        canvas_ventana1.itemconfig(pilotos[i][17],text=pilotos[i][9])
        canvas_ventana1.coords(pilotos[i][18],890,65+78*i)
        canvas_ventana1.itemconfig(pilotos[i][18],text=pilotos[i][10])
        
    if pilot_selected:
        deshabilitar_eleccion(pilot_waiting)
        



def ordenar_pilotos(valor):
    if valor== "rpg":
        n=9
    elif valor== "rep":
        n=10
    
    for i in range(len(pilotos)):
        for j in range(len(pilotos)-i-1):
            if int(pilotos[j][n][:-1])<int(pilotos[j+1][n][:-1]):
                temp=pilotos[j]
                pilotos[j]=pilotos[j+1]
                pilotos[j+1]=temp
    
def ordenar_inverso_pilotos(valor):
    if valor== "rpg":
        n=9
    elif valor== "rep":
        n=10

    for i in range(len(pilotos)):
        for j in range(len(pilotos)-i-1):            
            if int(pilotos[j][n][:-1])>int(pilotos[j+1][n][:-1]):
                temp=pilotos[j]
                pilotos[j]=pilotos[j+1]
                pilotos[j+1]=temp

    
orden_rpg=1
orden_rep=1
def ordenar_rpg():
    global orden_rpg
    if orden_rpg==1:
        ordenar_pilotos("rpg")
    else:
        ordenar_inverso_pilotos("rpg")
    orden_rpg*=-1        
        
    actualizar()

def ordenar_rep():
    global orden_rep
    if orden_rep==1:
        ordenar_pilotos("rep")
    else:
        ordenar_inverso_pilotos("rep")
    orden_rep*=-1

    actualizar()


def edit():
    global pilotos
    global pilot_waiting
    global animationFlag
    canvas_ventana1.pack_forget()
    animationFlag=False
    editar_piloto_ventana(pilotos[pilot_waiting],pilot_waiting)
    deshabilitar_eleccion(pilot_waiting)

    
pilot_waiting=-1
pilot_selected=False
def leftclick(event):
    x = canvas_ventana1.winfo_pointerx() - canvas_ventana1.winfo_rootx()
    y = canvas_ventana1.winfo_pointery() - canvas_ventana1.winfo_rooty()+scrollbar.get()[0]*(1800) 
    if  1<x<920:
        for i in range(22):
            if 40+78*i<y<32+78*(i+1):
                if canvas_ventana1.itemcget(rectangulos[i], "fill")=="#b5b5bc":
                    deshabilitar_eleccion(i)
                else:
                    deshabilitar_eleccion(pilot_waiting)
                    habilitar_eleccion(i)
            
                    
def habilitar_eleccion(indice_rectangulo):
    global pilot_selected
    global pilot_waiting
    canvas_ventana1.itemconfig(rectangulos[indice_rectangulo], fill="#b5b5bc")
    run_button.config(state="normal")
    edit_button.config(state="normal")
    pilot_selected=True
    pilot_waiting=indice_rectangulo                   

def deshabilitar_eleccion(indice_rectangulo):
    global pilot_selected
    global pilot_waiting
    canvas_ventana1.itemconfig(rectangulos[indice_rectangulo], fill="white")
    run_button.config(state="disabled")
    edit_button.config(state="disabled")
    pilot_waiting=-1
    pilot_selected=False

def colorear():
    global animationFlag
    global pilot_waiting
    anterior=0
    animationFlag=True
    while animationFlag==True:
        x = canvas_ventana1.winfo_pointerx() - canvas_ventana1.winfo_rootx()
        y = canvas_ventana1.winfo_pointery() - canvas_ventana1.winfo_rooty()+scrollbar.get()[0]*(1800) 
        for i in range(22):
            if 1<x<920 and 40+78*i<y<32+78*(i+1) and (anterior==-1 or anterior!=i) :
                if  not pilot_waiting==i:
                    canvas_ventana1.itemconfig(rectangulos[i], fill="#dbdde0")
                    if pilot_waiting!=anterior:
                        canvas_ventana1.itemconfig(rectangulos[anterior], fill="white")
                    anterior=i
                else:
                    canvas_ventana1.itemconfig(rectangulos[anterior], fill="white")
                    anterior=-1
            elif not (1<x<920) and anterior!=-1 and anterior!=pilot_waiting:
                canvas_ventana1.itemconfig(rectangulos[anterior], fill="white")
                anterior=-1
def colorear():
    global animationFlag
    global pilot_waiting
    animationFlag=True
    while animationFlag:
        time.sleep(0.03)
        x = canvas_ventana1.winfo_pointerx() - canvas_ventana1.winfo_rootx()
        y = canvas_ventana1.winfo_pointery() - canvas_ventana1.winfo_rooty()+scrollbar.get()[0]*(1800) 
        for i in range(22):
            if 1<x<920 and 40+78*i<y<32+78*(i+1):
                if i!=pilot_waiting:
                    canvas_ventana1.itemconfig(rectangulos[i], fill="#dbdde0")
                while 1<x<920 and 40+78*i<y<32+78*(i+1) and animationFlag:
                    x = canvas_ventana1.winfo_pointerx() - canvas_ventana1.winfo_rootx()
                    y = canvas_ventana1.winfo_pointery() - canvas_ventana1.winfo_rooty()+scrollbar.get()[0]*(1800) 
                    time.sleep(0.03)
                if i!=pilot_waiting:
                    canvas_ventana1.itemconfig(rectangulos[i], fill="white")
        
        
#Se establecen los botones

edit_button = Button(canvas_ventana1, text="Edit", font= ("Arial",13) , command=edit, state="disabled")
edit_button.place(x=930,y=30)
run_button = Button(canvas_ventana1, text="Run", font= ("Arial",13) , command=edit,state="disabled")
run_button.place(x=930,y=70)

imagen=cargar_imagen("button.png")
scrollbar.config( command = canvas_ventana1.yview )
rpg_button = Button(canvas_ventana1, image=imagen , command=ordenar_rpg)
rep_button = Button(canvas_ventana1, image=imagen , command=ordenar_rep)


rpg_button.place(x=848,y=8)
rep_button.place(x=933,y=8)

ventana1.bind("<Button-1>", leftclick)
thread1= Thread(target=colorear,args=())
thread1.start()
logo= cargar_imagen("logo.png")


def editar_piloto_ventana(piloto,piloto_ind):
    canvas2_ventana1 = Canvas(ventana1,width= 1000,height = 800, bg = "white")
    canvas2_ventana1.place(x=0, y=0)
    canvas2_ventana1.pack()
    global cara
    cara= cargar_imagen(piloto[1][:-1]+".png")
    imagen_logo = canvas2_ventana1.create_image(0,0,image = logo ,anchor = NW)


    posy=200
    deltay=50
    posx=250
    deltax=200
    rectangulo_cara=canvas2_ventana1.create_rectangle(posx+3*deltax/2+20, posy-2*deltay, posx+3*deltax/2+90,posy-2*deltay+70, fill='gray',outline="white")
    imagen_cara = canvas2_ventana1.create_image(posx+3*deltax/2+20,posy-2*deltay,image = cara ,anchor = NW)

    entry_nombre= Entry(canvas2_ventana1,font=("Arial",15),width=30,bg="White",fg="#515151")
    entry_nombre.place(x=posx+deltax,y=posy)
    entry_nombre.insert(0, piloto[0][:-1])

    label_nombre= Label(canvas2_ventana1,font=("Arial",15), text=" Nombre: ",bg="#0059A6", height=1,fg="White",borderwidth=2, relief="groove",width=15)
    label_nombre.place(x=posx,y=posy)


    entry_edad=Entry(canvas2_ventana1,font=("Arial",15),width=30,bg="White",fg="#515151")
    entry_edad.place(x=posx+deltax,y=posy+deltay)
    entry_edad.insert(0, piloto[2][:-1])
    label_edad= Label(canvas2_ventana1,font=("Arial",15), text=" Edad: ",bg="#0059A6", height=1,fg="White",borderwidth=2, relief="groove",width=15)
    label_edad.place(x=posx,y=posy+deltay)


    entry_nacionalidad=Entry(canvas2_ventana1,font=("Arial",15),width=30,bg="White",fg="#515151")
    entry_nacionalidad.place(x=posx+deltax,y=posy+2*deltay)
    entry_nacionalidad.insert(0, piloto[3][:-1])
    label_nacionalidad= Label(canvas2_ventana1,font=("Arial",15), text=" Nacionalidad: ",bg="#0059A6", height=1,fg="White",borderwidth=2, relief="groove",width=15)
    label_nacionalidad.place(x=posx,y=posy+2*deltay)


    entry_competencias=Entry(canvas2_ventana1,font=("Arial",15),width=30,bg="White",fg="#515151")
    entry_competencias.place(x=posx+deltax,y=posy+3*deltay)
    entry_competencias.insert(0, piloto[5][:-1])
    label_competencias= Label(canvas2_ventana1,font=("Arial",15), text=" Competencias: ",bg="#0059A6", height=1,fg="White",borderwidth=2, relief="groove",width=15)
    label_competencias.place(x=posx,y=posy+deltay*3)


    entry_ganados=Entry(canvas2_ventana1,font=("Arial",15),width=30,bg="White",fg="#515151")
    entry_ganados.place(x=posx+deltax,y=posy+deltay*4)
    entry_ganados.insert(0, piloto[6][:-1])
    label_ganados= Label(canvas2_ventana1,font=("Arial",15), text=" Ganados: ",bg="#0059A6", height=1,fg="White",borderwidth=2, relief="groove",width=15)
    label_ganados.place(x=posx,y=posy+deltay*4)


    entry_cuasiganados=Entry(canvas2_ventana1,font=("Arial",15),width=30,bg="White",fg="#515151")
    entry_cuasiganados.place(x=posx+deltax,y=posy+deltay*5)
    entry_cuasiganados.insert(0, piloto[7][:-1])
    label_cuasiganados= Label(canvas2_ventana1,font=("Arial",15), text=" Casiganados: ",bg="#0059A6", height=1,fg="White",borderwidth=2, relief="groove",width=15)
    label_cuasiganados.place(x=posx,y=posy+deltay*5)


    entry_descalificados=Entry(canvas2_ventana1,font=("Arial",15),width=30,bg="White",fg="#515151")
    entry_descalificados.place(x=posx+deltax,y=posy+deltay*6)
    entry_descalificados.insert(0, piloto[8][:-1])
    label_descalificados =Label(canvas2_ventana1,font=("Arial",15), text=" Descalificados: ",bg="#0059A6", height=1,fg="White",borderwidth=2, relief="groove",width=15)
    label_descalificados.place(x=posx,y=posy+deltay*6)



    def devolverse():
        canvas2_ventana1.pack_forget()
        time.sleep(0.05)
        canvas_ventana1.pack()
        global animationFlag
        animationFlag=True
        thread2= Thread(target=colorear,args=())
        thread2.start()
    
    def actualizar_pilotos():
        pilotos[piloto_ind]=piloto
        pil_texto= open("Pilotos.txt","w")
        pilotos_lista=[]
        for i in range(len(pilotos)):
            pilotos_lista+= pilotos[i][:9]
        pil_texto.writelines(pilotos_lista)
        pil_texto.close()
        actualizar()
        devolverse()

  
    def actualizar_piloto():
        error=False
        try:
            edad=abs(int(entry_edad.get()))
        except:
            messagebox.showinfo("Error","La edad debe ser un entero")
            error=True
            
        try:
            competencias=abs(int(entry_competencias.get()))
        except:
            messagebox.showinfo("Error","Las competencias debe ser un entero")
            error=True

        try:
            descalificados=abs(int(entry_descalificados.get()))
        except:
            messagebox.showinfo("Error","Los descalificados debe ser un entero")
            error=True
        
        try:
            ganados=abs(int(entry_ganados.get()))
        except:
            messagebox.showinfo("Error","Los ganados debe ser un entero")
            error=True

        try:
            casiganados=abs(int(entry_cuasiganados.get()))
        except:
            messagebox.showinfo("Error","Los casiganados debe ser un entero")
            error=True

        nombre=entry_nombre.get()
        if len(nombre)==0:
            messagebox.showinfo("Error","El nombre debe de tener letras")
            error=True

           
        pais=entry_nacionalidad.get()
        pais=pais.upper()
        paises="Argentina, Belgium, Brazil, France, Germany, Netherlands, New Zealand, Portugal, Switzerland, UK"
        if pais!="ARGENTINA" and pais!="BELGIUM" and pais!="BRAZIL" and pais!="FRANCE" and pais!="GERMANY" and pais!="NETHERLANDS" and pais!="NEW ZEALAND" and pais!="PORTUGAL" and pais!="SWITZERLAND" and pais!="UK":
            messagebox.showinfo("Error","Los paises soportados son: "+paises)
            error=True
        if error:
            return
        elif competencias<ganados+casiganados+descalificados:
            error=True
            messagebox.showinfo("Error","Hay incoherencia en las participaciones del piloto")
            return
        else:
            piloto[0]=nombre+"\n"
            piloto[2]=str(edad)+"\n"
            piloto[3]=pais+"\n"
            piloto[5]=str(competencias)+"\n"
            piloto[6]=str(ganados)+"\n"
            piloto[7]=str(casiganados)+"\n"
            piloto[8]=str(descalificados)+"\n"

            estadisticas=calcular_estadisticas(piloto)
            piloto[9]=estadisticas[0]
            piloto[10]=estadisticas[1]
            actualizar_pilotos()
            
    guardar_boton=Button(canvas2_ventana1, text= "Guardar",font=("Arial",15),bg="#ea8c00", fg="White",cursor="hand2", width=8, command=actualizar_piloto)
    guardar_boton.place(x=posx+deltax+80,y=posy+deltay*7)

    cancelar_boton=Button(canvas2_ventana1, text= "Cancelar",font=("Arial",15),bg="#ea8c00", fg="White",cursor="hand2", command=devolverse)
    cancelar_boton.place(x=posx+deltax-40,y=posy+deltay*7)
    
def _delete_window():
    global animationFlag
    animationFlag=False
    respuesta=messagebox.askokcancel("Python","Seguro que quiere salir?")
    if respuesta:
        ventana1.destroy()
    else:
        thread1= Thread(target=colorear,args=())
        thread1.start()
        

ventana1.protocol("WM_DELETE_WINDOW", _delete_window)
ventana1.mainloop()
