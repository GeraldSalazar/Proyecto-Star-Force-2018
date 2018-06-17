

#_____________________Importación de bibliotecas________________

import pygame, sys, os, random, time, serial
from pygame.locals import *
import tkinter
from tkinter import *
import threading
from threading import Thread
import winsound
from tkinter import messagebox

#_______________________Variables Globales_____________________

global j, Cambio, modo, restantes, energía, disparo, textofinal, terminado, pts, Lista_BestScores,leds, x, y, escribir
Lista_BestScores = []
escribir = True
leds = 000000
modo = 0
restantes = 0
pts = 0
energía = 0
disparo = False
textofinal = ''
terminado = False
i = 0
j = 0
Cambio = True
Piloto = False
x = 0
y = 0

#_______________________Cargar Imagenes______________________


def Imagenes(name):
        ruta=os.path.join('Images',name)
        imagen=PhotoImage(file=ruta) 
        return imagen

def ord_burbuja(Lista):
        return ord_burbuja_aux(Lista,0,0,False)

def ord_burbuja_aux(Lista,x,y,cambiar):
        if x == len(Lista)-y-1:
                if cambiar:
                        return ord_burbuja_aux(Lista,0,y+1,False)
                else:
                        return Lista
        if Lista[x] > Lista[x+1]:
                Tem = Lista[x]
                Lista[x] = Lista[x+1]
                Lista[x+1] = Tem
                return ord_burbuja_aux(Lista,x+1,0,True)
        else:
                return ord_burbuja_aux(Lista,x+1,0,cambiar)

def check_puntajes(B):
        global Lista_BestScores
        archivo = open("Puntajes Usuarios.txt",'r')
        if B == 120:
                archivo.close()
        else:
                archivo.seek(B)
                if archivo.readline()[:3] != '   ':
                        archivo.seek(B)
                        if archivo.readline()[1:3] != '  ':
                                archivo.seek(B)
                                if archivo.readline()[2:3] != ' ':
                                        archivo.seek(B)
                                        pts = int(archivo.readline()[:3])
                                else:
                                        archivo.seek(B)
                                        pts = int(archivo.readline()[:2])
                        else:
                                archivo.seek(B)
                                pts = int(archivo.readline()[0])
                        Lista_BestScores.append(pts)
                        Lista_BestScores = ord_burbuja(Lista_BestScores)
                archivo.close()
                return check_puntajes(B+25)

control = serial.Serial('COM5',38400,timeout=0)
time.sleep(2)

def act_control():
        global escribir
        while True:
                if escribir:
                        global leds, restantes
                        control.write('leds={leds},display={restantes};'.encode())
                        time.sleep(0.1)
                        escribir = False
                        
ac = Thread(target = act_control, args=())
ac.start()

def leer_mov():
        global escribir
        t=0
        while True:
                if not escribir:
                        global x, y
                        linea = control.readline()
                        if linea == b'':
                                escribir = True
                        else:
                                trunc_y = 36
                                if t > 2:
                                        x = linea[26:29]
                                        if x == b'-0.':
                                                trunc_y += 1
                                        x = int(float(x))
                                        if x < 0:
                                                trunc_y += 1
                                                if x < -9:
                                                        trunc_y += 1
                                        elif x > 9:
                                                trunc_y += 1
                                        y = linea[trunc_y:trunc_y+3]
                                        y = int(float(y))
                                        #print((x,y))
                                        escribir = True
                                        print(t)
                        t+=1

lm = Thread(target=leer_mov, args=())
lm.start()

def act_leds():
        global energía, restantes, leds
        while True:
                if energía > 833:
                        leds=111111
                elif energía > 666:
                        leds=111110
                elif energía > 500:
                        leds=111100
                elif energía > 333:
                        leds=111000
                elif energía > 166:
                        leds=110000
                elif energía > 0:
                        leds=100000
                else:
                        leds=000000
                time.sleep(1)

al = Thread(target=act_leds, args=())
al.start()

check_puntajes(20)

#______Listas Con Los Nombres y las Imagenes de Los Pilotos___________


Lista_N = ["Brad Owen", "Dina Brown", "Jackson Harrys", "Stephen Smith", "Frank Jones", "Kate Mason", "Vanessa Kyle", "Stella Murphy", "Evans O'Ryan", "Davis Miller", "Jaidan Lam", "Olivia Wilson", "Thomas Connor", "Charlotte Lee", "Arren Kae", "Akiha Tohno", "George Star", "Ash Fate"]
Lista_P = ["#1.gif","#2.gif","#3.gif","#4.gif","#5.gif","#6.gif","#7.gif","#8.gif","#9.gif","#10.gif","#11.gif","#12.gif","#13.gif","#14.gif","#15.gif","#16.gif","#17.gif","#18.gif"]


#______________________Pantalla Principal_________________________

Pantalla_Principal = Tk()
Pantalla_Principal.title("Star Force 2018")
Pantalla_Principal.resizable(width=NO,height=NO)
Pantalla_Principal.minsize(1000,700)

Fondo_Pantalla_P = Canvas(Pantalla_Principal, width= 1000, height= 700)
Fondo_Pantalla_P.place(x= 0, y = 0)

Img_Fondo= Imagenes("FondoInicio.gif")
Fondo_Pantalla_P.create_image(500, 350, image = Img_Fondo)


#_______________________Pantalla About___________________________


