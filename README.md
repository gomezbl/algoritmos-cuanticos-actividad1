# Modelización y Resolución del Problema del Viajante con D-Wave

## Descripción

Este proyecto desarrolla una solución para una instancia del Problema del Viajante (*Travelling Salesman Problem*, TSP) utilizando técnicas de optimización cuántica basadas en modelos QUBO (*Quadratic Unconstrained Binary Optimization*) y el ecosistema D-Wave Ocean SDK.

El objetivo consiste en encontrar una ruta de distancia mínima que visite todas las ciudades exactamente una vez y regrese al punto de partida, respetando un conjunto de restricciones adicionales definidas en el enunciado de la actividad.

La implementación forma parte de la asignatura **Algoritmos Cuánticos** del Máster en Computación Cuántica.

---

## Grafo del problema

La instancia del problema se define mediante el siguiente conjunto de carreteras:

```python
roads = {
    (0, 1): 3,
    (1, 2): 3,
    (1, 3): 4,
    (2, 3): 1,
    (0, 3): 4,
    (0, 4): 2,
    (2, 4): 6,
    (0, 2): 5
}
```

Cada nodo representa una ciudad y cada arista representa una carretera con una distancia asociada.

---

## Restricciones

La solución debe cumplir las siguientes condiciones:

- La ruta debe comenzar en la ciudad `0`.
- La ruta debe finalizar en la ciudad `0`.
- La segunda ciudad visitada debe ser la ciudad `2`.
- Todas las ciudades deben ser visitadas.
- Cada ciudad sólo puede visitarse una vez.
- Únicamente pueden utilizarse las carreteras definidas en el grafo.

---

## Tecnologías utilizadas

- Python 3
- D-Wave Ocean SDK
- dimod
- Leap Hybrid Solver
- Binary Quadratic Models (BQM)
- QUBO (Quadratic Unconstrained Binary Optimization)

---

## Formulación del problema

El TSP se modela mediante variables binarias:

```text
x(i,t)
```

donde:

- `i` representa una ciudad.
- `t` representa una posición dentro de la ruta.

Ejemplo:

```text
x(2,1) = 1
```

indica que la ciudad 2 ocupa la posición 1 del recorrido.

A partir de estas variables se construye un modelo QUBO que incorpora:

1. Función objetivo de minimización de distancia.
2. Restricción de visita única.
3. Restricción de posición única.
4. Nodo inicial obligatorio.
5. Segunda ciudad obligatoria.
6. Restricciones de conectividad.

---

## Implementación

La implementación realiza automáticamente los siguientes pasos:

1. Construcción de la matriz de distancias.
2. Generación de las variables binarias del modelo.
3. Construcción del Binary Quadratic Model (BQM).
4. Adición de restricciones mediante penalizaciones.
5. Envío del problema al solver híbrido de D-Wave.
6. Obtención de la solución.
7. Decodificación de la salida binaria.
8. Reconstrucción de la ruta obtenida.
9. Cálculo de la distancia total recorrida.

---

## Estructura del proyecto

```text
.
├── tsp_dwave.py
├── README.md
├── docs
│   ├── memoria.pdf
```

---

## Ejecución

### Instalar dependencias

```bash
pip install dwave-ocean-sdk
pip install dimod
pip install python-dotenv
```

### Configurar credenciales D-Wave


### Ejecutar el programa

```bash
python tsp_dwave.py
```

---

## Salida esperada

El programa muestra:

- Energía obtenida.
- Ruta encontrada.
- Distancia total recorrida.
- Variables binarias activadas.

Ejemplo:

```text
Ruta encontrada:
[0, 2, 3, 1, 4, 0]

Coste total:
15
```

---

## Aprendizajes obtenidos

Este proyecto permite comprender de forma práctica:

- La transformación de problemas clásicos a modelos QUBO.
- El uso de técnicas de Quantum Annealing.
- La construcción de modelos de optimización mediante D-Wave Ocean SDK.
- La resolución híbrida de problemas NP-Hard.
- Las ventajas y limitaciones actuales de la computación cuántica aplicada a optimización combinatoria.

---

## Referencias

- Lucas, A. (2014). *Ising formulations of many NP problems*.
- Glover, F., Kochenberger, G., & Du, Y. (2019). *A tutorial on formulating and using QUBO models*.
- Nielsen, M. A., & Chuang, I. L. (2010). *Quantum Computation and Quantum Information*.
- D-Wave Systems Documentation.

---

## Autor

**Rafael Gómez Blanes**

Máster en Computación Cuántica  
Universidad Internacional de La Rioja (UNIR)
``