import heapq

# Clase que representa el mapa
class Mapa:
    def __init__(self, filas, columnas):
        self.filas = filas
        self.columnas = columnas
        self.matriz = [['.' for _ in range(columnas)] for _ in range(filas)]
        self.inicio = None
        self.fin = None

    def agregar_obstaculo(self, x, y):
        if self.es_accesible(x, y):
            self.matriz[x][y] = 'E'

    def quitar_obstaculo(self, x, y):
        if self.matriz[x][y] == 'E':
            self.matriz[x][y] = '.'

    def es_accesible(self, x, y):
        return 0 <= x < self.filas and 0 <= y < self.columnas and self.matriz[x][y] != 'E'

    def establecer_inicio(self, x, y):
        self.inicio = (x, y)

    def establecer_fin(self, x, y):
        self.fin = (x, y)

    def imprimir_mapa(self, camino=None):
        matriz_copia = [fila[:] for fila in self.matriz]
        if camino:
            for x, y in camino:
                if (x, y) != self.inicio and (x, y) != self.fin:
                    matriz_copia[x][y] = '*'
            matriz_copia[self.inicio[0]][self.inicio[1]] = 'P'
            matriz_copia[self.fin[0]][self.fin[1]] = 'D'

        for fila in matriz_copia:
            print(' '.join(fila))


# Clase que representa la calculadora de rutas
class CalculadoraRutas:
    def __init__(self, mapa):
        self.mapa = mapa

    def distancia_manhattan(self, origen, destino):
        return abs(origen[0] - destino[0]) + abs(destino[1] - origen[1])

    def obtener_vecinos(self, nodo):
        x, y = nodo
        vecinos = []
        movimientos = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for movimiento in movimientos:
            nx, ny = x + movimiento[0], y + movimiento[1]
            if self.mapa.es_accesible(nx, ny):
                vecinos.append((nx, ny))
        return vecinos

    def encontrar_camino(self):
        inicio, fin = self.mapa.inicio, self.mapa.fin
        abierta = []
        heapq.heappush(abierta, (0 + self.distancia_manhattan(inicio, fin), 0, inicio))
        cerrada = set()
        padres = {}
        g_coste = {inicio: 0}

        while abierta:
            f_costo, coste_actual, nodo_actual = heapq.heappop(abierta)
            if nodo_actual in cerrada:
                continue

            cerrada.add(nodo_actual)

            if nodo_actual == fin:
                camino = []
                while nodo_actual in padres:
                    camino.append(nodo_actual)
                    nodo_actual = padres[nodo_actual]
                camino.append(inicio)
                return camino[::-1]

            vecinos = self.obtener_vecinos(nodo_actual)
            for vecino in vecinos:
                if vecino in cerrada:
                    continue

                coste_tentativo = coste_actual + 1
                if vecino not in g_coste or coste_tentativo < g_coste[vecino]:
                    g_coste[vecino] = coste_tentativo
                    f_costo = coste_tentativo + self.distancia_manhattan(vecino, fin)
                    heapq.heappush(abierta, (f_costo, coste_tentativo, vecino))
                    padres[vecino] = nodo_actual

        return None

    def dibujar_ruta(self):
        camino = self.encontrar_camino()
        if camino:
            self.mapa.imprimir_mapa(camino)
        else:
            print("No se encontró un camino")


# Función principal del programa
def main():
    filas, columnas = 10, 10
    mapa = Mapa(filas, columnas)

    while True:
        coord = input("Introduce las coordenadas del obstáculo (formato x,y) o 'fin' para terminar: ")
        if coord.lower() == 'fin':
            break
        x, y = map(int, coord.split(','))
        mapa.agregar_obstaculo(x, y)

    coordenadas_inicio = input("Introduce las coordenadas del punto de partida (formato x,y): ")
    x_inicio, y_inicio = map(int, coordenadas_inicio.split(','))
    mapa.establecer_inicio(x_inicio, y_inicio)

    coordenadas_fin = input("Introduce las coordenadas del punto de destino (formato x,y): ")
    x_fin, y_fin = map(int, coordenadas_fin.split(','))
    mapa.establecer_fin(x_fin, y_fin)

    calculadora_rutas = CalculadoraRutas(mapa)
    calculadora_rutas.dibujar_ruta()


if __name__ == "__main__":
    main()
