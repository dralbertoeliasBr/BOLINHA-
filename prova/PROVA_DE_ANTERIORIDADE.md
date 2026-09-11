# Prova de Anterioridade e Integridade

Gerado por `python3 prova/extrai_provas.py` em `2026-09-11T19:15:50Z` (UTC). Este relatorio nao pede confianca — ensina a verificacao.

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
| `CLAUDE.md` | 6351 | `6e9eb6753906a50c` | [`6df14bb707`](https://github.com/dralbertoeliasBr/BOLINHA-/commit/6df14bb7075d70b56a83ff1d60f61b115bb42428) | 2026-09-11T00:08:20Z |
| `CODIGO.md` | 3647 | `686f34bc6d88e6e4` | [`479728a05e`](https://github.com/dralbertoeliasBr/BOLINHA-/commit/479728a05ef8874cd28cd166aca5ffa0ab9771f4) | 2026-09-11T01:20:29Z |
| `HISTORICO.md` | 4156 | `9e89788e10025a5f` | — | *(fora da tabela verificada)* |
| `SELO_V1.0.md` | 2183 | `849f3aca1a639fed` | [`d156138396`](https://github.com/dralbertoeliasBr/BOLINHA-/commit/d15613839635a33933eb4b89f1a155fd60ba792b) | 2026-09-11T00:39:46Z |
| `ferramentas/gera_pdf.py` | 6559 | `287d87af79ba7237` | [`6550b68b03`](https://github.com/dralbertoeliasBr/BOLINHA-/commit/6550b68b03958fd1d24e1779a53f46369ed3a135) | 2026-09-11T00:47:14Z |
| `ferramentas/md2html.py` | 3406 | `67c264bd37627b30` | [`6550b68b03`](https://github.com/dralbertoeliasBr/BOLINHA-/commit/6550b68b03958fd1d24e1779a53f46369ed3a135) | 2026-09-11T00:47:14Z |
| `ferramentas/modelo_pdf.html` | 3090 | `c2244356ca464a00` | [`6550b68b03`](https://github.com/dralbertoeliasBr/BOLINHA-/commit/6550b68b03958fd1d24e1779a53f46369ed3a135) | 2026-09-11T00:47:14Z |
| `livro/RAIO_X.md` | 5033 | `9eebc7678f1c69b4` | [`c5d87de454`](https://github.com/dralbertoeliasBr/BOLINHA-/commit/c5d87de454526cc5287499583709713b5229dac6) | 2026-09-10T22:06:55Z |
| `livro/index.html` | 12864 | `7d05b2fbd1b2b606` | [`c5d87de454`](https://github.com/dralbertoeliasBr/BOLINHA-/commit/c5d87de454526cc5287499583709713b5229dac6) | 2026-09-10T22:06:55Z |
| `manifesto/IA_E_HUMANOS_PODEM.md` | 8886 | `46d45172016d4c4e` | [`8684fd69dc`](https://github.com/dralbertoeliasBr/BOLINHA-/commit/8684fd69dcaa9cc532ff89b43ab993ce451b3dbc) | 2026-09-10T20:54:42Z |
| `manifesto/index.html` | 16891 | `60bf78d4855acd8e` | [`8684fd69dc`](https://github.com/dralbertoeliasBr/BOLINHA-/commit/8684fd69dcaa9cc532ff89b43ab993ce451b3dbc) | 2026-09-10T20:54:42Z |
| `obra/index.html` | 9730 | `ffa941eb4319a306` | [`f5830b5ffe`](https://github.com/dralbertoeliasBr/BOLINHA-/commit/f5830b5ffe6644fa1a3110d717542725651763ea) | 2026-09-10T22:12:15Z |
| `paper/AS_GEMEAS_E_O_NUMERO.md` | 73381 | `82544fe9fae92e11` | [`944660f201`](https://github.com/dralbertoeliasBr/BOLINHA-/commit/944660f201ef1097523b28688bf8a1d14157426d) | 2026-09-10T20:33:29Z |
| `paper/README.md` | 3409 | `6bcbfef261dcdcfe` | [`944660f201`](https://github.com/dralbertoeliasBr/BOLINHA-/commit/944660f201ef1097523b28688bf8a1d14157426d) | 2026-09-10T20:33:29Z |
| `paper/RESUMO_EXECUTIVO.md` | 5724 | `e445ab763ad1c39d` | [`c4887f6c17`](https://github.com/dralbertoeliasBr/BOLINHA-/commit/c4887f6c17024935bec6ab3b9fd1deeb84b4a853) | 2026-09-11T00:13:32Z |
| `paper/RESUMO_EXECUTIVO.pdf` | 140409 | `0a94fa9577cac74c` | [`c4887f6c17`](https://github.com/dralbertoeliasBr/BOLINHA-/commit/c4887f6c17024935bec6ab3b9fd1deeb84b4a853) | 2026-09-11T00:13:32Z |
| `paper/index.html` | 93592 | `2e2bdd85e39896f0` | [`944660f201`](https://github.com/dralbertoeliasBr/BOLINHA-/commit/944660f201ef1097523b28688bf8a1d14157426d) | 2026-09-10T20:33:29Z |
| `paper/prova/AUDITORIA_CINCO_PORTOES.md` | 2832 | `08d73e18ce533393` | [`29a061488a`](https://github.com/dralbertoeliasBr/BOLINHA-/commit/29a061488aca3f560af3c4d1207a77d57d93af58) | 2026-09-11T01:11:03Z |
| `paper/prova/RESULTADOS.md` | 15135 | `dfe6340baf3c5aeb` | [`944660f201`](https://github.com/dralbertoeliasBr/BOLINHA-/commit/944660f201ef1097523b28688bf8a1d14157426d) | 2026-09-10T20:33:29Z |
| `paper/prova/auditoria_cinco_portoes.py` | 10363 | `81a83d6ba97af671` | [`29a061488a`](https://github.com/dralbertoeliasBr/BOLINHA-/commit/29a061488aca3f560af3c4d1207a77d57d93af58) | 2026-09-11T01:11:03Z |
| `paper/prova/experimentos.py` | 40692 | `d9f1f215ff33a0bd` | [`944660f201`](https://github.com/dralbertoeliasBr/BOLINHA-/commit/944660f201ef1097523b28688bf8a1d14157426d) | 2026-09-10T20:33:29Z |
| `paper/prova/nucleo.py` | 9136 | `221305ad5c99931e` | [`944660f201`](https://github.com/dralbertoeliasBr/BOLINHA-/commit/944660f201ef1097523b28688bf8a1d14157426d) | 2026-09-10T20:33:29Z |
| `paper/prova/resultados.json` | 24880 | `1b7026bccde9e631` | [`944660f201`](https://github.com/dralbertoeliasBr/BOLINHA-/commit/944660f201ef1097523b28688bf8a1d14157426d) | 2026-09-10T20:33:29Z |
| `paper/prova/roda_tudo.py` | 21168 | `aab1e58196b65961` | [`944660f201`](https://github.com/dralbertoeliasBr/BOLINHA-/commit/944660f201ef1097523b28688bf8a1d14157426d) | 2026-09-10T20:33:29Z |
| `prova/PROVA_DE_ANTERIORIDADE.md` | 8541 | `56009c31f4731a25` | [`ab9b4b25e4`](https://github.com/dralbertoeliasBr/BOLINHA-/commit/ab9b4b25e43cf7deed5f84b99567a3c1aa435cd1) | 2026-09-11T00:18:26Z |
| `prova/PROVA_DE_ANTERIORIDADE.pdf` | 128482 | `39e8d730b8c81819` | [`ab9b4b25e4`](https://github.com/dralbertoeliasBr/BOLINHA-/commit/ab9b4b25e43cf7deed5f84b99567a3c1aa435cd1) | 2026-09-11T00:18:26Z |
| `prova/commits_github_verificados.json` | 6967 | `aedbbb4cd8e6277a` | [`ab9b4b25e4`](https://github.com/dralbertoeliasBr/BOLINHA-/commit/ab9b4b25e43cf7deed5f84b99567a3c1aa435cd1) | 2026-09-11T00:18:26Z |
| `prova/extrai_provas.py` | 8743 | `cefda478098fb245` | [`ab9b4b25e4`](https://github.com/dralbertoeliasBr/BOLINHA-/commit/ab9b4b25e43cf7deed5f84b99567a3c1aa435cd1) | 2026-09-11T00:18:26Z |
| `prova/inventario.json` | 15843 | `e72fb6c3b4835b7a` | [`ab9b4b25e4`](https://github.com/dralbertoeliasBr/BOLINHA-/commit/ab9b4b25e43cf7deed5f84b99567a3c1aa435cd1) | 2026-09-11T00:18:26Z |
| `seguranca/RESULTADOS.md` | 3303 | `2e34d66d7c56fff9` | [`29a061488a`](https://github.com/dralbertoeliasBr/BOLINHA-/commit/29a061488aca3f560af3c4d1207a77d57d93af58) | 2026-09-11T01:11:03Z |
| `seguranca/simulacao_sobrevivencia.py` | 8557 | `faf1ac5f48782d66` | [`29a061488a`](https://github.com/dralbertoeliasBr/BOLINHA-/commit/29a061488aca3f560af3c4d1207a77d57d93af58) | 2026-09-11T01:11:03Z |
| `simbiose/O_DIVERGENTE_E_O_DETERMINISTA.md` | 11743 | `a17a4f169e22d518` | [`65543c255d`](https://github.com/dralbertoeliasBr/BOLINHA-/commit/65543c255de78865ec4abdf857de8ae19258abec) | 2026-09-10T21:55:37Z |
| `simbiose/O_DIVERGENTE_E_O_DETERMINISTA.pdf` | 133147 | `11a010041d0a41b4` | [`a9821e1141`](https://github.com/dralbertoeliasBr/BOLINHA-/commit/a9821e1141dbe9bd6f93b8b4a743021af3390802) | 2026-09-11T01:17:28Z |
| `simbiose/index.html` | 20258 | `57c13fd9d3d82903` | [`65543c255d`](https://github.com/dralbertoeliasBr/BOLINHA-/commit/65543c255de78865ec4abdf857de8ae19258abec) | 2026-09-10T21:55:37Z |

## O que isto prova, e o que não prova

**Prova:** que este conteúdo exato, byte a byte (o hash não mente), existia — público, no GitHub, com histórico visível a qualquer pessoa — no momento em que o servidor do GitHub recebeu o push listado. Isso é mais forte que um arquivo com data local, porque o timestamp não está sob controle de quem publicou.

**Não prova:** propriedade legal, registro de patente ou direito autoral formal. Git é evidência técnica de anterioridade, não um instrumento jurídico. Este projeto já usa o mecanismo formal para isso — DOIs Zenodo, registrados numa entidade terceira e independente — ver `paper/AS_GEMEAS_E_O_NUMERO.md`, seção de Referências, "Registro de anterioridade". Para uma prova ainda mais forte e sem depender de confiar no GitHub, existe [OpenTimestamps](https://opentimestamps.org/) — gratuito, independente, ancorado em blockchain, verificável por qualquer um sem precisar de conta em lugar nenhum.

