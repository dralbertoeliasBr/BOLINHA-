VERSAO = "V11-2026-08-07-1640-SEM-DUPLICATA"
print("#"*60)
print(f"# GAIA ARQUITETURA — VERSÃO: {VERSAO}")
print("#"*60)
print()

import re, json, os

# =========================================================
# CAMADA 1 e 2 (iguais à v8, sem mudança)
# =========================================================

class DetectorLexico:
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
        sinal = "Positiva" if pontuacao > 0 else "Negativa" if pontuacao < 0 else "Neutra"
        return {"score": round(pontuacao, 2), "sinal": sinal}


class VocabularioNativo:
    def __init__(self, caminho="vocabulario_nativo.json"):
        self.caminho = caminho
        if os.path.exists(caminho):
            with open(caminho, "r", encoding="utf-8") as f:
                self.dados = json.load(f)
        else:
            self.dados = {
                "constroi": ["traz", "ajuda", "salva", "protege", "cria", "corrige",
                             "resolve", "cura", "conserta", "combate", "defende"],
                "destroi": ["destrói", "mata", "ataca", "prejudica", "arruína",
                            "corrompe", "quebra", "engana"],
                "pendentes": []
            }
            self.salvar()

    def salvar(self):
        with open(self.caminho, "w", encoding="utf-8") as f:
            json.dump(self.dados, f, ensure_ascii=False, indent=2)

    def ensinar(self, verbo, tipo):
        verbo = verbo.lower().strip()
        if verbo not in self.dados[tipo]:
            self.dados[tipo].append(verbo)
        self.dados["pendentes"] = [p for p in self.dados["pendentes"] if verbo not in p["texto"].lower()]
        self.salvar()

    def registrar_pendente(self, texto):
        entrada = {"texto": texto}
        if entrada not in self.dados["pendentes"]:
            self.dados["pendentes"].append(entrada)
            self.salvar()


class DetectorEstrutural:
    def __init__(self, vocab):
        self.vocab = vocab

    def analisar(self, texto):
        palavras = re.findall(r'\b\w+\b', texto.lower())
        artigos = {"a", "o", "as", "os", "um", "uma", "uns", "umas"}
        for i, p in enumerate(palavras):
            veio_de_artigo = i > 0 and palavras[i-1] in artigos
            if veio_de_artigo: continue
            if p in self.vocab.dados["constroi"]:
                return {"veredito": "Positiva", "motivo": f'ação construtiva: "{p}"'}
            if p in self.vocab.dados["destroi"]:
                return {"veredito": "Negativa", "motivo": f'ação destrutiva: "{p}"'}
        self.vocab.registrar_pendente(texto)
        return {"veredito": "Indefinido", "motivo": "vocabulário nativo ainda não cobre essa frase"}


# =========================================================
# CAMADA 3: FILA DE LOTE (Stop/Go econômico)
# -----------------------------------------------------------
# Não dispara token a cada frase. Guarda tudo localmente.
# Só monta UMA chamada de API quando você decide disparar —
# seja porque quer resposta agora, seja porque achou sinal.
# =========================================================

