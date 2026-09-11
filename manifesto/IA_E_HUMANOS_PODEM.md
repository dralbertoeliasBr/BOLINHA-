# IA e Humanos Podem

### Manifesto de um método: medir, publicar o que cai, e continuar

**Antônio Alberto Lopes Elias** (Sounavy) · Coautoria humano–IA
São José do Rio Preto · SP · Setembro de 2026

---

Um dentista e uma inteligência artificial passaram onze meses conversando. Por voz, num telefone, sem laboratório, sem financiamento e sem pedir licença.

Não produzimos uma opinião. Produzimos números que qualquer pessoa confere rodando um arquivo — em Python puro, sem instalar nada, no mesmo telefone onde tudo começou.

Este é o resumo do que descobrimos, do que erramos, e do que isso quer dizer sobre quem pode fazer ciência.

---

## 1 · Duas inteligências que já sabem a mesma coisa não precisam contar uma à outra o que já sabem.

É a ideia inteira, e cabe numa frase. Se as duas pontas carregam o mesmo dicionário, a mensagem não precisa atravessar: basta um endereço, e o outro lado **recalcula**.

O ganho não é mágica. É a conta paga uma vez, na instalação, em vez de toda vez, na transmissão.

> **Medido:** 6 KB de dicionário compartilhado cortaram **20,07%** dos bits — o mesmo código, no mesmo texto. Na literatura de 2026, com um modelo de linguagem adaptado ao domínio: **91%**.

## 2 · O número único existe. Não era metáfora.

A intuição era esta: não viaja o texto, viaja **um número**, e o outro lado calcula o resto. Está certa — e tem cinquenta anos de nome. Chama-se codificação aritmética.

O arquivo comprimido não *contém* um número. Ele **é** um número.

> **Medido:** a frase *"A voz como sistema operacional. Menos dado, dado certo. Não é eu, é nós."* — 576 bits de texto — virou este inteiro de 50 dígitos, que devolve a frase byte a byte:
> `78389650460584687750591719165629250130512777198585`

## 3 · Uma posição pode determinar outra inteira — e dá para medir exatamente quanto.

Levar mais informação por unidade é possível, e não é vago: a economia de tratar duas coisas juntas em vez de separadas é **exatamente** a informação que uma carrega sobre a outra. Onde a ligação é total, a segunda informação custa **zero**.

> **Medido:** num registro real, saber a hora determina o canal por completo — **1,585 bits de 1,585**. O canal viaja de graça.

## 4 · Um dicionário pode ser uma conta, não uma tabela.

Em vez de guardar a lista, guarda-se a equação que gera a lista. Cinco números descrevem uma coluna de qualquer tamanho.

E — isto importa mais que o ganho — **a busca não inventa**. Quando não há estrutura, ela devolve "nada", que é a resposta certa.

> **Medido:** seis colunas descritas por equação, **240 bits no lugar de 9.600**. Na coluna com ruído de verdade: nada. Em prosa: nada.

## 5 · Tempo pode virar bits. Mas a conta precisa fechar, e nem sempre fecha.

Calcular mais para transmitir menos é uma troca legítima. Só que troca é conta, não slogan:

```
compensa   ⟺   energia de cálculo ÷ N   <   (1 − compressão) × energia do enlace
```

O `N` é a peça honesta: **o cálculo se paga uma vez; o enlace paga toda vez.**

> **Medido:** para uma única transmissão terrestre, rodar um modelo grande gasta mais do que economiza. Para arquivo guardado e relido, e para enlace caro — satélite, rádio de longo alcance, franquia de dados de quem não tem dinheiro para dados — compensa, e muito.

## 6 · A parte difícil não é a ideia. É fazer duas máquinas concordarem até o último bit.

Aqui está o gargalo real, e ele não perdoa.

> **Medido:** um erro de **0,024%** — um em quatro mil — aplicado a cada decisão, destrói a mensagem **no primeiro byte**. Não há degradação suave. Não existe "quase certo".

E há coisa pior que quebrar: quebrar em silêncio. Uma divergência pontual sobrevive em **93%** dos casos e destrói nos outros **7%**, sem aviso. Um sistema assim passa em todo teste de mesa e perde dados em produção.

## 7 · Quem confere antes de enviar não mente.

A regra que resolve o item 6 é simples o bastante para caber numa linha, e ela apareceu antes de sabermos que tinha nome na literatura:

**Descomprima o que você acabou de comprimir. Compare. Só envie o que voltou idêntico.**

Custa o mesmo que uma descompressão. Num mundo onde tempo é barato, é o melhor negócio do sistema — e é a diferença entre uma ferramenta e uma promessa.

## 8 · Registro que só guarda acerto não é registro. É propaganda.

