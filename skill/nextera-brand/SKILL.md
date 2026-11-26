---
name: nextera-brand
description: Дизайн-код Nextera — цвета, шрифт, правило зелёного, логотипы, бланк. Читать ПЕРЕД любой работой, где есть вид: сайт, прототип, презентация, документ Word/PDF, схема, аватар, письмо клиенту.
---

# Дизайн-код Nextera

Источник правды — репо https://github.com/Nextera-AI/brandbook (выгрузка из Figma NexteraBrandBook). Брендбук текстом — GUIDE.md: голос бренда, архетипы, правила логотипа. Значения ниже — справка; в коде **подключай файлы по ссылкам**, а не переписывай цвета.

## Цвета (75 % нейтральные / 25 % акцент)

| Имя | Значение | Роль |
|---|---|---|
| ink | #17171A | основной текст, тёмный фон |
| brown | #726658 | вторичный текст, акценты вместо зелёного, выделенные блоки схем |
| sand | #C2B59B | линии, разделители |
| stone | #E5E1DC | подложки |
| paper | #EFEEED | основной светлый фон |
| green | #4DE41D | ТОЛЬКО заливки, маркеры, точки, рамки |
| green-text | #2A7D10 | зелёный текст на светлом |

**Правило зелёного:** #4DE41D текстом на светлом не используется (контраст 1.46:1). Зелёного мало — один акцент на экран; вторичные акценты — brown.

## Шрифт

IBM Plex Sans 400/500/600. IBM Plex Mono — только код и данные. Halvar — шрифт логотипа, только контурами.

## Подключение

- CSS: `https://raw.githubusercontent.com/Nextera-AI/brandbook/main/tokens/tokens.css` (переменные --nx-ink, --nx-brown, --nx-green …)
- JSON: `https://raw.githubusercontent.com/Nextera-AI/brandbook/main/tokens/colors.json`, `https://raw.githubusercontent.com/Nextera-AI/brandbook/main/tokens/typography.json`
- Логотип SVG: `https://raw.githubusercontent.com/Nextera-AI/brandbook/main/logo/wordmark.svg`, символ `…/logo/symbol.svg`; PNG: `https://raw.githubusercontent.com/Nextera-AI/brandbook/main/logo/wordmark-ink.png` (на светлом), `https://raw.githubusercontent.com/Nextera-AI/brandbook/main/logo/wordmark-paper.png` (на тёмном), монограмма `https://raw.githubusercontent.com/Nextera-AI/brandbook/main/logo/monogram-n-ink.png`
- Бланк Word: `https://raw.githubusercontent.com/Nextera-AI/brandbook/main/templates/word/nextera-letterhead.docx`, генератор `templates/word/letterhead.py` (python-docx)

## Голос

Правитель × Бунтарь (через Творца): «Контроль, который переопределяет правила». Говорим: «скорость без системы — это риск», «мы возвращаем контроль». Не говорим: «мы поможем вам», «AI изменит мир», «удобный инструмент». Заголовки — со строчной.

**Nextera — платформа агентной инженерии.** Слово «вайбкод» о Nextera не используем (решение 26.11.2026). Дескриптор логотипа — «платформа агентной инженерии»; SVG дескриптора в репо пока со старым текстом — не использовать.

## Логотип: нельзя

Деформировать, поворачивать, перекрашивать, ставить на цветную подложку, менять буквы, ставить с низким контрастом. Охранное поле — «x» из построений (guide/18).

## Не делаем

Надписи капсом над заголовками · карточки «✕ / ✓» розовым и зелёным · градиентный текст · полоса сбоку у скруглённого блока · моноширинный шрифт для «технологичности» · чёрные и светлые слайды вперемешку.

## Если чего-то нет

Нужен ассет, которого нет в репо (SVG, новый шаблон), — не рисуй свой вариант логотипа: попроси владельца, ассет выгружается из Figma в репо.
