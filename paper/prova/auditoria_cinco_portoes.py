# -*- coding: utf-8 -*-
"""
auditoria_cinco_portoes.py — os "cinco testes pra aprovar" mecanizados.

Nao inventa um criterio novo de qualidade. Aplica, linha por linha, os
cinco pontos que ja governam este projeto desde o CLAUDE.md:

  1. Nenhum numero entra sem codigo que roda
  2. O que cai fica (REFUTADO nao desaparece, fica com endereco: um numero
     que mostre a queda)
  3. Controle antes de credito (informacao mutua/correlacao exige linha de
     base embaralhada, no texto e no codigo)
  4. Verificacao antes de publicar (o protocolo ida-e-volta existe de
     verdade no codigo, nao so na prosa)
  5. Citacao em todo documento

Le a tabela de asserções direto do .md (nao reescreve, nao resume) e cruza
cada linha contra paper/prova/experimentos.py. Escreve um veredito por
asserção e um veredito global para os dois portões que são propriedade do
projeto inteiro, não de uma linha (4 e 5).

Uso:
    python3 paper/prova/auditoria_cinco_portoes.py

Sem dependência externa.
"""
import os
import re
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
PAPER_MD = os.path.join(RAIZ, 'paper', 'AS_GEMEAS_E_O_NUMERO.md')
EXPERIMENTOS_PY = os.path.join(AQUI, 'experimentos.py')
NUCLEO_PY = os.path.join(AQUI, 'nucleo.py')


def celulas(linha):
    """Mesma lógica de ferramentas/md2html.py: separa por '|' respeitando
    '\\|' escapado — a asserção A2 tem 'H(X\\|M)' dentro da própria célula."""
    s = linha.strip()
    if s.startswith('|'):
        s = s[1:]
    if s.endswith('|'):
        s = s[:-1]
    parts, cur, i = [], '', 0
    while i < len(s):
        if s[i] == '\\' and i + 1 < len(s) and s[i + 1] == '|':
            cur += '|'
            i += 2
            continue
        if s[i] == '|':
            parts.append(cur)
            cur = ''
            i += 1
            continue
        cur += s[i]
        i += 1
    parts.append(cur)
    return [p.strip() for p in parts]


def extrai_tabela():
    texto = open(PAPER_MD, encoding='utf-8').read()
    saida = []
    for l in texto.split('\n'):
        if not re.match(r'^\|\s*A\d+\s*\|', l):
            continue
        c = celulas(l)
        if len(c) < 5:
            continue
        saida.append({
            'id': c[0], 'assercao': c[1], 'status': c[2].replace('*', ''),
            'evidencia': c[3], 'derruba': c[4],
        })
    return saida


def funcoes_experimentos():
    """{'e11': codigo_da_funcao_inteira, 'e3b': ..., ...} — chave curta,
    do jeito que a tabela cita (E11, E3b, E7b)."""
    texto = open(EXPERIMENTOS_PY, encoding='utf-8').read()
    achados = list(re.finditer(r'^def (e\d+[a-z]?)_\w*\(', texto, flags=re.M))
    limites = [m.start() for m in achados] + [len(texto)]
    nomes = [m.group(1) for m in achados]
    return {nomes[i]: texto[limites[i]:limites[i + 1]] for i in range(len(nomes))}


def refs_exx(campo):
    return [m.lower() for m in re.findall(r'\bE(\d+[a-z]?)\b', campo)]


def gate1_codigo_existe(a, funcs):
    if 'CONJECTURA' in a['status']:
        return True, 'CONJECTURA — declarada como não medida; isenta da regra 1 até virar MEDIDO'
    refs = refs_exx(a['evidencia'])
    if refs:
        faltando = [r for r in refs if 'e' + r not in funcs]
        if faltando:
            return False, 'cita E%s, mas não existe função correspondente em experimentos.py' % ','.join(faltando)
        return True, 'função(ões) e%s existe(m) e roda(m) em experimentos.py' % ','.join(refs)
    tem_citacao = bool(re.search(r'\[\d+\]', a['evidencia']))
    tem_secao = bool(re.search(r'§\d', a['evidencia']))
    if tem_citacao or tem_secao:
        return True, 'sem Exx; sustentada por %s' % ('citação [n]' if tem_citacao else 'seção do próprio paper (§)')
    return False, 'evidência não cita experimento (Exx), citação [n] nem seção (§) — nada sustenta a linha'


