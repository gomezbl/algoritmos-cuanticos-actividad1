from typing import AbstractSet, Mapping, Sequence


def is_valid_sample(
    sample: Mapping[str, int],
    cities: Sequence[int],
    valid_edges: AbstractSet[tuple[int, int]],
) -> bool:
    """Check that a sample represents a valid route through the city graph."""

    route = []

    for position in range(len(cities)):
        selected_cities = [
            city for city in cities
            if sample[f"x_{city}_{position}"] == 1
        ]

        if len(selected_cities) != 1:
            return False

        route.append(selected_cities[0])

    return (
        bool(route)
        and route[0] == 0
        and len(set(route)) == len(cities)
        and all(
            (start, end) in valid_edges
            for start, end in zip(route, route[1:] + [route[0]])
        )
    )
