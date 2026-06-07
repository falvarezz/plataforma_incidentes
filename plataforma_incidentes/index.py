"""
Módulo: index.py
Índice por clave para acceso en tiempo promedio O(1) mediante hashing.
"""
from typing import Any, List, Optional
from .event import Event


class Index:
    """
    Índice hash que mapea una clave de evento a su instancia.

    Decisión de diseño: se usa un diccionario de Python (tabla hash interna)
    porque ofrece inserción y búsqueda en O(1) promedio. Esto contrasta con
    la búsqueda secuencial O(n) del EventStore cuando el volumen de datos crece.

    Permite indexar por cualquier atributo del Event (id, categoria, origen, etc.).

    Attributes:
        _key_attr (str): Nombre del atributo de Event usado como clave del índice.
        _tabla (dict): Tabla hash interna; clave → lista de Events con esa clave.
    """

    def __init__(self, key_attr: str = "id"):
        """
        Inicializa el índice especificando el atributo clave.

        Args:
            key_attr: Atributo de Event que actúa como clave (default: 'id').
                      Usar 'id' para índice único; 'categoria' u 'origen'
                      para índices multi-valor.
        """
        self._key_attr = key_attr
        self._tabla: dict[Any, List[Event]] = {}

    def insert(self, event: Event) -> None:
        """
        Inserta un evento en el índice usando el atributo clave configurado.

        Args:
            event: Evento a indexar.

        Complexity: O(1) promedio.
        """
        key = getattr(event, self._key_attr)
        if key not in self._tabla:
            self._tabla[key] = []
        self._tabla[key].append(event)

    def search(self, key: Any) -> List[Event]:
        """
        Retorna todos los eventos asociados a una clave.

        Args:
            key: Valor de la clave a buscar (ej: 'EVT-001' para id, 'red' para categoria).

        Returns:
            Lista de eventos con esa clave, o lista vacía si no existe.

        Complexity: O(1) promedio (acceso a tabla hash).
        """
        return self._tabla.get(key, [])

    def search_one(self, key: Any) -> Optional[Event]:
        """
        Retorna el primer evento asociado a una clave (útil para índice por id).

        Args:
            key: Valor de la clave a buscar.

        Returns:
            Primer Event encontrado o None.

        Complexity: O(1) promedio.
        """
        resultados = self._tabla.get(key, [])
        return resultados[0] if resultados else None

    def keys(self) -> List[Any]:
        """Retorna todas las claves presentes en el índice."""
        return list(self._tabla.keys())

    def __len__(self) -> int:
        """Retorna la cantidad de claves únicas en el índice."""
        return len(self._tabla)

    def __repr__(self) -> str:
        return f"Index(key_attr={self._key_attr!r}, claves_unicas={len(self._tabla)})"
