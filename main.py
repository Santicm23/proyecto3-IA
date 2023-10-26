
from src.helpers import read_args
from src.inferencia_bayesiana import inferencia_bayesiana, probabilidad_condicional


def main() -> None:
    args = read_args()
    table_names = [table.Name[0].capitalize() for table in args['tables']]

    param1 = args['query'].split('|')[0].strip()

    if param1 in table_names:
        print(inferencia_bayesiana(args['query'], args['tables']))
    else:
        print('El resultado es:', probabilidad_condicional(args['query'], args['tables']))


if __name__ == "__main__":
    main()