Pantalla_About = Toplevel()
Pantalla_About.title("About")
Pantalla_About.resizable(width=NO,height=NO)
Pantalla_About.minsize(700,700)
Pantalla_About.withdraw()

Fondo_Pantalla_A = Canvas(Pantalla_About, width= 700, height= 700)
Fondo_Pantalla_A.place(x= 0, y = 0)

Img_Fondo_A= Imagenes("Fondo_About.gif")
Fondo_Pantalla_A = Label(Fondo_Pantalla_A, image = Img_Fondo_A,  width= 700, height= 700, borderwidth =1)
Fondo_Pantalla_A.place(x=0, y=0)


#_________________________Musica________________________________

#Funciones para iniciar y detener la música de fondo

def musica_fondo():
          winsound.PlaySound("Musica_Fondo.wav", winsound.SND_ASYNC)
          
##a = Thread(target = musica_fondo, args=())
##a.start()



def apagar():                           
    winsound.PlaySound(None, winsound.SND_ASYNC)
    


#________________________Pantalla Puntuaciones_________________________

def Puntuaciones():
        global Lista_BestScores
        
        Pantalla_Principal.withdraw()
        Pantalla_MejoresPts = Toplevel()
        Pantalla_MejoresPts.title("Mejores Puntajes")
        Pantalla_MejoresPts.minsize(700,350)
        Pantalla_MejoresPts.resizable(width=NO,height=NO)

        Fondo_PantallaMejoresPts = Canvas(Pantalla_MejoresPts, width=700, height=350)
        Fondo_PantallaMejoresPts.place(x=0, y=0)

        Img_Fondo_MejoresPts = Imagenes("Fondo_Punt.gif")
        L_Fondo_PantallaMejoresPts = Label(Fondo_PantallaMejoresPts, image=Img_Fondo_MejoresPts, width= 700, height= 700)
        L_Fondo_PantallaMejoresPts.place(x=0, y=0)

        archivo = open("Puntajes Usuarios.txt",'r')
        texto = archivo.read()

        tabla = Label(Fondo_PantallaMejoresPts, text = texto, font=("Times", 20), bg ="light grey", width=23, fg = "black", justify = LEFT, anchor=W)
        tabla.place(x=170, y=100)
        
        def Volver():
                Pantalla_MejoresPts.destroy()
                Pantalla_Principal.deiconify()
     
        Back_Imagen4 = Imagenes("Volver_Boton.gif")
        Back_Principal4 = Button(Pantalla_MejoresPts, image = Back_Imagen4, command = Volver)
        Back_Principal4.place(x = 620, y = 300)

        Pantalla_MejoresPts.mainloop()


#______________________Pantalla Elegir Personaje_______________________


