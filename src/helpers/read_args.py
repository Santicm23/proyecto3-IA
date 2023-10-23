
import sys

import pandas as pd

from .types import Args


def read_args() -> Args:
    if len(sys.argv) % 2 == 1 or len(sys.argv) < 4:
        print('Usage: python main.py <query> <table1_name> <path_to_csv1>... <tableN_name> <path_to_csvN>')
        sys.exit(1)

    args: Args = {'query': sys.argv[1], 'tables': []}

    table_name = ''
    path_to_csv = ''

    for i, arg in enumerate(sys.argv[2:]):
        if i % 2 == 0:
            table_name = arg
        else:
            path_to_csv = arg
            args['tables'].append(
                {'table_name': table_name, 'table': pd.DataFrame(), 'path_to_csv': path_to_csv})

    return args
