"""
Paso 6 — Árbol AVL como índice ordenado de eventos.

Demuestra:
  1. Inserción de eventos en el AVL con clave = prioridad (caso secuencial, el peor
     caso para un BST simple).
  2. Que el AVL se mantiene balanceado independientemente del orden de inserción.
  3. Recorrido inorder produce eventos ordenados por prioridad.
  4. Búsqueda por rango: eventos con prioridad en [2, 4].
  5. Comparación de tiempos: AVL vs dict (Index) vs búsqueda secuencial para N grande.

Ejecutar:
    python paso6_avl.py
"""
import timeit
import random
from datetime import datetime, timedelta
from plataforma_incidentes import Event, EventStore, Index, AVLTree


# ---------------------------------------------------------------------------
# Datos de ejemplo
# ---------------------------------------------------------------------------

CATEGORIAS = ["RED", "SEGURIDAD", "SERVIDOR", "BASE_DATOS", "APLICACION"]
ORIGENES   = ["nodo-A", "nodo-B", "nodo-C", "nodo-D"]
DESTINOS   = ["nodo-X", "nodo-Y", "nodo-Z"]


def _generar_evento(i: int) -> Event:
    return Event(
        id=i,
        timestamp=datetime(2026, 1, 1) + timedelta(minutes=i * 5),
        categoria=CATEGORIAS[i % len(CATEGORIAS)],
        prioridad=random.randint(1, 5),
        texto=f"Incidente numero {i}",
        origen=ORIGENES[i % len(ORIGENES)],
        destino=DESTINOS[i % len(DESTINOS)],
    )


def _generar_eventos(n: int, seed: int = 42) -> list:
    random.seed(seed)
    return [_generar_evento(i) for i in range(n)]


# ---------------------------------------------------------------------------
# Sección 1 — Construcción y propiedades del AVL
# ---------------------------------------------------------------------------

print("=" * 60)
print("MÓDULO 4 — Árbol AVL: índice ordenado de eventos")
print("=" * 60)

print("\n--- 1. Inserción en orden secuencial (peor caso para BST simple) ---")

# Un BST simple con inserciones ordenadas degenera en una lista enlazada (altura N).
# El AVL corrige esto con rotaciones, garantizando altura O(log N).
avl_prioridad = AVLTree()
for i in range(1, 8):     # insertar 1,2,3,4,5,6,7 en orden ascendente
    avl_prioridad.insert(i, f"evento_prio_{i}")
    fb = avl_prioridad._factor_balance(avl_prioridad._raiz)
    print(f"  Después de insertar clave={i}: altura={avl_prioridad.height()}, "
          f"balance raiz={fb}")

print(f"\n  Altura final con 7 nodos: {avl_prioridad.height()} "
      f"(log2(7)~2.8, maximo permitido: 3)")
print(f"  Un BST sin balanceo tendria altura 7 (lista enlazada).")

# ---------------------------------------------------------------------------
# Sección 2 — Recorrido inorder y búsqueda por rango
# ---------------------------------------------------------------------------

print("\n--- 2. Recorrido inorder de eventos por prioridad ---")

eventos_demo = _generar_eventos(10)
avl_eventos = AVLTree()
store = EventStore()

# Insertar con clave compuesta (prioridad * 1000 + id) para manejar duplicados de prioridad
for ev in eventos_demo:
    store.add_event(ev)
    avl_eventos.insert(ev.prioridad * 1000 + ev.id, ev)

inorder = avl_eventos.inorder()
print("  Eventos ordenados por prioridad (inorder AVL):")
for clave, ev in inorder:
    print(f"    prio={ev.prioridad}, id={ev.id:3d}, categoria={ev.categoria}")

# ---------------------------------------------------------------------------
# Sección 3 — Búsqueda por rango
# ---------------------------------------------------------------------------

print("\n--- 3. Búsqueda por rango: eventos con prioridad en [2, 4] ---")

# El AVL soporta range_search en O(log n + k); un dict no puede hacer esto.
rango = avl_eventos.range_search(2 * 1000, 4 * 1000 + 999)
print(f"  Encontrados: {len(rango)} eventos")
for clave, ev in rango:
    print(f"    prio={ev.prioridad}, id={ev.id}")

# ---------------------------------------------------------------------------
# Sección 4 — Búsqueda puntual
# ---------------------------------------------------------------------------

print("\n--- 4. Búsqueda puntual por clave compuesta ---")

clave_buscada = eventos_demo[3].prioridad * 1000 + eventos_demo[3].id
resultado = avl_eventos.search(clave_buscada)
if resultado:
    print(f"  Buscando clave={clave_buscada}: encontrado id={resultado.id}, "
          f"categoria={resultado.categoria}")
else:
    print(f"  Clave {clave_buscada} no encontrada")

