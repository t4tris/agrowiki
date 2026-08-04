# -*- coding: utf-8 -*-
"""Извлечь JSON-отчёт сабагента из output-файла и сохранить в vault (идемпотентно, с checksum)."""
import hashlib
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
payload = json.dumps(parsed, ensure_ascii=False, indent=2)
checksum = hashlib.md5(payload.encode('utf-8')).hexdigest()

# Идемпотентность: если файл уже есть с тем же checksum — пропускаем
if os.path.exists(dst):
    existing = open(dst, encoding='utf-8').read()
    if hashlib.md5(existing.encode('utf-8')).hexdigest() == checksum:
        print(f'SKIP: {dst} уже извлечён (checksum совпал, {checksum[:8]})')
        sys.exit(0)
    print(f'ОБНОВЛЕНИЕ: {dst} существует, но содержимое отличается (новый checksum {checksum[:8]})')

with open(dst, 'w', encoding='utf-8') as f:
    f.write(payload)
print(f'Сохранено: {dst}  [checksum {checksum[:8]}]')

# Краткая сводка
print('Культуры:', {c: v.get('status') for c, v in parsed['crops'].items()})
print('Всего claims:', sum(len(v.get('claims', [])) for v in parsed['crops'].values()))
print('Конфликты:', len(parsed.get('conflicts', [])))
print('Вердикт:', parsed.get('verdict'))
