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


#Ventana principal
root=Tk()
root.title('Test Drive')
root.minsize(1000, 550)
root.resizable(width=NO, height=NO)


#lienzo
Lienzo=Canvas(root, width=1000, height=550, bg='light blue')
Lienzo.place(x=-1, y=0)

imagen = PhotoImage(file = "fondo.png")
Lienzo.create_image(0,0,anchor=NW,image = imagen)


#cuadros de texto y sus nombres
Titulo1=Label(Lienzo, text="Mensajes enviados", font=('Arial', 6), bg='white', fg='black')
Titulo1.place(x=850, y=360)

Titulo2=Label(Lienzo, text="Mensaje recibido", font=('Arial', 6), bg='white', fg='black')
Titulo2.place(x=850, y=450)

enviar=tkscrolled.ScrolledText(Lienzo, height=2, width=20)
enviar.place(x=785,y=390)

recibir=tkscrolled.ScrolledText(Lienzo, height=2, width=20)
recibir.place(x=785, y=480)

#Se crea el cliente para NodeMCU
carro = NodeMCU()
carro.start()

#variable global para poder acelerar
global potencia
potencia=50

def get_mensajes():
    """El siguiente metodo se encarga de capturar los mensajes que se envian al node, junto con su respuesta, y los hace visibles en la pantalla
    E: Niguna
    S: Ninguna
    R: Ninguna"""
    indice = 0
    while(carro.loop):
        while(indice < len(carro.log)):
            msg_envio = "[{0}] cmd: {1}\n".format(indice,carro.log[indice][0])
            enviar.insert(END,msg_envio)
            enviar.see("end")

            msg_recibido = "[{0}] result: {1}\n".format(indice,carro.log[indice][1])
            recibir.insert(END, msg_recibido)
            recibir.see('end')

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

#Se vincula tecla Enter a la función send
root.bind('<Return>', send)

p = Thread(target=get_mensajes)
p.start()
           

titulo = Label(Lienzo,text="Mensaje:",font=('Agency FB',12),bg='white',fg='black')
titulo.place(x=300,y=50)

comando = Entry(Lienzo,width=20,font=('Agency FB',12))
comando.place(x=350,y=50)


#Botones

Btn_1 = Button(Lienzo,text='Send',command=lambda:send(None), fg='white',bg='blue', font=('Agency FB',12))
Btn_1.place(x=500,y=50)
#boton para acelerar
Acelerar = Button(Lienzo,text='Acelerar',command= Aceleracion, fg='white',bg='black', font=('Agency FB',15))
Acelerar.place(x=800,y=40)
#boton para frenar, pero tiene el comando sense para probarlo era nada mas
Frenar = Button(Lienzo,text=' Frenar ',command= lambda:send("Sense;"), fg='white',bg='black', font=('Agency FB',15))
Frenar.place(x=900,y=40)
Izq = Button(Lienzo,text='⇽',command= 1, fg='white',bg='black', font=('Agency FB',20))
Izq.place(x=810,y=100)
Der = Button(Lienzo,text='⇾',command= 1, fg='white',bg='black', font=('Agency FB',20))
Der.place(x=910,y=100)
Celeb = Button(Lienzo,text='Celebrar',command= 1, fg='white',bg='black', font=('Agency FB',15))
Celeb.place(x=800,y=300)
Mov = Button(Lienzo,text='Mov.Especial',command= 1, fg='white',bg='black', font=('Agency FB',15))
Mov.place(x=890,y=300)
LuzF = Button(Lienzo,text='Luces Frontales',command= 1, fg='white',bg='black', font=('Agency FB',15))
LuzF.place(x=770,y=180)
LuzT = Button(Lienzo,text='Luces Traseras',command= 1, fg='white',bg='black', font=('Agency FB',15))
LuzT.place(x=885,y=180)
LuzD = Button(Lienzo,text='Direccionales',command= 1, fg='white',bg='black', font=('Agency FB',15))
LuzD.place(x=830,y=240)

pwm = Label(Lienzo,text="pwm",font=('Agency FB',14),bg='white',fg='black')
pwm.place(x=355,y=358)

root.mainloop()