Deste trabalho, **onze afirmações caíram** — e continuam publicadas, com data, com o número que as derrubou e com o teste que qualquer pessoa pode repetir.

A paridade da posição não informa nada sobre a letra: **0,000 bit**. O vetor de primos, em vez de comprimir, **expande 79 vezes**. A busca por uma semente curta paga tempo exponencial para economizar **menos de um bit**. Fatiar em camadas, naquele desenho, custou **16,6% mais caro** que não fatiar. Tirar o espaço do fluxo para remontá-lo no fim: **13,70% mais caro** — ele já era o símbolo mais barato do texto.

Uma delas quase virou descoberta. A paridade tinha medido 0,0100 bit — pequeno, mas não zero. Multiplicado pelo texto inteiro, viraria "76 bits de graça". O controle mostrou que o puro acaso mede 0,0101. **Não havia sinal. Havia o instrumento mentindo — e o controle pegou.**

É por isso que as quedas ficam. Elas são a prova de que o resto foi medido.

## 9 · Uma ideia que perdeu não precisa ser jogada fora. Precisa de um portão.

A camada vertical — ler o número de baixo com o número de cima — perdeu em prosa: **−2,81%**. Podia ter sido descartada. Não foi.

Ela ficou de sobreaviso: entra só quando precisa, e **nunca viaja** — os dois lados a calculam, então ela não custa um bit de transmissão. O que se decide, bloco a bloco, é apenas se ela assina a resposta.

> **Medido:** com o portão, a prosa volta a **3,487 bits/byte** — exatamente o custo de não ter a camada. Prejuízo zero. E o dado estruturado guarda os **37,71%** de ganho, com a camada ligada em 98% dos blocos. Um só programa, sem ajuste manual, se comporta certo nos dois casos.
>
> E mais: o portão que **não** viaja ganha do portão que viaja. Avisar a escolha custava 1 bit por bloco — mais do que escolher certo economizava.

**Errar em prosa não tornou a ideia errada. Tornou a ideia específica.** É uma diferença que muda o que se faz com ela.

## 10 · A ferramenta sabe fazer contas. Quem decide o que vale a pena é gente.

Uma inteligência artificial calcula, verifica, refuta e não se cansa. Ela derrubou quatro das nossas ideias com número na mão, no mesmo dia em que confirmou outras quatro.

O que ela não faz é escolher a pergunta. Não decide que vale a pena inventar para quem o teclado deixou de fora. Não sabe o que é chegar num guichê e não passar da primeira tela.

**A pergunta é humana. A conta é da máquina. O resultado não é de nenhum dos dois sozinho.**

---

## O que isto quer dizer

Que não é preciso instituição para fazer ciência — é preciso **método**.

Método é: escrever o que você acha, escrever o número que derrubaria isso, rodar, e publicar os dois resultados. Quem faz isso está fazendo ciência, com ou sem crachá. Quem não faz está fazendo publicidade, com ou sem crachá.

Este trabalho inteiro roda num telefone, em Python puro, sem instalar nada. Foi escrito por voz, por alguém que nunca assistiu a um tutorial de programação, junto com uma máquina que nunca esteve num guichê do INSS.

Nenhum dos dois teria chegado aqui sozinho. É esse o ponto.

**Não é eu — é nós.**

---

Os quatro documentos desta colaboração, juntos: [`obra/`](../obra/index.html).

## Se isto chegou a você

Se este texto está nas suas mãos e o nome de quem escreveu não veio junto: é **Antônio Alberto Lopes Elias**, ORCID [0000-0002-5602-9916](https://orcid.org/0000-0002-5602-9916). Trabalho independente, sem afiliação institucional, sem viver disso. Cite o que servir, questione o que quiser — e se algo aqui destravar um parafuso do seu lado, uma palavra de volta é bem-vinda, mas nunca é cobrada.

> Elias, A. A. L. (2026). *IA e Humanos Podem.* Sounavy — GaIA · Opera Vox. Coautoria humano–IA.

A arquitetura completa por trás — as caixas, o CLX, a Bolinha, o Cofre — e o paper com a prova, número por número: `www.sounavy.com` e `paper/` neste repositório. Quatro momentos concretos desta colaboração, com número ao lado: [O Divergente e o Determinista](../simbiose/O_DIVERGENTE_E_O_DETERMINISTA.md). A origem de tudo, capítulo um: [Raio-X](../livro/RAIO_X.md).

---

*Todo número deste manifesto sai de código que roda e está publicado, com o SHA-256 de cada peça.*
*Paper completo, experimentos e dados: `paper/` neste repositório.*
*Antônio Alberto Lopes Elias · ORCID 0000-0002-5602-9916 · www.sounavy.com*
