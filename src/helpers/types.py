
from typing import TypedDict

import pandas as pd


Args = TypedDict('Args', {'query': str, 'tables': list[pd.DataFrame]})
