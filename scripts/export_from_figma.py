#!/usr/bin/env python3
"""Выгрузка брендбука из Figma NexteraBrandBook в это репо.

Запуск:  FIGMA_TOKEN=figd_... python3 scripts/export_from_figma.py
         (или токен в файле, путь в FIGMA_TOKEN_FILE)
Что делает:
  1. Сверяет палитру в tokens/colors.json с кадром палитры 711:1249 — расхождение = громкая ошибка.
  2. Выгружает логотипы и графику в SVG, 3D-рендеры в PNG.
  3. Выгружает все кадры брендбука (страница guide) в guide/ как PNG.
  4. Дизайн сайта (страница web) → web/, кейс бренда и соцформаты (страница case) → case/.
Токену достаточно прав только на чтение.
"""
import json, os, sys, urllib.request

FILE_KEY = 'KCfG4o42G1dTIOesBKcvUn'   # NexteraBrandBook
PALETTE_NODE = '711:1249'
SVG_NODES = {                                  # узел Figma → файл в репо
    '696:54': 'logo/wordmark.svg',               # логотип nextera
    '696:40': 'logo/symbol.svg',                 # символ-«бусины», градиент
    '696:42': 'logo/latin.svg',                  # символ над логотипом, латиница
    '696:166': 'logo/cyrillic.svg',              # «некстера», кириллица
    '696:64': 'logo/descriptor-ink.svg',         # логотип + дескриптор, на светлом
    '696:122': 'logo/descriptor-paper.svg',      # логотип + дескриптор, монохром на тёмном
    '696:6': 'logo/wordmark-display.svg',        # крупный логотип с построениями наклона
    '696:241': 'graphics/forms.svg',             # графика: формы из «бусин»
}
PNG_NODES = {                                  # растровые кадры (3D-рендеры) → файл, масштаб 2
    '696:28': 'graphics/material-1.png',
}
WEB_NODES = {                                  # страница web: дизайн сайта, PNG масштаб 0.5
    '2149:574': 'web/01-site-desktop.png',
    '2459:2444': 'web/02-site-desktop-v2.png',
    '2348:1996': 'web/03-site-mobile.png',
}
CASE_NODES = {                                 # страница case: кейс бренда целиком и соцформаты
    '1033:149': 'case/nextera-case-full.png',
    '1419:2': 'case/story-1.png', '1420:17': 'case/story-2.png', '1420:37': 'case/story-3.png',
    '1421:72': 'case/post-1.png', '2272:1820': 'case/post-2.png', '2272:1884': 'case/post-3.png',
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


def export_nodes(tok, nodes, fmt, scale=1):
    ids = ','.join(nodes)
    urls = api(f'/images/{FILE_KEY}?ids={ids}&format={fmt}&scale={scale}&svg_outline_text=true', tok)['images']
    for node, name in nodes.items():
        if not urls.get(node):
            sys.exit(f'Figma не отдала {fmt} для узла {node}')
        data = urllib.request.urlopen(urls[node], timeout=180).read()
        path = os.path.join(ROOT, name)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        open(path, 'wb').write(data)
        print(f'{node} → {name} ({len(data)} байт)')


def export_guide(tok):
    """Все кадры страницы guide в порядке GUIDE_ORDER (guide/order.json) как PNG 1152×648."""
    order = json.load(open(os.path.join(ROOT, 'guide', 'order.json')))
    export_nodes(tok, {o['id']: f"guide/{o['file']}" for o in order}, 'png', 0.6)


if __name__ == '__main__':
    t = token()
    check_palette(t)
    export_nodes(t, SVG_NODES, 'svg')
    export_nodes(t, PNG_NODES, 'png', 2)
    export_guide(t)
    export_nodes(t, WEB_NODES, 'png', 0.5)
    export_nodes(t, CASE_NODES, 'png', 0.3)
