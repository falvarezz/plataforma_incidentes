# Evaluación Integradora — Parte 1
## Plataforma de Análisis de Incidentes y Rutas

**Materia:** Algoritmos y Estructura de Datos  
**Carrera:** Licenciatura en Inteligencia Artificial  
**Año:** 2026  

---

## 1. Diseño del Sistema (POO + Modularidad)

### 1.1 Arquitectura general

La plataforma se implementó como un paquete Python (`plataforma_incidentes/`) compuesto por cinco módulos independientes. Cada módulo encapsula una responsabilidad específica, lo que permite reemplazar o extender cualquier componente sin afectar al resto del sistema.

```
plataforma_incidentes/
├── event.py          # Entidad base del dominio
├── event_store.py    # Repositorio central en memoria
├── index.py          # Índice hash por atributo clave
├── hash_table.py     # Tabla de dispersión propia
├── router.py         # Grafo de rutas origen→destino
├── structures.py     # Queue, Stack, PriorityQueue
├── search.py         # Búsqueda secuencial, binaria, bisect
└── sorting.py        # Insertion sort, merge sort, sorted()
```

### 1.2 Descripción de clases

**`Event`** modela un incidente individual con los atributos: `id`, `timestamp`, `categoria`, `prioridad`, `texto`, `origen` y `destino`. Implementa `__lt__` para permitir comparaciones directas en estructuras de heap sin código adicional.

**`EventStore`** actúa como repositorio central usando una lista interna. La elección de `list` sobre otras estructuras se justifica porque preserva el orden de inserción (útil para auditoría cronológica) y permite acceso por índice en O(1). Para búsquedas frecuentes por clave se delega al módulo `Index`.

**`Index`** implementa un índice configurable por cualquier atributo del evento usando un diccionario Python (`dict`). Permite crear índices múltiples: por `id` para acceso único, o por `categoria`/`origen` para consultas de tipo multi-valor.

**`Router`** modela la red de rutas como un grafo dirigido con lista de adyacencia. Se eligió esta representación sobre la matriz de adyacencia porque el grafo de incidentes es disperso: O(V+E) en memoria frente a O(V²) de la matriz.

**`TextAnalyzer`** analiza el campo descriptivo de los eventos usando fuerza bruta y KMP para detectar patrones de alerta configurables.

### 1.3 Relaciones entre clases

```
EventStore ──contiene──► Event ◄──indexa── Index
                            │
                  origen/destino
                            │
                            ▼
                         Router
                            
Event.texto ──analiza──► TextAnalyzer
```

**Decisión de diseño:** se prefirió composición sobre herencia en todos los casos, ya que cada clase representa un rol funcional distinto sin jerarquía natural entre ellas. Esto favorece la cohesión y reduce el acoplamiento.

---

## 2. Estructuras Lineales (TDA + Operaciones)

Se implementaron tres estructuras en `structures.py`, todas basadas en `collections.deque` y `heapq`.

### 2.1 Queue (Cola FIFO)

Usada para procesar eventos en orden de llegada (pipeline de ingesta). Se implementó con `collections.deque` en lugar de `list` porque `list.pop(0)` desplaza todos los elementos generando O(n), mientras que `deque.popleft()` opera en O(1) al ser una lista doblemente enlazada.

| Operación | Complejidad |
|-----------|-------------|
| `enqueue` | O(1) |
| `dequeue` | O(1) |
| `peek`    | O(1) |

### 2.2 Stack (Pila LIFO)

Usada para historial de operaciones y rollback de estado. Permite deshacer la última acción procesada sobre el sistema.

| Operación | Complejidad |
|-----------|-------------|
| `push` | O(1) |
| `pop`  | O(1) |
| `peek` | O(1) |

### 2.3 PriorityQueue (Cola de Prioridad)

Usada para atender primero los incidentes más críticos (menor valor de prioridad = mayor urgencia). Se implementó con `heapq` sobre una tupla `(prioridad, contador, evento)`. El contador incremental garantiza orden FIFO entre eventos de igual prioridad, evitando comparaciones entre objetos `Event`.

| Operación | Complejidad |
|-----------|-------------|
| `push` | O(log n) |
| `pop`  | O(log n) |
| `peek` | O(1) |

**Resultado de medición** (`timeit`, N=50.000, 500 repeticiones):

| Estructura | Operación | Tiempo |
|------------|-----------|--------|
| `list.pop(0)` | Extracción del frente | 0.56863s |
| `deque.popleft()` | Extracción del frente | 0.31564s |

La diferencia se acentúa con N pequeños: a N=10.000 la deque es el doble de rápida, y el gap crece con el tamaño del dataset.

---

## 3. Búsqueda, Ordenamiento y Medición

### 3.1 Búsqueda secuencial vs binaria vs bisect

