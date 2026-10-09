# Universidad José Antonio Páez (UJAP) - Métodos Cuantitativos
## Parcial V: Programación Dinámica

Proyecto desarrollado en **Python** aplicando **Programación Orientada a Objetos (POO)** y **Arquitectura Limpia (Clean Architecture)** con interfaz gráfica nativa en **PyQt6**.

---

### 📂 Estructura del Proyecto (Arquitectura Limpia)

```
Parcial5/
├── src/
│   ├── domain/                         # Capa de Dominio (Entidades y Modelos de Negocio)
│   │   ├── entities.py                 # Graph, Node, Edge, Item, KnapsackProblem
│   │   ├── models.py                   # StageTable, ShortestPathResult, KnapsackResult, AlgorithmComparison
│   │   └── exceptions.py               # Excepciones de dominio (ciclos negativos, no alcanzable, etc.)
│   ├── application/                    # Capa de Aplicación (Casos de Uso e Interfaces)
│   │   ├── interfaces.py               # IShortestPathSolver, IKnapsackSolver, ITextExporter, IPreloadedDataRepository
│   │   ├── dtos.py                     # Data Transfer Objects
│   │   └── use_cases/
│   │       ├── solve_shortest_path.py  # Forward DP, Backward DP, Bellman-Ford, Floyd-Warshall
│   │       ├── solve_knapsack.py       # Algoritmo VolumenCarga (0-1 y No Acotada)
│   │       ├── compare_algorithms.py   # Comparativa formal de algoritmos y equivalencias
│   │       └── export_reports.py       # Generación de informe del problema
│   ├── infrastructure/                 # Capa de Infraestructura (Algoritmos y Repositorios)
│   │   ├── repositories/
│   │   │   └── preloaded_data.py       # Precarga exacta de los datos del examen Parcial V
│   │   ├── solvers/
│   │   │   ├── forward_dp_solver.py    # DP Adelante hacia Atrás con tablas de etapas
│   │   │   ├── backward_dp_solver.py   # DP De Atrás hacia Adelante con tablas de etapas
│   │   │   ├── bellman_ford_solver.py  # Bellman-Ford con relajaciones sucesivas
│   │   │   ├── floyd_warshall_solver.py# Floyd-Warshall O(V³) para todos los pares
│   │   │   └── knapsack_dp_solver.py   # VolumenCarga con matriz V[i][w] y backtracking
│   │   └── exporters/
│   │       └── report_text_exporter.py # Exportador oficial a .txt
│   └── presentation/                   # Capa de Presentación (100% Python)
│       ├── controllers.py              # Controladores mediadores (Clean Architecture)
│       ├── cli/
│       │   └── cli_runner.py           # Ejecutor en consola
│       └── gui/                        # Interfaz Gráfica Nativa de Escritorio (PyQt6)
│           ├── main_window.py          # Ventana principal con pestañas
│           ├── components/
│           │   ├── graph_canvas.py     # Lienzo interactivo (QPainter, arrastre de nodos, resaltado de ruta)
│           │   ├── stage_table_view.py # Visor de tablas de decisión por etapas
│           │   └── dp_matrix_view.py   # Visor de la matriz 2D V[i][w]
│           ├── tabs/
│           │   ├── graph_tab.py        # Pestaña Problema 1 (Ruta más corta, lienzo y edición de aristas)
│           │   ├── knapsack_tab.py     # Pestaña Problema 2 (Volumen de Carga, edición de productos)
│           │   └── report_tab.py       # Pestaña Reporte del Problema (.txt)
│           └── styles/
│               └── theme.py            # Tema oscuro moderno (QSS)
├── tests/                              # Suite de pruebas unitarias automatizadas
│   ├── test_domain.py
│   ├── test_graph_solvers.py
│   └── test_knapsack_solver.py
├── main.py                             # Punto de entrada principal
├── reporte_problema.txt                # Archivo de texto generado con la resolución completa
├── requirements.txt
└── README.md
```

---

### 🚀 Cómo Ejecutar

#### 1. Iniciar la Interfaz Gráfica (PyQt6)
```bash
python3 main.py
```
*(Se abrirá la ventana con el lienzo interactivo, tablas dinámicas y controles).*

#### 2. Ejecutar Modo Consola (CLI)
```bash
python3 main.py --cli
```
*(Resuelve todos los problemas, imprime resultados en terminal y genera `reporte_problema.txt`).*

#### 3. Ejecutar Pruebas Unitarias
```bash
python3 -m unittest discover tests
```

---

### ✨ Características Principales

1. **Problemas Precargados del Parcial V**:
   - **Problema 1 (Grafo)**: Nodos 1 al 13 con topología, aristas y pesos idénticos a la lámina de examen (Origen: *1 - Oficina anterior*, Destino: *13 - Oficina nueva*).
   - **Problema 2 (Volumen de Carga)**: Capacidad de 10 kg, con Tablet Samsung (2 kg, $40), Dron DJI Mini (3 kg, $50), Proyector portátil (4 kg, $65) y Laptop ASUS ZenBook (5 kg, $60).
   - Botón de **1 clic** en cada pestaña para restablecer inmediatamente los datos originales del examen.

2. **Resolución con Datos Variables**:
   - En el grafo: permite agregar, modificar pesos o eliminar aristas dinámicamente, y reubicar nodos arrastrándolos con el mouse en el lienzo.
   - En Volumen de Carga: permite modificar la capacidad máxima de carga, añadir nuevos productos con pesos y precios arbitrarios, eliminar productos existentes y alternar entre modo 0/1 y modo con repetición.

3. **Múltiples Algoritmos de Resolución**:
   - **Programación Dinámica Adelante hacia Atrás (Forward DP)** con tablas de decisión formales por etapas.
   - **Programación Dinámica de Atrás hacia Adelante (Backward DP)** con ecuaciones de Bellman y tablas de etapas.
   - **Algoritmo Bellman-Ford** con registro de iteraciones y verificación de ausencia de ciclos negativos.
   - **Algoritmo Floyd-Warshall** con evaluación recursiva de vértices intermedios y reconstrucción de camino.
   - Comparación teórica automática de costos y complejidades computacionales.

4. **Entregable Oficial del Problema**:
   - Pestaña dedicada con visor y botón de exportación que genera el archivo `reporte_problema.txt` con todos los pasos de resolución.
# Parcial5_Programacion_Dinamica
