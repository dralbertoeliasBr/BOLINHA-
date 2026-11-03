# GaIA_all_in_2026-11-01.py — tudo num arquivo só (all-in)
# Conceito: Sounavy. Código: Claude. Arquivo novo; os anteriores continuam intactos.
# Junta: (1) escada de funções vitais, (2) regra 2/3 + Beta paralelo + 13 rodadas,
#        (3) Arquivista 2/3. Copiar, colar no Pythonista e apertar ▶.

# gaia_funcoes_vitais.py — Escada de funções vitais do GaIA (v1, 01/11/2026)
# Autor do conceito: Sounavy (Antônio Alberto Lopes Elias, ORCID 0000-0002-5602-9916)
# Coautoria de código: Claude. Arquivo novo; não altera nada anterior.
#
# Ideia: o Delta sobe a escada só quando o degrau de baixo não resolve.
# Caminho de menos energia ("dominó"). Decide quando a confiança passa de 0,618.
#   N0 REFLEXO  (tronco)    : o Delta resolve sozinho (2+2=4). Custo 1.
#   N1 BOX      (contexto)  : memória de contexto próxima.     Custo 3.
#   N2 PENTA    (cerebelo)  : correção aprendida; o Teta vigia. Custo 5.
#   N3 CLAUDE A (memória acionada): a "releitura do livro".     Custo 11.
# Regra de proveniência: LEMBRADO (já estava guardado) é diferente de APRENDIDO (novo).

import re, json, hashlib, datetime

LIMIAR = 0.618

class Gaia:
    def __init__(self):
        self.box = {}          # N1: contexto próximo  {chave: valor}
        self.penta = {}        # N2: pares fala_bruta -> intenção confirmada
        self.erros = {}        # Teta: contagem de erro repetido por entrada
        self.arquivo = {}      # N3: memória longa (o "livro" já lido)
        self.rastro = []

    # ---------- degraus ----------
    def n0_reflexo(self, q):
        if re.fullmatch(r"[\d\s\+\-\*/\(\)\.]+", q):
            try:
                return str(eval(q, {"__builtins__": {}})), 1.0
            except Exception:
                return None, 0.0
        return None, 0.0

    def n1_box(self, q):
        k = q.lower().strip()
        return (self.box[k], 0.9) if k in self.box else (None, 0.0)

    def n2_penta(self, q):
        k = q.lower().strip()
        if k in self.penta:
            if self.erros.get(k, 0) >= 2:      # Teta: erro repetido
                return None, 0.3               # força subir (modo hipótese)
            return self.penta[k], 0.8
        return None, 0.0

    def n3_claude_a(self, q):
        # Aqui entraria a chamada real ao Claude. Por enquanto: memória longa.
        # Se não estava guardado ("dormiu na aula"), NÃO finge que lembrou.
        k = q.lower().strip()
        for chave, texto in self.arquivo.items():
            if any(p in texto.lower() for p in k.split() if len(p) > 3):
                return ("LEMBRADO", chave, texto), 0.75
        return ("APRENDIDO", None, "novo — precisa da sua confirmação"), 0.5

    # ---------- o Delta ----------
    def delta(self, q):
        escada = [("N0_REFLEXO", self.n0_reflexo, 1),
                  ("N1_BOX", self.n1_box, 3),
                  ("N2_PENTA", self.n2_penta, 5),
                  ("N3_CLAUDE_A", self.n3_claude_a, 11)]
        gasto = 0
        for nome, f, custo in escada:
            gasto += custo
            r, conf = f(q)
            if r is not None and conf >= LIMIAR:
                return self._registra(q, nome, r, conf, gasto, "DECIDIU")
        # Ninguém passou do limiar: SEM_DESCIDA (reconhece que não sabe)
        return self._registra(q, nome, r, conf, gasto, "SEM_DESCIDA")

    def corrigir(self, fala, intencao):
        k = fala.lower().strip()
        if k in self.penta and self.penta[k] != intencao:
            self.erros[k] = self.erros.get(k, 0) + 1
        self.penta[k] = intencao

    def _registra(self, q, nivel, r, conf, gasto, status):
        e = {"quando": datetime.datetime.now().isoformat(timespec="seconds"),
             "pergunta": q, "nivel": nivel, "resposta": r,
             "confianca": conf, "energia": gasto, "status": status}
        e["selo"] = hashlib.sha256(json.dumps(e, ensure_ascii=False,
                                              default=str).encode()).hexdigest()[:16]
        self.rastro.append(e)
        return e

