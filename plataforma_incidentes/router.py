"""
Módulo: router.py
Modela la red de rutas entre nodos como un grafo dirigido (origen -> destino).

Parte 1: estructura base (add_node, add_edge, get_neighbors, has_path).
Parte 2 (Módulo 5): algoritmos de recorrido y caminos mínimos.
  - BFS  : recorrido en anchura, camino más corto en saltos O(V+E).
  - DFS  : recorrido en profundidad, detección de nodos alcanzables O(V+E).
  - Dijkstra: camino de menor costo con pesos O((V+E) log V).
  - Kruskal : árbol de expansión mínima sobre el grafo no dirigido O(E log E).
"""
from collections import deque
import heapq
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

    # ------------------------------------------------------------------
    # Módulo 5 — Algoritmos de recorrido y caminos mínimos
    # ------------------------------------------------------------------

    def bfs(self, origen: str) -> Tuple[Dict[str, int], Dict[str, Optional[str]]]:
        """
        Recorrido BFS (Breadth-First Search) desde un nodo origen.

        Procesa los nodos nivel por nivel usando una cola FIFO. Garantiza que
        el primer camino encontrado a cada nodo es el de menor cantidad de saltos.

        Uso en el sistema: detectar si un incidente puede propagarse de un nodo
        a otro, y en cuántos saltos mínimos.

        Args:
            origen: Nodo de partida.

        Returns:
            (distancias, predecesores)
            distancias: dict nodo -> saltos desde origen (None si inalcanzable).
            predecesores: dict nodo -> nodo previo en el camino más corto.

        Complexity: O(V + E).
        """
        distancias: Dict[str, int] = {origen: 0}
        predecesores: Dict[str, Optional[str]] = {origen: None}
        cola: deque = deque([origen])

        while cola:
            actual = cola.popleft()
            for vecino, _ in self._grafo.get(actual, []):
                if vecino not in distancias:
                    distancias[vecino] = distancias[actual] + 1
                    predecesores[vecino] = actual
                    cola.append(vecino)

        return distancias, predecesores

    def dfs(self, origen: str) -> List[str]:
        """
        Recorrido DFS (Depth-First Search) desde un nodo origen.

        Explora cada camino hasta su profundidad máxima antes de retroceder.
        Implementado de forma iterativa con una pila explícita para evitar
        desbordamiento de la pila de llamadas en grafos grandes.

        Uso en el sistema: encontrar todos los nodos alcanzables desde un origen
        (análisis de impacto de un incidente en la red).

        Args:
            origen: Nodo de partida.

        Returns:
            Lista de nodos en orden de primera visita.

        Complexity: O(V + E).
        """
        visitados: List[str] = []
        vistos = set()
        pila = [origen]

        while pila:
            actual = pila.pop()
            if actual in vistos:
                continue
            vistos.add(actual)
            visitados.append(actual)
            # Se agregan los vecinos en orden inverso para mantener el orden
            # lexicográfico de visita (el primero en la lista se procesa antes)
            for vecino, _ in reversed(self._grafo.get(actual, [])):
                if vecino not in vistos:
                    pila.append(vecino)

        return visitados

    def dijkstra(
        self, origen: str
    ) -> Tuple[Dict[str, float], Dict[str, Optional[str]]]:
        """
        Algoritmo de Dijkstra — camino de menor costo desde un nodo origen.

        Utiliza un min-heap (heapq) para extraer siempre el nodo no procesado
        con menor distancia acumulada. Solo funciona correctamente con pesos
        no negativos.

        Uso en el sistema: encontrar la ruta de menor latencia para enrutar
        una alerta entre dos nodos de la red.

        Args:
            origen: Nodo de partida.

        Returns:
            (distancias, predecesores)
            distancias: dict nodo -> costo mínimo desde origen (float('inf') si inalcanzable).
            predecesores: dict nodo -> nodo previo en el camino óptimo.

        Complexity: O((V + E) log V) con heap binario.
        """
        INF = float("inf")
        distancias: Dict[str, float] = {n: INF for n in self._grafo}
        distancias[origen] = 0.0
        predecesores: Dict[str, Optional[str]] = {n: None for n in self._grafo}

        heap = [(0.0, origen)]   # (costo_acumulado, nodo)
        procesados = set()

        while heap:
            costo, actual = heapq.heappop(heap)
            if actual in procesados:
                continue
            procesados.add(actual)

            for vecino, peso in self._grafo.get(actual, []):
                nuevo_costo = costo + peso
                if nuevo_costo < distancias.get(vecino, INF):
                    distancias[vecino] = nuevo_costo
                    predecesores[vecino] = actual
                    heapq.heappush(heap, (nuevo_costo, vecino))

        return distancias, predecesores

    def kruskal(self) -> List[Tuple[str, str, float]]:
        """
        Algoritmo de Kruskal — árbol de expansión mínima (MST).

        Trata el grafo como no dirigido (cada arco (u,v,w) se considera también
        como (v,u,w)). Ordena todos los arcos por peso y los agrega al MST si
        no crean un ciclo, usando Union-Find para la detección eficiente de ciclos.

        Uso en el sistema: encontrar la red de rutas de menor costo total que
        conecte todos los nodos (infraestructura mínima de monitoreo).

        Returns:
            Lista de tuplas (origen, destino, peso) que forman el MST,
            ordenadas por peso ascendente.

        Complexity: O(E log E) — dominado por el ordenamiento de arcos.
        """
        # Recolectar arcos únicos (grafo tratado como no dirigido)
        arcos_vistos = set()
        arcos = []
        for u, vecinos in self._grafo.items():
            for v, w in vecinos:
                clave = (min(u, v), max(u, v))
                if clave not in arcos_vistos:
                    arcos_vistos.add(clave)
                    arcos.append((w, u, v))

        arcos.sort()   # O(E log E)

        # Union-Find con compresión de camino y unión por rango
        padre = {n: n for n in self._grafo}
        rango  = {n: 0 for n in self._grafo}

        def encontrar(x: str) -> str:
            while padre[x] != x:
                padre[x] = padre[padre[x]]   # compresión de camino
                x = padre[x]
            return x

        def unir(x: str, y: str) -> bool:
            rx, ry = encontrar(x), encontrar(y)
            if rx == ry:
                return False   # misma componente → ciclo
            if rango[rx] < rango[ry]:
                rx, ry = ry, rx
            padre[ry] = rx
            if rango[rx] == rango[ry]:
                rango[rx] += 1
            return True

        mst: List[Tuple[str, str, float]] = []
        for peso, u, v in arcos:
            if unir(u, v):
                mst.append((u, v, peso))

        return mst

    def reconstruir_camino(
        self, predecesores: Dict[str, Optional[str]], destino: str
    ) -> List[str]:
        """
        Reconstruye el camino desde la fuente hasta un destino dado el dict
        de predecesores producido por BFS o Dijkstra.

        Args:
            predecesores: Dict nodo -> nodo previo (None en la fuente).
            destino: Nodo final del camino.

        Returns:
            Lista de nodos desde la fuente hasta el destino, en orden.
            Lista vacía si el destino no es alcanzable.

        Complexity: O(longitud del camino).
        """
        if destino not in predecesores:
            return []
        camino = []
        actual: Optional[str] = destino
        while actual is not None:
            camino.append(actual)
            actual = predecesores[actual]
        camino.reverse()
        return camino
