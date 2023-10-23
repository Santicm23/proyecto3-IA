
import pyAgrum as gum
import pandas as pd


def ejemplo(tables: list[pd.DataFrame]) -> None:
    bn = gum.BayesNet('WaterSprinkler')
    c = gum.LabelizedVariable('c', 'cloudy?', ['A', 'B'])
    c = bn.add(c)
    s = bn.add(gum.LabelizedVariable('s', 'sprinkler?', 2))
    r = bn.add(gum.LabelizedVariable('r', 'rain?', 2))
    w = bn.add(gum.LabelizedVariable('w', 'wet grass?', 2))

    for link in [(c, s), (c, r), (s, w), (r, w)]:
        bn.addArc(*link)

    bn.cpt(c)[:] = [0.4, 0.6]
    print(bn)
    print(bn.cpt(w))


def bn_from_dftables(tables: list[pd.DataFrame]) -> gum.BayesNet:
    '''Construye una red bayesiana a partir de tablas de frecuencia.'''

    bn = gum.BayesNet('Red Bayesiana')

    for table in tables:
        values = list(filter(lambda name: len(name) > 1 or not name.isupper, table.columns))
        bn.add(gum.LabelizedVariable(table.Name, table.Name[0].upper(), values))
    
    for table in tables:
        for column in table.columns:
            if len(column) == 1 and column.isupper:
                bn.addArc(column, table.Name)

    return bn