# ---------- teste ----------
def teste_escada():
    g = Gaia()
    g.box["paciente das 14h"] = "retorno de placa miorrelaxante"
    g.corrigir("dabi", "DABT")
    g.arquivo["R28"] = "Star System: estrelinhas como recompensa do sistema"
    testes = ["2+2", "paciente das 14h", "dabi", "o que eram as estrelinhas",
              "receita de bolo de fubá"]
    for t in testes:
        e = g.delta(t)
        print(f"{t!r:32} -> {e['nivel']:12} energia {e['energia']:2}  "
              f"{e['status']:11} {e['resposta']}")
    # Teta: o mesmo erro corrigido duas vezes -> sobe de modo
    g.corrigir("dabi", "David"); g.corrigir("dabi", "DABT")
    e = g.delta("dabi")
    print(f"{'dabi (erro repetido)':32} -> {e['nivel']:12} energia {e['energia']:2}  "
          f"{e['status']:11} {e['resposta']}")


# ============================================================
# gaia_beta_testes_solo.py — arquivo único, sem import (01/11/2026)
# Junta: regra 2/3 + Beta em paralelo + Beta em até 13 rodadas.
# Feito porque no Pythonista o import de gaia_regra_2de3 falhou.
# Não altera os arquivos anteriores. Basta abrir e apertar ▶.

from itertools import product
# gaia_regra_2de3.py — Regra 2/3 (v1, 01/11/2026)
# Conceito: Sounavy + Claude. Arquivo novo; não altera nada anterior.
#
# REGRA 2/3
#  1. Três votam. Decide quem tiver 2 de 3 (por peso: >= 2/3 do peso total).
#  2. 3/3 = CONSENSO (estrela). 2/3 = DECIDE, e o voto vencido fica GUARDADO.
#  3. 1/1/1 = SEM_DESCIDA -> nova rodada (máx. 3), não decide no meio.
#  4. Abstenção: decide quem tiver 2/3 de quem votou, se ainda houver 2 votos.
#  5. Zona de risco (pagamento, senha, apagamento): o humano TEM que estar
#     entre os que aprovam. Sem ele, não passa.
#  6. Anti-eco (Teta): se dois votam sempre juntos, a concordância deles vale
#     menos; o sistema avisa.
#
# Dois usos: (A) Sounavy, Claude, GaIA.  (B) DABT: Alfa, Beta(1,8), Teta; o
# Delta anuncia, o Penta só sugere e não vota.

from collections import defaultdict

RISCO = {"pagamento", "senha", "apagamento"}

def regra_2de3(votos, pesos=None, zona=None, humano="Sounavy", historico=None):
    """votos: {votante: opcao ou None(abstém)}"""
    pesos = pesos or {v: 1.0 for v in votos}
    validos = {v: o for v, o in votos.items() if o is not None}
    if len(validos) < 2:
        return {"status": "SEM_DESCIDA", "motivo": "menos de 2 votos"}
    total = sum(pesos[v] for v in validos)
    soma = defaultdict(float)
    for v, o in validos.items():
        soma[o] += pesos[v]
    opcao, peso = max(soma.items(), key=lambda x: x[1])
    aviso = []
    if historico:                                   # regra 6: anti-eco
        for a, b, taxa in _ecos(historico):
            aviso.append(f"eco: {a} e {b} concordam {taxa:.0%} das vezes")
    if peso < total * 2 / 3:
        return {"status": "SEM_DESCIDA", "motivo": "ninguém fez 2/3",
                "placar": dict(soma), "aviso": aviso}
    if zona in RISCO and validos.get(humano) != opcao:
        return {"status": "BLOQUEADO", "motivo": f"zona de risco sem o {humano}",
                "placar": dict(soma)}
    vencidos = {v: o for v, o in validos.items() if o != opcao}
    return {"status": "CONSENSO" if not vencidos else "DECIDE",
            "decisao": opcao, "placar": dict(soma),
            "voto_guardado": vencidos, "aviso": aviso}

