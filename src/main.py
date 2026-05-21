"""
Resolutor y Generador de Laberintos
Problema 4 - Proyecto Final Grafos y Arreglos
"""

import random
import json
from collections import deque


# ─────────────────────────────────────────────
#  ESTRUCTURAS DE DATOS
# ─────────────────────────────────────────────

class Cell:
    """Nodo del grafo: celda del laberinto."""
    def __init__(self, row: int, col: int):
        self.row = row
        self.col = col
        self.walls = {"N": True, "S": True, "E": True, "W": True}
        self.visited = False

    def __repr__(self):
        return f"Cell({self.row},{self.col})"


class Maze:
    """
    Laberinto como grafo no dirigido implícito.
    - Arreglo 2D (lista de listas) de celdas: O(N*M) espacio.
    - Lista de adyacencia construida dinámicamente según paredes.
    """

    OPPOSITE = {"N": "S", "S": "N", "E": "W", "W": "E"}
    DIRS = {"N": (-1, 0), "S": (1, 0), "E": (0, 1), "W": (0, -1)}

    def __init__(self, rows: int, cols: int):
        self.rows = rows
        self.cols = cols
        # Arreglo 2D de celdas (nodos del grafo)
        self.grid: list[list[Cell]] = [
            [Cell(r, c) for c in range(cols)] for r in range(rows)
        ]
        self.start = (0, 0)
        self.end = (rows - 1, cols - 1)

    # ── Acceso al arreglo ──────────────────────────────
    def cell(self, r: int, c: int) -> Cell | None:
        if 0 <= r < self.rows and 0 <= c < self.cols:
            return self.grid[r][c]
        return None

    def neighbors(self, r: int, c: int) -> list[tuple[str, Cell]]:
        """Vecinos accesibles (sin pared) desde (r,c)."""
        result = []
        for direction, (dr, dc) in self.DIRS.items():
            nr, nc = r + dr, c + dc
            neighbor = self.cell(nr, nc)
            if neighbor and not self.grid[r][c].walls[direction]:
                result.append((direction, neighbor))
        return result

    def all_neighbors(self, r: int, c: int) -> list[tuple[str, Cell]]:
        """Todos los vecinos físicos (sin importar paredes)."""
        result = []
        for direction, (dr, dc) in self.DIRS.items():
            nr, nc = r + dr, c + dc
            neighbor = self.cell(nr, nc)
            if neighbor:
                result.append((direction, neighbor))
        return result

    def remove_wall(self, r1: int, c1: int, direction: str):
        """Elimina pared entre (r1,c1) y su vecino en `direction`."""
        dr, dc = self.DIRS[direction]
        r2, c2 = r1 + dr, c1 + dc
        self.grid[r1][c1].walls[direction] = False
        self.grid[r2][c2].walls[self.OPPOSITE[direction]] = False

    # ── Generación: DFS con backtracking (Recursive Backtracker) ──
    def generate(self):
        """
        Genera laberinto con DFS + backtracking.
        Complejidad: O(N*M) tiempo y espacio.
        """
        # Reiniciar paredes
        for row in self.grid:
            for cell in row:
                cell.walls = {"N": True, "S": True, "E": True, "W": True}
                cell.visited = False

        stack = [self.grid[0][0]]
        self.grid[0][0].visited = True
        visited_count = 1
        total = self.rows * self.cols

        while stack:
            current = stack[-1]
            # Vecinos no visitados
            unvisited = [
                (d, nb) for d, nb in self.all_neighbors(current.row, current.col)
                if not nb.visited
            ]
            if unvisited:
                direction, chosen = random.choice(unvisited)
                self.remove_wall(current.row, current.col, direction)
                chosen.visited = True
                visited_count += 1
                stack.append(chosen)
            else:
                stack.pop()

        # Limpiar flags de visita
        for row in self.grid:
            for cell in row:
                cell.visited = False

    # ── BFS: camino más corto ──────────────────────────
    def solve_bfs(self) -> tuple[list[tuple[int, int]], list[list[tuple[int, int]]]]:
        """
        BFS desde start hasta end.
        Retorna (camino, orden_de_visita_por_nivel).
        Complejidad: O(V + E) = O(N*M).
        """
        sr, sc = self.start
        er, ec = self.end
        parent = {(sr, sc): None}
        queue = deque([(sr, sc)])
        levels: list[list[tuple[int, int]]] = [[(sr, sc)]]

        while queue:
            next_level = []
            level_size = len(queue)
            for _ in range(level_size):
                r, c = queue.popleft()
                if (r, c) == (er, ec):
                    return self._reconstruct(parent, er, ec), levels
                for _, nb in self.neighbors(r, c):
                    if (nb.row, nb.col) not in parent:
                        parent[(nb.row, nb.col)] = (r, c)
                        queue.append((nb.row, nb.col))
                        next_level.append((nb.row, nb.col))
            if next_level:
                levels.append(next_level)

        return [], levels  # Sin solución

    # ── DFS: cualquier camino ──────────────────────────
    def solve_dfs(self) -> tuple[list[tuple[int, int]], list[tuple[int, int]]]:
        """
        DFS iterativo desde start hasta end.
        Retorna (camino, orden_de_visita).
        Complejidad: O(V + E) = O(N*M).
        """
        sr, sc = self.start
        er, ec = self.end
        parent = {(sr, sc): None}
        stack = [(sr, sc)]
        visit_order: list[tuple[int, int]] = []

        while stack:
            r, c = stack.pop()
            if (r, c) in visit_order:
                continue
            visit_order.append((r, c))
            if (r, c) == (er, ec):
                return self._reconstruct(parent, er, ec), visit_order
            for _, nb in self.neighbors(r, c):
                pos = (nb.row, nb.col)
                if pos not in parent:
                    parent[pos] = (r, c)
                    stack.append(pos)

        return [], visit_order

    def _reconstruct(self, parent: dict, er: int, ec: int) -> list[tuple[int, int]]:
        path = []
        pos: tuple[int, int] | None = (er, ec)
        while pos is not None:
            path.append(pos)
            pos = parent[pos]
        path.reverse()
        return path

    # ── Serialización ──────────────────────────────────
    def to_dict(self) -> dict:
        return {
            "rows": self.rows,
            "cols": self.cols,
            "start": list(self.start),
            "end": list(self.end),
            "grid": [
                [
                    {"walls": cell.walls}
                    for cell in row
                ]
                for row in self.grid
            ]
        }

    def save(self, filepath: str):
        with open(filepath, "w") as f:
            json.dump(self.to_dict(), f, indent=2)
        print(f"Laberinto guardado en {filepath}")

    @classmethod
    def load(cls, filepath: str) -> "Maze":
        with open(filepath) as f:
            data = json.load(f)
        maze = cls(data["rows"], data["cols"])
        maze.start = tuple(data["start"])
        maze.end = tuple(data["end"])
        for r in range(maze.rows):
            for c in range(maze.cols):
                maze.grid[r][c].walls = data["grid"][r][c]["walls"]
        print(f"Laberinto cargado desde {filepath}")
        return maze

    # ── Representación ASCII ───────────────────────────
    def display(self, path: list[tuple[int, int]] | None = None) -> str:
        path_set = set(path) if path else set()
        sr, sc = self.start
        er, ec = self.end
        lines = ["+" + "---+" * self.cols]

        for r in range(self.rows):
            row_mid = "|"
            row_bot = "+"
            for c in range(self.cols):
                cell = self.grid[r][c]
                if (r, c) == (sr, sc):
                    content = " S "
                elif (r, c) == (er, ec):
                    content = " E "
                elif (r, c) in path_set:
                    content = " · "
                else:
                    content = "   "
                row_mid += content + ("|" if cell.walls["E"] else " ")
                row_bot += ("---+" if cell.walls["S"] else "   +")
            lines.append(row_mid)
            lines.append(row_bot)
        return "\n".join(lines)


