# para acceder a los argumentos de la línea de comandos
import sys
# para trabajar con DataFrames
import pandas as pd
# estamos importando un tipo de datos personalizado llamado Args desde un archivo llamado types
from .types import Args


# Definimos una función llamada read_args que toma argumentos y devuelve un objeto de tipo Args
def read_args() -> Args:

    # Verificamos si el número de argumentos en la línea de comandos es impar o si hay menos de 4 argumentos.
    # Si es así, se imprime un mensaje de uso y se sale del programa con un código de error 1.
    if len(sys.argv) % 2 == 1 or len(sys.argv) < 4:
        print('Usage: python main.py <query> <table1_name> <path_to_csv1>... <tableN_name> <path_to_csvN>')
        sys.exit(1)

    # Inicializamos una variable args como un diccionario con una clave 'query' que toma el valor del primer argumento
    # de la línea de comandos (sys.argv[1]) y una clave 'tables' que es una lista vacía.
    args: Args = {'query': sys.argv[1], 'tables': []}

    # Inicializamos dos variables, table_name y path_to_csv, como cadenas vacías.
    table_name = ''
    path_to_csv = ''

    # Iniciamos un bucle for que itera a través de los argumentos de la línea de comandos comenzando desde el tercer
    # argumento (índice 2) y obtenemos tanto el índice i como el valor arg.
    # ej: 'Appointment | none  delayed' rain examples/rain.csv maintenance examples/maintenance.csv appointment
    # examples/appointment.csv train examples/train.csv
    # Toma desde "none"
    for i, arg in enumerate(sys.argv[2:]):
        # Si el índice i es par, asumimos que arg es el nombre de una tabla y lo almacenamos en la variable table_name.
        if i % 2 == 0:
            table_name = arg
        # Si el índice i es impar, asumimos que arg es la ruta a un archivo CSV. Luego, leemos ese archivo CSV en un
        # DataFrame de pandas (df) y le asignamos el nombre de la tabla utilizando la variable table_name. Finalmente,
        # agregamos el DataFrame a la lista de tablas en args.
        else:
            path_to_csv = arg
            df = pd.read_csv(path_to_csv)
            df.Name = table_name
            args['tables'].append(df)
    # Devolvemos el objeto args, que contiene la consulta ('query') y una lista de DataFrames de tablas ('tables').
    return args
