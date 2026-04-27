import tkinter as tk
from tkinter import messagebox

# ======================================================
# JUEGO 2D DE PLATAFORMAS
# Sin clases, sin diccionarios, sin sets
# Usa matriz, listas, variables globales, funciones y Tkinter
# ======================================================

TAM = 40

# 0 = vacio
# 1 = bloque / plataforma
# 2 = escalera
# 3 = enemigo estatico
# 4 = enemigo movil inicial
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
    [6, 0, 0, 0, 5, 0, 0, 0, 5, 0, 0, 2, 0, 4, 0, 0],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

FILAS = len(matriz)
COLUMNAS = len(matriz[0])
ANCHO = COLUMNAS * TAM
ALTO = FILAS * TAM

ANCHO_PLAYER = 24
ALTO_PLAYER = 30

ANCHO_ENEMIGO = 26
ALTO_ENEMIGO = 26

VELOCIDAD = 6
VELOCIDAD_ESCALERA = 3
GRAVEDAD = 1
FUERZA_SALTO = -13
MAX_CAIDA = 12

VELOCIDAD_ENEMIGO = 2

player_x = 0
player_y = 0
player_vy = 0
player_en_suelo = False
player_en_escalera = False

tecla_izquierda = False
tecla_derecha = False
tecla_arriba = False
tecla_abajo = False

enemigos_x = []
enemigos_y = []
enemigos_inicio_x = []
enemigos_inicio_y = []
enemigos_direccion = []

juego_activo = True
mensaje = "Flechas: mover/subir/bajar | Espacio: saltar | R: reiniciar"
puntaje = 1000

ventana = tk.Tk()
ventana.title("Juego 2D de Plataformas - Movimiento suave")

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
    text="✏ Editar mapa",
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
boton_editar.pack(side="left", padx=8, pady=8)

etiqueta_modo = tk.Label(
    marco_superior,
    text="Modo juego",
    font=("Arial", 10, "bold"),
    bg=COLOR_FONDO_BARRA,
    fg="white"
)
etiqueta_modo.pack(side="left", padx=10)


# Este marco NO se muestra al inicio.
# Solo aparece cuando se presiona "Editar mapa".
marco_editor = tk.Frame(ventana, bg="#111827")


fila_editor_1 = tk.Frame(marco_editor, bg="#111827")
fila_editor_1.pack(pady=4)

fila_editor_2 = tk.Frame(marco_editor, bg="#111827")
fila_editor_2.pack(pady=4)


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
boton_trampa = crear_boton_herramienta(fila_editor_2, "Trampa", 5, "#111827")

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

# 0 = borrar / vacío
# 1 = bloque
# 2 = escalera
# 3 = enemigo fijo
# 4 = enemigo móvil
# 5 = trampa
# 6 = inicio
# 7 = meta

# ======================================================
# FUNCIONES DE BUSQUEDA
# ======================================================

def buscar_inicio():
    global player_x, player_y, player_vy
    global player_en_suelo, player_en_escalera

    for fila in range(FILAS):
        for col in range(COLUMNAS):
            if matriz[fila][col] == 6:
                player_x = col * TAM + (TAM - ANCHO_PLAYER) / 2
                player_y = fila * TAM + (TAM - ALTO_PLAYER)
                player_vy = 0
                player_en_suelo = False
                player_en_escalera = False


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

def dentro_del_mapa(fila, col):
    if fila < 0 or fila >= FILAS:
        return False

    if col < 0 or col >= COLUMNAS:
        return False

    return True


def obtener_celda(fila, col):
    if dentro_del_mapa(fila, col) == False:
        return 1

    return matriz[fila][col]


def es_bloque(fila, col):
    if obtener_celda(fila, col) == 1:
        return True

    return False


def es_escalera(fila, col):
    if obtener_celda(fila, col) == 2:
        return True

    return False