def _ecos(historico, limite=0.9):
    nomes = list(historico[0].keys())
    for i in range(len(nomes)):
        for j in range(i + 1, len(nomes)):
            a, b = nomes[i], nomes[j]
            iguais = sum(h[a] == h[b] for h in historico)
            taxa = iguais / len(historico)
            if taxa >= limite:
                yield a, b, taxa

def rodadas(funcao_votar, max_rodadas=3, **kw):
    for r in range(1, max_rodadas + 1):
        res = regra_2de3(funcao_votar(r), **kw)
        res["rodada"] = r
        if res["status"] != "SEM_DESCIDA":
            return res
    return res



V = {"Alfa": 1.0, "Beta": 1.8, "Teta": 1.0}
O = {"Alfa": 1.0, "Beta": 1.0, "Teta": 1.0}

def paralelo(votos):
    rv, ro = regra_2de3(votos, pesos=V), regra_2de3(votos, pesos=O)
    dv, do = rv.get("decisao", rv["status"]), ro.get("decisao", ro["status"])
    if dv == do:
        return "JUNTOS", dv, dv, do
    return "DIVERGEM", "debate/humano", dv, do



PHI = 0.618
PESOS_BETA = [1.0, 1.61, 1.8, 2.5]

FIB = [1, 1, 2, 3, 5, 8, 13, 13, 13, 13, 13, 13, 13]

def peso_beta(W, r, modo):
    if modo == "aurea":        # relaxa por 0,618 a cada rodada (nunca chega a 1)
        return 1 + (W - 1) * PHI ** (r - 1)
    # "fibonacci": relaxa devagar no começo, rápido depois; chega a 1 na rodada 7
    return W - (W - 1) * FIB[r - 1] / 13 if r > 1 else W

def decide_com_rodadas(votos, W, max_r=13, modo="aurea"):
    for r in range(1, max_r + 1):
        w = peso_beta(W, r, modo)
        res = regra_2de3(votos, pesos={"Alfa": 1.0, "Beta": w, "Teta": 1.0})
        if res["status"] != "SEM_DESCIDA":
            return res.get("decisao", res["status"]), r, w
    return "SEM_DESCIDA", max_r, w


def teste_paralelo():

        opcoes = ["ir", "parar", None]
        cont = {"JUNTOS": 0, "DIVERGEM": 0}
        print(f"{'Alfa':6}{'Beta':7}{'Teta':7}| {'Veto 1,8':12}{'Ombro 1,0':12}-> resultado")
        for a, b, t in product(opcoes, repeat=3):
            votos = {"Alfa": a, "Beta": b, "Teta": t}
            s, final, dv, do = paralelo(votos)
            cont[s] += 1
            if s == "DIVERGEM":
                print(f"{str(a):6}{str(b):7}{str(t):7}| {dv:12}{do:12}-> {final}")
        print(f"\n27 combinações: juntos {cont['JUNTOS']}, divergem {cont['DIVERGEM']}")

def teste_rodadas():

        combos = list(product(["ir", "parar", None], repeat=3))
        print(f"{'Beta':>5} | {'decide 1ª':>9} {'precisou +rodadas':>17} {'nunca':>6} "
              f"{'energia total':>13} | Beta vence sozinho?")
        for modo in ["aurea", "fibonacci"]:
            print(f"\n=== relaxamento {modo} ===")
            detalhes = {}
            for W in PESOS_BETA:
                prim, mais, nunca, energia, sozinho = 0, 0, 0, 0, 0
                for a, b, t in combos:
                    v = {"Alfa": a, "Beta": b, "Teta": t}
                    dec, r, w = decide_com_rodadas(v, W, modo=modo)
                    energia += r
                    if dec == "SEM_DESCIDA": nunca += 1
                    elif r == 1: prim += 1
                    else:
                        mais += 1
                        detalhes.setdefault(W, []).append((a, b, t, dec, r, round(w, 3)))
                    # Beta ganha sozinho contra alguém, na 1ª rodada?
                    if r == 1 and b is not None and dec == b and \
                       sum(1 for x in (a, t) if x == b) == 0 and any(x is not None for x in (a, t)):
                        sozinho += 1
                print(f"{W:>5} | {prim:>9} {mais:>17} {nunca:>6} {energia:>13} | {sozinho}")
            print("\nCasos que só destravaram relaxando o Beta:")
            for W, lista in detalhes.items():
                for a, b, t, dec, r, w in lista:
                    print(f"  Beta {W}: Alfa={a} Beta={b} Teta={t} -> {dec} na rodada {r} (Beta valia {w})")