Implementadas en `search.py`. La búsqueda binaria requiere la lista ordenada previamente por `id`.

**Medición** (`timeit`, 200 repeticiones, búsqueda en posición central):

| N      | Secuencial | Binaria propia | bisect   |
|--------|-----------|----------------|---------|
| 500    | 0.00116s  | 0.00016s       | 0.00055s |
| 2.000  | 0.00473s  | 0.00018s       | 0.00406s |
| 10.000 | 0.02825s  | 0.00023s       | 0.04732s |
| 30.000 | 0.08528s  | 0.00030s       | 0.46522s |

**Análisis:** la binaria propia es consistentemente más rápida que `bisect` para N grandes. Esto ocurre porque `bisect` extrae la lista de IDs en cada llamada (O(n) extra), mientras que la binaria opera directamente sobre la lista de eventos comparando atributos. A N=30.000 la diferencia es de 1.500x entre binaria y `bisect`, y de ~280x entre binaria y secuencial.

**Complejidad espacial:** ambas operan con O(1) de memoria adicional; no crean estructuras nuevas durante la búsqueda.

### 3.2 Ordenamiento: Insertion Sort vs Merge Sort vs `sorted()`

Implementados en `sorting.py`. Todos reciben una función `key` para ordenar por cualquier atributo de `Event`.

**Medición** (`timeit`, 10 repeticiones):

| N     | Insertion Sort | Merge Sort | `sorted()` | Mem. Insertion | Mem. Merge |
|-------|---------------|------------|-----------|----------------|------------|
| 200   | 0.0067s       | 0.0023s    | 0.0001s   | 1.7 KB         | 4.6 KB     |
| 1.000 | 0.2133s       | 0.0160s    | 0.0008s   | 8.0 KB         | 18.7 KB    |
| 3.000 | 1.7488s       | 0.0553s    | 0.0024s   | 23.6 KB        | 55.7 KB    |
| 5.000 | 4.8967s       | 0.0985s    | 0.0045s   | 39.3 KB        | 90.7 KB    |

**Análisis:**
- **Insertion sort** es conveniente para listas pequeñas (N < 200) o casi ordenadas (mejor caso O(n)), con la ventaja de ser in-place (O(1) memoria extra sobre la copia).
- **Merge sort** escala bien con O(n log n) garantizado, pero requiere O(n) de memoria auxiliar para las sublistas en cada nivel de recursión.
- **`sorted()` (Timsort)** supera a ambos porque combina insertion sort para segmentos pequeños con merge sort, implementado en C. Es el estándar de comparación para cualquier implementación propia.

---

## 4. Hashing e Índices

### 4.1 Índice con diccionario Python (`Index`)

El módulo `index.py` implementa índices sobre cualquier atributo del evento usando `dict`. Se crearon tres índices distintos sobre el mismo `EventStore`:

- `Index(key_attr="id")` → acceso único, O(1) promedio
- `Index(key_attr="categoria")` → multi-valor, permite filtrar por tipo
- `Index(key_attr="origen")` → multi-valor, útil para análisis de red

### 4.2 Tabla de dispersión propia (`HashTable`)

Se implementó en `hash_table.py` para demostrar el mecanismo interno del hashing. Características:

- **Función hash:** `hash(clave) % capacidad`, aprovechando el hash nativo de Python.
- **Resolución de colisiones:** encadenamiento separado (cada bucket es una lista de pares `(clave, valor)`).
- **Rehash automático:** cuando el factor de carga supera 0.75, la tabla duplica su capacidad y redistribuye todos los elementos.

**Estadísticas con 10 eventos y capacidad inicial 8:**

| Métrica | Valor |
|---------|-------|
| Capacidad tras rehash | 16 |
| Factor de carga | 0.625 |
| Buckets con colisión | 2 |
| Máx. elementos por bucket | 3 |

### 4.3 Manejo de colisiones — explicación conceptual

Una **colisión** ocurre cuando dos claves distintas producen el mismo índice de bucket (el dominio de claves es mayor que la capacidad de la tabla). Las dos estrategias clásicas son:

- **Encadenamiento:** cada bucket almacena una lista de elementos que colisionaron. Simple de implementar; degrada a O(k) donde k es el tamaño del bucket. **Estrategia usada en esta implementación.**
- **Direccionamiento abierto:** ante una colisión se busca otra posición libre dentro de la misma tabla (linear probing, quadratic probing). Más eficiente en caché pero requiere factor de carga < 0.7 para evitar degradación severa. **Estrategia usada internamente por Python** en sus objetos `dict`.

### 4.4 Medición comparativa

| N      | Secuencial | HashTable propia | `dict` (Index) |
|--------|-----------|-----------------|---------------|
| 500    | 0.00115s  | 0.00003s        | 0.00002s      |
| 2.000  | 0.00543s  | 0.00003s        | 0.00002s      |
| 10.000 | 0.02466s  | 0.00004s        | 0.00002s      |

