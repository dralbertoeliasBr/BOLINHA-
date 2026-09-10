# -*- coding: utf-8 -*-
"""
nucleo.py — codificador aritmetico binario DETERMINISTICO, inteiros puros.

Nao usa float em lugar nenhum do caminho critico. Nao usa dependencia externa.
Roda em Python 3.8+ (inclusive a-Shell / Pythonista no iPhone).

Pecas:
  squash/stretch  : logistica em aritmetica inteira (tabela de 33 pontos, PAQ)
  Tabela          : contadores adaptativos de 12 bits com contagem de 4 bits
  Misturador      : mistura logistica de preditores (pesos inteiros 16.16)
  Enc / Dec       : codificador aritmetico binario carryless de 32 bits
  Preditor        : arvore binaria de simbolo + N submodelos + misturador

O contrato das gemeas: os dois lados executam ESTE MESMO codigo, com as
MESMAS tabelas, na MESMA ordem. Qualquer divergencia quebra o fluxo inteiro
a partir do primeiro bit divergente -- por isso o emissor verifica antes
de enviar (ver verifica_ida_e_volta em experimentos.py).
"""
from array import array
import hashlib

# ---------------------------------------------------------------- logistica

_T = (1, 2, 3, 6, 10, 16, 27, 45, 73, 120, 194, 310, 488, 747, 1101, 1546,
      2047, 2549, 2994, 3348, 3607, 3785, 3901, 3975, 4024, 4050, 4068,
      4079, 4085, 4089, 4092, 4093, 4094)


def squash(d):
    """logistica inversa: (-2047..2047) -> (0..4095). So inteiros."""
    if d > 2047:
        return 4095
    if d < -2047:
        return 0
    w = d & 127
    d = (d >> 7) + 16
    return (_T[d] * (128 - w) + _T[d + 1] * w + 64) >> 7


def _tabela_stretch():
    t = [0] * 4096
    pi = 0
    for x in range(-2047, 2048):
        v = squash(x)
        for p in range(pi, v + 1):
            t[p] = x
        pi = v + 1
    for p in range(pi, 4096):
        t[p] = 2047
    return t


STRETCH = _tabela_stretch()


def impressao_digital_das_tabelas():
    """SHA-256 das tabelas. Vai no cabecalho do fluxo: se as gemeas
    divergirem de versao, isso acusa ANTES de decodificar um bit."""
    h = hashlib.sha256()
    h.update(repr(_T).encode())
    h.update(repr(STRETCH).encode())
    return h.hexdigest()


# ---------------------------------------------------------------- contadores

BITS_TABELA = 20
MASCARA = (1 << BITS_TABELA) - 1


class Tabela(object):
    """Contadores: probabilidade de 12 bits + contagem de 4 bits, em uint16."""
    __slots__ = ('t', 'mascara')

    def __init__(self, bits=BITS_TABELA):
        self.t = array('H', [2048 << 4]) * (1 << bits)
        self.mascara = (1 << bits) - 1

    def p(self, i):
        return self.t[i] >> 4

    def atualiza(self, i, bit):
        v = self.t[i]
        p = v >> 4
        n = v & 15
        p += ((bit << 12) - p) // (n + 2)
        if p < 1:
            p = 1
        elif p > 4094:
            p = 4094
        if n < 15:
            n += 1
        self.t[i] = (p << 4) | n


# ---------------------------------------------------------------- misturador

TAXA = 7


