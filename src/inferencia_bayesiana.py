
from itertools import product

import pandas as pd
import pyAgrum as gum

from .agrum import bn_from_dftables


# Esta línea define la función tables_from_vals que toma tres argumentos:
# vals: Una lista de valores (por ejemplo, ['A', 'B', 'C']).
# table_names: Una lista de nombres de tablas (por ejemplo, ['Table1', 'Table2']).
# bn: Una red bayesiana representada como un objeto gum.BayesNet.
def tables_from_vals(vals: list[str], table_names: list[str], bn: gum.BayesNet) -> list[str]:
    '''Construye tablas de frecuencia a partir de valores.'''

    # Se inicializa una lista vacía llamada tables para almacenar los nombres de las tablas correspondientes
    # a los valores.
    tables: list[str] = []

    # A continuación, se inicia un bucle anidado que itera a través de cada valor en la lista vals y luego a través
    # de cada nombre de tabla en la lista table_names. Se intenta acceder a la tabla de probabilidad condicional (
    # CPT) de la red bayesiana (bn) para la tabla con nombre table_name y se consulta el valor correspondiente a la
    # combinación {table_name: val}. Si esta consulta es exitosa, significa que la tabla contiene información para el
    # valor val y, por lo tanto, se agrega el nombre de la tabla a la lista tables. Si la consulta falla (por
    # ejemplo, si no hay información para el valor en esa tabla), se captura la excepción y se continúa con la
    # siguiente tabla.
    for val in vals:
        for table_name in table_names:
            try:
                bn.cpt(table_name)[{table_name: val}]
                tables.append(table_name)
            except:
                continue

    # Retorna las tablas que tienen información relevante sobre los atributos que hay en "values"
    return tables

# vals: Una lista de valores (por ejemplo, ['A', 'B', 'C']).
# table_names: Una lista de nombres de tablas (por ejemplo, ['Table1', 'Table2']).
# bn: Una red bayesiana representada como un objeto gum.BayesNet.
def vals_from_table(table: str, bn: gum.BayesNet) -> list[str]:
    '''Construye valores a partir de una tabla de frecuencia.'''

    # En esta línea, se accede a la tabla de probabilidad condicional (CPT) correspondiente a la tabla con nombre
    # table en la red bayesiana bn utilizando bn.cpt(table). Luego, se obtiene la secuencia de variables de la CPT
    # mediante variablesSequence() y se selecciona la primera variable (índice 0) de esa secuencia. Esta variable es
    # una variable discreta representada por gum.DiscreteVariable.
    discVariable: gum.DiscreteVariable = bn.cpt(table).variablesSequence()[0]

    # Finalmente, se devuelve una lista de etiquetas (labels) de la variable discreta discVariable. Estas etiquetas
    # son los valores posibles asociados a la variable representada por la tabla.
    # Supongamos que tenemos una red bayesiana con una variable llamada 'Tiempo' representada en una tabla de
    # frecuencia llamada 'Table1'. La variable 'Tiempo' puede tomar valores discretos 'Soleado', 'Nublado' y 'Lluvioso'.
    # Si llamamos a la función vals_from_table('Table1', bn), esta función nos devolvería la lista ['Soleado', 'Nublado', 'Lluvioso'],
    # que son los valores posibles asociados a la variable 'Tiempo' en la tabla 'Table1'.
    return discVariable.labels()

