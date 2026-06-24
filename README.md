# Plataforma de Análisis de Incidentes y Rutas

Evaluación Integradora — Algoritmos y Estructura de Datos  
Licenciatura en Inteligencia Artificial — 2026

## Estructura del proyecto

```
├── plataforma_incidentes/              # Paquete principal (lógica del sistema)
│   ├── event.py                        # Entidad base del dominio
│   ├── event_store.py                  # Repositorio central en memoria
│   ├── index.py                        # Índice hash por atributo clave
│   ├── hash_table.py                   # Tabla de dispersión propia
│   ├── router.py                       # Grafo de rutas con BFS, DFS, Dijkstra, Kruskal
│   ├── structures.py                   # Queue, Stack, PriorityQueue
│   ├── search.py                       # Búsqueda secuencial, binaria, bisect
│   ├── sorting.py                      # Insertion sort, merge sort, sorted()
│   ├── text_analyzer.py                # Búsqueda de patrones: fuerza bruta y KMP
│   ├── avl_tree.py                     # Árbol AVL con rotaciones y range_search
│   ├── rsa_demo.py                     # RSA demostrativo (cifrado asimétrico)
│   ├── dinamica.py                     # Knapsack 0/1 con programación dinámica
│   └── __init__.py                     # Exporta la interfaz pública del paquete
│
├── main.py                             # Demo de integración de todos los módulos
│
├── paso2_estructuras.py                # Parte 1 — Medición de estructuras lineales
├── paso3_busqueda_ordenamiento.py      # Parte 1 — Medición de búsqueda y ordenamiento
├── paso4_hashing.py                    # Parte 1 — Medición de hashing e índices
├── paso5_sintesis.py                   # Parte 1 — Medición integradora (tiempo + memoria)
│
├── paso6_avl.py                        # Parte 2 — Árbol AVL: rotaciones y range_search
├── paso7_grafos.py                     # Parte 2 — BFS, DFS, Dijkstra, Kruskal
└── paso8_algoritmos_avanzados.py       # Parte 2 — KMP, RSA, Knapsack 0/1
```

## Requisitos

- Python 3.10 o superior
- No requiere dependencias externas (solo biblioteca estándar de Python)

## Ejecución

### Demo de integración completa

```bash
python main.py
```

### Parte 1 — Scripts de medición

```bash
python paso2_estructuras.py            # Queue, Stack, PriorityQueue
python paso3_busqueda_ordenamiento.py  # Búsqueda secuencial, binaria, bisect y ordenamiento
python paso4_hashing.py                # Hashing e índices
python paso5_sintesis.py               # Medición integradora con tracemalloc
```

### Parte 2 — Scripts de algoritmos avanzados

```bash
python paso6_avl.py                    # Árbol AVL: inserción, rotaciones, range_search
python paso7_grafos.py                 # BFS, DFS, Dijkstra, Kruskal sobre Router
python paso8_algoritmos_avanzados.py   # KMP vs fuerza bruta, RSA, Knapsack 0/1
```

Cada script es independiente y reproducible. Las tablas de los informes académicos fueron generadas con estos scripts.
