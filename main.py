import tetris
import gamelib
ESPERA_DESCENDER = 8

#Las siguientes funciones se encargan de la parte grafica del tetris.

def dibujar_grilla():
    '''
    Dibuja las lineas que representan la superficie/grilla del juego.
    '''
    for lineas in range(0, 541, 30):
        gamelib.draw_line(0, lineas, 270, lineas, fill = "grey")
    for lineas in range(0, 271, 30):
        gamelib.draw_line(lineas, 0, lineas, 540, fill = "grey")

def dibujar_pieza_actual(juego):
    '''
    Dibuja las celdas de la pieza que cae y el jugador controla.
    '''
    superficie, pieza_actual = juego
    if tetris.esta_en_posicion_valida(superficie, pieza_actual) and not tetris.terminado(juego):
        for x, y in pieza_actual:
            gamelib.draw_rectangle(1 + x * 30, 1 + y * 30, 29 + x * 30, 29 + y * 30, outline = "pink", fill = "pink" )

def dibujar_piezas_consolidadas(juego):
    '''
    Dibuja las celdas ocupadas por piezas que ya consolidaron la superficie.
    '''
    superficie, pieza_centrada = juego
    for y, fila in enumerate(superficie):
        for x, columna in enumerate(fila):
            if tetris.hay_superficie(juego, x, y):
                gamelib.draw_rectangle(1 + x * 30, 1 + y * 30, 29 + x * 30, 29 + y * 30, outline = "purple", fill = "purple" )

def dibujar_siguiente_pieza(siguiente_pieza):
    '''
    Dibuja a la derecha la pieza proxima a aparecer,
    '''
    gamelib.draw_text("SIGUIENTE PIEZA:", 400, 30, size = 15)
    for x, y in siguiente_pieza:
        gamelib.draw_rectangle(361 + x * 30, 61 + y * 30, 389 + x * 30, 89 + y * 30, outline = "pink", fill = "pink" )

def dibujar_puntaje(score):
    '''
    Dibuja el puntaje actual del jugador.
    '''
    gamelib.draw_text(f"PUNTAJE: {score}", 400, 400, size = 15)

def dibujar_mejores_jugadores(nuevas_puntuaciones):
    '''
    Recibe una lista con las puntuaciones actualizadas y muestra en la pantalla
    los 10 mejores puntajes ordenados de mayor a menor.
    '''
    while gamelib.loop(fps=30):
        gamelib.draw_begin()
        gamelib.draw_text("Top 10 TETRIS MVP's", 250, 20, size = 20, fill = "orange")
        for i in range(len(nuevas_puntuaciones)):
            gamelib.draw_text(f"{nuevas_puntuaciones[i][0]} --> {nuevas_puntuaciones[i][1]}", 250, 50 + (50 * i), size = 15, fill = "orange")
        gamelib.draw_end()

#Las siguientes funciones se encargan del procesamiento de archivos.

def leer_movimiento(archivo):
    '''
    Procesa el archivo "teclas.txt" y devuelve un diccionario con las teclas
    como claves y sus respectivas acciones como valores.
    '''
    diccionario = {}
    with open(archivo, "r", encoding="utf8") as controles:
        lineas = controles.readlines()
        for linea in lineas:
            if len(linea) > 1:
                palabras = linea.rstrip('\n').split(" = ")
                for palabra in palabras:
                    if palabras[0] not in diccionario:
                        diccionario[palabras[0]] = palabras[1]
    return diccionario

def leer_puntuaciones(archivo):
    '''
    Procesa el archivo y devuelve una lista ordenada de todas las puntuaciones
    junto a su jugador correspondiente de mayor a menor.
    '''
    top_puntuaciones= []
    with open(archivo, "r", encoding = "utf8") as puntuaciones:
        puntajes = puntuaciones.readlines()
        if puntajes == []:
            return top_puntuaciones
        else:
            for puntaje in puntajes:
                puntos, jugador = puntaje.split(", ")
                top_puntuaciones.append((int(puntos), jugador.rstrip("\n")))
    return sorted(top_puntuaciones)[::-1]

