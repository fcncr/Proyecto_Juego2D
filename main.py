#Importación tKinter
import tkinter as tk

#------------------
#VARIABLES GLOBALES
#------------------
TAM=40


# Matriz lógica del mapa
# 0 = vacío
# 1 = bloque / plataforma
# 2 = escalera
# 3 = enemigo tipo 1
# 4 = enemigo tipo 2
# 5 = trampa
# 6 = inicio del jugador
# 7 = meta

matriz = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0],
    [0, 0, 0, 1, 1, 1, 0, 0, 3, 0, 2, 0, 0, 4, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 1, 1, 1],
    [0, 0, 5, 0, 0, 0, 0, 1, 1, 1, 2, 0, 0, 0, 0],
    [0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 3, 0, 0, 5, 0, 2, 0, 0, 0, 0],
    [6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 4, 0, 0],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

player_fila = 0
player_col = 0

#-----------------
#VENTANA PRINCIPAL
#-----------------
ventana = tk.Tk()
ventana.title("Juego 2D de Plataformas")

canvas = tk.Canvas(
    ventana,
    width=len(matriz[0]) * TAM,
    height=len(matriz) * TAM,
    bg="lightblue"
)

canvas.pack()


#-----------------
#FUNCIONES
#-----------------

def buscar_inicio():
    global player_fila, player_col

    for fila in range(len(matriz)):
        for col in range(len(matriz[fila])):
            if matriz[fila][col] == 6:
                player_fila = fila
                player_col = col


