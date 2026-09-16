# Bolinha Guia — protótipo de teste

**Isto não é o site em produção.** A Bolinha real, em `www.sounavy.com`, é `index.html` na raiz deste repositório — e continua intocada por esta pasta, conforme a regra do `CLAUDE.md`. Esta pasta é um protótipo separado, pra testar uma ideia específica antes de decidir se ela entra na produção.

## A ideia sendo testada

*"Bolinha é apenas a bolinha overlay que paira em cima de onde 'interagir' para realizar ou iniciar até chegar onde se deseja, como um guia, um tutor que te guia ensinando (em silêncio, quase sempre) para se poder querer usar sem complicações de navegação, por apps e ferramentas, uma 'segurança'. Acionável quando se não lembra ou desconhece o caminho."*

Em código: um botão flutuante que, acionado, guia a pessoa por uma tarefa real — passo a passo, iluminando só o próximo elemento certo, sem explicar em texto o que fazer a cada passo (fala uma vez, no início; depois só aponta). A pessoa completa a tarefa sozinha; a Bolinha nunca faz por ela.

## O protótipo

`poc_farol_inclusao.html` — HTML/CSS/JS puro, sem dependência, abre em qualquer navegador. Simula um app de banco genérico; a tarefa é mandar um Pix de R$ 50 pra um contato. Reflete a identidade visual do resto do projeto (mesmos tokens do `CLAUDE.md`).

Rodar localmente: abrir o arquivo direto no navegador. Não precisa de servidor.

## O que isto prova, e o que não prova

Prova que o mecanismo — destacar só o próximo alvo certo, recusar avançar em toque errado, falar uma vez e depois silenciar — funciona como interação, numa tarefa simulada. **Não prova** que isso resolve inclusão digital de verdade: isso só se mede com gente real, fora de uma simulação, tentando uma tarefa real. Esse teste ainda não foi feito.
