def convert_int(val):
    if val == 'None' or val == '':
        return None
    return int(val)


def convert_float(val):
    if val == 'None' or val == '':
        return None
    return float(val)


def convert_str(val):
    if val == 'None' or val == '':
        return None
    return str(val)


def make_interval_query(interval_id: str | None, charge: int | None, min_mass: float | None, max_mass: float | None,
                        min_rt: float | None, max_rt: float | None, min_ook0: float | None, max_ook0: float | None,
                        min_intensity: float | None, max_intensity: float | None):
    interval_query = ''
    if interval_id:
        interval_query += f'&interval_id={interval_id}'
    if charge:
        interval_query += f'&charge={charge}'
    if min_mass:
        interval_query += f'&min_mass={min_mass}'
    if max_mass:
        interval_query += f'&max_mass={max_mass}'
    if min_rt:
        interval_query += f'&min_rt={min_rt}'
    if max_rt:
        interval_query += f'&max_rt={max_rt}'
    if min_ook0:
        interval_query += f'&min_ook0={min_ook0}'
    if max_ook0:
        interval_query += f'&max_ook0={max_ook0}'
    if min_intensity:
        interval_query += f'&min_intensity={min_intensity}'
    if max_intensity:
        interval_query += f'&max_intensity={max_intensity}'

    if interval_query:
        interval_query = '?' + interval_query[1:]

    return interval_query