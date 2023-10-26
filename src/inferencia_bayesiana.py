
from itertools import product

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


def vals_from_table(table: str, bn: gum.BayesNet) -> list[str]:
    '''Construye valores a partir de una tabla de frecuencia.'''

    discVariable: gum.DiscreteVariable = bn.cpt(table).variablesSequence()[0]

    return discVariable.labels()


def calcular_probabilidad(query: str, bn: gum.BayesNet, table_names: list[str]) -> float:
    '''Calcula la probabilidad de una query.'''

    vals = list(map(lambda s: s.strip(), query.split('∧')))
    vals_tables = tables_from_vals(vals, table_names, bn)
    info_vals = list(zip(vals, vals_tables))

    prob = 1.0

    for info_val in info_vals:
        val = info_val[0]
        table_name = info_val[1]
        deps: list[int] = list(bn.parents(table_name))  # type: ignore
        if len(deps) == 0:
            prob *= float(bn.cpt(table_name)[{table_name: val}])
        else:
            deps_names = [bn.cpt(i).names[0] for i in deps]
            filtered = list(
                filter(lambda info: info[1] in deps_names, info_vals))
            index = {info[1]: info[0] for info in filtered}
            index[table_name] = val
            prob *= float(bn.cpt(table_name)[index])

    return prob


def inferencia_bayesiana(query: str, tables: list[pd.DataFrame]) -> dict[str, float]:
    '''Realiza la inferencia bayesiana.'''

    bn = bn_from_dftables(tables)

    table_names = [bn.cpt(i).names[0] for i in range(bn.size())]

    X, E = filter(lambda s: s.strip(), query.split('|'))

    X = X[0].capitalize()
    X_vals = vals_from_table(X, bn)

    E_vals = list(map(lambda s: s.strip(), E.split('∧')))

    E_tables = tables_from_vals(E_vals, table_names, bn)

    Y_tables = list(
        filter(lambda table: table not in E_tables and table != X, table_names))
    Y_vals = list(map(lambda table: vals_from_table(table, bn), Y_tables))

    m_probs = []
    inference: dict[str, float] = {}
    for i, x_val in enumerate(X_vals):
        m_probs.append([])
        inference[x_val] = 0.0
        if len(Y_tables) == 0:
            condition = ' ∧ '.join(E_vals + [x_val])
            prob = calcular_probabilidad(condition, bn, table_names)
            inference[x_val] = prob
            continue

        combinations = product(*Y_vals)

        for combination in combinations:
            condition = ' ∧ '.join(E_vals + [x_val] + list(combination))
            prob = calcular_probabilidad(condition, bn, table_names)

            m_probs[i].append(prob)

        inference[x_val] = sum(m_probs[i])

    alpha = 1 / sum(inference.values())

    for x_val in inference.keys():
        inference[x_val] *= alpha

    return inference
