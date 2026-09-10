# RESULTADOS — medicoes que sustentam o paper

Gerado por `python3 paper/prova/roda_tudo.py`. Nada aqui foi digitado a mao.

| ambiente | valor |
|---|---|
| Python | 3.11.15 |
| plataforma | Linux-6.18.44-fc-v24-x86_64-with-glibc2.39 |
| sha256 tabelas logisticas | `317f8cfbd08ae2a90832a5fb3ab14a44` |
| sha256 nucleo.py | `221305ad5c99931e107ee1316e75c061` |
| sha256 experimentos.py | `efcc5f714a015076c89fb00d0e3e4fb4` |
| sha256 corpus/estruturado.json | `cbae9c24e7e445096db0d441c3699aa1` |
| sha256 corpus/pt_sounavy.txt | `42c799b15165e8d426d9e594d08cfdce` |
| sha256 corpus/tabular.csv | `d1a4cc9c485df64138329c977d5a9e06` |
| tempo total | 39.0 s |

## E1 — o teto da contagem

Fracao maxima das cadeias de n bits que podem encolher k bits:

| k bits de ganho | fracao maxima das entradas |
|---|---|
| 1 | 0.5 |
| 4 | 0.0625 |
| 8 | 0.00391 |
| 16 | 1.53e-05 |
| 32 | 2.33e-10 |
| 64 | 5.42e-20 |

Teste: 64 buffers de 256 bytes de entropia maxima.

| compressor | tamanho medio (x original) |
|---|---|
| este codec (gemeas, ordem 1-4) | 1.0223 |
| xz -9 | 1.2344 |
| melhor caso observado do codec | 1.0156 |

## E2 — o que as gemeas ja sabem (H(X) -> H(X|M))

Dicionario previo: 6152 bytes. Mensagem: 3076 bytes. Ida-e-volta conferida: frio=True, quente=True.

| esquema | bits/byte | x sobre 8 bits |
|---|---|---|
| cru (UTF-8) | 8.000 | 1.00x |
| gzip -9 | 4.234 | 1.89x |
| bzip2 -9 | 4.349 | 1.84x |
| xz -9 | 4.536 | 1.76x |
| zlib com dicionario (32 KB) | 3.550 | 2.25x |
| ESTE codec, sem dicionario | 3.836 | 2.09x |
| ESTE codec, com dicionario | 3.066 | 2.61x |

Ganho do dicionario previo sobre o mesmo codec sem ele: **20.07%**.

SHA-256 da mensagem: `eb092b8fda4b51185628455a0f3279fc`

## E3 — ordens de leitura (frente, tras, vertical)

### prosa — 9228 bytes, passo vertical detectado sozinho: 45 (igualdade 6.59%)

| leitura | bits/byte |
|---|---|
| frente, ordens 1-4 | 3.487 |
| frente, ordens 1-8 (controle: mais modelos) | 3.469 |
| so vertical (2 alturas) | 5.206 |
| frente 1-4 + vertical 2 | 3.567 |
| de tras para frente, ordens 1-4 | 3.566 |

- ganho da camada vertical **contra o controle de mesmo tamanho**: -2.81%
- assimetria frente/tras: 2.25% (positivo = ler de tras custa mais)

### tabular — 14037 bytes, passo vertical detectado sozinho: 105 (igualdade 68.51%)

| leitura | bits/byte |
|---|---|
| frente, ordens 1-4 | 1.137 |
| frente, ordens 1-8 (controle: mais modelos) | 1.125 |
| so vertical (2 alturas) | 0.881 |
| frente 1-4 + vertical 2 | 0.700 |
| de tras para frente, ordens 1-4 | 1.225 |

- ganho da camada vertical **contra o controle de mesmo tamanho**: 37.71%
- assimetria frente/tras: 7.77% (positivo = ler de tras custa mais)

## E3b — retro-leitura legal: ler o futuro de uma camada ja inteira

