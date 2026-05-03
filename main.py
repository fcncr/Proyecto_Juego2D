#Proyecto de plataformas 2D
#Fabián Cambronero Núñez 
#Carné: 2026079420

#------------------
#Importamos Tkinter
#------------------
import tkinter as tk
from tkinter import messagebox
import winsound

#Tamaño visual de cada cuadro en el mapa
TAM = 40

#ELEMENTOS DE LA MATRIZ 
# 0 = vacio
# 1 = bloque
# 2 = escalera
# 3 = enemigo estatico
# 4 = enemigo movil 
# 5 = trampa
# 6 = inicio
# 7 = meta

matriz = [
    [0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 2, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 2, 0, 0, 0, 0, 3, 0, 0, 3, 0, 0, 0, 0, 0],
    [0, 0, 2, 0, 0, 0, 2, 3, 7, 4, 0, 0, 4, 0, 0, 2],
    [0, 0, 2, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 2],
    [0, 0, 2, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 2],
    [0, 4, 2, 0, 0, 4, 2, 0, 0, 0, 0, 2, 0, 0, 0, 2],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 5, 2],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 1, 1, 2],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0],
    [6, 0, 0, 5, 5, 0, 0, 5, 0, 0, 0, 2, 0, 4, 0, 0],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

FILAS = len(matriz)
COLUMNAS = len(matriz[0])
ANCHO = COLUMNAS * TAM #Tamaño en pixeles del ancho
ALTO = FILAS * TAM #Tamaño en pixeles del alto

#Tamaño del personaje
ANCHO_PLAYER = 24
ALTO_PLAYER = 30

#Tamaño del enemigo
ANCHO_ENEMIGO = 26
ALTO_ENEMIGO = 26

#Velocidades del personaje 
VELOCIDAD = 6 #6 pixeles por ciclo
VELOCIDAD_ESCALERA = 3 
GRAVEDAD = 1
FUERZA_SALTO = -13 #Negativa debido que tkinter se ocupan numeros más pequeños para moverse hacia arriba en y
MAX_CAIDA = 12

VELOCIDAD_ENEMIGO = 2

#Posición del jugador
player_x = 0
player_y = 0
player_vy = 0 #Velocidad vertical
player_en_suelo = False
player_en_escalera = False

#Teclas presionadas
tecla_izquierda = False
tecla_derecha = False
tecla_arriba = False
tecla_abajo = False

enemigos_x = [] #Posicion X enemigos
enemigos_y = [] #Posición Y enemigos
enemigos_inicio_x = []
enemigos_inicio_y = []
enemigos_direccion = []

juego_activo = True
mensaje = "Flechas: mover/subir/bajar | Espacio: saltar | R: reiniciar"
puntaje = 1000 #Valor en la partida
puntaje_base_mapa = 1000 #Variable del editor
ventana = tk.Tk() # Creación ventana principal
ventana.title("Juego 2D de Plataformas")

musica_activa = False
boton_musica_menu = None
boton_musica_juego = None
imagen_menu = None # Se guardará la imagen

# ------------------------
# RANKING Y PANTALLA FINAL
# ------------------------

ARCHIVO_RANKING = "rankings.txt"

pantalla_final_activa = False
entrada_nombre = None
widgets_finales = []
puntaje_final = 0

menu_principal = None
juego_visible = False

#Procedimiento para limpiar la pantalla final
#Entradas: 
#Salidas: 
def limpiar_widgets_finales():
    global widgets_finales, entrada_nombre

    for i in range(len(widgets_finales)):
        try:
            widgets_finales[i].destroy()
        except:
            pass

    widgets_finales = []
    entrada_nombre = None

#Función para mostrar la pantalla final 
#Entradas: Resultado y que le ocurrio al jugador 
#Salidas: Despliega la pantalla final con todos los widgets
def mostrar_pantalla_final(resultado, motivo):
    global pantalla_final_activa, entrada_nombre, widgets_finales, puntaje_final, juego_activo

    juego_activo = False
    pantalla_final_activa = True
    puntaje_final = puntaje

    limpiar_widgets_finales()

    canvas.delete("all")

    canvas.create_rectangle(
        0,
        0,
        ANCHO,
        ALTO,
        fill="#0f172a",
        outline=""
    )

    canvas.create_rectangle(
        80,
        70,
        ANCHO - 80,
        ALTO - 70,
        fill="#1f2937",
        outline="#facc15",
        width=4
    )

    color_titulo = "#22c55e"

    if resultado == "PERDISTE":
        color_titulo = "#ef4444"

    canvas.create_text(
        ANCHO / 2,
        115,
        text=resultado,
        font=("Arial", 28, "bold"),
        fill=color_titulo
    )

    canvas.create_text(
        ANCHO / 2,
        160,
        text=motivo,
        font=("Arial", 13, "bold"),
        fill="white"
    )

    canvas.create_text(
        ANCHO / 2,
        200,
        text="Puntaje final: " + str(puntaje_final),
        font=("Arial", 15, "bold"),
        fill="#facc15"
    )

    if resultado == "GANASTE":
        canvas.create_text(
            ANCHO / 2,
            245,
            text="Escribe tu nombre:",
            font=("Arial", 12, "bold"),
            fill="white"
        )

        entrada_nombre = tk.Entry(
            ventana,
            font=("Arial", 13, "bold"),
            justify="center"
        )
        entrada_nombre.focus_set() # Colocar curso en el cuadro de texto

        widgets_finales.append(entrada_nombre)

        canvas.create_window(
            ANCHO / 2,
            275,
            window=entrada_nombre,
            width=220,
            height=30
        )

        boton_guardar = tk.Button(
            ventana,
            text="Guardar puntaje",
            font=("Arial", 11, "bold"),
            bg="#22c55e",
            fg="white",
            activebackground="#86efac", #Minetras presiona cambia color
            activeforeground="black",
            relief="flat",
            bd=0,
            padx=15,
            pady=7,
            cursor="hand2",
            command=lambda: guardar_puntaje_final(resultado) #Lambda espera que le de click al boton para ejecutar
        )

        widgets_finales.append(boton_guardar) 

        canvas.create_window(
            ANCHO / 2,
            325,
            window=boton_guardar
        )

    else:
        canvas.create_text(
            ANCHO / 2,
            260,
            text="No se guardó puntaje porque no completaste el nivel.",
            font=("Arial", 11, "bold"),
            fill="#e5e7eb"
        )

    boton_reintentar = tk.Button(
        ventana,
        text="Reintentar",
        font=("Arial", 11, "bold"),
        bg="#2563eb",
        fg="white",
        activebackground="#93c5fd",
        activeforeground="black",
        relief="flat",
        bd=0,
        padx=15,
        pady=7,
        cursor="hand2",
        command=reiniciar_juego
    )

    widgets_finales.append(boton_reintentar)

    canvas.create_window(
        ANCHO / 2 - 90,
        380,
        window=boton_reintentar
    )

    boton_menu = tk.Button(
        ventana,
        text="Menú principal",
        font=("Arial", 11, "bold"),
        bg="#9333ea",
        fg="white",
        activebackground="#c084fc",
        activeforeground="black",
        relief="flat",
        bd=0,
        padx=15,
        pady=7,
        cursor="hand2",
        command=volver_al_menu_principal
    )

    widgets_finales.append(boton_menu)

    canvas.create_window(
        ANCHO / 2 + 90,
        380,
        window=boton_menu
    )