def rectangulos_chocan(x1, y1, ancho1, alto1, x2, y2, ancho2, alto2):
    if x1 < x2 + ancho2 and x1 + ancho1 > x2 and y1 < y2 + alto2 and y1 + alto1 > y2:
        return True

    return False


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

            elif valor == 1:
                canvas.create_rectangle(x1, y1, x2, y2, fill="#6b4f2a", outline="black")
                canvas.create_rectangle(x1, y1, x2, y1 + 8, fill="#8b6f3d", outline="")

            elif valor == 2:
                canvas.create_rectangle(x1, y1, x2, y2, fill="#87ceeb", outline="#9bd3f0")
                canvas.create_rectangle(x1 + 10, y1, x1 + 14, y2, fill="#8b5a2b", outline="")
                canvas.create_rectangle(x2 - 14, y1, x2 - 10, y2, fill="#8b5a2b", outline="")
                canvas.create_line(x1 + 10, y1 + 10, x2 - 10, y1 + 10, width=3, fill="#8b5a2b")
                canvas.create_line(x1 + 10, y1 + 22, x2 - 10, y1 + 22, width=3, fill="#8b5a2b")
                canvas.create_line(x1 + 10, y1 + 34, x2 - 10, y1 + 34, width=3, fill="#8b5a2b")

            elif valor == 3:
                canvas.create_rectangle(x1, y1, x2, y2, fill="#87ceeb", outline="#9bd3f0")
                canvas.create_rectangle(x1 + 7, y1 + 7, x2 - 7, y2 - 7, fill="red", outline="black", width=2)
                canvas.create_text(x1 + TAM / 2, y1 + TAM / 2, text="X", fill="white", font=("Arial", 13, "bold"))
            elif valor == 4:
                canvas.create_rectangle(
                    x1,
                    y1,
                    x2,
                    y2,
                    fill="#87ceeb",
                    outline="#9bd3f0"
    )
            elif valor == 5:
                canvas.create_rectangle(x1, y1, x2, y2, fill="#222222", outline="black")
                canvas.create_polygon(x1 + 5, y2 - 5, x1 + 15, y1 + 8, x1 + 25, y2 - 5, fill="red", outline="black")
                canvas.create_polygon(x1 + 18, y2 - 5, x1 + 28, y1 + 8, x1 + 38, y2 - 5, fill="red", outline="black")

            elif valor == 6:
                canvas.create_rectangle(x1, y1, x2, y2, fill="#87ceeb", outline="#9bd3f0")
                canvas.create_text(x1 + TAM / 2, y1 + TAM / 2, text="INICIO", fill="blue", font=("Arial", 7, "bold"))

            elif valor == 7:
                canvas.create_rectangle(x1, y1, x2, y2, fill="#87ceeb", outline="#9bd3f0")
                canvas.create_rectangle(x1 + 12, y1 + 5, x1 + 16, y2 - 5, fill="black", outline="")
                canvas.create_polygon(x1 + 16, y1 + 5, x2 - 4, y1 + 14, x1 + 16, y1 + 23, fill="gold", outline="black")
                canvas.create_text(x1 + TAM / 2, y2 - 7, text="META", fill="black", font=("Arial", 7, "bold"))

    dibujar_enemigos_moviles()
    dibujar_player()
    dibujar_mensaje()


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

    if juego_activo == False:
        canvas.create_rectangle(100, 160, 540, 300, fill="white", outline="black", width=3)
        canvas.create_text(320, 210, text=mensaje, fill="black", font=("Arial", 17, "bold"))
        canvas.create_text(320, 250, text="Presiona R para reiniciar", fill="black", font=("Arial", 12, "bold"))


# ======================================================
# MOVIMIENTO DEL JUGADOR
# ======================================================

def mover_horizontal():
    global player_x

    movimiento = 0

    if tecla_izquierda == True:
        movimiento = movimiento - VELOCIDAD

    if tecla_derecha == True:
        movimiento = movimiento + VELOCIDAD

    player_x = player_x + movimiento

    if rectangulo_toca_bloque(player_x, player_y, ANCHO_PLAYER, ALTO_PLAYER):
        if movimiento > 0:
            while rectangulo_toca_bloque(player_x, player_y, ANCHO_PLAYER, ALTO_PLAYER):
                player_x = player_x - 1

        elif movimiento < 0:
            while rectangulo_toca_bloque(player_x, player_y, ANCHO_PLAYER, ALTO_PLAYER):
                player_x = player_x + 1


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


def saltar():
    global player_vy, player_en_suelo

    if juego_activo == False:
        return

    if player_en_suelo == True:
        player_vy = FUERZA_SALTO
        player_en_suelo = False


# ======================================================
# ENEMIGO MOVIL
# ======================================================

