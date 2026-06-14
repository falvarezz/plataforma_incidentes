"""
Paso 7 — Algoritmos de grafos: BFS, DFS, Dijkstra, Kruskal.

Demuestra los cuatro algoritmos implementados en Router (Módulo 5) sobre
una red de nodos que simula la infraestructura del sistema de incidentes.

Red de ejemplo:
    A --3-- B --2-- E
    |       |       |
    4       1       5
    |       |       |
    C --2-- D --6-- F

Ejecutar:
    python paso7_grafos.py
"""
import timeit
import random
from plataforma_incidentes import Router

# ---------------------------------------------------------------------------
# Red de ejemplo
# ---------------------------------------------------------------------------

def crear_red_ejemplo() -> Router:
    r = Router()
    # Arcos con peso = latencia en ms
    arcos = [
        ("A", "B", 3), ("B", "A", 3),
        ("A", "C", 4), ("C", "A", 4),
        ("B", "D", 1), ("D", "B", 1),
        ("B", "E", 2), ("E", "B", 2),
        ("C", "D", 2), ("D", "C", 2),
        ("D", "F", 6), ("F", "D", 6),
        ("E", "F", 5), ("F", "E", 5),
    ]
    for u, v, w in arcos:
        r.add_edge(u, v, w)
    return r

red = crear_red_ejemplo()
print("=" * 60)
print("MODULO 5 - Algoritmos de grafos")
print("=" * 60)
print(f"\nRed: {red}")
print("Nodos:", red.get_nodes())

# ---------------------------------------------------------------------------
# BFS — camino mas corto en saltos
# ---------------------------------------------------------------------------

print("\n--- 1. BFS desde nodo A ---")
distancias_bfs, pred_bfs = red.bfs("A")
print("  Distancias en saltos desde A:")
for nodo in sorted(distancias_bfs):
    print(f"    A -> {nodo}: {distancias_bfs[nodo]} salto(s)")

camino_bfs = red.reconstruir_camino(pred_bfs, "F")
print(f"\n  Camino BFS A -> F: {' -> '.join(camino_bfs)}")
print(f"  Interpretacion: ruta con menor cantidad de saltos, NO necesariamente")
print(f"  la de menor latencia. BFS ignora los pesos.")

# ---------------------------------------------------------------------------
# DFS — exploración completa
# ---------------------------------------------------------------------------

print("\n--- 2. DFS desde nodo A ---")
orden_dfs = red.dfs("A")
print(f"  Orden de visita: {' -> '.join(orden_dfs)}")
print(f"  Todos los nodos alcanzados: {len(orden_dfs)} de {len(red.get_nodes())} en la red")
print(f"  Uso: detectar el alcance de un incidente propagado desde A.")

# Grafo con nodo aislado para demostrar inalcanzabilidad
red2 = Router()
red2.add_edge("X", "Y", 1)
red2.add_node("Z")   # nodo aislado
orden_dfs2 = red2.dfs("X")
print(f"\n  DFS desde X en red {{X->Y, Z aislado}}: {orden_dfs2}")
print(f"  El nodo Z no aparece: es inalcanzable desde X.")

# ---------------------------------------------------------------------------
# Dijkstra — camino de menor costo
# ---------------------------------------------------------------------------

print("\n--- 3. Dijkstra desde nodo A ---")
distancias_dij, pred_dij = red.dijkstra("A")
print("  Costos minimos desde A:")
for nodo in sorted(distancias_dij):
    costo = distancias_dij[nodo]
    camino = red.reconstruir_camino(pred_dij, nodo)
    ruta = " -> ".join(camino) if camino else "-"
    print(f"    A -> {nodo}: costo={costo:.0f}  ruta={ruta}")

print(f"\n  Comparacion BFS vs Dijkstra para A -> F:")
camino_dij = red.reconstruir_camino(pred_dij, "F")
print(f"    BFS  (min saltos): {' -> '.join(camino_bfs)}  saltos={distancias_bfs['F']}")
print(f"    Dijkstra (min costo): {' -> '.join(camino_dij)}  costo={distancias_dij['F']:.0f}")
if camino_bfs == camino_dij:
    print(f"  En esta red el camino coincide porque el de menos saltos tambien es el")
    print(f"  de menor costo. En redes con pesos heterogeneos divergen: BFS elegiria")
    print(f"  un salto directo de peso 100 antes que dos saltos de peso 3+3=6.")
else:
    print(f"  Caminos distintos: BFS optimiza saltos, Dijkstra optimiza peso total.")

# ---------------------------------------------------------------------------
# Kruskal — árbol de expansion minima
# ---------------------------------------------------------------------------

print("\n--- 4. Kruskal — Arbol de Expansion Minima (MST) ---")
mst = red.kruskal()
costo_total = sum(w for _, _, w in mst)
print(f"  Arcos del MST ({len(mst)} arcos, costo total={costo_total}):")
for u, v, w in mst:
    print(f"    {u} -- {v}  peso={w}")
print(f"\n  Interpretacion: estos {len(mst)} arcos conectan los {len(red.get_nodes())} nodos")
print(f"  con el menor costo total posible. Util para planificar la")
print(f"  infraestructura minima de monitoreo de la red.")

# ---------------------------------------------------------------------------
# Comparacion de tiempos
# ---------------------------------------------------------------------------

print("\n--- 5. Comparacion de tiempos (red grande, timeit) ---")

def crear_red_grande(n_nodos: int, seed: int = 0) -> Router:
    random.seed(seed)
    nodos = [f"N{i}" for i in range(n_nodos)]
    r = Router()
    for nodo in nodos:
        r.add_node(nodo)
    # Conectar en anillo para garantizar conectividad base
    for i in range(n_nodos):
        r.add_edge(nodos[i], nodos[(i + 1) % n_nodos], random.uniform(1, 10))
    # Arcos adicionales aleatorios
    for _ in range(n_nodos * 2):
        u = random.choice(nodos)
        v = random.choice(nodos)
        if u != v:
            r.add_edge(u, v, random.uniform(1, 20))
    return r

SIZES = [50, 200, 500]
REPS = 20

print(f"\n  {'N nodos':>8}  {'BFS':>10}  {'DFS':>10}  {'Dijkstra':>10}  {'Kruskal':>10}")
print("  " + "-" * 54)

for N in SIZES:
    red_n = crear_red_grande(N)
    origen = "N0"

    t_bfs = timeit.timeit(lambda: red_n.bfs(origen), number=REPS) / REPS
    t_dfs = timeit.timeit(lambda: red_n.dfs(origen), number=REPS) / REPS
    t_dij = timeit.timeit(lambda: red_n.dijkstra(origen), number=REPS) / REPS
    t_kru = timeit.timeit(lambda: red_n.kruskal(), number=REPS) / REPS

    print(f"  {N:>8}  {t_bfs:>10.5f}s  {t_dfs:>10.5f}s  "
          f"{t_dij:>10.5f}s  {t_kru:>10.5f}s")

print("""
  Analisis:
  - BFS y DFS: O(V+E) — crecimiento lineal con el tamanio del grafo.
  - Dijkstra: O((V+E) log V) — factor log visible al escalar; mas lento que
    BFS porque mantiene y actualiza el heap en cada relajacion de arco.
  - Kruskal: O(E log E) — dominado por el ordenamiento inicial de arcos.
    Mas lento que BFS/DFS porque procesa TODOS los arcos, no solo los
    alcanzables desde el origen.
""")

print("=" * 60)
print("Paso 7 completado.")
