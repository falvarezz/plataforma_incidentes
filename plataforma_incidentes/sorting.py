"""
Módulo: sorting.py
Algoritmos de ordenamiento sobre listas de eventos.

Implementaciones:
  - Insertion Sort : O(n²) — eficiente para listas pequeñas o casi ordenadas
  - Merge Sort     : O(n log n) — estable, eficiente en cualquier caso
  - Python sorted(): O(n log n) — Timsort (hibrido insertion + merge) en C

Decisión de diseño: todos los algoritmos reciben una función key para
ordenar por cualquier atributo de Event (prioridad, id, timestamp),
lo que los hace reutilizables sin duplicar código.
"""
from typing import Callable, List, Any
from .event import Event


def insertion_sort(eventos: List[Event], key: Callable[[Event], Any] = lambda e: e.prioridad) -> List[Event]:
    """
    Ordena una lista de eventos usando Insertion Sort.

    Construye la lista ordenada de izquierda a derecha: toma cada elemento
    y lo inserta en la posición correcta dentro del subarray ya ordenado.

    Ventaja práctica: muy eficiente cuando la lista ya está casi ordenada
    (O(n) en el mejor caso), común en streams de eventos con timestamps.

    Args:
        eventos: Lista a ordenar (no se modifica el original).
        key: Función que extrae la clave de comparación. Default: prioridad.

    Returns:
        Nueva lista ordenada de menor a mayor según key.

    Complexity:
        - Mejor caso  : O(n)   — lista ya ordenada
        - Caso promedio: O(n²)
        - Peor caso   : O(n²)  — lista en orden inverso
        - Espacio     : O(1)   — in-place (sobre la copia)
    """
    resultado = list(eventos)
    for i in range(1, len(resultado)):
        actual = resultado[i]
        j = i - 1
        while j >= 0 and key(resultado[j]) > key(actual):
            resultado[j + 1] = resultado[j]
            j -= 1
        resultado[j + 1] = actual
    return resultado


def merge_sort(eventos: List[Event], key: Callable[[Event], Any] = lambda e: e.prioridad) -> List[Event]:
    """
    Ordena una lista de eventos usando Merge Sort (divide y conquista).

    Divide la lista en mitades recursivamente hasta llegar a sublistas de
    un elemento, luego las fusiona en orden creciente.

    Ventaja práctica: rendimiento garantizado O(n log n) en todos los casos,
    estable (mantiene el orden relativo de elementos con igual prioridad).

    Args:
        eventos: Lista a ordenar (no se modifica el original).
        key: Función que extrae la clave de comparación. Default: prioridad.

    Returns:
        Nueva lista ordenada de menor a mayor según key.

    Complexity:
        - Todos los casos: O(n log n)
        - Espacio        : O(n) — requiere memoria auxiliar para fusionar
    """
    if len(eventos) <= 1:
        return list(eventos)

    mid = len(eventos) // 2
    izquierda = merge_sort(eventos[:mid], key)
    derecha   = merge_sort(eventos[mid:], key)
    return _merge(izquierda, derecha, key)


def _merge(izq: List[Event], der: List[Event], key: Callable[[Event], Any]) -> List[Event]:
    """Fusiona dos sublistas ordenadas en una sola lista ordenada."""
    resultado = []
    i = j = 0
    while i < len(izq) and j < len(der):
        if key(izq[i]) <= key(der[j]):
            resultado.append(izq[i])
            i += 1
        else:
            resultado.append(der[j])
            j += 1
    resultado.extend(izq[i:])
    resultado.extend(der[j:])
    return resultado


def python_sort(eventos: List[Event], key: Callable[[Event], Any] = lambda e: e.prioridad) -> List[Event]:
    """
    Ordena usando el sorted() nativo de Python (Timsort).

    Timsort es un algoritmo híbrido (Insertion Sort + Merge Sort) implementado
    en C, optimizado para datos del mundo real con runs parcialmente ordenados.
    Es el estándar de comparación para evaluar implementaciones propias.

    Args:
        eventos: Lista a ordenar.
        key: Función clave de comparación.

    Returns:
        Nueva lista ordenada.

    Complexity: O(n log n) en todos los casos.
    """
    return sorted(eventos, key=key)
