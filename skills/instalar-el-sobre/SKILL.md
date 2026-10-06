---
name: instalar-el-sobre
description: Instala Retenot en una escribanía. Busca la carpeta de escrituras y facturas, conecta el mail del contador y el calendario, configura la escribanía, carga las escrituras del mes, publica el tablero El Sobre y programa la revisión diaria y los avisos de vencimientos. Usar cuando digan "instalar Retenot", "armar el sobre", "configurar Retenot", "empezar con Retenot" o la primera vez que alguien usa el plugin.
---

# Instalar El Sobre de Retenot

El Sobre muestra cuánta plata de terceros tiene que tener apartada la escribanía: sellos para AGIP o ARBA, aportes para el Colegio o ARBA, IVA para ARCA. Dos tareas diarias lo mantienen al día solas: una carga las escrituras nuevas y otra lee el mail del contador, agenda los vencimientos y avisa al celular.

Los datos, las reglas de clasificación y el tablero viven en el servidor de Retenot y se usan con el conector **Retenot**. Este plugin no clasifica nada por su cuenta. Si el conector no responde o la cuenta no está activa, no hay que reemplazarlo con cálculos propios: avisá y mandá a `mi_cuenta_retenot`.

## Guía con imágenes

Si el usuario se traba en un paso que hace él (conectar la carpeta, tocar Permitir, guardar en favoritos, aprobación automática), pasale el link al paso exacto de https://retenot.com/instalar:

- abrir Claude: `#paso-1`
- agregar la carpeta: `#paso-3`
- carpeta del servidor: `#paso-4`
- conectar el mail y el calendario: `#paso-5`
- Permitir: `#paso-7`
- favoritos: `#paso-8`
- notificaciones y aprobación automática: `#paso-9`

Las escrituras **y** sus facturas o proformas tienen que estar dentro de carpetas conectadas. Si las facturas están en otra carpeta, pedí que conecte esa también.

## Reglas fijas

- Las carpetas de la escribanía son **solo lectura**: nunca escribir, mover, renombrar ni borrar ahí.
- Nunca pedir ni tipear claves fiscales (ARCA, AGIP, ARBA).
- Todo es por mes calendario, en hora de Buenos Aires.
- Con el usuario: castellano rioplatense, corto, montos como `$ 1.234.567`.

## Paso 1 · Conector

Verificá que estén las herramientas del conector Retenot (`cargar_escritura`, `tablero_mes`, `configurar_escribania`…).

Si no están, pedile al usuario que agregue el conector y que vuelva a llamarte:

> Para empezar, agregá el conector Retenot: entrá en https://claude.ai/directory/connectors/retenot, tocá **Conectar** y entrá con tu cuenta de Google. Tenés 14 días de prueba.

Después llamá a `mi_cuenta_retenot` y contale en una línea en qué plan está.

## Paso 2 · Carpeta de escrituras

Buscá en las carpetas conectadas una que tenga escrituras: archivos `.doc` o `.docx` cuyo nombre empieza con un número de 3 o 4 dígitos. Al lado tienen que estar las facturas en PDF ("comprobante-electronico", "Factura") o las proformas `.xlsx`. Mirá hasta 3 niveles de profundidad.

