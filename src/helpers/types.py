# Importamos TypedDict desde el módulo typing. TypedDict es una característica introducida en Python 3.8 que permite
# definir diccionarios con tipos específicos para las claves y los valores.
from typing import TypedDict

import pandas as pd

# Definimos un tipo de datos personalizado llamado Args. Este tipo de datos es un diccionario que contiene dos
# claves: 'query' y 'tables'.
# 'query' debe ser una cadena (string) (str). 'tables' debe ser una lista de objetos de tipo pd.DataFrame. Esto
# significa que tables es una lista que puede contener DataFrames de pandas.
Args = TypedDict('Args', {'query': str, 'tables': list[pd.DataFrame]})
