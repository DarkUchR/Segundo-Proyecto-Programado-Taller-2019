from tkinter import *
from threading import Thread
import threading 
import os
import time
from tkinter import messagebox
from interfaz_carros import*
#Se crea la ventana y se configura
ventana1 = Tk()
ventana1.title("Brayan Alfaro");
ventana1.minsize(1000,800)
ventana1.maxsize(1000,800)
ventana1.resizable(width=NO,height=NO)
scrollbar=Scrollbar(ventana1)
scrollbar.pack( side = RIGHT, fill=Y )

scrollbar2=Scrollbar(ventana1)
#Se crea el canvas y se configura
canvas_ventana1 = Canvas(ventana1,width= 1000,height = 800, bg = "white",scrollregion=(0, 0, 1000, 1800) , yscrollcommand = scrollbar.set)
canvas_ventana1.place(x=0, y=0)
canvas_ventana1.pack()

canvas2_ventana1 = Canvas(ventana1,width= 1000,height = 800, bg = "white",scrollregion=(0, 0, 1000, 1800) , yscrollcommand = scrollbar2.set)
canvas2_ventana1.place(x=0, y=0)
canvas2_ventana1.pack()
scrollbar2.config(command=canvas2_ventana1.yview)
canvas2_ventana1.pack_forget()


canvas= 1

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


carros_archivo= open("Carros.txt","r")
info_carros=carros_archivo.readlines()

