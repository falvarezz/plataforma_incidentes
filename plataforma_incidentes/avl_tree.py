"""
Módulo: avl_tree.py
Árbol AVL (Adelson-Velsky y Landis) — árbol binario de búsqueda autobalanceado.

Un AVL mantiene el invariante: para todo nodo, la diferencia de altura entre
su subárbol izquierdo y derecho (factor de balance) es -1, 0 o +1.
Esto garantiza O(log n) en inserción y búsqueda en todos los casos,
a diferencia del BST simple que degenera a O(n) con datos ordenados.

Decisión de diseño: se elige AVL sobre Rojo-Negro porque:
  - Las rotaciones son más simples de implementar y explicar.
  - Búsquedas más rápidas en la práctica (árbol más estrictamente balanceado).
  - Rojo-Negro favorece inserciones/eliminaciones frecuentes; AVL favorece
    lecturas frecuentes — patrón típico de un sistema de consulta de incidentes.

Aplicación al caso: el AVL actúa como índice ordenado de eventos, permitiendo
búsqueda por rango (ej: todos los eventos con prioridad entre 1 y 3) en O(log n),
algo que el Index basado en dict no puede hacer eficientemente.
"""
from typing import Any, List, Optional, Tuple


class _Nodo:
    """Nodo interno del AVL."""

    def __init__(self, clave: Any, valor: Any):
        self.clave  = clave
        self.valor  = valor
        self.izq:   Optional["_Nodo"] = None
        self.der:   Optional["_Nodo"] = None
        self.altura: int = 1


