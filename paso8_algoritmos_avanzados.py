"""
Paso 8 — Algoritmos avanzados: KMP, RSA demostrativo, Knapsack 0/1.

Demuestra los tres algoritmos del Módulo 6 aplicados al sistema de incidentes.

Ejecutar:
    python paso8_algoritmos_avanzados.py
"""
import timeit
import random
from plataforma_incidentes import Event, EventStore, RSADemo, knapsack, knapsack_optimizado
from plataforma_incidentes.text_analyzer import TextAnalyzer
from datetime import datetime, timedelta

print("=" * 62)
print("MODULO 6 - Algoritmos avanzados")
print("=" * 62)

# ---------------------------------------------------------------------------
# Sección 1 — KMP vs Fuerza Bruta (ya implementado, se mide aquí)
# ---------------------------------------------------------------------------

print("\n--- 1. Busqueda de patrones: Fuerza Bruta vs KMP ---")

analizador = TextAnalyzer(alertas=["error", "falla", "intrusion", "critico"])

# Caso 1: patron sin repeticiones (ambos algoritmos similares)
texto_simple = "incidente normal en el sistema " * 500 + "falla critica detectada"
patron_simple = "falla critica detectada"
pos_fb  = analizador.search_fuerza_bruta(texto_simple, patron_simple)
pos_kmp = analizador.search_kmp(texto_simple, patron_simple)
print(f"  Caso A - patron sin repeticiones internas:")
print(f"  Texto: {len(texto_simple)} chars, patron: '{patron_simple}'")
print(f"  FB={pos_fb}, KMP={pos_kmp}")

REPS = 200
t_fb_a  = timeit.timeit(lambda: analizador.search_fuerza_bruta(texto_simple, patron_simple), number=REPS) / REPS
t_kmp_a = timeit.timeit(lambda: analizador.search_kmp(texto_simple, patron_simple), number=REPS) / REPS
print(f"  FB: {t_fb_a:.5f}s  KMP: {t_kmp_a:.5f}s  mejora: {t_fb_a/t_kmp_a:.1f}x")

# Caso 2: patron con muchas repeticiones parciales (peor caso real de fuerza bruta)
# FB debe reiniciar desde cero cada vez que falla en el último carácter
texto_peor = ("aa" * 2000) + "aab"
patron_rep  = "a" * 15 + "b"   # "aaaaaaaaaaaaaaab"
pos_fb2  = analizador.search_fuerza_bruta(texto_peor, patron_rep)
pos_kmp2 = analizador.search_kmp(texto_peor, patron_rep)
print(f"\n  Caso B - patron con repeticiones internas (peor caso para FB):")
print(f"  Texto: {len(texto_peor)} chars de 'aa...', patron: '{patron_rep}'")
print(f"  FB={pos_fb2}, KMP={pos_kmp2}")

t_fb_b  = timeit.timeit(lambda: analizador.search_fuerza_bruta(texto_peor, patron_rep), number=REPS) / REPS
t_kmp_b = timeit.timeit(lambda: analizador.search_kmp(texto_peor, patron_rep), number=REPS) / REPS
print(f"  FB: {t_fb_b:.5f}s  KMP: {t_kmp_b:.5f}s  mejora: {t_fb_b/t_kmp_b:.1f}x")

print(f"\n  Analisis: en ambos casos la implementacion Python pura de KMP es igual")
print(f"  o mas lenta que FB. Motivo: texto[i:i+m]==patron en FB se ejecuta en C")
print(f"  (nivel nativo) con SIMD/memcmp, mientras que KMP recorre el texto")
print(f"  caracter a caracter en Python con overhead del interprete.")
print(f"  Complejidad teorica: FB=O(n*m), KMP=O(n+m). La ventaja de KMP es real")
print(f"  en lenguajes compilados (C, Java, Go) o con textos/patrones mucho mayores.")
print(f"  Leccion: complejidad asintotica != rendimiento practico en Python puro.")

# ---------------------------------------------------------------------------
# Sección 2 — RSA demostrativo
# ---------------------------------------------------------------------------

print("\n--- 2. RSA demostrativo: cifrado de clave publica ---")

# Generacion de claves con primos pequeños (solo educativo)
rsa = RSADemo(p=61, q=53)
print(f"  {rsa}")
print(f"  n = p*q = {rsa.p}*{rsa.q} = {rsa.n}")
print(f"  phi(n) = (p-1)*(q-1) = {(rsa.p-1)*(rsa.q-1)}")
print(f"  Clave publica  (e, n) = {rsa.clave_publica}")
print(f"  Clave privada  (d, n) = {rsa.clave_privada}")
print(f"  Verificacion: e*d mod phi = {(rsa.e * rsa.d) % ((rsa.p-1)*(rsa.q-1))} (debe ser 1)")

# Cifrar un número
m = 42
c = rsa.cifrar(m)
m2 = rsa.descifrar(c)
print(f"\n  Cifrar m={m}: c = {m}^{rsa.e} mod {rsa.n} = {c}")
print(f"  Descifrar c={c}: m = {c}^{rsa.d} mod {rsa.n} = {m2}")
print(f"  Recuperado correctamente: {m == m2}")

# Cifrar un string de alerta
alerta = "ALERTA"
cifrado = rsa.cifrar_texto(alerta)
recuperado = rsa.descifrar_texto(cifrado)
print(f"\n  Cifrar texto '{alerta}':")
print(f"    Caracteres cifrados: {cifrado}")
print(f"    Texto recuperado: '{recuperado}'")
print(f"    Integro: {alerta == recuperado}")

