import pandas as pd
from src.turing_machine import TuringMachine
from src.encoder import faixa, codificar

CSV_ENTRADA = "data/teste.csv"
CSV_SAIDA = "resultados/turing.csv"
MAQUINA = "machines/comparador.json"
COLUNA_VALOR = "Amount Paid"

LIMIAR_VALOR = 16389049.48


def classificar_df(df, tm, limiar_valor=LIMIAR_VALOR, coluna=COLUNA_VALOR):
    limiar_faixa = faixa(limiar_valor)

    cache = {}

    def rodar(f):
        if f not in cache:
            cache[f] = tm.run(codificar(f, limiar_faixa))
        return cache[f]

    faixas = df[coluna].apply(faixa)
    resultados = faixas.map(rodar)

    saida = pd.DataFrame({
        "id": df["id"].values,
        "faixa": faixas.values,
        "tm_rotulo": resultados.str[0].values,
        "tm_passos": resultados.str[1].values,
    })
    saida["tm_anomalia"] = (saida["tm_rotulo"] == "anomala").astype(int)
    return saida, limiar_faixa


def classificar(csv_entrada=CSV_ENTRADA, csv_saida=CSV_SAIDA, maquina=MAQUINA):
    tm = TuringMachine(maquina)
    df = pd.read_csv(csv_entrada, usecols=["id", COLUNA_VALOR, "Is Laundering"])
    saida, limiar_faixa = classificar_df(df, tm)
    saida["Is Laundering"] = df["Is Laundering"].values
    saida.to_csv(csv_saida, index=False)

    print(f"Transações (conjunto de teste): {len(saida)}")
    print(f"Limiar (p99 do treino): valor {LIMIAR_VALOR:.2f} -> faixa {limiar_faixa}")
    print(f"Marcadas como anômalas: {saida['tm_anomalia'].sum()} "
          f"({saida['tm_anomalia'].mean():.2%})")
    return saida


if __name__ == "__main__":
    classificar()