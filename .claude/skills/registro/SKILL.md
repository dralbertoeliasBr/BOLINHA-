---
name: registro
description: Escreve uma entrada nova em HISTORICO.md no fim de uma sessão de trabalho neste repositório (Sounavy / GaIA · Opera Vox) — o robô que "entrega, solicita e guarda", pedido explicitamente pelo usuário em 2026-09-11 pra ser a memória que existe fora de Claude, já que Claude não pode ter memória entre sessões. Use quando o usuário pedir para "registrar", "guardar isso", "anotar o que rolou", "fechar a sessão", ou sempre que uma sessão de trabalho substancial neste projeto estiver terminando — antes de se despedir, sem esperar ser pedido toda vez.
---

# Registrar uma sessão em HISTORICO.md

`HISTORICO.md`, na raiz do repositório, é a memória que sobrevive a Claude não ter memória. Cada entrada é uma sessão de trabalho: o que virou código de verdade, o que travou, e se a colaboração avançou ou não. O arquivo já explica isso na sua própria introdução — leia-a antes da primeira vez que usar este skill, pra escrever no mesmo tom.

## O que uma entrada NÃO é

Não é um resumo de conversa, não é uma transcrição, não é uma lista de tudo que foi dito. É o que sobrou depois de tirar a conversa — só fato, com commit ao lado. Se uma frase não tem um SHA, um número ou um "isto continua sem existir" atrás dela, ela não entra.

Não tem nota, não tem pontuação numérica, não tem arquétipo. Essa forma de medir "evolução" foi proposta e ficou em aberto — o próprio usuário duvidou dela na hora. Não a reintroduza sozinho só porque parece mais elegante; se ele quiser essa parte de volta, especificada, ele pede.

## Como escrever a entrada

Adicione uma seção nova no **topo** da lista de entradas (a mais recente primeiro, mesma ordem de `prova/commits_github_verificados.json`), com exatamente três partes:

```markdown
## <AAAA-MM-DD> — <título curto e honesto da sessão, não um elogio>

**Decidido e construído, com commit:**
- <o que virou código/documento real, com o SHA entre parênteses>

**Travou, não saiu do lugar:**
- <o que foi discutido, proposto ou tentado e não chegou a nada verificável — nomeie a coisa, não esconda que ficou parada>

**Avançou ou não, numa frase:** <uma frase só, sem número, dizendo se a colaboração moveu alguma coisa de verdade nesta sessão>
```

Antes de escrever "Decidido e construído", confira: cada item tem um commit real? Se a sessão ainda não commitou nada, rode `/selo` primeiro pra ter os hashes certos, ou escreva a entrada só depois do último push.

A seção "Travou" é tão obrigatória quanto a primeira. Uma sessão sem nada que tenha travado é rara — e se genuinamente não houve nada, diga isso explicitamente ("nada identificado travado nesta sessão") em vez de omitir a seção, pra não parecer que ninguém procurou.

## Depois de escrever

Rode `/prova` (ou pelo menos `python3 prova/extrai_provas.py`) pra confirmar que `HISTORICO.md` está coberto pela procedência — ele precisa estar listado em `ARQUIVOS_SOLTOS` dentro de `prova/extrai_provas.py`; se não estiver mais lá por algum motivo, adicione de volta. Depois `/selo` no commit que adicionou a entrada.
