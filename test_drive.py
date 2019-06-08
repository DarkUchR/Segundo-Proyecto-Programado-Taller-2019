#Importacion de bibliotecas
from tkinter import*
from threading import Thread
import os
import time
from tkinter import messagebox

#Biblioteca para el uso del carro
from WiFiClient import NodeMCU

#E:La ventana, el nombre del piloto, la nacionalidad del piloto, el nombre de la escuderia, la imagen del piloto, la imagen del pais, el movimiento de celebracion
#S:-
#R:-
def main_test_drive(ventana,nombre, nacionalidad, escuderia, piloto_img, pais_img, mov_especial):
    #Se configura la ventana principal
    global root
    root=ventana
    root.title('Test Drive')
    root.minsize(1000, 550)
    root.resizable(width=NO, height=NO)


    #Se configura el canvas
    global Lienzo
    Lienzo=Canvas(root, width=1000, height=550, bg='light blue')
    Lienzo.pack()

    #Se configura el fondo
    imagen = PhotoImage(file = "Imagenes/fondo.png")
    bat_img= PhotoImage(file="Imagenes/btr.png")
    Lienzo.create_image(0,0,anchor=NW,image = imagen)


    #Se crea el cliente para NodeMCU
    global carro
    carro = NodeMCU()
    carro.start()

    #Se crea una variable global para poder acelerar
    global potencia
    potencia=0

    #Se crea una variable global para saber si han habido errores
    global sent_error
    sent_error=False
    
    #Se crean los diferentes botones
    Acelerar = Button(Lienzo,text='Acelerar',command= aceleracion, fg='white',bg='black', font=('Agency FB',14))
    Acelerar.place(x=795,y=40)
    Frenar = Button(Lienzo,text='Desacelerar',command= send_reversa, fg='white',bg='black', font=('Agency FB',14))
    Frenar.place(x=885,y=40)
    Izq = Button(Lienzo,text='⇽',command= izquierda, fg='white',bg='black', font=('Agency FB',14))
    Izq.place(x=810,y=100)
    Centr=Button(Lienzo,text=' ',command= centro, fg='white',bg='black', font=('Agency FB',14))
    Centr.place(x=867,y=100)
    Der = Button(Lienzo,text='⇾',command= derecha, fg='white',bg='black', font=('Agency FB',14))
    Der.place(x=910,y=100)
    Celeb = Button(Lienzo,text='Celebrar',command= celebrar, fg='white',bg='black', font=('Agency FB',14))
    Celeb.place(x=840,y=300)
    Mov = Button(Lienzo,text='Mov.Especial',command= mover_especial, fg='white',bg='black', font=('Agency FB',14))
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

    #Se crea una lista que tiene las imagenes de la potencia y otra que tiene los canvases
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

    #Se crean variables globales para las imagenes de on y off de la luz
    global on
    global off
    global luz_img
    on= PhotoImage(file="Imagenes/on.png")
    off= PhotoImage(file="Imagenes/off.png")
    
    #Se crean los elementos de tcinter para la bateria y la luz
    bat_lienzo=Lienzo.create_image(40,195,image = bat_img ,anchor = NW)
    luz_img=Lienzo.create_image(60,240,image = on ,anchor = NW)

    #Se crean los elementos asociados a la bateria, el texto de nivel y rectangulo de nivel
    global bat
    global bat_text
    bat_text = Label(Lienzo, text= "100%", font=("Agency FB",15), bg="light gray",fg="black")
    bat_text.place(x=100,y=195)    
    bat=Lienzo.create_rectangle(45, 200,45+42,200+18, fill='green',outline="green")

    #Se hace global el movimiento especial de celebracion
    global especial
    especial=mov_especial

    #Se crean los textos de la informacion del piloto
    nombre_label = Label(Lienzo,text=nombre[:-1],font=('Agency FB',14),bg='gray',fg='white')
    nombre_label.place(x=40,y=125)
    escuderia_label = Label(Lienzo,text= escuderia[:-3],font=('Agency FB',14),bg='gray',fg='white')
    escuderia_label.place(x=40,y=160)

    #Se cran imagenes para las caracteristicas del piloto
    rectangulo_cara=Lienzo.create_rectangle(43, 50,43+65,50+68, fill='gray',outline="white")
    piloto=Lienzo.create_image(40,50,image = piloto_img ,anchor = NW)
    pais=Lienzo.create_image(120,70,image = pais_img ,anchor = NW)


    #Se crean los textos que indican el estado de las luces
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

    #Se crean variables para conocer el estado del carro y enviar mensajes
    global cola
    global btlv
    global ll
    global lr
    global lf
    global lb
    global dr
    dr=0
    ll=1
    lr=1
    lf=0
    lb=0
    btlv=100
    cola=[]

    #Se crea el thread de telemetria y el de enviar mensajes(cola)
    thread_cola=Thread(target=enviar_cola,args=())
    thread_cola.start()
    thread_telemetria=Thread(target=telemetria,args=())
    thread_telemetria.start()

    #Se asocia la funcion de salir al boton de salir
    root.protocol("WM_DELETE_WINDOW", _delete_window)
    root.mainloop()
        
