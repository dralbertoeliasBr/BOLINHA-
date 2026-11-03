import os, json, hashlib
class ArquivistaPrisma:
    def __init__(self):
        self.base = os.path.expanduser("~/Documents/DOCA_PRISMA")
        self.indices = [f"BOX_{i:02d}_DOURADO" for i in range(1, 8)]
        self.box_preto = "BOX_00_PRETO"
        for b in self.indices + [self.box_preto]:
            os.makedirs(f"{self.base}/{b}", exist_ok=True)
    def custodia(self, payload, box_id="preto"):
        target = self.box_preto if box_id == "preto" else self.indices[int(box_id)-1]
        h = hashlib.sha256(str(payload).encode()).hexdigest()[:12]
        with open(f"{self.base}/{target}/{h}.json", 'w') as f:
            json.dump({"data": payload, "sig": "ARQUITETO"}, f)
        return h
p=ArquivistaPrisma(); h=p.custodia("DNA_LEGADO_SOUNAVY_FREQ_432","preto"); print("selado",h)
print("conteudo no disco:", open(f"{p.base}/BOX_00_PRETO/{h}.json").read())
