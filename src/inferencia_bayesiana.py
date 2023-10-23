
import pandas as pd

from .agrum import bn_from_dftables


def calcular_probabilidad(query: str, tables: list[pd.DataFrame]) -> float:
    '''Calcula la probabilidad de una query.'''

    vals = query.split('∧')

    bn = bn_from_dftables(tables)

    data_tables = [{
        'name': table.Name[0].upper(),
        'deps': list(filter(lambda name: len(name) == 1 and name.isupper, table.columns)),
    } for table in tables]

    return 0.0


# def inferencia_bayesiana() -> None:
#     ...
