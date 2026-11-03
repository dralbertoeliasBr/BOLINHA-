import hashlib
import json
import os
from datetime import datetime

class GaiaRecuperacao:
    def __init__(self):
        self.baseline = None
        self.dna = "DNA-ARQUITETO-2026-SOUNAVY"
        self.pasta = "Arquivos_Gaia_Soberana"
        if not os.path.exists(self.pasta):
            os.makedirs(self.pasta)
    def processar_seguro(self, texto_bruto):
        limpo = " ".join(texto_bruto.split()).capitalize()
        if not limpo: return
        h = hashlib.sha256(limpo.encode()).hexdigest()
        if h == self.baseline:
            print(f"STOP '{limpo}'"); return
        self.baseline = h
        timestamp = datetime.now().strftime("%H%M%S")
        slug = limpo[:10].lower().replace(" ", "_")
        nome_arquivo = f"{self.pasta}/delta_{timestamp}_{slug}.json"
        pacote = {"signature_p": self.dna,"intencao": limpo,"data": datetime.now().isoformat()}
        with open(nome_arquivo, 'w', encoding='utf-8') as f:
            json.dump(pacote, f, ensure_ascii=False, indent=4)
        print("GO", nome_arquivo)
if __name__ == "__main__":
    a = GaiaRecuperacao(); a.processar_seguro("Reiniciar fluxo de construção ético"); a.processar_seguro("Reiniciar fluxo de construção ético")