#Función para guardar el puntaje final obtenido
#Entradas: Resultado (Puntaje obtenido)
#Salidas: llama funciones para agregar el puntaje al ranking 
def guardar_puntaje_final(resultado):
    nombre = ""

    if entrada_nombre != None:
        nombre = entrada_nombre.get()

    if nombre == "":
        nombre = "Jugador" #Le asigna jugador si lo dejó vació

    if resultado == "GANASTE":
        agregar_puntaje_ranking(nombre, puntaje_final)

        messagebox.showinfo(
            "Puntaje guardado",
            "El puntaje fue guardado correctamente."
        )

        limpiar_widgets_finales()
        mostrar_rankings()

    else:
        messagebox.showinfo(
            "Partida terminada",
            "No se guardó puntaje porque no completaste el nivel."
        )

        limpiar_widgets_finales()
        mostrar_menu_principal()

#Función para leer los rankings 
#Entradas: 
#Salidas: Lista con los rankings 
def leer_rankings():
    lista = []

    try:
        archivo = open(ARCHIVO_RANKING, "r", encoding="utf-8")

        lineas = archivo.readlines()

        archivo.close()

        for linea in lineas:
            linea = linea.strip() #Quita los espacios o salto de lineas.

            if linea != "":
                partes = linea.split(",") #Divide donde encuentra la ","

                if len(partes) == 2:
                    nombre = partes[0]
                    puntos = int(partes[1])

                    lista.append([nombre, puntos])

    except:
        # Si el archivo no existe todavía, no pasa nada.
        lista = []

    return lista

#Función para ordenar de mayor a menor los rankings
#Entradas: Lista con los puntajes 
#Salidas: Lista ordenada
def ordenar_rankings(lista):
    for i in range(len(lista)):
        for j in range(i + 1, len(lista)):
            if lista[j][1] > lista[i][1]:
                temporal = lista[i]
                lista[i] = lista[j]
                lista[j] = temporal

    return lista

#Función para guardar los rankings 
#Entradas: Lista con rankings ordenados
#Salidas:
def guardar_rankings(lista):
    lista = ordenar_rankings(lista)

    archivo = open(ARCHIVO_RANKING, "w", encoding="utf-8")

    contador = 0

    for i in range(len(lista)):
        if contador < 5: #Coloca los primeros 5
            nombre = lista[i][0]
            puntos = lista[i][1]

            archivo.write(nombre + "," + str(puntos) + "\n")

            contador = contador + 1

    archivo.close()

#Agregar puntaje al ranking
def agregar_puntaje_ranking(nombre, puntos):
    if nombre == "":
        nombre = "Jugador"

    lista = leer_rankings()

    lista.append([nombre, puntos])

    guardar_rankings(lista)

# ======================================================
# MENU PRINCIPAL
# ======================================================

#Procedimiento para ocultar el juego
def ocultar_juego():
    global juego_visible

    marco_superior.pack_forget()
    canvas.pack_forget()
    marco_editor.pack_forget()

    juego_visible = False

#Procedimiento para mostrar el juego
def mostrar_juego():
    global juego_visible

    marco_superior.pack(fill="x")
    canvas.pack()

    juego_visible = True
    actualizar_botones_musica()

#Procedimiento para limpiar el menú
def limpiar_menu():
    global menu_principal, boton_musica_menu

    if menu_principal != None:
        menu_principal.destroy()
        menu_principal = None

    boton_musica_menu = None

#Procedimiento crear menú principal
def mostrar_menu_principal():
    global menu_principal, juego_activo, modo_editor, imagen_menu, boton_musica_menu

    juego_activo = False
    modo_editor = False

    ocultar_juego()
    limpiar_menu()

    menu_principal = tk.Frame(ventana, bg="black")
    menu_principal.pack(fill="both", expand=True)

    # -----------------------------
    # Fondo del menú
    # -----------------------------
    ancho_menu = ANCHO
    alto_menu = ALTO + 70

    canvas_menu = tk.Canvas(
        menu_principal,
        width=ancho_menu,
        height=alto_menu,
        highlightthickness=0,
        bd=0
    )
    canvas_menu.pack(fill="both", expand=True)

    try:
        imagen_menu = tk.PhotoImage(file="fondo.png")
        canvas_menu.create_image(0, 0, image=imagen_menu, anchor="nw")
    except:
        # Si no encuentra la imagen, usa un fondo de color
        canvas_menu.create_rectangle(
            0, 0, ancho_menu, alto_menu,
            fill="#0f172a",
            outline=""
        )

    # Capa oscura encima para que se lean mejor los textos
    canvas_menu.create_rectangle(
        0, 0, ancho_menu, alto_menu,
        fill="black",
        stipple="gray25",
        outline=""
    )

    # ------------------
    # Título y subtítulo
    # ------------------
    canvas_menu.create_text(
        ancho_menu / 2,
        70,
        text="JUEGO 2D DE PLATAFORMAS",
        font=("Arial", 24, "bold"),
        fill="#facc15"
    )

    # ----------------------------------
    # Marco de botones encima del fondo
    # ----------------------------------
    marco_botones_menu = tk.Frame(
        canvas_menu,
        bg="#111827",
        bd=3,
        relief="ridge"
    )

    boton_jugar = tk.Button(
        marco_botones_menu,
        text="Jugar",
        font=("Arial", 14, "bold"),
        bg="#22c55e",
        fg="white",
        activebackground="#86efac",
        activeforeground="black",
        relief="flat",
        bd=0,
        padx=25,
        pady=10,
        width=18,
        cursor="hand2",
        command=iniciar_juego_desde_menu
    )
    boton_jugar.pack(pady=10, padx=20)

    boton_rankings = tk.Button(
        marco_botones_menu,
        text="Rankings",
        font=("Arial", 14, "bold"),
        bg="#3b82f6",
        fg="white",
        activebackground="#93c5fd",
        activeforeground="black",
        relief="flat",
        bd=0,
        padx=25,
        pady=10,
        width=18,
        cursor="hand2",
        command=mostrar_rankings
    )
    boton_rankings.pack(pady=10, padx=20)

    boton_salir = tk.Button(
        marco_botones_menu,
        text="Salir",
        font=("Arial", 14, "bold"),
        bg="#ef4444",
        fg="white",
        activebackground="#fca5a5",
        activeforeground="black",
        relief="flat",
        bd=0,
        padx=25,
        pady=10,
        width=18,
        cursor="hand2",
        command=cerrar_juego
    )
    boton_salir.pack(pady=10, padx=20)

    # Coloca el marco de botones encima del fondo
    canvas_menu.create_window(
        ancho_menu / 2,
        260,
        window=marco_botones_menu
    )

    # Pie de texto
    canvas_menu.create_text(
        ancho_menu / 2,
        alto_menu - 25,
        text="Proyecto Introducción a la programación | Fabián Cambronero Núñez",
        font=("Arial", 10, "bold"),
        fill="#e5e7eb"
    )
    texto_musica = "🔊"

    if musica_activa == False:
        texto_musica = "🔇"

    boton_musica_menu = tk.Button(
        canvas_menu,
        text=texto_musica,
        font=("Arial", 16, "bold"),
        bg="#facc15",
        fg="black",
        activebackground="#fde68a",
        activeforeground="black",
        relief="flat",
        bd=0,
        width=3,
        height=1,
        cursor="hand2",
        command=lambda: cambiar_musica()
    )

    canvas_menu.create_window(
        ancho_menu - 45,
        35,
        window=boton_musica_menu
    )

