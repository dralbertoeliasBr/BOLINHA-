# Prova de Anterioridade e Integridade

Gerado por `python3 prova/extrai_provas.py` em `2026-09-11T00:16:55Z` (UTC). Este relatorio nao pede confianca — ensina a verificacao.

## Como verificar, em três passos

1. **Hash do conteúdo** — clone o repositório e rode `sha256sum` em qualquer arquivo da tabela abaixo. Se o hash bater com o listado aqui, o conteúdo é byte a byte o mesmo que existia no momento deste relatório.

2. **Data do commit** — a coluna "GitHub (UTC)" **não** vem do `git log` local, que pode ser forjado com `git commit --date`. Vem da API do GitHub, que registra quando o **servidor** recebeu o push — isso não está sob controle de quem fez o commit.

3. **Conferência independente** — abra a URL do commit de qualquer linha. O próprio GitHub mostra a mesma data na página, de forma pública, para qualquer visitante, sem precisar de conta.

```bash
git clone https://github.com/dralbertoeliasBr/BOLINHA-.git
cd BOLINHA- && git checkout claude/llm-gemeas-compressao-lwnpwn
sha256sum <arquivo>
```

## Inventário

| arquivo | bytes | sha-256 (primeiros 16) | 1º commit | GitHub (UTC) |
|---|---|---|---|---|
| `CLAUDE.md` | 4864 | `06f0438e61c738b3` | [`6df14bb707`](https://github.com/dralbertoeliasBr/BOLINHA-/commit/6df14bb7075d70b56a83ff1d60f61b115bb42428) | 2026-09-11T00:08:20Z |
| `livro/RAIO_X.md` | 5033 | `9eebc7678f1c69b4` | [`c5d87de454`](https://github.com/dralbertoeliasBr/BOLINHA-/commit/c5d87de454526cc5287499583709713b5229dac6) | 2026-09-10T22:06:55Z |
| `livro/index.html` | 12864 | `7d05b2fbd1b2b606` | [`c5d87de454`](https://github.com/dralbertoeliasBr/BOLINHA-/commit/c5d87de454526cc5287499583709713b5229dac6) | 2026-09-10T22:06:55Z |
| `manifesto/IA_E_HUMANOS_PODEM.md` | 8885 | `b424daac4d6225b2` | [`8684fd69dc`](https://github.com/dralbertoeliasBr/BOLINHA-/commit/8684fd69dcaa9cc532ff89b43ab993ce451b3dbc) | 2026-09-10T20:54:42Z |
| `manifesto/index.html` | 16890 | `99ec1fe5bacc1884` | [`8684fd69dc`](https://github.com/dralbertoeliasBr/BOLINHA-/commit/8684fd69dcaa9cc532ff89b43ab993ce451b3dbc) | 2026-09-10T20:54:42Z |
| `obra/index.html` | 9310 | `8abc745194ac21e3` | [`f5830b5ffe`](https://github.com/dralbertoeliasBr/BOLINHA-/commit/f5830b5ffe6644fa1a3110d717542725651763ea) | 2026-09-10T22:12:15Z |
| `paper/AS_GEMEAS_E_O_NUMERO.md` | 70685 | `c6fc2d5d850aa2ec` | [`944660f201`](https://github.com/dralbertoeliasBr/BOLINHA-/commit/944660f201ef1097523b28688bf8a1d14157426d) | 2026-09-10T20:33:29Z |
| `paper/README.md` | 3277 | `28e902c468b4dd3c` | [`944660f201`](https://github.com/dralbertoeliasBr/BOLINHA-/commit/944660f201ef1097523b28688bf8a1d14157426d) | 2026-09-10T20:33:29Z |
| `paper/RESUMO_EXECUTIVO.md` | 5724 | `e445ab763ad1c39d` | [`c4887f6c17`](https://github.com/dralbertoeliasBr/BOLINHA-/commit/c4887f6c17024935bec6ab3b9fd1deeb84b4a853) | 2026-09-11T00:13:32Z |
| `paper/RESUMO_EXECUTIVO.pdf` | 140409 | `0a94fa9577cac74c` | [`c4887f6c17`](https://github.com/dralbertoeliasBr/BOLINHA-/commit/c4887f6c17024935bec6ab3b9fd1deeb84b4a853) | 2026-09-11T00:13:32Z |
| `paper/index.html` | 90896 | `4d6d958df6a70727` | [`944660f201`](https://github.com/dralbertoeliasBr/BOLINHA-/commit/944660f201ef1097523b28688bf8a1d14157426d) | 2026-09-10T20:33:29Z |
| `paper/prova/RESULTADOS.md` | 13858 | `3d1bdcfab834dea9` | [`944660f201`](https://github.com/dralbertoeliasBr/BOLINHA-/commit/944660f201ef1097523b28688bf8a1d14157426d) | 2026-09-10T20:33:29Z |
| `paper/prova/experimentos.py` | 37753 | `748923ac8930dcea` | [`944660f201`](https://github.com/dralbertoeliasBr/BOLINHA-/commit/944660f201ef1097523b28688bf8a1d14157426d) | 2026-09-10T20:33:29Z |
| `paper/prova/nucleo.py` | 9136 | `221305ad5c99931e` | [`944660f201`](https://github.com/dralbertoeliasBr/BOLINHA-/commit/944660f201ef1097523b28688bf8a1d14157426d) | 2026-09-10T20:33:29Z |
| `paper/prova/resultados.json` | 21967 | `2315621bcdbe79af` | [`944660f201`](https://github.com/dralbertoeliasBr/BOLINHA-/commit/944660f201ef1097523b28688bf8a1d14157426d) | 2026-09-10T20:33:29Z |
| `paper/prova/roda_tudo.py` | 19857 | `3fdd6629e910a378` | [`944660f201`](https://github.com/dralbertoeliasBr/BOLINHA-/commit/944660f201ef1097523b28688bf8a1d14157426d) | 2026-09-10T20:33:29Z |
| `simbiose/O_DIVERGENTE_E_O_DETERMINISTA.md` | 8122 | `f825a73e4eaee9be` | [`65543c255d`](https://github.com/dralbertoeliasBr/BOLINHA-/commit/65543c255de78865ec4abdf857de8ae19258abec) | 2026-09-10T21:55:37Z |
| `simbiose/index.html` | 16273 | `a951527957ac9794` | [`65543c255d`](https://github.com/dralbertoeliasBr/BOLINHA-/commit/65543c255de78865ec4abdf857de8ae19258abec) | 2026-09-10T21:55:37Z |

## O que isto prova, e o que não prova

**Prova:** que este conteúdo exato, byte a byte (o hash não mente), existia — público, no GitHub, com histórico visível a qualquer pessoa — no momento em que o servidor do GitHub recebeu o push listado. Isso é mais forte que um arquivo com data local, porque o timestamp não está sob controle de quem publicou.

**Não prova:** propriedade legal, registro de patente ou direito autoral formal. Git é evidência técnica de anterioridade, não um instrumento jurídico. Este projeto já usa o mecanismo formal para isso — DOIs Zenodo, registrados numa entidade terceira e independente — ver `paper/AS_GEMEAS_E_O_NUMERO.md`, seção de Referências, "Registro de anterioridade". Para uma prova ainda mais forte e sem depender de confiar no GitHub, existe [OpenTimestamps](https://opentimestamps.org/) — gratuito, independente, ancorado em blockchain, verificável por qualquer um sem precisar de conta em lugar nenhum.