class Misturador(object):
    __slots__ = ('n', 'w', 'base', 'pr')

    def __init__(self, n, n_contextos):
        self.n = n
        self.w = array('l', [65536 // n] * (n * n_contextos))
        self.base = 0
        self.pr = 2048

    def define_contexto(self, c):
        self.base = c * self.n

    def preve(self, st):
        w = self.w
        b = self.base
        s = 0
        for i in range(self.n):
            s += w[b + i] * st[i]
        s >>= 16
        if s > 2047:
            s = 2047
        elif s < -2047:
            s = -2047
        self.pr = squash(s)
        return self.pr

    def atualiza(self, st, bit):
        err = ((bit << 12) - self.pr) * TAXA
        w = self.w
        b = self.base
        for i in range(self.n):
            v = w[b + i] + ((st[i] * err) >> 10)
            if v > (1 << 22):
                v = 1 << 22
            elif v < -(1 << 22):
                v = -(1 << 22)
            w[b + i] = v


# ---------------------------------------------------------- codificador arit.

class Enc(object):
    __slots__ = ('x1', 'x2', 'out')

    def __init__(self):
        self.x1 = 0
        self.x2 = 0xFFFFFFFF
        self.out = bytearray()

    def codifica(self, bit, p):
        if p < 1:
            p = 1
        elif p > 4094:
            p = 4094
        xmid = self.x1 + ((self.x2 - self.x1) >> 12) * p
        if bit:
            self.x2 = xmid
        else:
            self.x1 = xmid + 1
        while ((self.x1 ^ self.x2) & 0xFF000000) == 0:
            self.out.append(self.x2 >> 24)
            self.x1 = (self.x1 << 8) & 0xFFFFFFFF
            self.x2 = ((self.x2 << 8) | 255) & 0xFFFFFFFF

    def encerra(self):
        for _ in range(4):
            self.out.append((self.x1 >> 24) & 255)
            self.x1 = (self.x1 << 8) & 0xFFFFFFFF
        return bytes(self.out)


class Dec(object):
    __slots__ = ('buf', 'pos', 'x1', 'x2', 'x')

    def __init__(self, buf):
        self.buf = buf
        self.pos = 0
        self.x1 = 0
        self.x2 = 0xFFFFFFFF
        self.x = 0
        for _ in range(4):
            self.x = ((self.x << 8) | self._byte()) & 0xFFFFFFFF

    def _byte(self):
        if self.pos < len(self.buf):
            b = self.buf[self.pos]
            self.pos += 1
            return b
        return 0

    def decodifica(self, p):
        if p < 1:
            p = 1
        elif p > 4094:
            p = 4094
        xmid = self.x1 + ((self.x2 - self.x1) >> 12) * p
        if self.x <= xmid:
            bit = 1
            self.x2 = xmid
        else:
            bit = 0
            self.x1 = xmid + 1
        while ((self.x1 ^ self.x2) & 0xFF000000) == 0:
            self.x1 = (self.x1 << 8) & 0xFFFFFFFF
            self.x2 = ((self.x2 << 8) | 255) & 0xFFFFFFFF
            self.x = ((self.x << 8) | self._byte()) & 0xFFFFFFFF
        return bit


# ---------------------------------------------------------------- preditor

def _mistura_hash(x):
    x = (x * 2654435761) & 0xFFFFFFFF
    x ^= x >> 15
    x = (x * 2246822519) & 0xFFFFFFFF
    x ^= x >> 13
    return x


class Preditor(object):
    """N submodelos (um por 'camada'/ordem de leitura) + misturador.

    Cada simbolo de `nbits` bits e' codificado descendo uma arvore binaria.
    Em cada no, cada submodelo consulta seu contador; o misturador pondera.
    """

    def __init__(self, n_sub, nbits=8, bits_tabela=BITS_TABELA):
        self.n_sub = n_sub
        self.nbits = nbits
        self.mascara = (1 << bits_tabela) - 1
        self.tabs = [Tabela(bits_tabela) for _ in range(n_sub)]
        self.mix = Misturador(n_sub + 1, 1 << nbits)
        self.pos = [0] * n_sub
        self.idx = [0] * n_sub

    def _prep(self, chaves):
        for j in range(self.n_sub):
            self.idx[j] = _mistura_hash(chaves[j] + j * 0x51ED2701)

    def _p(self, no):
        st = []
        d = no * 0x9E3779B1
        for j in range(self.n_sub):
            i = (self.idx[j] ^ d) & self.mascara
            self.pos[j] = i
            st.append(STRETCH[self.tabs[j].p(i)])
        st.append(256)
        self.mix.define_contexto(no)
        return self.mix.preve(st), st

    def _aprende(self, st, bit):
        self.mix.atualiza(st, bit)
        for j in range(self.n_sub):
            self.tabs[j].atualiza(self.pos[j], bit)

    def codifica(self, enc, sim, chaves):
        self._prep(chaves)
        no = 1
        for k in range(self.nbits - 1, -1, -1):
            bit = (sim >> k) & 1
            p, st = self._p(no)
            enc.codifica(bit, p)
            self._aprende(st, bit)
            no = no + no + bit

    def decodifica(self, dec, chaves, ruido=0, rnd=None):
        """`ruido` simula a GEMEA IMPERFEITA: a probabilidade calculada do
        outro lado difere em ate +-ruido (de 4096). E' o caso real de dois
        LLMs que nao sao bit-a-bit identicos."""
        self._prep(chaves)
        no = 1
        for _ in range(self.nbits):
            p, st = self._p(no)
            if ruido:
                p += rnd.randrange(-ruido, ruido + 1)
                if p < 1:
                    p = 1
                elif p > 4094:
                    p = 4094
            bit = dec.decodifica(p)
            self._aprende(st, bit)
            no = no + no + bit
        return no - (1 << self.nbits)

    def treina(self, sim, chaves):
        """Atualiza o modelo SEM emitir bit. E' assim que o dicionario previo
        entra: os dois lados 'leem' o mesmo material antes de conversar."""
        self._prep(chaves)
        no = 1
        for k in range(self.nbits - 1, -1, -1):
            bit = (sim >> k) & 1
            _, st = self._p(no)
            self._aprende(st, bit)
            no = no + no + bit

    def custo_em_bits(self, sim, chaves):
        """Custo ideal (-log2 p) do simbolo, sem codificar. Para medir camadas."""
        from math import log
        self._prep(chaves)
        no = 1
        total = 0.0
        for k in range(self.nbits - 1, -1, -1):
            bit = (sim >> k) & 1
            p, st = self._p(no)
            q = (p if bit else 4096 - p) / 4096.0
            if q < 1e-9:
                q = 1e-9
            total += -log(q, 2)
            self._aprende(st, bit)
            no = no + no + bit
        return total
