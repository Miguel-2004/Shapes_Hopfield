# ============================================================
# RED HOPFIELD
# Reconocimiento de los numeros 1, 2 y 4
# Matrices de 8 filas x 5 columnas = 40 neuronas
# ============================================================

FILAS = 8
COLUMNAS = 5
N = FILAS * COLUMNAS


# ------------------------------------------------------------
# PATRONES QUE APRENDERA LA RED
# ------------------------------------------------------------

numero1 = [
    [-1, -1,  1, -1, -1],
    [-1,  1,  1, -1, -1],
    [-1, -1,  1, -1, -1],
    [-1, -1,  1, -1, -1],
    [-1, -1,  1, -1, -1],
    [-1, -1,  1, -1, -1],
    [-1, -1,  1, -1, -1],
    [-1, -1, -1, -1, -1]
]

numero2 = [
    [-1,  1,  1,  1, -1],
    [ 1, -1, -1, -1,  1],
    [-1, -1, -1, -1,  1],
    [-1, -1,  1,  1, -1],
    [-1,  1, -1, -1, -1],
    [ 1, -1, -1, -1, -1],
    [ 1,  1,  1,  1,  1],
    [-1, -1, -1, -1, -1]
]

numero4 = [
    [ 1, -1, -1,  1, -1],
    [ 1, -1, -1,  1, -1],
    [ 1, -1, -1,  1, -1],
    [ 1,  1,  1,  1,  1],
    [-1, -1, -1,  1, -1],
    [-1, -1, -1,  1, -1],
    [-1, -1, -1,  1, -1],
    [-1, -1, -1, -1, -1]
]


# ------------------------------------------------------------
# Convierte una matriz 8x5 en un vector de 40 elementos
# ------------------------------------------------------------

def convertir_a_vector(matriz):
    vector = []

    for i in range(FILAS):
        for j in range(COLUMNAS):
            vector.append(matriz[i][j])

    return vector


# ------------------------------------------------------------
# Convierte un vector de 40 elementos a matriz 8x5
# ------------------------------------------------------------

def convertir_a_matriz(vector):
    matriz = []

    posicion = 0

    for i in range(FILAS):
        fila = []

        for j in range(COLUMNAS):
            fila.append(vector[posicion])
            posicion = posicion + 1

        matriz.append(fila)

    return matriz


# ------------------------------------------------------------
# Mostrar una figura
# ------------------------------------------------------------

def mostrar_figura(vector):
    matriz = convertir_a_matriz(vector)

    print("+----------+")

    for i in range(FILAS):

        print("|", end="")

        for j in range(COLUMNAS):

            if matriz[i][j] == 1:
                print("██", end="")
            else:
                print("  ", end="")

        print("|")

    print("+----------+")


# ------------------------------------------------------------
# CREAR MATRIZ DE PESOS
# ------------------------------------------------------------

def entrenar_red(patrones):

    pesos = []

    # Crear matriz N x N llena de ceros
    for i in range(N):

        fila = []

        for j in range(N):
            fila.append(0)

        pesos.append(fila)

    # Calcular cada peso
    for i in range(N):

        for j in range(N):

            if i == j:

                pesos[i][j] = 0

            else:

                suma = 0

                for p in range(len(patrones)):

                    suma = suma + patrones[p][i] * patrones[p][j]

                pesos[i][j] = suma

    return pesos


# ------------------------------------------------------------
# ACTUALIZAR LA RED HOPFIELD
# ------------------------------------------------------------

def actualizar_red(entrada, pesos):

    estado = entrada[:]

    iteracion = 0
    max_iteraciones = 20
    estable = False

    while estable == False and iteracion < max_iteraciones:

        nuevo_estado = []

        for i in range(N):

            suma = 0

            for j in range(N):

                suma = suma + pesos[i][j] * estado[j]

            # Funcion signo
            if suma > 0:

                nuevo_estado.append(1)

            elif suma < 0:

                nuevo_estado.append(-1)

            else:

                # Si la suma es cero conserva su valor anterior
                nuevo_estado.append(estado[i])

        # Comprobar si ya no hubo cambios
        estable = True

        for i in range(N):

            if estado[i] != nuevo_estado[i]:
                estable = False

        estado = nuevo_estado

        iteracion = iteracion + 1

        print("\nIteracion", iteracion)
        mostrar_figura(estado)

    return estado


# ------------------------------------------------------------
# Comparar el resultado contra los patrones almacenados
# ------------------------------------------------------------

def reconocer(resultado, patrones):

    nombres = ["1", "2", "4"]

    mejor_patron = -1
    menor_error = N + 1

    for p in range(len(patrones)):

        errores = 0

        for i in range(N):

            if resultado[i] != patrones[p][i]:
                errores = errores + 1

        if errores < menor_error:

            menor_error = errores
            mejor_patron = p

    print("\n===================================")
    print("RESULTADO DEL RECONOCIMIENTO")
    print("===================================")

    if mejor_patron != -1:

        print("La red reconoce el numero:", nombres[mejor_patron])
        print("Diferencias con el patron:", menor_error)

    else:

        print("No fue posible reconocer la figura.")


# ------------------------------------------------------------
# Permite introducir manualmente una figura.
#
# Usuario escribe:
#
# 1 = negro
# 0 = blanco
#
# Ejemplo:
#
# 00100
# 01100
# ...
# ------------------------------------------------------------

def leer_figura():

    vector = []

    print("\nIntroduce una figura de 8 filas y 5 columnas.")
    print("Usa:")
    print("1 = negro")
    print("0 = blanco")
    print()

    fila_actual = 0

    while fila_actual < FILAS:

        texto = input("Fila " + str(fila_actual + 1) + ": ")

        valido = True

        if len(texto) != COLUMNAS:

            valido = False

        else:

            for caracter in texto:

                if caracter != "0" and caracter != "1":
                    valido = False

        if valido == True:

            for caracter in texto:

                if caracter == "1":
                    vector.append(1)

                else:
                    vector.append(-1)

            fila_actual = fila_actual + 1

        else:

            print("ERROR: debes introducir exactamente 5 valores 0 o 1.")

    return vector


# ============================================================
# PROGRAMA PRINCIPAL
# ============================================================

patron1 = convertir_a_vector(numero1)
patron2 = convertir_a_vector(numero2)
patron4 = convertir_a_vector(numero4)

patrones = [
    patron1,
    patron2,
    patron4
]


print("===================================")
print("        RED NEURONAL HOPFIELD")
print("===================================")

print("\nPatrones almacenados:")

print("\nNumero 1:")
mostrar_figura(patron1)

print("\nNumero 2:")
mostrar_figura(patron2)

print("\nNumero 4:")
mostrar_figura(patron4)


# Entrenamiento
print("\nEntrenando red Hopfield...")

pesos = entrenar_red(patrones)

print("Entrenamiento terminado.")


# Leer figura alterada
entrada = leer_figura()

print("\nFigura introducida:")
mostrar_figura(entrada)


# Recuperar patron
print("\nIniciando recuperacion...")

resultado = actualizar_red(entrada, pesos)


# Resultado final
print("\nFigura recuperada:")

mostrar_figura(resultado)


# Identificar numero
reconocer(resultado, patrones)