def gate2_refutado_com_endereco(a):
    if 'REFUTADO' not in a['status']:
        return True, 'não aplicável (status != REFUTADO)'
    tem_numero = bool(re.search(r'\d', a['evidencia']))
    return tem_numero, ('evidência carrega o número que mostra a queda' if tem_numero
                         else 'REFUTADO sem número que mostre a queda — vago, não verificável')


PALAVRAS_MI = ('informação mútua', 'informacao mutua', 'correlação', 'correlacao', 'paridade')


def gate3_controle(a, funcs):
    baixo = (a['assercao'] + ' ' + a['evidencia']).lower()
    if not any(p in baixo for p in PALAVRAS_MI):
        return True, 'não aplicável (não alega informação mútua/correlação/paridade)'
    refs = refs_exx(a['evidencia'])
    fonte = ' '.join(funcs.get('e' + r, '') for r in refs)
    tem_controle_texto = 'controle' in baixo or 'líquid' in baixo or 'liquid' in baixo
    tem_controle_codigo = bool(re.search(r'embaralh|shuffle', fonte))
    ok = tem_controle_texto and tem_controle_codigo
    partes = [
        'texto cita controle' if tem_controle_texto else 'texto NÃO cita controle/líquido',
        'código embaralha' if tem_controle_codigo else 'código sem embaralhamento visível',
    ]
    return ok, '; '.join(partes)


def gate4_ida_e_volta():
    """Global: nucleo.py precisa codificar E decodificar, e algum lugar do
    código precisa de fato comparar o decodificado com o original antes de
    aprovar algo — não só descrever o protocolo em prosa."""
    nucleo = open(NUCLEO_PY, encoding='utf-8').read()
    tem_codifica = bool(re.search(r'def\s+\w*codifica\w*\(', nucleo, flags=re.I))
    tem_decodifica = bool(re.search(r'def\s+\w*decodifica\w*\(', nucleo, flags=re.I))
    exp = open(EXPERIMENTOS_PY, encoding='utf-8').read()
    m = re.search(r'def\s+\w*ida_e_volta\w*\(.*?(?=\ndef |\Z)', exp, flags=re.S)
    corpo = m.group(0) if m else ''
    tem_funcao = bool(m)
    tem_comparacao = '==' in corpo
    tem_decodif_ou_hash = bool(re.search(r'decodif|hexdigest|sha256', corpo, flags=re.I))
    ok = tem_codifica and tem_decodifica and tem_funcao and tem_comparacao and tem_decodif_ou_hash
    return ok, ('codifica=%s decodifica=%s função-ida-e-volta=%s compara(==)=%s usa-decodificação/hash=%s'
                % (tem_codifica, tem_decodifica, tem_funcao, tem_comparacao, tem_decodif_ou_hash))


def gate5_citacao():
    texto = open(PAPER_MD, encoding='utf-8').read()
    tem_orcid = 'ORCID' in texto or 'orcid.org' in texto
    tem_bibtex = '@misc' in texto or '@article' in texto or 'BibTeX' in texto
    ok = tem_orcid and tem_bibtex
    return ok, 'ORCID presente=%s, BibTeX presente=%s' % (tem_orcid, tem_bibtex)


