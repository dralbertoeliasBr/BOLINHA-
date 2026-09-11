# Simulação de sobrevivência — borda com IA contra borda sem IA

Modelo hipotético, não medida de sistema real. Toda suposição nomeada em `simulacao_sobrevivencia.py`; troque um parâmetro e rode de novo — o número muda, e é para mudar. Semente fixa (33), 20000 execuções por célula. Métrica: **tempo mediano até o primeiro comprometimento**, em anos (teto de relato em 200).

## Tabela 1 — mesma intensidade de ataque, vantagem de IA variando

Ambiente fixo em **20 tentativas de ataque/ano** (ordem de grandeza de um dispositivo de borda exposto, não um alvo de alto valor). A linha `vantagem=1×` é a própria definição de "sem IA" — não é um número medido à parte, é o ponto de partida com o qual tudo mais se compara.

| vantagem da IA (detecção × e resposta ÷) | tempo mediano até comprometer | razão sobre vantagem=1× |
|---|---|---|
| 1x | 1 ano | 1.00× |
| 2x | 28 anos | 28.00× |
| 3x | 42 anos | 42.00× |
| 5x | 70 anos | 70.00× |
| 10x | 138 anos | 138.00× |
| 20x | > 200 anos | 200.00× |

**Leitura, sem inflar:** em `vantagem=1×` a razão é 1,00× por definição — a tabela concorda consigo mesma, como tem que concordar. A partir daí o ganho não é linear: dobrar detecção-e-resposta mais que dobra o tempo mediano, porque os dois efeitos (menos ataques passam, e os que passam causam menos dano) se multiplicam, não somam.

## Tabela 2 — vantagem fixa, intensidade de ataque variando

`vantagem=5×` fixo (suposição explícita, não uma medida — troque e rode de novo). O que varia é o volume de tentativas por ano, de um ambiente calmo a um sob ataque ativo constante.

| tentativas/ano | tempo mediano, sem IA | tempo mediano, com IA (5×) | razão |
|---|---|---|---|
| 5 | 2 anos | > 200 anos | 100.00× |
| 20 | 1 ano | 70 anos | 70.00× |
| 50 | 1 ano | 28 anos | 28.00× |
| 100 | 1 ano | 14 anos | 14.00× |
| 300 | 1 ano | 5 anos | 5.00× |

**Leitura, sem inflar — e o modelo discorda da intuição fácil aqui, o que é o motivo de rodar em vez de chutar:** em termos absolutos, IA sempre vale mais tempo até comprometer, em qualquer volume testado. Mas a **razão** encolhe conforme o volume sobe, não cresce. Faz sentido matematicamente: a mesma vantagem multiplicativa (5×) reduz proporcionalmente menos o tempo mediano quando o tempo mediano já é pequeno — sob ataque intenso o suficiente, mesmo um defensor 5× melhor acaba encontrado. O modelo não está "provando" que IA vence sempre na mesma proporção — está mostrando que a vantagem relativa é **maior onde o ataque é raro**, e some perto do limite onde ninguém, com ou sem IA, sobrevive por muito tempo.

## O que isto não é

Não é uma previsão sobre o Sounavy, a Bolinha ou qualquer celular específico. Não é uma alegação de que a vantagem real é 2×, 5× ou 20× — esses são os pontos escolhidos para a tabela, não uma medida. É uma resposta séria a uma pergunta hipotética: **dado que automação detecta mais e reage mais rápido, o que a aritmética faz com isso ao longo do tempo, contra um volume de ataque que também sobe?** A aritmética faz o que as duas tabelas mostram. Se a vantagem real, num dispositivo de verdade, é 2× ou 20× — isso é uma pergunta empírica, não uma que este script responde.

