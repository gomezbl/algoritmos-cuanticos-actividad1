"""
TSP con restricciones utilizando D-Wave Ocean SDK

Restricciones:
- Inicio en ciudad 0
- Visitar todas las ciudades
- Visitar cada ciudad una única vez
- Regresar al nodo 0
"""

import dimod
from restrictions import restriccion_1, restriccion_2, restriccion_3
from tsp_validation import is_valid_sample

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

B = 50      # Carreteras inexistentes
A = 2 * (N - 1) * (BIG_PENALTY + B) + 1  # Restricciones estructurales

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

# Cada ciudad debe aparecer una sola vez.
restriccion_1(bqm, cities, N, A, x)

# Cada posición debe contener una única ciudad.
restriccion_2(bqm, cities, N, A, x)

# Inicio obligatorio en el nodo 0.
restriccion_3(bqm, 0, A, x)

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

print("Enviando problema al simulador computador cuántico de annealing...")

sampler = dimod.SimulatedAnnealingSampler()

# ================================================================================================
# IMPORTANTE: El proceso de annealing simulado (Simulated Annealing) es un algoritmo estocástico.
# Una semilla fija permite que esta simulación local sea reproducible,
# mientras que múltiples ejecuciones (reads) proporcionan al muestreador
# varias soluciones candidatas.
# ================================================================================================

SIMULATION_SEED = 12345
NUM_READS = 100

sample_kwargs = {"num_reads": NUM_READS}

if "seed" in sampler.parameters:
    sample_kwargs["seed"] = SIMULATION_SEED

sampleset = sampler.sample(bqm, **sample_kwargs)

feasible_samples = [
    sample_record
    for sample_record in sampleset.data(fields=["sample", "energy"])
    if is_valid_sample(sample_record.sample, cities, valid_edges)
]

if not feasible_samples:
    raise RuntimeError(
        "El muestreador no produjo ninguna ruta que cumpla las restricciones."
    )

best = min(feasible_samples, key=lambda sample_record: sample_record.energy)

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

print("\nDistancias por tramo:")
uses_missing_road = False
for start, end in zip(route, route[1:]):
    if (start, end) in valid_edges:
        print(f"{start} -> {end}: {distances[(start, end)]}")
    else:
        uses_missing_road = True
        print(
            f"{start} -> {end}: carretera inexistente "
            f"(penalización: {distances[(start, end)]})"
        )

if uses_missing_road:
    print(
        "\nCoste total con penalizaciones "
        f"(no es una ruta válida): {route_cost(route)}"
    )
else:
    print(f"\nDistancia total: {route_cost(route)}")

print("\nVariables activas:")

for var, value in best.sample.items():
    if value == 1:
        print(var)