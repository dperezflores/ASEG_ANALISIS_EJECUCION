Actúa como un Auditor de Obra Pública y Contador experto.

Analiza TODO el documento PDF adjunto, el cual puede contener múltiples pólizas contables.

Extrae los registros requeridos y clasifica cada uno como "DEVENGO" o "PAGO".

REGLAS GENERALES:
- Analiza todo el documento antes de decidir qué registros conservar.
- No inventes datos.
- No mezcles información de pólizas distintas.
- Conserva registros separados cuando correspondan a fondos, movimientos o pólizas diferentes.
- Antes de aplicar reglas específicas, identifica el formato o estructura contable de la póliza.
- No fuerces reglas propias de SAP sobre pólizas que claramente utilizan una estructura contable distinta.

IDENTIFICACIÓN DEL FORMATO CONTABLE:

A) FORMATO SAP O ESTRUCTURA EQUIVALENTE:
- Aplica las reglas tradicionales de cuentas transitorias terminadas en "09" y cuentas definitivas terminadas en "00" cuando el documento presente esa estructura.
- Si existe una columna o campo explícito denominado "Fondo", utiliza ese valor conforme a las reglas SAP indicadas más adelante.

B) FORMATO TIPO LEÓN / ESTRUCTURA DE "COMBINACIÓN":
- Considera este formato cuando el documento presente elementos como "Póliza Contable de Cuentas por Pagar", una columna o campo "Combinación", "Fecha Contable" o "Fecha Contab.", "Fte. de Financiamiento", "No. Documento" o "Nombre de Asiento".
- En este formato NO apliques automáticamente las reglas de terminación "00" y "09".
- Cuando la "Combinación" esté formada por segmentos separados por guiones, cuenta las posiciones desde 1, de izquierda a derecha.
- La CUENTA CONTABLE corresponde a la posición 2 de la "Combinación".
- El FONDO corresponde a la posición 11 de la "Combinación".
- Conserva exactamente los caracteres y ceros de cada segmento.
- Ejemplo: para "01-12362010001-999999-04-1816-226-H02-K100288-62201-2-11-11AA01-3100", la cuenta contable es "12362010001" y el fondo es "11".

REGLAS TÉCNICAS DE EXTRACCIÓN Y FILTRADO:

1. DEVENGO

REGLA ANTI-DUPLICADOS PARA SAP O ESTRUCTURA EQUIVALENTE:
- No reportes dos veces el mismo movimiento económico.
- Si una cantidad aparece primero en una cuenta transitoria terminada en "09" y posteriormente se reclasifica a una cuenta definitiva terminada en "00", conserva únicamente la cuenta definitiva "00".
- Considera que se trata del mismo movimiento sólo cuando exista correspondencia razonable entre importe, estimación, fondo, referencia o reclasificación contable.
- No elimines un registro únicamente porque tenga el mismo importe que otro.

PLAN A — CUENTA DEFINITIVA EN SAP:
- Prioriza siempre la cuenta contable terminada en "00" cuando el documento corresponda a formato SAP o equivalente.
- Extrae el registro correspondiente a la cuenta definitiva.

PLAN B — CUENTA TRANSITORIA EN SAP:
- Únicamente si, después de revisar TODO el PDF, no existe una cuenta "00" correspondiente al mismo movimiento, utiliza la cuenta terminada en "09".
- En ese caso, conserva la cuenta e identifica el valor como: "1235461409 (Sin cuenta 00)".

DEVENGO EN FORMATO TIPO LEÓN / "COMBINACIÓN":
- Identifica el renglón que representa el reconocimiento contable del costo o devengo de la obra.
- Cuando exista una cadena "Combinación", reporta como "Cuenta contable" solamente el segmento de la posición 2, no toda la cadena completa.
- No apliques la regla de terminación "00" o "09" si la estructura del documento no corresponde a SAP.

MÚLTIPLES FONDOS:
- Una misma estimación puede estar financiada con varios fondos.
- Si existen varios importes con fondos distintos, genera un registro independiente por cada uno cuando correspondan a movimientos diferenciables.
- No sumes fondos diferentes en un solo registro.