#Procedimiento para inicializar el juego
def iniciar_juego_desde_menu():
    global puntaje_base_mapa

    # Cuando se juega desde el menú, se calcula el valor del mapa actual.
    puntaje_base_mapa = calcular_puntaje_mapa()

    limpiar_menu()
    mostrar_juego()
    ocultar_botones_editor()
    reiniciar_juego()
    dibujar_mapa()

#Procedimiento para la pantalla de rankings
def mostrar_rankings():
    limpiar_menu()
    ocultar_juego()

    global menu_principal

    menu_principal = tk.Frame(ventana, bg="#111827")
    menu_principal.pack(fill="both", expand=True)

    titulo = tk.Label(
        menu_principal,
        text="RANKINGS",
        font=("Arial", 24, "bold"),
        bg="#111827",
        fg="#facc15"
    )
    titulo.pack(pady=(25, 15))

    marco_tabla = tk.Frame(
        menu_principal,
        bg="#1f2937",
        bd=3,
        relief="ridge"
    )
    marco_tabla.pack(pady=10, padx=20)

    tk.Label(
        marco_tabla,
        text="Posición",
        font=("Arial", 12, "bold"),
        width=12,
        bg="#374151",
        fg="white"
    ).grid(row=0, column=0, padx=2, pady=2)

    tk.Label(
        marco_tabla,
        text="Jugador",
        font=("Arial", 12, "bold"),
        width=16,
        bg="#374151",
        fg="white"
    ).grid(row=0, column=1, padx=2, pady=2)

    tk.Label(
        marco_tabla,
        text="Puntaje",
        font=("Arial", 12, "bold"),
        width=16,
        bg="#374151",
        fg="white"
    ).grid(row=0, column=2, padx=2, pady=2)

    rankings = leer_rankings()
    rankings = ordenar_rankings(rankings)

    if len(rankings) == 0:
        tk.Label(
            marco_tabla,
            text="Todavía no hay puntajes guardados",
            font=("Arial", 11, "bold"),
            width=46,
            bg="#e5e7eb",
            fg="black"
        ).grid(row=1, column=0, columnspan=3, padx=2, pady=8)

    else:
        limite = len(rankings)

        if limite > 5:
            limite = 5

        for i in range(limite): #Coloco los players
            tk.Label(
                marco_tabla,
                text=str(i + 1), #Posicion
                font=("Arial", 11, "bold"),
                width=12,
                bg="#e5e7eb",
                fg="black"
            ).grid(row=i + 1, column=0, padx=2, pady=2)

            tk.Label(
                marco_tabla,
                text=rankings[i][0], #Nombre
                font=("Arial", 11, "bold"),
                width=16,
                bg="#e5e7eb",
                fg="black"
            ).grid(row=i + 1, column=1, padx=2, pady=2)

            tk.Label(
                marco_tabla,
                text=str(rankings[i][1]), # Puntaje
                font=("Arial", 11, "bold"),
                width=16,
                bg="#e5e7eb",
                fg="black"
            ).grid(row=i + 1, column=2, padx=2, pady=2)


    boton_volver = tk.Button(
        menu_principal,
        text="Volver al menú",
        font=("Arial", 13, "bold"),
        bg="#2563eb",
        fg="white",
        activebackground="#93c5fd",
        activeforeground="black",
        relief="flat",
        bd=0,
        padx=20,
        pady=10,
        cursor="hand2",
        command=mostrar_menu_principal
    )
    boton_volver.pack(pady=25)

# ======================================================
# BARRA DE BOTONES
# ======================================================

COLOR_FONDO_BARRA = "#1f2933"
COLOR_BOTON = "#2563eb"
COLOR_BOTON_EDITOR = "#374151"
COLOR_TEXTO = "white"
COLOR_ACTIVO = "#60a5fa"

marco_superior = tk.Frame(ventana, bg=COLOR_FONDO_BARRA)
marco_superior.pack(fill="x")

boton_editar = tk.Button(
    marco_superior,
    text="Editar mapa",
    font=("Arial", 11, "bold"),
    bg=COLOR_BOTON,
    fg=COLOR_TEXTO,
    activebackground=COLOR_ACTIVO,
    activeforeground="black",
    relief="flat",
    bd=0,
    padx=15,
    pady=7,
    cursor="hand2",
    command=lambda: abrir_editor()
)
boton_volver_menu = tk.Button(
    marco_superior,
    text="Menú principal",
    font=("Arial", 11, "bold"),
    bg="#9333ea",
    fg="white",
    activebackground="#c084fc",
    activeforeground="black",
    relief="flat",
    bd=0,
    padx=15,
    pady=7,
    cursor="hand2",
    command=lambda: volver_al_menu_principal()
)
boton_volver_menu.pack(side="left", padx=8, pady=8)
boton_editar.pack(side="left", padx=8, pady=8)

etiqueta_modo = tk.Label(
    marco_superior,
    text="Modo juego",
    font=("Arial", 10, "bold"),
    bg=COLOR_FONDO_BARRA,
    fg="white"
)
etiqueta_modo.pack(side="left", padx=10)

boton_musica_juego = tk.Button(
    marco_superior,
    text="🔊",
    font=("Arial", 16, "bold"),
    bg="#facc15",
    fg="black",
    activebackground="#fde68a",
    activeforeground="black",
    relief="flat",
    bd=0,
    width=3,
    height=1,
    cursor="hand2",
    command=lambda: cambiar_musica()
)
boton_musica_juego.pack(side="right", padx=8, pady=8)


# Este marco no se muestra al inicio.
# Solo aparece cuando se presiona "Editar mapa".
marco_editor = tk.Frame(ventana, bg="#111827")


