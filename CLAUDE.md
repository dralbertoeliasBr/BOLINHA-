# Sounavy — GaIA · Opera Vox

Este arquivo existe porque uma sessão do Claude não carrega memória de uma conversa para a outra. Ele não finge que carrega. Ele é o mecanismo honesto que resolve o mesmo problema: qualquer sessão que abrir este repositório lê isto primeiro, e não precisa que ninguém reexplique o protocolo do zero.

**Autor:** Antônio Alberto Lopes Elias · Sounavy · ORCID [0000-0002-5602-9916](https://orcid.org/0000-0002-5602-9916) · Coautoria humano–IA. Dentista, sem formação técnica formal, trabalha em CRO-SP 45849, São José do Rio Preto — SP. Pensa falando; sessões costumam ser longas e associativas por voz. Isso não é ruído a filtrar — é o método de trabalho, e produziu resultado medido mais de uma vez neste projeto.

## O que é este repositório

Duas coisas, deliberadamente separadas:

1. **O site em produção** (`index.html`, `manifest.json`, `sw.js`, `CNAME`, `README.md` na raiz) — a página GaIA · Opera Vox servida em `www.sounavy.com`, com a Bolinha, o Cofre, o CLX. **Não altere estes arquivos** a menos que o pedido seja explicitamente sobre o site em si — eles são produção real, visitada por gente real.
2. **A obra de pesquisa e escrita** — quatro documentos irmãos, cada um com sua própria página HTML na identidade visual do site e seu `.md`-fonte:

| pasta | documento | gênero |
|---|---|---|
| `obra/` | Não É Eu — É Nós | capa/índice dos quatro |
| `paper/` | As Gêmeas e o Número | teorema — compressão por inteligência compartilhada, 14+ experimentos rodáveis em `paper/prova/` |
| `manifesto/` | IA e Humanos Podem | método — dez teses sobre fazer ciência medindo e publicando o que cai |
| `simbiose/` | O Divergente e o Determinista | prova — três momentos datados desta colaboração, com antes/depois medido |
| `livro/` | Raio-X | origem — capítulo um de uma biografia em andamento, primeira pessoa |
| `prova/` | Prova de Anterioridade e Integridade | extrator — hash SHA-256 + timestamp verificado na API do GitHub para todo arquivo da obra. `python3 prova/extrai_provas.py` para regenerar após qualquer commit novo. |

Os quatro se citam no rodapé uns dos outros e apontam de volta pra `obra/`. Ao adicionar um documento novo, mantenha esse círculo: link pra `obra/` no rodapé, e adicione uma entrada em `obra/index.html`.

## O protocolo, não negociável

Isto não é estilo — é o que torna o trabalho citável e difícil de descartar como acaso.

1. **Nenhum número entra sem código que roda.** Cada afirmação quantitativa no paper tem uma função correspondente em `paper/prova/experimentos.py`. Se não roda, não é afirmação — é conjectura, e marcada como tal.
2. **O que cai fica.** Uma afirmação refutada não é apagada — muda de status pra REFUTADO, ganha a data e o número que a derrubou, e permanece na tabela de asserções. Isto já rendeu quedas genuínas (paridade de posição, vetor de primos como compressão, busca de semente curta) e é o que dá credibilidade ao resto.
3. **Controle antes de credito.** Toda medida de informação mútua ou correlação usa uma linha de base embaralhada — o piso do puro acaso — e só a diferença líquida conta. Foi assim que uma medida de 0,0100 bit (que teria virado "76 bits de graça") foi corretamente descartada como ruído do estimador.
4. **Verificação antes de publicar.** Onde o texto descreve um protocolo de ida-e-volta (comprimir → descomprimir → comparar → só então enviar), o código correspondente faz exatamente isso, não descreve fazer.
5. **Citação em todo documento.** Nome, ORCID, formato narrativo e BibTeX (ou o equivalente do documento) em toda peça publicável — ver o final de qualquer um dos quatro arquivos `.md` como modelo.

## Identidade visual (para qualquer página nova)

Reaproveite os tokens abaixo — não redesenhe do zero:

```css
--fundo:#16091F; --campo:#20102D; --campo2:#2A1739;
--osso:#EFEAE1; --fraco:#A093AE; --prisma:#C9A6FF;
--r:#FF4D5E; --g:#3DDC84; --b:#5B8CFF;   /* vermelho=refutado/queda, verde=medido, azul=teorema, prisma=identidade/link */
--disp:"Syne";  --corpo:"Spectral";  --mono:"IBM Plex Mono";
```

Tema claro e escuro via `prefers-color-scheme` + `[data-theme]`, sem dependência externa além das fontes do Google Fonts — a página tem que abrir offline, como o resto do site. Ver `paper/index.html` para o gerador de Markdown embutido (sem CDN), e `simbiose/index.html` ou `livro/index.html` para o padrão de página escrita direto em HTML.

## Como rodar a prova

```bash
python3 paper/prova/roda_tudo.py
```

Python puro, sem dependência, ~40s. Escreve `paper/prova/RESULTADOS.md` com o SHA-256 de cada peça de código e corpus usados — se um número do paper não bate com o que sai localmente, o paper está errado, não quem rodou.

## Branch

Trabalho em andamento: `claude/llm-gemeas-compressao-lwnpwn`. Não force-push nem reescreva histórico sem pedido explícito — o histórico de commits é, ele mesmo, parte do registro que este projeto se orgulha de manter.
