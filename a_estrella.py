import heapq  # Importa la biblioteca heapq para usar una cola de prioridad

# Calcula la distancia de Manhattan entre dos puntos
def distancia_manhattan(origen, destino):
    return abs(origen[0] - destino[0]) + abs(destino[1] - origen[1])

# Implementa el algoritmo A* para encontrar el camino más corto
def a_estrella(matriz, inicio, fin):
    filas, columnas = len(matriz), len(matriz[0])  # Obtiene el tamaño de la matriz
    abierta = []  # Lista de nodos por evaluar (cola de prioridad)
    heapq.heappush(abierta, (0 + distancia_manhattan(inicio, fin), 0, inicio))  # Añade el nodo inicial a la cola
    cerrada = set()  # Conjunto de nodos ya evaluados
    padres = {}  # almacena el camino
    g_coste = {inicio: 0}  # Diccionario para almacenar el coste desde el inicio hasta un nodo

    while abierta:  # Mientras haya nodos por evaluar
        _, coste_actual, nodo_actual = heapq.heappop(abierta)  # Extrae el nodo con el menor coste estimado

        if nodo_actual in cerrada:
            continue  # Si el nodo ya ha sido evaluado, pasa al siguiente

        cerrada.add(nodo_actual)  # Marca el nodo actual como evaluado

        if nodo_actual == fin:  # Si se ha alcanzado el nodo destino
            camino = []  # Lista para almacenar el camino encontrado
            while nodo_actual in padres:
                camino.append(nodo_actual)  # Añade el nodo actual al camino
                nodo_actual = padres[nodo_actual]  # Retrocede al nodo padre
            camino.append(inicio)  # Añade el nodo inicial al camino
            return camino[::-1]  # Retorna el camino en orden correcto

        vecinos = obtener_vecinos(matriz, nodo_actual)  # Obtiene los vecinos del nodo actual

        for vecino in vecinos:
            if vecino in cerrada:
                continue  # Si el vecino ya ha sido evaluado, pasa al siguiente

            coste_tentativo = coste_actual + 1  # Calcula el coste desde el inicio hasta el vecino

            if vecino not in g_coste or coste_tentativo < g_coste[vecino]:
                g_coste[vecino] = coste_tentativo  # Actualiza el coste del vecino
                f_coste = coste_tentativo + distancia_manhattan(vecino, fin)  # Calcula el coste total estimado
                heapq.heappush(abierta, (f_coste, coste_tentativo, vecino))  # Añade el vecino a la cola
                padres[vecino] = nodo_actual  # Actualiza el nodo padre del vecino

    return None  # Retorna None si no se encuentra un camino

# Obtiene los vecinos de un nodo dado en la matriz
def obtener_vecinos(matriz, nodo):
    x, y = nodo  # Coordenadas del nodo actual
    vecinos = []  # Lista para almacenar los vecinos
    movimientos = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Posibles movimientos (arriba, abajo, izquierda, derecha)

    for movimiento in movimientos:
        nx, ny = x + movimiento[0], y + movimiento[1]  # Calcula las coordenadas del vecino
        if 0 <= nx < len(matriz) and 0 <= ny < len(matriz[0]):  # Verifica que las coordenadas estén dentro de la matriz
            if matriz[nx][ny] != 'E':  # Verifica que el vecino no sea un obstáculo
                vecinos.append((nx, ny))  # Añade el vecino a la lista

    return vecinos  # Retorna la lista de vecinos

# Imprime la matriz con el camino encontrado
def imprimir_matriz(matriz, camino, inicio, fin):
    matriz_copia = [fila[:] for fila in matriz]  # Crea una copia de la matriz original
    for x, y in camino:
        if (x, y) != inicio and (x, y) != fin:  # Si el nodo no es el inicio o el fin
            matriz_copia[x][y] = '*'  # Marca el nodo como parte del camino
    matriz_copia[inicio[0]][inicio[1]] = 'P'  # Marca el punto de inicio
    matriz_copia[fin[0]][fin[1]] = 'D'  # Marca el punto de destino
    for fila in matriz_copia:
        print(' '.join(fila))  # Imprime cada fila de la matriz

# Función principal del programa
def main():
    filas, columnas = 10, 10  # Define el tamaño de la matriz
    matriz = [['.' for _ in range(columnas)] for _ in range(filas)]  # Crea una matriz de 10x10 llena de puntos transitables

    obstaculos = []  # Lista para almacenar las coordenadas de los obstáculos
    while True:
        coord = input("Introduce las coordenadas del obstáculo (formato x,y) o 'fin' para terminar: ")  # Pide al usuario las coordenadas de los obstáculos
        if coord.lower() == 'fin':
            break  # Si el usuario escribe 'fin', termina el bucle
        x, y = map(int, coord.split(','))  # Divide la entrada en dos partes y las convierte en enteros
        obstaculos.append((x, y))  # Añade las coordenadas del obstáculo a la lista

    for obstaculo in obstaculos:
        matriz[obstaculo[0]][obstaculo[1]] = 'E'  # Marca los obstáculos en la matriz

    coordenadas_inicio = input("Introduce las coordenadas del punto de partida (formato x,y): ")  # Pide al usuario las coordenadas del punto de partida
    x_inicio, y_inicio = coordenadas_inicio.split(',')  # Divide la entrada en dos partes
    inicio = (int(x_inicio), int(y_inicio))  # Convierte las partes en enteros y crea una tupla

    coordenadas_fin = input("Introduce las coordenadas del punto de destino (formato x,y): ")  # Pide al usuario las coordenadas del punto de destino
    x_fin, y_fin = coordenadas_fin.split(',')  # Divide la entrada en dos partes
    fin = (int(x_fin), int(y_fin))  # Convierte las partes en enteros y crea una tupla

    camino = a_estrella(matriz, inicio, fin)  # Ejecuta el algoritmo A* para encontrar el camino

    if camino:
        imprimir_matriz(matriz, camino, inicio, fin)  # Si se encuentra un camino, lo imprime
    else:
        print("No se encontró un camino")  # Si no se encuentra un camino, muestra un mensaje de error

if __name__ == "__main__":
    main()  # Ejecuta la función principal si el archivo se ejecuta directamente
