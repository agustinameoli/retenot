---
name: revisar-escrituras
description: Revisa la carpeta de escrituras de la escribanía y carga en Retenot las escrituras nuevas con sus facturas o proformas. La usa la tarea diaria "Retenot - escrituras nuevas". También sirve a mano, cuando digan "cargá las escrituras nuevas", "actualizá el sobre" o "revisá la carpeta".
---

# Revisar escrituras nuevas

Leés los papeles de cada escritura y mandás sus renglones a Retenot con `cargar_escritura`. Retenot decide qué es sellos, aportes, IVA u honorarios: **vos no clasificás**. Si el conector no responde o la cuenta no está activa, no sigas: terminá con lo que dijo Retenot.

## Reglas fijas

- La carpeta es **solo lectura**. Nunca escribir, mover, renombrar ni borrar ahí.
- Si no llegás a la compu o a la carpeta, no reintentes: terminá diciendo que no estaba disponible.
- No cargues escrituras con N° menor a `cargar_desde`: esas ya estaban separadas antes de Retenot. Las que están en `fisicos` sí se cargan; Retenot las pone solas en el sobre físico.
- Se cargan solo las escrituras firmadas en el mes actual. Si es la primera corrida del mes, también las del mes anterior firmadas desde `ultima_revision`.

## 1 · Estado

Llamá a `estado_importacion`. Te devuelve:

- `carpeta`
- `cargar_desde`
- `fisicos`
- `ultimo_numero`
- `ultima_revision`
- `pendientes`
- `cargadas` (por mes)

Si no está configurado, pará y pedí que corran la instalación (skill instalar-el-sobre).

## 2 · Buscar

En la carpeta, buscá los `.doc`/`.docx` modificados en los últimos 45 días cuyo nombre empieza con un N° de 3 o 4 dígitos.

- Si un archivo no tiene número en el nombre, leé el comienzo del texto: "N° 678" o "ESCRITURA NÚMERO…". Para un `.docx`, el texto está en `word/document.xml` adentro del zip.
- Ignorá `~$*`, copias simples, minutas y certificados.

**Candidatos** = N° ≥ `cargar_desde`, que no estén en `cargadas`, más los `pendientes`.

## 3 · Clasificar el acto

- **No se cargan:** poderes, revocaciones, actas, certificaciones y autorizaciones. Igual cuentan para el número más alto.
- **Se cargan:** todo lo demás (compraventa, hipoteca, cancelación, donación, usufructo, tracto, división, cesión…).

## 4 · Papeles de cada escritura

**Dónde buscar.** En la carpeta de la operación: la del archivo, o una de primer nivel con un apellido del nombre del archivo.

**Qué buscar:**

- **Facturas:** PDFs "comprobante-electronico" o "Factura", hasta 2 niveles adentro. Si hay dos casi iguales al mismo CUIT, usá la de número mayor y dejalo en `nota`.
- **Proforma `.xlsx`:** la "definitiva" o la de fecha más nueva en el nombre. Las proformas de una parte sin factura son `.xlsx` con "proforma" dentro de la carpeta FACTURA(S).
- **Cancelaciones:** `Presupuesto_*.pdf`.

**Si no hay nada:** va a pendientes con el motivo.

## 5 · Extraer los renglones

Si los archivos están en la compu y tu shell no los ve, pasalos al espacio de trabajo. Corré el script de esta skill:

```
python3 <carpeta de esta skill>/scripts/extraer.py --factura F1.pdf F2.pdf [--proforma P.xlsx] [--proforma-sin-factura X.xlsx] [--presupuesto Presupuesto_1.pdf]
```

Si falta algo: `pip install openpyxl`. `pdftotext` viene en `poppler-utils`.

El script devuelve `{items, fecha_documento, notas}`. Si una factura no se pudo leer (por ejemplo, un escaneo), abrí el PDF, leelo vos y armá los renglones a mano: `{concepto, importe}` por renglón, más un renglón "IVA" con el IVA total.

## 6 · Datos de la escritura

- **`fecha`:** la fecha de firma que dice el texto de la escritura, convertida de letras a `AAAA-MM-DD`. **Nunca** uses la fecha de la factura.
- **`cliente`:** las partes, sacadas del nombre de la carpeta y limpias (sin prefijos, códigos ni sufijos de registro). Van separadas con " / ", **con el apellido del comprador primero**. Agregá el banco si interviene.
- **`acto`:** prolijo (Compraventa, Hipoteca, Cancelación de hipoteca…).
- **`jurisdiccion`:**
  - `PBA` si la carpeta o el archivo dicen PBA, Pcia, Provincia o el nombre de una localidad de Provincia;
  - si no, `CABA`.
- **`nota`:** junta las `notas` del script y lo que viste. Por ejemplo, si la escritura dice cuánto se retuvo de sellos y difiere en más de $100 de lo facturado.

## 7 · Cargar

Por cada escritura, llamá a `cargar_escritura` con estos campos:

- `numero`
- `fecha`
- `cliente`
- `acto`
- `jurisdiccion`
- `items`
- `nota` (si hay)

No mandes `sobre`: Retenot ya sabe cuáles son físicas.

Al terminar, llamá a `cerrar_revision` con:

- `ultimo_numero`: el N° más alto que viste, incluidos poderes y actas.
- `pendientes`: `[{numero, nombre, motivo}]`, con lo que no se pudo cargar.

## 8 · Resumen corto

- **Cargadas:** N°, partes y total para terceros. Usá el `total` que devuelve Retenot para cada una.
- **Para revisar:** las que Retenot marcó y por qué.
- **Fuera de la carga:** poderes y actas omitidos, escrituras viejas ignoradas y pendientes.
- **Cierre:** "Si alguna de estas tiene sobre físico, pasala desde el tablero o avisame."
