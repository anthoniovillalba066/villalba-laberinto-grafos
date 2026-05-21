"""
dfs.py
Algoritmo de Búsqueda en Profundidad (DFS) para resolver el laberinto.
Encuentra UN camino (no necesariamente el más corto).
"""


def dfs(laberinto, paso_a_paso: bool = False):
    """
    Resuelve el laberinto usando DFS iterativo con pila.

    Parámetros:
        laberinto : objeto Laberinto con grafo construido.
        paso_a_paso : si True, imprime el laberinto en cada paso del DFS.

    Retorna:
        camino   (list): lista de nodos del camino encontrado, o [] si no hay camino.
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

    # Pila DFS: cada elemento es el nodo actual
    pila = [inicio]

    # Registro de visitados y padres
    visitados = []
    padre = {inicio: None}

    while pila:
        actual = pila.pop()

        if actual in visitados:
            continue

        visitados.append(actual)

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
                pila.append(vecino)

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
