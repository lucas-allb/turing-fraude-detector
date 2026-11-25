from src.encoder import faixa, codificar


def test_faixa_valor_zero():
    assert faixa(0) == 0


def test_faixa_valor_negativo():
    assert faixa(-5) == 0


def test_faixa_exemplo():
    assert faixa(1_250_000) == 30


def test_faixa_respeita_teto():
    assert faixa(10**20) == 60


def test_faixa_preserva_ordem():
    valores = [0, 1, 10, 500, 10_000, 1_250_000, 10**9]
    faixas = [faixa(v) for v in valores]
    assert faixas == sorted(faixas)


def test_codificar():
    assert codificar(2, 3) == "11#111"
    assert codificar(0, 0) == "#"