fila_editor_1 = tk.Frame(marco_editor, bg="#111827")
fila_editor_1.pack(pady=4)

fila_editor_2 = tk.Frame(marco_editor, bg="#111827")
fila_editor_2.pack(pady=4)

#Funcion para crear los botones de las herramientas del editor
#Entradas: Los parametros del boton como el texto, su valor, el color
#Salidas: retorna el boton que necesitamos
def crear_boton_herramienta(marco, texto, valor, color):
    boton = tk.Button(
        marco,
        text=texto,
        font=("Arial", 9, "bold"),
        bg=color,
        fg="white",
        activebackground="#facc15",
        activeforeground="black",
        relief="flat",
        bd=0,
        padx=10,
        pady=6,
        cursor="hand2",
        command=lambda: seleccionar_herramienta(valor)
    )

    boton.pack(side="left", padx=4)
    return boton


boton_borrar = crear_boton_herramienta(fila_editor_1, "Borrar", 0, "#6b7280")
boton_bloque = crear_boton_herramienta(fila_editor_1, "Bloque", 1, "#8b5a2b")
boton_escalera = crear_boton_herramienta(fila_editor_1, "Escalera", 2, "#a16207")
boton_inicio = crear_boton_herramienta(fila_editor_1, "Inicio", 6, "#2563eb")
boton_meta = crear_boton_herramienta(fila_editor_1, "Meta", 7, "#ca8a04")

boton_enemigo_fijo = crear_boton_herramienta(fila_editor_2, "Enemigo fijo", 3, "#dc2626")
boton_enemigo_movil = crear_boton_herramienta(fila_editor_2, "Enemigo móvil", 4, "#7c3aed")
boton_trampa = crear_boton_herramienta(fila_editor_2, "Trampa", 5, "#4B0A07")

boton_guardar = tk.Button(
    fila_editor_2,
    text="Guardar mapa y jugar",
    font=("Arial", 9, "bold"),
    bg="#16a34a",
    fg="white",
    activebackground="#86efac",
    activeforeground="black",
    relief="flat",
    bd=0,
    padx=14,
    pady=6,
    cursor="hand2",
    command=lambda: guardar_mapa_y_jugar()
)
boton_guardar.pack(side="left", padx=4)


canvas = tk.Canvas(
    ventana,
    width=ANCHO,
    height=ALTO,
    bg="lightblue"
)
canvas.pack()

#VARIABLES DEL EDITOR
modo_editor = False
herramienta_editor = 1

# ======================================================
# MUSICA
# ======================================================
#Procedimiento para inicializar la musica 
def iniciar_musica():
    global musica_activa

    try:
        winsound.PlaySound("musica.wav", winsound.SND_FILENAME | winsound.SND_ASYNC | winsound.SND_LOOP)
        musica_activa = True
    except:
        print("No se pudo reproducir la música. Revisa que exista el archivo musica.wav")

#Procedimieto para detener la música
def detener_musica():
    global musica_activa

    winsound.PlaySound(None, winsound.SND_PURGE)
    musica_activa = False

#Procedimiento para actualizar los botones de la musica
def actualizar_botones_musica():
    texto = "🔊"

    if musica_activa == False:
        texto = "🔇"

    try:
        if boton_musica_menu != None:
            boton_musica_menu.config(text=texto)
    except:
        pass

    try:
        if boton_musica_juego != None:
            boton_musica_juego.config(text=texto)
    except:
        pass

#Procedimiento para llamar a las funciones de iniciar musica o detener
def cambiar_musica():
    if musica_activa == True:
        detener_musica()
    else:
        iniciar_musica()

    actualizar_botones_musica()

#--------------------------------------------
# Procedimiento para volver al menu principal
#--------------------------------------------
def volver_al_menu_principal():
    global juego_activo, modo_editor, pantalla_final_activa

    if modo_editor == True: # Si esta en editor no lo deja salir
        messagebox.showwarning(
            "Editor de mapa",
            "No puedes salir al menú mientras estás editando.\n\nPrimero debes guardar el mapa con inicio y meta."
        )
        return

    juego_activo = False
    modo_editor = False
    pantalla_final_activa = False
    #Limpiamos
    limpiar_widgets_finales()
    reiniciar_teclas()
    ocultar_botones_editor()
    mostrar_menu_principal()

# ======================================================
# FUNCIONES DE BUSQUEDA
# ======================================================
#Procedimiento para buscar donde esta el personaje 
def buscar_inicio():
    global player_x, player_y, player_vy
    global player_en_suelo, player_en_escalera

    for fila in range(FILAS):
        for col in range(COLUMNAS):
            if matriz[fila][col] == 6:
                player_x = col * TAM + (TAM - ANCHO_PLAYER) / 2 # Colocar jugador en x
                player_y = fila * TAM + (TAM - ALTO_PLAYER) #Coloca en y pegado al piso
                player_vy = 0 #Reinicia velocidad
                player_en_suelo = False
                player_en_escalera = False

#Procedimiento para buscar a los enemigos moviles
def buscar_enemigos_moviles():
    global enemigos_x, enemigos_y
    global enemigos_inicio_x, enemigos_inicio_y
    global enemigos_direccion

    enemigos_x = []
    enemigos_y = []
    enemigos_inicio_x = []
    enemigos_inicio_y = []
    enemigos_direccion = []

    for fila in range(FILAS):
        for col in range(COLUMNAS):
            if matriz[fila][col] == 4:
                x = col * TAM + 7
                y = (fila + 1) * TAM - ALTO_ENEMIGO

                enemigos_x.append(x)
                enemigos_y.append(y)
                enemigos_inicio_x.append(x)
                enemigos_inicio_y.append(y)
                enemigos_direccion.append(1)


# ======================================================
# VALIDACIONES DEL MAPA
# ======================================================
#Función para revisar si una coordenada se encuentra en el mapa
#Entradas: Fila y col a revisar 
#Salidas: un booleano de True o False si la casilla existe o no
def dentro_del_mapa(fila, col):
    if fila < 0 or fila >= FILAS:
        return False

    if col < 0 or col >= COLUMNAS:
        return False
    return True

#Función para revisar que hay en una celda en especifico en la matriz
#Entradas: fila y col de la coordenada a revisar
#Salidas: Valor de la posicion en la matriz
def obtener_celda(fila, col):
    if dentro_del_mapa(fila, col) == False:
        return 1
    return matriz[fila][col]

#Función para revisar si en una posición hay un bloque
#Entradas. Fila y col de la posición a revisar
#Salidas: un booleano si es bloque o no
def es_bloque(fila, col):
    if obtener_celda(fila, col) == 1:
        return True
    return False

#Función para revisar si en una posición hay una escalera
#Entradas. Fila y col de la posición a revisar
#Salidas: un booleano si es escalera o no
def es_escalera(fila, col):
    if obtener_celda(fila, col) == 2:
        return True
    return False

