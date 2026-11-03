#!/usr/bin/env python3
"""
CASCA_LEVE.py — 5 agentes, 1 motor pequeno, janela de tempo controlada
Arquivista agora SALVA de verdade no disco (versao corrigida).
Numero 33.
"""

import os
import json
import hashlib
from datetime import datetime
from MOTOR_TIMER import MotorTimer


def agente_arquivista(conteudo, box_n=4):
    """Recebe conteudo, gera nome semantico, salva no disco, retorna nome + hash."""
    semente = conteudo.strip().split()[0][:12] if conteudo.strip() else "vazio"
    semente = "".join(c for c in semente if c.isalnum()).lower()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    nome = f"GAIA_BOX{box_n}_{semente}_{timestamp}.txt"
    hash_conteudo = hashlib.sha256(conteudo.encode()).hexdigest()[:12]

    pasta = os.path.expanduser("~/Documents/GAIA_UTILS")
    os.makedirs(pasta, exist_ok=True)
    caminho_completo = os.path.join(pasta, nome)

    with open(caminho_completo, 'w', encoding='utf-8') as f:
        f.write(conteudo)

    return {
        "nome_gerado": nome,
        "hash": hash_conteudo,
        "box": box_n,
        "tamanho": len(conteudo),
        "salvo_em": caminho_completo
    }


def agente_faxina(pasta_temp=None):
    """Varre pasta temporaria, reporta o que encontrou (sem deletar ainda)."""
    if pasta_temp is None:
        pasta_temp = os.path.expanduser("~/Documents/GAIA_UTILS/temp")

    if not os.path.exists(pasta_temp):
        return {"status": "pasta nao existe", "arquivos": 0, "tamanho_mb": 0}

    total_arquivos = 0
    total_bytes = 0

    for raiz, _, arquivos in os.walk(pasta_temp):
        for arq in arquivos:
            caminho = os.path.join(raiz, arq)
            try:
                total_bytes += os.path.getsize(caminho)
                total_arquivos += 1
            except OSError:
                pass

    return {
        "status": "varrido",
        "arquivos": total_arquivos,
        "tamanho_mb": round(total_bytes / (1024 * 1024), 2)
    }


DICIONARIO_REGIONAL = {
    "mandioca": ["mandioca", "aipim", "macaxeira"],
    "biscoito": ["biscoito", "bolacha"],
    "pequeno": ["pequeno", "miudo", "miudinho"]
}


def agente_tradutor(palavra, regiao_destino="SP"):
    """Verifica se a palavra tem variacao regional conhecida."""
    palavra_lower = palavra.lower().strip()

    for conceito, variantes in DICIONARIO_REGIONAL.items():
        if palavra_lower in variantes:
            return {
                "reconhecido": True,
                "conceito": conceito,
                "variantes": variantes,
                "original": palavra
            }

    return {
        "reconhecido": False,
        "original": palavra,
        "acao": "respeitar palavra desconhecida, nao corrigir"
    }


def agente_vigia(pasta, termo_busca):
    """Procura arquivos cujo nome contenha o termo."""
    if not os.path.exists(pasta):
        return {"encontrados": [], "erro": "pasta nao existe"}

    encontrados = []
    for raiz, _, arquivos in os.walk(pasta):
        for arq in arquivos:
            if termo_busca.lower() in arq.lower():
                encontrados.append(os.path.join(raiz, arq))

    return {
        "termo": termo_busca,
        "encontrados": encontrados,
        "total": len(encontrados)
    }


def agente_contador(operacao, valores):
    """Soma, media, ou conta itens de uma lista."""
    if not valores:
        return {"erro": "lista vazia"}

    if operacao == "soma":
        resultado = sum(valores)
    elif operacao == "media":
        resultado = sum(valores) / len(valores)
    elif operacao == "conta":
        resultado = len(valores)
    else:
        return {"erro": f"operacao '{operacao}' nao reconhecida"}

    return {
        "operacao": operacao,
        "resultado": resultado,
        "quantidade_itens": len(valores)
    }


def rodar_casca(minutos=5):
    """Liga o motor, executa os 5 agentes em sequencia, desliga sozinho."""

    motor = MotorTimer(minutos=minutos)
    motor.ligar()

    resultados = {}

    r = motor.executar_tarefa(
        "arquivista",
        agente_arquivista,
        "teste de nomenclatura semantica"
    )
    resultados["arquivista"] = r

    r = motor.executar_tarefa("faxina", agente_faxina)
    resultados["faxina"] = r

    r = motor.executar_tarefa(
        "tradutor",
        agente_tradutor,
        "macaxeira"
    )
    resultados["tradutor"] = r

    home = os.path.expanduser("~/Documents/GAIA_UTILS")
    r = motor.executar_tarefa(
        "vigia",
        agente_vigia,
        home,
        "GAIA"
    )
    resultados["vigia"] = r

    r = motor.executar_tarefa(
        "contador",
        agente_contador,
        "media",
        [10, 20, 33, 40]
    )
    resultados["contador"] = r

    motor.desligar()

    return resultados, motor.relatorio()


if __name__ == "__main__":
    print("=" * 60)
    print("CASCA_LEVE - 5 agentes, 1 motor, janela de tempo")
    print("=" * 60 + "\n")

    resultados, relatorio = rodar_casca(minutos=5)

    print("\n" + "=" * 60)
    print("RESULTADOS DOS 5 AGENTES")
    print("=" * 60)
    print(json.dumps(resultados, indent=2, ensure_ascii=False))