class FilaCamada3:
    def __init__(self, caminho="fila_camada3.json"):
        self.caminho = caminho
        if os.path.exists(caminho):
            with open(caminho, "r", encoding="utf-8") as f:
                self.dados = json.load(f)
        else:
            self.dados = {"fila": []}
            self.salvar()

    def salvar(self):
        with open(self.caminho, "w", encoding="utf-8") as f:
            json.dump(self.dados, f, ensure_ascii=False, indent=2)

    def adicionar(self, texto, r1, r2, status):
        """
        status = 'confirmado' ou 'duvida'.
        SEM REDUÇÃO: guarda a frase INTACTA, mais o raciocínio
        completo de cada camada — não só o veredito final.
        Isso vale tanto pra confirmado quanto pra dúvida, porque
        um 'confirmado' pode estar errado (as duas camadas concordando
        por motivo errado, como já vimos acontecer).
        """
        item = {
            "texto_original_intacto": texto,
            "status": status,
            "camada1_sinal": r1["sinal"],
            "camada1_score": r1["score"],
            "camada2_veredito": r2["veredito"],
            "camada2_motivo": r2["motivo"],
        }
        # não duplica: se a mesma frase com o mesmo status já tá na fila, ignora
        ja_existe = any(
            i["texto_original_intacto"] == texto and i["status"] == status
            for i in self.dados["fila"]
        )
        if not ja_existe:
            self.dados["fila"].append(item)
            self.salvar()

    def tamanho(self):
        return len(self.dados["fila"])

    def montar_prompt_lote(self):
        """UMA chamada só. Cada item leva frase intacta + raciocínio
        completo — nunca só 'Positiva'/'Negativa' isolado."""
        if not self.dados["fila"]:
            return None

        blocos = []
        for i, item in enumerate(self.dados["fila"], start=1):
            blocos.append(
                f'{i}. Frase (intacta, sem alteração): "{item["texto_original_intacto"]}"\n'
                f'   Status local: {item["status"].upper()}\n'
                f'   Camada 1 (léxico) concluiu: {item["camada1_sinal"]} (score {item["camada1_score"]})\n'
                f'   Camada 2 (estrutural) concluiu: {item["camada2_veredito"]} — motivo: {item["camada2_motivo"]}'
            )

        corpo = "\n\n".join(blocos)
        prompt = f"""Analise as {len(self.dados['fila'])} frases abaixo.
Para as marcadas DUVIDA: as camadas locais discordaram, decida a intenção real.
Para as marcadas CONFIRMADO: as duas camadas concordaram, mas não assuma que
estão certas — o raciocínio de cada uma está exposto, avalie se a conclusão
local está correta ou se é concordância por motivo equivocado.

{corpo}"""
        return prompt

    def limpar(self):
        self.dados["fila"] = []
        self.salvar()


def processar(texto, lexico, estrutural, fila, modo="economico", auditar_confirmados=False):
    r1 = lexico.analisar(texto)
    r2 = estrutural.analisar(texto)

    if r2["veredito"] == "Indefinido":
        veredito_final = r1["sinal"]
        rota = "1 - Léxico decide (Camada 2 pendente)"

    elif r1["sinal"] == r2["veredito"]:
        veredito_final = r1["sinal"]
        # CONFIRMADO não significa correto -- se auditoria estiver ligada,
        # manda mesmo assim pra checagem, com frase intacta e raciocínio completo
        if auditar_confirmados:
            fila.adicionar(texto, r1, r2, status="confirmado")
            rota = f"1+2 - CONFIRMADO, mas enviado pra auditoria (fila tem {fila.tamanho()})"
        else:
            rota = "1+2 - CONFIRMADO (sem auditoria)"

    else:
        veredito_final = "Indeterminado"
        if modo == "profundo":
            rota = "3 - DISPARO IMEDIATO (modo profundo, gasta token agora)"
        else:
            fila.adicionar(texto, r1, r2, status="duvida")
            rota = f"3 - GUARDADO NA FILA (modo econômico, fila tem {fila.tamanho()} item(ns))"

    return {"texto": texto, "camada1": r1, "camada2": r2, "veredito_final": veredito_final, "rota": rota}


# ===== TESTE =====
if __name__ == "__main__":
    lexico = DetectorLexico()
    vocab = VocabularioNativo()
    estrutural = DetectorEstrutural(vocab)
    fila = FilaCamada3()

    frases = [
        "O amor é bom.",
        "A ajuda foi boa, mas o julgamento foi errado.",
        "O crime combate o amor.",       # concordância FALSA -- deve ir pra auditoria
        "O medo salva o crime.",         # discordância real -- vai pra dúvida
    ]

    print("MODO: econômico + auditoria de confirmados LIGADA")
    print("(nada dispara token na hora -- tudo vai pra fila, sem redução)")
    print("="*66)
    for f in frases:
        r = processar(f, lexico, estrutural, fila, modo="economico", auditar_confirmados=True)
        print(f'C1:{r["camada1"]["sinal"]:9s} C2:{r["camada2"]["veredito"]:11s} → {r["rota"]}')
        print(f'  "{f}"')
        print()

    print("="*66)
    print(f"FILA ACUMULADA: {fila.tamanho()} item(ns) esperando disparo em lote")
    print()
    prompt_lote = fila.montar_prompt_lote()
    if prompt_lote:
        print("PROMPT DE LOTE PRONTO (frase intacta + raciocínio, SEM redução):")
        print("-"*66)
        print(prompt_lote)

    print()
    print("#"*60)
    print(f"# FIM — VERSÃO: {VERSAO}")
    print("#"*60)