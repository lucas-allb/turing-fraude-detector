import pandas as pd
from sklearn.metrics import average_precision_score, roc_auc_score

from src.evaluate import carregar


def sobreposicao_lavagens(df):
    pos = df[df["Is Laundering"] == 1]
    print(f"\nLavagens reais no teste: {len(pos)}")
    print("\nMT (linhas) x IF (colunas), só nas lavagens reais:")
    print(pd.crosstab(pos["tm_anomalia"], pos["anomalia_if"]))

    y = df["Is Laundering"]
    combinacoes = [
        ("MT ou IF (união)", df["tm_anomalia"] | df["anomalia_if"]),
        ("MT e IF (interseção)", df["tm_anomalia"] & df["anomalia_if"]),
    ]
    print()
    for nome, marca in combinacoes:
        marcadas = int(marca.sum())
        acertos = int(((marca == 1) & (y == 1)).sum())
        print(f"{nome}: {marcadas} marcadas, {acertos} lavagens detectadas, "
              f"precisão {acertos / marcadas:.4f}, revocação {acertos / len(pos):.4f}")


def ordenacao(df):
    y = df["Is Laundering"]

    s_if = df["score_if"]
    if s_if[df["anomalia_if"] == 1].mean() < s_if[df["anomalia_if"] == 0].mean():
        s_if = -s_if

    s_tm = df["faixa"]

    print(f"\nPrevalência de lavagem (precisão média esperada ao acaso): {y.mean():.4f}")
    for nome, s in [("Máquina de Turing (faixa do valor)", s_tm),
                    ("Isolation Forest (score)", s_if)]:
        print(f"{nome}: AUC-ROC = {roc_auc_score(y, s):.3f} | "
              f"precisão média = {average_precision_score(y, s):.4f}")


if __name__ == "__main__":
    dados = carregar()
    sobreposicao_lavagens(dados)
    ordenacao(dados)