def teste_beta():
    print("########## BETA EM PARALELO ##########")
    teste_paralelo()
    print("\n########## BETA EM ATÉ 13 RODADAS ##########")
    teste_rodadas()


# ============================================================
# gaia_arquivista.py — Arquivista v1 (01/11/2026)
# Conceito: Sounavy (regra 2/3, 1/3 nuvem x 2/3 aqui, cada um começa diferente).
# Código: Claude. Só biblioteca padrão (roda no Pythonista). Arquivo novo.
#
# Como funciona:
#  1. Sela o conteúdo (SHA-256 + data/hora).
#  2. Quebra em 3 pedaços pela regra 2/3 (Shamir): QUALQUER 2 reconstroem;
#     1 pedaço sozinho não revela nada.
#  3. Distribui conforme o grau:  "borda" = 2 aqui + 1 nuvem
#                                 "nuvem" = 1 aqui + 2 nuvem
#                                 "blindado" = 1 aqui + 1 nuvem + 1 terceiro
#  4. Cada pessoa começa diferente: a "semente" dela muda o cálculo inicial.
#  5. Nunca apaga: mesmo nome vira versão nova (v2, v3...).
# PROTÓTIPO: a divisão é segura em teoria; falta criptografia de transporte
# e chave guardada no Keychain antes de uso real.

import os, json, hashlib, secrets, datetime

P = 2**521 - 1                 # primo grande (Mersenne) para a regra 2/3
BLOCO = 64                     # bytes por bloco (< 521 bits)
RAIZ = "arquivo_gaia"
LUGARES = {"borda": ["aqui", "aqui", "nuvem"],
           "nuvem": ["aqui", "nuvem", "nuvem"],
           "blindado": ["aqui", "nuvem", "terceiro"]}

# ---------- regra 2/3 (Shamir, grau 1) ----------
def _quebrar(segredo_int, semente):
    # coeficiente "aleatório" + semente pessoal: cada pessoa começa diferente
    a = (secrets.randbelow(P) + int.from_bytes(semente, "big")) % P
    return [(x, (segredo_int + a * x) % P) for x in (1, 2, 3)]

def _juntar(p1, p2):
    (x1, y1), (x2, y2) = p1, p2
    l1 = x2 * pow(x2 - x1, -1, P) % P
    l2 = x1 * pow(x1 - x2, -1, P) % P
    return (y1 * l1 + y2 * l2) % P

