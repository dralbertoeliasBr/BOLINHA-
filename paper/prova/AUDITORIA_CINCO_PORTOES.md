# Auditoria dos cinco portões

Verificação mecânica, não opinião: cada portão abaixo já era regra em `CLAUDE.md` antes desta auditoria existir. O que muda aqui é que agora um script confere, linha a linha, em vez de confiar em quem escreveu — inclusive em quem escreveu este script.

| portão | o que verifica |
|---|---|
| 1 — roda | a asserção cita um experimento (`Exx`) e a função `exx` existe em `experimentos.py`, ou é TEOREMA/LITERATURA com referência real |
| 2 — endereço da queda | toda asserção REFUTADO carrega um número que mostra a queda, não só a palavra |
| 3 — controle | toda alegação de informação mútua/correlação/paridade tem controle citado no texto **e** embaralhamento real no código |
| 4 — ida-e-volta (global) | `nucleo.py` codifica **e** decodifica, e algum experimento compara o decodificado com o original antes de aprovar |
| 5 — citação (global) | o paper carrega ORCID e BibTeX |

## Portões 1–3, por asserção

| # | 1 roda | 2 endereço | 3 controle | veredito |
|---|---|---|---|---|
| A1 | OK | OK | OK | **passa** |
| A2 | OK | OK | OK | **passa** |
| A3 | OK | OK | OK | **passa** |
| A4 | OK | OK | OK | **passa** |
| A5 | OK | OK | OK | **passa** |
| A6 | OK | OK | OK | **passa** |
| A7 | OK | OK | OK | **passa** |
| A8 | OK | OK | OK | **passa** |
| A9 | OK | OK | OK | **passa** |
| A10 | OK | OK | OK | **passa** |
| A11 | OK | OK | OK | **passa** |
| A12 | OK | OK | OK | **passa** |
| A13 | OK | OK | OK | **passa** |
| A14 | OK | OK | OK | **passa** |
| A15 | OK | OK | OK | **passa** |
| A16 | OK | OK | OK | **passa** |
| A17 | OK | OK | OK | **passa** |
| A18 | OK | OK | OK | **passa** |
| A19 | OK | OK | OK | **passa** |
| A20 | OK | OK | OK | **passa** |
| A21 | OK | OK | OK | **passa** |
| A22 | OK | OK | OK | **passa** |
| A23 | OK | OK | OK | **passa** |
| A24 | OK | OK | OK | **passa** |
| A25 | OK | OK | OK | **passa** |
| A26 | OK | OK | OK | **passa** |
| A27 | OK | OK | OK | **passa** |
| A28 | OK | OK | OK | **passa** |
| A29 | OK | OK | OK | **passa** |
| A30 | OK | OK | OK | **passa** |
| A31 | OK | OK | OK | **passa** |
| A32 | OK | OK | OK | **passa** |
| A33 | OK | OK | OK | **passa** |
| A34 | OK | OK | OK | **passa** |
| A35 | OK | OK | OK | **passa** |
| A36 | OK | OK | OK | **passa** |
| A37 | OK | OK | OK | **passa** |
| A38 | OK | OK | OK | **passa** |

## Portões 4–5, globais

| portão | veredito | detalhe |
|---|---|---|
| 4 — ida-e-volta | OK | codifica=True decodifica=True função-ida-e-volta=True compara(==)=True usa-decodificação/hash=True |
| 5 — citação | OK | ORCID presente=True, BibTeX presente=True |

## Veredito final

**38/38** asserções passam os portões 1–3. Portões globais: 4 = OK, 5 = OK.

**A obra passa nos cinco portões, mecanicamente conferida.**

