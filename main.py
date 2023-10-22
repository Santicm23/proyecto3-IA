
import pandas as pd

from src.helpers import read_args


def main():
    args = read_args()

    tables: list[pd.DataFrame] = []

    for table in args['tables']:
        tables.append(pd.read_csv(table['path_to_csv']))

    print(args)


if __name__ == "__main__":
    main()