def P_Personajes():
        global i, j
        j = 0
        posx = 90
        posx2 = 90
        posx3 = 90
        
        Pantalla_Principal.withdraw()
        Pantalla_Personajes = Toplevel()
        Pantalla_Personajes.title("Selección de Personajes")
        Pantalla_Personajes.resizable(width=NO,height=NO)
        Pantalla_Personajes.minsize(1300, 700)
        
        
        Fondo_Pantalla_Personajes = Canvas(Pantalla_Personajes, width= 1300, height= 700)
        Fondo_Pantalla_Personajes.place(x= 0, y = 0)
        
        Img_Fondo_Pers= Imagenes("Fondo_Personajes.gif")
        Fondo_Pantalla_Personajes2 = Label(Fondo_Pantalla_Personajes, image = Img_Fondo_Pers,  width= 1300, height= 700)
        Fondo_Pantalla_Personajes2.place(x=0, y=0)

        def Puntuaciones2():
                Pantalla_Personajes.withdraw()
                Pantalla_Puntuaciones = Toplevel()
                Pantalla_Puntuaciones.title("Mejores Puntuaciones")
                Pantalla_Puntuaciones.resizable(width=NO,height=NO)
                Pantalla_Puntuaciones.minsize(700, 700)

                Fondo_Pantalla_Puntuaciones = Canvas(Pantalla_Puntuaciones, width= 700, height= 700)
                Fondo_Pantalla_Puntuaciones.place(x= 0, y = 0)
        
                Img_Fondo_Punt= Imagenes("Fondo_Punt.gif")
                Fondo_Pantalla_Puntuaciones = Label(Fondo_Pantalla_Puntuaciones, image = Img_Fondo_Punt,  width= 700, height= 700)
                Fondo_Pantalla_Puntuaciones.place(x=0, y=0)

        
        
        
                #_______________________________ Puntos Aleatorios de los Pilotos__________________________________

                Lista_pilotos_dos = Lista_N[:]

                #Se inicia seleccionando puntajes aleatorios con el uso del random, y almacenando estos en una lista
                def punt_aleatorias():
                        global a, y
                        a = 0
                        y = 0
                        def valores_random(lista_valores_random):
                                lista_valores_random = []
                                Lista_N = ["Brad Owen", "Dina Brown", "Jackson Harrys", "Stephen Smith", "Frank Jones", "Kate Mason", "Vanessa Kyle", "Stella Murphy", "Evans O'Ryan", "Davis Miller", "Jaidan Lam", "Olivia Wilson", "Thomas Connor", "Charlotte Lee", "Arren Kae", "Akiha Tohno", "George Star", "Ash Fate"]
                                for i in Lista_N:
                                        rand_scores = int(random.uniform(10, 80))
                                        lista_valores_random.append(rand_scores)
                                return ordenar_burbuja(lista_valores_random)


                        #Una vez guardados en la lista los puntos aleatorios se llama a la función encargada de ordenar la lista
                        def ordenar_burbuja(lista_valores_random):
                                return ordenar_burbuja_aux(lista_valores_random, 0, 0, False)
                
                        #Se utiliza el algoritmo de ordenamiento burbuja que se encarga de ordenar la lista de forma ascendente
                        def ordenar_burbuja_aux(lista_valores_random, b, a, cambio):
                                if b == len(lista_valores_random) -a - 1:
                                        if cambio:
                                                return ordenar_burbuja_aux(lista_valores_random,0, a+1, False)
                                        else:
                                                os.remove("Puntuaciones_pilotos.txt")
                                                archivo = open("Puntuaciones_pilotos.txt", "a+")
                                                return asignar_valor_piloto(lista_valores_random[::-1], Lista_pilotos_dos, 0, archivo)    #Como la lista se ordena de menor a mayor, se le da vuelta a la misma ya que
                                if lista_valores_random[b] > lista_valores_random[b+1]:                                                                          #La tabla inicia con las puntuaciones más altas primero
                                        Tem = lista_valores_random[b]
                                        lista_valores_random[b] = lista_valores_random[b+1]
                                        lista_valores_random[b+1] = Tem
                                        return ordenar_burbuja_aux(lista_valores_random,b+1, 0, True)
                                else:
                                        return ordenar_burbuja_aux(lista_valores_random, b+1, 0, cambio)
                

                        #Una vez ordenada la lista de puntuaciones se le debe asignar cada puntuacion a un piloto al azar también, para estos se utiliza también la biblioteca random
                        #La cual selecciona cada uno de los personajes y despues los elimina de la lista para que no sea elegidos dos veces.
                        #Cada piloto con se respectiva puntuacion son escritos en un documento de texto el cual será leido posteriormente para crear la table de puntuaciones
                        #Y a su vez se crea la etiqueta en la pantalla con la informacion excrita el documento de texto antes mencionado
                                
                        def asignar_valor_piloto(lista_valores_random, Lista_pilotos_dos, p, archivo):
                                if p == len(lista_valores_random):
                                        archivo.seek(0)
                                        contenido = archivo.read()
                                        Lista_pilotos_dos = Lista_N
                                        tabla = Label(Fondo_Pantalla_Puntuaciones, text = contenido, font=("Times", 20), bg ="light grey", width=23, fg = "black", justify = LEFT, anchor=W)
                                        tabla.place(x=170, y=50)
                                else:
                                        piloto_random = random.choice(Lista_pilotos_dos)
                                        archivo.write(" " + str(piloto_random) + "-----------> "+ str(int(lista_valores_random[p]))+ '\n')
                                        Lista_pilotos_dos.remove(piloto_random)
                                        return asignar_valor_piloto(lista_valores_random, Lista_pilotos_dos, p+1, archivo)

                        
                        #Se llama a la funcion para iniciar el proceso
                        valores_random([])

                punt_aleatorias()

                #_____________________________________________Botón Para Volver a la Pantalla Principal_______________________________________

        
                def Volver3():
                        Pantalla_Puntuaciones.destroy()
                        Pantalla_Personajes.deiconify()
     
                Back_Imagen3 = Imagenes("Volver_Boton.gif")
                Back_Principal3 = Button(Pantalla_Puntuaciones, image = Back_Imagen3, command = Volver3)
                Back_Principal3.place(x = 620, y = 650)
  

                Pantalla_Puntuaciones.mainloop()


        def Volver2():
                global i, j
                i = 0
                Pantalla_Personajes.destroy()
                Pantalla_Principal.deiconify()
                
                Icono_Act = PhotoImage(file = Lista_P[j])
                Icono_P2 = Button(Pantalla_Principal, image = Icono_Act, width = 80, height= 75)
                Icono_P2.place(x=860, y = 12)
                Pantalla_Principal.update()

                
                Pantalla_Principal.mainloop()

        Imag_Boton_Punt2 = Imagenes("Puntuaciones.gif")
        Boton_Punt2 = Button(Fondo_Pantalla_Personajes, image = Imag_Boton_Punt, command = Puntuaciones2)
        Boton_Punt2.place(x=1220, y = 10)
     
        Back_Imagen2 = Imagenes("Volver_Boton.gif")
        Back_Principal2 = Button(Pantalla_Personajes, image = Back_Imagen2, command = Volver2)
        Back_Principal2.place(x = 1220, y = 650)


        #___________________________Bloque de codigo para la creacion de los persojes_____________________

        
        #Se establece la lista con los nombre de las imagenes de cada personaje, un contador, y dos listas vacías
        Lista_P = ["#1.gif","#2.gif","#3.gif","#4.gif","#5.gif","#6.gif","#7.gif","#8.gif","#9.gif","#10.gif","#11.gif","#12.gif","#13.gif","#14.gif","#15.gif","#16.gif","#17.gif","#18.gif"]
        cont =0
        list_botones = []
        lista_imagen = []


        #Se encaraga de cargar cada una de la imagenes a una variable y agregar esa variable a una de las lista vacías
        
        for i in Lista_P:
                carga_imagen = PhotoImage(file=i)
                lista_imagen.append(carga_imagen)


        #Se encarga de crear las etiquetas y los botones, los cuales se acomodas a una cierta cantidad de pixeles uno de otros para que se aprecien acomodados
        #Las etiquetas contienes los nombres de los respectivos personajes y los botones son las imagenes de los personajes en sí
        #Se establece una función lambda la cual me permite conocer cual personajes ha sido seleccionado por el usuario
        #al usuario seleccionar un personaje, esta funcion me retorna el subindice del nombre del personaje de la lista de los pilotos
        for i in lista_imagen:
                cmd = lambda  x = Lista_N[cont]:  Onclick(x)
                Nombres = Label(Fondo_Pantalla_Personajes, text= Lista_N[cont], anchor=CENTER, font=("Times", 12), bg ="Black", width=11, fg = "white")
                Nombres_Bot = Button(Fondo_Pantalla_Personajes ,text =  Lista_N[cont] ,image = i, command = cmd)
                
                if cont < 6:
                        Nombres_Bot.place(x=posx, y=185)
                        Nombres.place(x=posx+1, y=295)
                        posx += 200
                        cont += 1
                        
                elif cont < 12:
                        Nombres_Bot.place(x=posx2, y=345)
                        Nombres.place(x=posx2+1, y=455)
                        posx2 += 200
                        cont += 1
                else:
                        Nombres_Bot.place(x=posx3, y=520)
                        Nombres.place(x=posx3+1, y=630)
                        posx3 += 200
                        cont += 1

                list_botones.append(Nombres_Bot)

        Pantalla_Personajes.update()
                
        Pantalla_Personajes.mainloop()


