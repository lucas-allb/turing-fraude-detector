from pathlib import Path
import pytest
from src.turing_machine import TuringMachine
from src.encoder import codificar

tm = TuringMachine(Path(__file__).parent.parent / "machines" / "comparador.json")


def passos_esperados(a, b):
    if a <= b:
        return 2 * (a + 1) ** 2
    return 2 * (b + 1) ** 2 + (2 * b + 1) * (a - b)


@pytest.mark.parametrize("a", range(0, 13))
@pytest.mark.parametrize("b", range(0, 6))
def test_passos_seguem_formula(a, b):
    _, passos = tm.run(codificar(a, b))
    assert passos == passos_esperados(a, b)