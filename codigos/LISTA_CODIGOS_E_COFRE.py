#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# LISTA_CODIGOS_E_COFRE.py  (v1, 02/11/2026)
# Conceito: Sounavy. Codigo: Claude. Arquivo novo, nao mexe em nada.
#
# 1) Lista TODOS os seus codigos (.py, .html, .js, .sh) do Pythonista,
#    do MAIS NOVO para o mais antigo. Uma linha por codigo.
# 2) Faz um COFRE: copia todos eles para um .zip novo com data no nome.
#    Se algum codigo for apagado de novo, a copia continua no zip.
#    Nada e apagado, movido ou alterado.
# Uso: copiar, colar no Pythonista e apertar Play.

import os, zipfile, hashlib
from datetime import datetime

HOME = os.path.expanduser("~")
DOCS = os.path.join(HOME, "Documents")
BASE = DOCS if os.path.isdir(DOCS) else HOME

TIPOS = (".py", ".html", ".js", ".sh", ".pyui")
PULAR = ("site-packages", "node_modules", ".Trash", "__pycache__", ".git",
         "COFRE_CODIGOS")   # nao lista os proprios cofres
COFRE_DIR = os.path.join(BASE, "COFRE_CODIGOS")


def achar_codigos():
    cods = []
    for raiz, dirs, arqs in os.walk(BASE):
        dirs[:] = [d for d in dirs if not any(p in d for p in PULAR)]
        for a in arqs:
            if a.lower().endswith(TIPOS):
                c = os.path.join(raiz, a)
                try:
                    st = os.stat(c)
                except OSError:
                    continue
                cods.append((st.st_mtime, st.st_size, c))
    cods.sort(reverse=True)          # MAIS NOVO EM CIMA
    return cods


def selo(caminho):
    h = hashlib.sha256()
    with open(caminho, "rb") as f:
        for bloco in iter(lambda: f.read(65536), b""):
            h.update(bloco)
    return h.hexdigest()


def main():
    agora = datetime.now()
    cods = achar_codigos()
    print("=" * 46)
    print(" SEUS CODIGOS - o mais novo em cima")
    print(" " + agora.strftime("%d/%m/%Y %H:%M"))
    print("=" * 46)
    print("{} codigo(s) encontrados.\n".format(len(cods)))

    linhas = []
    for i, (mt, tam, c) in enumerate(cods, 1):
        quando = datetime.fromtimestamp(mt).strftime("%d/%m/%Y %H:%M")
        rel = os.path.relpath(c, BASE)
        print("{:>3}. {}  {}".format(i, quando, rel))
        linhas.append((quando, tam, rel, c))

    # ---- cofre: zip novo, nunca sobrescreve ----
    os.makedirs(COFRE_DIR, exist_ok=True)
    nome_zip = "cofre_codigos_{}.zip".format(agora.strftime("%Y%m%d_%H%M%S"))
    caminho_zip = os.path.join(COFRE_DIR, nome_zip)
    n = 2
    while os.path.exists(caminho_zip):      # nunca sobrescreve um cofre
        caminho_zip = os.path.join(COFRE_DIR, nome_zip.replace(".zip", "_{}.zip".format(n)))
        n += 1
    indice = ["data\ttamanho\tsha256\tcaminho"]
    ok = 0
    with zipfile.ZipFile(caminho_zip, "w", zipfile.ZIP_DEFLATED) as z:
        for quando, tam, rel, c in linhas:
            try:
                s = selo(c)
                z.write(c, arcname=rel)
                indice.append("{}\t{}\t{}\t{}".format(quando, tam, s, rel))
                ok += 1
            except Exception as e:
                indice.append("{}\t{}\tERRO\t{}  ({})".format(quando, tam, rel, e))
        z.writestr("_INDICE_mais_novo_em_cima.txt", "\n".join(indice))

    # confere o cofre: abre o zip e testa cada arquivo
    with zipfile.ZipFile(caminho_zip) as z:
        ruim = z.testzip()
    print("\nCOFRE: {} de {} codigos copiados.".format(ok, len(linhas)))
    print("Conferencia do zip:", "OK" if ruim is None else "FALHOU em " + ruim)
    print("Guardado em:", os.path.relpath(caminho_zip, HOME))
    print("Dica: mande esse .zip para o iCloud ou Drive (Compartilhar > Salvar em Arquivos).")


if __name__ == "__main__":
    main()
