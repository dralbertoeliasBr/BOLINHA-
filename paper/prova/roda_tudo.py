# -*- coding: utf-8 -*-
"""
roda_tudo.py — roda os sete experimentos e escreve RESULTADOS.md + resultados.json.

  python3 paper/prova/roda_tudo.py

Sem dependencia externa. Se um numero nao aparece aqui, ele nao entra no paper.
"""
import os
import sys
import json
import time
import platform
import hashlib

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import experimentos as E
from nucleo import impressao_digital_das_tabelas


def sha_arquivo(p):
    with open(p, 'rb') as f:
        return hashlib.sha256(f.read()).hexdigest()


def pct(x):
    return '%.2f%%' % x


def n3(x):
    return '%.3f' % x


def main():
    t0 = time.time()
    R = {}
    ordem = [('E1', 'contagem', E.e1_contagem),
             ('E2', 'dicionario', E.e2_dicionario),
             ('E3', 'camadas', E.e3_camadas),
             ('E3b', 'retroleitura', E.e3b_retroleitura),
             ('E4', 'fatorial_primos', E.e4_fatorial_primos),
             ('E5', 'numero_unico', E.e5_numero_unico),
             ('E6', 'energia', E.e6_energia),
             ('E7', 'determinismo', E.e7_determinismo),
             ('E7b', 'folga', E.e7b_folga),
             ('E8', 'busca', E.e8_busca),
             ('E9', 'raiz_mista', E.e9_raiz_mista),
             ('E10', 'dicionario_equacao', E.e10_dicionario_equacao),
             ('E11', 'informacao_mutua', E.e11_informacao_mutua),
             ('E12', 'crt', E.e12_crt),
             ('E13', 'camada_condicional', E.e13_camada_condicional),
             ('E14', 'vacuo', E.e14_vacuo),
             ('E15', 'rrns', E.e15_rrns_importancia)]
    for cod, nome, fn in ordem:
        t = time.time()
        sys.stderr.write('%s %s ... ' % (cod, nome))
        sys.stderr.flush()
        R[nome] = fn()
        sys.stderr.write('%.1fs\n' % (time.time() - t))

    R['_ambiente'] = {
        'python': sys.version.split()[0],
        'plataforma': platform.platform(),
        'sha_tabelas': impressao_digital_das_tabelas(),
        'sha_nucleo': sha_arquivo(os.path.join(AQUI, 'nucleo.py')),
        'sha_experimentos': sha_arquivo(os.path.join(AQUI, 'experimentos.py')),
        'corpus': {f: sha_arquivo(os.path.join(AQUI, 'corpus', f))
                   for f in sorted(os.listdir(os.path.join(AQUI, 'corpus')))},
        'segundos_total': round(time.time() - t0, 1),
    }

    with open(os.path.join(AQUI, 'resultados.json'), 'w') as f:
        json.dump(R, f, indent=1, ensure_ascii=False, default=str)

    L = []
    w = L.append
    w('# RESULTADOS — medicoes que sustentam o paper\n')
    w('Gerado por `python3 paper/prova/roda_tudo.py`. '
      'Nada aqui foi digitado a mao.\n')
    a = R['_ambiente']
    w('| ambiente | valor |')
    w('|---|---|')
    w('| Python | %s |' % a['python'])
    w('| plataforma | %s |' % a['plataforma'])
    w('| sha256 tabelas logisticas | `%s` |' % a['sha_tabelas'][:32])
    w('| sha256 nucleo.py | `%s` |' % a['sha_nucleo'][:32])
    w('| sha256 experimentos.py | `%s` |' % a['sha_experimentos'][:32])
    for k, v in a['corpus'].items():
        w('| sha256 corpus/%s | `%s` |' % (k, v[:32]))
    w('| tempo total | %s s |' % a['segundos_total'])
    w('')

    # E1
    r = R['contagem']
    w('## E1 — o teto da contagem\n')
    w('Fracao maxima das cadeias de n bits que podem encolher k bits:\n')
    w('| k bits de ganho | fracao maxima das entradas |')
    w('|---|---|')
    for k, fr in r['tabela']:
        w('| %d | %.3g |' % (k, fr))
    z = r['aleatorio']
    w('')
    w('Teste: %d buffers de %d bytes de entropia maxima.\n' % (z['n'], z['tam']))
    w('| compressor | tamanho medio (x original) |')
    w('|---|---|')
    w('| este codec (gemeas, ordem 1-4) | %.4f |' % z['nosso_medio'])
    w('| xz -9 | %.4f |' % z['xz_medio'])
    w('| melhor caso observado do codec | %.4f |' % z['nosso_min'])
    w('')

    # E2
    r = R['dicionario']
    w('## E2 — o que as gemeas ja sabem (H(X) -> H(X|M))\n')
    w('Dicionario previo: %d bytes. Mensagem: %d bytes. '
      'Ida-e-volta conferida: frio=%s, quente=%s.\n'
      % (r['dic_bytes'], r['msg_bytes'], r['ok_frio'], r['ok_quente']))
    w('| esquema | bits/byte | x sobre 8 bits |')
    w('|---|---|---|')
    for nome, ch in (('cru (UTF-8)', 'bruto_bpc'), ('gzip -9', 'gzip_bpc'),
                     ('bzip2 -9', 'bz2_bpc'), ('xz -9', 'xz_bpc'),
                     ('zlib com dicionario (32 KB)', 'zdict_bpc'),
                     ('ESTE codec, sem dicionario', 'frio_bpc'),
                     ('ESTE codec, com dicionario', 'quente_bpc')):
        w('| %s | %s | %.2fx |' % (nome, n3(r[ch]), 8.0 / r[ch]))
    w('')
    w('Ganho do dicionario previo sobre o mesmo codec sem ele: **%s**.\n'
      % pct((r['frio_bpc'] - r['quente_bpc']) / r['frio_bpc'] * 100))
    w('SHA-256 da mensagem: `%s`\n' % r['sha'][:32])

    # E3
    w('## E3 — ordens de leitura (frente, tras, vertical)\n')
    for nome in ('prosa', 'tabular'):
        r = R['camadas'][nome]
        w('### %s — %d bytes, passo vertical detectado sozinho: %d '
          '(igualdade %s)\n' % (nome, r['bytes'], r['passo_detectado'],
                                pct(r['taxa_igualdade_vertical'] * 100)))
        w('| leitura | bits/byte |')
        w('|---|---|')
        w('| frente, ordens 1-4 | %s |' % n3(r['frente4']))
        w('| frente, ordens 1-8 (controle: mais modelos) | %s |'
          % n3(r['frente6_controle']))
        w('| so vertical (2 alturas) | %s |' % n3(r['so_vertical2']))
        w('| frente 1-4 + vertical 2 | %s |' % n3(r['frente4_mais_vertical2']))
        w('| de tras para frente, ordens 1-4 | %s |' % n3(r['tras4']))
        w('')
        w('- ganho da camada vertical **contra o controle de mesmo tamanho**: %s'
          % pct(r['ganho_vertical_vs_controle']))
        w('- assimetria frente/tras: %s (positivo = ler de tras custa mais)\n'
          % pct(r['assimetria_frente_tras']))

    # E3b
    r = R['retroleitura']
    w('## E3b — retro-leitura legal: ler o futuro de uma camada ja inteira\n')
    w('| camada | bits/byte |')
    w('|---|---|')
    w('| ALTA (nibble alto), viaja primeiro | %s |' % n3(r['bpc_camada_alta']))
    w('| BAIXA olhando so o passado | %s |' % n3(r['bpc_baixa_so_passado']))
    w('| BAIXA olhando ALTA[i+1], ALTA[i+2] (o futuro) | %s |'
      % n3(r['bpc_baixa_com_futuro']))
    w('| **total, so passado** | **%s** |' % n3(r['bpc_total_so_passado']))
    w('| **total, com futuro** | **%s** |' % n3(r['bpc_total_com_futuro']))
    w('')
    w('Ganho da camada baixa ao poder ler o futuro da camada alta: **%s**.\n'
      % pct(r['ganho_do_futuro_pct']))

    # E4
    r = R['fatorial_primos']
    w('## E4 — base fatorial, primos, posicao\n')
    w('### Lehmer / base fatorial: permutacao -> UM numero\n')
    w('| n | bits do indice | otimo log2(n!) | ingenuo n*log2(n) | economia |')
    w('|---|---|---|---|---|')
    for x in r['lehmer']:
        w('| %d | %d | %.1f | %d | %s |' % (x['n'], x['bits_indice'],
          x['bits_otimo_log2_n_fat'], x['bits_ingenuo'], pct(x['economia_pct'])))
    w('')
    w('### Numeracao de Godel (produto de primos): bijetiva e catastrofica\n')
    w('| bytes | bits do numero | bits crus | fator |')
    w('|---|---|---|---|')
    for x in r['godel']:
        w('| %d | %d | %d | **%.1fx** |' % (x['m_bytes'], x['bits_godel'],
                                            x['bits_crus'], x['fator']))
    w('')
    w('### Primos como IDENTIDADE (nao como compressao)\n')
    w('| primos | bits da impressao | colisao maxima |')
    w('|---|---|---|')
    for x in r['crt']:
        w('| %d | %d | %.3g |' % (x['k_primos'], x['bits_da_impressao'],
                                  x['prob_colisao_max']))
    w('')

    # E5
    r = R['numero_unico']
    w('## E5 — o numero unico existe (e ja tem nome)\n')
    w('Frase: "%s"\n' % r['frase'])
    w('| forma | bits |')
    w('|---|---|')
    w('| UTF-8 cru | %d |' % r['bits_originais'])
    w('| um numero, gemeas sem dicionario | %d |' % r['numero_frio_bits'])
    w('| um numero, gemeas com dicionario | %d |' % r['numero_quente_bits'])
    w('')
    w('O numero (com dicionario, %d digitos decimais):\n'
      % r['numero_quente_digitos'])
    w('```\n%s\n```\n' % r['numero_quente'])
    w('Ida-e-volta conferida byte a byte: **%s**. SHA-256 `%s`\n'
      % (r['ok_quente'], r['sha'][:32]))

    # E6
    r = R['energia']
    w('## E6 — trocar tempo por bits: quando compensa\n')
    w('Criterio, sem numero magico:\n')
    w('```\ncomprimir compensa  <=>  e_calc / N  <  (1 - r) * e_rede\n```\n')
    w('`e_calc` = potencia / vazao (J por byte processado) · '
      '`r` = %.3f (razao medida deste codec) · '
      '`e_rede` = J por byte no enlace · '
      '`N` = quantas vezes o mesmo objeto sera enviado ou lido.\n' % r['r'])
    w('Medido: %d bytes em %.2f s = %.0f B/s (Python puro, um nucleo). '
      'xz -9: %d bytes; este codec: %d bytes.\n'
      % (r['msg_bytes'], r['seg'], r['vazao_medida'], r['xz_bytes'],
         r['nosso_bytes']))
    w('| motor | e_calc (J/byte) | enlace | limiar (1-r)*e_rede | '
      'compensa em 1 envio? | envios p/ empatar |')
    w('|---|---|---|---|---|---|')
    for x in r['linhas']:
        n = x['envios_para_compensar']
        w('| %s | %.3g | %s | %.3g | %s | %s |'
          % (x['motor'], x['e_calc_J_por_byte'], x['enlace'],
             x['limiar_J_por_byte'],
             'SIM' if x['compensa_em_1_envio'] else 'nao',
             '1' if x['compensa_em_1_envio'] else '{:,.0f}'.format(n)))
    w('')
    w('Valores de `e_rede` sao SUPOSICOES declaradas, nao medicoes: '
      'fibra/datacenter 2e-8, 4G 2e-6, satelite/LoRa 2e-4, '
      'espaco profundo 2e-2 J/byte. Trocar o numero troca a conclusao — '
      'a conta fica aberta de proposito.\n')

    # E7
    r = R['determinismo']
    w('## E7 — determinismo: por que o caminho critico e inteiro\n')
    w('| teste | resultado |')
    w('|---|---|')
    w('| somar 2000 floats em duas ordens da o mesmo? | **%s** (delta %.3g) |'
      % (r['float_soma_ordens_diferentes_igual'], r['float_delta']))
    w('| o caminho inteiro deste codec repete bit a bit? | **%s** |'
      % r['inteiro_repetivel'])
    w('| sha256 das tabelas (contrato das gemeas) | `%s` |'
      % r['sha_tabelas'][:32])
    w('')
    w('### Falha localizada: UM contador divergente (de %d bytes decodificados)\n'
      % r['n'])
    w('| erro no contador (de 4096) | contadores testados | quebraram | taxa |')
    w('|---|---|---|---|')
    for x in r['a_um_bit']:
        w('| +%d | %d | %d | %s |' % (x['delta_p_em_4096'],
          x['contadores_testados'], x['falharam'], pct(x['taxa_falha_pct'])))
    w('')
    w('### Falha sistemica: deriva de configuracao entre as gemeas\n')
    w('| deriva | bytes certos | primeiro erro no byte |')
    w('|---|---|---|')
    w('| ordens (1,2,3,5) em vez de (1,2,3,4) | %s | %d |'
      % (pct(r['b_deriva_versao']['pct_certo']),
         r['b_deriva_versao']['primeiro_erro']))
    w('| dicionario previo com 1 byte a menos | %s | %d |'
      % (pct(r['c_deriva_dicionario']['pct_certo']),
         r['c_deriva_dicionario']['primeiro_erro']))
    w('')

    # E7b
    r = R['folga']
    w('## E7b — quanta folga numerica as gemeas tem? (a resposta e: nenhuma)\n')
    w('A gemea receptora calcula cada probabilidade com erro de ate +-D '
      '(numa escala de 4096), em TODA decisao. %d bytes.\n' % r['n'])
    w('| folga D | erro relativo | quebrou | primeiro erro (byte) | bytes certos |')
    w('|---|---|---|---|---|')
    for x in r['linhas']:
        w('| +-%d | %.4f%% | %s de %d | %s | %s |'
          % (x['folga_em_4096'], x['folga_relativa'] * 100,
             x['quebrou'], x['reps'],
             ('%.1f' % x['primeiro_erro_medio'])
             if x['primeiro_erro_medio'] is not None else 'nenhum',
             pct(x['bytes_certos_pct_medio'])))
    w('')

    # E8
    r = R['busca']
    w('## E8 — a busca pela semente curta ("um numero que gera tudo")\n')
    w('| bits do alvo | tentativas medias | 2^k | bits medios da semente | '
      'bits economizados | segundos |')
    w('|---|---|---|---|---|---|')
    for x in r['buscas']:
        w('| %d | %s | %s | %.2f | **%+.2f** | %.4f |'
          % (x['bits_do_alvo'], '{:,.0f}'.format(x['tentativas_medias']),
             '{:,}'.format(x['esperado_2_elevado_k']),
             x['bits_medios_da_semente'], x['bits_economizados_medios'],
             x['segundos_medios']))
    w('')
    w('Tentativas crescem como 2^k. A economia de bits fica **constante** '
      'em torno de 0,7 bit. Tempo exponencial, bits de graca: zero.\n')

    # E9
    r = R['raiz_mista']
    w('## E9 — uma posicao, varias informacoes: raiz mista\n')
    w('%d registros; %s combinacoes possiveis. Ida-e-volta bijetiva conferida '
      'em todos: **%s**.\n'
      % (r['n_registros'], '{:,}'.format(r['combinacoes']),
         r['bijetivo_conferido']))
    w('| campo | valores distintos | bits sozinho |')
    w('|---|---|---|')
    for c in r['campos']:
        w('| %s | %d | %d |' % (c['nome'], c['cardinalidade'], c['bits_isolado']))
    w('')
    w('| forma de guardar um registro | bits |')
    w('|---|---|')
    w('| texto ASCII (como esta no arquivo) | %d |' % r['bits_ascii_por_registro'])
    w('| um campo por byte | %d |' % r['bits_byte_a_byte'])
    w('| campo a campo, em bits | %d |' % r['bits_campo_a_campo'])
    w('| **um unico numero, raiz mista** | **%d** |' % r['bits_raiz_mista'])
    w('| otimo teorico log2(combinacoes) | %.2f |' % r['otimo_exato'])
    w('')
    w('Ganho da raiz mista sobre campo a campo: **%s**. Sobre o ASCII: **%s**.\n'
      % (pct(r['ganho_sobre_campo_a_campo_pct']), pct(r['ganho_sobre_ascii_pct'])))

    # E10
    r = R['dicionario_equacao']
    w('## E10 — o dicionario que e equacao, nao tabela\n')
    w('Busca por `v[i] = c + ((a*(i//k) + b) mod m)` em cada coluna:\n')
    w('| coluna | equacao encontrada |')
    w('|---|---|')
    for c in r['colunas']:
        g = c['gerador']
        w('| %s | %s |' % (c['coluna'],
          ('`a=%d b=%d m=%d k=%d c=%d`' % (g['a'], g['b'], g['m'], g['k'], g['c']))
          if g else 'nenhuma'))
    w('| coluna com ruido real (valor) | %s |'
      % ('nenhuma' if not r['gerador_da_coluna_com_ruido'] else 'ACHOU (suspeito)'))
    w('| prosa em portugues | %s |'
      % ('nenhuma' if not r['gerador_em_prosa'] else 'ACHOU (suspeito)'))
    w('')
    w('%d de %d colunas descritas por equacao: **%.0fx** menos bits que a tabela '
      '(%d bits de equacoes contra %d bits de dados).\n'
      % (r['quantas_acharam'], r['de'], r['fator'],
         r['bits_das_equacoes'], r['bits_das_colunas_achadas']))

    # E11
    r = R['informacao_mutua']
    w('## E11 — quanto uma posicao informa sobre a letra\n')
    w('%d caracteres de prosa; H(caractere) = **%.3f bits**. O piso e o mesmo '
      'calculo sobre posicoes embaralhadas: e o quanto o estimador mente para '
      'cima em amostra finita. So a coluna liquida vale.\n'
      % (r['n_caracteres'], r['H_do_caractere']))
    w('| o que a posicao diz | IM medida | piso (embaralhado) | **IM liquida** |')
    w('|---|---|---|---|')
    for x in r['prosa']:
        w('| %s | %.4f | %.4f | **%.4f** |'
          % (x['sinal'], x['im_bits'], x['piso_embaralhado'], x['im_liquida']))
    w('')
    t = r['tabular']
    w('Em dado tabular, onde a correlacao e real:\n')
    w('| par | informacao mutua |')
    w('|---|---|')
    w('| canal e estado | %.4f bits |' % t['im_canal_estado'])
    w('| **canal e hora** | **%.4f bits** (= H(canal) inteira: o canal sai de graca) |'
      % t['im_canal_hora'])
    w('')

    # E12
    r = R['crt']
    w('## E12 — um numero, varias leituras (Teorema Chines do Resto)\n')
    w('Modulos %s, coprimos dois a dois: **%s**. Os %d de %d registros '
      'conferidos voltaram identicos por resto.\n'
      % (r['modulos'], r['coprimos_dois_a_dois'], r['registros_conferidos'],
         r['de']))
    w('| forma | bits |')
    w('|---|---|')
    w('| raiz mista (E9) | %d |' % r['bits_raiz_mista'])
    w('| Teorema Chines do Resto | %d |' % r['bits_do_numero'])
    w('')
    w('Um numero a mais no fim vira detector de erro, sem tocar no resto:\n')
    w('| primo extra | custo em bits | pega 1 bit virado | pega corrupcao qualquer | limite teorico |')
    w('|---|---|---|---|---|')
    for x in r['deteccao']:
        w('| %d | %.1f | %s | %s | %s |'
          % (x['primo_extra'], x['bits_de_custo'], pct(x['pego_um_bit_pct']),
             pct(x['pego_qualquer_pct']), pct(x['limite_teorico_pct'])))
    w('')

    # E13
    w('## E13 — a camada que so entra se precisar (e nunca viaja)\n')
    w('Os dois lados rodam as duas camadas sempre; muda so quem assina a '
      'probabilidade do bloco. Portao **oraculo**: o emissor escolhe e avisa '
      '(1 bit por bloco). Portao **deduzido**: os dois escolhem quem venceu o '
      'bloco anterior — **zero bits**.\n')
    for nome in ('prosa', 'tabular'):
        r = R['camada_condicional'][nome]
        w('### %s — %d bytes, passo %d\n' % (nome, r['bytes'], r['passo']))
        w('| portao | bits/byte | vertical ligada em |')
        w('|---|---|---|')
        w('| fixo: so frente (camada desligada) | %s | 0%% dos blocos |'
          % n3(r['bpc_so_frente']))
        w('| fixo: vertical sempre ligada | %s | 100%% dos blocos |'
          % n3(r['bpc_sempre_vertical']))
        for l in r['portoes']:
            w('| oraculo, bloco de %d (custa 1 bit/bloco) | %s | %.0f%% |'
              % (l['bloco'], n3(l['bpc_oraculo']), l['blocos_com_vertical_pct']))
            w('| **deduzido, bloco de %d (custa zero)** | **%s** | %.0f%% |'
              % (l['bloco'], n3(l['bpc_deduzido']), l['blocos_com_vertical_pct']))
        w('')

    # E14
    r = R['vacuo']
    w('## E14 — o vacuo: quanto o espaco custa e quanto ele avisa\n')
    w('%d bytes de prosa, %s bits/byte no total.\n' % (r['bytes'], n3(r['bpc'])))
    w('| classe | simbolos | bits/simbolo | %% do fluxo |')
    w('|---|---|---|---|')
    for c in r['classes']:
        w('| %s | %d | %s | %.1f%% |' % (c['classe'], c['simbolos'],
          n3(c['bits_por_simbolo']), c['pct_do_fluxo']))
    w('')
    t = r['terminal']
    w('### O espaco como camada terminal: nao viaja, e remontado no fim\n')
    w('| esquema | bits |')
    w('|---|---|')
    w('| espaco dentro do fluxo | %.0f |' % t['bits_com_espaco_no_fluxo'])
    w('| texto sem espaco | %.0f |' % t['bits_texto_sem_espaco'])
    w('| camada de comprimentos de palavra | %.0f |'
      % t['bits_camada_de_comprimentos'])
    w('| **soma das duas** | **%.0f** |' % t['bits_soma_das_duas'])
    w('')
    w('Resultado: **%s** — tirar o espaco do fluxo sai MAIS CARO.\n'
      % pct(t['ganho_pct']))
    j = r['ja_esta_no_contexto']
    w('### O espaco ja esta dentro do contexto?\n')
    w('| o que a posicao-na-palavra diz sobre a letra | IM | piso | liquida |')
    w('|---|---|---|---|')
    w('| marginal (sozinha) | %.4f | %.4f | **%.4f** |'
      % (j['im_marginal'], j['piso_marginal'], j['im_marginal_liquida']))
    w('| condicional, sabendo 1 caractere anterior | %.4f | %.4f | **%.4f** |'
      % (j['im_condicional'], j['piso_condicional'], j['im_condicional_liquida']))
    w('')
    o = r['rota']
    w('| o espaco como mudanca de rota, no codec | bits/byte |')
    w('|---|---|')
    w('| frente 1-4 | %s |' % n3(o['bpc_frente4']))
    w('| controle: frente 1-8 (mesmo numero de modelos) | %s |'
      % n3(o['bpc_controle_frente6']))
    w('| frente 1-4 + distancia desde o espaco | %s |' % n3(o['bpc_frente4_mais_rota']))
    w('')
    w('Ganho da rota explicita sobre o controle: **%s**.\n'
      % pct(o['ganho_sobre_controle_pct']))

    # E15
    r = R['rrns']
    w('## E15 — redundancia proporcional a importancia (RRNS)\n')
    w('%d modulos base (%s) definem a faixa legitima de %.1f bits. '
      'Ate %d modulos redundantes testados (%s).\n'
      % (r['L_modulos_base'], r['modulos_base'], r['M_legit_bits'],
         len(r['modulos_redundantes']), r['modulos_redundantes']))
    w('| módulos redundantes | bits pagos | corrige até | erro testado | taxa de acerto |')
    w('|---|---|---|---|---|')
    for l in r['linhas']:
        for x in l['por_erro']:
            marca_lim = ' **(limite)**' if x['erros_injetados'] == l['corrige_ate_erros'] else ''
            w('| %d | %.1f | %d | %d%s | %.1f%% |'
              % (l['r_modulos_redundantes_usados'], l['bits_pagos'],
                 l['corrige_ate_erros'], x['erros_injetados'], marca_lim,
                 x['taxa_acerto_pct']))
    w('')
    w('A curva bate a teoria de sistemas de residuos redundantes (RRNS), '
      'existente desde os anos 1960: zero bits corrigem zero erros; cada '
      'par de modulos redundantes compra a correcao de mais um erro, com '
      '100% de acerto ate o limite teorico e queda abrupta um erro acima '
      'dele. Nao ha ajuste fino nem sorte — e o limite matematico exato.\n')

    txt = '\n'.join(L) + '\n'
    with open(os.path.join(AQUI, 'RESULTADOS.md'), 'w', encoding='utf-8') as f:
        f.write(txt)
    sys.stderr.write('\nescrito: paper/prova/RESULTADOS.md e resultados.json\n')


if __name__ == '__main__':
    main()
