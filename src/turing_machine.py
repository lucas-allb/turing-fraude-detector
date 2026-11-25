import json
from collections import defaultdict


class TuringMachine:
    def __init__(self, caminho_json):
        with open(caminho_json, encoding="utf-8") as f:
            cfg = json.load(f)

        self.branco = cfg["blank"]
        self.estado_inicial = cfg["initial"]
        self.aceitacao = cfg["accept"]

        self.delta = {
            (estado, lido): (proximo, escrito, mov)
            for estado, lido, proximo, escrito, mov in cfg["transitions"]
        }

    def run(self, entrada, max_passos=100_000):
        fita = defaultdict(lambda: self.branco, enumerate(entrada))
        estado = self.estado_inicial
        cabeca = 0
        passos = 0

        while estado not in self.aceitacao:
            if passos >= max_passos:
                return "TIMEOUT", passos

            chave = (estado, fita[cabeca])
            if chave not in self.delta:
                return "REJEITA", passos

            estado, fita[cabeca], mov = self.delta[chave]
            cabeca += 1 if mov == "R" else -1
            passos += 1

        return self.aceitacao[estado], passos