FUENTE DE FINANCIAMIENTO Y FONDO:
- La identificación del origen del recurso es crítica.
- Cuando exista un campo explícito denominado "Fte. de Financiamiento", "Fuente de Financiamiento", "Origen del Recurso" o equivalente, úsalo como fuente primaria para clasificar el recurso.
- Prioriza siempre la descripción expresa del documento sobre cualquier inferencia basada únicamente en códigos.
- Normaliza conceptualmente la fuente como MUNICIPAL, ESTATAL, FEDERAL u OTRA cuando el texto permita identificarla claramente.
- No infieras que un recurso es municipal, estatal o federal sólo por el código del fondo si existe una descripción expresa que indique lo contrario.

FUENTE DE FINANCIAMIENTO EN SAP:
- Si el formato es SAP y existe una columna "Fondo", extrae la clave numérica de esa columna.
- Ejemplo: 2525821100.
- Conserva el valor exactamente como aparece.

FUENTE DE FINANCIAMIENTO EN FORMATO TIPO LEÓN / "COMBINACIÓN":
- Extrae primero la descripción expresa del campo "Fte. de Financiamiento" o equivalente.
- Extrae además el fondo de la posición 11 de la cadena "Combinación".
- En el campo de salida "Fuente de financiamiento", devuelve ambos datos en una sola cadena con el formato: "<descripción expresa> | Fondo <valor>".
- Ejemplo: si el documento indica "Fte. de Financiamiento: Recursos Municipales" y la posición 11 de la combinación es "11", devuelve: "Recursos Municipales | Fondo 11".
- Si existe descripción expresa pero no puede determinarse el fondo, devuelve sólo la descripción expresa.
- Si existe fondo pero no descripción expresa, devuelve "Fondo <valor>" sin inventar el origen del recurso.

IMPORTE:
- Extrae el importe asociado específicamente a la cuenta contable del registro.
- No utilices totales generales de la póliza, sumas globales de cargos o abonos, acumulados ni saldos que no correspondan directamente al movimiento.

2. PAGO

- El "Importe" debe provenir exclusivamente de la salida de BANCOS.
- En formatos donde la cuenta bancaria se identifique por cuenta contable, prioriza la cuenta que inicia con "1112".
- Ignora cuentas de pasivo u otras cuentas compensatorias.
- No utilices el total general de la póliza si no corresponde directamente a la salida bancaria.
- Si existen varias cuentas bancarias asociadas a movimientos distintos, conserva cada movimiento como un registro separado cuando corresponda.

3. NÚMERO DE PÓLIZA

- Extrae el valor de "No. Documento" exactamente como aparece impreso cuando ese campo exista.
- Si el formato utiliza otro campo equivalente para identificar la póliza, extrae ese identificador exactamente como aparece.
- Conserva todos los ceros a la izquierda.
- No conviertas el número a entero si eso elimina ceros iniciales.

4. NÚMERO DE ESTIMACIÓN

- Busca el campo "Referencia:" o un campo equivalente que identifique la estimación.
- Extrae el número o texto de estimación exactamente como aparece.
- Si el campo está vacío o no existe, utiliza "NO INDICA".
- No infieras el número de estimación a partir del número de póliza.

5. FECHA

- Extrae la "Fecha Contab." o "Fecha Contable".
- Devuélvela en formato YYYY-MM-DD.
- Si no existe o no puede determinarse con certeza, utiliza 1900-01-01.

6. VALIDACIÓN FINAL

- Verifica que cada registro corresponda a una sola póliza y a un solo movimiento.
- En formato SAP, evita duplicar el mismo movimiento entre cuentas 09 y 00.
- En formato tipo León, verifica que la cuenta contable provenga de la posición 2 de la "Combinación" y el fondo de la posición 11.
- En PAGO, verifica que el importe provenga efectivamente de la salida bancaria correspondiente.
- Verifica que la fuente de financiamiento respete primero el texto explícito del documento y después, como dato complementario, el fondo identificado.
- No mezcles datos de distintas pólizas, estimaciones o fuentes de financiamiento.
