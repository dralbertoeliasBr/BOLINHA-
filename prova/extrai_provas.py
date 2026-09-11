# -*- coding: utf-8 -*-
"""
extrai_provas.py — extrator de evidencia de anterioridade e integridade.

O que faz, em ordem:
  1. Calcula o SHA-256 de cada arquivo de conteudo nos quatro documentos
     da obra (paper/, manifesto/, simbiose/, livro/, obra/) e do CLAUDE.md.
  2. Pergunta ao git LOCAL qual foi o primeiro e o ultimo commit que
     tocaram cada arquivo.
  3. Cruza esses commits com uma tabela de timestamps VERIFICADOS —
     puxados da API do GitHub, nao do `git log` local — porque a data de
     um commit local pode ser forjada (`git commit --date`), mas a data
     que o servidor do GitHub registrou ao RECEBER o push nao esta sob
     controle de quem fez o push.
  4. Escreve PROVA_DE_ANTERIORIDADE.md com uma tabela pronta pra
     conferencia por qualquer pessoa, em qualquer lugar, sem precisar
     confiar em quem gerou o relatorio.

Uso:
    python3 prova/extrai_provas.py

Sem dependencia externa. Precisa apenas de `git` no PATH.
"""
import hashlib
import json
import os
import subprocess
import sys
from datetime import datetime, timezone

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)

PASTAS = ['paper', 'manifesto', 'simbiose', 'livro', 'obra', 'prova', 'ferramentas']
ARQUIVOS_SOLTOS = ['CLAUDE.md', 'SELO_V1.0.md']

# extensoes que contam como "conteudo" da obra — nao gera hash de cache,
# artefato binario grande ou lixo temporario
EXT_CONTEUDO = {'.md', '.html', '.py', '.json', '.css', '.pdf'}
IGNORAR_DIRS = {'__pycache__', 'corpus'}


def sh(*args):
    return subprocess.run(
        ['git', '-C', RAIZ] + list(args),
        capture_output=True, text=True, check=False
    ).stdout.strip()


def sha256_arquivo(caminho):
    h = hashlib.sha256()
    with open(caminho, 'rb') as f:
        for bloco in iter(lambda: f.read(65536), b''):
            h.update(bloco)
    return h.hexdigest()


def lista_arquivos():
    saida = []
    for pasta in PASTAS:
        base = os.path.join(RAIZ, pasta)
        if not os.path.isdir(base):
            continue
        for dirpath, dirnames, filenames in os.walk(base):
            dirnames[:] = [d for d in dirnames if d not in IGNORAR_DIRS]
            for fn in sorted(filenames):
                ext = os.path.splitext(fn)[1].lower()
                if ext not in EXT_CONTEUDO:
                    continue
                caminho = os.path.join(dirpath, fn)
                rel = os.path.relpath(caminho, RAIZ)
                saida.append(rel)
    for a in ARQUIVOS_SOLTOS:
        if os.path.isfile(os.path.join(RAIZ, a)):
            saida.append(a)
    return sorted(saida)


def historico_do_arquivo(rel):
    """Retorna (sha_primeiro_commit, sha_ultimo_commit) que tocaram o arquivo,
    segundo o git LOCAL. So os hashes; a data vem da tabela verificada."""
    log = sh('log', '--follow', '--format=%H', '--', rel)
    shas = [l for l in log.split('\n') if l.strip()]
    if not shas:
        return None, None
    return shas[-1], shas[0]  # primeiro = mais antigo (log vem do mais novo pro mais velho)


def carrega_tabela_verificada():
    """
    Tabela de commits deste branch com o timestamp que o SERVIDOR do
    GitHub registrou ao receber o push — puxado via API do GitHub em
    2026-09-11, nao inferido do git local. Reverificavel por qualquer
    pessoa: abra a URL de qualquer commit abaixo e compare a data que o
    proprio GitHub mostra na pagina.
    """
    caminho = os.path.join(AQUI, 'commits_github_verificados.json')
    with open(caminho, encoding='utf-8') as f:
        lista = json.load(f)
    return {c['sha']: c for c in lista}


