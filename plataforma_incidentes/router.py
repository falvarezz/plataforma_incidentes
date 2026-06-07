"""
Módulo: router.py
Modela la red de rutas entre nodos como un grafo dirigido (origen -> destino).

Nota: en la Parte 1 se define la estructura base. Los algoritmos de recorrido
(BFS, DFS, Dijkstra) se implementarán en la Parte 2.
"""
from typing import Dict, List, Optional, Tuple


class Router:
    """
    Grafo dirigido que representa la red de rutas entre nodos del sistema.

    Decisión de diseño: se usa lista de adyacencia (dict de listas) en lugar
    de matriz de adyacencia porque el grafo de incidentes es típicamente disperso
    (pocos arcos por nodo), lo que hace la lista más eficiente en memoria: O(V+E)
    frente a O(V²) de la matriz.

    Cada arco puede tener un peso opcional (ej: latencia, costo de ruta).

    Attributes:
        _grafo (Dict[str, List[Tuple[str, float]]]): Lista de adyacencia.
                clave = nodo origen, valor = lista de (nodo_destino, peso).
    """

    def __init__(self):
        """Inicializa el grafo con una lista de adyacencia vacía."""
        self._grafo: Dict[str, List[Tuple[str, float]]] = {}

    def add_node(self, nodo: str) -> None:
        """
        Agrega un nodo al grafo sin arcos.

        Args:
            nodo: Nombre del nodo a agregar.

        Complexity: O(1).
        """
        if nodo not in self._grafo:
            self._grafo[nodo] = []

    def add_edge(self, origen: str, destino: str, peso: float = 1.0) -> None:
        """
        Agrega un arco dirigido entre dos nodos.

        Crea los nodos automáticamente si no existen.

        Args:
            origen: Nodo de partida.
            destino: Nodo de llegada.
            peso: Costo o latencia del arco (default: 1.0).

        Complexity: O(1).
        """
        self.add_node(origen)
        self.add_node(destino)
        self._grafo[origen].append((destino, peso))

    def get_neighbors(self, nodo: str) -> List[Tuple[str, float]]:
        """
        Retorna los nodos adyacentes (vecinos) de un nodo dado.

        Args:
            nodo: Nodo del que se quieren los vecinos.

        Returns:
            Lista de tuplas (nodo_destino, peso). Lista vacía si el nodo no existe.

        Complexity: O(1).
        """
        return self._grafo.get(nodo, [])

    def get_nodes(self) -> List[str]:
        """Retorna todos los nodos del grafo."""
        return list(self._grafo.keys())

    def has_path(self, origen: str, destino: str) -> bool:
        """
        Verifica si existe al menos un arco directo entre origen y destino.

        Args:
            origen: Nodo de partida.
            destino: Nodo de llegada.

        Returns:
            True si hay arco directo, False en caso contrario.

        Complexity: O(grado(origen)).
        """
        return any(d == destino for d, _ in self._grafo.get(origen, []))

    def __repr__(self) -> str:
        nodos = len(self._grafo)
        arcos = sum(len(v) for v in self._grafo.values())
        return f"Router(nodos={nodos}, arcos={arcos})"