#Función lambda antes mencionada
def Onclick(opcion):
        global  Piloto, j
        Piloto = True
        if opcion == Lista_N[j]:                
                return
        else:
                j += 1
                return Onclick(opcion)


#______________________________Pantalla Configuración___________________________


def settings():
        global j                                                #La variable global "j" me indica el personaje escogido por el usuario, este es el subindice de la lista donde estan los nombres de los personajes
        Pantalla_Principal.withdraw()
        Pantalla_Settings = Toplevel()
        Pantalla_Settings.title("Configuraciones")
        Pantalla_Settings.resizable(width=NO,height=NO)
        Pantalla_Settings.minsize(700, 700)

        Fondo_Pantalla_Settings = Canvas(Pantalla_Settings, width= 700, height= 700)
        Fondo_Pantalla_Settings.place(x= 0, y = 0)
        
        Img_Fondo_Settings= Imagenes("Fondo Settings.gif")
        Fondo_Pantalla_S = Label(Fondo_Pantalla_Settings, image = Img_Fondo_Settings,  width= 700, height= 700)
        Fondo_Pantalla_S.place(x=0, y=0)

        if Piloto:
                        Personaje = Imagenes(Lista_P[j])
                        Personaje_Escogido= Button(Fondo_Pantalla_Settings, image = Personaje)
                        Personaje_Escogido.place(x=500, y = 200)

                        N_Personaje= Label(Fondo_Pantalla_Settings, text = Lista_N[j], anchor=CENTER, font=("Times", 12), bg ="Black", width=11, fg = "white")
                        N_Personaje.place(x=500, y = 315)

                        Pantalla_Settings.update()
        else:
                        No_Personaje = Imagenes("Sin_Personaje.gif")
                        No_Personaje_B= Button(Fondo_Pantalla_Settings, image = No_Personaje)
                        No_Personaje_B.place(x=500, y = 200)
                        
        
        def cambiar_b_s():
                global Cambio
                if Cambio:
                        apagar()
                        No_musica = Label(Pantalla_Settings, image=Imagen_no_musica)
                        No_musica.place(x = 500, y =100)
                        Fondo_Pantalla_Settings.update()
                        Cambio = False
                else:
                        musica_fondo()
                        No_musica = Label(Pantalla_Settings, image=Imagen_musica)
                        No_musica.place(x = 500, y =100)
                        Fondo_Pantalla_Settings.update()
                        Cambio = True


        Imagen_musica = Imagenes("Musica.gif")
        No_musica = Label(Pantalla_Settings, image=Imagen_musica)
        No_musica.place(x = 500, y =100)

        
        Imagen_no_musica = Imagenes("Quitar_Musica.gif")
        
        

        silenciar_m_image = Imagenes("Silenciar_Musica.gif")
        Boton_quitar_m = Button(Fondo_Pantalla_Settings, image = silenciar_m_image, command = cambiar_b_s)
        Boton_quitar_m.place(x=100, y=100)

        #_______________________________Cambio de Nombre____________________________________
        
        #Función Para cambiar de nombre al piloto
        #Al seleccionar cambio de nombre le saltaria una pantalla pequeña indicando el nombre nuevo del personaje
        #Al usuario escribir el nuevo nombre, esta información es tomada y la lista donde contiene los nombres de los personajes es editada, cambiando el
        #nombre anterior por el escrito por el usuario
        def cambio_de_nombre():
                global Piloto, j
                if Piloto:
                        Nuev_Nombre = Toplevel()
                        Nuev_Nombre.title("")
                        Nuev_Nombre.geometry("200x100")
                        Nuev_Nombre.resizable(width=NO,height=NO)

                        Fondo = Canvas(Nuev_Nombre, bg= "Black")
                        Fondo.place(x=0, y =0)
                        
                        Titulo = Label(Fondo, text="Editar Nombre", anchor=CENTER, font=("Times", 12), bg ="Black", width=11, fg = "white")
                        Titulo.place(x=50, y =2)
                        
                        N_Nombre = StringVar()
                        N_Nombre.set("Introduce El Nuevo Nombre")
                        Entry_Nuevo_N = Entry(Nuev_Nombre, textvariable =N_Nombre, width = 30)
                        Entry_Nuevo_N.place(x=10, y=40)


                        def cambiar_nombre():
                                global nombre_cambiado
                                Nombre_introducido = Entry_Nuevo_N.get()
                                Lista_N[j] = str(Nombre_introducido)
                                
                                N_Personaje= Label(Fondo_Pantalla_Settings, text = Lista_N[j], anchor=CENTER, font=("Times", 12), bg ="Black", width=11, fg = "white")
                                N_Personaje.place(x=500, y = 315)

                                Pantalla_Settings.update()
                                Nuev_Nombre.destroy()

                        def cancelar():
                                Nuev_Nombre.destroy()
                                

                        check = PhotoImage(file = "check.gif")
                        Boton_Check = Button(Nuev_Nombre, image = check, command = cambiar_nombre)
                        Boton_Check.place(x=50, y=65)

                        x = PhotoImage(file = "x.gif")
                        Boton_X = Button(Nuev_Nombre, image = x, command = cancelar)
                        Boton_X.place(x=125, y=65)

                        Nuev_Nombre.mainloop()
                        
                else:
                        messagebox.showinfo("Un paso antes...", "Debes escoger un piloto", parent =Fondo_Pantalla_Settings)



        
        Cambiar_N = Imagenes("Cambiar_Nombre.gif")
        Cambiar_Nombre = Button(Fondo_Pantalla_Settings, image = Cambiar_N,  command = cambio_de_nombre)
        Cambiar_Nombre.place(x=100, y = 225)

        def Volver4():
                Pantalla_Settings.destroy()
                Pantalla_Principal.deiconify()
     
        Back_Imagen4 = Imagenes("Volver_Boton.gif")
        Back_Principal4 = Button(Pantalla_Settings, image = Back_Imagen4, command = Volver4)
        Back_Principal4.place(x = 620, y = 650)      
                        
        Pantalla_Settings.mainloop()

        
