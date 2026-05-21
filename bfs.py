"""
bfs.py
Algoritmo de Búsqueda en Anchura (BFS) para resolver el laberinto.
Encuentra el camino MÁS CORTO entre inicio y fin.
"""

from collections import deque


def bfs(laberinto, paso_a_paso: bool = False):
    """
    Resuelve el laberinto usando BFS.

    Parámetros:
        laberinto : objeto Laberinto con grafo construido.
        paso_a_paso : si True, imprime el laberinto en cada nivel del BFS.

    Retorna:
        camino   (list): lista de nodos del camino más corto, o [] si no hay camino.
        visitados (list): todos los nodos explorados durante la búsqueda.
    """
    inicio = laberinto.inicio
    fin = laberinto.fin
    grafo = laberinto.adyacencia

    if inicio is None or fin is None:
        print("Error: el laberinto no tiene inicio o fin definido.")
        return [], []

    if inicio not in grafo:
        print("Error: el nodo de inicio no está en el grafo.")
        return [], []

    # Cola BFS: cada elemento es el nodo actual
    cola = deque([inicio])

    # Registro de visitados y el nodo padre de cada uno (para reconstruir camino)
    visitados = [inicio]
    padre = {inicio: None}

    while cola:
        actual = cola.popleft()

        if paso_a_paso:
            print(f"\n  Visitando: {actual}")
            laberinto.mostrar(visitados=visitados)
            input("  [Enter para continuar...]")

        if actual == fin:
            camino = _reconstruir_camino(padre, inicio, fin)
            return camino, visitados

        for vecino in grafo.get(actual, []):
            if vecino not in padre:
                padre[vecino] = actual
                visitados.append(vecino)
                cola.append(vecino)

    # Si la cola se vacía sin encontrar fin, no hay solución
    return [], visitados


def _reconstruir_camino(padre: dict, inicio, fin) -> list:
    """Recorre el diccionario de padres hacia atrás para obtener el camino."""
    camino = []
    actual = fin
    while actual is not None:
        camino.append(actual)
        actual = padre[actual]
    camino.reverse()
    return camino
