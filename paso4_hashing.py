"""
paso4_hashing.py
Demo y medicion de hashing e indices.
Compara HashTable propia (encadenamiento) vs Index (dict de Python).
Incluye visualizacion de colisiones y analisis de factor de carga.
"""
import timeit
import random
from datetime import datetime
from plataforma_incidentes import Event, Index, HashTable


# ---------------------------------------------------------------------------
# Generador de datos
# ---------------------------------------------------------------------------

def crear_evento(n: int) -> Event:
    return Event(
        id=f"EVT-{n:06d}",
        timestamp=datetime(2026, 6, 1, 8, n % 60),
        categoria=random.choice(["red", "seguridad", "hardware", "red"]),
        prioridad=random.randint(1, 5),
        texto=f"Incidente {n}",
        origen=f"nodo-{chr(65 + n % 6)}",
        destino=f"nodo-{chr(65 + (n + 1) % 6)}",
    )

random.seed(42)


# ---------------------------------------------------------------------------
# Demo HashTable propia — insercion, busqueda, actualizacion, eliminacion
# ---------------------------------------------------------------------------
print("=" * 60)
print("HASHTABLE PROPIA (encadenamiento)")
print("=" * 60)

ht = HashTable(capacidad=8)   # capacidad pequeña para forzar colisiones

# Casos borde: busqueda y eliminacion en tabla vacia
assert ht.search("EVT-000001") is None
assert ht.delete("EVT-000001") is False
print("Caso borde OK: tabla vacia retorna None / False")

# Insercion
eventos_demo = [crear_evento(i) for i in range(10)]
for e in eventos_demo:
    ht.insert(e.id, e)
print(f"\nDespues de insertar 10 eventos:")
print(f"  {ht}")

# Mostrar estadisticas internas (colisiones)
stats = ht.stats()
print(f"\nEstadisticas internas:")
print(f"  Capacidad            : {stats['capacidad']}")
print(f"  Elementos            : {stats['elementos']}")
print(f"  Factor de carga      : {stats['factor_de_carga']}")
print(f"  Buckets con colision : {stats['buckets_con_colision']}")
print(f"  Max elementos/bucket : {stats['max_elementos_bucket']}")

# Busqueda
target = eventos_demo[5].id
resultado = ht.search(target)
assert resultado is not None and resultado.id == target
print(f"\nBusqueda de '{target}': encontrado -> {resultado}")

# Busqueda de inexistente
assert ht.search("EVT-999999") is None
print("Busqueda de 'EVT-999999' (inexistente): None OK")

# Actualizacion (reinsertar misma clave)
nuevo_evento = crear_evento(999)
nuevo_evento.id = target
ht.insert(target, nuevo_evento)
assert len(ht) == 10   # no debe duplicar
print(f"Actualizacion de clave existente: size sigue siendo {len(ht)} OK")

# Eliminacion
ht.delete(target)
assert ht.search(target) is None
assert len(ht) == 9
print(f"Eliminacion de '{target}': size ahora {len(ht)} OK")

# Rehash automatico: insertar mas elementos para superar load_factor 0.75
ht2 = HashTable(capacidad=4)
for i in range(20):
    ht2.insert(f"K{i}", i)
print(f"\nRehash automatico al superar load_factor 0.75:")
print(f"  {ht2}")


# ---------------------------------------------------------------------------
# Index (dict de Python) — indices multiples por distintos atributos
# ---------------------------------------------------------------------------
print("\n" + "=" * 60)
print("INDEX (dict de Python) — indices por id, categoria, origen")
print("=" * 60)

random.seed(42)
eventos = [crear_evento(i) for i in range(100)]

idx_id  = Index(key_attr="id")
idx_cat = Index(key_attr="categoria")
idx_ori = Index(key_attr="origen")

for e in eventos:
    idx_id.insert(e)
    idx_cat.insert(e)
    idx_ori.insert(e)

print(f"  {idx_id}")
print(f"  {idx_cat}")
print(f"  {idx_ori}")

# Busqueda por categoria (multi-valor)
cat_resultado = idx_cat.search("seguridad")
print(f"\nEventos de categoria 'seguridad': {len(cat_resultado)} encontrados")

# Busqueda por origen
ori_resultado = idx_ori.search("nodo-A")
print(f"Eventos con origen 'nodo-A'     : {len(ori_resultado)} encontrados")


# ---------------------------------------------------------------------------
# Medicion: HashTable propia vs dict (Index) vs busqueda secuencial
# ---------------------------------------------------------------------------
print("\n" + "=" * 60)
print("MEDICION: busqueda por id — secuencial vs HashTable vs dict")
print("=" * 60)

print(f"\n{'N':>8}  {'Secuencial':>12}  {'HashTable':>12}  {'dict (Index)':>14}")
print("-" * 56)

for N in [100, 1_000, 5_000, 10_000]:
    random.seed(0)
    evts = [crear_evento(i) for i in range(N)]
    target_id = evts[N // 2].id

    # Secuencial
    t_sec = timeit.timeit(
        lambda: next((e for e in evts if e.id == target_id), None),
        number=500
    )

    # HashTable propia
    ht_med = HashTable()
    for e in evts:
        ht_med.insert(e.id, e)
    t_ht = timeit.timeit(lambda: ht_med.search(target_id), number=500)

    # dict nativo (Index)
    idx_med = Index(key_attr="id")
    for e in evts:
        idx_med.insert(e)
    t_dict = timeit.timeit(lambda: idx_med.search_one(target_id), number=500)

    print(f"{N:>8}  {t_sec:>11.5f}s  {t_ht:>11.5f}s  {t_dict:>13.5f}s")

print("\nConclucion:")
print("  - Secuencial crece con N (O(n)).")
print("  - HashTable propia y dict son O(1) promedio — estables con N.")
print("  - dict es mas rapido que HashTable propia porque su hash")
print("    esta implementado en C con optimizaciones de bajo nivel.")
print("\nTrade-off:")
print("  HashTable propia: didactica, permite controlar la funcion hash")
print("  y el manejo de colisiones. Util para entender el mecanismo.")
print("  dict nativo     : optimo para produccion. No expone internos.")
