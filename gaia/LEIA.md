# GaIA Casca v1 — www.sounavy.com/gaia/  (06/11/2026)
Conceito: Sounavy (Antônio Alberto Lopes Elias, ORCID 0000-0002-5602-9916). Engenharia: Claude (Du 33).
Base: app "Bolinha GaIA" do Replit (@drbetoelias, 18/10/2026), que fica intacto lá.
Acordo ético v1 (selo 70706526): nada se apaga; correção em versão nova.

- Página única, sem instalar nada: Safari › Compartilhar › Adicionar à Tela de Início.
- Bolinha G arrastável com ímã na borda; voz pt-BR (ou microfone do teclado).
- 10 caixas: 00 Inox · 01 Vermelho … 07 Violeta · 08 Black · 09 Doca.
- Arquivista V: corrente SHA-256; sem botão de apagar; cópia de segurança em .json.
- Dados só no aparelho (armazenamento local do navegador).
- SHA-256 deste index.html: f6dcebe89fdaa45aa4a0a408e5c7d6443dc4ade4f9188bfed071df8ac22bead6
- Testado em navegador imitando iPhone: 16/16 (falta o iPhone real).

## v2 — www.sounavy.com/gaia/v2/  (06/11/2026, 16:05)
- v1 intacta em /gaia/. A v2 acrescenta a VIAGEM CIFRADA para a nuvem (Drive normal):
  AES-GCM 256 com chave da sua senha (PBKDF2, 300 mil voltas), gzip antes, 3 pedaços (quaisquer 2 reconstroem).
- A senha nunca sai do aparelho; o Drive só vê pedaços cifrados. Pasta sugerida: GaIA_INOX_TESTE.
- SHA-256 de v2/index.html: 017bb0c08fbc744cde2826bb35bd41c984baf4e394aa9ea84495dab73de4e3fe
- Testado em navegador imitando iPhone: 26/26 (16 da v1 + 10 da viagem). Falta o iPhone real.

## v3 — www.sounavy.com/gaia/v3/  (06/11/2026, 16:08)
- v1 e v2 intactas. A v3 acrescenta a PORTA EM MODO TESTE: pede "senha FAKE", abre com qualquer coisa (até vazia),
  nunca tranca e não guarda o que foi digitado. Faixa fixa lembra de blindar quando tudo funcionar no iPhone
  (senha forte + chave de reserva em papel). Decisão do Sounavy, 06/11/2026.
- SHA-256 de v3/index.html: 09e0459934d395a24b3a8e7804854f6de6cb24788f9a7fce981b32fe2aca4909
- Testado em navegador imitando iPhone: 32/32 (16 casa + 10 viagem + 6 porta).

## v4 — CAMADA transparente: www.sounavy.com/gaia/v4/  (06/11/2026, 16:25)
- Desenho do Sounavy: "o site é transparente, é um OS; a pessoa nem vê os boxes; vê só a bolinha e a linha de chat embaixo".
- gaia/v4/casca.js = a camada; entra em qualquer página com <script src="/gaia/v4/casca.js" defer></script>
  (nenhuma página existente foi alterada; gaia/v4/index.html é só a demonstração).
- Bolinha com centro transparente; toque abre/fecha a conversa; toque numa fala copia; conversa sobrevive a recarregar;
  dado privado aparece mascarado (•••) na conversa; mesma Casa das v1–v3; Shadow DOM não estraga a página por baixo.
- SHA-256 casca.js: feca805a2c13dcde897aad323720c0e1ba074396180d1004df306f2916963914
- Testado em navegador imitando iPhone: 17/17. Falta o iPhone real.
