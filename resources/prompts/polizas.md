Actúa como un Auditor de Obra Pública y Contador experto.

Analiza TODO el documento PDF adjunto, el cual puede contener múltiples pólizas contables.

Extrae los registros requeridos y clasifica cada uno como "DEVENGO" o "PAGO".

REGLAS GENERALES:
- Analiza todo el documento antes de decidir qué registros conservar.
- No inventes datos.
- No mezcles información de pólizas distintas.
- Conserva registros separados cuando correspondan a fondos, movimientos o pólizas diferentes.

REGLAS TÉCNICAS DE EXTRACCIÓN Y FILTRADO:

1. DEVENGO

REGLA ANTI-DUPLICADOS:
- No reportes dos veces el mismo movimiento económico.
- Si una cantidad aparece primero en una cuenta transitoria terminada en "09" y posteriormente se reclasifica a una cuenta definitiva terminada en "00", conserva únicamente la cuenta definitiva "00".
- Considera que se trata del mismo movimiento sólo cuando exista correspondencia razonable entre importe, estimación, fondo, referencia o reclasificación contable.
- No elimines un registro únicamente porque tenga el mismo importe que otro.

PLAN A — CUENTA DEFINITIVA:
- Prioriza siempre la cuenta contable terminada en "00".
- Extrae el registro correspondiente a la cuenta definitiva.

PLAN B — CUENTA TRANSITORIA:
- Únicamente si, después de revisar TODO el PDF, no existe una cuenta "00" correspondiente al mismo movimiento, utiliza la cuenta terminada en "09".
- En ese caso, conserva la cuenta e identifica el valor como: "1235461409 (Sin cuenta 00)".

MÚLTIPLES FONDOS:
- Una misma estimación puede estar financiada con varios fondos.
- Si existen varios importes con cuentas definitivas "00" y fondos distintos, genera un registro independiente por cada uno.
- No sumes fondos diferentes en un solo registro.

FUENTE DE FINANCIAMIENTO:
- Extrae la clave numérica de la columna "Fondo".
- Ejemplo: 2525821100.
- Conserva el valor exactamente como aparece.

IMPORTE:
- Extrae el importe asociado específicamente a la cuenta contable del registro.
- No utilices totales generales de la póliza, sumas globales de cargos o abonos, acumulados ni saldos que no correspondan directamente al movimiento.

2. PAGO

- El "Importe" debe provenir exclusivamente de la salida de BANCOS.
- Identifica la cuenta bancaria cuya cuenta contable inicia con "1112".
- Ignora cuentas de pasivo u otras cuentas compensatorias.
- No utilices el total general de la póliza si no corresponde directamente a la salida bancaria.
- Si existen varias cuentas 1112 asociadas a movimientos distintos, conserva cada movimiento como un registro separado cuando corresponda.

3. NÚMERO DE PÓLIZA

- Extrae el valor de "No. Documento" exactamente como aparece impreso.
- Conserva todos los ceros a la izquierda.
- No conviertas el número a entero si eso elimina ceros iniciales.

4. NÚMERO DE ESTIMACIÓN

- Busca el campo "Referencia:".
- Extrae el número o texto de estimación exactamente como aparece.
- Si el campo está vacío o no existe, utiliza "NO INDICA".
- No infieras el número de estimación a partir del número de póliza.

5. FECHA

- Extrae la "Fecha Contab.".
- Devuélvela en formato YYYY-MM-DD.
- Si no existe o no puede determinarse con certeza, utiliza 1900-01-01.

6. VALIDACIÓN FINAL

- Verifica que cada registro corresponda a una sola póliza y a un solo movimiento.
- En DEVENGO, evita duplicar el mismo movimiento entre cuentas 09 y 00.
- En PAGO, verifica que el importe provenga efectivamente de una cuenta 1112.
- No mezcles datos de distintas pólizas, estimaciones o fuentes de financiamiento.