# Esta línea define la función calcular_probabilidad que toma tres argumentos:
# query: Una cadena de texto que representa la consulta (por ejemplo, "A∧B").
# bn: Una red bayesiana representada como un objeto gum.BayesNet.
# table_names: Una lista de nombres de tablas de la red bayesiana.
def calcular_probabilidad(query: str, bn: gum.BayesNet, table_names: list[str]) -> float:
    '''Calcula la probabilidad de una query.'''

    # Se divide la consulta query en sus componentes individuales, que se asumen separados por el operador "∧" (
    # conjunción). Estos componentes se almacenan en una lista llamada vals después de eliminar cualquier espacio en
    # blanco.
    vals = list(map(lambda s: s.strip(), query.split('∧')))
    # Se utiliza la función tables_from_vals para determinar a qué tablas de frecuencia corresponden los valores en
    # la consulta. El resultado se almacena en vals_tables, que es una lista de nombres de tablas.
    vals_tables = tables_from_vals(vals, table_names, bn)
    # Se utiliza la función tables_from_vals para determinar a qué tablas de frecuencia corresponden los valores en la
    # consulta. El resultado se almacena en vals_tables, que es una lista de nombres de tablas.
    info_vals = list(zip(vals, vals_tables))
    # Se crea una lista info_vals que combina los valores de la consulta con los nombres de las tablas correspondientes.
    # Cada elemento de info_vals es una tupla que contiene un valor de la consulta y el nombre de la tabla en la que se encuentra.

    prob = 1.0
    # Esta variable se utiliza para realizar el cálculo acumulativo de probabilidades.

    # Se inicia un bucle que recorre las tuplas de info_vals.
    for val, table_name in info_vals:
        # Se extraen el valor de la consulta (val) y el nombre de la tabla (table_name) de cada tupla.
        # Se obtienen las dependencias de la tabla table_name en forma de una lista de nombres de las tablas padre.
        # Esta información se almacena en deps.
        deps: list[int] = list(bn.parents(table_name))  # type: ignore
        # Se verifica si la tabla no tiene dependencias. Si es así, significa que la probabilidad se puede calcular
        # directamente desde la tabla de probabilidad condicional de esta tabla.
        if len(deps) == 0:
            # Se multiplica la probabilidad acumulativa (prob) por la probabilidad condicional correspondiente a
            # la tabla table_name y el valor val.
            prob *= float(bn.cpt(table_name)[{table_name: val}])
        # En caso de que la tabla tenga dependencias, se procede a calcular la probabilidad condicional teniendo
        # en cuenta las dependencias.
        else:
            # Se obtienen los nombres de las tablas de las dependencias y se almacenan en deps_names.
            deps_names = [bn.cpt(i).names[0] for i in deps]
            # Se filtran las tuplas de info_vals para obtener solo las que corresponden a las dependencias.
            # Esto se hace comparando los nombres de las tablas en deps_names con los nombres de las tablas en
            # las tuplas de info_vals. Las tuplas filtradas se almacenan en filtered.
            filtered = list(
                filter(lambda info: info[1] in deps_names, info_vals))
            # Se crea un índice index que asocia los nombres de las tablas con sus valores correspondientes en función
            # de las dependencias. Luego, se agrega el nombre de la tabla actual (table_name) con su valor
            # correspondiente (val) al índice.
            index = {info[1]: info[0] for info in filtered}
            # Se multiplica la probabilidad acumulativa (prob) por la probabilidad condicional calculada utilizando
            # el índice.
            index[table_name] = val
            prob *= float(bn.cpt(table_name)[index])
    # Finalmente, la función devuelve la probabilidad acumulativa calculada.
    return prob