| camada | bits/byte |
|---|---|
| ALTA (nibble alto), viaja primeiro | 1.956 |
| BAIXA olhando so o passado | 2.262 |
| BAIXA olhando ALTA[i+1], ALTA[i+2] (o futuro) | 2.110 |
| **total, so passado** | **4.218** |
| **total, com futuro** | **4.066** |

Ganho da camada baixa ao poder ler o futuro da camada alta: **6.72%**.

## E4 — base fatorial, primos, posicao

### Lehmer / base fatorial: permutacao -> UM numero

| n | bits do indice | otimo log2(n!) | ingenuo n*log2(n) | economia |
|---|---|---|---|---|
| 8 | 15 | 15.3 | 24 | 36.25% |
| 12 | 28 | 28.8 | 48 | 39.93% |
| 52 | 225 | 225.6 | 312 | 27.70% |
| 100 | 524 | 524.8 | 700 | 25.03% |

### Numeracao de Godel (produto de primos): bijetiva e catastrofica

| bytes | bits do numero | bits crus | fator |
|---|---|---|---|
| 4 | 217 | 32 | **6.8x** |
| 8 | 3164 | 64 | **49.4x** |
| 16 | 8637 | 128 | **67.5x** |
| 32 | 20322 | 256 | **79.4x** |

### Primos como IDENTIDADE (nao como compressao)

| primos | bits da impressao | colisao maxima |
|---|---|---|
| 4 | 8 | 0.00476 |
| 8 | 24 | 1.03e-07 |
| 16 | 65 | 3.07e-20 |

## E5 — o numero unico existe (e ja tem nome)

Frase: "A voz como sistema operacional. Menos dado, dado certo. Nao e eu, e nos."

| forma | bits |
|---|---|
| UTF-8 cru | 576 |
| um numero, gemeas sem dicionario | 472 |
| um numero, gemeas com dicionario | 166 |

O numero (com dicionario, 50 digitos decimais):

```
78389650460584687750591719165629250130512777198585
```

Ida-e-volta conferida byte a byte: **True**. SHA-256 `ac7af243eeb9fdfd8365e8c9ebfbbb54`

## E6 — trocar tempo por bits: quando compensa

Criterio, sem numero magico:

```
comprimir compensa  <=>  e_calc / N  <  (1 - r) * e_rede
```

`e_calc` = potencia / vazao (J por byte processado) · `r` = 0.383 (razao medida deste codec) · `e_rede` = J por byte no enlace · `N` = quantas vezes o mesmo objeto sera enviado ou lido.

Medido: 3076 bytes em 0.49 s = 6227 B/s (Python puro, um nucleo). xz -9: 1744 bytes; este codec: 1179 bytes.

| motor | e_calc (J/byte) | enlace | limiar (1-r)*e_rede | compensa em 1 envio? | envios p/ empatar |
|---|---|---|---|---|---|
| este codec, Python puro (MEDIDO) | 0.000803 | fibra / datacenter | 1.23e-08 | nao | 65,097 |
| este codec, Python puro (MEDIDO) | 0.000803 | 4G movel | 1.23e-06 | nao | 651 |
| este codec, Python puro (MEDIDO) | 0.000803 | satelite / LoRa | 0.000123 | nao | 7 |
| este codec, Python puro (MEDIDO) | 0.000803 | espaco profundo | 0.0123 | SIM | 1 |
| mesmo codec em C, estimado 10 MB/s | 5e-07 | fibra / datacenter | 1.23e-08 | nao | 41 |
| mesmo codec em C, estimado 10 MB/s | 5e-07 | 4G movel | 1.23e-06 | SIM | 1 |
| mesmo codec em C, estimado 10 MB/s | 5e-07 | satelite / LoRa | 0.000123 | SIM | 1 |
| mesmo codec em C, estimado 10 MB/s | 5e-07 | espaco profundo | 0.0123 | SIM | 1 |
| LLM gemea no iPhone: 14,1 tok/s medidos x 4 B/token | 0.0355 | fibra / datacenter | 1.23e-08 | nao | 2,875,014 |
| LLM gemea no iPhone: 14,1 tok/s medidos x 4 B/token | 0.0355 | 4G movel | 1.23e-06 | nao | 28,750 |
| LLM gemea no iPhone: 14,1 tok/s medidos x 4 B/token | 0.0355 | satelite / LoRa | 0.000123 | nao | 288 |
| LLM gemea no iPhone: 14,1 tok/s medidos x 4 B/token | 0.0355 | espaco profundo | 0.0123 | nao | 3 |
| LLM gemea em GPU: 2000 tok/s x 4 B/token | 0.05 | fibra / datacenter | 1.23e-08 | nao | 4,053,769 |
| LLM gemea em GPU: 2000 tok/s x 4 B/token | 0.05 | 4G movel | 1.23e-06 | nao | 40,538 |
| LLM gemea em GPU: 2000 tok/s x 4 B/token | 0.05 | satelite / LoRa | 0.000123 | nao | 405 |
| LLM gemea em GPU: 2000 tok/s x 4 B/token | 0.05 | espaco profundo | 0.0123 | nao | 4 |