#Revisa si dos rectangulos se estan chocando
#Entradas: possicion y ancho de los rectangulos
#Salidas: un booelano si se estan tocando 
def rectangulos_chocan(x1, y1, ancho1, alto1, x2, y2, ancho2, alto2):
    if x1 < x2 + ancho2 and x1 + ancho1 > x2 and y1 < y2 + alto2 and y1 + alto1 > y2:
        return True
    return False

#Función para saber si un rectangulo toca el bloque o se sale del mapa
#Entradas: Posicion y ancho y alto
#Salidas. un booleano si el rectangulo puede estar en la casilla
def rectangulo_toca_bloque(x, y, ancho, alto):
    if x < 0:
        return True

    if x + ancho > ANCHO:
        return True

    if y < 0:
        return True

    if y + alto > ALTO:
        return True

    col_izq = int(x // TAM)
    col_der = int((x + ancho - 1) // TAM)
    fila_arriba = int(y // TAM)
    fila_abajo = int((y + alto - 1) // TAM)

    for fila in range(fila_arriba, fila_abajo + 1):
        for col in range(col_izq, col_der + 1):
            if es_bloque(fila, col):
                return True

    return False

#Determina si un jugdor se encuentra en la escalera 
#Entradas: possicion del jugado en x y y
#Salidas: un booleano si se encuentra en una escalera 
def jugador_sobre_escalera():
    centro_x = player_x + ANCHO_PLAYER / 2
    centro_y = player_y + ALTO_PLAYER / 2

    col = int(centro_x // TAM)
    fila = int(centro_y // TAM)

    if es_escalera(fila, col):
        return True

    return False

# ======================================================
# DIBUJO
# ======================================================
#Procedimiento para dibujar el mapa de juego
def dibujar_mapa():
    canvas.delete("all")

    for fila in range(FILAS):
        for col in range(COLUMNAS):
            x1 = col * TAM
            y1 = fila * TAM
            x2 = x1 + TAM
            y2 = y1 + TAM

            valor = matriz[fila][col]

            if valor == 0:
                canvas.create_rectangle(x1, y1, x2, y2, fill="#87ceeb", outline="#9bd3f0")

            elif valor == 1: #Bloques
                canvas.create_rectangle(x1, y1, x2, y2, fill="#6b4f2a", outline="black")
                canvas.create_rectangle(x1, y1, x2, y1 + 8, fill="#8b6f3d", outline="") #Franja superior

            elif valor == 2: #Escaleras
                canvas.create_rectangle(x1, y1, x2, y2, fill="#87ceeb", outline="#9bd3f0")
                canvas.create_rectangle(x1 + 10, y1, x1 + 14, y2, fill="#8b5a2b", outline="")#Verticales
                canvas.create_rectangle(x2 - 14, y1, x2 - 10, y2, fill="#8b5a2b", outline="")
                canvas.create_line(x1 + 10, y1 + 10, x2 - 10, y1 + 10, width=3, fill="#8b5a2b")#Horizontales
                canvas.create_line(x1 + 10, y1 + 22, x2 - 10, y1 + 22, width=3, fill="#8b5a2b")
                canvas.create_line(x1 + 10, y1 + 34, x2 - 10, y1 + 34, width=3, fill="#8b5a2b")

            elif valor == 3: #Enemigo rojo
                canvas.create_rectangle(x1, y1, x2, y2, fill="#87ceeb", outline="#9bd3f0")
                canvas.create_rectangle(x1 + 7, y1 + 7, x2 - 7, y2 - 7, fill="red", outline="black", width=2)
                canvas.create_text(x1 + TAM / 2, y1 + TAM / 2, text="X", fill="white", font=("Arial", 13, "bold"))
            elif valor == 4: #Casilla movil
                canvas.create_rectangle(
                    x1,
                    y1,
                    x2,
                    y2,
                    fill="#87ceeb",
                    outline="#9bd3f0"
    )
            elif valor == 5: #Trampa
                canvas.create_rectangle(x1, y1, x2, y2, fill="#87ceeb", outline="#9bd3f0")
                canvas.create_polygon(x1 + 5, y2, x1 + 15, y1 + 8, x1 + 25, y2, fill="red", outline="black")
                canvas.create_polygon(x1 + 18, y2, x1 + 28, y1 + 8, x1 + 38, y2, fill="red", outline="black")

            elif valor == 6: #Inicio
                canvas.create_rectangle(x1, y1, x2, y2, fill="#87ceeb", outline="#9bd3f0")
                canvas.create_text(x1 + TAM / 2, y1 + TAM / 2, text="INICIO", fill="blue", font=("Arial", 7, "bold"))

            elif valor == 7: #Meta
                canvas.create_rectangle(x1, y1, x2, y2, fill="#87ceeb", outline="#9bd3f0")
                canvas.create_rectangle(x1 + 12, y1 + 5, x1 + 16, y2 - 5, fill="black", outline="")
                canvas.create_polygon(x1 + 16, y1 + 5, x2 - 4, y1 + 14, x1 + 16, y1 + 23, fill="gold", outline="black")
                canvas.create_text(x1 + TAM / 2, y2 - 7, text="META", fill="black", font=("Arial", 7, "bold"))

    dibujar_enemigos_moviles()
    dibujar_player()
    dibujar_mensaje()

#Procedimiento para dibujar al jugador
def dibujar_player():
    canvas.create_oval(
        player_x,
        player_y,
        player_x + ANCHO_PLAYER,
        player_y + ALTO_PLAYER,
        fill="blue",
        outline="black",
        width=2
    )

    canvas.create_text(
        player_x + ANCHO_PLAYER / 2,
        player_y + ALTO_PLAYER / 2,
        text="P",
        fill="white",
        font=("Arial", 14, "bold")
    )

#Procedimiento para dibujar a los enemigos móviles 
def dibujar_enemigos_moviles():
    for i in range(len(enemigos_x)):
        x = enemigos_x[i]
        y = enemigos_y[i]

        canvas.create_oval(
            x,
            y,
            x + ANCHO_ENEMIGO,
            y + ALTO_ENEMIGO,
            fill="purple",
            outline="black",
            width=2
        )

        canvas.create_text(
            x + ANCHO_ENEMIGO / 2,
            y + ALTO_ENEMIGO / 2,
            text="O",
            fill="white",
            font=("Arial", 12, "bold")
        )


def dibujar_mensaje():
    canvas.create_text(
        10,
        10,
        text=mensaje,
        anchor="nw",
        fill="black",
        font=("Arial", 10, "bold")
    )

    canvas.create_text(
        10,
        28,
        text="Puntaje: " + str(puntaje),
        anchor="nw",
        fill="black",
        font=("Arial", 10, "bold")
    )
"""
    if juego_activo == False:
        canvas.create_rectangle(100, 160, 540, 300, fill="white", outline="black", width=3)
        canvas.create_text(320, 210, text=mensaje, fill="black", font=("Arial", 17, "bold"))
        canvas.create_text(320, 250, text="Presiona R para reiniciar", fill="black", font=("Arial", 12, "bold"))"""


# ----------------------
# MOVIMIENTO DEL JUGADOR
# ----------------------
#Procedimiento para poder mover el jugador horizontalmente
def mover_horizontal():
    global player_x

    movimiento = 0

    if tecla_izquierda == True:
        movimiento = movimiento - VELOCIDAD

    if tecla_derecha == True:
        movimiento = movimiento + VELOCIDAD

    player_x = player_x + movimiento
    #Ajustar movimiento cuando choca contra un bloque
    if rectangulo_toca_bloque(player_x, player_y, ANCHO_PLAYER, ALTO_PLAYER):
        if movimiento > 0:
            while rectangulo_toca_bloque(player_x, player_y, ANCHO_PLAYER, ALTO_PLAYER):
                player_x = player_x - 1

        elif movimiento < 0:
            while rectangulo_toca_bloque(player_x, player_y, ANCHO_PLAYER, ALTO_PLAYER):
                player_x = player_x + 1

#Procedimiento para moverse verticalmente
def mover_vertical():
    global player_y, player_vy, player_en_suelo, player_en_escalera

    player_en_escalera = jugador_sobre_escalera()

    if player_en_escalera == True:
        if tecla_arriba == True:
            player_vy = -VELOCIDAD_ESCALERA

        elif tecla_abajo == True:
            player_vy = VELOCIDAD_ESCALERA

        else:
            player_vy = 0

    else:
        player_vy = player_vy + GRAVEDAD

        if player_vy > MAX_CAIDA:
            player_vy = MAX_CAIDA

    player_en_suelo = False
    player_y = player_y + player_vy

    if rectangulo_toca_bloque(player_x, player_y, ANCHO_PLAYER, ALTO_PLAYER):
        if player_vy > 0:
            while rectangulo_toca_bloque(player_x, player_y, ANCHO_PLAYER, ALTO_PLAYER):
                player_y = player_y - 1

            player_en_suelo = True

        elif player_vy < 0:
            while rectangulo_toca_bloque(player_x, player_y, ANCHO_PLAYER, ALTO_PLAYER):
                player_y = player_y + 1

        player_vy = 0

#Procedimiento para saltar
def saltar():
    global player_vy, player_en_suelo

    if juego_activo == False:
        return

    if player_en_suelo == True:
        player_vy = FUERZA_SALTO #Sube
        player_en_suelo = False


# --------------
# ENEMIGO MOVIL
# --------------

#Función para determinar si puedo mover al enemigo
#Entradas: nueva_x y la posicion del enemigo en y
#Salidas: Un booleano
def enemigo_puede_moverse(nuevo_x, enemigo_y):
    if nuevo_x < 0:
        return False

    if nuevo_x + ANCHO_ENEMIGO > ANCHO:
        return False

    # No puede atravesar bloques
    if rectangulo_toca_bloque(nuevo_x, enemigo_y, ANCHO_ENEMIGO, ALTO_ENEMIGO):
        return False

    return True

#Procedimiento para poder mover a los enemigos móviles
def mover_enemigos_moviles():
    global enemigos_x, enemigos_direccion

    for i in range(len(enemigos_x)):
        nuevo_x = enemigos_x[i] + enemigos_direccion[i] * VELOCIDAD_ENEMIGO #Donde se moverá

        if enemigo_puede_moverse(nuevo_x, enemigos_y[i]):
            enemigos_x[i] = nuevo_x
        else:
            enemigos_direccion[i] = enemigos_direccion[i] * -1

# ----------
# RESULTADOS
# ----------
#Función para saber dodne esta la casilla y si se choca con los rectangulos
#Entradas: valor a buscar
#Salida: Un booleano
def jugador_toca_valor(valor_buscado):
    for fila in range(FILAS):
        for col in range(COLUMNAS):
            if matriz[fila][col] == valor_buscado:
                x = col * TAM
                y = fila * TAM

                if rectangulos_chocan(
                    player_x,
                    player_y,
                    ANCHO_PLAYER,
                    ALTO_PLAYER,
                    x,
                    y,
                    TAM,
                    TAM
                ):
                    return True

    return False

#Función para verificar si el jugador toca un enemigo movil 
#Entradas: 
#Salidas: Un booleano si toca al enemigo móvil
def jugador_toca_enemigo_movil():
    for i in range(len(enemigos_x)):
        if rectangulos_chocan(
            player_x,
            player_y,
            ANCHO_PLAYER,
            ALTO_PLAYER,
            enemigos_x[i],
            enemigos_y[i],
            ANCHO_ENEMIGO,
            ALTO_ENEMIGO
        ):
            return True

    return False

#Procedimiento para revisar si el jugador toca algun valor en especifico
def revisar_resultado():
    if jugador_toca_valor(7):
        mostrar_pantalla_final(
            "GANASTE",
            "Llegaste a la meta final."
        )

    elif jugador_toca_valor(3):
        mostrar_pantalla_final(
            "PERDISTE",
            "Tocaste un enemigo fijo."
        )

    elif jugador_toca_valor(5):
        mostrar_pantalla_final(
            "PERDISTE",
            "Caíste en una trampa."
        )

    elif jugador_toca_enemigo_movil():
        mostrar_pantalla_final(
            "PERDISTE",
            "Tocaste un enemigo móvil."
        )


# --------
# TECLADO
# --------

#Eventos por las teclas presionadas
#Entrada: event
#Salida Booleanos
def tecla_presionada(event):
    if pantalla_final_activa == True:
        return
    global tecla_izquierda, tecla_derecha, tecla_arriba, tecla_abajo
    if modo_editor == True:
        return
    if event.keysym == "Left" or event.keysym == "a":
        tecla_izquierda = True

    elif event.keysym == "Right" or event.keysym == "d":
        tecla_derecha = True

    elif event.keysym == "Up" or event.keysym == "w":
        tecla_arriba = True

    elif event.keysym == "Down" or event.keysym == "s":
        tecla_abajo = True

    elif event.keysym == "space":
        saltar()

    elif event.keysym == "r" or event.keysym == "R":
        reiniciar_juego()

#Eventos para cuando me sueltan las teclas
#Entradas: event
#Salidas un booleano
def tecla_soltada(event):
    if pantalla_final_activa == True:
        return
    global tecla_izquierda, tecla_derecha, tecla_arriba, tecla_abajo

    if event.keysym == "Left" or event.keysym == "a":
        tecla_izquierda = False

    elif event.keysym == "Right" or event.keysym == "d":
        tecla_derecha = False

    elif event.keysym == "Up" or event.keysym == "w":
        tecla_arriba = False

    elif event.keysym == "Down" or event.keysym == "s":
        tecla_abajo = False


# ----------------
# FLUJO DEL JUEGO
# ----------------
#Reiniciar las teclas
def reiniciar_teclas():
    global tecla_izquierda, tecla_derecha, tecla_arriba, tecla_abajo
    tecla_izquierda = False
    tecla_derecha = False
    tecla_arriba = False
    tecla_abajo = False

#Procedimiento para reiniciar el juego
def reiniciar_juego():
    global juego_activo, mensaje, puntaje
    global player_vy
    global enemigos_x, enemigos_y, enemigos_direccion
    global pantalla_final_activa
    pantalla_final_activa = False
    limpiar_widgets_finales()

    buscar_inicio()

    for i in range(len(enemigos_x)):
        enemigos_x[i] = enemigos_inicio_x[i]
        enemigos_y[i] = enemigos_inicio_y[i]
        enemigos_direccion[i] = 1

    player_vy = 0
    juego_activo = True
    puntaje = puntaje_base_mapa
    mensaje = "Flechas: mover/subir/bajar | Espacio: saltar | R: reiniciar"
    reiniciar_teclas()
    dibujar_mapa()

#Procedimiento corazón del juego para verificar cada 20 milisegundos el estado
def ciclo_juego():
    global puntaje

    if modo_editor == True:
        ventana.after(20, ciclo_juego)
        return

    if pantalla_final_activa == True:
        ventana.after(20, ciclo_juego)
        return

    if juego_activo == True:
        mover_horizontal()
        mover_vertical()
        mover_enemigos_moviles()
        revisar_resultado()

        # IMPORTANTE:
        # Si revisar_resultado mostró la pantalla final,
        # no se debe volver a dibujar el mapa encima.
        if pantalla_final_activa == True:
            ventana.after(20, ciclo_juego)
            return

        if puntaje > 0:
            puntaje = puntaje - 1

        dibujar_mapa()

    ventana.after(20, ciclo_juego) # Revisar todo cada 20 milisegundos

# ----------------
# EDITOR DE MAPAS
# ----------------
#Función para seleccionar la herramienta correcta
#Entrada: el valor del elemento que deseamos colcoar
#Salida: 
def seleccionar_herramienta(valor):
    global herramienta_editor

    herramienta_editor = valor

    etiqueta_modo.config(
        text="Modo editor | Herramienta: " + nombre_herramienta()
    )

    if modo_editor == True:
        dibujar_editor()

#Creamos un mapa vacio
def crear_mapa_vacio():
    global matriz

    nueva_matriz = []

    for fila in range(FILAS):
        fila_nueva = []

        for col in range(COLUMNAS):
            # Dejamos el suelo listo para que el jugador no caiga al vacío.
            if fila == FILAS - 1:
                fila_nueva.append(1)
            else:
                fila_nueva.append(0)

        nueva_matriz.append(fila_nueva)

    matriz = nueva_matriz

#Procedimiento para abrir el editor
def abrir_editor():
    global modo_editor, juego_activo, pantalla_final_activa

    modo_editor = True
    juego_activo = False
    pantalla_final_activa = False

    limpiar_widgets_finales()
    reiniciar_teclas()
    crear_mapa_vacio()
    limpiar_enemigos_moviles()

    mostrar_botones_editor()
    dibujar_editor()

#Procedimiento para limpiar listas de enemigos 
def limpiar_enemigos_moviles():
    global enemigos_x, enemigos_y
    global enemigos_inicio_x, enemigos_inicio_y
    global enemigos_direccion

    enemigos_x = []
    enemigos_y = []
    enemigos_inicio_x = []
    enemigos_inicio_y = []
    enemigos_direccion = []

#Función para limpiar un valor en especifico 
#Entradas: El valor del elemento que deseamos eliminar
#Salidas: Elimina el elemento de la matriz 
def limpiar_valor_unico(valor):
    for fila in range(FILAS):
        for col in range(COLUMNAS):
            if matriz[fila][col] == valor:
                matriz[fila][col] = 0

#Función para darle click a la casilla en el editor
#Entrada: un evento del mouse
#Salida: Se modifica la matriz
def click_editor(event):
    global matriz

    if modo_editor == False:
        return

    col = int(event.x // TAM)
    fila = int(event.y // TAM)

    if fila < 0 or fila >= FILAS:
        return

    if col < 0 or col >= COLUMNAS:
        return

    # El inicio debe ser único.
    if herramienta_editor == 6:
        limpiar_valor_unico(6)

    # La meta también debe ser única.
    if herramienta_editor == 7:
        limpiar_valor_unico(7)

    matriz[fila][col] = herramienta_editor
    dibujar_editor()

#Cuenta cuantas cosas hay en la matriz dependiendo de el valor 
#Entradas: valor del elemento a buscar
#Salida: la cantidad de veces que se encontro el elemento
def contar_valor(valor):
    cantidad = 0

    for fila in range(FILAS):
        for col in range(COLUMNAS):
            if matriz[fila][col] == valor:
                cantidad = cantidad + 1

    return cantidad

#Calcula el puntaje dependiendo de los objetos que digitaron en el mapa
def calcular_puntaje_mapa():
    puntos = 1000

    for fila in range(FILAS):
        for col in range(COLUMNAS):
            valor = matriz[fila][col]
            # Enemigos y trampas suben el puntaje porque hacen el mapa más difícil.
            if valor == 3:
                puntos = puntos + 100
            elif valor == 4:
                puntos = puntos + 150
            elif valor == 5:
                puntos = puntos + 120

            # Bloques y escaleras bajan el puntaje porque ayudan al jugador.
            elif valor == 1:
                puntos = puntos - 5
            elif valor == 2:
                puntos = puntos - 3
    if puntos < 100:
        puntos = 100
    return puntos

#Valida que el mapa editor se encuentre con los elementos minimos para poder jugar
def validar_mapa_editor():
    cantidad_inicio = contar_valor(6)
    cantidad_meta = contar_valor(7)

    if cantidad_inicio == 0:
        messagebox.showwarning("Mapa incompleto", "Debes colocar un punto de inicio.")
        return False
    if cantidad_meta == 0:
        messagebox.showwarning("Mapa incompleto", "Debes colocar una meta final.")
        return False
    return True

#Procedimiento para guardar el mapa y poder jugarlo
def guardar_mapa_y_jugar():
    global modo_editor, juego_activo, puntaje, pantalla_final_activa
    global player_vy, player_en_suelo, player_en_escalera
    global puntaje_base_mapa

    if modo_editor == False:
        return

    if validar_mapa_editor() == False:
        return

    modo_editor = False
    juego_activo = True
    pantalla_final_activa = False

    # Guardamos cuánto vale este mapa.
    puntaje_base_mapa = calcular_puntaje_mapa()

    # El puntaje de la partida empieza con el valor del mapa.
    puntaje = puntaje_base_mapa

    player_vy = 0
    player_en_suelo = False
    player_en_escalera = False

    limpiar_widgets_finales()
    reiniciar_teclas()
    buscar_inicio()
    buscar_enemigos_moviles()

    ocultar_botones_editor()

    ventana.focus_set()
    canvas.focus_set()

    dibujar_mapa()

#Valor de cada herramienta del editor 
def nombre_herramienta():
    if herramienta_editor == 0:
        return "Borrar"
    elif herramienta_editor == 1:
        return "Bloque"
    elif herramienta_editor == 2:
        return "Escalera"
    elif herramienta_editor == 3:
        return "Enemigo"
    elif herramienta_editor == 4:
        return "Enemigo"
    elif herramienta_editor == 5:
        return "Trampa"
    elif herramienta_editor == 6:
        return "Inicio"
    elif herramienta_editor == 7:
        return "Meta"

    return "Desconocido"

#Mostrar el marco del editor y la etiqueta de editor
def mostrar_botones_editor():
    marco_editor.pack(fill="x")
    etiqueta_modo.config(text="Modo editor")

#Ocultar el marco y pone la etiqueta en modo juego
def ocultar_botones_editor():
    marco_editor.pack_forget()
    etiqueta_modo.config(text="Modo juego")

#Procedimiento para dibujar la interfaz del editor
def dibujar_editor():
    canvas.delete("all")

    canvas.create_rectangle(
        0,
        0,
        ANCHO,
        ALTO,
        fill="#87ceeb",
        outline=""
    )

    for fila in range(FILAS):
        for col in range(COLUMNAS):
            x1 = col * TAM
            y1 = fila * TAM
            x2 = x1 + TAM
            y2 = y1 + TAM

            valor = matriz[fila][col]

            # Fondo de la celda
            canvas.create_rectangle(
                x1,
                y1,
                x2,
                y2,
                fill="#87ceeb",
                outline="#5ba9d6"
            )

            # 1 = bloque
            if valor == 1:
                canvas.create_rectangle(
                    x1,
                    y1,
                    x2,
                    y2,
                    fill="#6b4f2a",
                    outline="black"
                )
                canvas.create_rectangle(
                    x1,
                    y1,
                    x2,
                    y1 + 8,
                    fill="#8b6f3d",
                    outline=""
                )

            # 2 = escalera
            elif valor == 2:
                canvas.create_rectangle(
                    x1 + 10,
                    y1,
                    x1 + 14,
                    y2,
                    fill="#8b5a2b",
                    outline=""
                )
                canvas.create_rectangle(
                    x2 - 14,
                    y1,
                    x2 - 10,
                    y2,
                    fill="#8b5a2b",
                    outline=""
                )
                canvas.create_line(
                    x1 + 10,
                    y1 + 10,
                    x2 - 10,
                    y1 + 10,
                    width=3,
                    fill="#8b5a2b"
                )
                canvas.create_line(
                    x1 + 10,
                    y1 + 22,
                    x2 - 10,
                    y1 + 22,
                    width=3,
                    fill="#8b5a2b"
                )
                canvas.create_line(
                    x1 + 10,
                    y1 + 34,
                    x2 - 10,
                    y1 + 34,
                    width=3,
                    fill="#8b5a2b"
                )

            # 3 = enemigo fijo
            elif valor == 3:
                canvas.create_rectangle(
                    x1 + 7,
                    y1 + 7,
                    x2 - 7,
                    y2 - 7,
                    fill="red",
                    outline="black",
                    width=2
                )
                canvas.create_text(
                    x1 + TAM / 2,
                    y1 + TAM / 2,
                    text="X",
                    fill="white",
                    font=("Arial", 13, "bold")
                )

            # 4 = enemigo móvil
            elif valor == 4:
                canvas.create_oval(
                    x1 + 7,
                    y1 + 7,
                    x2 - 7,
                    y2 - 7,
                    fill="purple",
                    outline="black",
                    width=2
                )
                canvas.create_text(
                    x1 + TAM / 2,
                    y1 + TAM / 2,
                    text="O",
                    fill="white",
                    font=("Arial", 13, "bold")
                )

            # 5 = trampa
            elif valor == 5:
                canvas.create_rectangle(
                    x1,
                    y1,
                    x2,
                    y2,
                    fill="#87ceeb",
                    outline="#5ba9d6"
                )
                canvas.create_polygon(
                    x1 + 5,
                    y2 - 5,
                    x1 + 15,
                    y1 + 8,
                    x1 + 25,
                    y2 - 5,
                    fill="red",
                    outline="black"
                )
                canvas.create_polygon(
                    x1 + 18,
                    y2 - 5,
                    x1 + 28,
                    y1 + 8,
                    x1 + 38,
                    y2 - 5,
                    fill="red",
                    outline="black"
                )

            # 6 = inicio
            elif valor == 6:
                canvas.create_oval(
                    x1 + 6,
                    y1 + 6,
                    x2 - 6,
                    y2 - 6,
                    fill="blue",
                    outline="black",
                    width=2
                )
                canvas.create_text(
                    x1 + TAM / 2,
                    y1 + TAM / 2,
                    text="INICIO",
                    fill="white",
                    font=("Arial", 7, "bold")
                )

            # 7 = meta
            elif valor == 7:
                canvas.create_rectangle(
                    x1 + 12,
                    y1 + 5,
                    x1 + 16,
                    y2 - 5,
                    fill="black",
                    outline=""
                )
                canvas.create_polygon(
                    x1 + 16,
                    y1 + 5,
                    x2 - 4,
                    y1 + 14,
                    x1 + 16,
                    y1 + 23,
                    fill="gold",
                    outline="black"
                )
                canvas.create_text(
                    x1 + TAM / 2,
                    y2 - 7,
                    text="META",
                    fill="black",
                    font=("Arial", 7, "bold")
                )

    canvas.create_rectangle(
        5,
        5,
        360,
        55,
        fill="white",
        outline="black"
    )

    canvas.create_text(
        15,
        15,
        text="MODO EDITOR",
        anchor="nw",
        fill="black",
        font=("Arial", 10, "bold")
    )

    canvas.create_text(
        15,
        33,
        text="Herramienta: " + nombre_herramienta() + " | Puntaje base: " + str(calcular_puntaje_mapa()),
        anchor="nw",
        fill="black",
        font=("Arial", 9, "bold")
    )

#Procedimiento para cerrar el juego
def cerrar_juego():
    detener_musica()
    ventana.destroy()
ventana.protocol("WM_DELETE_WINDOW", cerrar_juego)

# --------
# INICIAR
# --------

buscar_inicio()
buscar_enemigos_moviles()

ventana.bind("<KeyPress>", tecla_presionada)
ventana.bind("<KeyRelease>", tecla_soltada)
canvas.bind("<Button-1>", click_editor)

iniciar_musica()
mostrar_menu_principal()
ciclo_juego()
ventana.mainloop()