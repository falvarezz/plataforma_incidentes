"""
Módulo: search.py
Algoritmos de búsqueda sobre listas de eventos: secuencial y binaria.

Comparativa de complejidad:
  - Búsqueda secuencial : O(n)         — no requiere orden previo
  - Búsqueda binaria    : O(log n)     — requiere lista ordenada
  - bisect              : O(log n)     — búsqueda binaria nativa de Python (C)
"""
import bisect
from typing import List, Optional
from .event import Event


def busqueda_secuencial(eventos: List[Event], id_buscado: str) -> Optional[Event]:
    """
    Busca un evento por ID recorriendo la lista de principio a fin.

    No requiere que la lista esté ordenada. Caso promedio y peor caso O(n).

    Args:
        eventos: Lista de eventos donde buscar.
        id_buscado: ID del evento a encontrar.

    Returns:
        El Event con ese ID, o None si no existe.

    Complexity: O(n) — recorre hasta n elementos en el peor caso.
    """
    for evento in eventos:
        if evento.id == id_buscado:
            return evento
    return None


def busqueda_binaria(eventos: List[Event], id_buscado: str) -> Optional[Event]:
    """
    Busca un evento por ID usando búsqueda binaria manual.

    Requiere que la lista esté ordenada por ID (orden lexicográfico).
    Divide el espacio de búsqueda a la mitad en cada paso.

    Args:
        eventos: Lista de eventos ordenada por Event.id.
        id_buscado: ID a buscar.

    Returns:
        El Event con ese ID, o None si no existe.

    Complexity: O(log n) — descarta la mitad del espacio en cada iteración.
    """
    izq, der = 0, len(eventos) - 1
    while izq <= der:
        mid = (izq + der) // 2
        if eventos[mid].id == id_buscado:
            return eventos[mid]
        elif eventos[mid].id < id_buscado:
            izq = mid + 1
        else:
            der = mid - 1
    return None


def busqueda_bisect(eventos: List[Event], id_buscado: str) -> Optional[Event]:
    """
    Busca un evento por ID usando el módulo bisect de Python (implementación en C).

    Extrae los IDs a una lista auxiliar y usa bisect_left para localizar
    la posición de inserción, luego verifica si el elemento coincide.

    Args:
        eventos: Lista de eventos ordenada por Event.id.
        id_buscado: ID a buscar.

    Returns:
        El Event con ese ID, o None si no existe.

    Complexity: O(log n) para bisect + O(n) para extraer IDs.
    Nota: más eficiente en benchmarks repetidos si se precalcula la lista de IDs.
    """
    ids = [e.id for e in eventos]
    pos = bisect.bisect_left(ids, id_buscado)
    if pos < len(eventos) and eventos[pos].id == id_buscado:
        return eventos[pos]
    return None
