"""
TSP con restricciones utilizando D-Wave Ocean SDK

Restricciones:
- Inicio en ciudad 0
- Segunda ciudad = 2
- Visitar todas las ciudades
- Visitar cada ciudad una única vez
- Regresar al nodo 0
"""

import dimod
from dwave.system import LeapHybridSampler

# ============================================================
# DEFINICIÓN DEL GRAFO
# ============================================================

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

N = 5
cities = list(range(N))

# ============================================================
# CONSTRUCCIÓN DE MATRIZ DE DISTANCIAS
# ============================================================

BIG_PENALTY = 50

distances = {}

for i in cities:
    for j in cities:

        if i == j:
            distances[(i, j)] = 0

        elif (i, j) in roads:
            distances[(i, j)] = roads[(i, j)]

        elif (j, i) in roads:
            distances[(i, j)] = roads[(j, i)]

        else:
            distances[(i, j)] = BIG_PENALTY


# ============================================================
# NOMBRE DE VARIABLES
# ============================================================

def x(city, position):
    """
    Genera el nombre de la variable binaria.

    x(i,t)=1 => ciudad i ocupa la posición t
    """
    return f"x_{city}_{position}"


# ============================================================
# CREACIÓN DEL MODELO QUBO
# ============================================================

bqm = dimod.BinaryQuadraticModel({}, {}, 0.0, dimod.BINARY)

# ============================================================
# COEFICIENTES DE PENALIZACIÓN
# ============================================================

A = 20      # Restricciones estructurales
B = 50      # Carreteras inexistentes

# ============================================================
# FUNCIÓN OBJETIVO
# Minimizar distancia total
# ============================================================

for t in range(N):

    next_t = (t + 1) % N

    for i in cities:
        for j in cities:

            if i != j:

                cost = distances[(i, j)]

                bqm.add_interaction(
                    x(i, t),
                    x(j, next_t),
                    cost
                )

# ============================================================
# RESTRICCIÓN 1
# Cada ciudad debe aparecer una sola vez
# ============================================================

for city in cities:

    vars_city = [x(city, t) for t in range(N)]

    # expansión de:
    # A*(1 - sum(vars))²

    for v in vars_city:
        bqm.add_variable(v, -A)

    for i in range(len(vars_city)):
        for j in range(i + 1, len(vars_city)):
            bqm.add_interaction(
                vars_city[i],
                vars_city[j],
                2 * A
            )

    bqm.offset += A

# ============================================================
# RESTRICCIÓN 2
# Cada posición contiene una única ciudad
# ============================================================

for t in range(N):

    vars_position = [x(city, t) for city in cities]

    for v in vars_position:
        bqm.add_variable(v, -A)

    for i in range(len(vars_position)):
        for j in range(i + 1, len(vars_position)):
            bqm.add_interaction(
                vars_position[i],
                vars_position[j],
                2 * A
            )

    bqm.offset += A

# ============================================================
# RESTRICCIÓN 3
# Inicio obligatorio en nodo 0
# x(0,0) = 1
# ============================================================

bqm.add_variable(x(0, 0), -A)
bqm.offset += A

# ============================================================
# RESTRICCIÓN 4
# Segunda ciudad = nodo 2
# x(2,1) = 1
# ============================================================

bqm.add_variable(x(2, 1), -A)
bqm.offset += A

# ============================================================
# PENALIZACIÓN DE CARRETERAS INEXISTENTES
# ============================================================

valid_edges = set()

for edge in roads:
    a, b = edge

    valid_edges.add((a, b))
    valid_edges.add((b, a))

for t in range(N):

    next_t = (t + 1) % N

    for i in cities:
        for j in cities:

            if i == j:
                continue

            if (i, j) not in valid_edges:

                bqm.add_interaction(
                    x(i, t),
                    x(j, next_t),
                    B
                )

# ============================================================
# RESOLUCIÓN EN D-WAVE
# ============================================================

print("Enviando problema a D-Wave...")

sampler = dimod.SimulatedAnnealingSampler()

sampleset = sampler.sample(bqm)

best = sampleset.first

print("\nEnergia encontrada:")
print(best.energy)

# ============================================================
# DECODIFICAR SOLUCIÓN
# ============================================================

def decode_route(sample):
    """
    Convierte la salida binaria de D-Wave
    en una lista con el orden de visita.
    """

    route = []

    for position in range(N):

        selected_city = None

        for city in cities:

            if sample[x(city, position)] == 1:
                selected_city = city
                break

        route.append(selected_city)

    route.append(0)

    return route


# ============================================================
# CALCULAR COSTE DE LA RUTA
# ============================================================

def route_cost(route):
    """
    Calcula la distancia total recorrida.
    """

    total = 0

    for i in range(len(route) - 1):

        a = route[i]
        b = route[i + 1]

        total += distances[(a, b)]

    return total


# ============================================================
# MOSTRAR RESULTADOS
# ============================================================

route = decode_route(best.sample)

print("\nRuta encontrada:")
print(route)

print("\nVariables activas:")

for var, value in best.sample.items():
    if value == 1:
        print(var)