#__________________Pantalla de Selección de Modo de Juego___________________

def seleccion_modo_juego():
        global Piloto                           #La variable global Piloto me indica si el usuario ha selecionado personaje o no
        if Piloto:
                Pantalla_Principal.withdraw()
                Pantalla_Seleccion = Toplevel()
                Pantalla_Seleccion.title("Selección Del Modo De Juego")
                Pantalla_Seleccion.resizable(width=NO,height=NO)
                Pantalla_Seleccion.minsize(700, 500)


                Fondo_Pantalla_Modo_J = Canvas(Pantalla_Seleccion, width= 700, height= 500)
                Fondo_Pantalla_Modo_J.place(x= 0, y = 0)
                
                
                Img_Fondo_Modo_Juego= Imagenes("Fondo_Seleccion_Modo.gif")
                Fondo_Pantalla_M_J = Label(Fondo_Pantalla_Modo_J, image = Img_Fondo_Modo_Juego,  width= 700, height= 500)
                Fondo_Pantalla_M_J.place(x=0, y=0)


                Fondo_Boton_M1 = Imagenes("Modo1.gif")
                Boton_M1 = Label(Pantalla_Seleccion, image = Fondo_Boton_M1)
                Boton_M1.place(x=160, y=180)
                
                Fondo_Boton_M2 = Imagenes("Modo2.gif")
                Boton_M2 = Label(Pantalla_Seleccion, image = Fondo_Boton_M2)
                Boton_M2.place(x=380, y=180)

                #------------
                # Constantes
                #------------

                pantalla_ancho = 1000
                pantalla_alto = 700

                #-----------------------
                # Fundiones adicionales
                #-----------------------

                def buscar_pos(Lista,Num):
                        return buscar_pos_aux(Lista,Num,0,len(Lista))

                def buscar_pos_aux(Lista,Num,i,n):
                        if i == n:
                                return 'no se encontró el puntaje'
                        else:
                                if Lista[i] == Num:
                                        return i
                                else:
                                        return buscar_pos_aux(Lista,Num,i+1,n)
                                

                def cargar_img(nombre, alpha=False):
                        ruta = os.path.join('Img',nombre)
                        image = pygame.image.load(ruta)
                        # Comprobar si la imagen tiene "canal alpha"
                        if not terminado:
                                if alpha is True:
                                        image = image.convert_alpha()
                                else:
                                        image = image.convert()
                        return image

                def actualizar_pts():
                        global Lista_BestScores
                        global pts
                        global j

                        Lista_BestScores.append(pts)
                        Lista_BestScores = ord_burbuja(Lista_BestScores)
                        if len(Lista_BestScores) > 5:
                                Lista_BestScores = Lista_BestScores[1:]
                        pos = buscar_pos(Lista_BestScores,pts)
                        pts = 0

                        reescribir_puntajes(20,4)
                        if isinstance(pos,int):
                                reescribir_nombres(Lista_N[j],4-pos,False)

                def reescribir_puntajes(B,I):
                        global Lista_BestScores
                        archivo = open("Puntajes Usuarios.txt",'r+')
                        if I < 0:
                                archivo.close()
                        else:
                                archivo.seek(B)
                                archivo.write(str(Lista_BestScores[I]))
                                archivo.close()
                                return reescribir_puntajes(B+25,I-1)

                def reescribir_nombres(nombre,pos,mover):
                        archivo = open("Puntajes Usuarios.txt",'r+')
                        if not mover:
                                corte = buscar_pos(nombre,' ')
                                nombre = nombre[:corte]
                                archivo.seek(25*pos)
                                nombre2 = archivo.readline()[:11]
                                archivo.seek(25*pos)
                                archivo.write('          ')
                                archivo.seek(25*pos)
                                archivo.write(nombre)
                                archivo.close
                                if nombre != '          ':
                                        return reescribir_nombres(nombre2,pos+1,True)
                        else:
                                if pos < 5:
                                        archivo.seek(25*pos)
                                        nombre2 = archivo.readline()[:11]
                                        archivo.seek(25*pos)
                                        archivo.write('          ')
                                        archivo.seek(25*pos)
                                        archivo.write(nombre)
                                        archivo.close
                                        return reescribir_nombres(nombre2,pos+1,True)

                
                                
        
                #-------
                # Juego
                #-------

                def jugar():
                        global terminado
                        
                        Pantalla_Seleccion.withdraw()
                        pygame.init()

                        pantalla = pygame.display.set_mode((pantalla_ancho,pantalla_alto))
                        pygame.display.set_caption('Star Force 2018')
                        pygame.display.init()

                        #--------
                        # Clases
                        #--------

                        if not terminado:
                                class Nave(pygame.sprite.Sprite):

                                        def __init__(self):
                                                pygame.sprite.Sprite.__init__(self)
                                                self.image = cargar_img('Jugador.png', alpha=True)
                                                self.rect = self.image.get_rect()
                                                self.rect.centerx = pantalla_ancho/2
                                                self.rect.centery = pantalla_alto/2

                                        def bordes(self):
                                                if self.rect.top <= 0:
                                                        self.rect.top = 0
                                                if self.rect.left <= 0:
                                                        self.rect.left = 0
                                                if self.rect.bottom >= pantalla_alto:
                                                        self.rect.bottom = pantalla_alto
                                                if self.rect.right >= pantalla_ancho:
                                                        self.rect.right = pantalla_ancho

                                class Apuntador(pygame.sprite.Sprite):

                                        def __init__(self):
                                                pygame.sprite.Sprite.__init__(self)
                                                self.image = cargar_img('Mira.png', alpha=True)
                                                self.rect = self.image.get_rect()
                                                self.rect.centerx = pantalla_ancho/2
                                                self.rect.centery = (pantalla_alto/2)-254

                                        def bordes(self):
                                                if self.rect.top <= -250:
                                                        self.rect.top = -250
                                                if self.rect.left <= 80:
                                                        self.rect.left = 80
                                                if self.rect.bottom >= pantalla_alto-250:
                                                        self.rect.bottom = pantalla_alto-250
                                                if self.rect.right >= pantalla_ancho-80:
                                                        self.rect.right = pantalla_ancho-80

                                class Asteroide(pygame.sprite.Sprite):

                                        def __init__(self):
                                                pygame.sprite.Sprite.__init__(self)
                                                self.image = cargar_img('Asteroide.png', alpha=True)
                                                self.rect = self.image.get_rect()
                                                self.rect.centerx = random.randint(0,884)
                                                self.rect.centery = -100

                                        def avance(self):
                                                if self.rect.centery < 0:
                                                        self.rect.centery = random.randint(50,950)
                                                else:
                                                        if self.rect.size != (100,100):
                                                                x = self.rect.size[0]+1
                                                                y = self.rect.size[1]+1
                                                                self.rect.size = (x,y)
                                                                self.image = cargar_img(f'Asteroide {self.rect.size[0]}.png', alpha=True)
                                                        else:
                                                                time.sleep(1)
                                                                self.__init__()

                                        def colisiones(self,objeto):
                                                global textofinal
                                                global terminado
                                                if self.rect.size == (100,100):
                                                        if self.rect.colliderect(objeto.rect):
                                                                textofinal = 'Has perdido'
                                                                terminado = True
                                
                                        def desctruccion(self,objeto):
                                                global restantes
                                                global pts
                                                global disparo
                                                if disparo:
                                                        if self.rect.colliderect(objeto.rect):
                                                                restantes -= 1
                                                                pts += random.randint(1,10)
                                                                self.__init__()

                                class Anillo(pygame.sprite.Sprite):

                                        def __init__(self):
                                                pygame.sprite.Sprite.__init__(self)
                                                self.image = cargar_img('Anillo.png', alpha=True)
                                                self.rect = self.image.get_rect()
                                                self.rect.centerx = random.randint(0,700)
                                                self.rect.centery = -100

                                        def avance(self):
                                                if self.rect.centery < 0:
                                                        self.rect.centery = random.randint(50,950)
                                                else:
                                                        if self.rect.size != (100,100):
                                                                x = self.rect.size[0]+2
                                                                y = self.rect.size[1]+2
                                                                self.rect.size = (x,y)
                                                                self.image = cargar_img(f'Anillo {self.rect.size[0]}.png', alpha=True)
                                                        else:
                                                                time.sleep(1)
                                                                self.__init__()

                                        def colisiones(self,objeto):
                                                global restantes
                                                global pts
                                                if self.rect.size == (100,100):
                                                        if self.rect.colliderect(objeto.rect):
                                                                restantes -= 1
                                                                pts += random.randint(1,10)
                                                                self.__init__()

                                class Combustible(pygame.sprite.Sprite):

                                        def __init__(self):
                                                pygame.sprite.Sprite.__init__(self)
                                                self.image = cargar_img('Combustible.png', alpha=True)
                                                self.rect = self.image.get_rect()
                                                self.rect.centerx = random.randint(50,950)
                                                self.rect.centery = -100

                                        def avance(self):
                                                if self.rect.centery < 0:
                                                        self.rect.centery = random.randint(150,550)
                                                else:
                                                        if self.rect.size[0] != 50:
                                                                x = self.rect.size[0]+2
                                                                y = self.rect.size[1]+2
                                                                self.rect.size = (x,y)
                                                                self.image = cargar_img(f'Combustible {self.rect.size[0]}.png', alpha=True)
                                                        else:
                                                                self.__init__()
                    
                                        def colisiones(self,objeto):
                                                global energía
                                                if self.rect.size[0] == 50:
                                                        if self.rect.colliderect(objeto.rect):
                                                                energía += 200
                                                                self.__init__()                

                                class Laser(pygame.sprite.Sprite):
                    
                                        def __init__(self,x,y):
                                                pygame.sprite.Sprite.__init__(self)
                                                self.image = cargar_img('Laser.png', alpha=True)
                                                self.rect = self.image.get_rect()
                                                self.rect.centerx = x
                                                self.rect.centery = y

                                        def bordes(self):
                                                if self.rect.top <= 20:
                                                        self.rect.top = 20
                                                if self.rect.left <= 80:
                                                        self.rect.left = 80
                                                if self.rect.bottom >= pantalla_alto-20:
                                                        self.rect.bottom = pantalla_alto-20
                                                if self.rect.right >= pantalla_ancho-80:
                                                        self.rect.right = pantalla_ancho-80        

                                        def disparo(self,objetivo1,objetivo2,x,y):
                                                global disparo
                                                if disparo:
                                                        if not self.rect.colliderect(objetivo1.rect) and not self.rect.colliderect(objetivo2.rect):
                                                                self.rect.top -= 30
                                                        else:
                                                                self.__init__(x,y)
                                                                disparo = False
    
                        fondo = pygame.image.load('Img\Fondo_Juego.png')
                        jugador = Nave()
                        apuntador = Apuntador()
                        laser = Laser(jugador.rect.centerx,jugador.rect.centery)
                        combustible = Combustible()
                        asteroide = Asteroide()
                        anillo = Anillo()

                        

                        pygame.key.set_repeat(1, 20)
                        pygame.mouse.set_visible(False)

                        clock = pygame.time.Clock()
    
                        while True:
                                global modo, restantes, energía, disparo, textofinal,pts, x, y
                                
                                clock.tick(100)
                                
                                fuente = pygame.font.Font(None, 20)
                                fuente2 = pygame.font.Font(None, 100)

                                jugador.bordes()
                                apuntador.bordes()
                                laser.disparo(apuntador,asteroide,jugador.rect.centerx,jugador.rect.centery)

                                if modo == 1:
                                        asteroide.avance()
                                        asteroide.colisiones(jugador)
                                        asteroide.desctruccion(laser)
                                elif modo == 2:
                                        anillo.avance()
                                        anillo.colisiones(jugador)
                                        
                                if energía <= 700:
                                        aparecer = random.randint(1,5)
                                        if aparecer == 1:
                                                combustible.avance()
                                                combustible.colisiones(jugador)

                                if energía <= 0:
                                        textofinal = 'Has perdido'
                                        terminado = True
                                        
                                if restantes == 0:
                                        textofinal = 'Has ganado'
                                        terminado = True
            
                                for event in pygame.event.get():
                                        if event.type == pygame.QUIT:
                                                control.close()
                                                pygame.quit()
                                                restantes = 0
                                                energía = 0
                                                Pantalla_Seleccion.deiconify()
                                        if not disparo:
                                                laser.bordes()
                                                if y < -10:
                                                        jugador.rect.centery -= 10
                                                        apuntador.rect.centery -= 10
                                                        laser.rect.centery -= 10
                                                elif y > 10:
                                                        jugador.rect.centery += 10
                                                        apuntador.rect.centery += 10
                                                        laser.rect.centery += 10
                                                elif x > 10:
                                                        jugador.rect.centerx -= 10
                                                        apuntador.rect.centerx -= 10
                                                        laser.rect.centerx -= 10
                                                elif x < -10:
                                                        jugador.rect.centerx += 10
                                                        apuntador.rect.centerx += 10
                                                        laser.rect.centerx += 10
                                                if event.type == pygame.KEYDOWN:
                                                        if event.key == K_SPACE:
                                                                disparo = True
                                                        elif event.key == K_ESCAPE:
                                                                control.close()
                                                                pygame.quit()
                                                                restantes = 0
                                                                energía = 0
                                                                Pantalla_Seleccion.deiconify()
                                control.write(f'leds={leds},display={restantes};'.encode())
                                texto_puntos = fuente.render(f'Puntos = {pts}',1,(255,255,255))
                                texto_restantes = fuente.render(f'Restantes = {restantes}',1,(255,255,255))
                                texto_energía = fuente.render(f'Combustible = {energía}',1,(255,255,255))
                                texto_final = fuente2.render(f'{textofinal}',1,(255,255,255))
                                pantalla.blit(fondo,(0,0))
                                pantalla.blit(texto_puntos,(1,1))
                                pantalla.blit(texto_restantes,(1,12))
                                pantalla.blit(texto_energía,(1,23))
                                pantalla.blit(asteroide.image, asteroide.rect)
                                pantalla.blit(anillo.image, anillo.rect)
                                pantalla.blit(combustible.image, combustible.rect)
                                pantalla.blit(apuntador.image, apuntador.rect)
                                pantalla.blit(laser.image, laser.rect)
                                pantalla.blit(jugador.image, jugador.rect)
                                pantalla.blit(texto_final,(300,300))
                                energía -= 1
                                pygame.display.flip()

                                if terminado:
                                        time.sleep(2)
                                        pygame.quit()
                                        restantes = 0
                                        pts += energía//100
                                        actualizar_pts()
                                        energía = 0
                                        Pantalla_Seleccion.deiconify()


                def modo1():
                        global modo, restantes, energía, terminado, textofinal
                        terminado = False
                        pygame.init()
                        textofinal = ''
                        modo = 1
                        restantes = 9
                        energía = 1000
                        jugar()

                def modo2():
                        global modo, restantes, energía, terminado, textofinal
                        terminado = False
                        pygame.init()
                        textofinal = ''
                        modo = 2
                        restantes = 9
                        energía = 1000
                        jugar()
                        
                Modo_De_Juego1 = Button(Pantalla_Seleccion, text = "Destrucción de Asteroides", anchor=CENTER, font=("Times", 12), bg ="Black", fg = "white", command=modo1)
                Modo_De_Juego1.place(x = 150, y = 350)
                
                Modo_De_Juego2 = Button(Pantalla_Seleccion, text = "Maniobras", anchor=CENTER, font=("Times", 12), bg ="Black", width=11, fg = "white", command=modo2)
                Modo_De_Juego2.place(x = 400, y = 350)


                
                def Volver5():
                        Pantalla_Seleccion.withdraw()
                        Pantalla_Principal.deiconify()
             
                Back_Imagen5 = Imagenes("Retroceder.gif")
                Back_Principal5 = Button(Pantalla_Seleccion, image = Back_Imagen5, command = Volver5)
                Back_Principal5.place(x = 10, y = 10)

                Pantalla_Seleccion.mainloop()
                

        else:
                messagebox.showinfo("Un paso antes...", "Debes escoger un piloto")
                

