
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

def get_padres(bn: gum.BayesNet, nodo: str):
    '''Devuelve los padres de un nodo'''
    return bn.parents(nodo)

def imprimir_tabla(bn: gum.BayesNet):
    '''Imprime la tabla de probabilidad de un nodo'''
    for nodo in bn.nodes():
        print(f"Nodo: {nodo}")
        if bn.parents(nodo):
            print(f'padres: {bn.parents(nodo)}')
        else:
            print('no tiene padres')

        # Accede a la tabla de probabilidad (CPT) del nodo
        tabla_probabilidad = bn.cpt(nodo)
        # Imprime la tabla de probabilidad
        print(tabla_probabilidad)

def imprimir_nodo(bn: gum.BayesNet, nodo: str):
    '''Imprime la tabla de probabilidad de un nodo'''
    print(f"Nodo: {nodo}")
    # Accede a la tabla de probabilidad (CPT) del nodo
    tabla_probabilidad = bn.cpt(nodo)
    # Imprime la tabla de probabilidad
    print(tabla_probabilidad)

def get_nodo(bn: gum.BayesNet, nodo: str):
    '''Devuelve el nodo'''
    return bn.cpt(nodo)

def test(bn: gum.BayesNet, nodo, diccionario):
    '''Imprime la tabla de probabilidad de un nodo'''
    for nodo in bn.nodes():
        print(f"Nodo: {nodo}")
        if bn.parents(nodo):
            print(f'padres: {bn.parents(nodo)}')
        else:
            print('no tiene padres')

    for key, value in diccionario.items():
        ''''''
    tabla_probabilidad = bn.cpt(nodo)
        # Imprime la tabla de probabilidad
    print(tabla_probabilidad)


def get_freqs_from_tables(diccionario, bn: gum.BayesNet) -> float:
    '''Con base en el valor (light) devuelve la probabilidad de la tabla'''
    total_probability = 1.0
    # Agrega todos los nodos al mapping
    mapping = []
    for key, value in diccionario.items():
        mapping.append(key)

    for key, value in diccionario.items():
        if get_padres(bn, key):
            id_padres = bn.parents(key)
            # Creamos un diccionario temporal para almacenar las combinaciones de claves y valores de los padres
            combinaciones_padres = {}

            for id_padre in id_padres:
                id_padre_entero = int(id_padre)
                padre_key = mapping[id_padre_entero]  # Obtén la clave del padre
                padre_value = diccionario[padre_key]  # Obtén el valor del padre

                # Agregamos la combinación al diccionario temporal
                combinaciones_padres[padre_key] = padre_value
            temp_value = 1.0
            # Imprimimos el valor de cada combinación de claves y valores de los padres
            for combinacion_key, combinacion_value in combinaciones_padres.items():
                print(f"Para nodo {key}, padre {combinacion_key}, valor {combinacion_value}")
                print(bn.cpt(key)[{key: value, **combinaciones_padres}])
                temp_value= bn.cpt(key)[{key: value, **combinaciones_padres}]
            total_probability *= temp_value
            imprimir_nodo(bn, key)
        else:
            total_probability *= bn.cpt(key)[{key: value}]
            print(key, value)
            print(bn.cpt(key)[{key: value}])
            print('-------------------')

    return total_probability



def calcular_probabilidad(query: str, tables: list[pd.DataFrame]) -> float:
    '''Calcula la probabilidad de una query.'''

    name_tables = [table.Name[0].upper() for table in tables]
   # print(name_tables)
    bn = bn_from_dftables(tables)
    vals = list(map(lambda s: s.strip('()P '), query.split('∧')))

    vals_tables = tables_from_vals(vals, name_tables, bn)
    # print(vals)
    diccionario=dict(zip(vals_tables,vals))
    value = get_freqs_from_tables(diccionario, bn)
    print(value)
    return value
