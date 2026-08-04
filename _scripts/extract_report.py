# -*- coding: utf-8 -*-
"""Извлечь JSON-отчёт сабагента из output-файла и сохранить в vault (идемпотентно, с checksum).

Авто-retry (аудит 2026-08-04): можно передать до 2 дополнительных файлов ответа
(повторные запуски сабагента). Если в первом файле JSON не найден — пробуем следующие
автоматически; удачные retry логируются в task_queue.md (секция RETRY LOG).

Usage: python extract_report.py <src1> <dst.json> [src2] [src3]
Exit codes: 0 = ok; 2 = JSON не найден ни в одном файле (нужен повторный запуск сабагента).
"""
import hashlib
import json
import os
import sys
from datetime import date

srcs = [sys.argv[1]] + [a for a in sys.argv[3:] if a]
dst = sys.argv[2]

TASK_QUEUE = r'f:\agrowiki\task_queue.md'
RETRY_SECTION = '## 🔄 RETRY LOG'


def log_retry(code, src_used):
    line = f'- [ ] RETRY: {code} — успешно со {srcs.index(src_used) + 1}-й попытки (файл: {os.path.basename(src_used)}, {date.today().isoformat()})'
    try:
        with open(TASK_QUEUE, encoding='utf-8') as f:
            txt = f.read()
        if RETRY_SECTION in txt:
            txt = txt.rstrip() + '\n' + line + '\n'
        else:
            txt = txt.rstrip() + '\n\n' + RETRY_SECTION + '\n' + line + '\n'
        with open(TASK_QUEUE, 'w', encoding='utf-8') as f:
            f.write(txt)
    except Exception as e:
        print(f'WARN: не удалось залогировать retry: {e}')


def parse_json(txt):
    candidates = []
    for i, ch in enumerate(txt):
        if ch == '{':
            candidates.append(i)
            if len(candidates) > 50:
                break
    decoder = json.JSONDecoder()
    for start in candidates:
        try:
            d, end = decoder.raw_decode(txt[start:])
            if isinstance(d, dict) and 'contract_version' in d:
                return d, start, end
        except Exception:
            continue
    return None, None, None


parsed = None
used_src = None
for attempt, src in enumerate(srcs):
    try:
        txt = open(src, encoding='utf-8').read()
    except FileNotFoundError:
        print(f'NOT FOUND: {src}')
        continue
    d, start, end = parse_json(txt)
    if d is not None:
        parsed = d
        used_src = src
        print(f'JSON найден (попытка {attempt + 1}): start={start}, end={start + end}, version={d["contract_version"]}')
        break
    print(f'JSON не найден в: {src}')

if parsed is None:
    print('RETRY_NEEDED: JSON с contract_version не найден ни в одном файле. '
          'Запустите сабагента повторно (до 2 попыток) и передайте новые файлы.')
    sys.exit(2)

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

# Авто-retry: логируем успешную повторную попытку (аудит 2026-08-04)
code = parsed.get('substance', {}).get('code', dst)
if used_src and srcs.index(used_src) > 0:
    log_retry(code, used_src)

# Краткая сводка
print('Культуры:', {c: v.get('status') for c, v in parsed['crops'].items()})
print('Всего claims:', sum(len(v.get('claims', [])) for v in parsed['crops'].values()))
print('Конфликты:', len(parsed.get('conflicts', [])))
print('Вердикт:', parsed.get('verdict'))