def enemigo_puede_moverse(nuevo_x, enemigo_y):
    if nuevo_x < 0:
        return False

    if nuevo_x + ANCHO_ENEMIGO > ANCHO:
        return False

    # No puede atravesar bloques
    if rectangulo_toca_bloque(nuevo_x, enemigo_y, ANCHO_ENEMIGO, ALTO_ENEMIGO):
        return False

    # Revisa si hay piso debajo del enemigo
    centro_x = nuevo_x + ANCHO_ENEMIGO / 2
    abajo_y = enemigo_y + ALTO_ENEMIGO + 1

    col = int(centro_x // TAM)
    fila = int(abajo_y // TAM)

    if es_bloque(fila, col):
        return True

    return False


def mover_enemigos_moviles():
    global enemigos_x, enemigos_direccion

    for i in range(len(enemigos_x)):
        nuevo_x = enemigos_x[i] + enemigos_direccion[i] * VELOCIDAD_ENEMIGO

        if enemigo_puede_moverse(nuevo_x, enemigos_y[i]):
            enemigos_x[i] = nuevo_x
        else:
            enemigos_direccion[i] = enemigos_direccion[i] * -1


# ======================================================
# RESULTADOS
# ======================================================

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


def revisar_resultado():
    global juego_activo, mensaje

    if juego_activo == False:
        return

    if jugador_toca_valor(7):
        juego_activo = False
        mensaje = "¡Ganaste! Puntaje: " + str(puntaje)
        return

    if jugador_toca_valor(3):
        juego_activo = False
        mensaje = "Perdiste: tocaste enemigo rojo."
        return

    if jugador_toca_valor(5):
        juego_activo = False
        mensaje = "Perdiste: tocaste una trampa."
        return

    if jugador_toca_enemigo_movil():
        juego_activo = False
        mensaje = "Perdiste: tocaste enemigo morado."
        return


# ======================================================
# TECLADO
# ======================================================

def tecla_presionada(event):
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


def tecla_soltada(event):
    global tecla_izquierda, tecla_derecha, tecla_arriba, tecla_abajo

    if event.keysym == "Left" or event.keysym == "a":
        tecla_izquierda = False

    elif event.keysym == "Right" or event.keysym == "d":
        tecla_derecha = False

    elif event.keysym == "Up" or event.keysym == "w":
        tecla_arriba = False

    elif event.keysym == "Down" or event.keysym == "s":
        tecla_abajo = False


# ======================================================
# FLUJO DEL JUEGO
# ======================================================

def reiniciar_teclas():
    global tecla_izquierda, tecla_derecha, tecla_arriba, tecla_abajo

    tecla_izquierda = False
    tecla_derecha = False
    tecla_arriba = False
    tecla_abajo = False


def reiniciar_juego():
    global juego_activo, mensaje, puntaje
    global player_vy
    global enemigos_x, enemigos_y, enemigos_direccion

    buscar_inicio()

    for i in range(len(enemigos_x)):
        enemigos_x[i] = enemigos_inicio_x[i]
        enemigos_y[i] = enemigos_inicio_y[i]
        enemigos_direccion[i] = 1

    player_vy = 0
    juego_activo = True
    puntaje = 1000
    mensaje = "Flechas: mover/subir/bajar | Espacio: saltar | R: reiniciar"
    reiniciar_teclas()
    dibujar_mapa()


def ciclo_juego():
    global puntaje

    if modo_editor == True:
        ventana.after(20, ciclo_juego)
        return

    if juego_activo == True:
        mover_horizontal()
        mover_vertical()
        mover_enemigos_moviles()
        revisar_resultado()

        if puntaje > 0:
            puntaje = puntaje - 1

    dibujar_mapa()

    ventana.after(20, ciclo_juego)

# ======================================================
# EDITOR DE MAPAS
# ======================================================

def seleccionar_herramienta(valor):
    global herramienta_editor

    herramienta_editor = valor

    etiqueta_modo.config(
        text="Modo editor | Herramienta: " + nombre_herramienta()
    )

    if modo_editor == True:
        dibujar_editor()


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


def abrir_editor():
    global modo_editor, juego_activo

    modo_editor = True
    juego_activo = False

    reiniciar_teclas()
    crear_mapa_vacio()
    limpiar_enemigos_moviles()

    mostrar_botones_editor()
    dibujar_editor()


def limpiar_enemigos_moviles():
    global enemigos_x, enemigos_y
    global enemigos_inicio_x, enemigos_inicio_y
    global enemigos_direccion

    enemigos_x = []
    enemigos_y = []
    enemigos_inicio_x = []
    enemigos_inicio_y = []
    enemigos_direccion = []


def limpiar_valor_unico(valor):
    for fila in range(FILAS):
        for col in range(COLUMNAS):
            if matriz[fila][col] == valor:
                matriz[fila][col] = 0


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


def contar_valor(valor):
    cantidad = 0

    for fila in range(FILAS):
        for col in range(COLUMNAS):
            if matriz[fila][col] == valor:
                cantidad = cantidad + 1

    return cantidad


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


def guardar_mapa_y_jugar():
    global modo_editor, juego_activo, puntaje

    if modo_editor == False:
        return

    if validar_mapa_editor() == False:
        return

    modo_editor = False
    juego_activo = True

    puntaje = calcular_puntaje_mapa()

    reiniciar_teclas()
    buscar_inicio()
    buscar_enemigos_moviles()

    ocultar_botones_editor()
    dibujar_mapa()


def nombre_herramienta():
    if herramienta_editor == 0:
        return "Borrar"
    elif herramienta_editor == 1:
        return "Bloque"
    elif herramienta_editor == 2:
        return "Escalera"
    elif herramienta_editor == 3:
        return "Enemigo fijo"
    elif herramienta_editor == 4:
        return "Enemigo móvil"
    elif herramienta_editor == 5:
        return "Trampa"
    elif herramienta_editor == 6:
        return "Inicio"
    elif herramienta_editor == 7:
        return "Meta"

    return "Desconocido"

def mostrar_botones_editor():
    marco_editor.pack(fill="x")
    etiqueta_modo.config(text="Modo editor")


def ocultar_botones_editor():
    marco_editor.pack_forget()
    etiqueta_modo.config(text="Modo juego")

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
                    fill="#222222",
                    outline="black"
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

# ======================================================
# INICIO
# ======================================================

buscar_inicio()
buscar_enemigos_moviles()
dibujar_mapa()

ventana.bind("<KeyPress>", tecla_presionada)
ventana.bind("<KeyRelease>", tecla_soltada)

canvas.bind("<Button-1>", click_editor)

ciclo_juego()

ventana.mainloop()