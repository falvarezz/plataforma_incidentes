# Plataforma de Análisis de Incidentes y Rutas

Evaluación Integradora Parte 1 — Algoritmos y Estructura de Datos  
Licenciatura en Inteligencia Artificial — 2026

## Estructura del proyecto

```
├── plataforma_incidentes/         # Paquete principal (lógica del sistema)
│   ├── event.py                   # Entidad base del dominio
│   ├── event_store.py             # Repositorio central en memoria
│   ├── index.py                   # Índice hash por atributo clave
│   ├── hash_table.py              # Tabla de dispersión propia
│   ├── router.py                  # Grafo de rutas origen→destino
│   ├── structures.py              # Queue, Stack, PriorityQueue
│   ├── search.py                  # Búsqueda secuencial, binaria, bisect
│   ├── sorting.py                 # Insertion sort, merge sort, sorted()
│   └── __init__.py                # Exporta la interfaz pública del paquete
│
├── main.py                        # Demo de integración de todos los módulos
├── paso2_estructuras.py           # Medición de estructuras lineales
├── paso3_busqueda_ordenamiento.py # Medición de búsqueda y ordenamiento
├── paso4_hashing.py               # Medición de hashing e índices
└── paso5_sintesis.py              # Medición integradora (tiempo + memoria)
```

## Requisitos

- Python 3.10 o superior
- No requiere dependencias externas (solo biblioteca estándar de Python)

## Ejecución

### Demo de integración completa

```bash
python main.py
```

### Scripts de medición por paso

```bash
python paso2_estructuras.py       # Queue, Stack, PriorityQueue
python paso3_busqueda_ordenamiento.py  # Búsqueda y ordenamiento
python paso4_hashing.py           # Hashing e índices
python paso5_sintesis.py          # Medición integradora con tracemalloc
```

Cada script es independiente y reproducible. Las tablas del informe académico fueron generadas con estos scripts.
