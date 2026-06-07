"""
Módulo: event_store.py
Repositorio central en memoria para almacenar y consultar eventos.
"""
from typing import List, Optional
from .event import Event


class EventStore:
    """
    Almacén en memoria de objetos Event.

    Actúa como repositorio central del sistema: todos los eventos
    pasan por aquí antes de ser indexados o priorizados.

    Decisión de diseño: se usa una lista como colección interna porque
    permite recorrido secuencial O(n) para búsquedas lineales y
    preserva el orden de inserción (útil para auditoría cronológica).
    Para búsquedas rápidas por clave se delega al módulo Index.

    Attributes:
        _eventos (List[Event]): Colección interna de eventos almacenados.
    """

    def __init__(self):
        """Inicializa el almacén con una colección vacía."""
        self._eventos: List[Event] = []

    def add_event(self, event: Event) -> None:
        """
        Agrega un evento al almacén.

        Args:
            event: Instancia de Event a almacenar.

        Complexity: O(1) amortizado (append en lista de Python).
        """
        self._eventos.append(event)

    def get_all(self) -> List[Event]:
        """
        Retorna todos los eventos almacenados.

        Returns:
            Copia de la lista interna de eventos.

        Complexity: O(n).
        """
        return list(self._eventos)

    def get_by_categoria(self, categoria: str) -> List[Event]:
        """
        Filtra eventos por categoría mediante búsqueda secuencial.

        Args:
            categoria: Categoría a buscar.

        Returns:
            Lista de eventos que coinciden con la categoría.

        Complexity: O(n).
        """
        return [e for e in self._eventos if e.categoria == categoria]

    def get_by_id(self, id: str) -> Optional[Event]:
        """
        Busca un evento por su ID mediante búsqueda secuencial.

        Nota: para búsquedas frecuentes por ID usar Index.search() en su lugar (O(1)).

        Args:
            id: Identificador a buscar.

        Returns:
            El Event encontrado o None si no existe.

        Complexity: O(n).
        """
        for event in self._eventos:
            if event.id == id:
                return event
        return None

    def __len__(self) -> int:
        """Retorna la cantidad de eventos almacenados."""
        return len(self._eventos)

    def __repr__(self) -> str:
        return f"EventStore(total_eventos={len(self._eventos)})"
