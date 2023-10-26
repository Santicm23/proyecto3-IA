import pandas as pd
import pyAgrum as gum


# toma una lista de DataFrames de pandas llamada tables como
# argumento y devuelve un objeto gum.BayesNet, que es una red bayesiana.
def bn_from_dftables(tables: list[pd.DataFrame]) -> gum.BayesNet:
    '''Construye una red bayesiana a partir de tablas de frecuencia.'''

    # Creamos una nueva red bayesiana llamada bn con el nombre 'Red Bayesiana'.
    bn = gum.BayesNet('Red Bayesiana')

    # Recorremos las tablas en la lista tables. Para cada tabla, filtramos las columnas cuyos nombres tienen más
    # de una letra o que no están en mayúsculas y las almacenamos en values
    for table in tables:
        values = list(filter(lambda name: len(name) >
                                          1 or not name.isupper, table.columns))
        # agregamos una variable etiquetada (LabelizedVariable) a la red bayesiana con el nombre de la tabla
        # (la primera letra en mayúscula), los nombres de las columnas y los valores posibles.
        bn.add(gum.LabelizedVariable(
            table.Name[0].upper(), table.Name, values))

    # Nuevamente, recorremos las tablas. Esta vez, para cada tabla, recorremos las columnas. Si una columna tiene
    # un nombre de una sola letra en mayúsculas, agregamos un arco desde esa columna a la variable de la tabla en la red bayesiana.
    for table in tables:
        for column in table.columns:
            if len(column) == 1 and column.isupper:
                bn.addArc(column, table.Name[0].upper())

    # En este bloque, recorremos nuevamente las tablas. Para cada tabla, iteramos a través de las filas. Aquí, se
    # construye la tabla de probabilidades condicionales (CPT) para cada variable en la red bayesiana.
    for table in tables:
        for i in range(table.shape[0]):
            # Se identifican las dependencias de la variable actual, que son columnas con nombres de una
            # sola letra en mayúsculas.
            dependencies = list(filter(lambda name: len(name) == 1
                                                    and name.isupper, table.columns))
            # Se separan los valores de las columnas en dep_values (valores de dependencia) y values
            # (valores de probabilidad).
            dep_values = list(filter(lambda val: isinstance(
                val, str), list(table.iloc[i].values)))
            values = list(filter(lambda val: not isinstance(
                val, str), list(table.iloc[i].values)))

            # CONSTRUIR TABLA DE PROBABILIDADES CONDICIONALES pata cada variable de la red bayesiana -------------------
            # La CPT describe cómo cambia la probabilidad de la variable en función de sus dependencias

            # Se verifica si existen valores de dependencia (dep_values). Si no hay dependencias, se asignan
            # directamente los valores a la CPT de la variable en la red bayesiana.
            # Si dep_values es una lista vacía, significa que no hay dependencias para esta variable
            # bn.cpt("T")[:] = [0.4, 0.3, 0.3] Por ejemplo, probabilidad de Soleado, Nublado, Lluvioso
            if len(dep_values) == 0:
                bn.cpt(table.Name[0].upper())[:] = values
            # Si hay dependencias, se construye un índice basado en las dependencias y sus valores correspondientes,
            # y luego se asignan los valores a la CPT de la variable en la red bayesiana utilizando ese índice.
            else:
                # índice que asocie los valores de la tabla que son dependientes (dep_values) con las variables de
                # dependencia (dependencies)
                # dependencies = ['W'] (solo depende de "Viento").
                # dep_values = ['Débil', 'Fuerte'] (los valores posibles de "Viento").
                # values es una lista de probabilidades condicionales para "Tempo" dado "Viento".
                # index = {'W': 'Débil', 'W': 'Fuerte'}
                index = {dependencies[i]: dep_values[i]
                         for i in range(len(dependencies))}
                # bn.cpt("T")[index] = [0.7, 0.3, 0.4, 0.6, 0.2, 0.8]
                bn.cpt(table.Name[0].upper())[index] = values

    return bn
