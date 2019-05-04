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
root.title('Proyecto II, I Semestre 2019')
root.minsize(1000, 500)
root.resizable(width=NO, height=NO)


#lienzo
Lienzo=Canvas(root, width=1000, height=500, bg='light blue')
Lienzo.place(x=-1, y=0)

imagen = PhotoImage(file = "fondo.png")
Lienzo.create_image(0,0,anchor=NW,image = imagen)


#cuadros de texto y sus nombres
Titulo1=Label(Lienzo, text="Mensajes enviados", font=('Arial', 14), bg='white', fg='black')
Titulo1.place(x=190, y=65)

Titulo2=Label(Lienzo, text="Mensaje recibido", font=('Arial', 14), bg='white', fg='black')
Titulo2.place(x=650, y=65)

enviar=tkscrolled.ScrolledText(Lienzo, height=14, width=45)
enviar.place(x=90,y=105)

recibir=tkscrolled.ScrolledText(Lienzo, height=14, width=45)
recibir.place(x=530, y=105)

#Se crea el cliente para NodeMCU
carro = NodeMCU()
carro.start()

#El siguiente metodo se encarga de capturar los mensajes que se envian al node, junto con su respuesta, y los
#hace visibles en la pantalla
# E: Niguna
# S: Ninguna
# R: Ninguna

def get_mensajes():
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

#Este metodo envia el mensaje escrito en la interfaz al node, este mensaje debe de cumplir con el sintaxis adecuado para enviarse
#E: Ninguna
#S: Ninguna
#R: Ninguna
def send(event):

    mensaje = str(comando.get())
    if(len(mensaje)>0 and mensaje[-1] == ";"):
        comando.delete(0, 'end')
        carro.send(mensaje)
    else:
        messagebox.showwarning("Error en el mensaje", "Mensaje sin caracter de finalización ';' ")


#Se vincula tecla Enter a la función send
root.bind('<Return>', send)

p = Thread(target=get_mensajes)
p.start()
           

titulo = Label(Lienzo,text="Mensaje:",font=('Agency FB',14),bg='white',fg='black')
titulo.place(x=100,y=360)

comando = Entry(Lienzo,width=30,font=('Agency FB',14))
comando.place(x=200,y=360)




#Botones

Btn_1 = Button(Lienzo,text='Send',command=lambda:send(None), fg='white',bg='blue', font=('Agency FB',12))
Btn_1.place(x=460,y=360)

root.mainloop()
