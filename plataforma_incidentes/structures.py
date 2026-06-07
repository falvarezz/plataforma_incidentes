"""
Módulo: structures.py
Estructuras de datos lineales: Queue (FIFO), Stack (LIFO) y PriorityQueue (heap).

Todas usan las estructuras nativas de Python para garantizar eficiencia:
  - collections.deque  → O(1) en ambos extremos (no O(n) como list.insert(0,...))
  - heapq              → O(log n) en push/pop, O(1) en peek

Decisión de diseño: encapsular deque y heapq en clases propias permite
documentar la interfaz, agregar validaciones y hacer el código más legible
en el resto del sistema (EventStore, Router), sin cambiar la implementación interna.
"""
from collections import deque
from typing import Any, List, Optional, Tuple
import heapq

from .event import Event


# ---------------------------------------------------------------------------
# Queue (Cola FIFO)
# ---------------------------------------------------------------------------

class Queue:
    """
    Cola FIFO (First In, First Out) para procesamiento de eventos en orden de llegada.

    Caso de uso: encolar eventos a medida que ingresan al sistema y
    procesarlos en el mismo orden (ej: pipeline de ingesta).

    Decisión de diseño: se usa collections.deque en lugar de list porque
    list.pop(0) es O(n) (desplaza todos los elementos), mientras que
    deque.popleft() es O(1) gracias a su implementación como lista doblemente enlazada.

    Attributes:
        _cola (deque): Estructura interna de doble extremo.
    """

    def __init__(self):
        """Inicializa una cola vacía."""
        self._cola: deque = deque()

    def enqueue(self, event: Event) -> None:
        """
        Agrega un evento al final de la cola.

        Args:
            event: Evento a encolar.

        Complexity: O(1).
        """
        self._cola.append(event)

    def dequeue(self) -> Optional[Event]:
        """
        Extrae y retorna el evento del frente de la cola (el más antiguo).

        Returns:
            El Event más antiguo, o None si la cola está vacía.

        Complexity: O(1).
        """
        if self.is_empty():
            return None
        return self._cola.popleft()

    def peek(self) -> Optional[Event]:
        """
        Retorna el evento del frente sin extraerlo.

        Returns:
            El primer Event o None si la cola está vacía.

        Complexity: O(1).
        """
        return self._cola[0] if self._cola else None

    def is_empty(self) -> bool:
        """Retorna True si la cola no tiene elementos."""
        return len(self._cola) == 0

    def __len__(self) -> int:
        return len(self._cola)

    def __repr__(self) -> str:
        return f"Queue(size={len(self._cola)})"


# ---------------------------------------------------------------------------
# Stack (Pila LIFO)
# ---------------------------------------------------------------------------

class Stack:
    """
    Pila LIFO (Last In, First Out) para historial de eventos o deshacer operaciones.

    Caso de uso: registrar el historial de eventos procesados para poder
    "deshacer" la última operación o hacer rollback del estado del sistema.

    Decisión de diseño: se usa deque en lugar de list para consistencia con Queue
    y para aprovechar el append/pop O(1) garantizado. (list.pop() también es O(1)
    al final, pero deque tiene menor overhead de memoria en listas grandes.)

    Attributes:
        _pila (deque): Estructura interna.
    """

    def __init__(self):
        """Inicializa una pila vacía."""
        self._pila: deque = deque()

    def push(self, event: Event) -> None:
        """
        Apila un evento en el tope.

        Args:
            event: Evento a apilar.

        Complexity: O(1).
        """
        self._pila.append(event)

    def pop(self) -> Optional[Event]:
        """
        Extrae y retorna el evento del tope (el más reciente).

        Returns:
            El Event más reciente, o None si la pila está vacía.

        Complexity: O(1).
        """
        if self.is_empty():
            return None
        return self._pila.pop()

    def peek(self) -> Optional[Event]:
        """
        Retorna el evento del tope sin extraerlo.

        Returns:
            El Event del tope o None si la pila está vacía.

        Complexity: O(1).
        """
        return self._pila[-1] if self._pila else None

    def is_empty(self) -> bool:
        """Retorna True si la pila no tiene elementos."""
        return len(self._pila) == 0

    def __len__(self) -> int:
        return len(self._pila)

    def __repr__(self) -> str:
        return f"Stack(size={len(self._pila)})"


# ---------------------------------------------------------------------------
# PriorityQueue (Cola de Prioridad con heap)
# ---------------------------------------------------------------------------

class PriorityQueue:
    """
    Cola de prioridad basada en un min-heap para atender primero los incidentes
    más críticos (menor valor de prioridad = mayor urgencia).

    Caso de uso: gestión de incidentes donde un evento con prioridad=1 (crítico)
    debe atenderse antes que uno con prioridad=3 (bajo).

    Decisión de diseño: se usa heapq porque mantiene el invariante de heap en O(log n)
    por operación, con O(1) para consultar el mínimo. Esto es más eficiente que
    mantener una lista ordenada (O(n) por inserción) cuando hay muchos eventos.

    La tupla (prioridad, contador, event) evita comparar objetos Event directamente
    y garantiza orden estable (FIFO) entre eventos de igual prioridad mediante
    un contador incremental.

    Attributes:
        _heap (List): Heap interno de tuplas (prioridad, contador, Event).
        _contador (int): Desempata eventos con igual prioridad (orden FIFO).
    """

    def __init__(self):
        """Inicializa la cola de prioridad vacía."""
        self._heap: List[Tuple[int, int, Event]] = []
        self._contador: int = 0

    def push(self, event: Event) -> None:
        """
        Inserta un evento en la cola respetando su prioridad.

        Args:
            event: Evento a insertar. Se usa event.prioridad como clave de orden.

        Complexity: O(log n).
        """
        heapq.heappush(self._heap, (event.prioridad, self._contador, event))
        self._contador += 1

    def pop(self) -> Optional[Event]:
        """
        Extrae y retorna el evento de mayor prioridad (menor valor numérico).

        Returns:
            El Event más urgente, o None si la cola está vacía.

        Complexity: O(log n).
        """
        if self.is_empty():
            return None
        _, _, event = heapq.heappop(self._heap)
        return event

    def peek(self) -> Optional[Event]:
        """
        Retorna el evento más urgente sin extraerlo.

        Returns:
            El Event de mayor prioridad o None si la cola está vacía.

        Complexity: O(1).
        """
        if self.is_empty():
            return None
        return self._heap[0][2]

    def is_empty(self) -> bool:
        """Retorna True si la cola no tiene elementos."""
        return len(self._heap) == 0

    def __len__(self) -> int:
        return len(self._heap)

    def __repr__(self) -> str:
        top = self._heap[0][2] if self._heap else None
        return f"PriorityQueue(size={len(self._heap)}, top={top})"
