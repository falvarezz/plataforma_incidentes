"""
Módulo: hash_table.py
Tabla de dispersión propia con encadenamiento para manejo de colisiones.

Se implementa para demostrar el mecanismo interno del hashing.
En producción se usa Index (basado en dict de Python), que es más eficiente
porque su función hash y resolución de colisiones están implementadas en C.

Decisión de diseño — resolución de colisiones por ENCADENAMIENTO:
  Cada posición de la tabla contiene una lista de pares (clave, valor).
  Cuando dos claves producen el mismo índice, se agregan a esa lista.
  Ventaja: no requiere rehashing al llenarse un bucket.
  Desventaja: overhead de memoria por las listas auxiliares.

Comparado con DIRECCIONAMIENTO ABIERTO (usado internamente por Python):
  Python dict busca otra posición libre dentro de la misma tabla (probing).
  Más eficiente en caché pero requiere factor de carga < 0.7 para evitar degradación.
"""
from typing import Any, List, Optional, Tuple


class HashTable:
    """
    Tabla hash con encadenamiento (separate chaining).

    Attributes:
        _capacidad (int): Número de buckets de la tabla.
        _tabla (List[List]): Array de buckets; cada bucket es una lista de (key, value).
        _size (int): Cantidad total de pares almacenados.
    """

    # Factor de carga máximo antes de hacer rehash
    _LOAD_FACTOR_MAX = 0.75

    def __init__(self, capacidad: int = 16):
        """
        Inicializa la tabla con una capacidad inicial.

        Usar potencias de 2 como capacidad reduce colisiones al distribuir
        mejor los índices generados por la función hash.

        Args:
            capacidad: Número inicial de buckets (default: 16).
        """
        self._capacidad = capacidad
        self._tabla: List[List[Tuple[Any, Any]]] = [[] for _ in range(capacidad)]
        self._size = 0

    def _hash(self, clave: Any) -> int:
        """
        Función hash: convierte una clave en un índice de bucket.

        Usa el hash nativo de Python (que ya incorpora randomization)
        y aplica módulo para ajustar al rango [0, capacidad).

        Args:
            clave: Clave a hashear (debe ser hashable).

        Returns:
            Índice de bucket entre 0 y capacidad-1.

        Complexity: O(len(clave)) para strings, O(1) para enteros.
        """
        return hash(clave) % self._capacidad

    def insert(self, clave: Any, valor: Any) -> None:
        """
        Inserta o actualiza un par (clave, valor) en la tabla.

        Si la clave ya existe, actualiza su valor (no duplica).
        Si el factor de carga supera el umbral, hace rehash automático.

        Args:
            clave: Clave del par.
            valor: Valor asociado.

        Complexity: O(1) promedio, O(n) peor caso (todas las claves en un bucket).
        """
        if self._load_factor() >= self._LOAD_FACTOR_MAX:
            self._rehash()

        idx = self._hash(clave)
        bucket = self._tabla[idx]

        for i, (k, _) in enumerate(bucket):
            if k == clave:
                bucket[i] = (clave, valor)   # actualizar existente
                return

        bucket.append((clave, valor))
        self._size += 1

    def search(self, clave: Any) -> Optional[Any]:
        """
        Busca el valor asociado a una clave.

        Args:
            clave: Clave a buscar.

        Returns:
            El valor asociado, o None si la clave no existe.

        Complexity: O(1) promedio, O(k) donde k = tamaño del bucket (colisiones).
        """
        idx = self._hash(clave)
        for k, v in self._tabla[idx]:
            if k == clave:
                return v
        return None

    def delete(self, clave: Any) -> bool:
        """
        Elimina un par por clave.

        Args:
            clave: Clave a eliminar.

        Returns:
            True si se eliminó, False si no existía.

        Complexity: O(1) promedio.
        """
        idx = self._hash(clave)
        bucket = self._tabla[idx]
        for i, (k, _) in enumerate(bucket):
            if k == clave:
                bucket.pop(i)
                self._size -= 1
                return True
        return False

    def _load_factor(self) -> float:
        """Factor de carga actual: elementos / capacidad."""
        return self._size / self._capacidad

    def _rehash(self) -> None:
        """
        Duplica la capacidad y reinserta todos los pares existentes.

        Se dispara cuando el factor de carga supera el umbral.
        Garantiza que el rendimiento promedio se mantenga en O(1).

        Complexity: O(n) — recorre todos los elementos una vez.
        """
        pares_anteriores = [(k, v) for bucket in self._tabla for k, v in bucket]
        self._capacidad *= 2
        self._tabla = [[] for _ in range(self._capacidad)]
        self._size = 0
        for k, v in pares_anteriores:
            self.insert(k, v)

    def stats(self) -> dict:
        """
        Retorna estadísticas internas útiles para el informe académico.

        Returns:
            Dict con capacidad, elementos, factor de carga,
            buckets con colisiones y máximo de elementos por bucket.
        """
        buckets_con_colision = sum(1 for b in self._tabla if len(b) > 1)
        max_bucket = max((len(b) for b in self._tabla), default=0)
        return {
            "capacidad":            self._capacidad,
            "elementos":            self._size,
            "factor_de_carga":      round(self._load_factor(), 3),
            "buckets_con_colision": buckets_con_colision,
            "max_elementos_bucket": max_bucket,
        }

    def __len__(self) -> int:
        return self._size

    def __repr__(self) -> str:
        s = self.stats()
        return (
            f"HashTable(capacidad={s['capacidad']}, elementos={s['elementos']}, "
            f"load_factor={s['factor_de_carga']}, colisiones={s['buckets_con_colision']})"
        )
