
import pandas as pd

from src.helpers import read_args
from src.inferencia_bayesiana import inferencia_bayesiana, calcular_probabilidad


def main():
    args = read_args()

    for table in args['tables']:
        table['table'] = pd.read_csv(table['path_to_csv'])

    print(calcular_probabilidad(args['query'], args['tables']))


if __name__ == "__main__":
    main()
