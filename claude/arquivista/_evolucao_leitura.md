# Arquivista — evolução e leitura

## Origem
02/11/2026, conversa do site sounavy.com. Sounavy mandou as versões do Arquivista que tinha no iPhone e pediu para ordenar pelo tempo, a mais nova em cima. Objetivo do Arquivista: pegar o que entra, carimbar (selo), não duplicar e guardar na caixa certa, sem nunca apagar.

## Linha de evolução (mais nova em cima)
Data só onde o próprio arquivo tem data. As outras estão na ordem que o código mostra: uma versão corrige o que a anterior fingia.

| # | Arquivo | Data | O que trouxe | Estado |
|---|---|---|---|---|
| 9 | `codigos/ARQUIVISTA_LISTA_RECENTES_v2.py` | 02/11/2026 | Lista tudo que as versões gravaram, mais novo em cima; só lê | testada |
| 8 | bancada `gaia-ip-teste.html` (Inox + Arquivista) | 02/11/2026 | Inox na porta, cadeia SHA-256, Black 2/3, nome-informação | testada 15/15 |
| 7 | `codigos/GaIA_all_in_2026-11-01.py` | 01/11/2026 | Arquivista 2/3: quaisquer 2 de 3 pedaços reconstroem | testada |
| 6c | `a8_prova_de_conceito_2026-07-21.py` | 21/07/2026 12:26–12:27 (3 PROVA no iPhone) | Roda os 5 agentes sozinho e grava PROVA_*.json com hash do log, para filmar | testada |
| 6b | `a7_casca_leve_2026-07-21.py` | 21/07/2026 12:08 (GAIA_BOX4_teste no iPhone) | 5 agentes num motor com tempo: Arquivista com nome semântico, Faxina sem apagar, Tradutor regional, Vigia, Contador | testada com motor substituto |
| 6 | `a6_core_v1_real_hmac.py` | 06/07/2026 01:09 (1º uso no manifesto do iPhone) | HMAC real, nome = data + hash, índice, manifesto, verificar e recuperar | testada; chave padrão é pública |
| 5 | `a5_ssrd_v1.2_enclave_TEXTO-DO-DOCX.txt` | sem data | Stop/Go por hash, níveis L1–L4, zlib, Fernet na Violeta L4 | não rodou: o .docx perdeu a indentação |
| 4 | `a4_recuperacao_sem_exclusao.py` | sem data | Promessa explícita de nunca apagar; Stop/Go | testada |
| 3 | `a3_prisma_v1.0_7dourados_1preto.py` | sem data | 7 caixas + Box 00 Preto | testada; "sig" é só a palavra ARQUITETO |
| 2 | `a2_V11_2026-08-07_fila_lote.py` | 07/08/2026 16:40 | Vocabulário nativo, fila de lote (uma chamada de API só), auditoria de "confirmados" | testada |
| 0 | `a0_doca_bridge_mvp.py` | sem data | Ponte Pythonista ↔ Enclave (Qwen/Toca); fila append-only em `projeto_gaia_vault.jsonl` | testada; sincronizar não faz nada |
| 1 | `a1_camadas_3_lexico_llm_nuvem.py` | antes de 07/08 | Escada léxico → LLM local → nuvem | testada; camada 2 é simulada |
| — | Maestria (`MAESTRIA_AGENT_CORE_18jun2026.docx`) | 18/06/2026 | Orquestra os 7 boxes, rastro JSON | não incluída aqui (outro documento) |
| — | Memorial 7 Box v1.2 | 09/04/2026 | Prefixo 7 + caixa + data invertida | referência |

Nota: as versões 1 e 2 são o "cérebro" que decide (Delta). As versões 3 a 6 são o Arquivista que guarda. As duas linhas se juntam no all-in (7).

