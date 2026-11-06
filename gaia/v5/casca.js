/*
  GaIA Casca v5 — CAMADA (overlay)   (06/11/2026)  — v4 + o que era bom na versao do agente do Replit:
   (1) "copia" baixa a copia de seguranca so depois de perguntar "tem certeza?" e avisar que a Black vai junto sem cifra;
   (2) repetido e conferido sem acento e sem maiuscula ("Pão" = "pao");
   (3) mais dado privado: cartao de 13 a 19 digitos, celular com +55;
   (4) bolinha respeita o entalhe e as bordas do iPhone (area segura);
   (5) acessibilidade: contorno de foco visivel e menos movimento para quem pede.
  O que NAO foi trazido: caixas na tela (contra o desenho), "cartao" sozinho como privado (exagero), Casa separada.
  Usar:  <script src="/gaia/v5/casca.js" defer></script>   (v1..v4 intactas)

  GaIA Casca v4 — CAMADA (overlay) para qualquer pagina do sounavy.com   (06/11/2026)
  Conceito: Sounavy (Antonio Alberto Lopes Elias, ORCID 0000-0002-5602-9916): "o site e transparente, e um OS;
  a pessoa nem ve os boxes; ve so a bolinha e a linha de chat embaixo, minimizada".
  Engenharia: Claude. Acordo etico v1 (selo 70706526): nada se apaga; versao nova em arquivo novo (v1..v3 intactas).

  Como usar numa pagina:  <script src="/gaia/v4/casca.js" defer></script>
  - Bolinha G meio transparente no centro (da para ler atras), arrastavel, gruda na borda (ima), lembra a posicao.
  - Linha de chat minimizada embaixo (fala pelo microfone do teclado ou do navegador).
  - Toque na bolinha: abre/fecha a conversa. Toque numa fala: COPIA (aparece "copiado").
  - Conversa e Casa ficam gravadas no aparelho: se a pagina piscar/recarregar, volta igual.
  - Mesma Casa das v1..v3 (mesma chave), mesmas 10 caixas, Arquivista V com corrente SHA-256, sem botao de apagar.
  - Tudo isolado (Shadow DOM): nao estraga o visual da pagina por baixo.
*/
(function () {
  "use strict";
  if (window.__gaiaCasca) return;                       // so uma camada por pagina
  const CHAVE = "gaia.casca.v1.ledger", POS = "gaia.casca.v4.orb", CONV = "gaia.casca.v4.conversa";   // mesma Casa e conversa da v4
  const mem = {};
  const ler = k => { try { return localStorage.getItem(k); } catch (e) { return mem[k] ?? null; } };
  const gravar = (k, v) => { try { localStorage.setItem(k, v); } catch (e) { mem[k] = v; } };

  /* ---------- Casa (igual v1..v3) ---------- */
  const CAIXAS = { "00": ["Inox", "quarentena"], "01": ["Vermelho", "projetos"], "02": ["Laranja", "licenciáveis"],
    "03": ["Amarelo", "trabalho"], "04": ["Verde", "rotinas"], "05": ["Azul", "memórias"], "06": ["Anil", "reservada"],
    "07": ["Violeta", "código"], "08": ["Black", "privado"], "09": ["Doca", "diário"] };
  const PALAVRA_CAIXA = { vermelho: "01", vermelha: "01", red: "01", projeto: "01", laranja: "02", amarelo: "03", amarela: "03",
    trabalho: "03", verde: "04", azul: "05", anil: "06", violeta: "07", codigo: "07", black: "08", preta: "08", preto: "08",
    privado: "08", segredo: "08", doca: "09" };
  const PRIVADO = [/\b\d{3}\.?\d{3}\.?\d{3}-\d{2}\b/, /\b(?:\d[ -]?){13,19}\b/, /[\w.+-]+@[\w-]+\.[\w.]+/,
    /(?:\+55\s*)?\(?\b\d{2}\)?\s?9\d{4}[-.\s]?\d{4}\b/, /\bsenha\b/i, /\bpaciente\b/i, /\bprontu[aá]rio\b/i, /\blaudo\b/i, /\bpix\b/i, /\btoken\b/i];
  const PROJETO = /\b(projeto|gaia|enclave|livro|tese|cap[ií]tulo|cl[ií]nica|ideia|manifesto|zenodo)\b/i;
  const semAcento = t => t.normalize("NFD").replace(/[̀-ͯ]/g, "").toLowerCase();
  const privado = t => PRIVADO.some(r => r.test(t));
  function classificar(t) {
    if (privado(t)) return ["08", "tem dado privado"];
    if (/(^|\n)\s*(def |class |import |function |const |<html)/i.test(t)) return ["07", "é código"];
    if (PROJETO.test(t)) return ["01", "fala de projeto"];
    return ["03", "texto geral"];
  }
  async function sha256(txt) {
    const h = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(txt));
    return [...new Uint8Array(h)].map(x => x.toString(16).padStart(2, "0")).join("");
  }
  const corpo = r => JSON.stringify([r.seq, r.quando, r.tipo, r.caixa, r.texto, r.motivo, r.anterior]);
  let LEDGER = [], OK = true, ERRO = "";
  async function carregar() {
    let l = [];
    try { l = JSON.parse(ler(CHAVE) || "[]"); if (!Array.isArray(l)) throw 0; }
    catch (e) { LEDGER = []; OK = false; ERRO = "O arquivo da Casa não pôde ser lido. Nada foi apagado."; return; }
    let ant = "GENESIS";
    for (let i = 0; i < l.length; i++) {
      const r = l[i];
      if (!r || r.seq !== i + 1 || r.anterior !== ant || await sha256(corpo(r)) !== r.hash) {
        LEDGER = l; OK = false; ERRO = "A corrente quebrou no marco " + (i + 1) + ". Nada foi apagado."; return;
      }
      ant = r.hash;
    }
    LEDGER = l; OK = true; ERRO = "";
  }
  let fila = Promise.resolve();
  function anotar(tipo, caixa, texto, motivo) {
    fila = fila.catch(() => {}).then(async () => {
      await carregar();                                  // outra aba pode ter gravado: confere antes
      if (!OK) throw new Error(ERRO);
      const r = { seq: LEDGER.length + 1, quando: new Date().toISOString(), tipo, caixa, texto, motivo,
        anterior: LEDGER.length ? LEDGER[LEDGER.length - 1].hash : "GENESIS" };
      r.hash = await sha256(corpo(r));
      LEDGER.push(r); gravar(CHAVE, JSON.stringify(LEDGER)); return r;
    });
    return fila;
  }
  const vigentes = () => LEDGER.filter(r => r.tipo === "guardar");
  const VERBO = /^(guarda|guardar|guarde|arquiva|arquivar|arquive|anota|anotar|anote|lembra|lembrar|lembre|salva|salvar|salve|grava|gravar|grave|registra|registrar|registre)\b[:,]?\s*/i;
  async function responder(entrada) {
    const original = entrada.trim(), t = semAcento(original);
    if (!original) return "Diga ou escreva alguma coisa.";
    if (/^(ajuda|comandos|o que voce faz)\b/.test(t))
      return "guardar … · busca … · lista · caixas · casa · copia\nToque numa fala para copiar. Arraste a bolinha para tirar do caminho.";
    if (/^(caixas|boxes)$/.test(t)) {
      const c = {}; vigentes().forEach(r => c[r.caixa] = (c[r.caixa] || 0) + 1);
      return Object.entries(CAIXAS).map(([k, [n, p]]) => k + " " + n + " (" + p + "): " + (c[k] || 0)).join("\n");
    }
    if (/^(copia|copia de seguranca|backup|baixar copia)$/.test(t)) {
      await carregar();
      if (!OK) return "Não fiz a cópia: a corrente da Casa não confere. Nada foi mudado.";
      const temBlack = LEDGER.some(r => r.caixa === "08");
      if (!confirm("Baixar a cópia de segurança da Casa (" + LEDGER.length + " marcos)?" + (temBlack ? "\n\nAtenção: a caixa Black vai junto SEM cifra. Para a nuvem, use a viagem cifrada (v2)." : ""))) return "Cópia cancelada. Nada mudou.";
      const a = document.createElement("a");
      a.href = URL.createObjectURL(new Blob([JSON.stringify({ tipo: "GaIA Casca", quando: new Date().toISOString(), ledger: LEDGER }, null, 1)], { type: "application/json" }));
      a.download = "gaia_casa_" + new Date().toISOString().slice(0, 19).replace(/[:T]/g, "-") + ".json"; document.body.appendChild(a); a.click(); a.remove();
      return "Cópia baixada: " + LEDGER.length + " marcos" + (temBlack ? " (inclui a Black sem cifra; guarde em lugar seu)." : ".");
    }
    if (/^(casa|status|estado)$/.test(t))
      return OK ? "Casa: " + LEDGER.length + " marcos, corrente conferida. Porta em modo TESTE (blindar depois)." : "Alerta: " + ERRO;
    if (/^(lista|ultimos|o que tem)\b/.test(t)) {
      const v = vigentes().slice(-5).reverse();
      return v.length ? v.map(r => "[" + CAIXAS[r.caixa][0] + "] " + (r.caixa === "08" ? "(privado)" : r.texto.slice(0, 80))).join("\n") : "A Casa ainda está vazia.";
    }
    const mb = t.match(/^(busca|buscar|procura|procurar|traz|trazer|acha|achar)\s+(.+)$/);
    if (mb) {
      const q = mb[2].split(/\W+/).filter(w => w.length > 2);
      const a = vigentes().filter(r => r.caixa !== "08").map(r => { const w = semAcento(r.texto); return [r, q.filter(p => w.includes(p)).length / q.length]; })
        .filter(x => x[1] > 0).sort((x, y) => y[1] - x[1] || y[0].seq - x[0].seq).slice(0, 3);
      return a.length ? a.map(([r]) => "[" + CAIXAS[r.caixa][0] + "] " + r.texto.slice(0, 160)).join("\n") : "Não achei nada com isso (a Black nunca aparece em busca).";
    }
    if (VERBO.test(original)) {
      let texto = original.replace(VERBO, "").replace(/^(isso|isto|que)\s*[:,]?\s*/i, ""), caixa = null, motivo = "";
      const fim = semAcento(texto).match(/\s+(na|no|em)\s+(caixa\s+)?([a-z]+)\s*$/);
      if (fim && PALAVRA_CAIXA[fim[3]]) { caixa = PALAVRA_CAIXA[fim[3]]; texto = texto.slice(0, texto.length - fim[0].length).trim(); motivo = "você escolheu"; }
      if (!texto) return "Guardar o quê? Diga: guardar …";
      if (!caixa) [caixa, motivo] = classificar(texto);
      else if (caixa !== "08" && privado(texto)) { caixa = "08"; motivo = "tem dado privado"; }
      await carregar();
      if (vigentes().find(r => r.caixa === caixa && semAcento(r.texto).replace(/\s+/g, " ").trim() === semAcento(texto).replace(/\s+/g, " ").trim())) return "Isso já estava guardado na " + CAIXAS[caixa][0] + ".";
      const r = await anotar("guardar", caixa, texto, motivo);
      return "Guardado na " + CAIXAS[caixa][0] + " (" + motivo + "). Marco " + r.seq + " · selo " + r.hash.slice(0, 8) + ".";
    }
    return "Ainda não sei fazer isso. Para guardar: “guardar …”. Para achar: “busca …”. Ajuda: “ajuda”.";
  }

  /* ---------- camada visual (Shadow DOM) ---------- */
  const host = document.createElement("div");
  host.id = "gaia-casca"; host.style.cssText = "position:fixed;inset:0;pointer-events:none;z-index:2147483000";
  const raiz = host.attachShadow({ mode: "open" });
  raiz.innerHTML = `<style>
    :host{all:initial}
    *{box-sizing:border-box;font-family:-apple-system,BlinkMacSystemFont,system-ui,sans-serif;-webkit-tap-highlight-color:transparent}
    .orb{position:fixed;width:54px;height:54px;border-radius:50%;pointer-events:auto;touch-action:none;user-select:none;-webkit-user-select:none;
      display:grid;place-items:center;font-size:22px;font-weight:700;color:#fff;cursor:pointer;
      background:radial-gradient(circle, rgba(139,92,246,.14) 0 52%, rgba(139,92,246,.92) 56% 100%);
      box-shadow:0 4px 14px rgba(0,0,0,.35);transition:left .18s,top .18s;text-shadow:0 1px 3px rgba(0,0,0,.6)}
    .orb.drag{transition:none} .orb.ok{background:radial-gradient(circle, rgba(63,121,93,.14) 0 52%, rgba(63,121,93,.92) 56% 100%)}
    .orb.alerta{background:radial-gradient(circle, rgba(169,68,80,.18) 0 52%, rgba(169,68,80,.95) 56% 100%)}
    .orb.ouvindo{background:radial-gradient(circle, rgba(214,179,79,.2) 0 52%, rgba(214,179,79,.95) 56% 100%)}
    .barra{position:fixed;left:8px;right:8px;bottom:calc(env(safe-area-inset-bottom) + 8px);pointer-events:auto;
      display:flex;gap:6px;align-items:center;background:rgba(15,13,26,.88);backdrop-filter:blur(8px);-webkit-backdrop-filter:blur(8px);
      border:1px solid rgba(255,255,255,.12);border-radius:22px;padding:5px;max-width:620px;margin:0 auto}
    .barra input{flex:1;min-width:0;height:36px;border:0;outline:0;background:transparent;color:#F7F5FF;font-size:16px;padding:0 10px}
    .barra input::placeholder{color:#B8B0CE}
    .bt{min-width:36px;height:36px;border:0;border-radius:18px;background:#28213F;color:#F7F5FF;font-size:16px;cursor:pointer}
    .bt.pri{background:#8B5CF6}
    .conversa{position:fixed;left:8px;right:8px;bottom:calc(env(safe-area-inset-bottom) + 58px);max-width:620px;margin:0 auto;
      max-height:55vh;overflow:auto;pointer-events:auto;display:none;flex-direction:column;gap:6px;padding:8px;
      background:rgba(15,13,26,.82);backdrop-filter:blur(8px);-webkit-backdrop-filter:blur(8px);border:1px solid rgba(255,255,255,.1);border-radius:18px}
    .conversa.aberta{display:flex}
    .msg{max-width:88%;padding:9px 11px;border-radius:14px;font-size:14px;line-height:1.35;white-space:pre-wrap;color:#F7F5FF;cursor:copy;position:relative}
    .msg.eu{align-self:flex-end;background:#8B5CF6} .msg.gaia{align-self:flex-start;background:#28213F}
    .msg.copiado::after{content:"copiado ✓";position:absolute;top:-9px;right:8px;font-size:10px;background:#3B82F6;color:#fff;padding:1px 6px;border-radius:8px}
    .dica{font-size:10px;color:#B8B0CE;text-align:center}
    .orb:focus-visible,.bt:focus-visible,.barra input:focus-visible,.msg:focus-visible{outline:3px solid #F2C879;outline-offset:3px}
    .sonda{position:fixed;visibility:hidden;pointer-events:none;padding:env(safe-area-inset-top,0px) env(safe-area-inset-right,0px) env(safe-area-inset-bottom,0px) env(safe-area-inset-left,0px)}
    @media (prefers-reduced-motion: reduce){ .orb{transition:none} }
  </style>
  <div class="conversa" part="conversa" aria-live="polite"></div>
  <div class="barra"><input aria-label="Fale com a GaIA" placeholder="Fale com a GaIA…" enterkeyhint="send"><button class="bt mic" aria-label="Falar">🎤</button><button class="bt pri env" aria-label="Enviar">➤</button></div>
  <div class="sonda" aria-hidden="true"></div>
  <div class="orb" role="button" tabindex="0" aria-label="GaIA: abrir ou fechar a conversa">G</div>`;
  const $ = s => raiz.querySelector(s);
  const orb = $(".orb"), conv = $(".conversa"), campo = $(".barra input");

  /* conversa que sobrevive ao "flash" (recarregar) */
  let historia = [];
  try { historia = JSON.parse(ler(CONV) || "[]"); if (!Array.isArray(historia)) historia = []; } catch (e) { historia = []; }
  function desenharConversa() {
    conv.innerHTML = '<div class="dica">toque numa fala para copiar</div>';
    historia.slice(-60).forEach(m => {
      const d = document.createElement("div"); d.className = "msg " + m.de; d.textContent = m.t;
      d.onclick = () => copiar(m.t, d); conv.appendChild(d);
    });
    conv.scrollTop = conv.scrollHeight;
  }
  function mascarar(t) {                                // dado privado nunca fica na conversa (so na Black)
    let m = t; PRIVADO.slice(0, 4).forEach(r => { m = m.replace(new RegExp(r.source, "g"), "•••"); });
    return m;
  }
  function dizer(de, t) { t = mascarar(t); historia.push({ de, t, q: new Date().toISOString() }); gravar(CONV, JSON.stringify(historia.slice(-200))); desenharConversa(); }
  async function copiar(t, el) {
    try { await navigator.clipboard.writeText(t); }
    catch (e) { const ta = document.createElement("textarea"); ta.value = t; raiz.appendChild(ta); ta.select(); try { document.execCommand("copy"); } catch (_) {} ta.remove(); }
    el.classList.add("copiado"); setTimeout(() => el.classList.remove("copiado"), 1200);
  }
  function falar(t) { try { speechSynthesis.cancel(); const u = new SpeechSynthesisUtterance(t); u.lang = "pt-BR"; speechSynthesis.speak(u); } catch (e) {} }
  function corOrb() { orb.classList.toggle("alerta", !OK); orb.classList.toggle("ok", OK && LEDGER.length > 0); }
  async function enviar() {
    const v = campo.value.trim(); if (!v) return;
    campo.value = ""; dizer("eu", v); conv.classList.add("aberta");
    let r; try { r = await responder(v); } catch (e) { r = "Não consegui: " + e.message; }
    dizer("gaia", r); falar(r.split("\n")[0]); corOrb();
  }
  $(".env").onclick = enviar;
  campo.addEventListener("keydown", e => { if (e.key === "Enter") { e.preventDefault(); enviar(); } });
  campo.addEventListener("focus", () => conv.classList.add("aberta"));

  const Rec = window.SpeechRecognition || window.webkitSpeechRecognition; let rec = null;
  $(".mic").onclick = () => {
    if (!Rec) { campo.focus(); return; }                  // sem reconhecimento: usa o microfone do teclado
    if (rec) { rec.stop(); return; }
    rec = new Rec(); rec.lang = "pt-BR"; rec.interimResults = true;
    rec.onresult = e => { let s = ""; for (const r of e.results) s += r[0].transcript; campo.value = s; };
    rec.onend = () => { rec = null; orb.classList.remove("ouvindo"); };
    rec.onerror = () => { campo.focus(); };
    rec.start(); orb.classList.add("ouvindo");
  };

  /* bolinha: toque abre/fecha; arrastar move e gruda na borda */
  function area() { const c = getComputedStyle($(".sonda")); return { t: parseFloat(c.paddingTop) || 0, r: parseFloat(c.paddingRight) || 0, b: parseFloat(c.paddingBottom) || 0, l: parseFloat(c.paddingLeft) || 0 }; }
  function por(x, y) {
    const m = 8, s = 54, a = area();
    x = Math.min(Math.max(m + a.l, x), innerWidth - s - m - a.r); y = Math.min(Math.max(m + a.t + 12, y), innerHeight - s - 70 - a.b);
    orb.style.left = x + "px"; orb.style.top = y + "px"; return { x, y };
  }
  function ima() { const r = orb.getBoundingClientRect(), a = area(); gravar(POS, JSON.stringify(por(r.left + 27 < innerWidth / 2 ? 8 + a.l : innerWidth - 62 - a.r, r.top))); }
  (function () { let p = null; try { p = JSON.parse(ler(POS) || "null"); } catch (e) {} if (p && isFinite(p.x) && isFinite(p.y)) por(p.x, p.y); else por(innerWidth - 62, innerHeight * 0.55); })();
  let arr = null;
  orb.addEventListener("pointerdown", e => { arr = { x0: e.clientX, y0: e.clientY, l: orb.offsetLeft, t: orb.offsetTop, moveu: false }; orb.setPointerCapture(e.pointerId); });
  orb.addEventListener("pointermove", e => { if (!arr) return; const dx = e.clientX - arr.x0, dy = e.clientY - arr.y0;
    if (!arr.moveu && Math.hypot(dx, dy) > 6) { arr.moveu = true; orb.classList.add("drag"); } if (arr.moveu) por(arr.l + dx, arr.t + dy); });
  orb.addEventListener("pointerup", () => { if (!arr) return; const m = arr.moveu; arr = null; orb.classList.remove("drag");
    if (m) ima(); else conv.classList.toggle("aberta"); });
  orb.addEventListener("keydown", e => { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); conv.classList.toggle("aberta"); } });
  addEventListener("resize", ima);
  addEventListener("storage", e => { if (e.key === CHAVE) carregar().then(corOrb); });   // outra aba gravou

  function montar() {
    document.body.appendChild(host);
    carregar().then(() => {
      if (!historia.length) dizer("gaia", "Oi, eu sou a GaIA. Diga “guardar …” ou “busca …”. Porta em modo TESTE: blindar quando tudo funcionar.");
      else desenharConversa();
      corOrb();
    });
  }
  if (document.body) montar(); else document.addEventListener("DOMContentLoaded", montar);
  window.__gaiaCasca = { responder, carregar, get ledger() { return LEDGER; }, get ok() { return OK; }, raiz };
})();
