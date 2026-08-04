# -*- coding: utf-8 -*-
"""Извлечь JSON-отчёт сабагента из output-файла и сохранить в vault."""
import json
import os
import sys

src = sys.argv[1]
dst = sys.argv[2]

txt = open(src, encoding='utf-8').read()

# Пробуем распарсить JSON начиная с каждой позиции '{'
candidates = []
for i, ch in enumerate(txt):
    if ch == '{':
        candidates.append(i)
        if len(candidates) > 50:
            break

parsed = None
decoder = json.JSONDecoder()
for start in candidates:
    try:
        d, end = decoder.raw_decode(txt[start:])
        if isinstance(d, dict) and 'contract_version' in d:
            parsed = d
            print(f'JSON найден: start={start}, end={start + end}, version={d["contract_version"]}')
            break
    except Exception:
        continue

if parsed is None:
    print('JSON с contract_version не найден!')
    sys.exit(1)

os.makedirs(os.path.dirname(dst), exist_ok=True)
with open(dst, 'w', encoding='utf-8') as f:
    json.dump(parsed, f, ensure_ascii=False, indent=2)
print(f'Сохранено: {dst}')

# Краткая сводка
print('Культуры:', {c: v.get('status') for c, v in parsed['crops'].items()})
print('Всего claims:', sum(len(v.get('claims', [])) for v in parsed['crops'].values()))
print('Конфликты:', len(parsed.get('conflicts', [])))
print('Вердикт:', parsed.get('verdict'))
