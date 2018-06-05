#_____________________Importación de bibliotecas________________

import pygame, sys, os, random, time
from pygame.locals import *
import tkinter
from tkinter import *
import threading
from threading import Thread
import winsound
from tkinter import messagebox

#_______________________Variable Globales_____________________

global j, Cambio

j = 0
Cambio = True
Piloto = False

#_______________________Cargar Imagenes______________________


def Imagenes(name):
        ruta=os.path.join('Images',name)
        imagen=PhotoImage(file=ruta) 
        return imagen

#___________________________________________________________


Lista_N = ["Brad Owen", "Dina Brown", "Jackson Harrys", "Stephen Smith", "Frank Jones", "Kate Mason", "Vanessa Kyle", "Stella Murphy", "Evans O'Ryan", "Davis Miller", "Jaidan Lam", "Olivia Wilson", "Thomas Connor", "Charlotte Lee", "Arren Kae", "Akiha Tohno", "George Star", "Ash Fate"]
Lista_P = ["#1.gif","#2.gif","#3.gif","#4.gif","#5.gif","#6.gif","#7.gif","#8.gif","#9.gif","#10.gif","#11.gif","#12.gif","#13.gif","#14.gif","#15.gif","#16.gif","#17.gif","#18.gif"]


#___________________Pantalla Principal______________________

Pantalla_Principal = Tk()
Pantalla_Principal.title("Star Force 2018")
Pantalla_Principal.resizable(width=NO,height=NO)
Pantalla_Principal.minsize(1000,700)

Fondo_Pantalla_P = Canvas(Pantalla_Principal, width= 1000, height= 700)
Fondo_Pantalla_P.place(x= 0, y = 0)

Img_Fondo= Imagenes("FondoInicio.gif")
Fondo_Pantalla_P.create_image(500, 350, image = Img_Fondo)


#_________________Pantalla About___________________________


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



#_________________________________Musica_______________________________

def musica_fondo():
    winsound.PlaySound("Musica_Fondo.wav", winsound.SND_ASYNC)


a = Thread(target = musica_fondo, args=())
a.start()


def apagar():                           
    winsound.PlaySound(None, winsound.SND_ASYNC)


#_________________________________Botones_______________________________


def Abrir_About():
        Pantalla_About.deiconify()
        Pantalla_Principal.withdraw()
Boton_Imagen_About = Imagenes("About.gif")
Boton_About = Button(Pantalla_Principal, image = Boton_Imagen_About, command= Abrir_About)
Boton_About.place(x=10, y = 10)

#_____

def Volver():
        Pantalla_About.withdraw()
        Pantalla_Principal.deiconify()
Back_Imagen = Imagenes("Volver_Boton.gif")
Back_Principal = Button(Pantalla_About, image = Back_Imagen, command = Volver)
Back_Principal.place(x=620, y = 650)


#______

def Salir():
        apagar()
        Pantalla_Principal.destroy()
        sys.exit()
        
        
Salir_Imagen = Imagenes("Salir_Boton.gif")
Salir_Principal = Button(Pantalla_Principal, image = Salir_Imagen, command = Salir)
Salir_Principal.place(x=950, y = 10)

#_______


#_________________________________________Puntuaciones________________________________


def Puntuaciones():
        Pantalla_Principal.withdraw()
        Pantalla_Puntuaciones = Toplevel()
        Pantalla_Puntuaciones.title("Mejores Puntuaciones")
        Pantalla_Puntuaciones.resizable(width=NO,height=NO)
        Pantalla_Puntuaciones.minsize(700, 700)

        Fondo_Pantalla_Puntuaciones = Canvas(Pantalla_Puntuaciones, width= 700, height= 700)
        Fondo_Pantalla_Puntuaciones.place(x= 0, y = 0)
        
        Img_Fondo_Punt= Imagenes("Fondo_Punt.gif")
        Fondo_Pantalla_Puntuaciones = Label(Fondo_Pantalla_Puntuaciones, image = Img_Fondo_Punt,  width= 700, height= 700)
        Fondo_Pantalla_Puntuaciones.place(x=0, y=0)

        
        Lista_pilotos_dos = Lista_N[:]
        
        def punt_aleatorias():
                global x, y
                x = 0
                y = 0
                def valores_random(lista_valores_random):
                        lista_valores_random = []
                        Lista_N = ["Brad Owen", "Dina Brown", "Jackson Harrys", "Stephen Smith", "Frank Jones", "Kate Mason", "Vanessa Kyle", "Stella Murphy", "Evans O'Ryan", "Davis Miller", "Jaidan Lam", "Olivia Wilson", "Thomas Connor", "Charlotte Lee", "Arren Kae", "Akiha Tohno", "George Star", "Ash Fate"]
                        for i in Lista_N:
                                rand_scores = int(random.uniform(10, 80))
                                lista_valores_random.append(rand_scores)
                        return ordenar_burbuja(lista_valores_random)

                 
                def ordenar_burbuja(lista_valores_random):
                        return ordenar_burbuja_aux(lista_valores_random, 0, 0, False)
                
                def ordenar_burbuja_aux(lista_valores_random, y, x, cambio):
                            if y == len(lista_valores_random) -x - 1:
                                        if cambio:
                                            return ordenar_burbuja_aux(lista_valores_random,0, x+1, False)
                                        else:
                                                os.remove("Puntuaciones_pilotos.txt")
                                                archivo = open("Puntuaciones_pilotos.txt", "a+")
                                                return asignar_valor_piloto(lista_valores_random, Lista_pilotos_dos, 0, archivo)     
                            if lista_valores_random[y] > lista_valores_random[y+1]:
                                        Tem = lista_valores_random[y]
                                        lista_valores_random[y] = lista_valores_random[y+1]
                                        lista_valores_random[y+1] = Tem
                                        return ordenar_burbuja_aux(lista_valores_random,y+1, i, True)
                            else:
                                        return ordenar_burbuja_aux(lista_valores_random, y+1, i, cambio)
                

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
                        

                valores_random([])

        punt_aleatorias()
        
        def Volver3():
                Pantalla_Puntuaciones.destroy()
                Pantalla_Principal.deiconify()
     
        Back_Imagen3 = Imagenes("Volver_Boton.gif")
        Back_Principal3 = Button(Pantalla_Puntuaciones, image = Back_Imagen3, command = Volver3)
        Back_Principal3.place(x = 620, y = 650)

        

        Pantalla_Puntuaciones.mainloop()

