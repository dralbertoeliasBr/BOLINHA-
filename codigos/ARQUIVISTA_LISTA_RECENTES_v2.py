#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ARQUIVISTA_LISTA_RECENTES_v2.py  (v2, 02/11/2026) - v1 continua intacta
# Conceito: Sounavy. Codigo: Claude. Arquivo novo, nao mexe em nada.
# O que faz: procura tudo que os Arquivistas gravaram no iPhone e lista
# do MAIS NOVO para o mais antigo. So le. Nao apaga, nao move, nao altera.
# Uso: copiar, colar no Pythonista e apertar Play.

import os, json, re
from datetime import datetime

MOSTRAR = 40   # quantos itens aparecem na tela (mude se quiser)

HOME = os.path.expanduser("~")
DOCS = os.path.join(HOME, "Documents")

# Pastas conhecidas de cada Arquivista
CONHECIDAS = [
    os.path.join(DOCS, "ARQUIVISTA_CORE"),   # Arquivista Core v1 (HMAC)
    os.path.join(DOCS, "Arquivos_Gaia"),     # ArquivistaSSRD v1.2 Enclave
    os.path.join(HOME, "MAESTRO"),           # Maestria
    os.path.join(DOCS, "MAESTRO"),
    os.path.join(DOCS, "Arquivista"),
    os.path.join(DOCS, "Arquivos_Gaia_Soberana"),  # GaiaRecuperacao
    os.path.join(DOCS, "DOCA_PRISMA"),             # Prisma v1.0
    os.path.join(DOCS, "SSRD"),                    # Enclave SSRD + Llama
]
# arquivos soltos que as versoes de camadas gravam na pasta onde rodam
SOLTOS = ("memoria_arquitetura.json", "vocabulario_nativo.json", "fila_camada3.json", "vault.jsonl", "violet_box.txt")
PISTAS = ("arquiv", "ssrd", "gaia", "maestr", "box", "violet", "vault", "rastro", "prisma", "doca", "delta")
EXTS = (".json", ".jsonl", ".log", ".txt", ".enc")
PULAR = ("site-packages", ".Trash", "__pycache__")


def achar_pastas():
    vistas = []
    for p in CONHECIDAS:
        if os.path.isdir(p):
            vistas.append(os.path.realpath(p))
    # varre Documents por pastas com nome de Arquivista (pega versoes perdidas)
    base = DOCS if os.path.isdir(DOCS) else HOME
    for raiz, dirs, _ in os.walk(base):
        dirs[:] = [d for d in dirs if not any(x in d for x in PULAR)]
        for d in dirs:
            if any(k in d.lower() for k in PISTAS):
                vistas.append(os.path.realpath(os.path.join(raiz, d)))
        if raiz.count(os.sep) - base.count(os.sep) >= 3:
            dirs[:] = []
    # tira repetidas e as que estao dentro de outra ja listada
    vistas = sorted(set(vistas))
    finais = []
    for v in vistas:
        if not any(v.startswith(f + os.sep) for f in finais):
            finais.append(v)
    return finais


def ler_detalhe(caminho):
    """Tira do arquivo: caixa, hash curto e se esta cifrado (sem decifrar)."""
    box, selo, cifrado = "", "", ""
    if caminho.endswith(".json"):
        try:
            with open(caminho, "r", encoding="utf-8") as f:
                r = json.load(f)
            if isinstance(r, dict):
                box = str(r.get("box") or r.get("nivel") or "")
                selo = str(r.get("hash_sha256") or r.get("hash") or "")[:12]
                if "encrypted" in r:
                    cifrado = "cifrado" if r.get("encrypted") else "aberto"
                elif "violeta" in r:
                    cifrado = "violeta" if r.get("violeta") else ""
        except Exception:
            pass
    if not box:
        m = re.search(r"BOX_(\d\d)", caminho)
        if m:
            box = m.group(1)
    return box, selo, cifrado


