# -*- coding: utf-8 -*-
"""
experimentos.py — cada funcao aqui e' UMA afirmacao do paper.
Se a funcao nao roda, a afirmacao sai do paper.

Uso:  python3 roda_tudo.py
"""
import os
import sys
import time
import zlib
import bz2
import lzma
import random
import hashlib
from math import log, factorial, ceil

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nucleo import (Preditor, Enc, Dec, impressao_digital_das_tabelas)

AQUI = os.path.dirname(os.path.abspath(__file__))
CORPUS = os.path.join(AQUI, 'corpus')


def le(nome):
    with open(os.path.join(CORPUS, nome), 'rb') as f:
        return f.read()


# ============================================================ chaves (camadas)
# Toda funcao de chave so' pode olhar para d[j] com j < i.
# Isso NAO e' disciplina do programador: e' o tipo do argumento.
# O decodificador chama a mesma funcao com um buffer de tamanho i.
# -> a Lei da Admissibilidade e' imposta pela API, nao prometida.

def faz_chaves_frente(ordens):
    def f(d, i):
        ks = []
        for o in ordens:
            h = (o * 0x2F0FD693) & 0xFFFFFFFF
            for j in range(i - o, i):
                b = d[j] if j >= 0 else 0
                h = ((h * 0x01000193) ^ b) & 0xFFFFFFFF
            ks.append(h)
        return ks
    return f


def faz_chaves_vertical(W, alturas):
    def f(d, i):
        ks = []
        for a in alturas:
            h = (0x7ED55D16 ^ ((a * 2654435761) & 0xFFFFFFFF)) & 0xFFFFFFFF
            for r in range(1, a + 1):
                j = i - r * W
                b = d[j] if j >= 0 else 0
                h = ((h * 0x01000193) ^ b) & 0xFFFFFFFF
            ks.append(h)
        return ks
    return f


def soma_chaves(*fs):
    def f(d, i):
        ks = []
        for g in fs:
            ks.extend(g(d, i))
        return ks
    return f


