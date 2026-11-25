from pathlib import Path
import pandas as pd
from src.turing_machine import TuringMachine
from src.classify import classificar_df

tm = TuringMachine(Path(__file__).parent.parent / "machines" / "comparador.json")


def test_marca_apenas_valor_acima_do_limiar():
    valores = [10] * 98 + [100, 10_000_000]
    df = pd.DataFrame({"Amount Paid": valores})
    saida, _, _ = classificar_df(df, tm, percentil=0.99)

    assert len(saida) == len(df)
    assert saida["tm_anomalia"].iloc[-1] == 1
    assert saida["tm_anomalia"].iloc[:-1].sum() == 0