def actualizar_puntuaciones(lista, score, jugador):
    '''
    Si la lista pasada por parametro tiene entre [0, 10) elementos agrega al final
    el puntaje junto al jugador correspondiente.
    En caso que la lista tenga 10 elementos y el ultimo puntaje (justamente el minimo)
    sea menor al puntaje actual(score), entonces el ultimo elemento es eliminado y se
    agrega el nuevo puntaje y jugador.
    Finalmente devuelve la lista sobre la que opera.
    '''
    if 0 <= len(lista) < 10:
        lista.append((int(score), jugador))

    if len(lista) == 10 and lista[-1][0] < score:
        lista.pop()
        lista.append((int(score), jugador))

    return lista

def reescribir_puntuaciones(lista, archivo):
    '''
    Crea una lista vacia e itera los indices de la lista pasada por parametro
    para crear cadenas con los puntos y jugadores que luego serán agregados a la lista
    creada, finalmente se escribe en el archivo la lista creada en un principio.
    '''
    puntajes_a_escribir = []
    with open(archivo, "w", encoding = "utf8") as puntuaciones:
        for i in range(len(lista)):
            linea = ""
            linea += str(lista[i][0]) + ", "
            linea += lista[i][1] + "\n"
            puntajes_a_escribir.append(linea)
            continue

        puntuaciones.writelines(puntajes_a_escribir)
    return

def main():
    gamelib.title("TETRIS")
    gamelib.resize(540, 540)

    # Inicializar el estado del juego

    siguiente_pieza = tetris.generar_pieza()
    juego = tetris.crear_juego(tetris.generar_pieza())
    score = 0
    timer_bajar = ESPERA_DESCENDER

    while gamelib.loop(fps=30):
        gamelib.draw_begin()
        dibujar_grilla()
        dibujar_pieza_actual(juego)
        dibujar_piezas_consolidadas(juego)
        dibujar_siguiente_pieza(siguiente_pieza)
        dibujar_puntaje(score)
        if tetris.terminado(juego):
            dibujar_mejores_jugadores(nuevas_puntuaciones)
        gamelib.draw_end()

        for event in gamelib.get_events():
          if not event:
              break
          if event.type == gamelib.EventType.KeyPress:
              tecla = event.key
              controles = leer_movimiento("teclas.txt")
              # Actualizar el juego, según la tecla presionada
              if tecla in controles:
                  if tecla == "d":
                     juego = tetris.mover(juego, tetris.DERECHA)
                  elif tecla == "a":
                      juego = tetris.mover(juego, tetris.IZQUIERDA)
                  elif tecla == "s":
                      juego, cambiar_pieza = tetris.avanzar(juego, siguiente_pieza)
                  elif tecla == "w":
                      juego = tetris.rotar(juego, tetris.rotaciones)
                  elif tecla == "g":
                      tetris.guardar_partida(juego, "partida_guardada.txt")
                  elif tecla == "c":
                      juego = tetris.cargar_partida("partida_guardada.txt")
                  elif tecla == "Escape":
                      return

        timer_bajar -= 1
        if timer_bajar == 0 and not tetris.terminado(juego):
            score += 5
            timer_bajar = ESPERA_DESCENDER
            # Descender la pieza automáticamente
            juego_actual, cambiar_pieza = tetris.avanzar(juego, siguiente_pieza)
            if cambiar_pieza:
                siguiente_pieza = tetris.generar_pieza()
            juego = juego_actual

            if tetris.terminado(juego):
                jugador = gamelib.input("Ingrese nombre de jugador: ")
                top_puntuaciones = leer_puntuaciones("puntuaciones.txt")
                actualizar_puntuaciones(top_puntuaciones, score, jugador)
                reescribir_puntuaciones(top_puntuaciones, "puntuaciones.txt")
                nuevas_puntuaciones = leer_puntuaciones("puntuaciones.txt")

gamelib.init(main)
