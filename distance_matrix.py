from collections.abc import Mapping, Sequence


def construir_matriz_distancias(
    roads: Mapping[tuple[int, int], int],
    cities: Sequence[int],
    missing_road_penalty: int,
) -> dict[tuple[int, int], int]:
    """Build a symmetric distance matrix, assigning a penalty to missing roads."""

    distances = {}

    for city_a in cities:
        for city_b in cities:
            if city_a == city_b:
                distances[(city_a, city_b)] = 0
            elif (city_a, city_b) in roads:
                distances[(city_a, city_b)] = roads[(city_a, city_b)]
            elif (city_b, city_a) in roads:
                distances[(city_a, city_b)] = roads[(city_b, city_a)]
            else:
                distances[(city_a, city_b)] = missing_road_penalty

    return distances
