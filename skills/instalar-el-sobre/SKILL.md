---
name: instalar-el-sobre
description: Instala Retenot en una escribanía. Busca la carpeta de escrituras y facturas, conecta el mail del contador y el calendario, configura la escribanía, carga las escrituras del mes, publica el tablero El Sobre y programa la revisión diaria y los avisos de vencimientos. Usar cuando digan "instalar Retenot", "armar el sobre", "configurar Retenot", "empezar con Retenot" o la primera vez que alguien usa el plugin.
---

# Instalar El Sobre de Retenot

Las instrucciones de esta tarea viven en el servidor de Retenot, así hay un solo texto y siempre está al día.

1. Llamá a `instrucciones_retenot` con `tarea: "instalar"`.
2. Seguí lo que devuelve al pie de la letra.

Si las herramientas del conector Retenot no están, pedile al usuario que lo agregue y vuelva a llamarte:

> Para empezar, agregá el conector Retenot: en la app de Claude de escritorio entrá en Personalización → Conectores, buscá **Retenot**, tocá **Conectar** y entrá con tu cuenta de Google. Tenés 14 días de prueba. Guía con imágenes: https://retenot.com/instalar#paso-2

Si el conector no responde o la cuenta no está activa, no lo reemplaces con cálculos propios: avisá y usá `mi_cuenta_retenot`.