Tanto `HashTable` como `dict` mantienen tiempo constante independientemente del N, confirmando el comportamiento O(1) promedio.

---

## 5. Síntesis Integradora

### 5.1 Mejoras de rendimiento logradas

El sistema incorpora tres mejoras estructurales respecto a una implementación naive basada únicamente en listas y búsqueda secuencial:

1. **`Index` sobre `EventStore`:** convierte cada búsqueda por `id` de O(n) a O(1) promedio. A N=10.000, esto representa una reducción de ~1.600x en tiempo de consulta. La inversión de memoria adicional (la estructura del índice) se amortiza rápidamente cuando la cantidad de consultas supera la cantidad de inserciones.

2. **Búsqueda binaria sobre datos ordenados:** reduce el tiempo de búsqueda de O(n) a O(log n). A N=30.000 es ~280x más rápida que la secuencial. El costo de mantener la lista ordenada (O(n log n) de preparación) conviene cuando el dataset es estático o de baja frecuencia de modificación.

3. **`deque` en lugar de `list` para colas:** elimina el cuello de botella de `list.pop(0)` O(n), garantizando O(1) en ambos extremos. Crítico para colas de incidentes de alto volumen.

### 5.2 Trade-off tiempo vs memoria

| Decisión | Ganancia de tiempo | Costo de memoria |
|----------|--------------------|-----------------|
| HashTable / Index | O(n) → O(1) búsqueda | O(n) extra para la tabla |
| Merge sort vs Insertion | O(n²) → O(n log n) | O(1) → O(n) auxiliar |
| Búsqueda binaria | O(n) → O(log n) | O(n log n) costo de ordenar |
| `deque` vs `list` | O(n) → O(1) extracción | Overhead de nodos enlazados |

**Principio general observado:** invertir memoria para indexar o estructurar los datos de antemano siempre reduce el costo temporal de las operaciones repetidas. Esta inversión es especialmente conveniente en sistemas de IA donde la fase de consulta supera ampliamente en frecuencia a la fase de ingesta.

### 5.3 POO, modularidad y mantenibilidad en software de IA

El diseño modular adoptado permite **experimentación aislada**: reemplazar `Index` por un BST o una base de datos es un cambio localizado en `index.py`, invisible para `EventStore` o `TextAnalyzer`. Esto es fundamental en IA, donde se prueba continuamente si una estructura más avanzada justifica su costo.

La combinación de **docstrings con complejidad explícita** y **mediciones reproducibles con `timeit` y `tracemalloc`** transforma las decisiones de diseño en evidencia empírica. Un desarrollador que ingrese al proyecto puede leer la complejidad declarada en cada método, ejecutar los scripts de medición para validarla con datos reales, y tomar decisiones de escalabilidad basadas en hechos y no en suposiciones.

Finalmente, modelar el dominio con POO (`Event` como entidad central) permite que los algoritmos sean agnósticos al contenido: `insertion_sort`, `merge_sort` y `busqueda_binaria` reciben una función `key` y operan sobre cualquier colección de objetos. Esto reduce la duplicación de código y facilita la extensión del sistema a nuevos tipos de incidentes o atributos.

---

## Anexo: Registro de uso de Inteligencia Artificial Generativa

**Herramienta utilizada:** Claude Code (Anthropic) — modelo Claude Sonnet 4.6  
**Fecha de uso:** 07/06/2026  
**Modalidad:** consultas conceptuales y asistencia en codificación dentro del entorno de desarrollo local.

### Registro de diálogos relevantes

| # | Consulta realizada | Uso en el trabajo |
|---|-------------------|-------------------|
| 1 | Estructura de clases esperada para Event, EventStore, Index, Router y TextAnalyzer según las consignas | Orientación inicial del diseño; la arquitectura final y las decisiones fueron propias |
| 2 | Diferencia entre encadenamiento y direccionamiento abierto para colisiones | Apoyo conceptual para la sección 4.3; redacción y ejemplos propios |
| 3 | Por qué `deque.popleft()` es O(1) y `list.pop(0)` es O(n) | Verificación conceptual; la medición y análisis fueron propios |
| 4 | Revisión de sintaxis en la implementación de KMP | Corrección de un error de indexación en `_build_kmp_table` |

### Declaración de autoría

El presente trabajo, incluyendo el diseño de la arquitectura, la implementación del código, el análisis de resultados y la redacción del informe, es de autoría propia. La IAG fue utilizada exclusivamente como herramienta de consulta conceptual y verificación, sin copiar respuestas generadas directamente como producción final. Todos los fragmentos de código fueron comprendidos, adaptados y probados de forma independiente.
