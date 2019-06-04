#Importacion de bibliotecas
from tkinter import*
from threading import Thread
import os
import time
from tkinter import messagebox

#Biblioteca para el uso del carro
from WiFiClient import NodeMCU


def main_test_drive(ventana,nombre, nacionalidad, escuderia, piloto_img, pais_img):
    #Ventana principal
    global root
    root=ventana
    root.title('Test Drive')
    root.minsize(1000, 550)
    root.resizable(width=NO, height=NO)


    #lienzo
    global Lienzo
    Lienzo=Canvas(root, width=1000, height=550, bg='light blue')
    Lienzo.pack()

    imagen = PhotoImage(file = "Imagenes/fondo.png")
    bat_img= PhotoImage(file="Imagenes/btr.png")

    Lienzo.create_image(0,0,anchor=NW,image = imagen)


    #Se crea el cliente para NodeMCU
    global carro
    carro = NodeMCU()
    carro.start()

    #variable global para poder acelerar
    global potencia
    potencia=0

    
    #boton para acelerar
    Acelerar = Button(Lienzo,text='Acelerar',command= aceleracion, fg='white',bg='black', font=('Agency FB',14))
    Acelerar.place(x=795,y=40)
    #boton para frenar, pero tiene el comando sense para probarlo era nada mas
    Frenar = Button(Lienzo,text=' Frenar ',command= send_reversa, fg='white',bg='black', font=('Agency FB',14))
    Frenar.place(x=885,y=40)
    Izq = Button(Lienzo,text='⇽',command= izquierda, fg='white',bg='black', font=('Agency FB',14))
    Izq.place(x=810,y=100)
    Centr=Button(Lienzo,text=' ',command= centro, fg='white',bg='black', font=('Agency FB',14))
    Centr.place(x=867,y=100)
    Der = Button(Lienzo,text='⇾',command= derecha, fg='white',bg='black', font=('Agency FB',14))
    Der.place(x=910,y=100)
    Celeb = Button(Lienzo,text='Celebrar',command= 1, fg='white',bg='black', font=('Agency FB',14))
    Celeb.place(x=840,y=300)
    Mov = Button(Lienzo,text='Mov.Especial',command= mov_especial, fg='white',bg='black', font=('Agency FB',14))
    Mov.place(x=822,y=350)
    LuzF = Button(Lienzo,text='Luz Frontal',command= luces_frontales, fg='white',bg='black', font=('Agency FB',14))
    LuzF.place(x=770,y=180)
    LuzT = Button(Lienzo,text='Luz Trasera',command= luces_traseras, fg='white',bg='black', font=('Agency FB',14))
    LuzT.place(x=882,y=180)
    LuzDI = Button(Lienzo,text='Dir Izq',command= luces_izquierda, fg='white',bg='black', font=('Agency FB',14))
    LuzDI.place(x=808,y=240)
    LuzDD = Button(Lienzo,text='Dir Der',command= luces_derecha, fg='white',bg='black', font=('Agency FB',14))
    LuzDD.place(x=882,y=240)
    salir = Button(Lienzo,text='Volver',command= regresar_test_drive, fg='white',bg='black', font=('Agency FB',14))
    salir.place(x=850,y=400)


    global pwm_imgs
    global pwm_canvases
    pwm_imgs=[]
    pwm_canvases=[]
    x=440
    y=430
    for i in range(1,22):
        img=PhotoImage(file="Imagenes/image_part_0"+str(i)+".png")
        pwm_imgs.append(img)
        canvas=Lienzo.create_image(x+14*i,y,image = "",anchor = NW)
        pwm_canvases.append(canvas)

    global on
    global off
    global luz_img
    on= PhotoImage(file="Imagenes/on.png")
    off= PhotoImage(file="Imagenes/off.png")

    bat_lienzo=Lienzo.create_image(40,195,image = bat_img ,anchor = NW)
    luz_img=Lienzo.create_image(60,240,image = on ,anchor = NW)

    global bat
    global bat_text
    bat_text = Label(Lienzo, text= "100%", font=("Agency FB",15), bg="light gray",fg="black")
    bat_text.place(x=100,y=195)    
    bat=Lienzo.create_rectangle(45, 200,45+42,200+18, fill='green',outline="green")

    nombre_label = Label(Lienzo,text=nombre[:-1],font=('Agency FB',14),bg='gray',fg='white')
    nombre_label.place(x=40,y=125)
    escuderia_label = Label(Lienzo,text= escuderia[:-3],font=('Agency FB',14),bg='gray',fg='white')
    escuderia_label.place(x=40,y=160)

    rectangulo_cara=Lienzo.create_rectangle(43, 50,43+65,50+68, fill='gray',outline="white")
    piloto=Lienzo.create_image(40,50,image = piloto_img ,anchor = NW)
    pais=Lienzo.create_image(120,70,image = pais_img ,anchor = NW)



    global lucesf
    lucesf = Label(Lienzo,text="  A  ",font=('Agency FB',18),bg='white',fg='black')
    lucesf.place(x=515,y=95)

    global lucesb
    lucesb = Label(Lienzo,text="  A  ",font=('Agency FB',18),bg='red',fg='black')
    lucesb.place(x=565,y=95)

    global lucesl
    lucesl = Label(Lienzo,text="  A  ",font=('Agency FB',18),bg='yellow',fg='black')
    lucesl.place(x=615,y=95)

    global lucesr
    lucesr = Label(Lienzo,text="  A  ",font=('Agency FB',18),bg='yellow',fg='black')
    lucesr.place(x=665,y=95)


    global btlv
    global ll
    global lr
    global lf
    global lb
    global dr
    dr=0
    ll=1
    lr=1
    lf=1
    lb=1
    btlv=100
    
    thread_telemetria=Thread(target=enviar_mensajes,args=["indeciso;",0])
    thread_telemetria.start()

    root.protocol("WM_DELETE_WINDOW", _delete_window)
    root.mainloop()

