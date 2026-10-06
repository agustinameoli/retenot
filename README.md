# Retenot · El Sobre

Plugin de Retenot para escribanías de la Ciudad y de la Provincia de Buenos Aires. Todos los días revisa la carpeta de escrituras de la escribanía, lee las facturas y proformas de cada escritura nueva y separa la plata de terceros de los honorarios: sellos para AGIP o ARBA, aportes y derechos para el Colegio de Escribanos o ARBA, e IVA para ARCA. Con eso arma **El Sobre**, un tablero que muestra cuánto tiene que haber apartado en el mes, por organismo y por escritura. Además lee el mail mensual del estudio contable con los vencimientos, los agenda en el calendario y avisa al celular con una notificación de Claude el día anterior y el día del vencimiento.

Guía de instalación con imágenes: https://retenot.com/instalar

## Qué incluye

- **instalar-el-sobre**: la primera vez. Encuentra la carpeta de escrituras (o pide su ubicación), hace cuatro preguntas, carga el mes, publica el tablero El Sobre y programa la revisión diaria.
- **revisar-escrituras**: la tarea de todos los días hábiles. Lee los papeles de las escrituras nuevas y los carga en Retenot.
- **vencimientos-del-contador**: la otra tarea diaria. Lee el mail del contador, guarda los vencimientos en Retenot, los agenda y avisa al celular.
- **Conector Retenot** (`https://app.retenot.com/mcp`): el servidor de Retenot, con inicio de sesión de Google. Ahí viven los datos de la escribanía, las reglas de clasificación y los cálculos.

## Requisitos

- Claude con Cowork y la app de escritorio, en una computadora que vea la carpeta de escrituras.
- Una cuenta de Retenot: 14 días de prueba gratis y después plan Básico o Completo, que se paga con Mercado Pago.
- Para los vencimientos: el conector Gmail (Gmail o Google Workspace) o Microsoft 365 (cuenta de trabajo), y Google Calendar o el calendario de Microsoft 365 para agendar. Para los avisos, la app de Claude en el celular con las notificaciones permitidas.

## Qué datos se usan y adónde van

- **Carpeta de escrituras**: el plugin solo la **lee**. Nunca escribe, mueve ni borra archivos. Los archivos no salen de la computadora ni de Claude.
- **Lo que se envía a Retenot** (app.retenot.com), por cada escritura: número, fecha, tipo de acto, jurisdicción, los nombres de las partes como figuran en la carpeta y los renglones de la factura o proforma (concepto e importe). También el nombre de la escribanía, el nombre de su cuenta aparte, la ruta de la carpeta, los pagos y el saldo que el usuario registre.
- **Correo**: el plugin solo **lee** los mails del remitente que configura el usuario (el estudio contable). A Retenot le manda el mes, el asunto, el identificador del mail y cada vencimiento (nombre, período, fecha y, si figura, el monto). No manda el texto del mail. Nunca envía, responde, borra ni etiqueta correos.
- **Calendario**: crea un evento por vencimiento en el calendario del usuario, con recordatorios. No modifica ni borra otros eventos.
- **Nada más**: no se envían los PDF ni los documentos, ni datos de identidad, domicilios o CUIT de las partes. Fuera de Retenot, el correo y el calendario del propio usuario, el plugin no se conecta a ningún otro servicio.
- **Para qué**: para calcular y mostrar el sobre del mes de esa escribanía. Los datos no se comparten con terceros ni se usan para otra cosa.
- **Cuánto tiempo**: mientras la cuenta esté activa. Se pueden borrar pidiéndolo a meoliagustina@gmail.com.

Política de privacidad: https://retenot.com/privacidad · Términos: https://retenot.com/terminos

## Soporte

https://retenot.com · meoliagustina@gmail.com

Los importes son una referencia y no reemplazan la liquidación oficial ni el criterio del escribano.