#____________________________Botones_____________________________

#Abrir La Ventana About
    
def Abrir_About():
        Pantalla_About.deiconify()
        Pantalla_Principal.withdraw()
Boton_Imagen_About = Imagenes("About.gif")
Boton_About = Button(Pantalla_Principal, image = Boton_Imagen_About, command= Abrir_About)
Boton_About.place(x=10, y = 10)


#_____
#Volver a la Pantalla Principal

def Volver():
        Pantalla_About.withdraw()
        Pantalla_Principal.deiconify()
Back_Imagen = Imagenes("Volver_Boton.gif")
Back_Principal = Button(Pantalla_About, image = Back_Imagen, command = Volver)
Back_Principal.place(x=620, y = 650)


#______
#Salir del Juego

def Salir():
        apagar()
        Pantalla_Principal.destroy()
        sys.exit()        
Salir_Imagen = Imagenes("Salir_Boton.gif")
Salir_Principal = Button(Pantalla_Principal, image = Salir_Imagen, command = Salir)
Salir_Principal.place(x=950, y = 10)


#______
#Botón Jugar

Imag_Boton_Jugar = Imagenes("button_jugar.gif")
Boton_Jugar = Button(Pantalla_Principal, image = Imag_Boton_Jugar, command = seleccion_modo_juego)
Boton_Jugar.place(x=885, y = 630)