def dibujar_mapa():
    canvas.delete("all")

    # Fondo del cielo
    canvas.create_rectangle(
        0,
        0,
        len(matriz[0]) * TAM,
        len(matriz) * TAM,
        fill="#87ceeb",
        outline=""
    )

    for fila in range(len(matriz)):
        for col in range(len(matriz[fila])):
            x1 = col * TAM
            y1 = fila * TAM
            x2 = x1 + TAM
            y2 = y1 + TAM

            valor = matriz[fila][col]

            # 1 = bloque / plataforma
            if valor == 1:
                canvas.create_rectangle(
                    x1,
                    y1,
                    x2,
                    y2,
                    fill="#6b4f2a",
                    outline="#3e2f1c",
                    width=2
                )

                # detalle superior del bloque
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
                # postes verticales
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

                # peldaños
                canvas.create_line(
                    x1 + 10,
                    y1 + 8,
                    x2 - 10,
                    y1 + 8,
                    width=3,
                    fill="#8b5a2b"
                )

                canvas.create_line(
                    x1 + 10,
                    y1 + 20,
                    x2 - 10,
                    y1 + 20,
                    width=3,
                    fill="#8b5a2b"
                )

                canvas.create_line(
                    x1 + 10,
                    y1 + 32,
                    x2 - 10,
                    y1 + 32,
                    width=3,
                    fill="#8b5a2b"
                )

            # 3 = enemigo tipo 1
            elif valor == 3:
                canvas.create_rectangle(
                    x1 + 6,
                    y1 + 8,
                    x2 - 6,
                    y2 - 4,
                    fill="#d62828",
                    outline="black",
                    width=2
                )

                canvas.create_text(
                    x1 + TAM / 2,
                    y1 + TAM / 2,
                    text="X",
                    font=("Arial", 13, "bold"),
                    fill="white"
                )

            # 4 = enemigo tipo 2
            elif valor == 4:
                canvas.create_oval(
                    x1 + 6,
                    y1 + 6,
                    x2 - 6,
                    y2 - 6,
                    fill="#7b2cbf",
                    outline="black",
                    width=2
                )

                # ojos
                canvas.create_oval(
                    x1 + 14,
                    y1 + 15,
                    x1 + 18,
                    y1 + 19,
                    fill="white",
                    outline=""
                )

                canvas.create_oval(
                    x1 + 24,
                    y1 + 15,
                    x1 + 28,
                    y1 + 19,
                    fill="white",
                    outline=""
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

                # picos de la trampa
                canvas.create_polygon(
                    x1 + 4, y2 - 4,
                    x1 + 12, y1 + 8,
                    x1 + 20, y2 - 4,
                    fill="red",
                    outline="black"
                )

                canvas.create_polygon(
                    x1 + 20, y2 - 4,
                    x1 + 28, y1 + 8,
                    x1 + 36, y2 - 4,
                    fill="red",
                    outline="black"
                )

            # 6 = inicio
            elif valor == 6:
                canvas.create_text(
                    x1 + TAM / 2,
                    y1 + TAM / 2,
                    text="INICIO",
                    font=("Arial", 7, "bold"),
                    fill="#0b3d91"
                )

            # 7 = meta
            elif valor == 7:
                # poste
                canvas.create_rectangle(
                    x1 + 14,
                    y1 + 4,
                    x1 + 18,
                    y2 - 4,
                    fill="black",
                    outline=""
                )

                # bandera
                canvas.create_polygon(
                    x1 + 18, y1 + 5,
                    x2 - 4, y1 + 12,
                    x1 + 18, y1 + 20,
                    fill="gold",
                    outline="black"
                )
    
                canvas.create_text(
                    x1 + TAM / 2,
                    y2 - 6,
                    text="META",
                    font=("Arial", 7, "bold"),
                    fill="black"
                )
    dibujar_player()
def dibujar_player():
    x1 = player_col * TAM + 8
    y1 = player_fila * TAM + 6
    x2 = x1 + TAM - 16
    y2 = y1 + TAM - 10

    # cuerpo del jugador
    canvas.create_rectangle(
        x1,
        y1,
        x2,
        y2,
        fill="#2f80ed",
        outline="black",
        width=2
    )

    # ojo izquierdo
    canvas.create_oval(
        x1 + 6,
        y1 + 7,
        x1 + 10,
        y1 + 11,
        fill="white",
        outline=""
    )

    # ojo derecho
    canvas.create_oval(
        x1 + 15,
        y1 + 7,
        x1 + 19,
        y1 + 11,
        fill="white",
        outline=""
    )
def puede_moverse(fila, col):
    # Revisa si se sale por arriba o por abajo
    if fila < 0 or fila >= len(matriz):
        return False

    # Revisa si se sale por izquierda o derecha
    if col < 0 or col >= len(matriz[0]):
        return False

    # No puede atravesar bloques
    if matriz[fila][col] == 1:
        return False

    return True


def esta_en_escalera(fila, col):
    if fila < 0 or fila >= len(matriz):
        return False

    if col < 0 or col >= len(matriz[0]):
        return False

    if matriz[fila][col] == 2:
        return True

    return False


def tiene_piso(fila, col):
    # Si está en escalera, la escalera lo sostiene
    if matriz[fila][col] == 2:
        return True

    # Si está en la última fila, no cae más
    if fila + 1 >= len(matriz):
        return True

    # Si abajo hay un bloque, está sobre piso
    if matriz[fila + 1][col] == 1:
        return True

    return False


def revisar_celda_actual():
    valor = matriz[player_fila][player_col]

    if valor == 7:
        print("Ganaste, llegaste a la meta.")

    elif valor == 5:
        print("Perdiste, tocaste una trampa.")

    elif valor == 3:
        print("Perdiste, tocaste un enemigo tipo 1.")

    elif valor == 4:
        print("Perdiste, tocaste un enemigo tipo 2.")


def aplicar_gravedad():
    global player_fila

    # Mientras no tenga piso y no esté en escalera, cae
    while tiene_piso(player_fila, player_col) == False:
        nueva_fila = player_fila + 1

        if puede_moverse(nueva_fila, player_col):
            player_fila = nueva_fila
            revisar_celda_actual()
        else:
            break


def mover(event):
    global player_fila, player_col

    nueva_fila = player_fila
    nueva_col = player_col

    if event.keysym == "Left":
        nueva_col -= 1

    elif event.keysym == "Right":
        nueva_col += 1

    elif event.keysym == "Up":
        # Solo puede subir si está en una escalera
        if esta_en_escalera(player_fila, player_col):
            nueva_fila -= 1

    elif event.keysym == "Down":
        # Puede bajar si está en escalera
        if esta_en_escalera(player_fila, player_col):
            nueva_fila += 1

        # También puede bajar si la escalera está justo debajo
        elif player_fila + 1 < len(matriz) and esta_en_escalera(player_fila + 1, player_col):
            nueva_fila += 1

    else:
        return

    if puede_moverse(nueva_fila, nueva_col):
        player_fila = nueva_fila
        player_col = nueva_col

    revisar_celda_actual()
    aplicar_gravedad()
    dibujar_mapa()
#--------
#INICIO
#--------
buscar_inicio()
dibujar_mapa()

ventana.bind("<Key>", mover)

ventana.mainloop()