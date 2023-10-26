import pandas as pd


#  toma la ruta de un archivo CSV como argumento y devuelve un DataFrame de pandas
def read_csv(path) -> pd.DataFrame:
    return pd.read_csv(path)
