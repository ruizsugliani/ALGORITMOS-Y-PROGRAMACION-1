import random
ANCHO_JUEGO, ALTO_JUEGO = 9, 18
IZQUIERDA, DERECHA = -1, 1
CUBO = 0
Z = 1
S = 2
I = 3
L = 4
L_INV = 5
T = 6

def leer_piezas(archivo):
    '''
    Procesa el archivo 'piezas.txt' y devuelve una lista de tuplas con las piezas
    y rotaciones.
    '''
    with open(archivo, "r") as piezas:
        lista_de_tuplas = []
        for linea in piezas:
            pieza = []
            linea = linea.rstrip("\n").split(" ")
            for cadena in linea:
                coordenadas = []
                cadena = cadena.split(";")
                for subcadena in cadena:
                    coordenada = []
                    subcadena = subcadena.split(",")
                    for ubicacion in subcadena:
                        ubicacion = int(ubicacion)
                        coordenada.append(ubicacion)
                    coordenadas.append(tuple(coordenada))
                pieza.append(tuple(coordenadas))
            lista_de_tuplas.append(tuple(pieza))
    return lista_de_tuplas

def generar_pieza(pieza=None):
    '''
    Utiliza la lista de tuplas obtenida por la funcion leer_piezas(archivo)
    crea una nueva lista con las coordenadas de la pieza por default y devuelve
    la tupla de tuplas de una de las piezas al azar, si se le indica el parametro,
    genera la pieza indicada.
    '''
    lista_de_tuplas = leer_piezas("piezas.txt")
    piezas_default = []
    for i in range(len(lista_de_tuplas)):
        piezas_default.append(lista_de_tuplas[i][0])

    if pieza == None:
        return random.choice(piezas_default)

    elif pieza == CUBO:
        return piezas_default[0]

    elif pieza == Z:
        return piezas_default[1]

    elif pieza == S:
        return piezas_default[2]

    elif pieza == I:
        return piezas_default[3]

    elif pieza == L:
        return piezas_default[4]

    elif pieza == -L:
        return piezas_default[5]

    elif pieza == T:
        return piezas_default[6]

def asignar_rotaciones():
    '''
    A partir de las piezas capaces de ser rotadas (todas menos el cubo), devuelve
    un diccionario el cual tiene R1 -> R2 -> R3 -> R4 -> R1 (una rotacion como clave
    y la que le sigue como valor, en el caso de la ultima rotacion, su valor es la primera
    rotacion)
    '''
    lista_de_tuplas = leer_piezas("piezas.txt")
    dict = {}
    for tupla in lista_de_tuplas:
        if len(tupla) == 1:
            dict[tupla[0]] = tupla[0]

        if len(tupla) == 2:
            dict[tupla[0]] = tupla[1]
            dict[tupla[1]] = tupla[0]

        if len(tupla) == 4:
            dict[tupla[0]] = tupla[1]
            dict[tupla[1]] = tupla[2]
            dict[tupla[2]] = tupla[3]
            dict[tupla[3]] = tupla[0]
    return dict

rotaciones = asignar_rotaciones()

def trasladar_pieza(pieza, dx, dy):
    """
    Traslada la pieza de su posición actual a (posicion + (dx, dy)).

    La pieza está representada como una tupla de posiciones ocupadas,
    donde cada posición ocupada es una tupla (x, y).
    Por ejemplo para la pieza ( (0, 0), (0, 1), (0, 2), (0, 3) ) y
    el desplazamiento dx=2, dy=3 se devolverá la pieza
    ( (2, 3), (2, 4), (2, 5), (2, 6) ).
    """
    movimiento = list(pieza)
    for i in range(len(movimiento)):
        x, y = movimiento[i]
        movimiento[i] = x + dx, y + dy
    return tuple(movimiento)

def rotar(juego, rotaciones):
    '''
    Devuelve un nuevo estado de juego con la pieza rotada o el mismo estado
    recibido si la rotacion no se puede realizar.
    '''
    superficie, pieza_actual = juego
    pieza_ordenada = sorted(pieza_actual)
    primer_posicion = pieza_ordenada[0]
    pieza_en_origen = trasladar_pieza(pieza_ordenada, tupla_a_restar(primer_posicion)[0], tupla_a_restar(primer_posicion)[1])
    siguiente_rotacion = rotaciones[pieza_en_origen]
    pieza_rotada = trasladar_pieza(siguiente_rotacion, primer_posicion[0], primer_posicion[1])
    if esta_en_posicion_valida(superficie, pieza_rotada):
        juego = superficie, pieza_rotada
    return juego

