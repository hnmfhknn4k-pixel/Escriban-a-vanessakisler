# Plantilla de compraventa de automotor

También está disponible **Compraventa privada de automotor, certificación y protocolización**, un borrador conjunto derivado de los tres modelos aportados. Sus tres piezas mantienen referencias comunes y campos pendientes; no constituye testimonio autorizado. Revisar `docs/compraventa-automotor.md` para el fundamento legal, instrucciones oficiales de DGR y verificaciones pendientes. Las adaptaciones nuevas muestran resúmenes sin datos del caso y exigen aceptación previa en la interfaz.

Origen: `MODELO CV AUTOMOTOR.doc`, aportado por la usuaria. El original se conserva sin modificar en los adjuntos de la tarea. Se entregan por separado una conversión DOCX del original y una plantilla adaptada. El original DOC y su conversión no se incorporan al catálogo público del código: se distribuye solamente la plantilla preparada sin metadatos de autor del modelo.

## Conversión y conservación

Se convirtió localmente con LibreOfficeDev 26.8.0.0.alpha0 a DOCX. No se envió el documento a un proveedor de IA. Se comparó el texto del DOC exportado directamente a TXT con el del DOCX y coincidió normalizando únicamente espacios y saltos. Esto verifica el contenido textual, no certifica una maquetación idéntica en Word o en la impresión. La copia convertida conserva los datos y márgenes del modelo original; no está aprobada ni se presenta como plantilla normativa.

El modelo heredaba aproximadamente 4/1/4/2 cm en márgenes superior/inferior/interior/exterior. Esos valores no se adoptaron como exigencia legal. Los borradores conservan el formato de referencia; la aprobación notarial requiere el perfil técnico único validado de la app y el cotejo de impresión ya documentados en `fuentes.md`.

## Adaptaciones visibles

La plantilla conserva la estructura del contrato y sus cláusulas de objeto, precio, tradición, declaración, procedencia, domicilios e intervención notarial. Hay 14 adaptaciones de párrafos registradas antes/después en `templates/automotor.json`, visibles en la interfaz antes de abrir el borrador.

Se sustituyeron nombres de ejemplo, ciudad y fecha, nacionalidad, capacidad y estado civil, documentos, domicilios, datos del vehículo, moneda y precio en letras/cifras, datos de pago, hora y circunstancias de entrega, antecedentes e inscripción, datos profesionales y referencia al papel notarial por campos pendientes. No se trasladan como hechos de un nuevo contrato la recepción total del precio, la ausencia de gravámenes, la tradición efectiva ni la condición tributaria del vendedor.

Hay 49 campos y avisos pendientes distintos. Su número no constituye un listado exhaustivo de requisitos jurídicos: la escribana debe revisar también todo el texto fijo, la adecuación de las cláusulas y los documentos exigibles para el acto concreto. Las declaraciones tributarias y la carta de pago requieren corroboración y redacción profesional según la evidencia.

## Uso en la app

1. Ingresar con cuenta y TOTP.
2. Abrir **Plantillas revisables → Compraventa de automotor**.
3. Examinar **Revisar adaptaciones del modelo** y confirmar que se trata de un borrador pendiente de completar y revisar.
4. Pulsar **Abrir borrador de automotor**. Se crea un expediente propio cifrado, con huella del documento, versión y procedencia de la plantilla y evento de creación con usuario autenticado.
5. Completar únicamente con datos corroborados. Las identidades se toman de fichas cotejadas y las propuestas se aceptan, rechazan o deshacen con fundamento. La herramienta de corrección desde ficha permite sustituir una mención pendiente con el valor cotejado del campo elegido.
6. Revisar todos los antecedentes, certificados y requisitos aplicables; ejecutar análisis y registrar fuentes, decisiones y evidencia. Mientras existan campos entre corchetes o falte revisión/plantilla normativa, la aprobación queda bloqueada.

También se puede descargar la plantilla DOCX desde el catálogo para completarla en Word y volver a importarla. Una descarga no equivale a aprobación. La plantilla no genera una certificación notarial válida ni firma por la escribana o por los comparecientes.

El manifiesto registra huellas y adaptaciones como documentación de procedencia; no es prueba independiente de autoría o fecha ni sustituye la auditoría del expediente.