print(f"\n  Aplicacion al sistema: un nodo origen puede firmar digitalmente")
print(f"  el campo 'origen' del Event con su clave privada. El receptor")
print(f"  verifica con la clave publica, garantizando autenticidad.")
print(f"\n  Nota de seguridad: n={rsa.n} es factorizable trivialmente.")
print(f"  RSA seguro requiere primos de 1024+ bits (n de ~300 digitos).")

# Demostrar que sin la clave privada no se puede descifrar
print(f"\n  Demostracion de confidencialidad:")
print(f"    Mensaje original m=65 (letra 'A')")
c65 = rsa.cifrar(65)
print(f"    Cifrado con clave publica (e={rsa.e}, n={rsa.n}): {c65}")
print(f"    Para descifrar se necesita d={rsa.d} (secreto).")
print(f"    Obtener d requiere factorizar n={rsa.n} = {rsa.p}*{rsa.q}.")

# ---------------------------------------------------------------------------
# Sección 3 — Knapsack 0/1: selección óptima de incidentes
# ---------------------------------------------------------------------------

print("\n--- 3. Knapsack 0/1: seleccion optima de incidentes ---")

# Contexto: el sistema tiene capacidad de procesar 10 unidades de tiempo.
# Cada incidente tiene un costo de procesamiento y una prioridad (valor).
incidentes = [
    {"nombre": "Caida de servidor", "costo": 4, "prioridad": 8},
    {"nombre": "Falla de red",       "costo": 3, "prioridad": 7},
    {"nombre": "Alerta de memoria",  "costo": 2, "prioridad": 4},
    {"nombre": "Intrusion detectada","costo": 5, "prioridad": 9},
    {"nombre": "Disco lleno",        "costo": 1, "prioridad": 3},
    {"nombre": "Servicio caido",     "costo": 3, "prioridad": 6},
]

CAPACIDAD = 10
costos    = [inc["costo"]     for inc in incidentes]
prioridades = [inc["prioridad"] for inc in incidentes]

print(f"\n  Capacidad de procesamiento disponible: {CAPACIDAD} unidades")
print(f"\n  {'Incidente':<25} {'Costo':>6} {'Prioridad':>10}")
print("  " + "-" * 43)
for inc in incidentes:
    print(f"  {inc['nombre']:<25} {inc['costo']:>6}     {inc['prioridad']:>6}")

valor_opt, seleccionados = knapsack(CAPACIDAD, costos, prioridades)

print(f"\n  Solucion optima (Knapsack 0/1):")
print(f"  {'Incidente':<25} {'Costo':>6} {'Prioridad':>10}")
print("  " + "-" * 43)
costo_total = 0
for idx in seleccionados:
    inc = incidentes[idx]
    costo_total += inc["costo"]
    print(f"  {inc['nombre']:<25} {inc['costo']:>6}     {inc['prioridad']:>6}")
print(f"\n  Costo total usado: {costo_total}/{CAPACIDAD}")
print(f"  Prioridad total atendida: {valor_opt}")

# Comparar con greedy ratio (para mostrar que no es optimo en 0/1)
print(f"\n  Comparacion con greedy (mayor ratio prioridad/costo):")
ratios = sorted(enumerate(incidentes), key=lambda x: x[1]["prioridad"]/x[1]["costo"], reverse=True)
greedy_sel = []
greedy_costo = 0
greedy_valor = 0
for idx, inc in ratios:
    if greedy_costo + inc["costo"] <= CAPACIDAD:
        greedy_sel.append(idx)
        greedy_costo += inc["costo"]
        greedy_valor += inc["prioridad"]

print(f"  Incidentes greedy: {[incidentes[i]['nombre'] for i in sorted(greedy_sel)]}")
print(f"  Prioridad greedy: {greedy_valor}  vs  DP optimo: {valor_opt}")
if greedy_valor < valor_opt:
    print(f"  Greedy es SUBOPTIMO en {valor_opt - greedy_valor} unidades de prioridad.")
else:
    print(f"  En este caso greedy coincide con el optimo (no siempre ocurre).")

# ---------------------------------------------------------------------------
# Sección 4 — Medición de tiempos Knapsack
# ---------------------------------------------------------------------------

print("\n--- 4. Escalabilidad de Knapsack (timeit) ---")

def generar_instancia(n: int, cap: int, seed: int = 0) -> tuple:
    random.seed(seed)
    costos_r   = [random.randint(1, cap // 3) for _ in range(n)]
    valores_r  = [random.randint(1, 20)       for _ in range(n)]
    return cap, costos_r, valores_r

casos = [(10, 50), (20, 100), (50, 200), (100, 500)]
REPS2 = 50

print(f"\n  {'N items':>8}  {'Capacidad':>10}  {'Tiempo DP':>12}  {'Tiempo DP-opt':>14}")
print("  " + "-" * 50)
for n, cap in casos:
    cap_r, cos_r, val_r = generar_instancia(n, cap)
    t_dp  = timeit.timeit(lambda: knapsack(cap_r, cos_r, val_r), number=REPS2) / REPS2
    t_opt = timeit.timeit(lambda: knapsack_optimizado(cap_r, cos_r, val_r), number=REPS2) / REPS2
    print(f"  {n:>8}  {cap_r:>10}  {t_dp:>12.5f}s  {t_opt:>14.5f}s")

print(f"""
  Analisis:
  - DP completo: O(n*W) tiempo y espacio. Permite reconstruir que items
    se eligieron (necesario para saber cuales incidentes procesar).
  - DP optimizado: O(n*W) tiempo pero O(W) espacio (una sola fila).
    Mas rapido en la practica por mejor localidad de cache.
  - Fuerza bruta (no implementada): O(2^n) — inviable para n>30.
  - La ventaja de DP sobre greedy: garantiza el optimo global en 0/1.
""")

print("=" * 62)
print("Paso 8 completado.")
