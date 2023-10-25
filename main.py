
from src.helpers import read_args
from src.inferencia_bayesiana import inferencia_bayesiana


def main():
    args = read_args()

    print(inferencia_bayesiana(args['query'], args['tables']))


if __name__ == "__main__":
    main()