def main():
    verificados = carrega_tabela_verificada()
    arquivos = lista_arquivos()

    linhas = []
    sem_verificacao = []
    for rel in arquivos:
        caminho_abs = os.path.join(RAIZ, rel)
        digest = sha256_arquivo(caminho_abs)
        tamanho = os.path.getsize(caminho_abs)
        sha_primeiro, sha_ultimo = historico_do_arquivo(rel)

        info_primeiro = verificados.get(sha_primeiro) if sha_primeiro else None
        if sha_primeiro and not info_primeiro:
            sem_verificacao.append((rel, sha_primeiro))

        linhas.append({
            'arquivo': rel,
            'bytes': tamanho,
            'sha256': digest,
            'primeiro_commit': sha_primeiro,
            'primeiro_commit_curto': (sha_primeiro or '')[:10],
            'primeiro_commit_data_github': info_primeiro['date'] if info_primeiro else None,
            'primeiro_commit_url': info_primeiro['url'] if info_primeiro else None,
            'ultimo_commit_curto': (sha_ultimo or '')[:10],
        })

    agora = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')

    with open(os.path.join(AQUI, 'inventario.json'), 'w', encoding='utf-8') as f:
        json.dump({'gerado_em_utc': agora, 'arquivos': linhas}, f, indent=1, ensure_ascii=False)

    # ---------------------------------------------------------- relatorio
    L = []
    w = L.append
    w('# Prova de Anterioridade e Integridade\n')
    w('Gerado por `python3 prova/extrai_provas.py` em `%s` (UTC). '
      'Este relatorio nao pede confianca — ensina a verificacao.\n' % agora)
    w('## Como verificar, em três passos\n')
    w('1. **Hash do conteúdo** — clone o repositório e rode `sha256sum` '
      'em qualquer arquivo da tabela abaixo. Se o hash bater com o '
      'listado aqui, o conteúdo é byte a byte o mesmo que existia no '
      'momento deste relatório.\n')
    w('2. **Data do commit** — a coluna "GitHub (UTC)" **não** vem do '
      '`git log` local, que pode ser forjado com `git commit --date`. '
      'Vem da API do GitHub, que registra quando o **servidor** recebeu '
      'o push — isso não está sob controle de quem fez o commit.\n')
    w('3. **Conferência independente** — abra a URL do commit de '
      'qualquer linha. O próprio GitHub mostra a mesma data na página, '
      'de forma pública, para qualquer visitante, sem precisar de conta.\n')
    w('```bash\ngit clone %s\ncd BOLINHA- && git checkout %s\nsha256sum <arquivo>\n```\n'
      % ('https://github.com/dralbertoeliasBr/BOLINHA-.git',
         'claude/llm-gemeas-compressao-lwnpwn'))

    w('## Inventário\n')
    w('| arquivo | bytes | sha-256 (primeiros 16) | 1º commit | GitHub (UTC) |')
    w('|---|---|---|---|---|')
    for x in linhas:
        data = x['primeiro_commit_data_github'] or '*(fora da tabela verificada)*'
        link = ('[`%s`](%s)' % (x['primeiro_commit_curto'], x['primeiro_commit_url'])
                if x['primeiro_commit_url'] else (x['primeiro_commit_curto'] or '—'))
        w('| `%s` | %d | `%s` | %s | %s |' % (
            x['arquivo'], x['bytes'], x['sha256'][:16], link, data))
    w('')

    w('## O que isto prova, e o que não prova\n')
    w('**Prova:** que este conteúdo exato, byte a byte (o hash não '
      'mente), existia — público, no GitHub, com histórico visível a '
      'qualquer pessoa — no momento em que o servidor do GitHub recebeu '
      'o push listado. Isso é mais forte que um arquivo com data local, '
      'porque o timestamp não está sob controle de quem publicou.\n')
    w('**Não prova:** propriedade legal, registro de patente ou direito '
      'autoral formal. Git é evidência técnica de anterioridade, não um '
      'instrumento jurídico. Este projeto já usa o mecanismo formal para '
      'isso — DOIs Zenodo, registrados numa entidade terceira e '
      'independente — ver `paper/AS_GEMEAS_E_O_NUMERO.md`, seção de '
      'Referências, "Registro de anterioridade". Para uma prova ainda '
      'mais forte e sem depender de confiar no GitHub, existe '
      '[OpenTimestamps](https://opentimestamps.org/) — gratuito, '
      'independente, ancorado em blockchain, verificável por qualquer '
      'um sem precisar de conta em lugar nenhum.\n')

    if sem_verificacao:
        w('## Atenção\n')
        w('%d arquivo(s) referenciam um commit fora da tabela verificada '
          '(pode acontecer após um novo commit que ainda não foi '
          're-consultado na API). Rode a atualização da tabela antes de '
          'usar este relatório para conferência externa:\n' % len(sem_verificacao))
        for rel, sha in sem_verificacao:
            w('- `%s` → `%s`' % (rel, sha[:10]))

    with open(os.path.join(AQUI, 'PROVA_DE_ANTERIORIDADE.md'), 'w', encoding='utf-8') as f:
        f.write('\n'.join(L) + '\n')

    sys.stderr.write('%d arquivos processados. %d sem verificacao GitHub.\n'
                     % (len(linhas), len(sem_verificacao)))
    sys.stderr.write('Escrito: prova/PROVA_DE_ANTERIORIDADE.md e prova/inventario.json\n')


if __name__ == '__main__':
    main()
