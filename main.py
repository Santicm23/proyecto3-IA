
from src.helpers import read_args
# from src.inferencia_bayesiana import inferencia_bayesiana, calcular_probabilidad
from src.agrum import ejemplo


def main():
    args = read_args()

    tables = args['tables']

    ejemplo(tables)



if __name__ == "__main__":
    main()