Imag_Boton_Punt = Imagenes("Puntuaciones.gif")
Boton_Punt = Button(Pantalla_Principal, image = Imag_Boton_Punt, command = Puntuaciones)
Boton_Punt.place(x=130, y = 10)

#______________________Pantalla Elegir Personaje_______________________

i = 0


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

        def Volver2():
                global i, j
                print (j)
                i = 0
                Pantalla_Personajes.withdraw()
                Pantalla_Principal.deiconify()
                
                Icono_Act = PhotoImage(file = Lista_P[j])
                Icono_P2 = Button(Pantalla_Principal, image = Icono_Act, width = 80, height= 75)
                Icono_P2.place(x=860, y = 12)
                Pantalla_Principal.update()

                
                Pantalla_Principal.mainloop()
     
        Back_Imagen2 = Imagenes("Volver_Boton.gif")
        Back_Principal2 = Button(Pantalla_Personajes, image = Back_Imagen2, command = Volver2)
        Back_Principal2.place(x = 1220, y = 650)

        
        Lista_P = ["#1.gif","#2.gif","#3.gif","#4.gif","#5.gif","#6.gif","#7.gif","#8.gif","#9.gif","#10.gif","#11.gif","#12.gif","#13.gif","#14.gif","#15.gif","#16.gif","#17.gif","#18.gif"]
        cont =0
        list_botones = []
        lista_imagen = []
        
        for i in Lista_P:
                carga_imagen = PhotoImage(file=i)
                lista_imagen.append(carga_imagen)
       
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

Pers_Ima_Boton = Imagenes("Personajes.gif")

Personajes = Button(Pantalla_Principal, command = P_Personajes, image = Pers_Ima_Boton)
Personajes.place(x=70, y = 10)


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
        global j
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
                                print (Lista_N)
                                
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
                print (Lista_N)
                Pantalla_Settings.withdraw()
                Pantalla_Principal.deiconify()
     
        Back_Imagen4 = Imagenes("Volver_Boton.gif")
        Back_Principal4 = Button(Pantalla_Settings, image = Back_Imagen4, command = Volver4)
        Back_Principal4.place(x = 620, y = 650)

        #_______________Cambio de nombre________________________________

       
                        
        Pantalla_Settings.mainloop()
        
Imag_Boton_Sett = Imagenes("Settings.gif")
Boton_Sett = Button(Pantalla_Principal, image = Imag_Boton_Sett, command = settings)
Boton_Sett.place(x=10, y = 645)
        
#_________________________________________________________________________________________

def seleccion_modo_juego():
        global Piloto
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


                Modo_De_Juego1 = Button(Pantalla_Seleccion, text = "Destrucción de Asteroides", anchor=CENTER, font=("Times", 12), bg ="Black", fg = "white")
                Modo_De_Juego1.place(x = 150, y = 350)
                
                Modo_De_Juego2 = Button(Pantalla_Seleccion, text = "Maniobras", anchor=CENTER, font=("Times", 12), bg ="Black", width=11, fg = "white")
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
                


Imag_Boton_Jugar = Imagenes("button_jugar.gif")
Boton_Jugar = Button(Pantalla_Principal, image = Imag_Boton_Jugar, command = seleccion_modo_juego)
Boton_Jugar.place(x=885, y = 630)


Image_Nombre_Personaje = Imagenes("Personaje_Seleccionado.gif")
Nombre_Personaje = Label(Pantalla_Principal, image = Image_Nombre_Personaje)
Nombre_Personaje.place(x=675, y=12)


Icono_No_P = Imagenes("Sin_Personaje.gif")
Icono_P = Button(Pantalla_Principal, image =Icono_No_P, width = 80, height=75)
Icono_P.place(x=860, y = 12)


apagar()



Pantalla_Principal.mainloop()

