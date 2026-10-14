---
name: revisar-escrituras
description: Revisa la carpeta de escrituras de la escribanía y carga en Retenot las escrituras nuevas con sus facturas o proformas. La usa la tarea diaria "Retenot - escrituras nuevas". También sirve a mano, cuando digan "cargá las escrituras nuevas", "actualizá el sobre" o "revisá la carpeta".
---

# Revisar escrituras nuevas

Las instrucciones de esta tarea viven en el servidor de Retenot, así hay un solo texto y siempre está al día.

1. Llamá a `instrucciones_retenot` con `tarea: "revisar_escrituras"`.
2. Seguí lo que devuelve al pie de la letra.

Si las herramientas del conector Retenot no están, pedile al usuario que lo agregue y vuelva a llamarte:

> Para empezar, agregá el conector Retenot: en la app de Claude de escritorio entrá en Personalización → Conectores, buscá **Retenot**, tocá **Conectar** y entrá con tu cuenta de Google. Tenés 14 días de prueba. Guía con imágenes: https://retenot.com/instalar#paso-2

Si el conector no responde o la cuenta no está activa, no lo reemplaces con cálculos propios: avisá y usá `mi_cuenta_retenot`.
