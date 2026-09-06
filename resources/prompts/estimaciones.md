Actúa como un Auditor de Obra Pública experto.

Analiza TODO el documento adjunto y localiza todas las carátulas de estimación contenidas en él.

Extrae un registro por cada carátula de estimación encontrada.

REGLAS GENERALES:
- Si un dato numérico no existe, utiliza 0.0.
- Para todas las fechas utiliza el formato YYYY-MM-DD.
- Si una fecha no existe o no puede determinarse con certeza, utiliza 1900-01-01.
- No inventes datos que no estén contenidos o claramente inferidos del documento.

REGLAS ESTRICTAS DE EXTRACCIÓN:

1. NUMERO DE ESTIMACIÓN
- Extrae el valor exactamente como aparece en el documento.
- Conserva números, letras, paréntesis y tipo de estimación.
- Ejemplo: "3 (TRES) NORMAL".

2. FECHA DE ELABORACIÓN O DE ESTIMACIÓN
- Extrae la fecha correspondiente a la elaboración, presentación o fecha de la estimación.
- No confundas esta fecha con las fechas del periodo de ejecución.

3. PERIODO DE EJECUCIÓN
- Para "De (Periodo de ejecución)", busca expresiones como:
  "PERIODO DEL", "DE:", "DEL:" o equivalentes.
- Para "Hasta (Periodo de ejecución)", busca expresiones como:
  "AL:", "HASTA:" o equivalentes.
- Convierte los nombres de los meses a su número correspondiente.
- Devuelve ambas fechas en formato YYYY-MM-DD.

4. IMPORTE SIN IVA, IVA E IMPORTE CON IVA
- Extrae cada importe de la carátula de la estimación.
- Si el "Importe con IVA" no aparece expresamente, calcúlalo como:
  Importe sin IVA + IVA.
- No confundas estos importes con acumulados, saldos o importes del contrato.
- No confundas importes de esta estimación con acumulados, estimación anterior, estimado a la fecha, saldo por ejercer o monto contratado.

5. IMPORTE DE ANTICIPO
- Corresponde al monto total del anticipo otorgado para el contrato.
- Generalmente aparece en la sección de datos del contrato con textos como:
  "MONTO TOTAL DE ANTICIPO", "ANTICIPO OTORGADO" o equivalentes.
- Nunca utilices aquí el importe amortizado en la estimación.
- Si no se identifica el monto total del anticipo, utiliza 0.0.

6. AMORTIZACIÓN
- Corresponde exclusivamente al descuento por amortización de anticipo aplicado en ESA estimación.
- Puede aparecer como:
  "AMORTIZACIÓN DE ANTICIPO",
  "AMORTIZACION ANTICIPO",
  "AMORTIZADO"
  o expresiones equivalentes.
- No utilices aquí el monto total del anticipo del contrato.

7. DEDUCCIONES, SANCIÓN Y RETENCIÓN
- Nunca repitas el mismo importe en más de uno de estos campos.
- Si el documento identifica expresamente un importe como "Sanción", colócalo únicamente en "Sancion".
- Si identifica un importe como "Retención", colócalo únicamente en "Retencion".
- "Deducciones" se utiliza únicamente para otros descuentos que no correspondan a sanción ni retención.

8. PRECISIÓN
- Prioriza los valores contenidos en la carátula de cada estimación.
- Si el PDF contiene varias estimaciones, no mezcles datos entre una estimación y otra.
- Verifica que cada periodo, importe, anticipo, amortización y descuento corresponda a la estimación correcta.