# ─────────────────────────────────────────────
#  INTERFAZ DE LÍNEA DE COMANDOS
# ─────────────────────────────────────────────

def menu():
    maze: Maze | None = None
    bfs_path: list[tuple[int, int]] = []
    dfs_path: list[tuple[int, int]] = []

    while True:
        print("\n╔══════════════════════════════╗")
        print("║   RESOLUTOR DE LABERINTOS   ║")
        print("╠══════════════════════════════╣")
        print("║ 1. Generar laberinto         ║")
        print("║ 2. Cargar desde archivo      ║")
        print("║ 3. Guardar en archivo        ║")
        print("║ 4. Mostrar laberinto         ║")
        print("║ 5. Resolver con BFS          ║")
        print("║ 6. Resolver con DFS          ║")
        print("║ 7. Comparar BFS vs DFS       ║")
        print("║ 8. Salir                     ║")
        print("╚══════════════════════════════╝")
        op = input("Opción: ").strip()

        if op == "1":
            r = int(input("Filas (ej. 10): "))
            c = int(input("Columnas (ej. 10): "))
            maze = Maze(r, c)
            maze.generate()
            bfs_path, dfs_path = [], []
            print("✓ Laberinto generado.")
            print(maze.display())

        elif op == "2":
            path = input("Ruta del archivo: ").strip()
            try:
                maze = Maze.load(path)
                bfs_path, dfs_path = [], []
            except FileNotFoundError:
                print("✗ Archivo no encontrado.")

        elif op == "3":
            if not maze:
                print("✗ Primero genera o carga un laberinto.")
                continue
            path = input("Nombre del archivo (ej. data/maze.json): ").strip()
            maze.save(path)

        elif op == "4":
            if not maze:
                print("✗ No hay laberinto cargado.")
                continue
            print(maze.display())

        elif op == "5":
            if not maze:
                print("✗ No hay laberinto cargado.")
                continue
            bfs_path, levels = maze.solve_bfs()
            if bfs_path:
                print(f"✓ BFS encontró camino de {len(bfs_path)} pasos.")
                print(maze.display(bfs_path))
                show = input("¿Ver paso a paso? (s/n): ")
                if show.lower() == "s":
                    for i, level in enumerate(levels):
                        visited = [p for lvl in levels[:i+1] for p in lvl]
                        print(f"\n--- Nivel {i} ---")
                        print(maze.display(visited))
                        input("(Enter para continuar)")
            else:
                print("✗ No se encontró solución.")

        elif op == "6":
            if not maze:
                print("✗ No hay laberinto cargado.")
                continue
            dfs_path, visit_order = maze.solve_dfs()
            if dfs_path:
                print(f"✓ DFS encontró camino de {len(dfs_path)} pasos.")
                print(maze.display(dfs_path))
                show = input("¿Ver paso a paso? (s/n): ")
                if show.lower() == "s":
                    for i, pos in enumerate(visit_order):
                        print(f"\n--- Paso {i+1} ---")
                        print(maze.display(visit_order[:i+1]))
                        input("(Enter para continuar)")
            else:
                print("✗ No se encontró solución.")

        elif op == "7":
            if not maze:
                print("✗ No hay laberinto cargado.")
                continue
            bfs_path, _ = maze.solve_bfs()
            dfs_path, dfs_order = maze.solve_dfs()
            print("\n┌─────────────────────────────────┐")
            print("│       COMPARACIÓN BFS vs DFS    │")
            print("├──────────────┬──────────────────┤")
            print(f"│ BFS pasos    │ {len(bfs_path):<16} │")
            print(f"│ DFS pasos    │ {len(dfs_path):<16} │")
            print(f"│ BFS óptimo   │ {'Sí':<16} │")
            print(f"│ DFS óptimo   │ {'No garantizado':<16} │")
            print("└──────────────┴──────────────────┘")
            if len(bfs_path) < len(dfs_path):
                diff = len(dfs_path) - len(bfs_path)
                print(f"  BFS es {diff} paso(s) más corto que DFS.")
            elif len(bfs_path) == len(dfs_path):
                print("  Ambos encontraron el mismo largo de camino.")
            print("\nCamino BFS:")
            print(maze.display(bfs_path))
            print("\nCamino DFS:")
            print(maze.display(dfs_path))

        elif op == "8":
            print("¡Hasta luego!")
            break
        else:
            print("Opción inválida.")


if __name__ == "__main__":
    menu()