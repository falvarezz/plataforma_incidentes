"""
Plataforma de análisis de incidentes y rutas.
Módulos: Event, EventStore, Index, Router, TextAnalyzer, Queue, Stack, PriorityQueue.
"""
from .event import Event
from .event_store import EventStore
from .index import Index
from .router import Router
from .text_analyzer import TextAnalyzer
from .structures import Queue, Stack, PriorityQueue
from .search import busqueda_secuencial, busqueda_binaria, busqueda_bisect
from .sorting import insertion_sort, merge_sort, python_sort

__all__ = [
    "Event", "EventStore", "Index", "Router", "TextAnalyzer",
    "Queue", "Stack", "PriorityQueue",
    "busqueda_secuencial", "busqueda_binaria", "busqueda_bisect",
    "insertion_sort", "merge_sort", "python_sort",
]