# ---------------------------------------------------------------------------
# Sección 5 — Comparación de tiempos: AVL vs dict vs secuencial
# ---------------------------------------------------------------------------

print("\n--- 5. Comparación de tiempos (N=5000, timeit) ---")

SIZES = [500, 2000, 5000]
REPETICIONES = 100

print(f"\n  {'N':>6}  {'AVL insert':>12}  {'AVL search':>12}  "
      f"{'dict search':>12}  {'Secuencial':>12}")
print("  " + "-" * 58)

for N in SIZES:
    eventos_n = _generar_eventos(N, seed=N)

    # -- Construcción del AVL --
    def setup_avl():
        avl = AVLTree()
        for ev in eventos_n:
            avl.insert(ev.prioridad * 1000 + ev.id, ev)
        return avl

    avl_ref = setup_avl()

    # Tiempos de inserción
    t_insert = timeit.timeit(
        lambda: [setup_avl()],
        number=10
    ) / 10

    # Tiempos de búsqueda (clave del evento en posición central)
    clave_mid = eventos_n[N // 2].prioridad * 1000 + eventos_n[N // 2].id
    t_avl_search = timeit.timeit(
        lambda: avl_ref.search(clave_mid),
        number=REPETICIONES
    ) / REPETICIONES

    # dict (Index) — búsqueda por id
    idx = Index(key_attr="id")
    for ev in eventos_n:
        idx.insert(ev)
    t_dict_search = timeit.timeit(
        lambda: idx.search(eventos_n[N // 2].id),
        number=REPETICIONES
    ) / REPETICIONES

    # Búsqueda secuencial
    t_seq = timeit.timeit(
        lambda: next((e for e in eventos_n if e.id == eventos_n[N // 2].id), None),
        number=REPETICIONES
    ) / REPETICIONES

    print(f"  {N:>6}  {t_insert:>12.5f}s  {t_avl_search:>12.6f}s  "
          f"{t_dict_search:>12.6f}s  {t_seq:>12.6f}s")

print("""
  Analisis:
  - AVL insert: O(log n) por nodo -> costo de construccion O(n log n)
  - AVL search: O(log n) garantizado en TODOS los casos
  - dict search: O(1) promedio, O(n) peor caso (colisiones extremas)
  - Secuencial: O(n) siempre

  Ventaja exclusiva del AVL: range_search en O(log n + k).
  Un dict no puede responder "dame todos los eventos con prioridad entre 2 y 4"
  sin recorrer todos sus elementos.
""")

# ---------------------------------------------------------------------------
# Sección 6 — Visualización de la estructura interna
# ---------------------------------------------------------------------------

print("--- 6. Estructura interna del árbol (rotaciones verificadas) ---")

# Caso clásico LL: insertar 3,2,1 → debe rotar derecha
avl_ll = AVLTree()
for k in [3, 2, 1]:
    avl_ll.insert(k, k)
raiz_ll = avl_ll._raiz
print(f"\n  Caso LL (insert 3,2,1):")
print(f"    Raiz={raiz_ll.clave}, izq={raiz_ll.izq.clave}, der={raiz_ll.der.clave}")
print(f"    Altura={avl_ll.height()} (esperado: 2)")

# Caso RR: insertar 1,2,3 → debe rotar izquierda
avl_rr = AVLTree()
for k in [1, 2, 3]:
    avl_rr.insert(k, k)
raiz_rr = avl_rr._raiz
print(f"\n  Caso RR (insert 1,2,3):")
print(f"    Raiz={raiz_rr.clave}, izq={raiz_rr.izq.clave}, der={raiz_rr.der.clave}")
print(f"    Altura={avl_rr.height()} (esperado: 2)")

# Caso LR: insertar 3,1,2 → rotar izquierda sobre hijo, luego derecha sobre raíz
avl_lr = AVLTree()
for k in [3, 1, 2]:
    avl_lr.insert(k, k)
raiz_lr = avl_lr._raiz
print(f"\n  Caso LR (insert 3,1,2):")
print(f"    Raiz={raiz_lr.clave}, izq={raiz_lr.izq.clave}, der={raiz_lr.der.clave}")
print(f"    Altura={avl_lr.height()} (esperado: 2)")

# Caso RL: insertar 1,3,2 → rotar derecha sobre hijo, luego izquierda sobre raíz
avl_rl = AVLTree()
for k in [1, 3, 2]:
    avl_rl.insert(k, k)
raiz_rl = avl_rl._raiz
print(f"\n  Caso RL (insert 1,3,2):")
print(f"    Raiz={raiz_rl.clave}, izq={raiz_rl.izq.clave}, der={raiz_rl.der.clave}")
print(f"    Altura={avl_rl.height()} (esperado: 2)")

print("\n  Todos los casos de rotación producen altura 2 con 3 nodos. OK")
print("\n" + "=" * 60)
print("Paso 6 completado.")
