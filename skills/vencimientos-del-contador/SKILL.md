---
name: vencimientos-del-contador
description: Lee el mail mensual del estudio contable con los vencimientos de la escribanía, los guarda en Retenot, los agenda en el calendario y avisa al celular con una notificación de Claude antes de cada vencimiento y el mismo día. La usa la tarea diaria "Retenot - vencimientos". También sirve a mano, cuando digan "¿qué vence esta semana?", "leé el mail del contador" o "agendá los vencimientos".
---

# Vencimientos del contador

Cada mes el estudio contable le manda a la escribanía un mail con los vencimientos. Esta skill hace cuatro cosas con ese mail:

1. Lo lee.
2. Guarda las fechas en Retenot, así el sobre y el tablero usan las fechas reales de esta escribanía.
3. Agenda cada vencimiento en el calendario.
4. Avisa al celular el día anterior y el mismo día, aclarando si la plata sale del sobre y cuánto hay separado.

## Reglas fijas

- El mail es **solo lectura**. Nunca mandar, responder, reenviar, borrar, archivar ni etiquetar.
- En el calendario, solo crear los eventos de Retenot. Nunca modificar ni borrar otros.
- Nunca pedir claves. Si un conector no está o no responde, no reintentes: decilo en el resumen.
- Fechas en hora de Buenos Aires, formato `AAAA-MM-DD`.

## Qué conectores hacen falta

| Dónde está el mail de la escribanía | Qué usar |
|---|---|
| Gmail, o un dominio propio en **Google Workspace** (ej. estudio@escribaniaperez.com.ar con Gmail) | Conector **Gmail** |
| Dominio propio en **Microsoft 365** (Outlook del trabajo) | Conector **Microsoft 365**. Lo tiene que habilitar el administrador de Microsoft de la escribanía, una sola vez. |
| Outlook.com, Hotmail u otro proveedor | Claude no puede leerlos. Crear en ese correo una regla que **reenvíe automáticamente** los mails del contador a una cuenta de Gmail, y conectar esa cuenta. |

Para agendar: conector **Google Calendar**, o el calendario de **Microsoft 365**. Si no hay ninguno conectado, la skill igual guarda y avisa; solo no agenda.

Para avisar: la herramienta de notificaciones de Claude. El usuario tiene que tener la app de Claude en el celular con las notificaciones permitidas. En la tarea programada, dejar activadas las notificaciones al celular.

## 1 · Estado

Llamá a `estado_vencimientos`. Te devuelve:

- `remitente` y `asunto` del mail del contador;
- los `meses` ya cargados, con su `mail_id`;
- `hoy`.

Si no hay remitente configurado, pará: pedí que corran la instalación (skill instalar-el-sobre) o configuralo con `configurar_escribania` si el usuario está presente.

## 2 · Buscar el mail

Buscá en el correo los mails de `remitente`, con `asunto` si lo hay, de los últimos 45 días. En Gmail: `from:<remitente> subject:<asunto> newer_than:45d`.

El mes sale del asunto o del cuerpo, por ejemplo "Vencimientos noviembre 2026" → `2026-11`.

- Si ese mes ya está cargado con el mismo `mail_id`, saltá al paso 4.
- Si el contador mandó una corrección (otro mail del mismo mes), procesá el más nuevo.

## 3 · Leer y guardar

Leé el mail como texto plano y armá dos listas.

**`obligaciones`**: cada una con `nombre`, `periodo`, `vence`, `concepto` y, si el mail lo dice, `quincena` y `monto`. El `concepto` va así:

| Obligación | `concepto` |
|---|---|
| Sellos CABA / AGIP / SIE | `sellos_caba` |
| Sellos ARBA / SIESBA (aclarar quincena 1 o 2) | `sellos_pba` |
| Aportes notariales de Provincia | `aportes_pba` |
| IVA mensual | `iva` |
| Aportes del Colegio de Escribanos CABA | `aportes` |
| Cualquier otra (ganancias, autónomos, cargas sociales, etc.) | `null`: no sale del sobre |

**`tareas`**: cosas con fecha que no son pagos, por ejemplo "presentar DDJJ UIF" o "mandar facturas al estudio".

Guardá con `guardar_vencimientos`, pasando: `mes`, `mail_id`, `asunto`, `mail_fecha`, `obligaciones` y `tareas`.

**Agendar.** Si hay calendario conectado, creá un evento por cada obligación y cada tarea que no esté ya agendada. Antes de crear cada uno, buscá eventos de ese día con el mismo título.

- **Título:** `Vence: <nombre> (<organismo>)`. Si sale del sobre, agregá " · sale del sobre".
- **Horario:** ese día de 9:00 a 9:30, hora de Buenos Aires.
- **Descripción:** "Agendado por Retenot desde el mail del contador (<asunto>)."
- **Recordatorios:** un día antes y 30 minutos antes.

## 4 · Avisar

Llamá a `vencimientos_a_avisar`. Devuelve lo que vence de hoy a 3 días y todavía no se avisó. De cada ítem te da:

- la `clave` y el `tipo` (`previo` o `hoy`);
- si sale del sobre;
- `separado_mes_anterior`: lo que hay que tener separado para ese organismo.

Si hay algo, mandá **una sola** notificación de Claude:

- **Primer renglón:** lo más urgente, por ejemplo "Hoy vence Sellos CABA (AGIP)".
- **Después:** un renglón por ítem. En los que salen del sobre, agregá "sale del sobre · separado $ X". Para las quincenas de ARBA, si el mail no dice el monto, poné "separado en el mes $ X".
- **Monto del mail:** si el contador mandó un monto distinto de lo separado, decilo.

Recién después de mandar la notificación, llamá a `marcar_avisados` con `mes`, `clave` y `tipo` de cada ítem.

Si no hay nada para avisar, no mandes notificación.

## 5 · Resumen corto

Al final de la tarea, en tres renglones como máximo:

- **Mail:** si se leyó un mail nuevo y de qué mes, o "sin mail nuevo".
- **Agenda:** cuántos vencimientos se agendaron.
- **Avisos:** qué se avisó, o "Sin vencimientos próximos".

Si faltó un conector (correo o calendario), decilo en una línea con qué hay que conectar.
