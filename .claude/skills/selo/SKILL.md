---
name: selo
description: Depois de fazer um commit e dar push neste repositório (Sounavy / GaIA · Opera Vox), busca o timestamp real que o servidor do GitHub registrou pra esse commit, adiciona na tabela verificada, e regenera a prova de anterioridade. Use sempre que acabar de commitar e dar push neste projeto, ou quando o usuário pedir para "selar", "travar", "verificar o commit", "atualizar a procedência", ou `prova/PROVA_DE_ANTERIORIDADE.md` mostrar algum arquivo "fora da tabela verificada". Não serve pra nada antes do push — o commit precisa já estar no GitHub.
---

# Selar um commit — timestamp verificado, não confiado

Este projeto não aceita a data de um commit local como prova de quando algo existiu — `git commit --date` forja isso trivialmente. A prova real é o timestamp que o **servidor** do GitHub registrou ao receber o push, e só a API do GitHub entrega isso (não `git log`). Este skill automatiza a sequência que fecha esse ciclo depois de cada commit.

## Passo a passo

1. **Pegue o SHA do commit que acabou de ser empurrado** (`git log -1 --format=%H`, ou o SHA que o `git push` acabou de confirmar).

2. **Busque o commit real na API do GitHub** — use a ferramenta MCP do GitHub (`get_commit`, ou equivalente disponível na sessão) com:
   - owner: `dralbertoeliasBr`
   - repo: `BOLINHA-`
   - sha: o SHA do passo 1
   - detail: `none` (não precisa do diff, só do timestamp)

   Se nenhuma ferramenta do GitHub estiver disponível nesta sessão, pare aqui e diga isso ao usuário — não invente uma data. Sem a API, não tem selo.

3. **Pegue a data do commit vinda da resposta** — o campo `commit.author.date` (formato `2026-09-11T01:11:03Z`). É essa data, não a hora local, que vale.

4. **Adicione uma entrada nova no topo do array** em `prova/commits_github_verificados.json`, no mesmo formato das entradas existentes:
   ```json
   {
    "sha": "<sha completo>",
    "date": "<data do passo 3>",
    "msg": "<primeira linha da mensagem do commit, sem acento problemático>",
    "url": "https://github.com/dralbertoeliasBr/BOLINHA-/commit/<sha completo>"
   }
   ```

5. **Regenere a prova**: `python3 prova/extrai_provas.py`. A saída deve terminar em "0 sem verificacao GitHub" — se não terminar, algum outro arquivo mudou sem selo; resolva antes de seguir.

6. **Commite e faça push dessa atualização** (`prova/commits_github_verificados.json`, `prova/PROVA_DE_ANTERIORIDADE.md`, `prova/inventario.json`) — isso gera um commit novo, que por sua vez também não está selado ainda. Está tudo bem parar aqui: selar o penúltimo commit com o último é o padrão deste projeto (ver o histórico de `prova/commits_github_verificados.json` — cada entrada sela o commit anterior a ela). Não entre num laço infinito tentando selar o próprio commit do selo.

## O que reportar

Diga o SHA selado, a data real do GitHub, e o resultado de `extrai_provas.py` (quantos arquivos, quantos sem verificação). Se `extrai_provas.py` mostrar mais de zero "sem verificação" mesmo depois deste processo, liste exatamente quais arquivos e seus SHAs — não diga "tudo certo" se não está.