#Funciones asociadas a cada boton de comandos:
        
#funcion para acelerar de 50 en 50, que muestra la potencia en pantalla
def aceleracion():
    global potencia
    if potencia<=1000:
        potencia+=50
        Thread(target=enviar_mensajes,args=(["pwm:",potencia])).start()
        indice=potencia//50-1
        Lienzo.itemconfig(pwm_canvases[indice],image=pwm_imgs[indice])
    
def send_reversa():
    global potencia
    potencia=0    
    Thread(target=enviar_mensajes,args=(["pwm:",potencia])).start()
    for i in range(21):
        Lienzo.itemconfig(pwm_canvases[i],image="")
        

def luces_frontales():
    global lf
    if lf==1:
        lf=0
        lucesf.config(text="  E  ")
    else:
        lf=1
        lucesf.config(text="  A  ")
    Thread(target=enviar_mensajes,args=(["lf:",lf])).start()    
def luces_traseras():
    global lb
    if lb==1:
        lb=0
        lucesb.config(text="  E  ")
    else:
        lb=1
        lucesb.config(text="  A  ")
    Thread(target=enviar_mensajes,args=(["lb:",lb])).start()
    
def luces_izquierda():
    global ll
    if ll==1:
        ll=0
        lucesl.config(text="  E  ")
    else:
        ll=1
        lucesl.config(text="  A  ")
    Thread(target=enviar_mensajes,args=(["ll:",ll])).start()

def luces_derecha():
    global lr
    if lr==1:
        lr=0
        lucesr.config(text="  E  ")
    else:
        lr=1
        lucesr.config(text="  A  ")
    Thread(target=enviar_mensajes,args=["lr:",lr]).start()

def izquierda():
    global dr
    dr=1
    Thread(target=enviar_mensajes,args=["dir:",dr]).start()
    
def derecha():
    global dr
    dr=-1
    Thread(target=enviar_mensajes,args=["dir:",dr]).start()

def centro():
    global dr
    dr=0
    Thread(target=enviar_mensajes,args=["dir:",dr]).start()

def mov_especial():
    Thread(target=enviar_mensajes,args=["indeciso;",0]).start()
    
    

    
def telemetria():
    global btlv
    while carro.loop:
        recibido=False
        msg_recibido="-1"
        while not(recibido) and errores<5 and carro.loop:
            ide = carro.send("sense;")
            while msg_recibido =="-1" and carro.loop:
                msg_recibido = carro.readById(ide)
                time.sleep(0.200)
            if msg_recibido[0:4]=="blvl":
                recibido=True
            else:
                errores+=1                
        if errores==5:
            sense= "-1"
        else:
            sense= msg_recibido
            btlv=int(sense.split(";")[0][5:])
            luz= sense.split(";")[1][4:]
            
            if luz=="1":
                Lienzo.itemconfig(luz_img,image = on)
            else:
                Lienzo.itemconfig(luz_img,image = off)
            if btlv>=0:
                Lienzo.coords(bat,45, 200,45+(42/btlv),200+18)
                Lienzo.itemconfig(bat_text,text=str(btlv)+"%")
                if btlv == 100:
                    Lienzo.itemconfig(bat,fill="green",outline="green")
                elif 74<btlv<100:
                    Lienzo.itemconfig(bat,fill="Light Green",outline="Light Green")
                elif 49<btlv<75:
                    Lienzo.itemconfig(bat,fill="Yellow",outline="Yellow")
                elif 24<btlv<50:
                    Lienzo.itemconfig(bat,fill="Orange",outline="Orange")
                else:
                    Lienzo.itemconfig(bat,fill="Red",outline="Red")
        time.sleep(30)
        

def enviar_mensajes(texto,variable):
    errores=0
    recibido=False
    if texto[-1:]==":":
        mensaje=texto+str(variable)+";"
    else:
        mensaje=texto
    msg_recibido="-1"
    while not(recibido) and errores<5 and carro.loop:
        ide = carro.send(mensaje)
        while msg_recibido =="-1" and carro.loop:
            msg_recibido = carro.readById(ide)
            time.sleep(0.200)
        new_value=cambios(texto, variable)
        if msg_recibido=="ok":
            recibido=True
        if new_value:
            break
        else:
            errores+=1            

def cambios(texto,inicial):
    variable=inicial
    if texto=="lr:":
        variable=lr
    elif texto=="ll:":
        variable=ll
    elif texto=="lf:":
        variable=lf
    elif texto=="lb:":
        variable=lb
    elif texto== "pwm:":
        variable = potencia
    elif texto== "dir:":
        variable = dr
    if str(inicial)!=str(variable):
        return True
    else:
        return False
    
    
def get_btlv():
    return btlv
def regresar_test_drive():
    global carro
    carro.loop=False
    time.sleep(0.5)
    Lienzo.pack_forget()
    root.quit()

def _delete_window():
    global carro
    carro.loop=False
    time.sleep(0.5)
    root.destroy()


