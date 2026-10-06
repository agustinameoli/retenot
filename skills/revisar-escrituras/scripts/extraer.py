#!/usr/bin/env python3
"""Extrae los renglones (concepto, importe) de los papeles de UNA escritura
para mandarlos a Retenot con cargar_escritura. No clasifica nada: eso lo hace
el servidor de Retenot.

Uso:
  python3 extraer.py [--factura F.pdf ...] [--proforma P.xlsx]
                     [--proforma-sin-factura P.xlsx ...] [--presupuesto Presupuesto.pdf]

Facturas: comprobantes electrónicos de ARCA (A, B, C y notas de crédito).
Proforma: .xlsx con bloques "Presupuesto parte ...". Se usa solo si no hay facturas.
Imprime JSON: {"items":[{"concepto","importe"}], "fecha_documento", "notas":[]}
Necesita pdftotext (poppler-utils) y openpyxl.
"""
import argparse, datetime, json, os, re, subprocess, sys


def ar(x):
    neg = x.startswith('-')
    v = float(x.lstrip('-').replace('.', '').replace(',', '.'))
    return -v if neg else v


def clean(s):
    return re.sub(r'[\s.…:]+$', '', re.sub(r'\s+', ' ', re.sub(r'[.…]{2,}', ' ', str(s)))).strip()


def pdf_text(path, first_page_only=False):
    cmd = ['pdftotext', '-layout'] + (['-f', '1', '-l', '1'] if first_page_only else []) + [path, '-']
    return subprocess.run(cmd, capture_output=True, text=True).stdout


def factura(path):
    t = pdf_text(path, True)
    L = t.split('\n')
    cod = int(re.search(r'Cod\.?\s*0*(\d+)', t)[1])
    letra, sg = {1: ('A', 1), 6: ('B', 1), 11: ('C', 1), 3: ('A', -1), 8: ('B', -1), 13: ('C', -1)}[cod]
    f = re.search(r'Emisi[oó]n:\s*(\d{2})/(\d{2})/(\d{4})', t)
    if letra == 'A':
        iva = round(sum(ar(x) for x in re.findall(r'IVA\s*(?:27|21|10[.,]5|5|2[.,]5|0)\s*%:\s*\$?\s*([\d.]+,\d{2})', t)), 2)
    else:
        m = re.search(r'IVA Contenido:\s*\$?\s*([\d.]+,\d{2})', t)
        iva = ar(m[1]) if m else 0
    st = next(i for i, l in enumerate(L) if re.search(r'Producto\s*/\s*Servicio', l))
    items = []
    for l in L[st + 1:]:
        if re.search(r'Subtotal:|Importe Otros tributos|Importe Neto|Importe Total|Descripci[oó]n\s+Detalle|Transparencia Fiscal|P[aá]g\.\s*\d|CAE', l):
            break
        tk = l.split()
        qi = next((i for i, x in enumerate(tk) if re.fullmatch(r'\d+,\d{3}', x)), -1)
        if qi > 0:
            d = ' '.join(tk[:qi]); q = ar(tk[qi])
            nums = [ar(x) for x in tk[qi + 1:] if re.fullmatch(r'-?[\d.]+,\d{2}', x)]; n = len(nums)
            if n < 2:
                continue
            if letra == 'A' and n >= 4:
                neto = nums[n - 3]; iv = round(nums[n - 1] - nums[n - 3], 2)
            elif letra == 'B':
                fin = nums[-1]; base = round(nums[0] * q - (nums[n - 2] if n >= 4 else 0), 2)
                neto, iv = (base, round(fin - base, 2)) if base > 0 and fin - base > 0.02 else (fin, 0)
            else:
                neto = nums[-1]; iv = 0
            items.append({'d': d, 'neto': round(neto * sg, 2), 'iva': round(iv * sg, 2)})
        elif items and l.strip() and not re.search(r'\d', l) and not re.fullmatch(r'(IVA|Al[ií]cuota|Subtotal c/IVA)', l.strip(), re.I):
            items[-1]['d'] += ' ' + l.strip()
    notas = []
    if abs(sum(x['iva'] for x in items) - iva) > 1:
        notas.append(f'La factura {letra} {os.path.basename(path)} no cuadra (IVA de los renglones distinto del total): revisala.')
    fecha = f'{f[3]}-{f[2]}-{f[1]}' if f else None
    return [{'concepto': x['d'], 'importe': x['neto']} for x in items], round(iva * sg, 2), fecha, notas


