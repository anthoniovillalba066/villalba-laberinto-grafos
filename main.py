"""
main.py
Punto de entrada del programa. Menú interactivo en consola.
"""

import os
import sys

# Asegura que src/ esté en el path al ejecutar desde la raíz del proyecto
sys.path.insert(0, os.path.dirname(__file__))

from laberinto import Laberinto
from bfs import bfs
from dfs import dfs


# ------------------------------------------------------------------
# Utilidades de consola
# ------------------------------------------------------------------

def limpiar():
    os.system("cls" if os.name == "nt" else "clear")


def separador():
    print("\n" + "=" * 50)


def pausar():
    input("\n[Enter para volver al menú...]")


# ------------------------------------------------------------------
# Opciones del menú
# ------------------------------------------------------------------

def opcion_generar(lab: Laberinto):
    """Genera un laberinto aleatorio."""
    try:
        n = int(input("Ingrese el tamaño del laberinto (número impar, ej: 11, 15, 21): "))
        if n < 5:
            print("El tamaño mínimo es 5.")
            return
        if n % 2 == 0:
            n += 1
            print(f"Se ajustó a {n} para que sea impar.")
        lab.__init__(n, n)
        lab.generar_aleatorio()
        print(f"\nLaberinto {n}x{n} generado:")
        lab.mostrar()
    except ValueError:
        print("Entrada inválida. Ingrese un número entero.")


def opcion_cargar(lab: Laberinto):
    """Carga un laberinto desde archivo."""
    ruta = input("Ingrese la ruta del archivo (ej: data/laberinto1.txt): ").strip()
    if not os.path.exists(ruta):
        print(f"No se encontró el archivo '{ruta}'.")
        return
    lab.cargar_desde_archivo(ruta)
    print(f"\nLaberinto cargado desde '{ruta}':")
    lab.mostrar()


def opcion_mostrar(lab: Laberinto):
    """Muestra el laberinto actual en consola."""
    if not lab.matriz:
        print("No hay laberinto cargado. Genera o carga uno primero.")
        return
    print("\nLaberinto actual:")
    lab.mostrar()
    print(f"\n  S = Inicio {lab.inicio}   E = Salida {lab.fin}")


def opcion_bfs(lab: Laberinto):
    """Resuelve el laberinto con BFS."""
    if not lab.matriz:
        print("No hay laberinto cargado.")
        return

    paso = input("¿Mostrar paso a paso? (s/n): ").strip().lower() == "s"
    print("\nResolviendo con BFS...")
    camino, visitados = bfs(lab, paso_a_paso=paso)

    separador()
    if camino:
        print(f"✔ Camino encontrado con BFS ({len(camino)} pasos, {len(visitados)} celdas visitadas):")
        lab.mostrar(camino=camino, visitados=visitados)
    else:
        print("✘ No existe camino entre el inicio y la salida.")


def opcion_dfs(lab: Laberinto):
    """Resuelve el laberinto con DFS."""
    if not lab.matriz:
        print("No hay laberinto cargado.")
        return

    paso = input("¿Mostrar paso a paso? (s/n): ").strip().lower() == "s"
    print("\nResolviendo con DFS...")
    camino, visitados = dfs(lab, paso_a_paso=paso)

    separador()
    if camino:
        print(f"✔ Camino encontrado con DFS ({len(camino)} pasos, {len(visitados)} celdas visitadas):")
        lab.mostrar(camino=camino, visitados=visitados)
    else:
        print("✘ No existe camino entre el inicio y la salida.")


def opcion_comparar(lab: Laberinto):
    """Ejecuta BFS y DFS y compara los resultados."""
    if not lab.matriz:
        print("No hay laberinto cargado.")
        return

    print("\nComparando BFS vs DFS...\n")

    camino_bfs, visitados_bfs = bfs(lab)
    camino_dfs, visitados_dfs = dfs(lab)

    separador()
    print(f"{'Métrica':<30} {'BFS':>10} {'DFS':>10}")
    print("-" * 52)
    print(f"{'Longitud del camino':<30} {len(camino_bfs):>10} {len(camino_dfs):>10}")
    print(f"{'Celdas visitadas':<30} {len(visitados_bfs):>10} {len(visitados_dfs):>10}")
    separador()

    print("\n--- Solución BFS (camino más corto) ---")
    lab.mostrar(camino=camino_bfs)

    print("\n--- Solución DFS ---")
    lab.mostrar(camino=camino_dfs)


def opcion_grafo(lab: Laberinto):
    """Muestra la lista de adyacencia del grafo."""
    if not lab.adyacencia:
        print("No hay grafo construido. Genera o carga un laberinto primero.")
        return
    lab.mostrar_grafo()
    print(f"\nTotal de nodos en el grafo: {len(lab.adyacencia)}")


def opcion_guardar(lab: Laberinto):
    """Guarda el laberinto actual en un archivo."""
    if not lab.matriz:
        print("No hay laberinto para guardar.")
        return
    ruta = input("Nombre del archivo (ej: data/mi_laberinto.txt): ").strip()
    lab.guardar_en_archivo(ruta)


# ------------------------------------------------------------------
# Menú principal
# ------------------------------------------------------------------

def menu():
    lab = Laberinto(0, 0)

    while True:
        limpiar()
        print("╔══════════════════════════════════════════╗")
        print("║   Resolutor y Generador de Laberintos   ║")
        print("║        Grafos y Arreglos — Python        ║")
        print("╠══════════════════════════════════════════╣")
        print("║  1. Generar laberinto aleatorio          ║")
        print("║  2. Cargar laberinto desde archivo       ║")
        print("║  3. Mostrar laberinto actual             ║")
        print("║  4. Resolver con BFS                     ║")
        print("║  5. Resolver con DFS                     ║")
        print("║  6. Comparar BFS vs DFS                  ║")
        print("║  7. Mostrar representación del grafo     ║")
        print("║  8. Guardar laberinto en archivo         ║")
        print("║  0. Salir                                ║")
        print("╚══════════════════════════════════════════╝")

        opcion = input("\nSeleccione una opción: ").strip()

        separador()

        if opcion == "1":
            opcion_generar(lab)
        elif opcion == "2":
            opcion_cargar(lab)
        elif opcion == "3":
            opcion_mostrar(lab)
        elif opcion == "4":
            opcion_bfs(lab)
        elif opcion == "5":
            opcion_dfs(lab)
        elif opcion == "6":
            opcion_comparar(lab)
        elif opcion == "7":
            opcion_grafo(lab)
        elif opcion == "8":
            opcion_guardar(lab)
        elif opcion == "0":
            print("¡Hasta luego!")
            break
        else:
            print("Opción no válida. Intente de nuevo.")

        pausar()


if __name__ == "__main__":
    menu()
