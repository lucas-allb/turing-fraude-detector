# Detecção de anomalias em transações financeiras: Isolation Forest x Máquina de Turing

Trabalho de Teoria da Computação. Compara dois
procedimentos de detecção de anomalias na base IBM Transactions for Anti Money
Laundering (HI-Small): um modelo de aprendizado não supervisionado (Isolation Forest,
executado no Google Colab) e uma Máquina de Turing que compara o valor da transação
com um limiar fixo, definido previamente.

O Isolation Forest comparado é o descrito no artigo: 43 características, 100 árvores,
`max_samples` 256, `contamination` 0,005, `random_state` 42, treinado no conjunto de
treino, com limiar no percentil 98 do score na validação (taxa de sinalização de 2%).

## Como funciona a Máquina de Turing

- O valor pago vira uma faixa logarítmica, `min(int(log10(valor + 1) * 5), 60)`, que
  preserva a ordem dos valores.
- A fita recebe `1^a # 1^b`, em que `a` é a faixa da transação e `b` é a faixa do limiar.
- A máquina risca um `1` de cada lado até um dos blocos acabar. Se os da direita acabam
  primeiro (`a > b`), a transação é **anômala** (estado `q7`). Caso contrário, é
  **normal** (estado `q6`).
- O limiar é o percentil 99 de `Amount Paid` no conjunto de treino (16.389.049,48,
  faixa 36), fixado antes da execução.

## Estrutura

```
turing-fraude-detector/
├── data/
│   └── teste.csv                      (não versionado)
├── machines/
│   └── comparador.json                definição da Máquina de Turing
├── resultados/
│   ├── analise_complementar.txt       saída da análise complementar
│   ├── avaliacao.txt                  saída da avaliação usada no artigo
│   ├── isolation_forest.csv           (não versionado)
│   └── turing.csv                     (não versionado)
├── src/
│   ├── __init__.py
│   ├── analise_complementar.py        sobreposição nas lavagens e ordenação (AUC)
│   ├── classify.py                    aplica a máquina ao conjunto de teste
│   ├── complexidade.py                resume os passos executados
│   ├── encoder.py                     valor em faixa logarítmica e fita 1^a # 1^b
│   ├── evaluate.py                    compara a máquina com o Isolation Forest
│   └── turing_machine.py              simulador com limite de passos
├── tests/
│   ├── test_classify.py
│   ├── test_complexidade.py
│   ├── test_encoder.py
│   └── test_machine.py
├── .gitignore
├── README.md
└── requirements.txt
```

Os arquivos marcados como "não versionado" estão no `.gitignore` e precisam ser gerados
localmente (veja "Como reproduzir").

## Como reproduzir

1. Ambiente (Python 3.13):

   ```
   python -m venv .venv
   .venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. No notebook do Colab (Isolation Forest), exporte `teste.csv` e `isolation_forest.csv`
   com o conjunto de teste (1.015.558 transações). Coloque `teste.csv` em `data/` e
   `isolation_forest.csv` em `resultados/`. Esses arquivos não são versionados. O
   `isolation_forest.csv` deve vir do modelo de 43 características: na conferência, ele
   marca 6.293 transações e acerta 71 lavagens.

3. Execute, da raiz do projeto:

   ```
   python -m src.classify
   python -m src.evaluate
   python -m src.complexidade
   python -m src.analise_complementar
   python -m pytest -v
   ```

## Resultados (conjunto de teste, 1.015.558 transações)

| Método | Marcadas | Precisão | Revocação | F1 |
|---|---|---|---|---|
| Máquina de Turing | 5.834 | 0,002 | 0,007 | 0,003 |
| Isolation Forest | 6.293 | 0,011 | 0,040 | 0,018 |

Concordância de 99,08% e Kappa de Cohen de 0,2208. Apenas 1.367 transações foram
marcadas pelos dois métodos. A máquina executa, em média, 636 passos por transação.

Análise complementar, sem depender do ponto de corte (prevalência de lavagem: 0,0018):

| Método | AUC-ROC | Precisão média |
|---|---|---|
| Máquina de Turing (faixa do valor) | 0,717 | 0,0032 |
| Isolation Forest (score) | 0,642 | 0,0035 |

Entre as 1.797 lavagens reais, a Máquina de Turing detectou 13 e o Isolation Forest 71;
6 foram detectadas pelos dois métodos.

## Limitações

- O critério da máquina usa só o valor pago, sem conversão entre moedas.
- O corte no percentil 99 captura apenas o extremo superior dos valores, e o limiar não
  foi reajustado com base no conjunto de teste.
- O limiar do Isolation Forest foi escolhido na validação com os rótulos (maior F1),
  enquanto o da máquina foi fixado previamente, sem rótulos.
- A base é sintética e a classe de lavagem é muito rara (0,18% do conjunto de teste).
- O limiar vem do treino, e o teste é posterior no tempo.

## Autores

Natália Nascimento, Jamili Oliveira e Lucas Albuquerque.