#E:-
#S:-
#R:-
#Funcion que sube la potencia y la agrega a la cola de mensajes y actualiza la imagen de potencia
def aceleracion():
    global potencia
    global lb
    if potencia<=1000:
        potencia+=50
        cola.append("pwm:"+str(potencia)+";")
        indice=potencia//50
        if indice<=0:
            if indice==0:
                lb=1
                luces_traseras()
            indice=abs(indice)
            Lienzo.itemconfig(pwm_canvases[indice],image="")
        else:
            indice=indice-1
            Lienzo.itemconfig(pwm_canvases[indice],image=pwm_imgs[indice])
#E:-
#S:-
#R:-
#Funcion que baja la potencia y la agrega a la cola de mensajes y actualiza la imagen de potencia    
def send_reversa():
    global potencia
    global lb
    if potencia>=-1000:
        potencia-=50
        cola.append("pwm:"+str(potencia)+";")
        indice=potencia//50
        if indice>=0:
            Lienzo.itemconfig(pwm_canvases[indice],image="")
        else:
            if indice==-1:
                lb=0
                luces_traseras()
            indice=abs(indice)-1
            Lienzo.itemconfig(pwm_canvases[indice],image=pwm_imgs[indice])
#E:-
#S:-
#R:-
#Funcion cambia las luces frontales, actualiza el texto relacionado y agrega las luces frontales a la cola
def luces_frontales():
    global lf
    if lf==0:
        lf=1
        lucesf.config(text="  E  ")
    else:
        lf=0
        lucesf.config(text="  A  ")
    cola.append("lf:")
#E:-
#S:-
#R:-
#Funcion cambia las luces traseras, actualiza el texto relacionado y agrega las luces traseras a la cola
def luces_traseras():
    global lb
    if lb==0:
        lb=1
        lucesb.config(text="  E  ")
    else:
        lb=0
        lucesb.config(text="  A  ")
    cola.append("lb:")

#E:-
#S:-
#R:-
#Funcion cambia las luces izquierda, actualiza el texto relacionado y crea el thread que las hace oscilar
def luces_izquierda():
    global ll
    if ll==1:
        ll=0
        lucesl.config(text="  E  ")
        Thread(target=actualizar_luces_izquierda,args=()).start()

    else:
        ll=1
        lucesl.config(text="  A  ")

#E:-
#S:-
#R:-
#Funcion cambia las luces derecha, actualiza el texto relacionado y crea el thread que las hace oscilar
def luces_derecha():
    global lr
    if lr==1:
        lr=0
        lucesr.config(text="  E  ")
        Thread(target=actualizar_luces_derecha,args=()).start()
    else:
        lr=1
        lucesr.config(text="  A  ")

#E:-
#S:-
#R:-
#Envia mensajes que hacen oscilar las luces derecha, termina cuando la variable global de luces derecha cambie a apagado
def actualizar_luces_derecha():
    luz=1
    while lr==0 and carro.loop:
        enviar_mensajes("lr:"+str(luz)+";")
        time.sleep(0.5)
        if luz==1:
            luz=0
        else:
            luz=1

    enviar_mensajes("lr:0;")

#E:-
#S:-
#R:-
#Envia mensajes que hacen oscilar las luces izquierda, termina cuando la variable global de luces izquierda cambie a apagado
def actualizar_luces_izquierda():
    luz=1
    while ll==0 and carro.loop:
        enviar_mensajes("ll:"+str(luz)+";")
        time.sleep(1)
        if luz==1:
            luz=0
        else:
            luz=1
    enviar_mensajes("ll:0;")

#E:-
#S:-
#R:-
#Cambia la direccional a izquierda y se lo envia a la cola            
def izquierda():
    global dr
    dr=1
    cola.append("dir:")

#E:-
#S:-
#R:-
#Cambia la direccional a derecha y se lo envia a la cola                
def derecha():
    global dr
    dr=-1
    cola.append("dir:")
#E:-
#S:-
#R:-
#Cambia la direccional a centro y se lo envia a la cola                
def centro():
    global dr
    dr=0
    cola.append("dir:")

#E:-
#S:-
#R:-
#Envia a la cola el movimiento especial del carro                    
def mover_especial():
    cola.append("indeciso;")

#E:-
#S:-
#R:-
#Crea el thread que ejecuta el movimiento especial del piloto                
def celebrar():
    Thread(target=celebrar_aux,args=()).start()

#E:-
#S:-
#R:-
#Va enviando los comandos del movimiento especial del piloto poco a poco                
def celebrar_aux():
    global especial
    especial=especial.split(";")
    global ll
    global lr
    ll=1
    lr=1
    for comando in especial:
        if comando[0:1]=="w":
            time.sleep(int(comando[1:]))
        elif comando[0:2]=="ll":
            luces_izquierda()
        elif comando[0:2]=="lr":
            luces_derecha()
        elif comando.split(":")[0]=="pwm":
            if int(comando.split(":")[1])<0:
                enviar_mensajes("lb:0;","cola")
            else:
                enviar_mensajes("lb:1;","cola")                
            enviar_mensajes(comando+";","cola")    
        else:
            enviar_mensajes(comando+";","cola")
                    
