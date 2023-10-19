
import sys

import pandas as pd


def main():
    df = pd.read_csv("ejemplo.csv")

    print(list(df.columns))

if __name__ == "__main__":
    main()
