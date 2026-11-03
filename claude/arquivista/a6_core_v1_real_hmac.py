#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ARQUIVISTA CORE - v1 real
Ecossistema de borda para custodia soberana de arquivos.
Arquiteto: Sounavy (CRO 45849 / ORCID 0000-0002-5602-9916)
DNA: DNA-ARQUITETO-2026-SOUNAVY-CLX

O QUE ESTA VERSAO HONRA (diferente das coladas):
- Integridade VERIFICAVEL: assinatura HMAC-SHA256 real sobre o conteudo,
  conferivel por chave. Nao e a etiqueta "ARQUITETO" decorativa.
- Sem colisao silenciosa: nome = timestamp + hash; indice por hash COMPLETO.
- Extracao REAL: varre pasta, deduplica (Stop/Go SHA-256) e sela em lote.
- Manifesto: cada operacao registrada em _manifesto.log, auditavel.
- Criptografia HONESTA: cifra autenticada (Fernet) SE a lib existir; se nao
  existir, NAO finge .enc - marca encrypted=False e mantem HMAC + hash.
"""

import os
import json
import base64
import hashlib
import hmac
from datetime import datetime

# ---- camada de confidencialidade opcional, sem mentira ----
try:
    from cryptography.fernet import Fernet
    _CRYPTO = True
except Exception:
    _CRYPTO = False

DNA = "DNA-ARQUITETO-2026-SOUNAVY-CLX"

# Semantica das 7 Boxes (arquitetura do Arquiteto)
BOX_SEMANTICA = {
    "00": "BOX_00_PRETO",   # selado / recuperacao
    "01": "BOX_01_VERDE",   # dados verdes / vivo
    "02": "BOX_02",
    "03": "BOX_03",
    "04": "BOX_04",         # 04-07: replicacao vitalicia (Legado)
    "05": "BOX_05",
    "06": "BOX_06",
    "07": "BOX_07",
}


def _fernet_key(chave_bytes):
    # Fernet exige 32 bytes urlsafe-b64. Derivamos da chave por SHA-256.
    return base64.urlsafe_b64encode(hashlib.sha256(chave_bytes).digest())


class Arquivista:
    def __init__(self, chave_secreta=None):
        self.base = os.path.expanduser("~/Documents/ARQUIVISTA_CORE")
        self.index_path = os.path.join(self.base, "_index.json")
        self.manifesto_path = os.path.join(self.base, "_manifesto.log")
        # chave para assinatura/integridade. Publica por padrao (DNA) -> honesto:
        # so vira confidencial de verdade se voce passar sua propria chave (QRNG).
        self.chave = (chave_secreta or DNA).encode()
        self._inicializar()
        self.index = self._carregar_index()

    def _inicializar(self):
        os.makedirs(self.base, exist_ok=True)
        for nome in BOX_SEMANTICA.values():
            os.makedirs(os.path.join(self.base, nome), exist_ok=True)

    def _carregar_index(self):
        if os.path.exists(self.index_path):
            try:
                with open(self.index_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                return {}
        return {}

    def _salvar_index(self):
        with open(self.index_path, "w", encoding="utf-8") as f:
            json.dump(self.index, f, indent=2, ensure_ascii=False)

    def _log(self, evento):
        linha = "{} | {}\n".format(datetime.now().isoformat(), evento)
        with open(self.manifesto_path, "a", encoding="utf-8") as f:
            f.write(linha)

    def _assinar(self, dados_bytes):
        # HMAC-SHA256 real: assinatura conferivel por chave.
        return hmac.new(self.chave, dados_bytes, hashlib.sha256).hexdigest()

    def _box_dir(self, box_id):
        nome = BOX_SEMANTICA.get(str(box_id).zfill(2))
        if not nome:
            raise ValueError("Box inexistente: {}".format(box_id))
        return os.path.join(self.base, nome)

    # ---------- CUSTODIA (selar um payload) ----------
    def custodia(self, payload, box_id="00", origem="manual"):
        conteudo = payload if isinstance(payload, str) else json.dumps(payload, ensure_ascii=False)
        dados_bytes = conteudo.encode("utf-8")
        hash_full = hashlib.sha256(dados_bytes).hexdigest()

        # Stop/Go: hash ja existe -> NAO regrava (dedup real, nao acidental)
        if hash_full in self.index:
            self._log("STOP (duplicado) {} origem={}".format(hash_full[:12], origem))
            return {"status": "STOP_DUPLICADO", "hash": hash_full, "ref": self.index[hash_full]}

        assinatura = self._assinar(dados_bytes)

        encrypted = False
        armazenado = conteudo
        if _CRYPTO:
            token = Fernet(_fernet_key(self.chave)).encrypt(dados_bytes)
            armazenado = token.decode("utf-8")
            encrypted = True

        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        nome_arquivo = "{}_{}.json".format(ts, hash_full[:12])
        caminho = os.path.join(self._box_dir(box_id), nome_arquivo)

        registro = {
            "dna": DNA,
            "hash_sha256": hash_full,
            "hmac_sig": assinatura,
            "encrypted": encrypted,
            "box": str(box_id).zfill(2),
            "origem": origem,
            "criado_em": ts,
            "payload": armazenado,
        }
        with open(caminho, "w", encoding="utf-8") as f:
            json.dump(registro, f, indent=2, ensure_ascii=False)

        self.index[hash_full] = caminho
        self._salvar_index()
        self._log("GO (selado) {} box={} origem={}".format(hash_full[:12], box_id, origem))
        return {"status": "GO_SELADO", "hash": hash_full, "caminho": caminho, "encrypted": encrypted}

    # ---------- VERIFICAR (integridade real, funcao separada) ----------
    def verificar(self, caminho):
        try:
            with open(caminho, "r", encoding="utf-8") as f:
                reg = json.load(f)
        except Exception as e:
            return {"ok": False, "motivo": "arquivo ilegivel: {}".format(e)}

        armazenado = reg["payload"]
        if reg.get("encrypted"):
            if not _CRYPTO:
                return {"ok": False, "motivo": "cifrado mas lib cryptography ausente"}
            try:
                conteudo_bytes = Fernet(_fernet_key(self.chave)).decrypt(armazenado.encode("utf-8"))
            except Exception:
                # token adulterado ou chave errada
                return {"ok": False, "hash_ok": False, "sig_ok": False,
                        "motivo": "ADULTERADO ou chave incorreta", "caminho": caminho}
        else:
            conteudo_bytes = armazenado.encode("utf-8")

        hash_recalc = hashlib.sha256(conteudo_bytes).hexdigest()
        sig_recalc = self._assinar(conteudo_bytes)
        ok_hash = hmac.compare_digest(hash_recalc, reg["hash_sha256"])
        ok_sig = hmac.compare_digest(sig_recalc, reg["hmac_sig"])
        return {"ok": ok_hash and ok_sig, "hash_ok": ok_hash, "sig_ok": ok_sig, "caminho": caminho}

    def recuperar(self, caminho):
        # devolve o conteudo original (decifra se preciso) apos verificar
        v = self.verificar(caminho)
        if not v["ok"]:
            return {"ok": False, "verificacao": v}
        with open(caminho, "r", encoding="utf-8") as f:
            reg = json.load(f)
        if reg.get("encrypted"):
            texto = Fernet(_fernet_key(self.chave)).decrypt(reg["payload"].encode("utf-8")).decode("utf-8")
        else:
            texto = reg["payload"]
        return {"ok": True, "conteudo": texto, "box": reg["box"], "origem": reg["origem"]}

    # ---------- EXTRAIR (varredura + dedup + selagem em lote) ----------
    def extrair(self, pasta_origem, box_id="00", extensoes=None):
        pasta_origem = os.path.expanduser(pasta_origem)
        resultado = {"selados": [], "duplicados": [], "erros": []}
        for raiz, _, arquivos in os.walk(pasta_origem):
            for nome in arquivos:
                if extensoes and not nome.lower().endswith(tuple(extensoes)):
                    continue
                fpath = os.path.join(raiz, nome)
                try:
                    with open(fpath, "r", encoding="utf-8", errors="replace") as f:
                        conteudo = f.read()
                    r = self.custodia(conteudo, box_id=box_id, origem=nome)
                    if r["status"] == "GO_SELADO":
                        resultado["selados"].append(nome)
                    else:
                        resultado["duplicados"].append(nome)
                except Exception as e:
                    resultado["erros"].append("{}: {}".format(nome, e))
        self._log("EXTRACAO pasta={} +{} sel / {} dup".format(
            pasta_origem, len(resultado["selados"]), len(resultado["duplicados"])))
        return resultado


# ---------------- TESTE HONESTO ----------------
if __name__ == "__main__":
    arq = Arquivista()
    print("Crypto disponivel:", _CRYPTO)

    r1 = arq.custodia("DADO_BRUTO_CONFIDENCIAL", box_id="00", origem="teste1")
    print("1o selo:", r1["status"], r1["hash"][:12])

    r2 = arq.custodia("DADO_BRUTO_CONFIDENCIAL", box_id="00", origem="teste1")
    print("2o selo (mesmo dado):", r2["status"], "<- dedup Stop/Go")

    v = arq.verificar(r1["caminho"])
    print("Verificacao integridade:", v["ok"], v)

    rec = arq.recuperar(r1["caminho"])
    print("Recuperado:", rec["conteudo"])