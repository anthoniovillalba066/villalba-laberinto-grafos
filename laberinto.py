"""
laberinto.py
Clase Laberinto: representa el tablero como matriz 2D y como grafo (lista de adyacencia).
"""

import random


class Laberinto:
    """
    Modela un laberinto como:
      - Una matriz N x N (arreglo 2D) donde 0 = camino, 1 = pared.
      - Un grafo no dirigido con lista de adyacencia donde cada celda libre es un nodo.
    """

    PARED = 1
    LIBRE = 0

    def __init__(self, filas: int, columnas: int):
        self.filas = filas
        self.columnas = columnas
        self.matriz = []          # Arreglo 2D (la "cuadrícula" del laberinto)
        self.adyacencia = {}      # Lista de adyacencia: {nodo: [vecinos]}
        self.inicio = None        # Tupla (fila, col) del inicio
        self.fin = None           # Tupla (fila, col) de la salida

    # ------------------------------------------------------------------
    # Generación aleatoria
    # ------------------------------------------------------------------

    def generar_aleatorio(self):
        """Genera un laberinto aleatorio usando el algoritmo de Recursive Backtracking."""

        # 1. Llenar toda la matriz de paredes
        self.matriz = [[self.PARED] * self.columnas for _ in range(self.filas)]

        # 2. DFS / backtracking para abrir caminos
        inicio = (1, 1)
        self._abrir_camino(*inicio)

        # 3. Fijar inicio y fin
        self.inicio = (1, 1)
        self.fin = (self.filas - 2, self.columnas - 2)
        self.matriz[self.inicio[0]][self.inicio[1]] = self.LIBRE
        self.matriz[self.fin[0]][self.fin[1]] = self.LIBRE

        # 4. Construir grafo desde la matriz resultante
        self._construir_grafo()

    def _abrir_camino(self, fila: int, col: int):
        """Recursive Backtracking: abre celdas en la matriz para formar el laberinto."""
        self.matriz[fila][col] = self.LIBRE
        direcciones = [(0, 2), (0, -2), (2, 0), (-2, 0)]
        random.shuffle(direcciones)

        for df, dc in direcciones:
            nf, nc = fila + df, col + dc
            if 0 < nf < self.filas - 1 and 0 < nc < self.columnas - 1:
                if self.matriz[nf][nc] == self.PARED:
                    # Derribar la pared entre la celda actual y la vecina
                    self.matriz[fila + df // 2][col + dc // 2] = self.LIBRE
                    self._abrir_camino(nf, nc)

    # ------------------------------------------------------------------
    # Carga desde archivo
    # ------------------------------------------------------------------

    def cargar_desde_archivo(self, ruta: str):
        """
        Lee un archivo .txt con el laberinto.
        Formato: filas de números separados por espacios (0 = camino, 1 = pared).
        La primera celda libre es el inicio; la última celda libre es la salida.
        """
        self.matriz = []
        with open(ruta, "r", encoding="utf-8") as f:
            for linea in f:
                linea = linea.strip()
                if linea:
                    fila = [int(x) for x in linea.split()]
                    self.matriz.append(fila)

        self.filas = len(self.matriz)
        self.columnas = len(self.matriz[0]) if self.filas > 0 else 0

        # Detectar inicio y fin automáticamente
        self.inicio = self._primera_celda_libre()
        self.fin = self._ultima_celda_libre()

        self._construir_grafo()

    def _primera_celda_libre(self):
        for f in range(self.filas):
            for c in range(self.columnas):
                if self.matriz[f][c] == self.LIBRE:
                    return (f, c)
        return None

    def _ultima_celda_libre(self):
        for f in range(self.filas - 1, -1, -1):
            for c in range(self.columnas - 1, -1, -1):
                if self.matriz[f][c] == self.LIBRE:
                    return (f, c)
        return None

    # ------------------------------------------------------------------
    # Construcción del grafo
    # ------------------------------------------------------------------

    def _construir_grafo(self):
        """
        Recorre la matriz y conecta celdas libres adyacentes (arriba, abajo, izq, der).
        Resultado: lista de adyacencia almacenada en self.adyacencia.
        """
        self.adyacencia = {}

        for f in range(self.filas):
            for c in range(self.columnas):
                if self.matriz[f][c] == self.LIBRE:
                    nodo = (f, c)
                    self.adyacencia[nodo] = []

                    for df, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                        nf, nc = f + df, c + dc
                        if 0 <= nf < self.filas and 0 <= nc < self.columnas:
                            if self.matriz[nf][nc] == self.LIBRE:
                                self.adyacencia[nodo].append((nf, nc))

    # ------------------------------------------------------------------
    # Visualización
    # ------------------------------------------------------------------

    def mostrar(self, camino=None, visitados=None):
        """
        Imprime el laberinto en consola.
        - '#' = pared
        - ' ' = camino libre
        - 'S' = inicio
        - 'E' = fin (exit)
        - '*' = parte del camino solución
        - '·' = celda visitada durante la búsqueda
        """
        camino_set = set(camino) if camino else set()
        visitados_set = set(visitados) if visitados else set()

        for f in range(self.filas):
            fila_str = ""
            for c in range(self.columnas):
                celda = (f, c)
                if self.matriz[f][c] == self.PARED:
                    fila_str += "██"
                elif celda == self.inicio:
                    fila_str += " S"
                elif celda == self.fin:
                    fila_str += " E"
                elif celda in camino_set:
                    fila_str += " *"
                elif celda in visitados_set:
                    fila_str += " ·"
                else:
                    fila_str += "  "
            print(fila_str)

    def mostrar_grafo(self):
        """Imprime la lista de adyacencia del grafo."""
        print("\n--- Lista de Adyacencia del Grafo ---")
        for nodo, vecinos in sorted(self.adyacencia.items()):
            print(f"  {nodo} -> {vecinos}")

    def guardar_en_archivo(self, ruta: str):
        """Guarda la matriz actual en un archivo de texto."""
        with open(ruta, "w", encoding="utf-8") as f:
            for fila in self.matriz:
                f.write(" ".join(map(str, fila)) + "\n")
        print(f"Laberinto guardado en '{ruta}'.")
