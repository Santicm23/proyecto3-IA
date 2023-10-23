
import numpy as np
import pyAgrum as gum
import pandas as pd


def ejemplo(tables: list[pd.DataFrame]) -> None:
    bn = bn_from_dftables(tables)

    print(bn)
    for table in tables:
        print(table.Name)
        print(bn.cpt(table.Name[0].upper()))


def bn_from_dftables(tables: list[pd.DataFrame]) -> gum.BayesNet:
    '''Construye una red bayesiana a partir de tablas de frecuencia.'''

    bn = gum.BayesNet('Red Bayesiana')

    for table in tables:
        values = list(filter(lambda name: len(name) >
                      1 or not name.isupper, table.columns))
        bn.add(gum.LabelizedVariable(
            table.Name[0].upper(), table.Name, values))

    for table in tables:
        for column in table.columns:
            if len(column) == 1 and column.isupper:
                bn.addArc(column, table.Name[0].upper())

    for table in tables:
        for i in range(table.shape[0]):
            dependencies = list(filter(lambda name: len(name) == 1
                                       and name.isupper, table.columns))
            dep_values = list(filter(lambda val: isinstance(
                val, str), list(table.iloc[i].values)))
            values = list(filter(lambda val: not isinstance(
                val, str), list(table.iloc[i].values)))

            if len(dep_values) == 0:
                bn.cpt(table.Name[0].upper())[:] = values
            else:
                index = {dependencies[i]: dep_values[i]
                         for i in range(len(dependencies))}
                bn.cpt(table.Name[0].upper())[index] = values

    return bn