def proforma(path, con_factura=None):
    import openpyxl
    ws = openpyxl.load_workbook(path, data_only=True).worksheets[0]
    rows = [[c.value for c in r] for r in ws.iter_rows()]
    s = lambda v: v.strip() if isinstance(v, str) else ''
    start = next(i for i, r in enumerate(rows) if any(re.search(r'Presupuesto\s+parte', s(c), re.I) for c in r))
    fecha = next((c.date().isoformat() for r in rows[:10] for c in r if isinstance(c, datetime.datetime)), None)
    iva_col = -1
    for i in range(start, min(len(rows), start + 3)):
        for j, c in enumerate(rows[i]):
            if re.fullmatch(r'I\.?\s?V\.?\s?A\.?', s(c), re.I):
                iva_col = j
        if iva_col >= 0:
            break
    amt = iva_col - 1 if iva_col > 0 else 3
    if iva_col < 0:
        iva_col = amt + 1
    partes = []; cur = None
    for r in rows[start:]:
        a = s(r[0]) or (s(r[1]) if len(r) > 1 else '')
        m = re.match(r'Presupuesto\s+parte\s+(.+?)\s*:?\s*$', a, re.I)
        if m:
            cur = {'nombre': clean(m[1]), 'items': []}; partes.append(cur); continue
        if not cur or not a or re.search(r'Conceptos\s+(no\s+)?gravados|Descuento|Honorarios final', a, re.I) or re.fullmatch(r'(SUB)?TOTAL|I\.?V\.?A\.?', a, re.I):
            continue
        mv = r[amt] if amt < len(r) else None
        if not isinstance(mv, (int, float)):
            continue
        iv = r[iva_col] if iva_col < len(r) and isinstance(r[iva_col], (int, float)) else 0
        cur['items'].append({'d': clean(a), 'monto': round(mv, 2), 'iva': round(iv, 2)})
    items = []; iva = 0
    for p in partes:
        lleva = con_factura if con_factura is not None else any(x['iva'] > 0 for x in p['items'])
        for x in p['items']:
            items.append({'concepto': x['d'], 'importe': x['monto']})
            if lleva:
                iva += x['iva']
    return items, round(iva, 2), fecha


def presupuesto(path):
    t = pdf_text(path)
    items = []
    for l in t.split('\n'):
        m = re.match(r'\s*(.+?)\s{2,}\$\s*([\d.]+,\d{2})\s*$', l)
        if m and not re.search(r'Subtotal|Total', m[1]):
            items.append({'concepto': m[1].strip(), 'importe': ar(m[2])})
    m = re.search(r'Subtotal IVA:\s*\$\s*([\d.]+,\d{2})', t)
    fe = re.search(r'Fecha:\s*(\d{2})/(\d{2})/(\d{4})', t)
    return items, (ar(m[1]) if m else 0), (f'{fe[3]}-{fe[2]}-{fe[1]}' if fe else None)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--factura', nargs='*', default=[])
    ap.add_argument('--proforma')
    ap.add_argument('--proforma-sin-factura', nargs='*', default=[])
    ap.add_argument('--presupuesto')
    a = ap.parse_args()
    items, iva, notas, fecha = [], 0.0, [], None
    for fp in a.factura:
        try:
            it, iv, fe, nt = factura(fp); items += it; iva += iv; notas += nt; fecha = fecha or fe
        except Exception as e:
            notas.append(f'No pude leer la factura {os.path.basename(fp)} ({e.__class__.__name__}).')
    if a.proforma and not a.factura:
        it, iv, fe = proforma(a.proforma); items += it; iva += iv; fecha = fecha or fe
        notas.append('Cargada desde la proforma, sin facturas: tomé con factura a las partes que tienen IVA en la proforma.')
    for pf in a.proforma_sin_factura:
        it, iv, fe = proforma(pf, False); items += it; fecha = fecha or fe
    if a.presupuesto:
        it, iv, fe = presupuesto(a.presupuesto); items += it; iva += iv; fecha = fecha or fe
    if round(iva, 2):
        items.append({'concepto': 'IVA', 'importe': round(iva, 2)})
    print(json.dumps({'items': [x for x in items if x['importe']], 'fecha_documento': fecha, 'notas': notas}, ensure_ascii=False))


if __name__ == '__main__':
    main()