def data_no_nome(nome):
    """Arquivos do Core tem a data no nome: 20261102_211800_xxxx.json"""
    m = re.match(r"(\d{8})_(\d{6})_", nome)
    if m:
        try:
            return datetime.strptime(m.group(1) + m.group(2), "%Y%m%d%H%M%S")
        except ValueError:
            return None
    return None


def coletar(pastas):
    itens = []
    for p in pastas:
        for raiz, dirs, arqs in os.walk(p):
            dirs[:] = [d for d in dirs if not any(x in d for x in PULAR)]
            for a in arqs:
                if not a.lower().endswith(EXTS) or a in ("last_hash.txt", "_index.json", "_manifesto.log"):
                    continue
                c = os.path.join(raiz, a)
                try:
                    st = os.stat(c)
                except OSError:
                    continue
                quando = data_no_nome(a) or datetime.fromtimestamp(st.st_mtime)
                box, selo, cif = ler_detalhe(c)
                itens.append({"quando": quando, "caminho": c, "nome": a,
                              "pasta": os.path.relpath(raiz, HOME),
                              "kb": st.st_size / 1024, "box": box,
                              "selo": selo, "cif": cif})
    for base in (DOCS, HOME):
        for a in SOLTOS:
            c = os.path.join(base, a)
            if os.path.isfile(c) and not any(i["caminho"] == c for i in itens):
                st = os.stat(c)
                itens.append({"quando": datetime.fromtimestamp(st.st_mtime), "caminho": c, "nome": a,
                              "pasta": os.path.relpath(base, HOME), "kb": st.st_size / 1024,
                              "box": "", "selo": "", "cif": ""})
    itens.sort(key=lambda x: x["quando"], reverse=True)   # MAIS NOVO EM CIMA
    return itens


def manifesto(pastas):
    linhas = []
    for p in pastas:
        m = os.path.join(p, "_manifesto.log")
        if os.path.exists(m):
            try:
                with open(m, "r", encoding="utf-8", errors="replace") as f:
                    linhas += [l.strip() for l in f if l.strip()]
            except OSError:
                pass
    linhas.sort(reverse=True)   # a linha comeca com a data ISO
    return linhas


def main():
    pastas = achar_pastas()
    print("=" * 46)
    print(" ARQUIVISTA  -  o mais novo em cima")
    print(" " + datetime.now().strftime("%d/%m/%Y %H:%M"))
    print("=" * 46)
    if not pastas:
        print("Nenhuma pasta de Arquivista encontrada em", DOCS)
        print("Rode o Arquivista uma vez e tente de novo.")
        return
    print("Pastas lidas:")
    for p in pastas:
        print("  -", os.path.relpath(p, HOME))

    itens = coletar(pastas)
    print("\n{} arquivo(s). Mostrando {}:\n".format(len(itens), min(MOSTRAR, len(itens))))
    for i, it in enumerate(itens[:MOSTRAR], 1):
        extra = " | ".join(x for x in (
            ("box " + it["box"]) if it["box"] else "",
            it["selo"], it["cif"]) if x)
        print("{:>2}. {}  {}".format(i, it["quando"].strftime("%d/%m/%Y %H:%M:%S"), it["nome"]))
        print("    {}  ({:.1f} KB){}".format(it["pasta"], it["kb"], ("  " + extra) if extra else ""))

    man = manifesto(pastas)
    if man:
        print("\nManifesto (ultimas 15 operacoes, mais nova em cima):")
        for l in man[:15]:
            print("  " + l)

    # guarda a lista num arquivo NOVO, com data no nome (nao sobrescreve nada)
    nome = "lista_arquivista_{}.txt".format(datetime.now().strftime("%Y%m%d_%H%M%S"))
    saida = os.path.join(DOCS if os.path.isdir(DOCS) else HOME, nome)
    try:
        with open(saida, "w", encoding="utf-8") as f:
            for it in itens:
                f.write("{}\t{}\t{}\n".format(it["quando"].isoformat(), it["box"], it["caminho"]))
        print("\nLista completa salva em:", os.path.relpath(saida, HOME))
    except OSError as e:
        print("\nNao consegui salvar a lista:", e)


if __name__ == "__main__":
    main()
