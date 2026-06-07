# 💡 Tips Clave para el Éxito en el Desarrollo

---

## 🧩 Parte 1 — Diseño Modular y Medición

### 1. No programes todo de golpe

Comenzá por las **clases base** antes de agregar complejidad:

1. Diseñá `Event` y `EventStore` como punto de partida.
2. Una vez que la estructura modular en Python funcione, incorporá las estructuras lineales.
3. Finalmente, sumá las búsquedas y ordenamientos.

> **Regla de oro:** estructura primero, funcionalidad después.

---

### 2. El código se mide, no solo se escribe

La eficiencia importa. Usá **`timeit`** para comparar algoritmos y tomar decisiones basadas en datos reales.

```python
import timeit

# Ejemplo: comparar búsqueda lineal vs. binaria
tiempo_lineal = timeit.timeit(lambda: busqueda_lineal(lista, objetivo), number=1000)
tiempo_binaria = timeit.timeit(lambda: busqueda_binaria(lista, objetivo), number=1000)

print(f"Lineal:  {tiempo_lineal:.4f}s")
print(f"Binaria: {tiempo_binaria:.4f}s")
```

Siempre preguntate:
- ¿Ganamos **tiempo** de ejecución?
- ¿Ahorramos **memoria**?
- ¿Cuál es el **trade-off** entre ambos?

---

## 🎯 Parte 2 — Elección Justificada y Presentación

### 3. Justificá cada decisión de diseño

Al elegir entre estructuras y algoritmos, no alcanza con que "funcione". Tu elección debe estar **justificada con un criterio claro**:

| Criterio | Ejemplo de justificación |
|---|---|
| Tiempo de acceso | "Usé un diccionario porque el acceso es O(1) vs. O(n) de una lista." |
| Memoria | "Preferí un generador para no cargar todos los eventos en RAM." |
| Frecuencia de operación | "Como se busca más de lo que se inserta, prioricé la búsqueda." |

---

### 4. El video es tu presentación profesional

Imaginá que le presentás el proyecto a un **cliente o líder técnico**. El video debe:

- ✅ Explicar el **porqué** de tus elecciones (no solo el cómo).
- ✅ Mostrar los **conceptos utilizados** (no solo el código corriendo).
- ✅ Ser visual y natural — usá diagramas, esquemas o capturas si ayudan.
- ✅ Durar **máximo 8 minutos**.

> **Tip:** Armá un guion antes de grabar. La estructura sugerida: contexto del problema → decisiones de diseño → demo → conclusiones.

---

### 5. Podés usar IA Generativa — registrala con transparencia

Herramientas como Claude, ChatGPT u otras pueden ayudarte a:
- Consultar dudas conceptuales.
- Optimizar fragmentos de código.
- Armar el guion del video.

**Requisito obligatorio:** registrá todo uso de IAG en el **Anexo obligatorio** del informe.

---

## 📋 Checklist de Entrega

### Parte 1
- [ ] Informe académico
- [ ] Código modular en Python (`Event`, `EventStore`, estructuras lineales, búsquedas)
- [ ] Datos de prueba incluidos

### Parte 2
- [ ] Informe con justificación de decisiones
- [ ] Código completo y funcional
- [ ] Enlace al video explicativo (máx. 8 min)

### Siempre
- [ ] **Anexo obligatorio:** registro de uso de IAG
- [ ] **Datos de prueba** que demuestren todas las funcionalidades y mediciones

---

## 🧪 Sobre los Datos de Prueba

Incluí datos de prueba que permitan verificar:

- Las distintas **funcionalidades** implementadas (inserción, búsqueda, ordenamiento, etc.).
- Las **mediciones de rendimiento** (comparaciones con `timeit`).
- **Casos borde**: listas vacías, un solo elemento, elementos duplicados, búsqueda de algo inexistente.

```python
# Ejemplo de dataset de prueba
eventos_prueba = [
    Event(id=1, nombre="Conferencia Python", fecha="2025-03-15"),
    Event(id=2, nombre="Workshop IA",        fecha="2025-01-20"),
    Event(id=3, nombre="Hackathon",          fecha="2025-06-01"),
    # ... más eventos para probar volumen
]
```

---

*¡Éxito en el desarrollo! Recordá: un buen programador no solo hace que el código funcione, sino que puede **explicar por qué lo hizo así**.*
