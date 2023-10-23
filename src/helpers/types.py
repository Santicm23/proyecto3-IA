
from typing import TypedDict

import pandas as pd


Table = TypedDict('Table', {'table_name': str, 'table': pd.DataFrame, 'path_to_csv': str})
Args = TypedDict('Args', {'query': str, 'tables': list[Table]})
InfoCol = TypedDict('InfoCol', {'name': str, 'table': Table, 'table_dependencies': list[Table]})
