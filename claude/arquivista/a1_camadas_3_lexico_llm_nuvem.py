import re, json, os
from datetime import datetime

# =========================================================
# CAMADA 1: LÉXICO RÍGIDO (determinístico, local, rápido)
# =========================================================

class DetectorSegundaIntencao:
    def __init__(self):
        self.lexico = {
            "bom": 2.5, "amor": 3.5, "ajuda": 2.0, "certo": 1.5, "justo": 2.0,
            "ruim": -2.5, "medo": -2.0, "ódio": -3.5, "errado": -1.5, "crime": -3.0,
        }
        self.variantes = {"certa": "certo", "boa": "bom", "justa": "justo", "errada": "errado"}
        self.negacoes = {"não", "nada", "nunca", "jamais", "nem", "sem"}
        self.adversativas = {"mas", "porém", "contudo", "entretanto", "todavia"}
        self.verbos_inversores = {"corrigir", "resolver", "curar", "salvar", "consertar",
                                    "superar", "vencer", "evitar", "combater", "impedir",
                                    "prevenir", "denunciar", "punir"}

    def analisar(self, texto):
        palavras = re.findall(r'\b\w+\b', texto.lower())
        pontuacao = 0.0
        inv_neg = inv_verbo = False
        boost = 1.0
        for p in palavras:
            if p in self.adversativas: boost = 1.5; continue
            if p in self.negacoes: inv_neg = True; continue
            if p in self.verbos_inversores: inv_verbo = True; continue
            base = self.variantes.get(p, p)
            if base in self.lexico:
                v = self.lexico[base]
                if inv_verbo: v *= -0.9; inv_verbo = False
                if inv_neg: v *= -0.8; inv_neg = False
                pontuacao += v * boost
        return round(pontuacao, 2)


def delta_decide(score):
    if score > 0: return 1
    if score < 0: return -1
    return 0


def calcular_pi(score):
    decisao = delta_decide(score)
    peso_decisao = abs(decisao) * 2.5
    peso_lexico = min(abs(score) / 4.0, 2.5)
    pi = round(peso_decisao + peso_lexico, 2)
    distancia = round(abs(5 - pi), 2)
    return decisao, pi, distancia


# =========================================================
# CAMADA 2: LLM LOCAL PEQUENA (offline, segunda checagem)
# -----------------------------------------------------------
# No Pythonista isso é o PocketPal + Llama 3.2 3B que você já
# tem rodando offline. Aqui deixo o CONTRATO da função —
# a interface que sua LLM local precisa cumprir. Troque o corpo
# dessa função pela chamada real ao seu modelo local.
# =========================================================

def chamar_llm_local(texto, contexto_lexico):
    """
    STUB — representa a chamada ao Llama 3.2 local via PocketPal.
    Espera-se que a LLM local responda com:
      { "confianca": 0.0 a 1.0, "leitura": "texto curto" }

    Por enquanto (sem o modelo real plugado), simulamos uma
    heurística simples: quanto mais perto de Π=5, menor a confiança
    que uma leitura rápida teria — isso é só placeholder até você
    conectar o Llama de verdade.
    """
    _, pi, distancia = calcular_pi(contexto_lexico)
    # dentro da zona de dúvida (distância 0 a 1.5), reescala pra 0 a 1
    # quanto mais perto de 0 (mais perto do Π=5, mais ambíguo), menor a confiança
    confianca_simulada = round(min(distancia / 1.5, 1.0), 2)
    return {
        "confianca": confianca_simulada,
        "leitura": f"[SIMULADO] leitura offline com confiança {confianca_simulada}"
    }


# =========================================================
# CAMADA 3: NUVEM (Claude) — só quando as duas de baixo falham
# =========================================================

def montar_prompt_para_nuvem(texto, score, pi, leitura_local):
    return f"""Analise a intenção real desta frase, considerando possível
segunda intenção, sarcasmo ou construção retórica:

Frase: "{texto}"

Dados da análise local:
- Score léxico: {score}
- Π (complexidade): {pi}
- Leitura da LLM local (baixa confiança): {leitura_local}

Responda: qual a intenção mais provável, e por quê?"""


# =========================================================
# ORQUESTRADOR — decide qual camada resolve cada frase
# =========================================================

class MemoriaLexica:
    def __init__(self, caminho="memoria_arquitetura.json"):
        self.caminho = caminho
        self.dados = {"registros": []}

    def registrar(self, entrada):
        self.dados["registros"].append(entrada)

    def salvar(self):
        with open(self.caminho, "w", encoding="utf-8") as f:
            json.dump(self.dados, f, ensure_ascii=False, indent=2)


def processar(texto, detector, memoria):
    score = detector.analisar(texto)
    decisao, pi, distancia = calcular_pi(score)

    resultado = {
        "texto": texto, "score": score, "decisao_delta": decisao,
        "pi": pi, "distancia_de_5": distancia,
        "camada_resolveu": None, "detalhe": None
    }

    # CAMADA 1 resolve sozinha: score forte e longe da zona de dúvida
    if distancia > 1.5:
        resultado["camada_resolveu"] = "1 - Léxico"
        resultado["detalhe"] = f"decisão direta: {'Positiva' if decisao>0 else 'Negativa' if decisao<0 else 'Neutra'}"

    else:
        # zona de dúvida: chama CAMADA 2 (LLM local offline)
        checagem_local = chamar_llm_local(texto, score)

        if checagem_local["confianca"] >= 0.6:
            resultado["camada_resolveu"] = "2 - LLM local (offline)"
            resultado["detalhe"] = checagem_local["leitura"]
        else:
            # nem a camada 2 fechou com confiança -> escalona pra nuvem
            resultado["camada_resolveu"] = "3 - Nuvem (Claude)"
            resultado["detalhe"] = montar_prompt_para_nuvem(texto, score, pi, checagem_local["leitura"])

    memoria.registrar(resultado)
    return resultado


# ===== TESTE COM O BANCO INTEIRO =====
detector = DetectorSegundaIntencao()
memoria = MemoriaLexica()

frases = [
    "O amor é bom.",
    "O crime é ruim.",
    "Sentir medo é ruim, mas o amor traz a ajuda certa para fazer o que é justo e corrigir o crime errado.",
    "A ajuda foi boa, mas o julgamento foi errado.",
    "Isso não é bom, isso é péssimo.",
    "O amor combate o crime errado, mas o medo ruim destrói a ajuda certa e o julgamento justo.",
]

contagem_camadas = {"1 - Léxico": 0, "2 - LLM local (offline)": 0, "3 - Nuvem (Claude)": 0}

print("="*78)
for f in frases:
    r = processar(f, detector, memoria)
    contagem_camadas[r["camada_resolveu"]] += 1
    print(f'Π={r["pi"]:.2f} | dist={r["distancia_de_5"]:.2f} → {r["camada_resolveu"]}')
    print(f'  "{f}"')
    print()

memoria.salvar()
print("="*78)
print("DISTRIBUIÇÃO DE CARGA ENTRE AS TRÊS CAMADAS:")
for camada, n in contagem_camadas.items():
    print(f"  {camada}: {n} frase(s)")