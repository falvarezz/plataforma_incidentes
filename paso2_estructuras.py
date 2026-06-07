"""
paso2_estructuras.py
Demo y medicion de estructuras lineales: Queue, Stack y PriorityQueue.
Incluye casos de uso, casos borde y comparacion de rendimiento con timeit.
"""
import timeit
from datetime import datetime
from plataforma_incidentes import Event, Queue, Stack, PriorityQueue

# ---------------------------------------------------------------------------
# Dataset de prueba (variado: distintas prioridades, casos borde)
# ---------------------------------------------------------------------------

def crear_evento(n: int, prioridad: int, categoria: str = "red") -> Event:
    return Event(
        id=f"EVT-{n:03d}",
        timestamp=datetime(2026, 6, 1, 8, n % 60),
        categoria=categoria,
        prioridad=prioridad,
        texto=f"Incidente numero {n}",
        origen=f"nodo-{chr(65 + n % 4)}",
        destino=f"nodo-{chr(65 + (n + 1) % 4)}",
    )

# Eventos con prioridades variadas para mostrar el heap
eventos_demo = [
    crear_evento(1, prioridad=3, categoria="hardware"),
    crear_evento(2, prioridad=1, categoria="red"),       # mas urgente
    crear_evento(3, prioridad=2, categoria="seguridad"),
    crear_evento(4, prioridad=1, categoria="red"),       # igual prioridad que EVT-002 (FIFO)
    crear_evento(5, prioridad=3, categoria="hardware"),
]

# Dataset grande para mediciones
N = 10_000
eventos_grandes = [crear_evento(i, prioridad=i % 5 + 1) for i in range(N)]


# ---------------------------------------------------------------------------
# Demo Queue (FIFO)
# ---------------------------------------------------------------------------
print("=" * 55)
print("QUEUE (FIFO) — procesamiento en orden de llegada")
print("=" * 55)

q = Queue()

# Caso borde: dequeue en cola vacia
assert q.dequeue() is None, "dequeue() en cola vacia debe retornar None"
assert q.peek()    is None, "peek() en cola vacia debe retornar None"
print("Caso borde OK: queue vacia retorna None")

for e in eventos_demo:
    q.enqueue(e)
    print(f"  enqueue -> {e.id} (prioridad={e.prioridad})")

print(f"\nOrden de salida (FIFO — sale primero el que llego primero):")
while not q.is_empty():
    e = q.dequeue()
    print(f"  dequeue -> {e.id} (prioridad={e.prioridad})")


# ---------------------------------------------------------------------------
# Demo Stack (LIFO)
# ---------------------------------------------------------------------------
print("\n" + "=" * 55)
print("STACK (LIFO) — historial / ultimo procesado primero")
print("=" * 55)

s = Stack()

# Caso borde: pop en pila vacia
assert s.pop()  is None, "pop() en pila vacia debe retornar None"
assert s.peek() is None, "peek() en pila vacia debe retornar None"
print("Caso borde OK: stack vacio retorna None")

for e in eventos_demo:
    s.push(e)
    print(f"  push -> {e.id}")

print(f"\nOrden de salida (LIFO — sale el ultimo que entro):")
while not s.is_empty():
    e = s.pop()
    print(f"  pop  -> {e.id}")


# ---------------------------------------------------------------------------
# Demo PriorityQueue (heap)
# ---------------------------------------------------------------------------
print("\n" + "=" * 55)
print("PRIORITY QUEUE (heap) — atencion por urgencia")
print("=" * 55)

pq = PriorityQueue()

# Caso borde: pop en cola vacia
assert pq.pop()  is None, "pop() en PQ vacia debe retornar None"
assert pq.peek() is None, "peek() en PQ vacia debe retornar None"
print("Caso borde OK: priority queue vacia retorna None")

# Caso borde: un solo elemento
pq.push(eventos_demo[0])
assert pq.peek().id == eventos_demo[0].id
pq.pop()
print("Caso borde OK: un solo elemento ingresa y sale correctamente")

for e in eventos_demo:
    pq.push(e)
    print(f"  push -> {e.id} (prioridad={e.prioridad})")

print(f"\nOrden de salida (prioridad 1=critico primero; FIFO entre iguales):")
while not pq.is_empty():
    e = pq.pop()
    print(f"  pop  -> {e.id} (prioridad={e.prioridad}, categoria={e.categoria})")


# ---------------------------------------------------------------------------
# Medicion con timeit: list.pop(0) vs deque.popleft()
# ---------------------------------------------------------------------------
print("\n" + "=" * 55)
print("MEDICION: list.pop(0) vs deque.popleft() — N =", N)
print("=" * 55)

tiempo_list = timeit.timeit(
    stmt="cola_list.pop(0)",
    setup=f"cola_list = list(range({N}))",
    number=1000,
)

tiempo_deque = timeit.timeit(
    stmt="cola_deque.popleft()",
    setup=f"from collections import deque; cola_deque = deque(range({N}))",
    number=1000,
)

print(f"  list.pop(0)      : {tiempo_list:.5f}s  -> O(n) — desplaza todos los elementos")
print(f"  deque.popleft()  : {tiempo_deque:.5f}s  -> O(1) — extraccion en extremo")
print(f"  Speedup          : {tiempo_list / tiempo_deque:.1f}x mas rapido con deque")


# ---------------------------------------------------------------------------
# Medicion con timeit: insercion en PriorityQueue vs lista ordenada
# ---------------------------------------------------------------------------
print("\n" + "=" * 55)
print("MEDICION: heapq.heappush vs insort (lista siempre ordenada) — N =", N)
print("=" * 55)

tiempo_heap = timeit.timeit(
    stmt="heapq.heappush(h, i)",
    setup=f"import heapq; h = list(range({N})); heapq.heapify(h); i = 0",
    number=1000,
)

tiempo_insort = timeit.timeit(
    stmt="bisect.insort(l, i)",
    setup=f"import bisect; l = list(range({N})); i = 0",
    number=1000,
)

print(f"  heapq.heappush   : {tiempo_heap:.5f}s  -> O(log n)")
print(f"  bisect.insort    : {tiempo_insort:.5f}s  -> O(n) por desplazamiento")
print(f"  Speedup          : {tiempo_insort / tiempo_heap:.1f}x mas rapido con heap")

print("\nTrade-off: heapq es mas rapido para insertar pero solo garantiza")
print("acceso O(1) al minimo. insort mantiene la lista ordenada completa,")
print("util si se necesita iterar todos los elementos en orden.")
