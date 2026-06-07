"""
Módulo: event.py
Entidad base que representa un incidente dentro de la plataforma.
"""
from datetime import datetime


class Event:
    """
    Modela un incidente individual procesado por la plataforma.

    Attributes:
        id (str): Identificador único del evento.
        timestamp (datetime): Fecha y hora en que ocurrió el incidente.
        categoria (str): Tipo de incidente (ej: 'red', 'seguridad', 'hardware').
        prioridad (int): Nivel de severidad; menor valor = mayor prioridad (1=crítico).
        texto (str): Descripción textual del incidente.
        origen (str): Nodo o sistema donde se originó el evento.
        destino (str): Nodo o sistema al que se dirige o afecta el evento.
    """

    def __init__(
        self,
        id: str,
        timestamp: datetime,
        categoria: str,
        prioridad: int,
        texto: str,
        origen: str,
        destino: str,
    ):
        """
        Inicializa un Event con todos sus campos obligatorios.

        Args:
            id: Identificador único (ej: 'EVT-001').
            timestamp: Momento del incidente.
            categoria: Clasificación del incidente.
            prioridad: Severidad numérica (1 = más urgente).
            texto: Descripción del incidente.
            origen: Nodo de origen en la red.
            destino: Nodo de destino en la red.
        """
        self.id = id
        self.timestamp = timestamp
        self.categoria = categoria
        self.prioridad = prioridad
        self.texto = texto
        self.origen = origen
        self.destino = destino

    def __repr__(self) -> str:
        """Representación legible del evento para depuración."""
        return (
            f"Event(id={self.id!r}, categoria={self.categoria!r}, "
            f"prioridad={self.prioridad}, origen={self.origen!r} -> destino={self.destino!r})"
        )

    def __lt__(self, other: "Event") -> bool:
        """Permite comparar eventos por prioridad (necesario para heapq)."""
        return self.prioridad < other.prioridad