carros=[]
for i in range(len(info_carros)//14):
    
    carros_simple= info_carros[14*i:14*(i+1)]
    carros.append(carros_simple)

titulos2= Label(canvas2_ventana1,font=("Arial",13),bg="#0059A6",fg ="white",borderwidth=2, relief="groove", text="               Carro                                 Marca             Modelo               Piloto              Temporada           Eficiencia                          ")
titulos2.place(x=1,y=1)
rectangulos2=[]
caras2=[]
carros_imgs2=[]
indice= cargar_imagen("position.png")
bar= cargar_imagen("bar.png")

pilotos_archivo= open("Pilotos.txt","r")
info_pilotos=pilotos_archivo.readlines()

pilotos=[]
for i in range(len(info_pilotos)//9):

    piloto_simple= info_pilotos[9*i:9*(i+1)]
    piloto_simple+=calcular_estadisticas(piloto_simple)
    pilotos.append(piloto_simple)

titulos1= Label(canvas_ventana1,font=("Arial",13),bg="#0059A6",fg ="white",borderwidth=2, relief="groove", text="               Piloto                                 Edad      Nacionalidad               Carro                 Competencias           RGP          REP                ")
titulos1.place(x=1,y=1)
rectangulos1=[]
paises1=[]    
caras1=[]
carros1=[]

for i in range(len(carros)):
    carro=carros[i]

    rectangulos2.append(canvas2_ventana1.create_rectangle(1, 40+78*i, 920, 32+78*(i+1), fill='white',outline="white"))
    canvas2_ventana1.tag_lower(rectangulos2[-1])
    
    imagen_indice2=canvas2_ventana1.create_image(1,40+78*i,image = indice ,anchor = NW)
    carros_imgs2= [cargar_imagen(carro[4][:-1]+".png")]+carros_imgs2
    imagen_carro2=canvas2_ventana1.create_image(70,55+78*i,image = carros_imgs2[0] ,anchor = NW)
    caras2= [cargar_imagen(carro[0][:-1]+".png")]+caras2
    imagen_cara2 = canvas2_ventana1.create_image(510,40+78*i,image = caras2[0] ,anchor = NW)
    imagen_bar2 = canvas2_ventana1.create_image(30,110+78*i,image = bar ,anchor = NW)
    
    imagen_marca= canvas2_ventana1.create_text((285,65+78*i),font=("Arial",15), text=carro[2],anchor = NW)
    imagen_modelo= canvas2_ventana1.create_text((384,65+78*i),font=("Arial",15),text=carro[3],anchor = NW)
    imagen_temporada= canvas2_ventana1.create_text((650,65+78*i),font=("Arial",15), text=carro[5],anchor = NW)
    imagen_eficiencia= canvas2_ventana1.create_text((805,65+78*i),font=("Arial",15),text=carro[12],anchor = NW)
    carro+=[imagen_carro2,imagen_cara2,imagen_marca,imagen_modelo, imagen_temporada, imagen_eficiencia]

    piloto=pilotos[i]

    rectangulos1.append(canvas_ventana1.create_rectangle(1, 40+78*i, 920, 32+78*(i+1), fill='white',outline="white"))
    canvas_ventana1.tag_lower(rectangulos1[-1])
    
    imagen_indice1=canvas_ventana1.create_image(1,40+78*i,image = indice ,anchor = NW)
    
    carros1= [cargar_imagen(piloto[4][:-1]+".png")]+carros1
    imagen_carro1=canvas_ventana1.create_image(480,55+78*i,image = carros1[0] ,anchor = NW)
    caras1= [cargar_imagen(piloto[1][:-1]+".png")]+caras1
    imagen_cara1 = canvas_ventana1.create_image(70,40+78*i,image = caras1[0] ,anchor = NW)
    paises1= [cargar_imagen(piloto[3][:-1]+".png")]+paises1
    imagen_pais1 = canvas_ventana1.create_image(370,55+78*i,image = paises1[0] ,anchor = NW)
    imagen_bar1 = canvas_ventana1.create_image(30,110+78*i,image = bar ,anchor = NW)
    
    imagen_edad= canvas_ventana1.create_text((295,65+78*i),font=("Arial",15), text=piloto[2],anchor = NW)
    imagen_nombre= canvas_ventana1.create_text((150,65+78*i),font=("Arial",15),text=piloto[0],anchor = NW)
    imagen_competencias= canvas_ventana1.create_text((680,65+78*i),font=("Arial",15), text=piloto[5],anchor = NW)
    imagen_rgp= canvas_ventana1.create_text((805,65+78*i),font=("Arial",15),text=piloto[9],anchor = NW)
    imagen_rep= canvas_ventana1.create_text((890,65+78*i),font=("Arial",15), text=piloto[10],anchor = NW)

    piloto+=[imagen_carro1,imagen_cara1,imagen_pais1,imagen_edad, imagen_nombre, imagen_competencias,imagen_rgp, imagen_rep]

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

        canvas2_ventana1.coords(carros[i][14],70,55+78*i)
        canvas2_ventana1.coords(carros[i][15],510,40+78*i)
        canvas2_ventana1.coords(carros[i][16],285,65+78*i)
        canvas2_ventana1.itemconfig(carros[i][16],text=carros[i][2])
        canvas2_ventana1.coords(carros[i][17],384,65+78*i)
        canvas2_ventana1.itemconfig(carros[i][17],text=carros[i][3])
        canvas2_ventana1.coords(carros[i][18],650,65+78*i)
        canvas2_ventana1.itemconfig(carros[i][18],text=carros[i][5])
        canvas2_ventana1.coords(carros[i][19],805,65+78*i)
        canvas2_ventana1.itemconfig(carros[i][19],text=carros[i][12])
        
    if pilot_selected:
        deshabilitar_eleccion(pilot_waiting)
        



def ordenar_pilotos(valor):
    if valor== "rpg":
        n=9
        comparador=pilotos
    elif valor== "rep":
        n=10
        comparador=pilotos
    elif valor=="eficiencia":
        n=12
        comparador=carros
    for i in range(len(comparador)):
        for j in range(len(comparador)-i-1):
            if int(comparador[j][n][:-1])<int(comparador[j+1][n][:-1]):
                temp1=pilotos[j]
                temp2=carros[j]
                pilotos[j]=pilotos[j+1]
                carros[j]=carros[j+1]
                pilotos[j+1]=temp1
                carros[j+1]=temp2
    
def ordenar_inverso_pilotos(valor):
    if valor== "rpg":
        n=9
        comparador=pilotos
    elif valor== "rep":
        n=10
        comparador=pilotos
    elif valor=="eficiencia":
        n=12
        comparador=carros
    for i in range(len(comparador)):
        for j in range(len(comparador)-i-1):
            if int(comparador[j][n][:-1])>int(comparador[j+1][n][:-1]):
                temp1=pilotos[j]
                temp2=carros[j]
                pilotos[j]=pilotos[j+1]
                carros[j]=carros[j+1]
                pilotos[j+1]=temp1
                carros[j+1]=temp2
orden_rpg=1
orden_rep=1
orden_eficiencia=1
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

def ordenar_eficiencia():
    global orden_eficiencia
    if orden_eficiencia==1:
        ordenar_pilotos("eficiencia")
    else:
        ordenar_inverso_pilotos("eficiencia")
    orden_eficiencia*=-1        
        
    actualizar()
    
   
def edit():
    global pilotos
    global pilot_waiting
    global animationFlag
    global carros
    global canvas
    if canvas==1:
        canvas_ventana1.pack_forget()
    elif canvas==2:
        canvas2_ventana1.pack_forget()
    animationFlag=False
    if canvas==1:    
        editar_piloto_ventana(pilotos[pilot_waiting],pilot_waiting)
    elif canvas==2:
        editar_carro_ventana(carros[pilot_waiting],pilot_waiting)
    deshabilitar_eleccion(pilot_waiting)

    
pilot_waiting=-1
pilot_selected=False
def leftclick(event):
    x = get_mousex()
    y = get_mousey()
    if  1<x<920:
        for i in range(22):
            if 40+78*i<y<32+78*(i+1):
                if (canvas==1 and canvas_ventana1.itemcget(rectangulos1[i], "fill")=="#b5b5bc") or (canvas==2 and canvas2_ventana1.itemcget(rectangulos2[i], "fill")=="#b5b5bc"):
                    deshabilitar_eleccion(i)
                else:
                    deshabilitar_eleccion(pilot_waiting)
                    habilitar_eleccion(i)
            
                    
def habilitar_eleccion(indice_rectangulo):
    global pilot_selected
    global pilot_waiting
    if canvas==1:
        canvas_ventana1.itemconfig(rectangulos1[indice_rectangulo], fill="#b5b5bc")
        run1_button.config(state="normal")
        edit1_button.config(state="normal")
    elif canvas==2:
        canvas2_ventana1.itemconfig(rectangulos2[indice_rectangulo], fill="#b5b5bc")
        run2_button.config(state="normal")
        edit2_button.config(state="normal")
    pilot_selected=True
    pilot_waiting=indice_rectangulo                   

def deshabilitar_eleccion(indice_rectangulo):
    global pilot_selected
    global pilot_waiting
    if canvas==1:
        canvas_ventana1.itemconfig(rectangulos1[indice_rectangulo], fill="white")
        run1_button.config(state="disabled")
        edit1_button.config(state="disabled")
    elif canvas==2:
        canvas2_ventana1.itemconfig(rectangulos2[indice_rectangulo], fill="white")
        run2_button.config(state="disabled")
        edit2_button.config(state="disabled")
    pilot_waiting=-1
    pilot_selected=False


def colorear():
    global animationFlag
    global pilot_waiting
    animationFlag=True
    while animationFlag:
        time.sleep(0.03)
        
        x = get_mousex()
        y = get_mousey()
        for i in range(22):
            if 1<x<920 and 40+78*i<y<32+78*(i+1):
                if i!=pilot_waiting:
                    if canvas==1:
                        canvas_ventana1.itemconfig(rectangulos1[i], fill="#dbdde0")
                    elif canvas==2:
                        canvas2_ventana1.itemconfig(rectangulos2[i], fill="#dbdde0")
                while 1<x<920 and 40+78*i<y<32+78*(i+1) and animationFlag:
                    x = get_mousex()
                    y = get_mousey()
                    time.sleep(0.03)
                if i!=pilot_waiting:
                    if canvas==1:
                        canvas_ventana1.itemconfig(rectangulos1[i], fill="white")
                    elif canvas==2:
                        canvas2_ventana1.itemconfig(rectangulos2[i], fill="white")
def get_mousex():
    if canvas==1:
        return canvas_ventana1.winfo_pointerx() - canvas_ventana1.winfo_rootx()
    else:
        return canvas2_ventana1.winfo_pointerx() - canvas2_ventana1.winfo_rootx()

def get_mousey():
    if canvas==1:
        return canvas_ventana1.winfo_pointery() - canvas_ventana1.winfo_rooty()+scrollbar.get()[0]*(1800)
    else:
        return canvas2_ventana1.winfo_pointery() - canvas2_ventana1.winfo_rooty()+scrollbar2.get()[0]*(1800)
    
def cambiar_menu_carros():
    global canvas
    if pilot_waiting>=0:
        deshabilitar_eleccion(pilot_waiting)
    canvas=2
    scrollbar.pack_forget()
    canvas_ventana1.pack_forget()
    scrollbar2.pack( side = RIGHT, fill=Y )
    canvas2_ventana1.pack()
    


def cambiar_menu_pilotos():
    global canvas
    if pilot_waiting>=0:
        deshabilitar_eleccion(pilot_waiting)
    canvas=1
    scrollbar2.pack_forget()
    canvas2_ventana1.pack_forget()
    scrollbar.pack( side = RIGHT, fill=Y )
    canvas_ventana1.pack()



def devolverse(canvas_actual):
    if canvas==1:
        canvas_actual.pack_forget()
        canvas_ventana1.pack()
    elif canvas==2:
        canvas_actual.pack_forget()
        canvas2_ventana1.pack()
    global animationFlag
    animationFlag=True
    thread2= Thread(target=colorear,args=())
    thread2.start()
    scrollbar.pack( side = RIGHT, fill=Y )


def actualizar_pilotos(piloto,piloto_indice,canvas_actual):
    pilotos[piloto_indice]=piloto
    pil_texto= open("Pilotos.txt","w")
    pilotos_lista=[]
    for i in range(len(pilotos)):
        pilotos_lista+= pilotos[i][:9]
    pil_texto.writelines(pilotos_lista)
    pil_texto.close()

    car_texto= open("Carros.txt","w")
    carros_lista=[]
    for i in range(len(carros)):
        carros_lista+= carros[i][:14]
    car_texto.writelines(carros_lista)
    car_texto.close()
    actualizar()
    devolverse(canvas_actual)

def actualizar_carros(carro,carro_indice,canvas_actual):
    carros[carro_indice]=carro
    car_texto= open("Carros.txt","w")
    carros_lista=[]
    for i in range(len(carros)):
        carros_lista+= carros[i][:14]
        
    car_texto.writelines(carros_lista)
    car_texto.close()
    pil_texto= open("Pilotos.txt","w")
    pilotos_lista=[]
    for i in range(len(pilotos)):
        pilotos_lista+= pilotos[i][:9]    
    pil_texto.writelines(pilotos_lista)
    pil_texto.close()
    actualizar()
    devolverse(canvas_actual)
#Se establecen los botones

edit1_button = Button(canvas_ventana1, text="Edit", font= ("Arial",13) , command=edit, state="disabled")
edit1_button.place(x=930,y=30)
run1_button = Button(canvas_ventana1, text="Run", font= ("Arial",13) , command=edit,state="disabled")
run1_button.place(x=930,y=70)

edit2_button = Button(canvas2_ventana1, text="Edit", font= ("Arial",13) , command=edit, state="disabled")
edit2_button.place(x=930,y=30)
run2_button = Button(canvas2_ventana1, text="Run", font= ("Arial",13) , command=edit, state="disabled")
run2_button.place(x=930,y=70)

imagen=cargar_imagen("button.png")
scrollbar.config( command = canvas_ventana1.yview )
rpg_button = Button(canvas_ventana1, image=imagen , command=ordenar_rpg)
rep_button = Button(canvas_ventana1, image=imagen , command=ordenar_rep)
cars_button = Button(canvas_ventana1, image=imagen , command=cambiar_menu_carros)
pilots_button = Button(canvas2_ventana1, image=imagen , command=cambiar_menu_pilotos)
eficiencia_button = Button(canvas2_ventana1, image=imagen , command=ordenar_eficiencia)

eficiencia_button.place(x=848,y=8)
pilots_button.place(x=570,y=8)
rpg_button.place(x=848,y=8)
rep_button.place(x=933,y=8)
cars_button.place(x=570,y=8)

ventana1.bind("<Button-1>", leftclick)
thread1= Thread(target=colorear,args=())
thread1.start()
logo= cargar_imagen("logo.png")


def editar_piloto_ventana(piloto,piloto_ind):
    scrollbar.pack_forget()
    canvas3_ventana1 = Canvas(ventana1,width= 1000,height = 800, bg = "white")
    canvas3_ventana1.place(x=0, y=0)
    canvas3_ventana1.pack()
    global cara
    cara= cargar_imagen(piloto[1][:-1]+".png")
    imagen_logo = canvas3_ventana1.create_image(0,0,image = logo ,anchor = NW)


    posy=200
    deltay=50
    posx=250
    deltax=200
    rectangulo_cara=canvas3_ventana1.create_rectangle(posx+3*deltax/2+20, posy-2*deltay, posx+3*deltax/2+90,posy-2*deltay+70, fill='gray',outline="white")
    imagen_cara = canvas3_ventana1.create_image(posx+3*deltax/2+20,posy-2*deltay,image = cara ,anchor = NW)

    entry_nombre= Entry(canvas3_ventana1,font=("Arial",15),width=30,bg="White",fg="#515151")
    entry_nombre.place(x=posx+deltax,y=posy)
    entry_nombre.insert(0, piloto[0][:-1])

    label_nombre= Label(canvas3_ventana1,font=("Arial",15), text=" Nombre: ",bg="#0059A6", height=1,fg="White",borderwidth=2, relief="groove",width=15)
    label_nombre.place(x=posx,y=posy)


    entry_edad=Entry(canvas3_ventana1,font=("Arial",15),width=30,bg="White",fg="#515151")
    entry_edad.place(x=posx+deltax,y=posy+deltay)
    entry_edad.insert(0, piloto[2][:-1])
    label_edad= Label(canvas3_ventana1,font=("Arial",15), text=" Edad: ",bg="#0059A6", height=1,fg="White",borderwidth=2, relief="groove",width=15)
    label_edad.place(x=posx,y=posy+deltay)


    entry_nacionalidad=Entry(canvas3_ventana1,font=("Arial",15),width=30,bg="White",fg="#515151")
    entry_nacionalidad.place(x=posx+deltax,y=posy+2*deltay)
    entry_nacionalidad.insert(0, piloto[3][:-1])
    label_nacionalidad= Label(canvas3_ventana1,font=("Arial",15), text=" Nacionalidad: ",bg="#0059A6", height=1,fg="White",borderwidth=2, relief="groove",width=15)
    label_nacionalidad.place(x=posx,y=posy+2*deltay)


    entry_competencias=Entry(canvas3_ventana1,font=("Arial",15),width=30,bg="White",fg="#515151")
    entry_competencias.place(x=posx+deltax,y=posy+3*deltay)
    entry_competencias.insert(0, piloto[5][:-1])
    label_competencias= Label(canvas3_ventana1,font=("Arial",15), text=" Competencias: ",bg="#0059A6", height=1,fg="White",borderwidth=2, relief="groove",width=15)
    label_competencias.place(x=posx,y=posy+deltay*3)


    entry_ganados=Entry(canvas3_ventana1,font=("Arial",15),width=30,bg="White",fg="#515151")
    entry_ganados.place(x=posx+deltax,y=posy+deltay*4)
    entry_ganados.insert(0, piloto[6][:-1])
    label_ganados= Label(canvas3_ventana1,font=("Arial",15), text=" Ganados: ",bg="#0059A6", height=1,fg="White",borderwidth=2, relief="groove",width=15)
    label_ganados.place(x=posx,y=posy+deltay*4)


    entry_cuasiganados=Entry(canvas3_ventana1,font=("Arial",15),width=30,bg="White",fg="#515151")
    entry_cuasiganados.place(x=posx+deltax,y=posy+deltay*5)
    entry_cuasiganados.insert(0, piloto[7][:-1])
    label_cuasiganados= Label(canvas3_ventana1,font=("Arial",15), text=" Casiganados: ",bg="#0059A6", height=1,fg="White",borderwidth=2, relief="groove",width=15)
    label_cuasiganados.place(x=posx,y=posy+deltay*5)


    entry_descalificados=Entry(canvas3_ventana1,font=("Arial",15),width=30,bg="White",fg="#515151")
    entry_descalificados.place(x=posx+deltax,y=posy+deltay*6)
    entry_descalificados.insert(0, piloto[8][:-1])
    label_descalificados =Label(canvas3_ventana1,font=("Arial",15), text=" Descalificados: ",bg="#0059A6", height=1,fg="White",borderwidth=2, relief="groove",width=15)
    label_descalificados.place(x=posx,y=posy+deltay*6)
  
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
            actualizar_pilotos(piloto,piloto_ind,canvas3_ventana1)

    def devolverse_aux():
        devolverse(canvas3_ventana1)
    guardar_boton=Button(canvas3_ventana1, text= "Guardar",font=("Arial",15),bg="#ea8c00", fg="White",cursor="hand2", width=8, command=actualizar_piloto)
    guardar_boton.place(x=posx+deltax+80,y=posy+deltay*7)

    cancelar_boton=Button(canvas3_ventana1, text= "Cancelar",font=("Arial",15),bg="#ea8c00", fg="White",cursor="hand2", command=devolverse_aux)
    cancelar_boton.place(x=posx+deltax-40,y=posy+deltay*7)
def editar_carro_ventana(carro,carro_ind):
    scrollbar.pack_forget()
    canvas4_ventana1 = Canvas(ventana1,width= 1000,height = 800, bg = "white")
    canvas4_ventana1.place(x=0, y=0)
    canvas4_ventana1.pack()
    global carro_img
    carro_img= cargar_imagen(carro[4][:-1]+".png")
    imagen_logo = canvas4_ventana1.create_image(0,0,image = logo ,anchor = NW)


    posy=150
    deltay=50
    posx=250
    deltax=200
    rectangulo_cara=canvas4_ventana1.create_rectangle(posx+3*deltax/2-10, posy-1.5*deltay, posx+4*deltax/2+65,posy-1.5*deltay+40, fill='gray',outline="white")
    imagen_carro = canvas4_ventana1.create_image(posx+3*deltax/2,posy-1.5*deltay,image = carro_img ,anchor = NW)

    
    entrys=[]
    labels=[]
    texts=["Pais","Marca","Modelo","Temporada","Baterias","Pilas (pb)","Tension (pb)","Estado","Consumo","Peso","Sensores"]
    j=0
    for i in range(14):
        if i ==0 or i==4 or i==12:
            pass
        else:
            entry= Entry(canvas4_ventana1,font=("Arial",15),width=30,bg="White",fg="#515151")
            entry.place(x=posx+deltax,y=posy+deltay*j)
            entry.insert(0, carro[i][:-1])

            label= Label(canvas4_ventana1,font=("Arial",15), text=(" "+texts[j]+": "),bg="#0059A6", height=1,fg="White",borderwidth=2, relief="groove",width=15)
            label.place(x=posx,y=posy+deltay*j)
            entrys.append(entry)
            labels.append(label)
            j+=1
  
    def actualizar_carro():
        error=False
        data=[]
        data.append(carro[0])

        for i in range(0,3):
            if len(entrys[i].get())>0:
                data+=[entrys[i].get()+"\n"]
            else:
                messagebox.showinfo("Error","La entrada "+ texts[i].lower()+" debe tener caracteres")
                error=True
                break
        data.append(carro[4])
        
        for i in range(3,7):
            try:
                data+=[str(abs(int(entrys[i].get())))+"\n"]
            except:
                messagebox.showinfo("Error","La entrada "+ texts[i].lower()+" debe ser un entero")
                error=True

        if entrys[7].get()=="Disponible" or entrys[7].get()=="Descargado" or entrys[7].get()=="En Reparacion":
            data+=[entrys[7].get()+"\n"]
        else:
            messagebox.showinfo("Error","Los estados posibles son: Disponible, Descargado, En Reparacion")
            error=True
            
        for i in range(8,10):
            try:
                data+=[str(abs(int(entrys[i].get())))+"\n"]
            except:
                messagebox.showinfo("Error","La entrada "+ texts[i].lower()+" debe ser un entero")
                error=True
        data.append(carro[12])        
        if entrys[10].get()== "Luz" or entrys[10].get()=="Bateria" or entrys[10].get()== "Luz\Bateria" or entrys[10].get()=="Bateria\Luz" :
            data+=[entrys[10].get()+"\n"]
        else:
            messagebox.showinfo("Error","Los sensores validos son: Luz, Bateria, Luz\Bateria, Bateria\Luz")
            error=True
            
        if error:
            pass
        else:
            for i in range(14):
                carro[i]=data[i]
            print(carro)
            actualizar_carros(carro,carro_ind, canvas4_ventana1)
    def devolverse_aux():
        devolverse(canvas4_ventana1)            
    guardar_boton=Button(canvas4_ventana1, text= "Guardar",font=("Arial",15),bg="#ea8c00", fg="White",cursor="hand2", width=8, command=actualizar_carro)
    guardar_boton.place(x=posx+deltax+80,y=posy+deltay*11)

    cancelar_boton=Button(canvas4_ventana1, text= "Cancelar",font=("Arial",15),bg="#ea8c00", fg="White",cursor="hand2", command=devolverse_aux)
    cancelar_boton.place(x=posx+deltax-40,y=posy+deltay*11)


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
