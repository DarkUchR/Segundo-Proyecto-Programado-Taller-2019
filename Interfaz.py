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

#           _____________________________________
#__________/Creando el cliente para NodeMCU
myCar = NodeMCU()
myCar.start()


def get_log():
    """
    Hilo que actualiza los Text cada vez que se agrega un nuevo mensaje al log de myCar
    """
    indice = 0
    # Variable del carro que mantiene el hilo de escribir.
    while(myCar.loop):
        while(indice < len(myCar.log)):
            mnsSend = "[{0}] cmd: {1}\n".format(indice,myCar.log[indice][0])
            enviar.insert(END,mnsSend)
            enviar.see("end")

            mnsRecv = "[{0}] result: {1}\n".format(indice,myCar.log[indice][1])
            recibir.insert(END, mnsRecv)
            recibir.see('end')

            indice+=1
        time.sleep(0.200)
    
p = Thread(target=get_log)
p.start()
           


L_Titulo = Label(Lienzo,text="Mensaje:",font=('Agency FB',14),bg='white',fg='black')
L_Titulo.place(x=100,y=360)

E_Command = Entry(Lienzo,width=30,font=('Agency FB',14))
E_Command.place(x=200,y=360)

L_Titulo = Label(Lienzo,text="ID mensaje:",font=('Agency FB',14),bg='white',fg='black')
L_Titulo.place(x=550,y=360)

E_read = Entry(Lienzo,width=30,font=('Agency FB',14))
E_read.place(x=650,y=360)


def send (event):
    """
    Ejemplo como enviar un mensaje sencillo sin importar la respuesta
    """
    mns = str(E_Command.get())
    if(len(mns)>0 and mns[-1] == ";"):
        E_Command.delete(0, 'end')
        myCar.send(mns)
    else:
        messagebox.showwarning("Error del mensaje", "Mensaje sin caracter de finalización (';')") 


def sendShowID():
    """
    Ejemplo como capturar un ID de un mensaje específico.
    """
    mns = str(E_Command.get())
    if(len(mns)>0 and mns[-1] == ";"):
        E_Command.delete(0, 'end')
        mnsID = myCar.send(mns)
        messagebox.showinfo("Mensaje pendiente", "Intentando enviar mensaje, ID obtenido: {0}\n\
La respuesta definitiva se obtine en un máximo de {1}s".format(mnsID, myCar.timeoutLimit))
        
    else:
        messagebox.showwarning("Error del mensaje", "Mensaje sin caracter de finalización (';')")

def read():
    """
    Ejemplo de como leer un mensaje enviado con un ID específico
    """
    mnsID = str(E_read.get())
    if(len(mnsID)>0 and ":" in mnsID):
        mns = myCar.readById(mnsID)
        if(mns != ""):
            messagebox.showinfo("Resultado Obtenido", "El mensaje con ID:{0}, obtuvo de respuesta:\n{1}".format(mnsID, mns))
            E_read.delete(0, 'end')
        else:
            messagebox.showerror("Error de ID", "No se obtuvo respuesta\n\
El mensaje no ha sido procesado o el ID es invalido\n\
Asegurese que el ID: {0} sea correcto".format(mnsID))

    else:
        messagebox.showwarning("Error en formato", "Recuerde ingresar el separador (':')")

root.bind('<Return>', send) #Vinculando tecla Enter a la función send



#Botones

Btn_1 = Button(Lienzo,text='Send',command=lambda:send(None),fg='white',bg='blue', font=('Agency FB',12))
Btn_1.place(x=200,y=400)

Btn_2 = Button(Lienzo,text='Send & Show ID',command=sendShowID,fg='white',bg='blue', font=('Agency FB',12))
Btn_2.place(x=250,y=400)

Btn_3 = Button(Lienzo,text='Leer Mensaje',command=read,fg='white',bg='blue', font=('Agency FB',12))
Btn_3.place(x=650,y=400)
root.mainloop()
