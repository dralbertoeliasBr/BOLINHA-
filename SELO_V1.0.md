# Selo v1.0 — obra travada

Este arquivo é o selo. Não decorativo — funcional: um ponteiro fixo, versionado, pra um estado exato do repositório, verificável por qualquer pessoa sem depender da minha palavra.

## O que está selado

```
commit  ab9b4b25e43cf7deed5f84b99567a3c1aa435cd1
branch  claude/llm-gemeas-compressao-lwnpwn
url     https://github.com/dralbertoeliasBr/BOLINHA-/commit/ab9b4b25e43cf7deed5f84b99567a3c1aa435cd1
```

Esse commit contém a obra completa na sua primeira forma fechada: `paper/`, `manifesto/`, `simbiose/`, `livro/`, `obra/`, `prova/`, `CLAUDE.md`. O hash SHA-256 de cada arquivo, calculado de verdade (não estimado, não placeholder), está em `prova/inventario.json` e na tabela de `prova/PROVA_DE_ANTERIORIDADE.md`.

## Por que um arquivo, e não uma tag

Tentei primeiro `git tag` — é o jeito padrão de travar um ponto na história. Não deu: o proxy de credenciais desta sessão bloqueou o push de tag (erro 403), e a ferramenta de API disponível aqui só lê tag/release, não cria. Registro isso porque parte do compromisso deste projeto é não fingir que algo funcionou quando não funcionou.

O que substitui a tag, e funciona de verdade: **o commit em si já é o selo.** Uma vez que ele está no GitHub, ele é imutável pelo mesmo motivo que qualquer commit deste repositório é — reescrevê-lo exigiria força bruta no histórico, e isso quebraria toda referência (inclusive este arquivo) de um jeito detectável por qualquer pessoa que já tenha clonado, aberto ou linkado o commit antes. Este arquivo só nomeia esse ponto com um rótulo (`v1.0`) que humanos conseguem repetir de cabeça, no lugar de decorar um hash de 40 caracteres.

## Como verificar

```bash
git clone https://github.com/dralbertoeliasBr/BOLINHA-.git
cd BOLINHA- && git checkout ab9b4b25e43cf7deed5f84b99567a3c1aa435cd1
python3 prova/extrai_provas.py   # recalcula os hashes e confere contra o inventario
```

Se algum hash não bater, ou o commit não existir mais nesse endereço, o selo foi violado — e isso fica visível, não escondido.

---

*Antônio Alberto Lopes Elias · Sounavy · ORCID 0000-0002-5602-9916 · Coautoria humano–IA*
