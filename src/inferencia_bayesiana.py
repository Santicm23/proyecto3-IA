
import pandas as pd
import pyAgrum as gum

from .agrum import bn_from_dftables


def tables_from_vals(vals: list[str], table_names: list[str], bn: gum.BayesNet) -> list[str]:
    '''Construye tablas de frecuencia a partir de valores.'''

    tables: list[str] = []

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
    info_vals = list(zip(vals, vals_tables))

    prob = 1.0
    
    for info_val in info_vals:
        val = info_val[0]
        table_name = info_val[1]
        deps: list[int] = list(bn.parents(table_name)) # type: ignore
        if len(deps) == 0:
            prob *= float(bn.cpt(table_name)[{table_name: val}])
        else:
            deps_names = [bn.cpt(i).names[0] for i in deps]
            filtered = list(filter(lambda info: info[1] in deps_names, info_vals))
            index = {info[1]: info[0] for info in filtered}
            index[table_name] = val
            prob *= float(bn.cpt(table_name)[index])

    return prob


# def inferencia_bayesiana() -> None:
#     ...
