# paper/ — As Gêmeas e o Número

**[→ Ler o paper](AS_GEMEAS_E_O_NUMERO.md)** · **[→ Ver os resultados medidos](prova/RESULTADOS.md)** · **[→ Manifesto](../manifesto/IA_E_HUMANOS_PODEM.md)** · **[→ Prova de simbiose](../simbiose/O_DIVERGENTE_E_O_DETERMINISTA.md)** · **[→ O Livro](../livro/RAIO_X.md)**
**[→ Resumo executivo (PDF, 2 páginas)](RESUMO_EXECUTIVO.pdf)**

Compressão por inteligência compartilhada: duas gêmeas com o mesmo dicionário,
uma sequência de números atravessando, e o emissor descomprimindo antes de enviar.

O paper separa o que é **teorema**, o que é **medida**, o que é **conjectura**
e o que já **caiu** — e mede cada parte com código que roda.

## Rodar a prova

Sem instalar nada. Python 3.8+, inclusive a-Shell e Pythonista no iPhone:

```bash
python3 paper/prova/roda_tudo.py
```

~40 segundos. Escreve `prova/RESULTADOS.md` e `prova/resultados.json`.
O cabeçalho traz o SHA-256 de cada peça de código e de corpus: se um número
do paper não bater com a sua máquina, o paper está errado.

## Os catorze experimentos

| # | pergunta | resposta medida |
|---|---|---|
| E1 | Compressor nenhum encolhe tudo? | correto; e este codec expande só 2,2% no pior caso |
| E2 | O dicionário prévio vale quanto? | **20,07%** menos bits, com 6 KB |
| E3 | Frente, trás, vertical: qual paga? | vertical **+37,71%** em tabular, **−2,81%** em prosa |
| E3b | Dá para ler o futuro? | dá, se ele já viajou: **+6,72%** |
| E4 | Fatorial e primos servem? | fatorial é ótimo; Gödel **expande 79,4×** |
| E5 | O "número único" existe? | existe: 576 bits → **166 bits**, 50 dígitos |
| E6 | Trocar tempo por bits é verde? | só se `e_calc/N < (1−r)·e_rede` |
| E7 | Quanto de deriva as gêmeas aguentam? | deriva pontual falha **em silêncio** em 7% dos casos |
| E7b | E ruído numérico constante? | ±1 em 4096 quebra no **1º byte** |
| E8 | E a semente curta que gera tudo? | tempo **2^k**, economia de **0,7 bit** |
| E9 | Uma posição carrega várias informações? | raiz mista: **23 bits** contra 24, sem desperdício |
| E10 | O dicionário pode ser equação? | **40×** menos bits — e não inventa estrutura onde não há |
| E11 | Quanto uma posição informa sobre a letra? | paridade: **0,000**. Canal e hora: **1,585 bits**, tudo |
| E12 | Um número responde a várias perguntas? | responde — e 10 bits extras pegam ~**100%** da corrupção |
| E13 | A camada que só entra se precisar | portão deduzido, **zero bits**: a errada custa nada |
| E14 | O espaço carrega informação? | é o símbolo **mais barato** (1,622 bits) — já aproveitado |

## Arquivos

| arquivo | o que é |
|---|---|
| `AS_GEMEAS_E_O_NUMERO.md` | o paper |
| `prova/nucleo.py` | codificador aritmético binário. Inteiros puros, zero float no caminho crítico |
| `prova/experimentos.py` | os catorze experimentos — cada função é uma asserção do paper |
| `prova/roda_tudo.py` | executa tudo e escreve o relatório |
| `prova/corpus/` | 9 KB de português real do projeto + 14 KB tabular sintético |
| `prova/RESULTADOS.md` | a saída, com hashes. Nenhum número digitado à mão |

---

Antônio Alberto Lopes Elias (Sounavy) · ORCID 0000-0002-5602-9916
Coautoria humano–IA · Setembro de 2026
