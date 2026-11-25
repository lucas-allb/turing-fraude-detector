import math


def faixa(valor, escala=5, teto=60):
    valor = max(valor, 0)
    return min(int(math.log10(valor + 1) * escala), teto)


def codificar(a, b):
    # Monta a fita no formato 1^a # 1^b (ex.: a=2, b=3 -> "11#111")
    return "1" * a + "#" + "1" * b