# ---------- Arquivista ----------
class Arquivista:
    def __init__(self, dono, raiz=RAIZ):
        self.dono, self.raiz = dono, raiz
        self.semente = hashlib.sha256(("semente:" + dono).encode()).digest()
        os.makedirs(raiz, exist_ok=True)
        self.indice_path = os.path.join(raiz, "indice.json")
        self.indice = json.load(open(self.indice_path)) if os.path.exists(self.indice_path) else {}

    def arquivar(self, nome, conteudo, grau="borda", box="05"):
        dados = conteudo.encode() if isinstance(conteudo, str) else conteudo
        selo = hashlib.sha256(dados).hexdigest()
        versao = sum(1 for k in self.indice if k.startswith(nome + "@v")) + 1
        chave = f"{nome}@v{versao}"
        pedacos = [[], [], []]
        for i in range(0, len(dados), BLOCO):
            n = int.from_bytes(b"\x01" + dados[i:i + BLOCO], "big")
            for j, (x, y) in enumerate(_quebrar(n, self.semente)):
                pedacos[j].append(y)
        lugares = LUGARES[grau]
        arquivos = []
        for j, lugar in enumerate(lugares):
            pasta = os.path.join(self.raiz, lugar)
            os.makedirs(pasta, exist_ok=True)
            arq = os.path.join(pasta, f"{chave}.p{j+1}.json")
            json.dump({"x": j + 1, "y": [hex(v) for v in pedacos[j]]}, open(arq, "w"))
            arquivos.append(arq)
        self.indice[chave] = {"selo": selo, "quando": datetime.datetime.now().isoformat(timespec="seconds"),
                              "grau": grau, "box": box, "lugares": lugares,
                              "arquivos": arquivos, "tamanho": len(dados)}
        json.dump(self.indice, open(self.indice_path, "w"), indent=1, ensure_ascii=False)
        return chave, selo

    def desarquivar(self, chave, usar=(0, 1)):
        info = self.indice[chave]
        ps = [json.load(open(info["arquivos"][i])) for i in usar]
        saida = b""
        for y1, y2 in zip(ps[0]["y"], ps[1]["y"]):
            n = _juntar((ps[0]["x"], int(y1, 16)), (ps[1]["x"], int(y2, 16)))
            saida += n.to_bytes((n.bit_length() + 7) // 8, "big")[1:]
        ok = hashlib.sha256(saida).hexdigest() == info["selo"]
        return saida.decode(errors="replace"), ok

# ---------------- teste ----------------
def teste_arquivista():
    import shutil
    shutil.rmtree(RAIZ, ignore_errors=True)
    a = Arquivista("Sounavy")
    texto = ("Escada de funções vitais: reflexo, box, Penta+Teta, Claude A. "
             "Regra 2/3: eu, você e o GaIA. O 9 fica na vertical. ") * 3
    chave, selo = a.arquivar("funcoes_vitais", texto, grau="borda")
    print("Arquivado:", chave, "selo", selo[:16], "lugares", a.indice[chave]["lugares"])
    for par in [(0, 1), (0, 2), (1, 2)]:
        t, ok = a.desarquivar(chave, par)
        print(f"  pedaços {par[0]+1}+{par[1]+1}: reconstrói={'SIM' if t == texto else 'NÃO'} selo={'OK' if ok else 'FALHOU'}")
    # um pedaço sozinho: o que ele mostra?
    p = json.load(open(a.indice[chave]["arquivos"][2]))
    print("  pedaço da nuvem sozinho (início):", p["y"][0][:40], "...  -> não legível")
    # adulteração
    arq = a.indice[chave]["arquivos"][0]
    d = json.load(open(arq)); d["y"][0] = hex(int(d["y"][0], 16) ^ 1); json.dump(d, open(arq, "w"))
    t, ok = a.desarquivar(chave, (0, 1))
    print("  adulterado 1 pedaço: selo", "OK" if ok else "FALHOU -> detectado")
    t, ok = a.desarquivar(chave, (1, 2))
    print("  sem o pedaço adulterado (2+3):", "recupera" if ok else "falha")
    # nunca apaga
    chave2, _ = a.arquivar("funcoes_vitais", texto + " v2", grau="nuvem")
    print("Mesmo nome de novo ->", chave2, "| v1 continua:", "funcoes_vitais@v1" in a.indice)
    # cada um começa diferente: mesmo texto, mesmo dono, duas vezes
    c1, _ = a.arquivar("teste", "mesmo texto")
    c2, _ = a.arquivar("teste", "mesmo texto")
    y1 = json.load(open(a.indice[c1]["arquivos"][0]))["y"][0]
    y2 = json.load(open(a.indice[c2]["arquivos"][0]))["y"][0]
    print("Mesmo texto arquivado 2x gera pedaços iguais?", "SIM" if y1 == y2 else "NÃO (nunca repete o começo)")


# =================== RODA TUDO ===================
if __name__ == "__main__":
    print("=" * 10, "1) ESCADA DE FUNÇÕES VITAIS", "=" * 10)
    teste_escada()
    print("\n" + "=" * 10, "2) REGRA 2/3 E BETA", "=" * 10)
    teste_beta()
    print("\n" + "=" * 10, "3) ARQUIVISTA 2/3", "=" * 10)
    teste_arquivista()
