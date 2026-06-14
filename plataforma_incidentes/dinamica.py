"""
Módulo: dinamica.py
Programación dinámica — Knapsack 0/1 aplicado a selección de incidentes.

Problema: dado un presupuesto máximo de capacidad de procesamiento (en unidades
de tiempo), seleccionar el subconjunto de incidentes pendientes que maximice
la suma de prioridades atendidas, sin superar la capacidad disponible.

Modelado como Knapsack 0/1:
  - Cada incidente es un ítem con peso = costo_procesamiento y valor = prioridad.
  - La mochila tiene capacidad W = presupuesto_total.
  - Cada incidente puede incluirse (1) o no (0); no puede fraccionarse.

Estrategia: programación dinámica bottom-up.
  - Se construye una tabla dp[i][w] = máxima prioridad atendible usando los
    primeros i incidentes con capacidad w.
  - Relación de recurrencia:
      dp[i][w] = dp[i-1][w]                          si peso[i] > w
      dp[i][w] = max(dp[i-1][w],
                     dp[i-1][w - peso[i]] + valor[i]) si peso[i] <= w
  - La solución es dp[n][W].

La ventaja frente a fuerza bruta (2^n subconjuntos) es la reutilización de
subproblemas solapados: O(n * W) en tiempo y espacio, polinomial en W.

Nota conceptual: si los costos fueran fraccionables (Knapsack fraccional)
el algoritmo greedy (mayor ratio valor/peso) bastaría y sería O(n log n).
El 0/1 no admite greedy óptimo porque el llenado parcial no funciona.
"""
from typing import List, Tuple


def knapsack(
    capacidad: int,
    costos: List[int],
    valores: List[int],
) -> Tuple[int, List[int]]:
    """
    Resuelve el problema de la mochila 0/1 con programación dinámica.

    Args:
        capacidad: Capacidad máxima de la mochila (W).
        costos: Lista de pesos/costos de cada ítem (enteros positivos).
        valores: Lista de valores/prioridades de cada ítem.

    Returns:
        (valor_optimo, indices_seleccionados)
        valor_optimo: Suma máxima de valores alcanzable.
        indices_seleccionados: Índices de los ítems incluidos en la solución.

    Complexity: O(n * W) tiempo, O(n * W) espacio.
    """
    n = len(costos)
    # Tabla dp: (n+1) filas × (capacidad+1) columnas, inicializada en 0
    dp = [[0] * (capacidad + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        peso_i  = costos[i - 1]
        valor_i = valores[i - 1]
        for w in range(capacidad + 1):
            # Opción 1: no incluir el ítem i
            dp[i][w] = dp[i - 1][w]
            # Opción 2: incluir el ítem i (solo si cabe)
            if peso_i <= w:
                con_i = dp[i - 1][w - peso_i] + valor_i
                if con_i > dp[i][w]:
                    dp[i][w] = con_i

    # Reconstrucción: retroceder por la tabla para identificar ítems elegidos
    seleccionados: List[int] = []
    w = capacidad
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i - 1][w]:
            seleccionados.append(i - 1)   # índice base-0
            w -= costos[i - 1]

    seleccionados.reverse()
    return dp[n][capacidad], seleccionados


def knapsack_optimizado(
    capacidad: int,
    costos: List[int],
    valores: List[int],
) -> int:
    """
    Versión optimizada en memoria: solo mantiene una fila de la tabla DP.

    No permite reconstruir los ítems seleccionados, pero reduce el espacio
    de O(n * W) a O(W). Útil cuando solo se necesita el valor óptimo.

    Args:
        capacidad: Capacidad máxima.
        costos: Lista de costos por ítem.
        valores: Lista de valores por ítem.

    Returns:
        Valor óptimo máximo alcanzable.

    Complexity: O(n * W) tiempo, O(W) espacio.
    """
    dp = [0] * (capacidad + 1)
    for i, (costo, valor) in enumerate(zip(costos, valores)):
        # Se recorre de mayor a menor para evitar usar el mismo ítem dos veces
        for w in range(capacidad, costo - 1, -1):
            dp[w] = max(dp[w], dp[w - costo] + valor)
    return dp[capacidad]
