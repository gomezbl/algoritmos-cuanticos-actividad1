from collections.abc import Callable, Sequence


def restriccion_1(
    bqm,
    cities: Sequence[int],
    positions: int,
    penalty: int,
    variable_name: Callable[[int, int], str],
) -> None:
    """Añade al BQM la restricción de que cada ciudad aparezca una sola vez."""

    for city in cities:
        city_variables = [
            variable_name(city, position) for position in range(positions)
        ]

        for variable in city_variables:
            bqm.add_variable(variable, -penalty)

        for i in range(len(city_variables)):
            for j in range(i + 1, len(city_variables)):
                bqm.add_interaction(
                    city_variables[i],
                    city_variables[j],
                    2 * penalty,
                )

        bqm.offset += penalty


def restriccion_2(
    bqm,
    cities: Sequence[int],
    positions: int,
    penalty: int,
    variable_name: Callable[[int, int], str],
) -> None:
    """Añade al BQM la restricción de que cada posición contenga una ciudad."""

    for position in range(positions):
        position_variables = [
            variable_name(city, position) for city in cities
        ]

        for variable in position_variables:
            bqm.add_variable(variable, -penalty)

        for i in range(len(position_variables)):
            for j in range(i + 1, len(position_variables)):
                bqm.add_interaction(
                    position_variables[i],
                    position_variables[j],
                    2 * penalty,
                )

        bqm.offset += penalty


def restriccion_3(
    bqm,
    start_city: int,
    penalty: int,
    variable_name: Callable[[int, int], str],
) -> None:
    """Añade al BQM la restricción de que la ruta comience en una ciudad."""

    bqm.add_variable(variable_name(start_city, 0), -penalty)
    bqm.offset += penalty
