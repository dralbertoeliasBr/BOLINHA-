# -*- coding: utf-8 -*-
"""
gera_pdf.py — orquestra .md -> HTML de impressão -> PDF.

Honestidade de fronteira, porque isto quebra o padrão do resto do
projeto: paper/prova/ roda em qualquer lugar com Python puro, sem
dependência. ESTA ferramenta não. Ela tem duas metades:

  1. .md -> HTML de impressão   — determinístico, zero dependência,
     usa só `md2html.py` (biblioteca padrão). Roda em qualquer Python
     3.8+, inclusive Pythonista/a-Shell.
  2. HTML -> PDF                — precisa de um motor de navegador
     (Chromium via `playwright-core`) rodando no ambiente. Isso NÃO
     está disponível em toda máquina, e certamente não num iPhone.
     Quando não está disponível, o script para na etapa 1 e imprime
     o comando exato para terminar manualmente em qualquer navegador
     (abrir o HTML, Imprimir, Salvar como PDF) — nunca falha calado.

Uso:
    python3 ferramentas/gera_pdf.py <fonte.md> <capa.html> <saida_base>

    <fonte.md>     caminho do markdown (o corpo vem a partir do
                   primeiro "## " — o título e o resumo ficam na capa)
    <capa.html>    arquivo HTML com o bloco <div class="head">...</div>
                   pronto (ver paper/RESUMO_EXECUTIVO_capa.html como
                   exemplo, ou escreva um na hora)
    <saida_base>   caminho sem extensão — gera <saida_base>.html
                   sempre, e <saida_base>.pdf se houver navegador

Exemplo real (o que gerou os dois PDFs já publicados nesta obra):
    python3 ferramentas/gera_pdf.py \\
        paper/RESUMO_EXECUTIVO.md \\
        /tmp/capa_resumo.html \\
        paper/RESUMO_EXECUTIVO
"""
import os
import re
import subprocess
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import md2html  # noqa: E402


def monta_html(caminho_md, caminho_capa, titulo_pagina, css_extra=''):
    md = open(caminho_md, encoding='utf-8').read()
    m = re.search(r'\n(## .*)$', '\n' + md, flags=re.S)
    corpo_md = m.group(1) if m else md
    corpo_html = md2html.render(corpo_md)

    capa_html = ''
    if caminho_capa and os.path.isfile(caminho_capa):
        capa_html = open(caminho_capa, encoding='utf-8').read()

    molde = open(os.path.join(AQUI, 'modelo_pdf.html'), encoding='utf-8').read()
    if css_extra:
        molde = molde.replace('</style>', css_extra + '\n</style>')
    if titulo_pagina:
        molde = re.sub(r'<title>.*?</title>', '<title>%s</title>' % titulo_pagina, molde, count=1)
    return molde.replace('__CORPO__', capa_html + corpo_html)


def tenta_gerar_pdf(caminho_html, caminho_pdf):
    """Best-effort: só funciona se playwright-core + Chromium estiverem
    presentes no ambiente. Nunca lança exceção pro chamador — devolve
    True/False e imprime o motivo."""
    try:
        from playwright.sync_api import sync_playwright  # type: ignore
    except ImportError:
        try:
            import subprocess as _sp
            _sp.run(['node', '-e', 'require.resolve("playwright-core")'],
                    check=True, capture_output=True)
        except Exception:
            sys.stderr.write(
                'playwright nao disponivel neste ambiente — pulei a etapa '
                'de PDF. O HTML em "%s" esta pronto: abra num navegador, '
                'Imprimir -> Salvar como PDF, formato A4.\n' % caminho_html)
            return False
        # ambiente com playwright-core (Node), sem binding Python: usa node.
        # Alguns ambientes trazem Chromium pre-instalado num caminho que o
        # playwright-core baixado nao conhece por padrao. Se isso acontecer,
        # defina a variavel de ambiente CHROMIUM_PATH apontando pro binario
        # (ex.: export CHROMIUM_PATH=/opt/pw-browsers/chromium) e rode de novo.
        caminho_chromium = os.environ.get('CHROMIUM_PATH', '')
        opcoes_launch = "{args:['--no-sandbox']" + (
            ", executablePath:'%s'}" % caminho_chromium if caminho_chromium else "}")
        script = '''
const {chromium} = require('playwright-core');
(async () => {
  const b = await chromium.launch(%s);''' % opcoes_launch + '''
  const p = await b.newPage();
  await p.goto('file://%s', {waitUntil:'networkidle'});
  await p.pdf({path:'%s', format:'A4',
    margin:{top:'20mm',bottom:'16mm',left:'18mm',right:'18mm'},
    displayHeaderFooter:true,
    headerTemplate:'<span></span>',
    footerTemplate:'<div style="width:100%%;font-family:Liberation Sans,Arial,sans-serif;font-size:7.6pt;color:#777;text-align:center;padding-top:2mm"><span class="pageNumber"></span> / <span class="totalPages"></span></div>',
    printBackground:true});
  await b.close();
})();
''' % (os.path.abspath(caminho_html), os.path.abspath(caminho_pdf))
        r = subprocess.run(['node', '-e', script], capture_output=True, text=True)
        if r.returncode != 0:
            sys.stderr.write('geracao de PDF via node/playwright falhou:\n%s\n' % r.stderr)
            return False
        return True

    with sync_playwright() as p:
        b = p.chromium.launch(args=['--no-sandbox'])
        pg = b.new_page()
        pg.goto('file://' + os.path.abspath(caminho_html), wait_until='networkidle')
        pg.pdf(path=caminho_pdf, format='A4',
              margin={'top': '20mm', 'bottom': '16mm', 'left': '18mm', 'right': '18mm'},
              display_header_footer=True,
              header_template='<span></span>',
              footer_template=('<div style="width:100%;font-family:Liberation Sans,'
                               'Arial,sans-serif;font-size:7.6pt;color:#777;'
                               'text-align:center;padding-top:2mm">'
                               '<span class="pageNumber"></span> / '
                               '<span class="totalPages"></span></div>'),
              print_background=True)
        b.close()
    return True


def main():
    if len(sys.argv) < 4:
        sys.stderr.write(__doc__)
        sys.exit(1)
    caminho_md, caminho_capa, base = sys.argv[1:4]
    titulo = os.path.splitext(os.path.basename(base))[0].replace('_', ' ').title()

    html = monta_html(caminho_md, caminho_capa, titulo)
    caminho_html = base + '.html'
    with open(caminho_html, 'w', encoding='utf-8') as f:
        f.write(html)
    sys.stderr.write('Escrito: %s\n' % caminho_html)

    caminho_pdf = base + '.pdf'
    if tenta_gerar_pdf(caminho_html, caminho_pdf):
        sys.stderr.write('Escrito: %s\n' % caminho_pdf)
    else:
        sys.stderr.write('PDF NAO gerado automaticamente — veja instrucao acima.\n')


if __name__ == '__main__':
    main()