def tupla_a_restar(tupla):
    '''
    Transforma en numero negativo al X e Y de la tupla pasada por parametro.
    '''
    tupla = list(tupla)
    for i in range(len(tupla)):
        tupla[i] = -tupla[i]
    return(tuple(tupla))

def crear_juego(pieza_inicial):
    """
    Crea un nuevo juego de Tetris.

    El parámetro pieza_inicial es una pieza obtenida mediante
    pieza.generar_pieza. Ver documentación de esa función para más información.

    El juego creado debe cumplir con lo siguiente:
    - La grilla está vacía: hay_superficie da False para todas las ubicaciones
    - La pieza actual está arriba de todo, en el centro de la pantalla.
    - El juego no está terminado: terminado(juego) da False

    Que la pieza actual esté arriba de todo significa que la coordenada Y de
    sus posiciones superiores es 0 (cero).
    """
    pieza_centrada = trasladar_pieza(pieza_inicial, ANCHO_JUEGO // 2, 0)
    superficie = [["VACIA"]*ANCHO_JUEGO for _ in range(ALTO_JUEGO)]
    juego = superficie, pieza_centrada
    return juego

def guardar_partida(juego, ruta):
    '''
    Guarda el estado actual del juego(superficie y pieza_actual) en la ruta.
    '''
    superficie, pieza_actual = juego
    with open(ruta, "w", encoding = "utf8") as guardado:
        p_actual = []
        for coordenadas in pieza_actual:
            p_actual.append(str(coordenadas))
        guardado.writelines(p_actual)
        guardado.write("\n")

        for fila in superficie:
            for i in range(len(fila)):
                guardado.write(fila[i] + ", ")
            guardado.write("\n")
    return

def cargar_partida(ruta):
    '''
    Carga el estado de juego guardado anteriormente(superficie, pieza_actual),
    el cual fue guardado en la ruta pasada por parametro.
    '''
    lineas = []
    superficie = []
    pieza_actual = []
    with open(ruta, "r", encoding = "utf8") as partida_guardada:
        lineas = partida_guardada.readlines()

        for i in range(len(lineas)):
            if lineas[i] == lineas[0]:
                pieza = lineas[i].rstrip("\n")
                coords = []
                for caracter in pieza:
                    if caracter.isdigit():
                        coords.append(int(caracter))
                        coord1 = tuple(coords[0:2])
                        coord2 = tuple(coords[2:4])
                        coord3 = tuple(coords[4:6])
                        coord4 = tuple(coords[6:8])
                        pieza_actual = (coord1, coord2, coord3, coord4)

            else:
                fila = lineas[i].rstrip("\n").rstrip(",")
                fila = fila.split(", ")
                superficie.append(fila)

    juego = superficie, pieza_actual
    return juego

def dimensiones(juego):
    """
    Devuelve las dimensiones de la grilla del juego como una tupla (ancho, alto).
    """
    dimensiones = (ANCHO_JUEGO, ALTO_JUEGO)
    return dimensiones

def pieza_actual(juego):
    """
    Devuelve una tupla de tuplas (x, y) con todas las posiciones de la
    grilla ocupadas por la pieza actual.

    Se entiende por pieza actual a la pieza que está cayendo y todavía no
    fue consolidada con la superficie.

    La coordenada (0, 0) se refiere a la posición que está en la esquina
    superior izquierda de la grilla.
    """
    superficie, pieza_centrada = juego
    pieza_actual = pieza_centrada
    return pieza_actual

def hay_superficie(juego, x, y):
    """
    Devuelve True si la celda (x, y) está ocupada por la superficie consolidada.

    La coordenada (0, 0) se refiere a la posición que está en la esquina
    superior izquierda de la grilla.
    """
    superficie, pieza_actual = juego

    if superficie[y][x] == "OCUPADA":
        return superficie[y][x] == "OCUPADA"
    return superficie[y][x] == "OCUPADA"

def esta_en_posicion_valida(superficie, pieza):
    """
    Devuelve True si todas las posiciones de pieza están en
    posiciones válidas. Lo cual indica que todas las posiciones están dentro de
    los límites y que ninguna de las posiciones esté tocando la superficie.
    La posición x, y es válida si:
    - x es mayor o igual a 0 y menor a ANCHO_JUEGO
    - y es mayor o igual a 0 y menor a ALTO_JUEGO
    - La celda está vacía (superficie[y][x] == 0)
    """
    for x, y in pieza:
        if 0 <= x < ANCHO_JUEGO and 0 <= y < ALTO_JUEGO and superficie[y][x] == "VACIA":
            continue
        return False
    return True

def mover(juego, direccion):
    """
    Mueve la pieza actual hacia la derecha o izquierda, si es posible.
    Devuelve un nuevo estado de juego con la pieza movida o el mismo estado
    recibido si el movimiento no se puede realizar.

    El parámetro direccion debe ser una de las constantes DERECHA o IZQUIERDA.
    """
    superficie, pieza_actual = juego
    if direccion == IZQUIERDA:
        mover_izq = trasladar_pieza(pieza_actual, -1, 0)
        if esta_en_posicion_valida(superficie, mover_izq):
            juego = superficie, mover_izq
        return juego

    if direccion == DERECHA:
        mover_der = trasladar_pieza(pieza_actual, 1, 0)
        if esta_en_posicion_valida(superficie, mover_der):
            juego = superficie, mover_der

        return juego

def eliminar_lineas_completas(superficie):
    """
    Devuelve una nueva superficie que no tenga las líneas completas.Y baja una
    posición a las demas.
    """
    nueva_superficie = []
    for l in range(ALTO_JUEGO):
        if superficie[l] == ["OCUPADA"] * ANCHO_JUEGO:
            nueva_superficie.insert(0, ["VACIA"] * ANCHO_JUEGO)
        else:
            nueva_superficie.insert(l, superficie[l])
    return nueva_superficie

def avanzar(juego, siguiente_pieza):
    """
    Avanza al siguiente estado de juego a partir del estado actual.

    Devuelve una tupla (juego_nuevo, cambiar_pieza) donde el primer valor
    es el nuevo estado del juego y el segundo valor es un booleano que indica
    si se debe cambiar la siguiente_pieza (es decir, se consolidó la pieza
    actual con la superficie).

    Avanzar el estado del juego significa:
     - Descender una posición la pieza actual.
     - Si al descender la pieza no colisiona con la superficie, simplemente
       devolver el nuevo juego con la pieza en la nueva ubicación.
     - En caso contrario, se debe
       - Consolidar la pieza actual con la superficie.
       - Eliminar las líneas que se hayan completado.
       - Cambiar la pieza actual por siguiente_pieza.

    Si se debe agregar una nueva pieza, se utilizará la pieza indicada en
    el parámetro siguiente_pieza. El valor del parámetro es una pieza obtenida
    llamando a generar_pieza().

    **NOTA:** Hay una simplificación respecto del Tetris real a tener en
    consideración en esta función: la próxima pieza a agregar debe entrar
    completamente en la grilla para poder seguir jugando, si al intentar
    incorporar la nueva pieza arriba de todo en el medio de la grilla se
    pisara la superficie, se considerará que el juego está terminado.

    Si el juego está terminado (no se pueden agregar más piezas), la funcion no hace nada,
    se debe devolver el mismo juego que se recibió.
    """
    superficie, pieza_actual = juego
    descender = trasladar_pieza(pieza_actual, 0, 1)

    if terminado(juego):
        return juego, False

    if esta_en_posicion_valida(superficie, descender):
        juego = superficie, descender
        return juego, False

    if not esta_en_posicion_valida(superficie, descender):
        for x, y in pieza_actual:
            superficie[y][x] = "OCUPADA"
        superficie_alterada = eliminar_lineas_completas(superficie)
        respawn_pieza = trasladar_pieza(siguiente_pieza, ANCHO_JUEGO // 2, 0)
        juego = superficie_alterada, respawn_pieza
        return juego, True

def terminado(juego):
    """
    Devuelve True si el juego terminó, es decir no se pueden agregar
    nuevas piezas, o False si se puede seguir jugando.
    """
    superficie, pieza_centrada = juego
    if esta_en_posicion_valida(superficie, pieza_centrada):
        return False
    return True