class AVLTree:
    """
    Árbol AVL genérico que asocia claves comparables con valores arbitrarios.

    Soporta claves de cualquier tipo ordenable (int, str, float).
    Para indexar eventos se recomienda usar el id o la prioridad como clave.

    Attributes:
        _raiz (_Nodo | None): Raíz del árbol.
        _size (int): Cantidad de nodos.
    """

    def __init__(self):
        """Inicializa un árbol AVL vacío."""
        self._raiz: Optional[_Nodo] = None
        self._size: int = 0

    # ------------------------------------------------------------------
    # API pública
    # ------------------------------------------------------------------

    def insert(self, clave: Any, valor: Any) -> None:
        """
        Inserta un par (clave, valor) y rebalancea el árbol si es necesario.

        Si la clave ya existe, actualiza su valor.

        Args:
            clave: Clave de ordenamiento (debe ser comparable con < y >).
            valor: Valor asociado a la clave.

        Complexity: O(log n) — la altura del AVL está acotada a 1.44·log₂(n).
        """
        self._raiz = self._insert(self._raiz, clave, valor)

    def search(self, clave: Any) -> Optional[Any]:
        """
        Busca el valor asociado a una clave.

        Args:
            clave: Clave a buscar.

        Returns:
            El valor asociado, o None si no existe.

        Complexity: O(log n).
        """
        nodo = self._search(self._raiz, clave)
        return nodo.valor if nodo else None

    def range_search(self, clave_min: Any, clave_max: Any) -> List[Tuple[Any, Any]]:
        """
        Retorna todos los pares (clave, valor) cuya clave está en [clave_min, clave_max].

        Esta operación es la ventaja clave del AVL sobre un dict:
        permite consultas por rango en O(log n + k), donde k = resultados encontrados.

        Args:
            clave_min: Límite inferior del rango (inclusivo).
            clave_max: Límite superior del rango (inclusivo).

        Returns:
            Lista de tuplas (clave, valor) ordenadas por clave.

        Complexity: O(log n + k).
        """
        resultados: List[Tuple[Any, Any]] = []
        self._range_search(self._raiz, clave_min, clave_max, resultados)
        return resultados

    def inorder(self) -> List[Tuple[Any, Any]]:
        """
        Recorre el árbol en inorder (izquierda → raíz → derecha).

        El recorrido inorder de un BST/AVL siempre produce las claves en orden
        ascendente — propiedad fundamental del árbol de búsqueda binaria.

        Returns:
            Lista de tuplas (clave, valor) ordenadas por clave.

        Complexity: O(n).
        """
        resultado: List[Tuple[Any, Any]] = []
        self._inorder(self._raiz, resultado)
        return resultado

    def height(self) -> int:
        """Retorna la altura del árbol (0 si está vacío)."""
        return self._altura(self._raiz)

    def __len__(self) -> int:
        return self._size

    def __repr__(self) -> str:
        return f"AVLTree(nodos={self._size}, altura={self.height()})"

    # ------------------------------------------------------------------
    # Métodos internos — inserción y balanceo
    # ------------------------------------------------------------------

    def _insert(self, nodo: Optional[_Nodo], clave: Any, valor: Any) -> _Nodo:
        """Inserción recursiva con rebalanceo post-inserción."""
        # Caso base: posición vacía → crear nodo
        if nodo is None:
            self._size += 1
            return _Nodo(clave, valor)

        if clave < nodo.clave:
            nodo.izq = self._insert(nodo.izq, clave, valor)
        elif clave > nodo.clave:
            nodo.der = self._insert(nodo.der, clave, valor)
        else:
            nodo.valor = valor   # actualizar valor existente
            return nodo

        # Actualizar altura del nodo actual
        self._actualizar_altura(nodo)

        # Verificar y corregir el balance
        return self._rebalancear(nodo, clave)

    def _rebalancear(self, nodo: _Nodo, clave_insertada: Any) -> _Nodo:
        """
        Aplica la rotación necesaria según el factor de balance y la posición
        de la clave insertada. Existen cuatro casos:

        Caso LL (izquierda-izquierda): rotación simple derecha.
        Caso RR (derecha-derecha):     rotación simple izquierda.
        Caso LR (izquierda-derecha):   rotación doble (izq sobre hijo, der sobre nodo).
        Caso RL (derecha-izquierda):   rotación doble (der sobre hijo, izq sobre nodo).
        """
        balance = self._factor_balance(nodo)

        # Caso LL: subárbol izquierdo pesa más y la clave fue a la izquierda
        if balance > 1 and clave_insertada < nodo.izq.clave:
            return self._rotar_derecha(nodo)

        # Caso RR: subárbol derecho pesa más y la clave fue a la derecha
        if balance < -1 and clave_insertada > nodo.der.clave:
            return self._rotar_izquierda(nodo)

        # Caso LR: subárbol izquierdo pesa más pero la clave fue a la derecha del hijo
        if balance > 1 and clave_insertada > nodo.izq.clave:
            nodo.izq = self._rotar_izquierda(nodo.izq)
            return self._rotar_derecha(nodo)

        # Caso RL: subárbol derecho pesa más pero la clave fue a la izquierda del hijo
        if balance < -1 and clave_insertada < nodo.der.clave:
            nodo.der = self._rotar_derecha(nodo.der)
            return self._rotar_izquierda(nodo)

        return nodo   # árbol ya balanceado

    def _rotar_derecha(self, z: _Nodo) -> _Nodo:
        """
        Rotación simple a la derecha sobre el nodo z.

        Antes:          Después:
             z               y
            / \\            / \\
           y   T4          x   z
          / \\            / \\ / \\
         x  T3          T1 T2 T3 T4

        El hijo izquierdo y sube; z pasa a ser hijo derecho de y.
        Se actualizan las alturas de z primero (ahora es hoja en ese nivel)
        y luego de y (nueva raíz del subárbol).
        """
        y = z.izq
        T3 = y.der

        y.der = z
        z.izq = T3

        self._actualizar_altura(z)
        self._actualizar_altura(y)
        return y

    def _rotar_izquierda(self, z: _Nodo) -> _Nodo:
        """
        Rotación simple a la izquierda sobre el nodo z.

        Antes:      Después:
           z             y
          / \\          / \\
         T1  y         z   x
            / \\      / \\ / \\
           T2  x    T1 T2 T3 T4

        El hijo derecho y sube; z pasa a ser hijo izquierdo de y.
        """
        y = z.der
        T2 = y.izq

        y.izq = z
        z.der = T2

        self._actualizar_altura(z)
        self._actualizar_altura(y)
        return y

    # ------------------------------------------------------------------
    # Métodos auxiliares
    # ------------------------------------------------------------------

    def _altura(self, nodo: Optional[_Nodo]) -> int:
        """Altura de un nodo (0 si es None)."""
        return nodo.altura if nodo else 0

    def _actualizar_altura(self, nodo: _Nodo) -> None:
        """Recalcula la altura de un nodo a partir de sus hijos."""
        nodo.altura = 1 + max(self._altura(nodo.izq), self._altura(nodo.der))

    def _factor_balance(self, nodo: Optional[_Nodo]) -> int:
        """
        Factor de balance = altura(izq) - altura(der).
        > 1  → subárbol izquierdo demasiado alto (rotar derecha).
        < -1 → subárbol derecho demasiado alto (rotar izquierda).
        """
        if nodo is None:
            return 0
        return self._altura(nodo.izq) - self._altura(nodo.der)

    def _search(self, nodo: Optional[_Nodo], clave: Any) -> Optional[_Nodo]:
        """Búsqueda binaria recursiva."""
        if nodo is None or nodo.clave == clave:
            return nodo
        if clave < nodo.clave:
            return self._search(nodo.izq, clave)
        return self._search(nodo.der, clave)

    def _range_search(
        self, nodo: Optional[_Nodo], cmin: Any, cmax: Any,
        resultado: List[Tuple[Any, Any]]
    ) -> None:
        """Recorrido inorder acotado al rango [cmin, cmax]."""
        if nodo is None:
            return
        if nodo.clave > cmin:
            self._range_search(nodo.izq, cmin, cmax, resultado)
        if cmin <= nodo.clave <= cmax:
            resultado.append((nodo.clave, nodo.valor))
        if nodo.clave < cmax:
            self._range_search(nodo.der, cmin, cmax, resultado)

    def _inorder(self, nodo: Optional[_Nodo], resultado: List[Tuple[Any, Any]]) -> None:
        """Recorrido inorder completo."""
        if nodo is None:
            return
        self._inorder(nodo.izq, resultado)
        resultado.append((nodo.clave, nodo.valor))
        self._inorder(nodo.der, resultado)
