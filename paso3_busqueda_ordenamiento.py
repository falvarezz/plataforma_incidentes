"""
paso3_busqueda_ordenamiento.py
Demo y medicion de busqueda y ordenamiento sobre eventos.
Compara algoritmos propios vs nativos de Python con timeit y tamanios crecientes.
"""
import timeit
import random
from datetime import datetime
from plataforma_incidentes import (
    Event,
    busqueda_secuencial, busqueda_binaria, busqueda_bisect,
    insertion_sort, merge_sort, python_sort,
)


# ---------------------------------------------------------------------------
# Generador de datos de prueba
# ---------------------------------------------------------------------------

def crear_evento(n: int) -> Event:
    return Event(
        id=f"EVT-{n:06d}",
        timestamp=datetime(2026, 6, 1, 8, n % 60),
        categoria=random.choice(["red", "seguridad", "hardware"]),
        prioridad=random.randint(1, 5),
        texto=f"Incidente {n}",
        origen=f"nodo-{chr(65 + n % 6)}",
        destino=f"nodo-{chr(65 + (n + 1) % 6)}",
    )

random.seed(42)


# ---------------------------------------------------------------------------
# BUSQUEDA — demo con casos borde
# ---------------------------------------------------------------------------
print("=" * 60)
print("BUSQUEDA SECUENCIAL vs BINARIA vs BISECT")
print("=" * 60)

# Lista ordenada por id (requerido para busqueda binaria)
eventos_ord = sorted([crear_evento(i) for i in range(200)], key=lambda e: e.id)
objetivo    = eventos_ord[150].id   # elemento que existe
inexistente = "EVT-999999"          # elemento que NO existe

# Casos borde: lista vacia
assert busqueda_secuencial([], "EVT-000001") is None
assert busqueda_binaria([], "EVT-000001")    is None
assert busqueda_bisect([], "EVT-000001")     is None
print("Caso borde OK: lista vacia retorna None en los tres algoritmos")

# Casos borde: elemento inexistente
assert busqueda_secuencial(eventos_ord, inexistente) is None
assert busqueda_binaria(eventos_ord, inexistente)    is None
assert busqueda_bisect(eventos_ord, inexistente)     is None
print("Caso borde OK: busqueda de elemento inexistente retorna None")

# Verificar que los tres encuentran el mismo resultado
r1 = busqueda_secuencial(eventos_ord, objetivo)
r2 = busqueda_binaria(eventos_ord, objetivo)
r3 = busqueda_bisect(eventos_ord, objetivo)
assert r1.id == r2.id == r3.id == objetivo
print(f"Los tres algoritmos encuentran correctamente: {objetivo}\n")

# Medicion sobre tamanios crecientes
print(f"{'N':>8}  {'Secuencial':>12}  {'Binaria':>12}  {'Bisect':>12}")
print("-" * 52)

for N in [100, 1_000, 5_000, 10_000, 50_000]:
    datos = sorted([crear_evento(i) for i in range(N)], key=lambda e: e.id)
    target = datos[N // 2].id

    t_sec = timeit.timeit(
        lambda: busqueda_secuencial(datos, target), number=300
    )
    t_bin = timeit.timeit(
        lambda: busqueda_binaria(datos, target), number=300
    )
    t_bis = timeit.timeit(
        lambda: busqueda_bisect(datos, target), number=300
    )
    print(f"{N:>8}  {t_sec:>11.5f}s  {t_bin:>11.5f}s  {t_bis:>11.5f}s")

print("\nConclucion: binaria y bisect crecen logaritmicamente (O(log n)).")
print("Secuencial crece linealmente (O(n)) — a N=50000 es mucho mas lenta.")


# ---------------------------------------------------------------------------
# ORDENAMIENTO — demo con casos borde
# ---------------------------------------------------------------------------
print("\n" + "=" * 60)
print("INSERTION SORT vs MERGE SORT vs Python sorted()")
print("=" * 60)

# Casos borde: lista vacia y un solo elemento
assert insertion_sort([]) == []
assert merge_sort([])     == []
print("Caso borde OK: lista vacia retorna lista vacia")

evento_unico = [crear_evento(1)]
assert insertion_sort(evento_unico)[0].id == evento_unico[0].id
assert merge_sort(evento_unico)[0].id     == evento_unico[0].id
print("Caso borde OK: lista de un elemento se ordena sin errores")

# Caso borde: elementos con prioridad duplicada (estabilidad)
eventos_dup = [crear_evento(i) for i in range(5)]
for e in eventos_dup:
    e.prioridad = 2   # todos igual prioridad
r_ins = insertion_sort(eventos_dup)
r_mrg = merge_sort(eventos_dup)
# Ambos deben devolver los mismos elementos
assert {e.id for e in r_ins} == {e.id for e in r_mrg}
print("Caso borde OK: prioridades iguales (elementos duplicados) sin errores\n")

# Verificar correctitud: todos deben ordenar igual
random.seed(42)
muestra = [crear_evento(i) for i in range(20)]
r1 = insertion_sort(muestra)
r2 = merge_sort(muestra)
r3 = python_sort(muestra)
assert [e.prioridad for e in r1] == [e.prioridad for e in r2] == [e.prioridad for e in r3]
print("Correctitud OK: los tres algoritmos producen el mismo orden de prioridades")

# Medicion sobre tamanios crecientes
print(f"\n{'N':>8}  {'Insertion':>12}  {'Merge':>12}  {'Python sorted':>14}")
print("-" * 56)

for N in [100, 500, 1_000, 5_000, 10_000]:
    random.seed(0)
    datos = [crear_evento(i) for i in range(N)]

    t_ins = timeit.timeit(lambda: insertion_sort(datos), number=20)
    t_mrg = timeit.timeit(lambda: merge_sort(datos),     number=20)
    t_pyt = timeit.timeit(lambda: python_sort(datos),    number=20)
    print(f"{N:>8}  {t_ins:>11.5f}s  {t_mrg:>11.5f}s  {t_pyt:>13.5f}s")

print("\nConclucion:")
print("  - Insertion sort O(n2) se vuelve muy lento a partir de N~5000.")
print("  - Merge sort O(n log n) escala bien, pero Python sorted() lo supera")
print("    porque Timsort esta implementado en C y optimizado para datos reales.")
print("\nTrade-off tiempo/memoria:")
print("  - Insertion sort: O(1) extra en memoria — ordena in-place.")
print("  - Merge sort    : O(n) extra en memoria — crea sublistas auxiliares.")
print("  - Python sorted : O(n) extra — pero amortizado con optimizaciones de C.")