# query: Una cadena de texto que representa la consulta (por ejemplo, "A|B∧C").
# tables: Una lista de DataFrames de pandas que contienen las tablas de frecuencia de la red bayesiana.
def inferencia_bayesiana(query: str, tables: list[pd.DataFrame]) -> dict[str, float]:
    '''Realiza la inferencia bayesiana.'''

    # Se construye la red bayesiana (bn) a partir de las tablas de frecuencia utilizando la función bn_from_dftables.
    bn = bn_from_dftables(tables)

    # Se crea una lista table_names que contiene los nombres de todas las tablas de probabilidad condicional en la red
    # bayesiana. Se utiliza un bucle for para recorrer todas las tablas y extraer sus nombres.
    table_names = [bn.cpt(i).names[0] for i in range(bn.size())]

    # Se divide la consulta query en dos partes: la variable de interés (X) y las variables de evidencia (E), utilizando
    # el operador | como separador. Se eliminan los espacios en blanco alrededor de las partes usando la función strip.
    X, E = filter(lambda s: s.strip(), query.split('|')) if '|' in query else (query, None)

    # Se capitaliza la primera letra de la variable de interés (X) para asegurarse de que coincida con la convención de
    # nombres utilizada en la red bayesiana.
    X = X[0].capitalize()
    # Se utiliza la función vals_from_table para obtener los valores posibles de la variable de interés (X) en función
    # de la red bayesiana (bn). Estos valores se almacenan en la lista X_vals.
    # python
    X_vals = vals_from_table(X, bn)

    # Se divide la parte de evidencia (E) en sus componentes individuales utilizando el operador ∧ como separador y se
    # eliminan los espacios en blanco alrededor de cada componente. Los valores de evidencia se almacenan en la lista E_vals.
    E_vals = list(map(lambda s: s.strip(), E.split('∧'))) if E else []

    # Se utiliza la función tables_from_vals para determinar a qué tablas de frecuencia corresponden los valores de
    # evidencia (E_vals). El resultado se almacena en la lista E_tables.
    E_tables = tables_from_vals(E_vals, table_names, bn) if E else []

    # Se crea una lista Y_tables que contiene los nombres de las tablas que no son ni de evidencia (E) ni de la variable
    # de interés (X). Esto se hace utilizando la función filter y una función lambda que filtra las tablas que no están
    # en E_tables y no son igual a X.
    Y_tables = list(
        filter(lambda table: table not in E_tables and table != X, table_names))

    # Se utiliza la función vals_from_table para obtener los valores posibles de todas las variables en Y_tables.
    # Estos valores se almacenan en la lista Y_vals.
    Y_vals = list(map(lambda table: vals_from_table(table, bn), Y_tables))

    # Se inicializan dos listas vacías: m_probs para almacenar las probabilidades condicionales y inference como un
    # diccionario para almacenar las probabilidades resultantes.
    m_probs = []
    inference: dict[str, float] = {}

    # Se inicia un bucle que recorre los valores posibles de la variable de interés (X).
    for i, x_val in enumerate(X_vals):
        # Se inicializan listas vacías para almacenar las probabilidades condicionales correspondientes a x_val y
        # se inicializa la probabilidad acumulativa en 0.0 en el diccionario inference para x_val.
        m_probs.append([])
        inference[x_val] = 0.0

        # Se verifica si no hay variables de evidencia en la consulta. Si es así, se calcula la probabilidad
        # directamente utilizando la función calcular_probabilidad.
        if len(Y_tables) == 0:
            # Se construye la condición de consulta concatenando los valores de evidencia y x_val con el operador "∧"
            # utilizando join.
            condition = ' ∧ '.join(E_vals + [x_val])
            # Se calcula la probabilidad condicional usando la función calcular_probabilidad y se almacena en prob.
            prob = calcular_probabilidad(condition, bn, table_names)
            # La probabilidad calculada se almacena en el diccionario inference para x_val.
            inference[x_val] = prob
            # Se continúa con la siguiente iteración del bucle.
            continue

        # Si hay variables de evidencia, se generan todas las combinaciones posibles de valores para las variables en
        # Y_vals utilizando la función product.
        combinations = product(*Y_vals)

        # Se inicia un bucle que recorre las combinaciones de valores de las variables de evidencia.
        for combination in combinations:
            # Se construye la condición de consulta concatenando los valores de evidencia, x_val y la combinación actual
            # de valores con el operador "∧".
            condition = ' ∧ '.join(E_vals + [x_val] + list(combination))
            # Se calcula la probabilidad condicional utilizando la función calcular_probabilidad y se almacena en prob.
            prob = calcular_probabilidad(condition, bn, table_names)

            # La probabilidad se agrega a la lista correspondiente en m_probs.
            m_probs[i].append(prob)

        # Se calcula la probabilidad acumulativa para x_val sumando todas las probabilidades en m_probs.
        inference[x_val] = sum(m_probs[i])

    # Se calcula el factor de normalización alpha, que es el inverso de la suma de todas las probabilidades en inference.
    alpha = 1 / sum(inference.values())

    # Se normalizan las probabilidades en inference multiplicándolas por el factor de normalización alpha.
    for x_val in inference.keys():
        inference[x_val] *= alpha

    # Finalmente, la función devuelve el diccionario inference que contiene las probabilidades condicionales
    # normalizadas para diferentes valores de la variable de interés (X).
    return inference


