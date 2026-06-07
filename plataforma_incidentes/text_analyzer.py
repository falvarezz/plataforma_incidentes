"""
Módulo: text_analyzer.py
Análisis de texto en incidentes para detección de patrones y alertas.
"""
from typing import List, Optional


class TextAnalyzer:
    """
    Analizador de texto para el campo descriptivo de los eventos.

    Implementa dos estrategias de búsqueda de patrones:
      - Fuerza bruta: simple, O(n*m), adecuado para patrones cortos.
      - KMP (Knuth-Morris-Pratt): O(n+m), eficiente para patrones repetidos.

    Decisión de diseño: se ofrecen ambas implementaciones para poder
    compararlas empíricamente con timeit (requerimiento del parcial).

    Attributes:
        _alertas (List[str]): Palabras clave que disparan una alerta al detectarse.
    """

    def __init__(self, alertas: Optional[List[str]] = None):
        """
        Inicializa el analizador con una lista opcional de palabras de alerta.

        Args:
            alertas: Lista de patrones que, al encontrarse en el texto de un
                     evento, indican que debe dispararse una alerta.
                     Ejemplo: ['crítico', 'falla', 'intrusion'].
        """
        self._alertas: List[str] = alertas or []

    def search_fuerza_bruta(self, texto: str, patron: str) -> List[int]:
        """
        Busca todas las ocurrencias de patron en texto usando fuerza bruta.

        Compara el patrón carácter a carácter desplazándose por el texto.

        Args:
            texto: Cadena donde se busca.
            patron: Cadena a localizar.

        Returns:
            Lista de índices donde comienza cada ocurrencia. Lista vacía si no hay.

        Complexity: O(n * m), donde n = len(texto), m = len(patron).
        """
        n, m = len(texto), len(patron)
        posiciones = []
        for i in range(n - m + 1):
            if texto[i:i + m] == patron:
                posiciones.append(i)
        return posiciones

    def _build_kmp_table(self, patron: str) -> List[int]:
        """
        Construye la tabla de fallos (failure function) para KMP.

        La tabla indica cuántos caracteres del patrón pueden reutilizarse
        tras una falla de comparación, evitando retroceder en el texto.

        Args:
            patron: Patrón para el que se construye la tabla.

        Returns:
            Lista de enteros con la longitud del prefijo-sufijo más largo.

        Complexity: O(m).
        """
        m = len(patron)
        tabla = [0] * m
        j = 0
        for i in range(1, m):
            while j > 0 and patron[i] != patron[j]:
                j = tabla[j - 1]
            if patron[i] == patron[j]:
                j += 1
            tabla[i] = j
        return tabla

    def search_kmp(self, texto: str, patron: str) -> List[int]:
        """
        Busca todas las ocurrencias de patron en texto usando el algoritmo KMP.

        Aprovecha la tabla de fallos para nunca retroceder en el texto,
        lo que lo hace más eficiente que fuerza bruta en casos con muchas
        coincidencias parciales.

        Args:
            texto: Cadena donde se busca.
            patron: Cadena a localizar.

        Returns:
            Lista de índices donde comienza cada ocurrencia.

        Complexity: O(n + m).
        """
        if not patron:
            return []
        tabla = self._build_kmp_table(patron)
        posiciones = []
        j = 0
        for i, c in enumerate(texto):
            while j > 0 and c != patron[j]:
                j = tabla[j - 1]
            if c == patron[j]:
                j += 1
            if j == len(patron):
                posiciones.append(i - j + 1)
                j = tabla[j - 1]
        return posiciones

    def detectar_alertas(self, texto: str) -> List[str]:
        """
        Retorna las palabras de alerta presentes en el texto del evento.

        Usa KMP para cada palabra de alerta configurada.

        Args:
            texto: Texto descriptivo del evento (Event.texto).

        Returns:
            Lista de palabras de alerta encontradas en el texto.
        """
        texto_lower = texto.lower()
        return [a for a in self._alertas if self.search_kmp(texto_lower, a.lower())]

    def __repr__(self) -> str:
        return f"TextAnalyzer(alertas_configuradas={len(self._alertas)})"
