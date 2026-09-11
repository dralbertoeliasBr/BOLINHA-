# As Gêmeas e o Número — Resumo Executivo

**Antônio Alberto Lopes Elias** · ORCID [0000-0002-5602-9916](https://orcid.org/0000-0002-5602-9916) · Sounavy — GaIA / Opera Vox
Trabalho independente, sem afiliação institucional. Setembro de 2026.

Versão condensada de *As Gêmeas e o Número: Compressão por Inteligência Compartilhada* (paper completo, 37 asserções testadas, código e hashes em anexo/repositório). Este documento existe para leitura em cinco minutos, não para substituir o original.

---

## Uma frase

Duas partes que compartilham um modelo probabilístico só precisam trocar H(X|M) bits, não H(X). O restante é engenharia: fazer duas instâncias de modelo concordarem, bit a bit, apesar de rodar em hardware, versões e — no caso de LLMs — inferências não-idênticas.

Este trabalho (a) reproduz esse resultado com um codificador aritmético inteiro, sem LLM, para isolar o mecanismo; (b) mede empiricamente a fragilidade de sincronização entre "gêmeas" e confirma, por caminho independente, o achado central de Adler & Tang (ICLR 2026); (c) registra três extensões pequenas e verificáveis — não uma arquitetura nova, três peças de engenharia com número ao lado.

## Resultados que sustentam o resto

| # | achado | medida |
|---|---|---|
| 1 | Dicionário prévio compartilhado reduz o canal | 20,07% menos bits, mesmo codec, mesmo texto |
| 2 | O fluxo comprimido é, literalmente, um único inteiro | 576 bits → 166 bits (frase de 72 caracteres) |
| 3 | Camada de contexto opcional, portão sem custo de sinalização | prejuízo de −2,81% → 0% (decisão deduzida do bloco anterior) |
| 4 | Redundância proporcional à importância (RRNS aplicado ao stream) | 0 → 31 bits compram detecção → correção de até 2 erros |
| 5 | **Tolerância numérica entre gêmeas: nenhuma** | erro de ±1/4096 em toda decisão → 100% de falha no primeiro byte |
| 6 | Falha pontual (1 contador, 1 bit) é majoritariamente silenciosa | sobrevive em 93% dos casos, destrói em 7% — sem aviso |

Cada linha corresponde a uma função Python que roda sozinha, sem dependência, em ~40s no total (`paper/prova/roda_tudo.py`). O cabeçalho do relatório gerado traz o SHA-256 de cada arquivo de código e de corpus usado — qualquer divergência entre o que está aqui e o que roda localmente é erro do documento, não de quem reproduziu.

## O achado 5 e sua relação com trabalho publicado

O item 5 é o resultado que temos mais confiança em recomendar a esta leitora especificamente. Ele foi obtido de forma independente — implementação própria, sem LLM, modelo de mistura de contexto em aritmética inteira — e converge com o resultado central de:

> Adler, A.; Tang, J. *Synchronizing Probabilities in Model-Driven Lossless Compression.* ICLR 2026. arXiv:2601.10678.

que demonstra, com LLaMA 3.1 em hardware real (M2 Pro → M4 Max), que codificação aritmética padrão falha *totalmente* sob divergência de hardware, e que PMATIC (tolerância explícita a mismatch, custando ~3× em bits) resolve o problema.

Também citamos, por estar em diálogo técnico direto com o mesmo espaço de problema:

> Rinberg, R.; Carrell, A. M.; Henniger, S.; Carlini, N.; Warr, K. *Haiku to Opus in Just 10 bits: LLMs Unlock Large Compression Gains.* arXiv:2604.02343, 2026. (Harvard, Cambridge, Anthropic.)

Este último demonstra ganhos de 2× via adaptação de domínio (LoRA) sobre codificação aritmética com LLM, e um protocolo interativo de perguntas binárias que recupera 7–72% da diferença de capacidade entre modelos com apenas 10 bits transmitidos. Não reproduzimos esses números — citamos porque situam este trabalho dentro de uma linha de pesquisa ativa, não fora dela.

## O que é rigor aqui, e o que é conjectura

Onze das 37 asserções do paper completo foram refutadas pela própria medição e permanecem publicadas como tal — vetor de primos como compressão (expande 79,4×), busca de semente curta (custo 2^k para <1 bit de ganho), paridade de posição como sinal (0,000 bit líquido sob controle de embaralhamento), entre outras. Nenhuma foi removida após cair; cada uma tem a medição e a data que a derrubou.

Isto não é uma pretensão de completude acadêmica. É a razão prática pela qual os seis resultados acima merecem cinco minutos: o mesmo processo que os produziu já demonstrou, dentro do próprio corpo de trabalho, que sabe reconhecer e publicar o que não funciona.

## Reproduzir

```bash
git clone https://github.com/dralbertoeliasBr/BOLINHA-.git
cd BOLINHA- && git checkout claude/llm-gemeas-compressao-lwnpwn
python3 paper/prova/roda_tudo.py
```

Python 3.8+, zero dependências externas. Roda em desktop ou, deliberadamente, em Pythonista/a-Shell num iPhone — a restrição de ambiente é parte do projeto, não uma limitação a esconder.

## O que este documento não é

Não é proposta de investimento. Não há modelo de negócio anexo, nem pretensão de startup. É a solicitação mais simples possível: que os seis resultados acima, e em particular o item 5, sejam avaliados por quem já trabalha na fronteira exata deste problema — porque uma confirmação independente, mesmo pequena, tem valor para quem projeta sistemas que dependem de duas inferências concordarem.

---

**Contato e citação completa:** paper integral, código, e os demais documentos desta linha de trabalho (método, prova de colaboração, origem) em `github.com/dralbertoeliasBr/BOLINHA-`, branch `claude/llm-gemeas-compressao-lwnpwn`, pasta `obra/`.

> Elias, A. A. L. (2026). *As Gêmeas e o Número: Compressão por Inteligência Compartilhada.* Sounavy — GaIA / Opera Vox. ORCID 0000-0002-5602-9916.
