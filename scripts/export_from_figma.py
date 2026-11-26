#!/usr/bin/env python3
"""Выгрузка брендбука из Figma TOLK_NEXTERA в это репо.

Запуск:  FIGMA_TOKEN=figd_... python3 scripts/export_from_figma.py
         (или токен в файле, путь в FIGMA_TOKEN_FILE)
Что делает:
  1. Сверяет палитру в tokens/colors.json с кадром палитры 711:1249 — расхождение = громкая ошибка.
  2. Выгружает логотипы в SVG в logo/.
Токену достаточно прав только на чтение.
"""
import json, os, sys, urllib.request

FILE_KEY = 'eJKQuooNI4IBcZsXrLQ5yi'
PALETTE_NODE = '711:1249'
SVG_NODES = {                      # узел Figma → файл в logo/
    '696:54': 'wordmark.svg',      # логотип nextera
    '696:122': 'lockup.svg',       # логотип с символом
    '696:40': 'symbol.svg',        # символ-«бусины», градиент
}
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def token():
    t = os.environ.get('FIGMA_TOKEN')
    if not t and os.environ.get('FIGMA_TOKEN_FILE'):
        t = open(os.environ['FIGMA_TOKEN_FILE']).read().strip()
    if not t:
        sys.exit('Нет токена: задайте FIGMA_TOKEN или FIGMA_TOKEN_FILE')
    return t


def api(path, tok):
    rq = urllib.request.Request('https://api.figma.com/v1' + path, headers={'X-Figma-Token': tok})
    return json.load(urllib.request.urlopen(rq, timeout=120))


def hexc(c):
    return '#%02X%02X%02X' % (round(c['r'] * 255), round(c['g'] * 255), round(c['b'] * 255))


def check_palette(tok):
    doc = api(f'/files/{FILE_KEY}/nodes?ids={PALETTE_NODE}&depth=2', tok)['nodes'][PALETTE_NODE]['document']
    figma = {hexc(f['color']) for ch in doc['children'] for f in ch.get('fills', []) if f.get('type') == 'SOLID' and f.get('visible', True)}
    figma.discard('#000000')  # подписи кадра
    cols = json.load(open(os.path.join(ROOT, 'tokens', 'colors.json')))
    repo = {v['value'].upper() for grp in ('neutral', 'accent') for k, v in cols[grp].items() if k != 'green-text'}
    if figma != repo:
        sys.exit(f'Палитра разошлась с Figma. Только в Figma: {sorted(figma - repo)}; только в репо: {sorted(repo - figma)}')
    print('палитра совпадает с Figma:', ', '.join(sorted(figma)))


def export_svgs(tok):
    ids = ','.join(SVG_NODES)
    urls = api(f'/images/{FILE_KEY}?ids={ids}&format=svg&svg_outline_text=true', tok)['images']
    for node, name in SVG_NODES.items():
        if not urls.get(node):
            sys.exit(f'Figma не отдала SVG для узла {node}')
        data = urllib.request.urlopen(urls[node], timeout=120).read()
        open(os.path.join(ROOT, 'logo', name), 'wb').write(data)
        print(f'{node} → logo/{name} ({len(data)} байт)')


if __name__ == '__main__':
    t = token()
    check_palette(t)
    export_svgs(t)