#E:-
#S:-
#R:-
#Se ejecuta en un thread que envia el mensajes de sense al carro cada 30 segundos y actualiza los elementos asociados a la luz y a la bateria
def telemetria():
    global btlv
    while carro.loop:
        #Se envia el mensaje de sense
        recepcion= enviar_mensajes("sense;")
        #Si el mensaje es correcto, se procede
        if recepcion[1]:
            #Se toma del mensaje recibido el valor de la bateria y de la luz
            sense=recepcion[0]
            print(sense)
            btlv=int(sense.split(";")[0][5:])
            luz= sense.split(";")[1][4:]
            #Se cambia la imagen de la luz de acuerdo a lo recibido
            if luz=="1":
                Lienzo.itemconfig(luz_img,image = on)
            else:
                Lienzo.itemconfig(luz_img,image = off)
            #Se cambia el color y tamano del rectangulo de bateria de acuerdo al nivel de bateria
            #Tambien se actualiza el texto de porcentaje de bateria
            if btlv>=0:
                Lienzo.coords(bat,45, 200,45+(42*btlv/100),200+18)
                bat_text.configure(text=(str(btlv)+"%"))
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
        #Se esperan 30 segundos
        time.sleep(30)
        
#E:-
#S:-
#R:-
#Envia al carro el primer elemento de la cola y lo elimina de esta, si el elemento esta definido con una variable usa esta variable como parte del mensaje
#luego elimina todas las apariciones en la cola de este tipo de variable
def enviar_cola():
    global cola
    while carro.loop:
        if len(cola)>0:
            mensaje=cola[0]
            #Si el mensaje es de pwm,dir,lf o lb se toma el valor global de estos para enviarlo al carro
            if mensaje=="pwm:":
                mensaje="pwm:"+str(potencia)+";"
                cola=delete("pwm:")
            elif mensaje =="dir:":
                mensaje="dir:"+str(dr)+";"
                cola=delete("dir:")
            elif mensaje =="lf:":
                mensaje="lf:"+str(lf)+";"
                cola=delete("lf:")
            elif mensaje =="lb:":
                mensaje="lb:"+str(lb)+";"
                cola=delete("lb:")              
            else:
                cola=cola[1:]
            enviar_mensajes(mensaje, "cola")            
        else:
            time.sleep(0.2)
#E:El mensaje, un string que indica si la fuente es la cola u otro
#S:Una dupla del mensaje recibido y un booleano que indica si este es valido o no
#R:-
#Intenta enviar el mensaje, si falla y el mensaje proviene de la cola entonces envia un mensaje de error al usuario y sale del test drive                                             
def enviar_mensajes(mensaje, fuente="no-cola"):
    errores=0
    recibido=False
    msg_recibido="-1"
    global sent_error
    #Trata de enviar el mensaje 5 veces
    while not(recibido) and errores<5 and carro.loop:
        ide = carro.send(mensaje)
        msg_recibido ="-1"
        #Mientras que no halla recibido respuesta y el tiempo de espera del carro no halla transcurrid, se fija si ha llegado respuesta
        while msg_recibido =="-1" and carro.loop:
            print(msg_recibido)
            msg_recibido = carro.readById(ide)
            time.sleep(0.200)
        #Si se recibio mensaje entonces recibido se hace True
        #Si no, se aumenta en uno los errores
        if msg_recibido=="ok" or msg_recibido[0:4]=="blvl":
            recibido=True
        else:
            errores+=1
    #Si los errores fueron 5 y la provenencia es la cola, se muestra un mensaje de error
    #Si llego correctamente el mensaje o la fuente no es cola, se retorna una tupla con el mensaje recibido y el estado del envio
    if errores==5 and fuente=="cola" and not(sent_error):
        sent_error=True
        messagebox.showinfo("Error","Error de comunicacion con el carro")             
        regresar_test_drive()
    else:
        return (msg_recibido,recibido)
#E:El mensaje
#S:Una lista, la cual es la cola con todos los mensajes iguales a la entrada recibida eliminados
#R:-
#Elimina todas las apariciones del mensaje en la cola                                
def delete(mensaje):
    result=[]
    for msg in cola:
        if msg!=mensaje:
            result.append(msg)
    return result
#E:-
#S:El nivel de la bateria
#R:-
def get_btlv():
    return btlv

#E:-
#S:-
#R:-
#Regresa al menu de pilotos                
def regresar_test_drive():
    global carro
    carro.loop=False
    time.sleep(0.5)
    Lienzo.pack_forget()
    root.quit()
#E:-
#S:-
#R:-
#Se sale adecuadamente del programa                
def _delete_window():
    global carro
    carro.loop=False
    time.sleep(0.5)
    root.destroy()


