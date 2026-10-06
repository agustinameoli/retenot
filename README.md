# Retenot · El Sobre

Plugin de Retenot para escribanías de la Ciudad y de la Provincia de Buenos Aires. Todos los días revisa la carpeta de escrituras de la escribanía, lee las facturas y proformas de cada escritura nueva y separa la plata de terceros de los honorarios: sellos para AGIP o ARBA, aportes y derechos para el Colegio de Escribanos o ARBA, e IVA para ARCA. Con eso arma **El Sobre**, un tablero que muestra cuánto tiene que haber apartado en el mes, por organismo y por escritura, y cuándo vence cada pago.

Guía de instalación con imágenes: https://retenot.com/instalar

## Qué incluye

- **instalar-el-sobre**: la primera vez. Encuentra la carpeta de escrituras (o pide su ubicación), hace cuatro preguntas, carga el mes, publica el tablero El Sobre y programa la revisión diaria.
- **revisar-escrituras**: la tarea de todos los días hábiles. Lee los papeles de las escrituras nuevas y los carga en Retenot.
- **Conector Retenot** (`https://app.retenot.com/mcp`): el servidor de Retenot, con inicio de sesión de Google. Ahí viven los datos de la escribanía, las reglas de clasificación y los cálculos.

## Requisitos

- Claude con Cowork y la app de escritorio, en una computadora que vea la carpeta de escrituras.
- Una cuenta de Retenot: 14 días de prueba gratis y después plan Básico o Completo, que se paga con Mercado Pago.

## Qué datos se usan y adónde van

- **Carpeta de escrituras**: el plugin solo la **lee**. Nunca escribe, mueve ni borra archivos. Los archivos no salen de la computadora ni de Claude.
- **Lo que se envía a Retenot** (app.retenot.com), por cada escritura: número, fecha, tipo de acto, jurisdicción, los nombres de las partes como figuran en la carpeta y los renglones de la factura o proforma (concepto e importe). También el nombre de la escribanía, el nombre de su cuenta aparte, la ruta de la carpeta, los pagos y el saldo que el usuario registre.
- **Nada más**: no se envían los PDF ni los documentos, ni datos de identidad, domicilios o CUIT de las partes. El plugin no se conecta a ningún otro servicio.
- **Para qué**: para calcular y mostrar el sobre del mes de esa escribanía. Los datos no se comparten con terceros ni se usan para otra cosa.
- **Cuánto tiempo**: mientras la cuenta esté activa. Se pueden borrar pidiéndolo a meoliagustina@gmail.com.

Política de privacidad: https://retenot.com/privacidad · Términos: https://retenot.com/terminos

## Soporte

https://retenot.com · meoliagustina@gmail.com

Los importes son una referencia y no reemplazan la liquidación oficial ni el criterio del escribano.