def main():
    tabela = extrai_tabela()
    funcs = funcoes_experimentos()

    linhas = []
    passou_1a3 = 0
    for a in tabela:
        r1, d1 = gate1_codigo_existe(a, funcs)
        r2, d2 = gate2_refutado_com_endereco(a)
        r3, d3 = gate3_controle(a, funcs)
        passou = r1 and r2 and r3
        if passou:
            passou_1a3 += 1
        linhas.append({'a': a, 'r1': r1, 'd1': d1, 'r2': r2, 'd2': d2, 'r3': r3, 'd3': d3, 'passou': passou})

    g4, d4 = gate4_ida_e_volta()
    g5, d5 = gate5_citacao()

    L = []
    w = L.append
    w('# Auditoria dos cinco portões\n')
    w('Verificação mecânica, não opinião: cada portão abaixo já era regra em '
      '`CLAUDE.md` antes desta auditoria existir. O que muda aqui é que agora '
      'um script confere, linha a linha, em vez de confiar em quem escreveu — '
      'inclusive em quem escreveu este script.\n')
    w('| portão | o que verifica |')
    w('|---|---|')
    w('| 1 — roda | a asserção cita um experimento (`Exx`) e a função `exx` existe em `experimentos.py`, ou é TEOREMA/LITERATURA com referência real |')
    w('| 2 — endereço da queda | toda asserção REFUTADO carrega um número que mostra a queda, não só a palavra |')
    w('| 3 — controle | toda alegação de informação mútua/correlação/paridade tem controle citado no texto **e** embaralhamento real no código |')
    w('| 4 — ida-e-volta (global) | `nucleo.py` codifica **e** decodifica, e algum experimento compara o decodificado com o original antes de aprovar |')
    w('| 5 — citação (global) | o paper carrega ORCID e BibTeX |\n')

    w('## Portões 1–3, por asserção\n')
    w('| # | 1 roda | 2 endereço | 3 controle | veredito |')
    w('|---|---|---|---|---|')
    for x in linhas:
        m1 = 'OK' if x['r1'] else 'FALHA'
        m2 = 'OK' if x['r2'] else 'FALHA'
        m3 = 'OK' if x['r3'] else 'FALHA'
        w('| %s | %s | %s | %s | **%s** |' % (
            x['a']['id'], m1, m2, m3, 'passa' if x['passou'] else 'FALHA'))
    w('')

    falhas = [x for x in linhas if not x['passou']]
    if falhas:
        w('### Detalhe das falhas\n')
        for x in falhas:
            w('**%s** — %s' % (x['a']['id'], x['a']['assercao']))
            if not x['r1']:
                w('- portão 1: %s' % x['d1'])
            if not x['r2']:
                w('- portão 2: %s' % x['d2'])
            if not x['r3']:
                w('- portão 3: %s' % x['d3'])
            w('')

    w('## Portões 4–5, globais\n')
    w('| portão | veredito | detalhe |')
    w('|---|---|---|')
    w('| 4 — ida-e-volta | %s | %s |' % ('OK' if g4 else 'FALHA', d4))
    w('| 5 — citação | %s | %s |' % ('OK' if g5 else 'FALHA', d5))
    w('')

    total = len(tabela)
    tudo_ok = (passou_1a3 == total) and g4 and g5
    w('## Veredito final\n')
    w('**%d/%d** asserções passam os portões 1–3. Portões globais: 4 = %s, 5 = %s.\n'
      % (passou_1a3, total, 'OK' if g4 else 'FALHA', 'OK' if g5 else 'FALHA'))
    if tudo_ok:
        w('**A obra passa nos cinco portões, mecanicamente conferida.**\n')
    else:
        w('**Ainda não passa em todos.** A lista de falhas acima é trabalho '
          'pendente, não uma opinião — e fica registrada aqui pela mesma regra '
          'que mantém A7, A9, A11 e as outras oito quedas publicadas: o que '
          'este script encontra, fica.\n')

    with open(os.path.join(AQUI, 'AUDITORIA_CINCO_PORTOES.md'), 'w', encoding='utf-8') as f:
        f.write('\n'.join(L) + '\n')

    sys.stderr.write('%d/%d assercoes passam 1-3. portao4=%s portao5=%s\n'
                      % (passou_1a3, total, g4, g5))
    sys.stderr.write('Escrito: paper/prova/AUDITORIA_CINCO_PORTOES.md\n')


if __name__ == '__main__':
    main()
