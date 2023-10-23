
from src.helpers import read_args
# from src.inferencia_bayesiana import inferencia_bayesiana, calcular_probabilidad
from src.agrum import bn_from_dftables


def main():
    args = read_args()

    tables = args['tables']

    bn = bn_from_dftables(tables)

    print(bn)
    for table in tables:
        print(table.Name)
        print(bn.cpt(table.Name[0].upper()))



if __name__ == "__main__":
    main()
