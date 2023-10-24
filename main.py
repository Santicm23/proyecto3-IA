
from src.helpers import read_args
from src.inferencia_bayesiana import calcular_probabilidad
# from src.agrum import bn_from_dftables


def main():
    args = read_args()

    print(calcular_probabilidad(args['query'], args['tables']))


if __name__ == "__main__":
    main()
