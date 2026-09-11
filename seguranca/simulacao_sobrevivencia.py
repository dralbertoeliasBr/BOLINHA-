# -*- coding: utf-8 -*-
"""
simulacao_sobrevivencia.py — resposta à pergunta feita por voz: "qual a
chance de uma IA na borda sobreviver a ataques futuros, contra a chance de
quem guarda tudo na borda sem usar IA?"

O que este script NÃO faz: não inventa uma porcentagem única e a apresenta
como fato ("87% de chance"). Isso violaria a regra 1 deste projeto — nenhum
número entra sem código que roda — na sua forma mais perigosa: um número
que roda mas mede a suposição, não a realidade, e se disfarça de medida.

O que ele FAZ: constrói um modelo Monte Carlo explícito, com toda suposição
nomeada como parâmetro, e mostra como a resposta MUDA quando a suposição
muda. Ninguém precisa acreditar num número — pode trocar `VANTAGEM_IA` ou
`ATAQUES_POR_ANO` e rodar de novo. A "chance" não é uma constante da
natureza; é uma função de quanto se assume que a automação ajuda.

A métrica é **tempo mediano até o primeiro comprometimento**, não
"probabilidade de sobreviver N anos" — de propósito. "Sobreviver todo
ataque de todo ano" é um produto de probabilidades independentes: com
qualquer defesa imperfeita, ao longo de dezenas de tentativas esse produto
desaba pra perto de zero pros dois lados (é a mesma verdade de segurança
real: quem defende precisa acertar sempre, quem ataca só precisa acertar
uma vez). Isso é matematicamente correto, mas esconde a diferença que
importa atrás de dois zeros. Tempo mediano até a primeira falha é a mesma
matemática, numa escala que se lê.

O modelo, em uma frase: por ano, chegam N ataques (Poisson). Cada ataque é
detectado com probabilidade p_deteccao; se não for detectado, ele causa
dano com probabilidade proporcional à janela de exposição até alguém (ou
algo) perceber e reagir. A "vantagem de IA" multiplica a probabilidade de
detecção e divide a janela de exposição — os dois jeitos concretos que
monitoramento automatizado supera atenção humana: vê mais tentativas, e
reage mais rápido às que passam.

Isto não mede o Sounavy, a Bolinha ou nenhum sistema real. É um modelo de
brinquedo, honesto sobre ser um modelo de brinquedo, cujo único compromisso
é matemático: dadas as suposições X, a matemática diz Y — e Y roda, aqui,
de novo, sempre igual, com a mesma semente.

Uso:
    python3 seguranca/simulacao_sobrevivencia.py
"""
import math
import random
import sys

SEMENTE = 33              # reprodutível: mesma semente, mesmo resultado
EXECUCOES = 20000         # trajetórias Monte Carlo por célula da tabela
ANOS_TETO = 200           # se ninguém foi comprometido até aqui, reporta "> teto"
P_DETECCAO_BASE = 0.80    # chance de perceber UM ataque, sem ajuda nenhuma
JANELA_EXPOSICAO_BASE = 12    # horas até perceber+reagir, sem ajuda (suposição nomeada)
JANELA_REFERENCIA = 24        # horas de exposição que já bastam p/ dano bem provável


def poisson(rnd, lam):
    """Amostra de Poisson sem numpy (algoritmo de Knuth) — pura stdlib."""
    L = math.exp(-lam)
    k, p = 0, 1.0
    while True:
        k += 1
        p *= rnd.random()
        if p <= L:
            return k - 1


def sobrevive_um_ataque(rnd, vantagem):
    p_detecta = min(0.995, P_DETECCAO_BASE * vantagem)
    if rnd.random() < p_detecta:
        return True  # percebido a tempo, bloqueado
    exposicao = JANELA_EXPOSICAO_BASE / vantagem
    p_dano = min(0.9, exposicao / JANELA_REFERENCIA)
    return rnd.random() >= p_dano


def anos_ate_comprometimento(rnd, ataques_por_ano, vantagem, anos_teto):
    for ano in range(1, anos_teto + 1):
        for _ in range(poisson(rnd, ataques_por_ano)):
            if not sobrevive_um_ataque(rnd, vantagem):
                return ano
    return None  # sobreviveu ao teto inteiro, nesta trajetória


