import pandas as pd
from sklearn.metrics import classification_report, cohen_kappa_score, confusion_matrix

CSV_TM = "resultados/turing.csv"
CSV_IF = "resultados/isolation_forest.csv"


def carregar(csv_tm=CSV_TM, csv_if=CSV_IF):
    tm = pd.read_csv(csv_tm)
    iso = pd.read_csv(csv_if)
    df = tm.merge(iso, on="id", how="inner", suffixes=("", "_if"))


    if not (df["Is Laundering"] == df["Is Laundering_if"]).all():
        raise ValueError("Os ids não correspondem às mesmas transações nos dois arquivos.")
    print(f"Transações comparadas: {len(df)} (MT: {len(tm)}, IF: {len(iso)})")
    return df


def avaliar(df):
    y = df["Is Laundering"]


    for nome, col in [("Máquina de Turing", "tm_anomalia"), ("Isolation Forest", "anomalia_if")]:
        print(f"\n=== {nome} vs. rótulo real ===")
        print(confusion_matrix(y, df[col]))
        print(classification_report(y, df[col], digits=3, zero_division=0))


    concordancia = (df["tm_anomalia"] == df["anomalia_if"]).mean()
    kappa = cohen_kappa_score(df["tm_anomalia"], df["anomalia_if"])
    print(f"\nConcordância MT x IF: {concordancia:.4f} | Kappa: {kappa:.4f}")

    print("\nMT (linhas) x IF (colunas):")
    print(pd.crosstab(df["tm_anomalia"], df["anomalia_if"]))


if __name__ == "__main__":
    avaliar(carregar())