Valores de `e_rede` sao SUPOSICOES declaradas, nao medicoes: fibra/datacenter 2e-8, 4G 2e-6, satelite/LoRa 2e-4, espaco profundo 2e-2 J/byte. Trocar o numero troca a conclusao — a conta fica aberta de proposito.

## E7 — determinismo: por que o caminho critico e inteiro

| teste | resultado |
|---|---|
| somar 2000 floats em duas ordens da o mesmo? | **False** (delta 1.94e-07) |
| o caminho inteiro deste codec repete bit a bit? | **True** |
| sha256 das tabelas (contrato das gemeas) | `317f8cfbd08ae2a90832a5fb3ab14a44` |

### Falha localizada: UM contador divergente (de 1500 bytes decodificados)

| erro no contador (de 4096) | contadores testados | quebraram | taxa |
|---|---|---|---|
| +1 | 60 | 0 | 0.00% |
| +16 | 60 | 4 | 6.67% |
| +256 | 60 | 4 | 6.67% |
| +2048 | 60 | 4 | 6.67% |

### Falha sistemica: deriva de configuracao entre as gemeas

| deriva | bytes certos | primeiro erro no byte |
|---|---|---|
| ordens (1,2,3,5) em vez de (1,2,3,4) | 5.67% | 67 |
| dicionario previo com 1 byte a menos | 4.13% | 0 |

## E7b — quanta folga numerica as gemeas tem? (a resposta e: nenhuma)

A gemea receptora calcula cada probabilidade com erro de ate +-D (numa escala de 4096), em TODA decisao. 1200 bytes.

| folga D | erro relativo | quebrou | primeiro erro (byte) | bytes certos |
|---|---|---|---|---|
| +-0 | 0.0000% | 0 de 1 | nenhum | 100.00% |
| +-1 | 0.0244% | 12 de 12 | 1.1 | 0.27% |
| +-2 | 0.0488% | 12 de 12 | 1.0 | 0.31% |
| +-4 | 0.0977% | 12 de 12 | 0.8 | 0.29% |
| +-8 | 0.1953% | 12 de 12 | 0.8 | 0.24% |
| +-16 | 0.3906% | 12 de 12 | 0.7 | 0.36% |
| +-64 | 1.5625% | 12 de 12 | 0.3 | 0.21% |
| +-256 | 6.2500% | 12 de 12 | 0.1 | 0.29% |

## E8 — a busca pela semente curta ("um numero que gera tudo")

| bits do alvo | tentativas medias | 2^k | bits medios da semente | bits economizados | segundos |
|---|---|---|---|---|---|
| 8 | 280 | 256 | 7.75 | **+0.25** | 0.0002 |
| 12 | 3,545 | 4,096 | 11.42 | **+0.58** | 0.0026 |
| 16 | 33,237 | 65,536 | 15.08 | **+0.92** | 0.0236 |
| 20 | 751,504 | 1,048,576 | 19.33 | **+0.67** | 0.5433 |

Tentativas crescem como 2^k. A economia de bits fica **constante** em torno de 0,7 bit. Tempo exponencial, bits de graca: zero.

