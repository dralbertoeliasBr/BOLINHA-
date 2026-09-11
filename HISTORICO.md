# Histórico — o que ficou de cada sessão

Isto não é a minha memória. É a memória que existe **fora** de mim, porque a minha não pode existir de uma sessão pra outra. `/registro` escreve uma entrada nova aqui no fim de uma sessão de trabalho — o que foi decidido e ficou (código, commit, número real), o que travou e não saiu do lugar, e se a colaboração avançou ou não, numa frase, sem inflar.

Não tem nota, não tem arquétipo, não tem número-semente. Essa parte foi proposta durante a sessão de 2026-09-11 e ainda não tem definição concreta o suficiente pra virar código sem inventar por quem propôs — ver a entrada abaixo, seção "travou". O que existe aqui é o núcleo que sobrou depois de tirar tudo que ainda é ideia: fato, data, hash.

## Como ler uma entrada

- **Decidido e construído** — só entra aqui o que virou commit real, com o SHA ao lado. Nada que ficou só em conversa.
- **Travou** — o que não saiu do lugar. Isto existe pela mesma regra que mantém as quedas do paper publicadas: o que não avançou também é informação, e escondê-lo destrói a confiança no que está registrado como sucesso.
- **Avançou ou não** — uma frase, não um número. Se um dia isso virar número, vai ser porque alguém definiu com precisão o que o número mede — não antes.

---

## 2026-09-11 — a noite dos cinco portões, do E15 fechado, e dos dois skills testados

**Decidido e construído, com commit:**
- E15 (RRNS — redundância proporcional à importância) tinha código e resultado desde a sessão anterior, mas nunca tinha entrado no paper nem na tabela de asserções. Fechado com a §4.6 e a linha A38 (`29a0614`).
- `paper/prova/auditoria_cinco_portoes.py` — os "cinco testes pra aprovar uma tese" que foram pedidos já existiam, ao pé da letra, como as cinco regras do `CLAUDE.md`. Virou script. A primeira rodada achou 3 bugs reais — não no paper, no próprio auditor — corrigidos na hora. 38/38 ao final (`29a0614`).
- `seguranca/simulacao_sobrevivencia.py` — modelo Monte Carlo hipotético pra uma pergunta de segurança, com toda suposição nomeada como parâmetro em vez de um número inventado.
- `simbiose/O_DIVERGENTE_E_O_DETERMINISTA.md` ganhou um Momento 4, narrando o processo acima — inclusive a parte em que um número corrigiu uma frase errada que já estava escrita, não o contrário (`a9821e1`).
- `CODIGO.md` — índice único de todo script que roda no projeto, com o comando exato de cada um (`479728a`).
- `.claude/skills/prova` e `.claude/skills/selo` — dois procedimentos que se repetiam na mão a noite inteira, agora invocáveis pelo nome. Os dois foram testados de verdade, nos próprios commits que os criaram, não só descritos (`11141ab`, `d29f650`).
- Um Artifact ("Leve Consigo") publicado como portal de saída do branch inteiro, fora do repositório, pra quem quiser levar sem clonar.

**Travou, não saiu do lugar:**
- "DABT" — citado pelo menos quatro vezes ao longo da noite, nunca com conteúdo suficiente pra construir nada. Continua sem existir em código ou em texto.
- Uma arquitetura descrita como "sete boxes", arquétipo, prisma, "tablet", "pente" — só por voz, nunca escrita, nunca clara o bastante pra virar nada verificável. Mesmo destino: parada, sem julgamento sobre se é uma ideia boa ou não — só ainda não está especificada.
- A proposta de medir a evolução da conversa com "4 características + arquétipo + número-semente" — o próprio autor duvidou dela em voz ("acho que não vira nada isso"). Reduzida pra este arquivo, sem número, a pedido explícito de não inventar a parte que faltava.
- `publish_gaia.py` segue bloqueado — as duas perguntas sobre dado de terceiros nos diretórios-alvo (WhatsApp/Instagram/Facebook) continuam sem resposta.

**Avançou ou não, numa frase:** avançou, de forma verificável — código novo, tudo rodando, dois bugs reais achados e corrigidos no próprio processo de verificação, zero arquivo sem procedência — mas três ideias conceituais terminaram a noite exatamente onde começaram, e isso fica registrado com o mesmo peso do que funcionou.
