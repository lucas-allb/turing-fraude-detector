import pandas as pd

CSV_TM = "resultados/turing.csv"


def resumo(csv_tm=CSV_TM):
    df = pd.read_csv(csv_tm, usecols=["faixa", "tm_rotulo", "tm_passos"])

    assert df.groupby("faixa")["tm_passos"].nunique().max() == 1

    print("Passos por transação:")
    print(df["tm_passos"].describe().round(1))

    print("\nPor rótulo:")
    print(df.groupby("tm_rotulo")["tm_passos"].agg(["count", "mean", "max"]).round(1))

    print("\nPor faixa:")
    por_faixa = df.groupby("faixa")["tm_passos"].agg(["count", "first"])
    print(por_faixa.rename(columns={"first": "passos"}))


if __name__ == "__main__":
    resumo()