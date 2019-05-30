#Importacion de bibliotecas
from tkinter import*
from threading import Thread
import threading
import os
import time
from tkinter import messagebox
import tkinter.scrolledtext as tkscrolled

#Biblioteca para el uso del carro
from WiFiClient import NodeMCU


def main_test_drive(ventana):
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

    imagen = PhotoImage(file = "fondo.png")
    Lienzo.create_image(0,0,anchor=NW,image = imagen)


    #Se crea el cliente para NodeMCU
    global carro
    carro = NodeMCU()
    carro.start()

    #variable global para poder acelerar
    global potencia
    potencia=0


    #Se vincula tecla Enter a la función send
    root.bind('<Return>', send)

    p = Thread(target=get_mensajes)
    p.start()

    #boton para acelerar
    Acelerar = Button(Lienzo,text='Acelerar',command= aceleracion, fg='white',bg='black', font=('Agency FB',14))
    Acelerar.place(x=795,y=40)
    #boton para frenar, pero tiene el comando sense para probarlo era nada mas
    Frenar = Button(Lienzo,text=' Frenar ',command= send_reversa, fg='white',bg='black', font=('Agency FB',14))
    Frenar.place(x=885,y=40)
    Izq = Button(Lienzo,text='⇽',command= izquierda, fg='white',bg='black', font=('Agency FB',14))
    Izq.place(x=810,y=100)
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

    global pwm
    pwm = Label(Lienzo,text="pwm: "+str(potencia),font=('Agency FB',14),bg='white',fg='black')
    pwm.place(x=355,y=358)

    global btr
    btr = Label(Lienzo,text="Bateria: "),font=('Agency FB',14),bg='white',fg='black')
    btr.place(x=355,y=358)

    global luz
    luz = Label(Lienzo,text=""),font=('Agency FB',14),bg='white',fg='black')
    luz.place(x=355,y=358)

    
    root.protocol("WM_DELETE_WINDOW", _delete_window)
    root.mainloop()

#Funciones asociadas a cada boton de comandos:
        
#funcion para acelerar de 50 en 50, que muestra la potencia en pantalla
def aceleracion():
    global potencia
    global pwm
    potencia+=50
    pwm.config(text= "pwm: "+str(potencia))
    enviar_mensajes("pwm:"+str(potencia)+";")

def send_reversa():
    
    enviar_mensajes("pwm:0;")
    global potencia
    global pwm
    potencia=0
    pwm.config(text= "pwm: 0")

def luces_frontales():
    global lf
    enviar_mensajes("lf:"+str(lf)+";")
    if lf==1:
        lf=0
    else:
        lf=1
    
def luces_traseras():
    global lb
    enviar_mensajes("lb:"+str(lb)+";")
    if lb==1:
        lb=0
    else:
        lb=1
    
def luces_izquierda():
    global ll
    enviar_mensajes("ll:"+str(ll)+";")
    if ll==1:
        ll=0
    else:
        ll=1

def luces_derecha():
    global lr
    enviar_mensajes("lr:"+str(lr)+";")
    if lr==1:
        lr=0
    else:
        lr=1


def get_sense():
    enviar_mensajes("sense;")

def izquierda():
    enviar_mensajes("dir:1;")
    
def derecha():
    enviar_mensajes("dir:-1;")

def centro():
    enviar_mensajes("dir:0;")

def mov_especial():
    enviar_mensajes("indeciso;")
    
    

    
def telemetria():
    
def enviar_mensajes(mensaje):
    errores=0
    recibido=False
    carro.send(mensaje)
    msg_recibido="-1"
    while not(recibido) and errores<5:
        carro.send(mensaje)
        while msg_recibido ="-1" and carro.loop:
            msg_recibido = carro.readById(ide)
            time.sleep(0.200)

        if msg_recibido=="ok":
            recibido=True
        elif msg_recibido[0:4]=="blvl":
            recibido=True
        else:
            errores+=1
        
    if errores=5:
        messagebox.showinfo("Error","Fallo de comunicacion con el carro, reinicielo para recuperar la comunicacion")
        return "-1"
    else:
        return msg_recibido

        
    
    
    
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


