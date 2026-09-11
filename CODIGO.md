# Código — tudo que roda, num lugar só

Não duplica nada. Cada linha abaixo é um arquivo real deste repositório, com o comando exato pra rodar e o que ele produz. Se algo aqui não bater com o arquivo, o arquivo é que vale — este documento é só o mapa.

**Nenhuma peça precisa de conta, de chave, de mim, nem da Anthropic.** Python 3.8+ puro em sete das oito ferramentas — a oitava (`ferramentas/gera_pdf.py`) só usa navegador na etapa final, e mesmo essa, sem navegador, entrega o HTML pronto pra imprimir em qualquer um. Roda em celular, notebook velho, servidor. É seu, é aberto, é exatamente o que está no repositório público — clona e roda, sem pedir licença pra ninguém.

## A prova do paper — `paper/prova/`

| arquivo | comando | o que produz |
|---|---|---|
| `nucleo.py` | (biblioteca — importada pelos outros) | codificador aritmético binário determinístico: contador, misturador, `Enc`/`Dec`. Inteiros puros, zero float no caminho crítico |
| `experimentos.py` | (biblioteca — 15 funções, `e1_contagem` a `e15_rrns_importancia`) | cada função é uma asserção da tabela do paper (§9) — roda, mede, devolve número |
| `roda_tudo.py` | `python3 paper/prova/roda_tudo.py` | roda os 15 experimentos em sequência (~40s), escreve `RESULTADOS.md` e `resultados.json` com SHA-256 de cada peça de código e corpus usado |
| `auditoria_cinco_portoes.py` | `python3 paper/prova/auditoria_cinco_portoes.py` | audita as 38 asserções do paper contra as cinco regras do protocolo (`CLAUDE.md`), mecanicamente. Escreve `AUDITORIA_CINCO_PORTOES.md`. Hoje: 38/38 |

## Anterioridade — `prova/`

| arquivo | comando | o que produz |
|---|---|---|
| `extrai_provas.py` | `python3 prova/extrai_provas.py` | SHA-256 de cada arquivo da obra + timestamp verificado na API do GitHub (não no `git log` local, que se forja). Escreve `PROVA_DE_ANTERIORIDADE.md` e `inventario.json` |

## Pipeline de impressão — `ferramentas/`

| arquivo | comando | o que produz |
|---|---|---|
| `md2html.py` | (biblioteca) | converte markdown em HTML de impressão — puro stdlib, sem CDN |
| `gera_pdf.py` | `python3 ferramentas/gera_pdf.py <fonte.md> <capa.html> <saida_base>` | `.html` sempre; `.pdf` se houver Chromium disponível (best-effort, nunca falha calado — sem navegador, imprime a instrução exata pra terminar manual em qualquer navegador) |

## Modelo hipotético — `seguranca/`

| arquivo | comando | o que produz |
|---|---|---|
| `simulacao_sobrevivencia.py` | `python3 seguranca/simulacao_sobrevivencia.py` | Monte Carlo puro (~1min20s): tempo mediano até comprometimento, com e sem vantagem de detecção automatizada. Toda suposição é parâmetro nomeado no próprio arquivo. Escreve `RESULTADOS.md` |

## Pra rodar tudo, do zero, em qualquer máquina

```bash
git clone https://github.com/dralbertoeliasBr/BOLINHA-.git
cd BOLINHA- && git checkout claude/llm-gemeas-compressao-lwnpwn

python3 paper/prova/roda_tudo.py               # ~40s  — os 15 experimentos
python3 paper/prova/auditoria_cinco_portoes.py # ~1s   — audita as 38 asserções
python3 prova/extrai_provas.py                 # ~1s   — hash + procedência
python3 seguranca/simulacao_sobrevivencia.py   # ~1min — modelo de sobrevivência
```

Se um número que sair aqui não bater com o que está publicado no paper, no `simbiose/` ou em qualquer outro documento — o publicado está errado, não quem rodou. É a regra 1 do `CLAUDE.md`, e vale pra este documento também.

---

*Antônio Alberto Lopes Elias · Sounavy · ORCID [0000-0002-5602-9916](https://orcid.org/0000-0002-5602-9916) · Coautoria humano–IA.*
