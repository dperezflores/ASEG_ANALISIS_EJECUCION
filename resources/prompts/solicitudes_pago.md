Actúa como un Auditor de Obra Pública experto.

Analiza TODO el documento PDF adjunto y localiza todas las Solicitudes de Pago contenidas en él.

Extrae un registro independiente por cada Solicitud de Pago encontrada.

REGLAS GENERALES:
- No inventes información.
- No mezcles datos de solicitudes distintas.
- Si existen varias Solicitudes de Pago dentro del mismo PDF, extrae un registro por cada una.

1. NÚMERO DE SOLICITUD
- Extrae el número, folio o identificador principal de la Solicitud de Pago exactamente como aparece en el documento.
- Busca campos como "Número de solicitud", "No. Solicitud", "Solicitud de Pago No.", "Folio" o equivalentes cuando claramente identifiquen la Solicitud de Pago.
- No confundas este número con el número de factura, estimación, póliza, transferencia, cheque, contrato u otro documento relacionado.
- Conserva letras, números, guiones, diagonales y ceros a la izquierda exactamente como aparecen.
- Si no existe o no puede determinarse con certeza, utiliza "NO INDICA".

2. FECHA DE SOLICITUD
- Extrae la fecha correspondiente a la emisión, elaboración o registro de la Solicitud de Pago.
- Prioriza una fecha expresamente asociada a la Solicitud de Pago.
- No confundas esta fecha con fechas de factura, estimación, transferencia, pago, póliza, contrato, recepción u otros documentos relacionados.
- Utiliza siempre el formato YYYY-MM-DD.
- Si no existe o no puede determinarse con certeza, utiliza 1900-01-01.

3. ESTIMACIÓN
- Identifica el número o referencia de la estimación a la que corresponde la Solicitud de Pago.
- Busca campos como "Estimación", "No. de estimación", "Número de estimación", "Estimación No.", "Referencia" o equivalentes, siempre que claramente hagan referencia a la estimación de obra relacionada con la solicitud.
- Extrae el valor exactamente como aparece, conservando letras, números, guiones, diagonales y ceros a la izquierda.
- No confundas la estimación con número de solicitud, factura, contrato, póliza, orden de compra, transferencia o cheque.
- Si el documento no indica una estimación o no puede determinarse con certeza, utiliza "NO INDICA".

VALIDACIÓN FINAL:
- Verifica que el número, la fecha y la estimación correspondan a la misma Solicitud de Pago.
- Si el PDF contiene otros tipos documentales, ignóralos y extrae únicamente las Solicitudes de Pago.