#______
#Boton del personaje seleccionado

Image_Nombre_Personaje = Imagenes("Personaje_Seleccionado.gif")
Nombre_Personaje = Label(Pantalla_Principal, image = Image_Nombre_Personaje)
Nombre_Personaje.place(x=675, y=12)


#______
#Botón cuando no se ha seleccionado personaje

Icono_No_P = Imagenes("Sin_Personaje.gif")
Icono_P = Button(Pantalla_Principal, image =Icono_No_P, width = 80, height=75)
Icono_P.place(x=860, y = 12)


#______
#Botón Pantalla Configuraciones

Imag_Boton_Sett = Imagenes("Settings.gif")
Boton_Sett = Button(Pantalla_Principal, image = Imag_Boton_Sett, command = settings)
Boton_Sett.place(x=10, y = 645)


#________
#Boton para ir a la Pantalla Puntuaciones

Imag_Boton_Punt = Imagenes("Puntuaciones.gif")
Boton_Punt = Button(Pantalla_Principal, image = Imag_Boton_Punt, command = Puntuaciones)
Boton_Punt.place(x=130, y = 10)


#________
#Botón para ir a la Pantalla de selección de personaje

Pers_Ima_Boton = Imagenes("Personajes.gif")
Personajes = Button(Pantalla_Principal, command = P_Personajes, image = Pers_Ima_Boton)
Personajes.place(x=70, y = 10)


Pantalla_Principal.mainloop()

