"""Бланк Nextera для Word: шапка с логотипом и реквизитами, подвал. Запуск: python3 letterhead.py → nextera-letterhead.docx"""
from docx import Document
from docx.shared import Pt, Cm, RGBColor, Emu
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

INK = RGBColor(0x17, 0x17, 0x1A)
TAUPE = RGBColor(0x72, 0x66, 0x58)
FONT = 'IBM Plex Sans'
import os
LOGO = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'logo', 'wordmark-ink.png')

d = Document()
sec = d.sections[0]
sec.page_width, sec.page_height = Cm(21), Cm(29.7)
sec.left_margin = sec.right_margin = Cm(2.2)
sec.top_margin, sec.bottom_margin = Cm(3.0), Cm(2.2)
sec.header_distance, sec.footer_distance = Cm(1.0), Cm(1.0)

st = d.styles['Normal']
st.font.name = FONT
st.font.size = Pt(10.5)
st.font.color.rgb = INK
st.element.rPr.rFonts.set(qn('w:eastAsia'), FONT)
st.paragraph_format.space_after = Pt(4)
st.paragraph_format.line_spacing = 1.18


def border_bottom(par, color='C2B59B', sz=6):
    pPr = par._p.get_or_add_pPr()
    b = OxmlElement('w:pBdr')
    e = OxmlElement('w:bottom')
    e.set(qn('w:val'), 'single'); e.set(qn('w:sz'), str(sz)); e.set(qn('w:space'), '6'); e.set(qn('w:color'), color)
    b.append(e); pPr.append(b)


def run(par, text, bold=False, size=None, color=None, italic=False):
    r = par.add_run(text)
    r.bold = bold; r.italic = italic
    r.font.name = FONT
    r._element.rPr.rFonts.set(qn('w:eastAsia'), FONT)
    if size: r.font.size = Pt(size)
    if color: r.font.color.rgb = color
    return r


def no_borders(t):
    tbl = t._tbl
    tblPr = tbl.tblPr
    b = OxmlElement('w:tblBorders')
    for side in ('top', 'left', 'bottom', 'right', 'insideH', 'insideV'):
        e = OxmlElement(f'w:{side}'); e.set(qn('w:val'), 'nil'); b.append(e)
    tblPr.append(b)


def cell_border_bottom(cell, color='C2B59B', sz=4):
    tcPr = cell._tc.get_or_add_tcPr()
    b = OxmlElement('w:tcBorders')
    e = OxmlElement('w:bottom'); e.set(qn('w:val'), 'single'); e.set(qn('w:sz'), str(sz)); e.set(qn('w:color'), color)
    b.append(e); tcPr.append(b)


# ── Бланк: шапка ──
hdr = sec.header
ht = hdr.add_table(rows=1, cols=2, width=Cm(16.6))
no_borders(ht)
ht.columns[0].width = Cm(6); ht.columns[1].width = Cm(10.6)
c0, c1 = ht.rows[0].cells
c0.width, c1.width = Cm(6), Cm(10.6)
p = c0.paragraphs[0]
p.add_run().add_picture(LOGO, height=Cm(0.75))
p = c1.paragraphs[0]; p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
p.paragraph_format.space_after = Pt(0)
run(p, 'ООО «Некстера»\n', bold=True, size=8.5)
run(p, 'ИНН 9705255565 · КПП 770501001 · ОГРН 1267700137880\n', size=7.5, color=TAUPE)
run(p, 'г. Москва, ул. Валовая, д. 35 · hello@nextera.ru · nextera.ru', size=7.5, color=TAUPE)
hp = hdr.add_paragraph(); border_bottom(hp, '17171A', 8); hp.paragraph_format.space_after = Pt(0)

# ── Подвал ──
fp = sec.footer.paragraphs[0]
fp.alignment = WD_ALIGN_PARAGRAPH.LEFT
run(fp, 'nextera.ru', size=7.5, color=TAUPE)


def h1(text):
    p = d.add_paragraph(); p.paragraph_format.space_before = Pt(14); p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.keep_with_next = True
    run(p, text, bold=True, size=13)
    return p


def para(text, color=None, size=None, bold_prefix=None):
    p = d.add_paragraph()
    if bold_prefix: run(p, bold_prefix, bold=True, size=size)
    run(p, text, size=size, color=color)
    return p


def kv(rows, w=(5.2, 11.4)):
    t = d.add_table(rows=0, cols=2)
    no_borders(t)
    t.alignment = WD_TABLE_ALIGNMENT.LEFT
    t.autofit = False
    for k, v in rows:
        r = t.add_row().cells
        r[0].width, r[1].width = Cm(w[0]), Cm(w[1])
        for c in r: cell_border_bottom(c)
        pk = r[0].paragraphs[0]; run(pk, k, size=9.5, color=TAUPE)
        pv = r[1].paragraphs[0]
        parts = v if isinstance(v, list) else [v]
        for i, part in enumerate(parts):
            if i: pv = r[1].add_paragraph()
            if isinstance(part, tuple): run(pv, part[0], bold=True, size=10)
            else: run(pv, part, size=10)
        for c in r:
            for pp in c.paragraphs: pp.paragraph_format.space_after = Pt(3); pp.paragraph_format.space_before = Pt(3)
    for i, wd in enumerate(w): t.columns[i].width = Cm(wd)
    return t



p = d.add_paragraph()
run(p, 'Заголовок документа', bold=True, size=18)
d.add_paragraph('Текст документа.')
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'nextera-letterhead.docx')
d.save(out)
print(out)
