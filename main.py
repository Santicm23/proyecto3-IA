
from src.helpers import read_args
from src.inferencia_bayesiana import calcular_probabilidad


def main():
    args = read_args()

    calcular_probabilidad(args['query'], args['tables'])


if __name__ == "__main__":
    main()
