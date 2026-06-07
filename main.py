"""
main.py — Punto de entrada de la Plataforma de Análisis de Incidentes.
Demuestra la integración de los cinco módulos del sistema.
"""
from datetime import datetime
from plataforma_incidentes import Event, EventStore, Index, Router, TextAnalyzer


def main():
    # --- 1. Crear eventos de ejemplo ---
    eventos = [
        Event("EVT-001", datetime(2026, 6, 1, 8, 0), "red",       1, "falla crítica en router principal", "nodo-A", "nodo-B"),
        Event("EVT-002", datetime(2026, 6, 1, 8, 5), "seguridad", 2, "intrusión detectada en firewall",   "nodo-B", "nodo-C"),
        Event("EVT-003", datetime(2026, 6, 1, 8, 10),"hardware",  3, "temperatura elevada en servidor",   "nodo-A", "nodo-D"),
        Event("EVT-004", datetime(2026, 6, 1, 8, 15),"red",       1, "pérdida de paquetes en enlace",     "nodo-C", "nodo-A"),
    ]

    # --- 2. EventStore: almacenar eventos ---
    store = EventStore()
    for e in eventos:
        store.add_event(e)
    print(store)

    # --- 3. Index: indexar por id y por categoria ---
    idx_id  = Index(key_attr="id")
    idx_cat = Index(key_attr="categoria")
    for e in store.get_all():
        idx_id.insert(e)
        idx_cat.insert(e)

    print(f"\nBúsqueda por id 'EVT-002': {idx_id.search_one('EVT-002')}")
    print(f"Búsqueda por categoria 'red': {idx_cat.search('red')}")

    # --- 4. Router: construir grafo de rutas ---
    router = Router()
    for e in store.get_all():
        router.add_edge(e.origen, e.destino)
    print(f"\n{router}")
    print(f"Vecinos de nodo-A: {router.get_neighbors('nodo-A')}")

    # --- 5. TextAnalyzer: detectar alertas en textos ---
    analyzer = TextAnalyzer(alertas=["crítica", "intrusión", "pérdida"])
    for e in store.get_all():
        alertas = analyzer.detectar_alertas(e.texto)
        if alertas:
            print(f"\nALERTA en {e.id}: {alertas} -> '{e.texto}'")


if __name__ == "__main__":
    main()
