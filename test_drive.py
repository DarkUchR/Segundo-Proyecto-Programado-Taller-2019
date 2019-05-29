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
    potencia=50


    #Se vincula tecla Enter a la función send
    root.bind('<Return>', send)

    p = Thread(target=get_mensajes)
    p.start()

    #boton para acelerar
    Acelerar = Button(Lienzo,text='Acelerar',command= Aceleracion, fg='white',bg='black', font=('Agency FB',14))
    Acelerar.place(x=795,y=40)
    #boton para frenar, pero tiene el comando sense para probarlo era nada mas
    Frenar = Button(Lienzo,text=' Frenar ',command= lambda:send("Sense;"), fg='white',bg='black', font=('Agency FB',14))
    Frenar.place(x=885,y=40)
    Izq = Button(Lienzo,text='⇽',command= 1, fg='white',bg='black', font=('Agency FB',14))
    Izq.place(x=810,y=100)
    Der = Button(Lienzo,text='⇾',command= 1, fg='white',bg='black', font=('Agency FB',14))
    Der.place(x=910,y=100)
    Celeb = Button(Lienzo,text='Celebrar',command= 1, fg='white',bg='black', font=('Agency FB',14))
    Celeb.place(x=840,y=300)
    Mov = Button(Lienzo,text='Mov.Especial',command= 1, fg='white',bg='black', font=('Agency FB',14))
    Mov.place(x=822,y=350)
    LuzF = Button(Lienzo,text='Luz Frontal',command= 1, fg='white',bg='black', font=('Agency FB',14))
    LuzF.place(x=770,y=180)
    LuzT = Button(Lienzo,text='Luz Trasera',command= 1, fg='white',bg='black', font=('Agency FB',14))
    LuzT.place(x=882,y=180)
    LuzDI = Button(Lienzo,text='Dir Izq',command= 1, fg='white',bg='black', font=('Agency FB',14))
    LuzDI.place(x=808,y=240)
    LuzDD = Button(Lienzo,text='Dir Der',command= 1, fg='white',bg='black', font=('Agency FB',14))
    LuzDD.place(x=882,y=240)
    salir = Button(Lienzo,text='Volver',command= regresar_test_drive, fg='white',bg='black', font=('Agency FB',14))
    salir.place(x=850,y=400)

    pwm = Label(Lienzo,text="pwm",font=('Agency FB',14),bg='white',fg='black')
    pwm.place(x=355,y=358)
    root.protocol("WM_DELETE_WINDOW", _delete_window)
    root.mainloop()

def get_mensajes():

    """El siguiente metodo se encarga de capturar los mensajes que se envian al node, junto con su respuesta, y los hace visibles en la pantalla
    E: Niguna
    S: Ninguna
    R: Ninguna"""
    indice = 0
    while(carro.loop):
        while(indice < len(carro.log)):
            msg_envio = "[{0}] cmd: {1}\n".format(indice,carro.log[indice][0])
            
            msg_recibido = "[{0}] result: {1}\n".format(indice,carro.log[indice][1])

            indice+=1
        time.sleep(0.200)
#funcion send modificada para recibir valores mediante la configuracion de los botones nada mas
def send(msg):
    """Este metodo envia el mensaje escrito en la interfaz al node, este mensaje debe de cumplir con el sintaxis adecuado para enviarse
    E: Un evento
    S: Ninguna
    R: El mensaje debe de terminar con ; """
    mensaje = str(msg)
    if(len(mensaje)>0 and mensaje[-1] == ";"):
        carro.send(mensaje)
    else:
        messagebox.showwarning("Error en el mensaje", "Mensaje sin caracter de finalización ';' ")

#Funciones asociadas a cada boton de comandos:
        
#funcion para acelerar de 50 en 50, que muestra la potencia en pantalla
def Aceleracion():
    i=0
    global potencia
    while i<1:
        sendAcelerar(str(potencia))
        pwm2 = Label(Lienzo,text="pwm:"+str(potencia),font=('Agency FB',14),bg='white',fg='black')
        pwm2.place(x=350,y=358)
        potencia+=50
        i+=1
    
def sendAcelerar(pot):
    """Este metodo envia el mensaje escrito en la interfaz al node, este mensaje debe de cumplir con el sintaxis adecuado para enviarse
    E: Ninguna
    S: Ninguna
    R: El mensaje debe de terminar con ; """
    mensaje = "pwm,"+pot+";"
    if(len(mensaje)>0 and mensaje[-1] == ";"):
        carro.send(mensaje)
    else:
        messagebox.showwarning("Error en el mensaje", "Mensaje sin caracter de finalización ';' ")

#funcion para reversa, sin terminar
def sendReversa():
    """Este metodo envia el mensaje escrito en la interfaz al node, este mensaje debe de cumplir con el sintaxis adecuado para enviarse
    E: Ninguna
    S: Ninguna
    R: El mensaje debe de terminar con ; """
    mensaje = ""
    if(len(mensaje)>0 and mensaje[-1] == ";"):
        carro.send(mensaje)
    else:
        messagebox.showwarning("Error en el mensaje", "Mensaje sin caracter de finalización ';' ")
           

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