- Si hay una sola candidata, confirmala con el usuario mostrando 3 o 4 nombres de ejemplo.
- Si no encontrás ninguna (o no hay carpetas conectadas), preguntá exactamente:

  > **Por favor ingresá la ubicación de la carpeta con tus escrituras y facturas / proformas.**

  Con la ruta, pedí acceso a esa carpeta (si tenés una herramienta para pedir acceso a carpetas, usala; si no, explicale cómo conectarla en la app de escritorio de Claude). Si después de eso sigue sin haber escrituras ahí, decilo y pedí otra ubicación.

  **Carpetas de red (servidor de la escribanía).** Si la ruta empieza con una letra de unidad de red (`Z:\`, `S:\`…) o el pedido de acceso la rechaza, no insistas con la letra. Pedile que la conecte con el botón **Agregar carpeta**, debajo del cuadro de texto, escribiendo en la barra de direcciones del selector la ruta de red completa, con el nombre del servidor: `\\NOMBRE-DEL-SERVIDOR\carpeta\subcarpeta`. Para saber el nombre: en el Explorador de archivos, en "Este equipo", la unidad aparece como "carpeta (\\NOMBRE-DEL-SERVIDOR) (Z:)". Avisale que la tarea diaria solo puede leer esa carpeta si la compu está prendida y conectada a la red de la escribanía.

Anotá cómo nombran las carpetas: apellido del comprador, prefijos, sufijos de registro, "PBA" o localidad para Provincia.

## Paso 2b · Mail del contador y calendario

Retenot lee el mail mensual del estudio contable con los vencimientos. Preguntá dónde está el mail de la escribanía y verificá el conector que corresponde:

- **Gmail, o dominio propio en Google Workspace:** conector **Gmail**.
- **Dominio propio en Microsoft 365 (Outlook del trabajo):** conector **Microsoft 365**. Lo habilita una vez el administrador de Microsoft de la escribanía.
- **Outlook.com, Hotmail u otro proveedor:** Claude no puede leerlos. Que creen en ese correo una regla que reenvíe automáticamente los mails del contador a una cuenta de Gmail, y conecten esa cuenta.

Para agendar: **Google Calendar** (o el calendario de Microsoft 365).

Si falta un conector, pedile que lo agregue en Configuración → Conectores (retenot.com/instalar#paso-5) y seguí con lo demás: la skill de vencimientos funciona sin calendario, pero no sin correo.

Buscá en el correo los últimos mails que hablen de vencimientos y proponé el remitente y las palabras del asunto. Que el usuario confirme cuál es.

## Paso 3 · Preguntas (AskUserQuestion, en una o dos tandas)

1. Nombre de la escribanía, tal como tiene que aparecer (ej. "Escribanía Pérez").
2. Nombre del sobre digital: la cuenta o fondo donde apartan la plata (ej. "Fondo común $ Banco X").
3. Desde qué N° de escritura empieza el sobre digital. Las anteriores se toman como ya separadas. Sugerí el número más alto de este mes que encontraste en la carpeta.
4. ¿Alguna escritura nueva ya tiene sobre físico (efectivo)? Lista de N°.
5. Jurisdicciones: CABA, Provincia o las dos. Si opera en otra provincia, avisá que Retenot hoy cubre CABA y Provincia de Buenos Aires.
6. El mail del contador: remitente y palabras del asunto (lo que encontraste en el paso 2b).

Guardá todo con `configurar_escribania`:

- `escribania`
- `cuenta`
- `carpeta`: la ruta tal como la ves
- `cargar_desde`
- `fisicos`
- `mail_contador_remitente` y `mail_contador_asunto`

## Paso 4 · Primera carga

Seguí la skill **revisar-escrituras** una vez, a mano, para cargar las escrituras del mes. Mostrá el resumen. Pedile al usuario que compare una escritura contra su factura y que confirme que los números dan.

Después seguí la skill **vencimientos-del-contador** una vez: lee el último mail, guarda las fechas y las agenda.

Si el plan es Completo, preguntá cuánto hay hoy en el sobre digital y cargalo con `registrar_cuenta_aparte`.

## Paso 5 · Publicar el tablero

1. Cargá la skill `artifact-capabilities` (y la de diseño de artifacts si la pide).
2. Publicá `assets/tablero.html` de esta skill **tal cual**: los datos no van en la página, la página los lee de Retenot.
   - Título: "El Sobre · <nombre de la escribanía>".
   - Ícono: `envelope`.
   - Capabilities, exactamente así:

```json
{"mcp": {"servers": [{"server": "Retenot", "tools": ["tablero_mes", "registrar_pago", "marcar_sobre", "registrar_cuenta_aparte"]}]}}
```

3. Al abrirla, Claude le pregunta al usuario si la página puede usar Retenot: tiene que tocar **Permitir**.
4. Recomendá guardarla en favoritos:

   > Guardá esta página en la barra de favoritos de tu navegador. En el iPad o el celular, usá "Agregar a pantalla de inicio". Así el sobre queda a un toque.

5. Si alguien más tiene que mirarla (por ejemplo, el escribano), se comparte en modo lectura desde el botón Compartir. Esa persona también necesita el conector Retenot en su cuenta para ver los datos.

## Paso 6 · Revisión diaria

Creá una tarea programada con la herramienta de tareas programadas que tengas:

- **Nombre:** "Retenot: escrituras nuevas"
- **Cuándo:** días hábiles, un horario después del mediodía con minuto no redondo (ej. 13:54, hora de Buenos Aires).
- **Si la carpeta está en la compu o en el servidor (casi siempre):** la tarea **tiene** que requerir esta computadora y llevar la carpeta de escrituras. Si tu herramienta lo permite, marcalo al crearla. Si no, decile al usuario que abra la tarea en Tareas programadas y active **Requerir esta computadora** (retenot.com/instalar#paso-8). Sin eso la tarea corre en la nube y no ve la carpeta.
- **Prompt** (completá la carpeta):

```
Usá la skill revisar-escrituras del plugin Retenot para cargar en Retenot las escrituras nuevas de la carpeta <RUTA>. Al final, dejá un resumen corto: escrituras cargadas, cuáles hay que revisar y cuáles quedaron pendientes.
```

Creá una segunda tarea programada:

- **Nombre:** "Retenot: vencimientos"
- **Cuándo:** días hábiles a la mañana, con minuto no redondo (ej. 8:47, hora de Buenos Aires).
- **No necesita la computadora:** usa el correo y el calendario conectados.
- **Notificaciones:** activadas al celular.
- **Prompt:**

```
Usá la skill vencimientos-del-contador del plugin Retenot: leé el mail del contador si llegó uno nuevo, guardá y agendá los vencimientos, y mandame una notificación con lo que vence de hoy a 3 días. Al final, dejá un resumen corto.
```

Decí en una línea qué modo de aprobación le quedó a cada tarea.

## Paso 7 · Permisos para que corra sola

Explicalo con estas palabras:

> Para que Retenot trabaje solo todos los días necesito cuatro cosas:
>
> 1. **Acceso a la carpeta** de escrituras. Ya lo diste; es solo lectura: Retenot nunca cambia nada ahí.
> 2. **Interruptores en Tareas programadas.** En "Retenot: escrituras nuevas", activá **Requerir esta computadora** y **Aprobar automáticamente**. En "Retenot: vencimientos", activá **Aprobar automáticamente** y las **notificaciones al celular**.
> 3. **Notificaciones de Claude en el celular.** Instalá la app de Claude, entrá con tu cuenta y permití las notificaciones. Por ahí llegan los avisos de vencimientos.
> 4. **La compu prendida** con la app de Claude abierta a la hora de la revisión de escrituras, si la carpeta está en esta compu o en un disco de la red.
>
> En Configuración → Conectores podés marcar Retenot, Gmail y Google Calendar como "Permitir siempre". Así no te pregunta cada vez. Retenot solo lee tu correo: nunca manda, borra ni responde mails.

## Cierre

En tres renglones:

- Dónde está el tablero (link).
- A qué hora corren la revisión de escrituras y la de vencimientos.
- Que para registrar un pago, pasar una escritura al sobre físico o cargar el saldo, lo pueden hacer desde el tablero o pedírselo a Claude.
