# villalba-laberinto-grafos

Proyecto final de la asignatura de Estructuras de Datos.  
Aplicación en consola desarrollada en Python que genera y resuelve laberintos usando grafos y arreglos como estructuras de datos principales.

---

## 📋 Descripción general

Este proyecto modela un laberinto como un **grafo no dirigido**, donde cada celda de la matriz es un nodo y las conexiones entre celdas accesibles representan las aristas. Se implementan dos algoritmos de búsqueda (**BFS** y **DFS**) para resolver el laberinto, permitiendo comparar sus resultados y visualizar el proceso paso a paso.

---

## 🎯 Objetivos

- Modelar un laberinto como grafo usando listas de adyacencia.
- Generar laberintos aleatorios mediante algoritmos de construcción de grafos.
- Cargar y mostrar laberintos desde archivos de texto.
- Resolver laberintos con BFS (camino más corto) y DFS (exploración profunda).
- Comparar los resultados de ambos algoritmos.
- Visualizar el avance del algoritmo paso a paso en consola.

---

## 👤 Integrantes

| Nombre | GitHub |
|---|---|
| Anthonio Villalba | [@anthoniovillalba066](https://github.com/anthonio-villalba) |

---

## 🛠️ Tecnologías usadas

| Tecnología | Uso |
|---|---|
| Python 3.x | Lenguaje principal |
| `collections.deque` | Cola para BFS |
| Módulo `random` | Generación aleatoria del laberinto |
| Archivos `.txt` | Carga y almacenamiento de laberintos |

> No se usan librerías externas. Solo la biblioteca estándar de Python.

---

## 📁 Estructura del proyecto

```
villalba-laberinto-grafos/
│
├── README.md
│
├── src/
│   ├── main.py           # Punto de entrada del programa
│   ├── laberinto.py      # Clase Laberinto (matriz + grafo)
│   ├── bfs.py            # Algoritmo BFS
│   └── dfs.py            # Algoritmo DFS
│
├── data/
│   ├── laberinto1.txt    # Laberinto de ejemplo pequeño
│   └── laberinto2.txt    # Laberinto de ejemplo mediano
│
└── docs/
    ├── documento_tecnico.md
    └── diagramas/
```

---

## ▶️ Instrucciones de ejecución

### 1. Clonar el repositorio

```bash
git clone https://github.com/anthonio-villalba/villalba-laberinto-grafos.git
cd villalba-laberinto-grafos
```

### 2. Verificar Python instalado

```bash
python --version
# Se requiere Python 3.x
```

### 3. Ejecutar el programa

```bash
python src/main.py
```

---

## ⚙️ Funcionalidades principales

1. **Generar laberinto aleatorio** — Crea un laberinto de tamaño N×N con caminos y paredes generados aleatoriamente.
2. **Cargar laberinto desde archivo** — Lee un laberinto en formato de texto y lo representa en pantalla.
3. **Mostrar el laberinto** — Imprime la matriz en consola con caracteres que representan paredes y caminos.
4. **Resolver con BFS** — Encuentra el camino más corto desde la entrada hasta la salida.
5. **Resolver con DFS** — Explora el laberinto en profundidad y encuentra un camino (no necesariamente el más corto).
6. **Comparar BFS vs DFS** — Muestra ambas soluciones y compara longitud del camino y nodos visitados.
7. **Visualización paso a paso** — Imprime el avance del algoritmo celda por celda durante la búsqueda.

---

## 📌 Formato del archivo de laberinto

Los archivos en `data/` usan el siguiente formato:

```
1 1 1 1 1
1 0 0 0 1
1 0 1 0 1
1 0 0 0 1
1 1 1 1 1
```

- `1` → Pared  
- `0` → Camino libre  
- La entrada es la primera celda libre y la salida la última.

---

## 📚 Conceptos aplicados

- Grafos no dirigidos representados con listas de adyacencia
- Recorrido en anchura (BFS) con cola
- Recorrido en profundidad (DFS) con pila o recursión
- Arreglos bidimensionales como tablero del laberinto
- Backtracking para generación aleatoria

---

*Proyecto desarrollado para la asignatura de Estructuras de Datos — Ingeniería de Software.*