## Uso real no iPhone (lista v2 rodada por Sounavy em 02/11/2026 21:24)
107 arquivos em mais de 70 pastas. Do mais novo ao mais antigo:
- 02/11 03:10 · `SRD Gaia gêmini/resultado_execucao.txt`
- 01/11 21:08 · `arquivo_gaia/` aqui + nuvem · teste 2/3 do all-in (v1 e v2 de funcoes_vitais)
- 07/08 19:05 · `GAIA_UTILS/vigia_bilateral.jsonl`
- 25/07 19:08 · `GAIA_UTILS/vault.jsonl` e `violet_box.txt` (DOCA_1)
- 21/07 15:31 · `ENCLAVE_DOCA/BOX_04` · PROCESSADO_ARMAZENADO
- 21/07 12:08–12:27 · `GAIA_UTILS` · 3 PROVA + testes da Box 4
- 21/07 00:50–01:28 · `GAIA_ARQUIVOS` · 12 registros na Box 1
- 06/07 01:09 · `ARQUIVISTA_CORE` · Core v1 (GO + STOP)
Achado: existe uma DOCA com 14 caixas (08 Impressão Claude, 09 Relação, 10 Definitivo, 11 Histórico, 12 Índice, 13 Essência, 14 Livro). Saída completa em `saida_iphone_2026-11-02_2124.txt`.

## Como funciona (Core v1, a mais madura das antigas)
1. Recebe um texto e calcula o SHA-256 completo.
2. Se o hash já está no índice: STOP, não grava de novo.
3. Assina com HMAC-SHA256 usando a chave.
4. Se a biblioteca `cryptography` existe, cifra (Fernet); se não, grava aberto e marca `encrypted=False`, sem fingir.
5. Nome do arquivo: data + 12 letras do hash. O nome não carrega o texto.
6. Anota a operação no `_manifesto.log`.
7. `verificar` recalcula hash e assinatura; qualquer mudança aparece.

O que nenhuma versão faz: não apaga arquivo, não manda nada para a internet (exceto o Enclave SSRD + Llama, que fala com o Llama no próprio aparelho, em 127.0.0.1).

## Particularidades
- Casca Leve: o nome é semântico (primeira palavra do texto). É a primeira versão do "nome já é informação", mas vaza o texto: "Contrato secreto…" vira `GAIA_BOX4_contrato_…`. Depende de `MOTOR_TIMER.py`, que não veio; testei com um substituto que só chama as funções.
- Prova de Conceito: o hash vai dentro do próprio arquivo; para conferir, tira-se o campo `hash_integridade` e recalcula.
- Doca Bridge: grava cada envio numa fila que só cresce (bom: nunca apaga). Mas não tem selo, deixa o mesmo dado entrar duas vezes, e `sincronizar` só imprime "próxima semana" e devolve "pronto". Status "pendente" nunca muda.
- O nome do arquivo vaza o texto em duas versões: SSRD v1.2 (15 letras), Recuperação (10 letras). Core e bancada corrigem isso.
- Prisma: a "assinatura" é fixa, não prova nada.
- Core: sem chave própria, a chave é o DNA, que está no código. Cifra de verdade só com chave sua.
- Recuperação: o Stop/Go só lembra o último texto e esquece ao fechar.
- Pastas diferentes por versão: ARQUIVISTA_CORE, Arquivos_Gaia, Arquivos_Gaia_Soberana, DOCA_PRISMA, SSRD, MAESTRO. A lista v2 procura em todas.

## Testes (rodados em 02/11/2026, em pasta isolada)
- Recuperação: grava e bloqueia a repetição.
- Prisma: grava no BOX_00_PRETO em texto aberto.
- Camadas 3: 3 frases no léxico, 2 na LLM (simulada), 1 na nuvem.
- V11: "O crime combate o amor" saiu CONFIRMADO Positiva e foi para auditoria — a própria v11 previa esse erro.
- Core v1: grava, deduplica, verifica e recupera.
- Lista v2: achou as cinco pastas/arquivos, mais novo em cima.

## Pendências
- SSRD v1.2: preciso do .py original (o .docx não guarda espaços).
- Datas reais das versões 3 a 5: o Core v1 já tem (06/07); faltam Prisma, Recuperação e SSRD.
- A DOCA de 14 caixas: achar o código que criou.
- Escolher uma pasta só para o Arquivista daqui em diante.
