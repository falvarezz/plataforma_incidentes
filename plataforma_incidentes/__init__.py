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

__all__ = ["Event", "EventStore", "Index", "Router", "TextAnalyzer", "Queue", "Stack", "PriorityQueue"]
