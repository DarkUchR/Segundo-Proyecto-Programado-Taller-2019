from tkinter import *
from threading import Thread
import threading 
import os
import time
from tkinter import messagebox

#Se crea la ventana y se configura
def cambiar_menu_carros(ventana1, canvas_original, scrollbar ):
    #Se crea el canvas y se configura
    canvas_ventana1 = Canvas(ventana1,width= 1000,height = 800, bg = "white",scrollregion=(0, 0, 1000, 1800) , yscrollcommand = scrollbar.set)
    canvas_ventana1.place(x=0, y=0)
    canvas_ventana1.pack()


    def cargar_imagen(nombre):
        direccion= os.path.join('Imagenes',nombre)
        imagen= PhotoImage(file=direccion)
        return imagen

    carros_archivo= open("Carros.txt","r")
    info_carros=carros_archivo.readlines()

    carros=[]
    for i in range(len(info_carros)//14):
        
        carros_simple= info_carros[14*i:14*(i+1)]
        carros.append(carros_simple)
    global bar
    bar= cargar_imagen("bar.png")
    titulos= Label(canvas_ventana1,font=("Arial",13),bg="#0059A6",fg ="white",borderwidth=2, relief="groove", text="               Carro                                 Marca             Modelo               Piloto              Temporada           Eficiencia                          ")
    titulos.place(x=1,y=1)
    rectangulos=[]
    global caras
    caras=[]
    global carros_imgs
    carros_imgs=[]
    global indice
    indice= cargar_imagen("position.png")
    for i in range(len(carros)):
        carro=carros[i]

        rectangulos.append(canvas_ventana1.create_rectangle(1, 40+78*i, 920, 32+78*(i+1), fill='white',outline="white"))
        canvas_ventana1.tag_lower(rectangulos[-1])
        
        imagen_indice=canvas_ventana1.create_image(1,40+78*i,image = indice ,anchor = NW)
        carros_imgs= [cargar_imagen(carro[4][:-1]+".png")]+carros_imgs
        imagen_carro=canvas_ventana1.create_image(70,55+78*i,image = carros_imgs[0] ,anchor = NW)
        caras= [cargar_imagen(carro[0][:-1]+".png")]+caras
        imagen_cara = canvas_ventana1.create_image(510,40+78*i,image = caras[0] ,anchor = NW)
        imagen_bar = canvas_ventana1.create_image(30,110+78*i,image = bar ,anchor = NW)
        
        imagen_marca= canvas_ventana1.create_text((285,65+78*i),font=("Arial",15), text=carro[2],anchor = NW)
        imagen_modelo= canvas_ventana1.create_text((384,65+78*i),font=("Arial",15),text=carro[3],anchor = NW)
        imagen_temporada= canvas_ventana1.create_text((650,65+78*i),font=("Arial",15), text=carro[5],anchor = NW)
        imagen_eficiencia= canvas_ventana1.create_text((805,65+78*i),font=("Arial",15),text=carro[12],anchor = NW)
        carro+=[imagen_carro,imagen_cara,imagen_marca,imagen_modelo, imagen_temporada, imagen_eficiencia]

    def actualizar():
        for i in range(len(carros)):
            canvas_ventana1.coords(carros[i][14],70,55+78*i)
            canvas_ventana1.coords(carros[i][15],510,40+78*i)
            canvas_ventana1.coords(carros[i][16],285,65+78*i)
            canvas_ventana1.itemconfig(carros[i][16],text=carros[i][2])
            canvas_ventana1.coords(carros[i][17],384,65+78*i)
            canvas_ventana1.itemconfig(carros[i][17],text=carros[i][3])
            canvas_ventana1.coords(carros[i][18],650,65+78*i)
            canvas_ventana1.itemconfig(carros[i][18],text=carros[i][5])
            canvas_ventana1.coords(carros[i][19],805,65+78*i)
            canvas_ventana1.itemconfig(carros[i][19],text=carros[i][12])

        if carro_selected:
            deshabilitar_eleccion(carro_waiting)
            



    def ordenar_carros(valor):
        if valor== "eficiencia":
            n=12
        
        for i in range(len(carros)):
            for j in range(len(carros)-i-1):
                if int(carros[j][n][:-1])<int(carros[j+1][n][:-1]):
                    temp=carros[j]
                    carros[j]=carros[j+1]
                    carros[j+1]=temp
        
    def ordenar_inverso_carros(valor):
        if valor== "eficiencia":
            n=12

        for i in range(len(carros)):
            for j in range(len(carros)-i-1):            
                if int(carros[j][n][:-1])>int(carros[j+1][n][:-1]):
                    temp=carros[j]
                    carros[j]=carros[j+1]
                    carros[j+1]=temp

        
    orden_eficiencia=1
    def ordenar_eficiencia():
        nonlocal orden_eficiencia
        if orden_eficiencia==1:
            ordenar_carros("eficiencia")
        else:
            ordenar_inverso_carros("eficiencia")
        orden_eficiencia*=-1        
            
        actualizar()



    def edit():
        nonlocal carro_waiting
        global animationFlag
        canvas_ventana1.pack_forget()
        animationFlag=False
        editar_carro_ventana(carros[carro_waiting],carro_waiting)
        deshabilitar_eleccion(carro_waiting)

        
    carro_waiting=-1
    carro_selected=False
    def leftclick(event):
        x = canvas_ventana1.winfo_pointerx() - canvas_ventana1.winfo_rootx()
        y = canvas_ventana1.winfo_pointery() - canvas_ventana1.winfo_rooty()+scrollbar.get()[0]*(1800) 
        if  1<x<920:
            for i in range(22):
                if 40+78*i<y<32+78*(i+1):
                    if canvas_ventana1.itemcget(rectangulos[i], "fill")=="#b5b5bc":
                        deshabilitar_eleccion(i)
                    else:
                        deshabilitar_eleccion(carro_waiting)
                        habilitar_eleccion(i)
                
                        
    def habilitar_eleccion(indice_rectangulo):
        nonlocal carro_selected
        nonlocal carro_waiting
        canvas_ventana1.itemconfig(rectangulos[indice_rectangulo], fill="#b5b5bc")
        run_button.config(state="normal")
        edit_button.config(state="normal")
        carro_selected=True
        carro_waiting=indice_rectangulo                   

    def deshabilitar_eleccion(indice_rectangulo):
        nonlocal carro_selected
        nonlocal carro_waiting
        canvas_ventana1.itemconfig(rectangulos[indice_rectangulo], fill="white")
        run_button.config(state="disabled")
        edit_button.config(state="disabled")
        carro_waiting=-1
        carro_selected=False

    def colorear():
        global animationFlag
        nonlocal carro_waiting
        animationFlag=True
        while animationFlag:
            time.sleep(0.03)
            x = canvas_ventana1.winfo_pointerx() - canvas_ventana1.winfo_rootx()
            y = canvas_ventana1.winfo_pointery() - canvas_ventana1.winfo_rooty()+scrollbar.get()[0]*(1800) 
            for i in range(len(rectangulos)):
                if 1<x<920 and 40+78*i<y<32+78*(i+1):
                    if i!=carro_waiting:
                        canvas_ventana1.itemconfig(rectangulos[i], fill="#dbdde0")
                    while 1<x<920 and 40+78*i<y<32+78*(i+1) and animationFlag:
                        x = canvas_ventana1.winfo_pointerx() - canvas_ventana1.winfo_rootx()
                        y = canvas_ventana1.winfo_pointery() - canvas_ventana1.winfo_rooty()+scrollbar.get()[0]*(1800) 
                        time.sleep(0.03)
                    if i!=carro_waiting:
                        canvas_ventana1.itemconfig(rectangulos[i], fill="white")
            
            
    #Se establecen los botones

    edit_button = Button(canvas_ventana1, text="Edit", font= ("Arial",13) , command=edit, state="disabled")
    edit_button.place(x=930,y=30)
    run_button = Button(canvas_ventana1, text="Run", font= ("Arial",13) , command=edit,state="disabled")
    run_button.place(x=930,y=70)

    global button_img
    button_img=cargar_imagen("button.png")
    scrollbar.config( command = canvas_ventana1.yview )
    eficiencia_button = Button(canvas_ventana1, image=button_img , command=ordenar_eficiencia)
    eficiencia_button.place(x=848,y=8)
    

    ventana1.bind("<Button-1>", leftclick)
    thread1= Thread(target=colorear,args=())
    thread1.start()
    logo= cargar_imagen("logo.png")


    def editar_carro_ventana(carro,carro_ind):
        scrollbar.pack_forget()
        canvas2_ventana1 = Canvas(ventana1,width= 1000,height = 800, bg = "white")
        canvas2_ventana1.place(x=0, y=0)
        canvas2_ventana1.pack()
        global carro_img
        carro_img= cargar_imagen(carro[4][:-1]+".png")
        imagen_logo = canvas2_ventana1.create_image(0,0,image = logo ,anchor = NW)


        posy=150
        deltay=50
        posx=250
        deltax=200
        rectangulo_cara=canvas2_ventana1.create_rectangle(posx+3*deltax/2-10, posy-1.5*deltay, posx+4*deltax/2+65,posy-1.5*deltay+40, fill='gray',outline="white")
        imagen_carro = canvas2_ventana1.create_image(posx+3*deltax/2,posy-1.5*deltay,image = carro_img ,anchor = NW)

        
        entrys=[]
        labels=[]
        texts=["Pais","Marca","Modelo","Temporada","Baterias","Pilas (pb)","Tension (pb)","Estado","Consumo","Peso","Sensores"]
        j=0
        for i in range(14):
            if i ==0 or i==4 or i==12:
                pass
            else:
                entry= Entry(canvas2_ventana1,font=("Arial",15),width=30,bg="White",fg="#515151")
                entry.place(x=posx+deltax,y=posy+deltay*j)
                entry.insert(0, carro[i][:-1])

                label= Label(canvas2_ventana1,font=("Arial",15), text=(" "+texts[j]+": "),bg="#0059A6", height=1,fg="White",borderwidth=2, relief="groove",width=15)
                label.place(x=posx,y=posy+deltay*j)
                entrys.append(entry)
                labels.append(label)
                j+=1




        def devolverse():
            canvas2_ventana1.pack_forget()
            time.sleep(0.05)
            scrollbar.pack(side = RIGHT, fill=Y)
            canvas_ventana1.pack()
            global animationFlag
            animationFlag=True
            thread2= Thread(target=colorear,args=())
            thread2.start()
        
        def actualizar_carros(carro_data):
            carros[carro_ind]=carro_data
            car_texto= open("Carros.txt","w")
            carros_lista=[]
            for i in range(len(carros)):
                carros_lista+= carros[i][:14]
                
            car_texto.writelines(carros_lista)
            car_texto.close()
            actualizar()
            devolverse()

      
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
                actualizar_carros(carro)
                
        guardar_boton=Button(canvas2_ventana1, text= "Guardar",font=("Arial",15),bg="#ea8c00", fg="White",cursor="hand2", width=8, command=actualizar_carro)
        guardar_boton.place(x=posx+deltax+80,y=posy+deltay*11)

        cancelar_boton=Button(canvas2_ventana1, text= "Cancelar",font=("Arial",15),bg="#ea8c00", fg="White",cursor="hand2", command=devolverse)
        cancelar_boton.place(x=posx+deltax-40,y=posy+deltay*11)

    def cambiar_menu_pilotos():
        canvas_ventana1.pack_forget()
        canvas_original.pack()

    def _delete_window():
        global animationFlag
        animationFlag=False
        respuesta=messagebox.askokcancel("Python","Seguro que quiere salir?")
        if respuesta:
            ventana1.destroy()
        else:
            thread1= Thread(target=colorear,args=())
            thread1.start()
            
    pilots_button = Button(canvas_ventana1, image=button_img , command=cambiar_menu_pilotos)
    pilots_button.place(x=570,y=8)
    ventana1.protocol("WM_DELETE_WINDOW", _delete_window)
