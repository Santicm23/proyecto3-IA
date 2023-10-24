
import pandas as pd
import pyAgrum as gum

from .agrum import bn_from_dftables


def tables_from_vals(vals: list[str], table_names: list[str], bn: gum.BayesNet) -> list[gum.Potential]:
    '''Construye tablas de frecuencia a partir de valores.'''

    tables = []

    for val in vals:
        for table_name in table_names:
            try:
                bn.cpt(table_name)[{table_name: val}]
                tables.append(table_name)
            except:
                continue

    return tables


def calcular_probabilidad(query: str, tables: list[pd.DataFrame]) -> float:
    '''Calcula la probabilidad de una query.'''

    name_tables = [table.Name[0].upper() for table in tables]

    bn = bn_from_dftables(tables)

    vals = list(map(lambda s: s.strip(), query.split('∧')))
    vals_tables = tables_from_vals(vals, name_tables, bn)
    print(vals)
    print(vals_tables)

    return 0.0


# def inferencia_bayesiana() -> None:
#     ...
