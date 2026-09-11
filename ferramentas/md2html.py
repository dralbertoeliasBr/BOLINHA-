import re, html

def esc(s):
    return html.escape(s, quote=False)

def inl(s):
    cofre = []
    def take_code(m):
        cofre.append('<code>' + esc(m.group(1)) + '</code>')
        return '%d' % (len(cofre) - 1)
    s = re.sub(r'`([^`]+)`', take_code, s)
    s = esc(s)
    s = re.sub(r'\[([^\]]+)\]\(([^)\s]+)\)', r'<a href="\2">\1</a>', s)
    s = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', s)
    s = re.sub(r'(^|[^*])\*([^*\n]+)\*', r'\1<em>\2</em>', s)
    def restore(m):
        return cofre[int(m.group(1))]
    s = re.sub(r'(\d+)', restore, s)
    return s

def celulas(linha):
    s = linha.strip()
    if s.startswith('|'): s = s[1:]
    if s.endswith('|'): s = s[:-1]
    parts, cur, i = [], '', 0
    while i < len(s):
        if s[i] == '\\' and i+1 < len(s) and s[i+1] == '|':
            cur += '|'; i += 2; continue
        if s[i] == '|':
            parts.append(cur); cur = ''; i += 1; continue
        cur += s[i]; i += 1
    parts.append(cur)
    return [p.strip() for p in parts]

def e_sep(l):
    return bool(re.match(r'^\|?[\s:|-]*-[\s:|-]*\|?$', l.strip())) and '-' in l

def render(md):
    L = md.replace('\r', '').split('\n')
    out, i, n = [], 0, len(L)
    while i < n:
        l = L[i]
        if not l.strip():
            i += 1; continue
        if l.startswith('```'):
            buf = []
            i += 1
            while i < n and not L[i].startswith('```'):
                buf.append(L[i]); i += 1
            i += 1
            out.append('<pre><code>%s</code></pre>' % esc('\n'.join(buf)))
            continue
        if re.match(r'^---+\s*$', l):
            out.append('<hr>'); i += 1; continue
        m = re.match(r'^(#{1,4})\s+(.*)$', l)
        if m:
            lvl = len(m.group(1))
            out.append('<h%d>%s</h%d>' % (lvl, inl(m.group(2)), lvl))
            i += 1; continue
        if l.strip().startswith('|') and i+1 < n and e_sep(L[i+1]):
            cab = celulas(l); i += 2
            corpo = []
            while i < n and L[i].strip().startswith('|'):
                corpo.append(celulas(L[i])); i += 1
            h = '<table><thead><tr>' + ''.join('<th>%s</th>' % inl(c) for c in cab) + '</tr></thead><tbody>'
            for r in corpo:
                h += '<tr>' + ''.join('<td>%s</td>' % inl(c) for c in r) + '</tr>'
            out.append(h + '</tbody></table>')
            continue
        if l.startswith('>'):
            paras, atual = [], []
            while i < n and L[i].startswith('>'):
                c = re.sub(r'^>\s?', '', L[i])
                if not c.strip():
                    if atual: paras.append(' '.join(atual)); atual = []
                else:
                    atual.append(c)
                i += 1
            if atual: paras.append(' '.join(atual))
            out.append('<blockquote>' + ''.join('<p>%s</p>' % inl(p) for p in paras) + '</blockquote>')
            continue
        p = []
        while i < n and L[i].strip() and not re.match(r'^(#{1,4}\s|```|>|---+\s*$)', L[i]) and L[i].strip()[:1] != '|':
            p.append(L[i].strip()); i += 1
        if p:
            out.append('<p>%s</p>' % inl(' '.join(p)))
    return '\n'.join(out)

if __name__ == '__main__':
    import sys
    md = open(sys.argv[1], encoding='utf-8').read()
    # corta o titulo H1 (ja esta na .head customizada)
    md = re.sub(r'^# .*\n', '', md, count=1)
    print(render(md))
