
import pandas as pd

from src.helpers.types import Table, InfoCol


def obtener_tabla(col: str, tables: list[Table]) -> Table | None:
    '''Devuelve la tabla correspondiente la columna dada.'''

    for table in tables:
        if col in table['table'].columns:
            return table


def obtener_tablas_dependientes(table: Table, tables: list[Table]) -> list[Table]:
    '''Devuelve las tablas de las que depende la tabla dada.'''

    l: list[Table] = []

    for t in tables:
        if t['table_name'][0].capitalize() in table['table'].columns:
            l.append(t)

    return l


def obtener_info_cols(query: str, tables: list[Table]) -> list[InfoCol]:
    '''Devuelve la información de las columnas de la query.'''

    l: list[InfoCol] = []

    for col in query.split('∧'):
        name = col.strip()
        table = obtener_tabla(name, tables)

        if not table:
            raise Exception(f'La columna {name} no existe en ninguna tabla.')

        table_dependientes = obtener_tablas_dependientes(table, tables)

        l.append({'name': col.strip(), 'table': table,
                 'table_dependencies': table_dependientes})

    return l


def calcular_probabilidad(query: str, tables: list[Table]):
    '''Calcula la probabilidad de una query.'''

    info_cols = obtener_info_cols(query, tables)

    if len(info_cols) == 0:
        return 0.0

    info_col = info_cols[0]
    prob_tmp = 0.0

    if len(info_col['table_dependencies']) == 0:
        prob_tmp = info_col['table']['table'][info_col['name']].mean()
    else:
        table_filtered = info_col['table']['table'][info_col['name']]
        for ic in info_cols:
            if ic['table']['table_name'][0].capitalize() in info_col['table']['table'].columns:
                table_filtered = info_col['table']['table'][table_filtered == ic['name']]
        
        print(table_filtered)
        prob_tmp = table_filtered.mean()
    
    return prob_tmp * calcular_probabilidad(query[query.find('∧') + 1:], tables)


def inferencia_bayesiana() -> None:
    ...