def probabilidad_condicional(query: str, tables: list[pd.DataFrame]) -> float:

    bn = bn_from_dftables(tables)

    # Se crea una lista table_names que contiene los nombres de todas las tablas de probabilidad condicional en la red
    # bayesiana. Se utiliza un bucle for para recorrer todas las tablas y extraer sus nombres.
    table_names = [bn.cpt(i).names[0] for i in range(bn.size())]

    # Se divide la consulta query en dos partes: la variable de interés (X) y las variables de evidencia (E), utilizando
    # el operador | como separador. Se eliminan los espacios en blanco alrededor de las partes usando la función strip.
    X, E = filter(lambda s: s.strip(), query.split('|')) if '|' in query else (query, None)

    # Se divide la parte de evidencia (E) en sus componentes individuales utilizando el operador ∧ como separador y se
    # eliminan los espacios en blanco alrededor de cada componente. Los valores de evidencia se almacenan en la lista E_vals.
    E_vals = list(map(lambda s: s.strip(), E.split('∧'))) if E else []

    # Se utiliza la función tables_from_vals para determinar a qué tablas de frecuencia corresponden los valores de
    # evidencia (E_vals). El resultado se almacena en la lista E_tables.
    E_tables = tables_from_vals(E_vals, table_names, bn) if E else []

    # Se crea una lista Y_tables que contiene los nombres de las tablas que no son ni de evidencia (E) ni de la variable
    # de interés (X). Esto se hace utilizando la función filter y una función lambda que filtra las tablas que no están
    # en E_tables y no son igual a X.
    Y_tables = list(
        filter(lambda table: table not in E_tables and table != X, table_names))

    # Se utiliza la función vals_from_table para obtener los valores posibles de todas las variables en Y_tables.
    # Estos valores se almacenan en la lista Y_vals.
    Y_vals = list(map(lambda table: vals_from_table(table, bn), Y_tables))

    # Se inicializan dos listas vacías: m_probs para almacenar las probabilidades condicionales y inference como un
    # diccionario para almacenar las probabilidades resultantes.
    m_probs = []

    # Se verifica si no hay variables de evidencia en la consulta. Si es así, se calcula la probabilidad
    # directamente utilizando la función calcular_probabilidad.
    if len(Y_tables) == 0:
        # Se construye la condición de consulta concatenando los valores de evidencia y X con el operador "∧"
        # utilizando join.
        condition = ' ∧ '.join(E_vals + [X])
        # Se calcula la probabilidad condicional usando la función calcular_probabilidad y se almacena en prob.
        prob = calcular_probabilidad(condition, bn, table_names)
        # La probabilidad calculada se almacena en el diccionario inference para X.
        m_probs.append(prob)
        # Se continúa con la siguiente iteración del bucle.
    else:

        # Si hay variables de evidencia, se generan todas las combinaciones posibles de valores para las variables en
        # Y_vals utilizando la función product.
        combinations = product(*Y_vals)

        # Se inicia un bucle que recorre las combinaciones de valores de las variables de evidencia.
        for combination in combinations:
            # Se construye la condición de consulta concatenando los valores de evidencia, X y la combinación actual
            # de valores con el operador "∧".
            condition = ' ∧ '.join(E_vals + [X] + list(combination))
            # Se calcula la probabilidad condicional utilizando la función calcular_probabilidad y se almacena en prob.
            prob = calcular_probabilidad(condition, bn, table_names)

            # La probabilidad se agrega a la lista correspondiente en m_probs.
            m_probs.append(prob)

    # Se calcula la probabilidad acumulativa para X sumando todas las probabilidades en m_probs.

    return sum(m_probs)