def tempo_mediano(ataques_por_ano, vantagem, execucoes=EXECUCOES, semente=SEMENTE, anos_teto=ANOS_TETO):
    rnd = random.Random(semente)
    amostras = sorted(
        (anos_ate_comprometimento(rnd, ataques_por_ano, vantagem, anos_teto) or (anos_teto + 1))
        for _ in range(execucoes)
    )
    mediana = amostras[len(amostras) // 2]
    return anos_teto if mediana > anos_teto else mediana


def fmt_anos(v):
    if v >= ANOS_TETO:
        return '> %d anos' % ANOS_TETO
    return '%d ano' % v if v == 1 else '%d anos' % v


def main():
    L = []
    w = L.append
    w('# Simulação de sobrevivência — borda com IA contra borda sem IA\n')
    w('Modelo hipotético, não medida de sistema real. Toda suposição nomeada '
      'em `simulacao_sobrevivencia.py`; troque um parâmetro e rode de novo — '
      'o número muda, e é para mudar. Semente fixa (%d), %d execuções por '
      'célula. Métrica: **tempo mediano até o primeiro comprometimento**, '
      'em anos (teto de relato em %d).\n' % (SEMENTE, EXECUCOES, ANOS_TETO))

    w('## Tabela 1 — mesma intensidade de ataque, vantagem de IA variando\n')
    w('Ambiente fixo em **20 tentativas de ataque/ano** (ordem de grandeza de '
      'um dispositivo de borda exposto, não um alvo de alto valor). A linha '
      '`vantagem=1×` é a própria definição de "sem IA" — não é um número '
      'medido à parte, é o ponto de partida com o qual tudo mais se compara.\n')
    w('| vantagem da IA (detecção × e resposta ÷) | tempo mediano até comprometer | razão sobre vantagem=1× |')
    w('|---|---|---|')
    base = tempo_mediano(20, 1.0)
    for vant in (1, 2, 3, 5, 10, 20):
        t = tempo_mediano(20, float(vant))
        razao = t / base if base > 0 else float('inf')
        w('| %sx | %s | %.2f× |' % (vant, fmt_anos(t), razao))
    w('')
    w('**Leitura, sem inflar:** em `vantagem=1×` a razão é 1,00× por '
      'definição — a tabela concorda consigo mesma, como tem que concordar. '
      'A partir daí o ganho não é linear: dobrar detecção-e-resposta mais '
      'que dobra o tempo mediano, porque os dois efeitos (menos ataques '
      'passam, e os que passam causam menos dano) se multiplicam, não somam.\n')

    w('## Tabela 2 — vantagem fixa, intensidade de ataque variando\n')
    w('`vantagem=5×` fixo (suposição explícita, não uma medida — troque e '
      'rode de novo). O que varia é o volume de tentativas por ano, de um '
      'ambiente calmo a um sob ataque ativo constante.\n')
    w('| tentativas/ano | tempo mediano, sem IA | tempo mediano, com IA (5×) | razão |')
    w('|---|---|---|---|')
    for ataques in (5, 20, 50, 100, 300):
        sem_ia = tempo_mediano(ataques, 1.0)
        com_ia = tempo_mediano(ataques, 5.0)
        razao = com_ia / sem_ia if sem_ia > 0 else float('inf')
        w('| %d | %s | %s | %.2f× |' % (
            ataques, fmt_anos(sem_ia), fmt_anos(com_ia), razao))
    w('')
    w('**Leitura, sem inflar — e o modelo discorda da intuição fácil aqui, o '
      'que é o motivo de rodar em vez de chutar:** em termos absolutos, IA '
      'sempre vale mais tempo até comprometer, em qualquer volume testado. '
      'Mas a **razão** encolhe conforme o volume sobe, não cresce. Faz '
      'sentido matematicamente: a mesma vantagem multiplicativa (5×) reduz '
      'proporcionalmente menos o tempo mediano quando o tempo mediano já é '
      'pequeno — sob ataque intenso o suficiente, mesmo um defensor 5× '
      'melhor acaba encontrado. O modelo não está "provando" que IA vence '
      'sempre na mesma proporção — está mostrando que a vantagem relativa é '
      '**maior onde o ataque é raro**, e some perto do limite onde ninguém, '
      'com ou sem IA, sobrevive por muito tempo.\n')

    w('## O que isto não é\n')
    w('Não é uma previsão sobre o Sounavy, a Bolinha ou qualquer celular '
      'específico. Não é uma alegação de que a vantagem real é 2×, 5× ou '
      '20× — esses são os pontos escolhidos para a tabela, não uma medida. '
      'É uma resposta séria a uma pergunta hipotética: **dado que automação '
      'detecta mais e reage mais rápido, o que a aritmética faz com isso ao '
      'longo do tempo, contra um volume de ataque que também sobe?** A '
      'aritmética faz o que as duas tabelas mostram. Se a vantagem real, num '
      'dispositivo de verdade, é 2× ou 20× — isso é uma pergunta empírica, '
      'não uma que este script responde.\n')

    saida = '\n'.join(L) + '\n'
    with open('seguranca/RESULTADOS.md', 'w', encoding='utf-8') as f:
        f.write(saida)
    sys.stderr.write('Escrito: seguranca/RESULTADOS.md\n')
    sys.stderr.write(saida)


if __name__ == '__main__':
    main()
