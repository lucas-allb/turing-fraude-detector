from pathlib import Path
import pytest
from src.turing_machine import TuringMachine

JSON = Path(__file__).parent.parent / "machines" / "comparador.json"
tm = TuringMachine(JSON)


def entrada(a, b):
    return "1" * a + "#" + "1" * b


@pytest.mark.parametrize("a, b, esperado", [
    (0, 0, "normal"),
    (3, 3, "normal"),
    (2, 5, "normal"),
    (0, 4, "normal"),
    (5, 2, "anomala"),
    (1, 0, "anomala"),
])
def test_esperado(a, b, esperado):
    rotulo, _ = tm.run(entrada(a, b))
    assert rotulo == esperado


def test_entrada_invalida_rejeitada():
    assert tm.run("111")[0] == "REJEITA"


def test_timeout():
    assert tm.run(entrada(30, 5), max_passos=10)[0] == "TIMEOUT"