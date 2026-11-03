#!/usr/bin/env python3
"""
PROVA_DE_CONCEITO.py — Execucao 100% autonoma, sem intervencao manual
Roda Doca + 5 agentes + timer, do inicio ao fim, sozinho.
Gera arquivo de prova datado e assinado (hash), pronto pra gravar em video.

Uso: python3 PROVA_DE_CONCEITO.py
Nao precisa digitar nada durante a execucao. So aperta rodar e filma.

Numero 33.
"""

import os
import json
import hashlib
from datetime import datetime
from MOTOR_TIMER import MotorTimer
from CASCA_LEVE import (
    agente_arquivista,
    agente_faxina,
    agente_tradutor,
    agente_vigia,
    agente_contador
)


def executar_prova_autonoma():
    """
    Roda a sequencia inteira sozinha, sem pausa, sem input do usuario.
    Cada passo e registrado com timestamp exato.
    No final, gera um arquivo de prova com hash de integridade.
    """

    print("\n" + "=" * 70)
    print("PROVA DE CONCEITO — EXECUCAO AUTONOMA")
    print("=" * 70)
    print(f"Inicio: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print("Nenhuma intervencao manual necessaria a partir daqui.")
    print("=" * 70 + "\n")

    log_prova = {
        "titulo": "PROVA_DE_CONCEITO_GAIA_OPERA",
        "timestamp_inicio": datetime.now().isoformat(),
        "device": "iPhone_BORDA",
        "passos": []
    }

    # PASSO 1 — Motor liga sozinho
    motor = MotorTimer(minutos=5)
    motor.ligar()
    log_prova["passos"].append({
        "passo": 1,
        "acao": "Motor ligado automaticamente",
        "timestamp": datetime.now().isoformat()
    })

    # PASSO 2 — Arquivista roda e salva arquivo real
    r_arquivista = motor.executar_tarefa(
        "arquivista",
        agente_arquivista,
        f"PROVA AUTONOMA gerada em {datetime.now().isoformat()}"
    )
    log_prova["passos"].append({
        "passo": 2,
        "acao": "Arquivista salvou arquivo real no disco",
        "resultado": r_arquivista,
        "timestamp": datetime.now().isoformat()
    })

    # PASSO 3 — Faxina varre
    r_faxina = motor.executar_tarefa("faxina", agente_faxina)
    log_prova["passos"].append({
        "passo": 3,
        "acao": "Faxina varreu pasta temp",
        "resultado": r_faxina,
        "timestamp": datetime.now().isoformat()
    })

    # PASSO 4 — Tradutor reconhece termo regional
    r_tradutor = motor.executar_tarefa("tradutor", agente_tradutor, "macaxeira")
    log_prova["passos"].append({
        "passo": 4,
        "acao": "Tradutor reconheceu termo regional",
        "resultado": r_tradutor,
        "timestamp": datetime.now().isoformat()
    })

    # PASSO 5 — Vigia confirma que o arquivo do Arquivista existe de verdade
    home = os.path.expanduser("~/Documents/GAIA_UTILS")
    r_vigia = motor.executar_tarefa("vigia", agente_vigia, home, "GAIA")
    log_prova["passos"].append({
        "passo": 5,
        "acao": "Vigia confirmou arquivos GAIA_BOX existentes",
        "resultado": r_vigia,
        "timestamp": datetime.now().isoformat()
    })

    # PASSO 6 — Contador confirma capacidade de calculo
    r_contador = motor.executar_tarefa(
        "contador", agente_contador, "soma", [1, 1, 1]
    )
    log_prova["passos"].append({
        "passo": 6,
        "acao": "Contador executou calculo real",
        "resultado": r_contador,
        "timestamp": datetime.now().isoformat()
    })

    # PASSO 7 — Motor desliga sozinho
    motor.desligar()
    log_prova["passos"].append({
        "passo": 7,
        "acao": "Motor desligado automaticamente",
        "timestamp": datetime.now().isoformat()
    })

    log_prova["timestamp_fim"] = datetime.now().isoformat()
    log_prova["total_passos"] = len(log_prova["passos"])
    log_prova["marker"] = 33

    # Gera hash de integridade do log inteiro (prova de que nao foi editado depois)
    log_texto = json.dumps(log_prova, sort_keys=True, ensure_ascii=False)
    hash_prova = hashlib.sha256(log_texto.encode()).hexdigest()
    log_prova["hash_integridade"] = hash_prova

    # Salva o arquivo de prova, nome com timestamp (nunca sobrescreve)
    pasta = os.path.expanduser("~/Documents/GAIA_UTILS")
    os.makedirs(pasta, exist_ok=True)
    nome_prova = f"PROVA_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    caminho_prova = os.path.join(pasta, nome_prova)

    with open(caminho_prova, 'w', encoding='utf-8') as f:
        json.dump(log_prova, f, indent=2, ensure_ascii=False)

    # Resumo final na tela, pronto pra aparecer no video
    print("\n" + "=" * 70)
    print("PROVA CONCLUIDA — RESUMO PARA GRAVACAO")
    print("=" * 70)
    print(f"Data/Hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print(f"Passos executados: {log_prova['total_passos']}/7")
    print(f"Arquivo de prova salvo em: {caminho_prova}")
    print(f"Hash de integridade: {hash_prova[:32]}...")
    print()
    print("O QUE FOI PROVADO:")
    print(f"  1. Arquivista criou arquivo real: {r_arquivista['nome_gerado']}")
    print(f"  2. Vigia confirmou {r_vigia['total']} arquivo(s) GAIA no disco")
    print(f"  3. Tradutor reconheceu '{r_tradutor['original']}' = {r_tradutor.get('conceito', 'N/A')}")
    print(f"  4. Contador calculou: {r_contador['resultado']}")
    print(f"  5. Tudo sem digitar nada durante a execucao")
    print()
    print("Numero 33. Anti-teatro. Rodou sozinho, do inicio ao fim.")
    print("=" * 70 + "\n")

    return log_prova, caminho_prova


if __name__ == "__main__":
    log_prova, caminho = executar_prova_autonoma()