def detecta_passo(d, maximo=160):
    """Acha sozinho a largura da camada vertical (o 'numero de cima')."""
    melhor, melhor_p = 0, 0
    n = len(d)
    for W in range(2, min(maximo, n // 4)):
        c = 0
        for i in range(W, n):
            if d[i] == d[i - W]:
                c += 1
        taxa = c / float(n - W)
        if taxa > melhor:
            melhor, melhor_p = taxa, W
    return melhor_p, melhor


# ============================================================ motor

def custo_bits(dados, chaves_fn, n_sub, dicionario=b''):
    pr = Preditor(n_sub, 8)
    for i in range(len(dicionario)):
        pr.treina(dicionario[i], chaves_fn(dicionario, i))
    t = 0.0
    for i in range(len(dados)):
        t += pr.custo_em_bits(dados[i], chaves_fn(dados, i))
    return t


def comprime(dados, chaves_fn, n_sub, dicionario=b''):
    pr = Preditor(n_sub, 8)
    for i in range(len(dicionario)):
        pr.treina(dicionario[i], chaves_fn(dicionario, i))
    e = Enc()
    for i in range(len(dados)):
        pr.codifica(e, dados[i], chaves_fn(dados, i))
    return e.encerra()


def descomprime(fluxo, n, chaves_fn, n_sub, dicionario=b''):
    pr = Preditor(n_sub, 8)
    for i in range(len(dicionario)):
        pr.treina(dicionario[i], chaves_fn(dicionario, i))
    dec = Dec(fluxo)
    saida = bytearray()
    for i in range(n):
        saida.append(pr.decodifica(dec, chaves_fn(saida, i)))
    return bytes(saida)


def verifica_ida_e_volta(dados, chaves_fn, n_sub, dicionario=b''):
    """O PROTOCOLO: quem comprime descomprime antes de enviar.
    So' sai da maquina o que voltou identico. Devolve (fluxo, ok, sha)."""
    fluxo = comprime(dados, chaves_fn, n_sub, dicionario)
    volta = descomprime(fluxo, len(dados), chaves_fn, n_sub, dicionario)
    h1 = hashlib.sha256(dados).hexdigest()
    h2 = hashlib.sha256(volta).hexdigest()
    return fluxo, (h1 == h2), h1


# ============================================================ E1 — contagem

def e1_contagem():
    """Nenhum mapa injetivo encolhe todas as entradas. Nem IA muda isso."""
    r = {'tabela': [], 'aleatorio': []}
    for k in (1, 4, 8, 16, 32, 64):
        r['tabela'].append((k, 2.0 ** (-k)))
    rnd = random.Random(33)
    n_amostras, tam = 64, 256
    exp_nosso, exp_xz = [], []
    fk = faz_chaves_frente((1, 2, 3, 4))
    for _ in range(n_amostras):
        b = bytes(rnd.randrange(256) for _ in range(tam))
        exp_nosso.append(len(comprime(b, fk, 4)) / float(tam))
        exp_xz.append(len(lzma.compress(b, preset=9)) / float(tam))
    r['aleatorio'] = {
        'n': n_amostras, 'tam': tam,
        'nosso_medio': sum(exp_nosso) / n_amostras,
        'xz_medio': sum(exp_xz) / n_amostras,
        'nosso_min': min(exp_nosso),
    }
    return r


# ============================================================ E2 — dicionario

def e2_dicionario():
    """O ganho das gemeas vem do que as duas ja' sabem: H(X) -> H(X|M)."""
    d = le('pt_sounavy.txt')
    corte = (len(d) * 2) // 3
    dic, msg = d[:corte], d[corte:]
    fk = faz_chaves_frente((1, 2, 3, 4, 6))
    n = 5

    t0 = time.time()
    fluxo_frio, ok_frio, _ = verifica_ida_e_volta(msg, fk, n)
    t_frio = time.time() - t0

    t0 = time.time()
    fluxo_quente, ok_quente, sha = verifica_ida_e_volta(msg, fk, n, dic)
    t_quente = time.time() - t0

    co = zlib.compressobj(9, zlib.DEFLATED, -15, 9, 0, zdict=dic[-32768:])
    zdic = co.compress(msg) + co.flush()

    L = float(len(msg))
    return {
        'dic_bytes': len(dic), 'msg_bytes': len(msg),
        'bruto_bpc': 8.0,
        'gzip_bpc': len(zlib.compress(msg, 9)) * 8 / L,
        'bz2_bpc': len(bz2.compress(msg, 9)) * 8 / L,
        'xz_bpc': len(lzma.compress(msg, preset=9)) * 8 / L,
        'zdict_bpc': len(zdic) * 8 / L,
        'frio_bpc': len(fluxo_frio) * 8 / L,
        'quente_bpc': len(fluxo_quente) * 8 / L,
        'ok_frio': ok_frio, 'ok_quente': ok_quente, 'sha': sha,
        'seg_frio': t_frio, 'seg_quente': t_quente,
        'bytes_frio': len(fluxo_frio), 'bytes_quente': len(fluxo_quente),
    }


# ============================================================ E3 — camadas

def _bpc(dados, fn, n, dic=b''):
    return custo_bits(dados, fn, n, dic) / float(len(dados))


def e3_camadas():
    """Frente, tras, vertical, e a mistura. Onde cada leitura paga."""
    out = {}
    for nome, arq in (('prosa', 'pt_sounavy.txt'), ('tabular', 'tabular.csv')):
        d = le(arq)
        W, taxa = detecta_passo(d)
        f4 = faz_chaves_frente((1, 2, 3, 4))
        f6 = faz_chaves_frente((1, 2, 3, 4, 6, 8))
        v2 = faz_chaves_vertical(W, (1, 2))
        mist = soma_chaves(f4, v2)

        r = {
            'passo_detectado': W, 'taxa_igualdade_vertical': taxa,
            'frente4': _bpc(d, f4, 4),
            'frente6_controle': _bpc(d, f6, 6),
            'so_vertical2': _bpc(d, v2, 2),
            'frente4_mais_vertical2': _bpc(d, mist, 6),
            'tras4': _bpc(d[::-1], f4, 4),
            'bytes': len(d),
        }
        r['ganho_vertical_vs_controle'] = (
            (r['frente6_controle'] - r['frente4_mais_vertical2'])
            / r['frente6_controle'] * 100.0)
        r['assimetria_frente_tras'] = (r['tras4'] - r['frente4']) / r['frente4'] * 100.0
        out[nome] = r
    return out


def e3b_retroleitura():
    """A retro-leitura LEGAL: ler o futuro de uma camada ja' inteira.

    Camada ALTA (nibble alto) viaja primeiro, inteira. Depois a camada BAIXA
    e' codificada podendo olhar ALTA[i+1] e ALTA[i+2] -- o futuro -- porque
    o receptor ja' tem a camada ALTA toda. Nada e' prometido: e' medido.
    """
    d = le('pt_sounavy.txt')
    hi = bytes(b >> 4 for b in d)
    lo = bytes(b & 15 for b in d)

    def custo4(seq, chaves_fn, n_sub):
        pr = Preditor(n_sub, 4)
        t = 0.0
        for i in range(len(seq)):
            t += pr.custo_em_bits(seq[i], chaves_fn(i))
        return t

    def hh(*vs):
        h = 0x811C9DC5
        for v in vs:
            h = ((h * 0x01000193) ^ (v & 0xFF)) & 0xFFFFFFFF
        return h

    g = lambda s, j: (s[j] if 0 <= j < len(s) else 0)

    ch_hi = lambda i: [hh(1, g(hi, i - 1)), hh(2, g(hi, i - 1), g(hi, i - 2)),
                       hh(3, g(hi, i - 1), g(hi, i - 2), g(hi, i - 3))]
    bits_hi = custo4(hi, ch_hi, 3)

    ch_lo_passado = lambda i: [
        hh(11, g(hi, i)),
        hh(12, g(hi, i), g(lo, i - 1)),
        hh(13, g(hi, i), g(hi, i - 1), g(lo, i - 1)),
        hh(14, g(hi, i), g(lo, i - 1), g(lo, i - 2)),
    ]
    ch_lo_futuro = lambda i: [
        hh(11, g(hi, i)),
        hh(12, g(hi, i), g(lo, i - 1)),
        hh(13, g(hi, i), g(hi, i - 1), g(lo, i - 1)),
        hh(14, g(hi, i), g(lo, i - 1), g(lo, i - 2)),
        hh(15, g(hi, i), g(hi, i + 1)),
        hh(16, g(hi, i), g(hi, i + 1), g(hi, i + 2)),
    ]
    bits_lo_p = custo4(lo, ch_lo_passado, 4)
    bits_lo_f = custo4(lo, ch_lo_futuro, 6)

    L = float(len(d))
    return {
        'bytes': len(d),
        'bpc_camada_alta': bits_hi / L,
        'bpc_baixa_so_passado': bits_lo_p / L,
        'bpc_baixa_com_futuro': bits_lo_f / L,
        'bpc_total_so_passado': (bits_hi + bits_lo_p) / L,
        'bpc_total_com_futuro': (bits_hi + bits_lo_f) / L,
        'ganho_do_futuro_pct': (bits_lo_p - bits_lo_f) / bits_lo_p * 100.0,
    }


# ============================================== E4 — fatorial, primos, posicao

def bits_exatos(n):
    return n.bit_length()


def lehmer_codifica(perm):
    """permutacao -> UM numero (base fatorial). Bijetivo, sem desperdicio."""
    n = len(perm)
    disp = list(range(n))
    idx = 0
    for k in range(n):
        j = disp.index(perm[k])
        idx = idx * (n - k) + j
        disp.pop(j)
    return idx


def lehmer_decodifica(idx, n):
    disp = list(range(n))
    saida = []
    for k in range(n):
        base = factorial(n - k - 1)
        j = idx // base if base else 0
        idx -= j * base
        saida.append(disp.pop(j))
    return saida


PRIMOS = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61,
          67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131]


def godel(bs):
    """Numeracao de Godel: multiset -> UM numero. Bijetivo e catastrofico."""
    x = 1
    for i, b in enumerate(bs[:len(PRIMOS)]):
        x *= PRIMOS[i] ** (b + 1)
    return x


def e4_fatorial_primos():
    rnd = random.Random(33)
    r = {'lehmer': [], 'godel': [], 'crt': []}
    for n in (8, 12, 52, 100):
        p = list(range(n))
        rnd.shuffle(p)
        idx = lehmer_codifica(p)
        assert lehmer_decodifica(idx, n) == p
        otimo = log(factorial(n), 2)
        ingenuo = n * ceil(log(n, 2))
        r['lehmer'].append({
            'n': n, 'bits_indice': max(1, bits_exatos(idx)),
            'bits_otimo_log2_n_fat': otimo, 'bits_ingenuo': ingenuo,
            'economia_pct': (ingenuo - otimo) / ingenuo * 100.0,
        })
    for m in (4, 8, 16, 32):
        bs = bytes(rnd.randrange(256) for _ in range(m))
        x = godel(bs)
        r['godel'].append({
            'm_bytes': m, 'bits_godel': bits_exatos(x),
            'bits_crus': 8 * m, 'fator': bits_exatos(x) / float(8 * m),
        })
    # primos como IDENTIDADE (nao como compressao): impressao por residuos
    for k in (4, 8, 16):
        prod = 1
        for p in PRIMOS[:k]:
            prod *= p
        r['crt'].append({
            'k_primos': k, 'bits_da_impressao': bits_exatos(prod),
            'prob_colisao_max': 1.0 / prod,
        })
    return r


# ============================================================ E5 — um numero

def e5_numero_unico():
    """A intuicao do 'um numero so' esta' certa -- e ja' tem nome."""
    d = le('pt_sounavy.txt')
    corte = (len(d) * 2) // 3
    dic = d[:corte]
    frase = ('A voz como sistema operacional. Menos dado, dado certo. '
             'Nao e eu, e nos.').encode('utf-8')
    fk = faz_chaves_frente((1, 2, 3, 4, 6))

    f_frio, ok_f, _ = verifica_ida_e_volta(frase, fk, 5)
    f_quente, ok_q, sha = verifica_ida_e_volta(frase, fk, 5, dic)
    N_frio = int.from_bytes(f_frio, 'big')
    N_quente = int.from_bytes(f_quente, 'big')
    return {
        'frase': frase.decode('utf-8'), 'bytes_originais': len(frase),
        'bits_originais': 8 * len(frase),
        'numero_frio_bits': N_frio.bit_length(),
        'numero_quente_bits': N_quente.bit_length(),
        'numero_quente_digitos': len(str(N_quente)),
        'numero_quente': str(N_quente),
        'ok_frio': ok_f, 'ok_quente': ok_q, 'sha': sha,
    }


# ============================================================ E6 — energia

def e6_energia():
    """Quando trocar TEMPO por BITS economiza energia?

    Enviar B bytes crus custa            B * e_rede
    Enviar comprimido custa    B * e_calc + B * r * e_rede
    Logo compensa se e somente se:

        e_calc  <  (1 - r) * e_rede            [criterio verde]

    e_calc  = potencia / vazao   (J por byte processado)
    r       = tamanho comprimido / original
    N       = quantas vezes o mesmo objeto sera' enviado/lido
              (o calculo se paga UMA vez; o enlace paga TODA vez)
        e_calc / N  <  (1 - r) * e_rede

    Nao ha' numero magico: ha' uma desigualdade com parametros declarados.
    """
    d = le('pt_sounavy.txt')
    corte = (len(d) * 2) // 3
    dic, msg = d[:corte], d[corte:]
    fk = faz_chaves_frente((1, 2, 3, 4, 6))
    t0 = time.time()
    fluxo = comprime(msg, fk, 5, dic)
    t = time.time() - t0
    vazao_medida = len(msg) / t
    r = len(fluxo) / float(len(msg))

    # (nome, vazao B/s, potencia W). O primeiro e' MEDIDO aqui.
    motores = [
        ('este codec, Python puro (MEDIDO)', vazao_medida, 5.0),
        ('mesmo codec em C, estimado 10 MB/s', 10e6, 5.0),
        ('LLM gemea no iPhone: 14,1 tok/s medidos x 4 B/token', 14.1 * 4, 2.0),
        ('LLM gemea em GPU: 2000 tok/s x 4 B/token', 2000 * 4, 400.0),
    ]
    enlaces = [('fibra / datacenter', 2e-8), ('4G movel', 2e-6),
               ('satelite / LoRa', 2e-4), ('espaco profundo', 2e-2)]

    linhas = []
    for nm, vaz, pot in motores:
        e_calc = pot / vaz
        for en, e_rede in enlaces:
            limiar = (1.0 - r) * e_rede
            n_min = e_calc / limiar if limiar > 0 else float('inf')
            linhas.append({
                'motor': nm, 'vazao_B_por_s': vaz, 'potencia_W': pot,
                'e_calc_J_por_byte': e_calc, 'enlace': en,
                'e_rede_J_por_byte': e_rede, 'limiar_J_por_byte': limiar,
                'compensa_em_1_envio': e_calc < limiar,
                'envios_para_compensar': n_min,
            })
    return {'r': r, 'seg': t, 'vazao_medida': vazao_medida,
            'msg_bytes': len(msg), 'nosso_bytes': len(fluxo),
            'xz_bytes': len(lzma.compress(msg, preset=9)),
            'linhas': linhas}


# ============================================================ E7 — determinismo

def e7_determinismo():
    """Por que o caminho critico e' inteiro, e por que se confere antes.

    Tres dessincronizacoes, da mais leve a mais banal:
      (a) UM bit virado em UM contador que o decodificador REALMENTE visita
      (b) deriva de versao: a gemea remota usa ordens (1,2,3,5) em vez de
          (1,2,3,4) -- um 'detalhe' de configuracao
      (c) deriva de dicionario: a gemea remota leu 1 byte a menos do previo
    """
    rnd = random.Random(33)
    xs = [rnd.random() * (10 ** rnd.randrange(-6, 7)) for _ in range(2000)]
    ys = xs[:]
    rnd.shuffle(ys)
    s1, s2 = sum(xs), sum(ys)

    d = le('pt_sounavy.txt')[:1500]
    fk = faz_chaves_frente((1, 2, 3, 4))
    a = comprime(d, fk, 4)
    b = comprime(d, fk, 4)
    inteiro_igual = (hashlib.sha256(a).hexdigest() ==
                     hashlib.sha256(b).hexdigest())

    def mede(saida):
        n = min(len(saida), len(d))
        iguais = sum(1 for i in range(n) if saida[i] == d[i])
        prim = next((i for i in range(n) if saida[i] != d[i]), -1)
        return {'pct_certo': iguais * 100.0 / len(d), 'primeiro_erro': prim}

    # (a) descobrir um contador que o decodificador visita de fato
    pr = Preditor(4, 8)
    dec = Dec(a)
    saida = bytearray()
    visitados = set()
    for i in range(len(d)):
        s_ = pr.decodifica(dec, fk(saida, i))
        saida.append(s_)
        visitados.update(pr.pos)
        if len(visitados) > 4000:
            break
    alvo = sorted(visitados)[len(visitados) // 2]

    # UM bit virado, repetido sobre muitos contadores realmente visitados:
    # o que interessa nao e' um caso, e' a TAXA de falha -- e o silencio.
    amostra = sorted(visitados)
    passo = max(1, len(amostra) // 60)
    amostra = amostra[::passo][:60]
    ra = []
    for delta_p in (1, 16, 256, 2048):
        falhas, piores = 0, []
        for alvo_i in amostra:
            pr = Preditor(4, 8)
            v = pr.tabs[0].t[alvo_i]
            np_ = min(4094, max(1, (v >> 4) + delta_p))
            pr.tabs[0].t[alvo_i] = (np_ << 4) | (v & 15)
            dec = Dec(a)
            sa = bytearray()
            for i in range(len(d)):
                sa.append(pr.decodifica(dec, fk(sa, i)))
            m = mede(sa)
            if m['primeiro_erro'] >= 0:
                falhas += 1
                piores.append(m)
        ra.append({'delta_p_em_4096': delta_p,
                   'contadores_testados': len(amostra), 'falharam': falhas,
                   'taxa_falha_pct': falhas * 100.0 / len(amostra),
                   'primeiro_erro_medio': (
                       sum(x['primeiro_erro'] for x in piores) / float(len(piores))
                       if piores else None)})
    alvo = amostra[len(amostra) // 2]

    # (b) deriva de versao no modelo
    fk_torto = faz_chaves_frente((1, 2, 3, 5))
    pr = Preditor(4, 8)
    dec = Dec(a)
    saida_b = bytearray()
    for i in range(len(d)):
        saida_b.append(pr.decodifica(dec, fk_torto(saida_b, i)))
    rb = mede(saida_b)

    # (c) deriva de dicionario
    dic = le('pt_sounavy.txt')[1500:3000]
    a2 = comprime(d, fk, 4, dic)
    pr = Preditor(4, 8)
    dic_torto = dic[:-1]
    for i in range(len(dic_torto)):
        pr.treina(dic_torto[i], fk(dic_torto, i))
    dec = Dec(a2)
    saida_c = bytearray()
    for i in range(len(d)):
        saida_c.append(pr.decodifica(dec, fk(saida_c, i)))
    rc = mede(saida_c)

    return {
        'float_soma_ordens_diferentes_igual': (s1 == s2),
        'float_delta': abs(s1 - s2),
        'inteiro_repetivel': inteiro_igual,
        'sha_tabelas': impressao_digital_das_tabelas(),
        'n': len(d),
        'contador_alvo': alvo,
        'a_um_bit': ra,
        'b_deriva_versao': rb,
        'c_deriva_dicionario': rc,
    }


# ================================================== E7b — folga das gemeas

def e7b_folga():
    """QUANTA divergencia numerica as gemeas aguentam antes de quebrar?

    Este e' o problema real de duas LLMs: elas nao sao bit-a-bit identicas.
    Aqui a gemea receptora calcula p com erro de ate +-D (em 4096) e mede-se
    ate onde o fluxo sobrevive. Nao e' argumento: e' curva medida.
    """
    d = le('pt_sounavy.txt')[:1200]
    fk = faz_chaves_frente((1, 2, 3, 4))
    fluxo = comprime(d, fk, 4)
    linhas = []
    for D in (0, 1, 2, 4, 8, 16, 64, 256):
        quebrou, primeiros, certos = 0, [], []
        reps = 1 if D == 0 else 12
        for s_ in range(reps):
            rnd = random.Random(1000 + s_)
            pr = Preditor(4, 8)
            dec = Dec(fluxo)
            saida = bytearray()
            for i in range(len(d)):
                saida.append(pr.decodifica(dec, fk(saida, i), D, rnd))
            prim = next((i for i in range(len(d)) if saida[i] != d[i]), -1)
            ig = sum(1 for i in range(len(d)) if saida[i] == d[i])
            certos.append(ig * 100.0 / len(d))
            if prim >= 0:
                quebrou += 1
                primeiros.append(prim)
        linhas.append({
            'folga_em_4096': D,
            'folga_relativa': D / 4096.0,
            'reps': reps, 'quebrou': quebrou,
            'taxa_quebra_pct': quebrou * 100.0 / reps,
            'primeiro_erro_medio': (sum(primeiros) / float(len(primeiros))
                                    if primeiros else None),
            'bytes_certos_pct_medio': sum(certos) / float(reps),
        })
    return {'n': len(d), 'linhas': linhas}


# ============================================================ E8 — a busca

def e8_busca():
    """O 'um bit que gera tudo': procurar semente curta que reproduz o alvo.

    Se o alvo e' arbitrario, achar semente que gere k bits custa ~2^k
    tentativas E a semente sai com ~k bits. Tempo explode, bits nao encolhem.
    Media sobre varios alvos, para que sorte nao vire resultado.
    """
    rnd = random.Random(33)
    saidas = []
    for k, reps in ((8, 24), (12, 24), (16, 12), (20, 6)):
        tent, bits_sem, seg = [], [], []
        for _ in range(reps):
            alvo = rnd.getrandbits(k)
            mascara = (1 << k) - 1
            t0 = time.time()
            semente = 0
            n = 0
            while True:
                h = hashlib.sha256(semente.to_bytes(8, 'big')).digest()
                n += 1
                if (int.from_bytes(h[:4], 'big') & mascara) == alvo:
                    break
                semente += 1
            seg.append(time.time() - t0)
            tent.append(n)
            bits_sem.append(max(1, semente.bit_length()))
        m_t = sum(tent) / float(reps)
        m_b = sum(bits_sem) / float(reps)
        saidas.append({
            'bits_do_alvo': k, 'repeticoes': reps,
            'tentativas_medias': m_t, 'esperado_2_elevado_k': 2 ** k,
            'bits_medios_da_semente': m_b,
            'bits_economizados_medios': k - m_b,
            'segundos_medios': sum(seg) / float(reps),
        })
    return {'buscas': saidas}
