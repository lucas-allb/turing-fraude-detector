from pathlib import Path
import pandas as pd
from src.turing_machine import TuringMachine
from src.classify import classificar_df

tm = TuringMachine(Path(__file__).parent.parent / "machines" / "comparador.json")


def test_marca_apenas_valor_acima_do_limiar():
    valores = [10] * 99 + [10_000_000]
    df = pd.DataFrame({"id": range(100), "Amount Paid": valores})
    saida, _ = classificar_df(df, tm, limiar_valor=1000)

    assert len(saida) == len(df)
    assert saida["tm_anomalia"].iloc[-1] == 1
    assert saida["tm_anomalia"].iloc[:-1].sum() == 0