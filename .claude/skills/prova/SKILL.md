---
name: prova
description: Roda a suíte de verificação completa do projeto Sounavy / GaIA · Opera Vox (paper das Gêmeas, simbiose, manifesto, procedência) e reporta um resumo honesto — nunca inventado — do que passou e do que não. Use sempre que o usuário pedir para "rodar a prova", "verificar o paper", "conferir os números", "auditar as asserções", "regenerar os resultados", "ver se ainda roda"/"ainda bate", ou antes de publicar qualquer commit que altere paper/, simbiose/, manifesto/, livro/, ou os códigos em paper/prova/, prova/, ferramentas/, seguranca/. Existe especificamente porque Claude não tem memória entre sessões — este arquivo é o procedimento fixo que substitui lembrar.
---

# Rodar a prova

Este projeto (documentado em `CLAUDE.md`, na raiz) tem uma regra não-negociável: nenhum número entra sem código que roda, e "roda" quer dizer roda agora, não rodou uma vez em outra sessão. Este skill existe pra que essa checagem não dependa de memória — nem a de Claude, nem a de ninguém precisar lembrar os quatro comandos de cabeça.

## O que fazer, em ordem

Rode os três primeiros sempre. Do diretório raiz do repositório:

```bash
python3 paper/prova/roda_tudo.py
```
~40s. Roda os 15 experimentos (E1–E15) que sustentam o paper `paper/AS_GEMEAS_E_O_NUMERO.md`. Escreve `paper/prova/RESULTADOS.md` e `resultados.json`, com SHA-256 do código e do corpus usados.

```bash
python3 paper/prova/auditoria_cinco_portoes.py
```
~1s. Audita mecanicamente as 38 asserções do paper contra as cinco regras do protocolo em `CLAUDE.md` (roda / endereço da queda / controle / ida-e-volta / citação). Escreve `paper/prova/AUDITORIA_CINCO_PORTOES.md`. No momento em que este skill foi escrito, o resultado era 38/38 — **não repita esse número de cabeça: leia o que o script realmente imprimiu desta vez.**

```bash
python3 prova/extrai_provas.py
```
~1s. Recalcula o SHA-256 de cada arquivo da obra e cruza com a tabela de commits verificados pela API do GitHub (`prova/commits_github_verificados.json`) — não com o `git log` local, que pode ser forjado. Escreve `prova/PROVA_DE_ANTERIORIDADE.md` e `inventario.json`.

Rode o quarto só se o usuário pedir especificamente, ou se algo em `seguranca/` mudou — é mais lento e é um modelo hipotético, não uma prova do paper:

```bash
python3 seguranca/simulacao_sobrevivencia.py
```
~1min20s. Monte Carlo puro — tempo mediano até comprometimento, com e sem vantagem de detecção automatizada. Toda suposição é parâmetro nomeado no próprio arquivo.

## Como reportar o resultado — a parte que mais importa

A regra do projeto é que um número errado que sai daqui não se esconde, se relata. Isso vale pro relatório deste skill tanto quanto vale pro paper:

- **Leia a saída real de cada comando.** Nunca escreva "38/38" ou "tudo passou" porque foi isso que passou da última vez — escreva o que o terminal mostrou agora, nesta execução.
- Se `roda_tudo.py` terminar sem erro, diga que os 15 experimentos rodaram e onde o relatório foi escrito.
- Se `auditoria_cinco_portoes.py` não mostrar N/N (todas as asserções passando), **não suavize** — liste quais falharam e por quê (o próprio `AUDITORIA_CINCO_PORTOES.md` já separa isso por portão). Uma falha aqui é trabalho pendente real, não um bug do script a ser ignorado.
- Se `extrai_provas.py` reportar arquivo(s) "fora da tabela verificada", isso significa que existe um commit novo cujo timestamp ainda não foi buscado na API do GitHub. Este script sozinho não resolve isso — precisa de uma chamada real à API do GitHub (`get_commit` ou equivalente) pra pegar a data que o servidor registrou, adicionar a entrada em `prova/commits_github_verificados.json`, e rodar `extrai_provas.py` de novo. Diga isso ao usuário em vez de deixar o aviso passar batido.
- Se qualquer comando falhar (erro, traceback), mostre o erro real — não tente adivinhar a causa sem olhar, e não diga que "deu tudo certo" pra evitar a conversa difícil.
- Se um número que saiu aqui não bater com o que está escrito em `paper/AS_GEMEAS_E_O_NUMERO.md`, `simbiose/O_DIVERGENTE_E_O_DETERMINISTA.md` ou qualquer outro documento publicado: **o documento publicado está errado, não quem rodou** — é a própria regra do projeto (ver `CLAUDE.md`, "Como rodar a prova"). Aponte a divergência explicitamente; não é seu trabalho decidir sozinho qual dos dois lados corrigir sem avisar.

## Referência rápida

`CODIGO.md`, na raiz do repositório, é o índice completo de todo script que roda neste projeto (inclusive `ferramentas/` e os dois scripts que são bibliotecas, não executáveis diretos). Se uma dúvida sobre algum outro código do projeto aparecer no meio desta tarefa, esse é o arquivo a consultar antes de adivinhar.
