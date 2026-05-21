# Documento Técnico — Resolutor y Generador de Laberintos

**Proyecto Final — Estructuras de Datos**  
**Autor:** Anthonio Villalba  
**Repositorio:** [villalba-laberinto-grafos](https://github.com/anthonio-villalba/villalba-laberinto-grafos)

---

## 1. Descripción del problema y motivación

Un laberinto es un espacio estructurado de celdas donde algunas están bloqueadas (paredes) y otras son transitables (caminos). El reto es encontrar una ruta válida desde un punto de entrada hasta un punto de salida.

Este tipo de problema es una aplicación directa de los grafos: si modelamos cada celda como un nodo y las conexiones entre celdas libres como aristas, podemos usar algoritmos de búsqueda para resolver el laberinto de forma eficiente.

La motivación es aplicar de manera práctica dos conceptos fundamentales: las **matrices bidimensionales** como estructura de almacenamiento y los **grafos con lista de adyacencia** como modelo de relaciones entre nodos.

---

## 2. Modelado del problema con el grafo

### Tipo de grafo
- **No dirigido**: si se puede ir de la celda A a la B, también se puede ir de B a A.
- **Sin pesos**: todas las conexiones tienen el mismo costo (1 paso).

### Nodos
Cada celda libre `(fila, columna)` de la matriz es un nodo del grafo.

```
Ejemplo de matriz 5x5:
  1 1 1 1 1
  1 0 0 0 1
  1 0 1 0 1
  1 0 0 0 1
  1 1 1 1 1

Nodos: (1,1), (1,2), (1,3), (2,1), (2,3), (3,1), (3,2), (3,3)
```

### Aristas
Dos nodos están conectados si son celdas libres adyacentes (arriba, abajo, izquierda, derecha).

```
(1,1) — (1,2) — (1,3)
  |               |
(2,1)           (2,3)
  |               |
(3,1) — (3,2) — (3,3)
```

### Inicio y fin
- **Inicio (S):** primera celda libre encontrada en la matriz (esquina superior izquierda).
- **Fin (E):** última celda libre encontrada (esquina inferior derecha).

---

## 3. Estructuras de datos utilizadas

### 3.1 Matriz bidimensional (arreglo 2D)
```python
self.matriz = [[1, 1, 1], [1, 0, 1], [1, 1, 1]]
```
- Tipo: lista de listas en Python.
- Uso: almacenar el estado de cada celda (0 = libre, 1 = pared).
- Justificación: acceso directo a cualquier celda en O(1) usando `matriz[fila][col]`.

### 3.2 Lista de adyacencia (diccionario de listas)
```python
self.adyacencia = {
    (1, 1): [(1, 2), (2, 1)],
    (1, 2): [(1, 1), (1, 3)],
    ...
}
```
- Tipo: diccionario donde la clave es una tupla `(fila, col)` y el valor es una lista de vecinos.
- Uso: representar el grafo del laberinto.
- Justificación: más eficiente en memoria que una matriz de adyacencia cuando el grafo es disperso (muchas celdas son paredes).

### 3.3 Cola (BFS)
```python
from collections import deque
cola = deque([inicio])
```
- Uso: garantiza el procesamiento en orden FIFO, necesario para BFS.

### 3.4 Pila (DFS)
```python
pila = [inicio]
actual = pila.pop()
```
- Uso: procesamiento LIFO para exploración en profundidad.

### 3.5 Diccionario de padres (reconstrucción del camino)
```python
padre = {inicio: None}
```
- Uso: registrar de dónde vino cada nodo para reconstruir el camino al llegar al fin.

---

## 4. Operaciones implementadas

| Operación | Módulo | Descripción | Complejidad |
|---|---|---|---|
| Generar laberinto aleatorio | `laberinto.py` | Recursive Backtracking sobre la matriz | O(N²) |
| Cargar desde archivo | `laberinto.py` | Lectura línea por línea del archivo .txt | O(N²) |
| Mostrar laberinto | `laberinto.py` | Recorre toda la matriz e imprime caracteres | O(N²) |
| Construir grafo | `laberinto.py` | Recorre celdas libres y conecta vecinos | O(N²) |
| Resolver con BFS | `bfs.py` | Búsqueda en anchura con cola | O(V + E) |
| Resolver con DFS | `dfs.py` | Búsqueda en profundidad con pila | O(V + E) |
| Comparar BFS vs DFS | `main.py` | Ejecuta ambos y muestra tabla comparativa | O(V + E) |
| Mostrar grafo | `laberinto.py` | Imprime la lista de adyacencia | O(V + E) |
| Guardar en archivo | `laberinto.py` | Escribe la matriz en un .txt | O(N²) |

> V = número de nodos (celdas libres), E = número de aristas (conexiones), N = tamaño del lado.

---

## 5. Casos de prueba

### Caso 1: Laberinto pequeño con solución (laberinto1.txt)

**Entrada:**
```
1 1 1 1 1 1 1 1 1
1 0 0 0 1 0 0 0 1
...
```

**Salida esperada BFS:**
```
Camino encontrado con BFS (X pasos, Y celdas visitadas)
```
El camino de BFS debe ser el más corto posible.

**Salida esperada DFS:**
```
Camino encontrado con DFS (X pasos, Y celdas visitadas)
```
El camino de DFS puede ser más largo, pero siempre válido.

### Caso 2: Laberinto mediano (laberinto2.txt)
Similar al caso 1, pero con más nodos. Se espera que BFS visite más celdas que DFS en algunos casos, pero encuentre un camino más corto.

### Caso 3: Laberinto sin solución
Si el laberinto está completamente cerrado, ambos algoritmos deben retornar lista vacía y mostrar:
```
✘ No existe camino entre el inicio y la salida.
```

### Caso 4: Laberinto generado aleatoriamente
Cualquier laberinto generado con la opción 1 debe tener al menos un camino válido, garantizado por el algoritmo de generación (Recursive Backtracking).

---

## 6. Diagramas e imágenes

Los diagramas del modelado del grafo, flujo de los algoritmos y capturas del demo se encuentran en la carpeta `docs/diagramas/`.

---

## 7. Instrucciones para ejecutar el código

```bash
# 1. Clonar el repositorio
git clone https://github.com/anthonio-villalba/villalba-laberinto-grafos.git
cd villalba-laberinto-grafos

# 2. Verificar Python 3
python --version

# 3. Ejecutar el programa
python src/main.py
```

No se necesita instalar ninguna librería externa.

---

## 8. Limitaciones y posibles mejoras

### Limitaciones actuales
- La visualización es solo en consola con caracteres ASCII.
- El tamaño del laberinto está limitado por el tamaño de la terminal.
- La generación aleatoria requiere que el tamaño sea impar para funcionar correctamente.
- No se valida si el archivo de entrada tiene un formato incorrecto.

### Posibles mejoras
- Agregar interfaz gráfica con `tkinter` o `pygame`.
- Implementar el algoritmo A* para comparar con BFS y DFS.
- Permitir laberintos con múltiples entradas y salidas.
- Agregar manejo de errores más robusto para archivos de entrada.
- Exportar la visualización del camino como imagen.
