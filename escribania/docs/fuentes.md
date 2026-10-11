# Fuentes oficiales y alcance de la verificación

Consulta realizada el 11 de octubre de 2026. Los textos públicos de IMPO se descargaron por HTTPS con verificación TLS. La página de una norma no acredita por sí sola que se hayan revisado todas las resoluciones, modificaciones o exigencias técnicas aplicables al acto concreto.

## Papel notarial: un perfil para todos

Fuente consultada: [texto original publicado de la Acordada 7.533](https://www.impo.com.uy/bases/acordadas-scj-originales/7533-2004), artículos 37 a 43.

El artículo 37 remite las características del papel a la Suprema Corte de Justicia. El artículo 39 dice: «En el liso, deberán respetarse los márgenes establecidos para el rayado». También establece un máximo de 25 líneas por carilla, 55 letras o caracteres por línea y un espacio entre líneas no menor a 8 milímetros. El artículo 41 atribuye la administración, impresión y distribución del papel a la Caja Notarial.

Estos artículos no ofrecen cuatro valores en centímetros ni dimensiones completas de una plantilla. No se deducen ni se configuran los anteriores 4/1/4/2 cm. Se requiere especificación técnica oficial del papel y verificar modificaciones del reglamento, anverso y reverso y una impresión real. El acceso público intentado a la ruta de artículo consolidado devolvió «Acceso no válido»; no se interpreta HTTP 200 como acceso a la norma consolidada.

La aplicación no deja escoger márgenes por expediente. Un responsable instala una única plantilla validada mediante `manage.py install-profile`. Sin ella se puede trabajar y descargar borradores con el formato original, pero no aprobar la versión notarial final. La extracción de texto no prueba número de renglones impresos, caracteres por renglón ni distancia física; tampoco reemplaza la revisión de la salida de Word.

## Datos personales y secreto

Fuente consultada: [Ley 18.331, documento actualizado en IMPO](https://www.impo.com.uy/bases/leyes/18331-2008).

| Artículos | Obligación y consecuencia para el diseño |
|---|---|
| 7 y 8 | Exactitud, adecuación, minimización, finalidad y eliminación cuando los datos dejen de ser necesarios. La conservación requiere justificar finalidad y excepciones aplicables; 30 días es una fecha operativa de revisión, no un plazo legal notarial. |
| 9 y 13 | Determinar y documentar el fundamento lícito del tratamiento y brindar información a titulares. No se presume que un consentimiento genérico habilite todos los usos o transferencias. El texto actualizado del art. 13 incluye información sobre transferencias y valoraciones automatizadas. |
| 10 y 11 | Seguridad, confidencialidad, integridad, reserva y secreto profesional. El secreto continúa luego de finalizar la relación. Cifrado, permisos y MFA son controles técnicos, no una declaración de cumplimiento integral. |
| 12 | Responsabilidad del responsable y, en su caso, del encargado; medidas técnicas y organizativas apropiadas y evidencia de implementación. La revisión humana no exime automáticamente al proveedor. |
| 14 y 15 | Acceso, rectificación, actualización, inclusión y supresión, con procedimientos y plazos aplicables. El prototipo requiere canal organizativo y operación externa para atender solicitudes y copias de respaldo. |
| 16 | Impugnación de valoraciones personales en el ámbito y supuestos definidos por la norma. Cuestionar una observación en la app es un mecanismo interno; no se presenta como recurso judicial ni como extensión automática de esos supuestos. |
| 17 y 23 | Evaluar comunicación a terceros y transferencias internacionales, destinos, nivel de protección y fundamento o excepción aplicable. Seudonimizar de forma reversible no convierte automáticamente los datos en no personales. |
| 28 y 29 | Evaluar y gestionar inscripción registral de bases, condiciones de seguridad, responsables, destinatarios y conservación conforme al régimen aplicable. |

Reglamentación consultada: [Decreto 414/009](https://www.impo.com.uy/bases/decretos/414-2009) y [Decreto 64/020](https://www.impo.com.uy/bases/decretos/64-2020).

En el Decreto 64/020: art. 3, medidas de seguridad e inicio de mitigación dentro de las primeras 24 horas de constatado el incidente; art. 4, comunicación del responsable a URCDP en un máximo de 72 horas de conocida la vulneración y comunicación inmediata del encargado al responsable; arts. 5–9, responsabilidad proactiva, documentación, evaluación de impacto cuando corresponda y privacidad por diseño y por defecto; arts. 10–12, evaluar designación y funciones del delegado cuando se cumplan los supuestos. Hay que revisar las condiciones del caso y las instrucciones vigentes de [URCDP](https://www.gub.uy/unidad-reguladora-control-datos-personales/).

## Firma, fecha y valor del registro

Fuente consultada: [Ley 18.600, texto actualizado en IMPO](https://www.impo.com.uy/bases/leyes/18600-2009), artículos 4, 5 y 6.

Una huella SHA-256 detecta diferencias con un valor de referencia confiable; no identifica al autor ni acredita fecha. HMAC ofrece autenticación de integridad para quien protege la clave compartida; no es una firma electrónica avanzada del revisor. El art. 6 regula las condiciones de firma avanzada y dice que el documento no hará fe respecto de su fecha salvo fechado electrónico de un prestador acreditado. Evaluar firma y fechado con prestador acreditado, certificados, validación y conservación según el uso y las excepciones del régimen documental.

## Proveedor de IA: verificación pendiente

El adaptador Anthropic existe, pero no se efectuó una consulta real ni se verificaron condiciones contractuales del proveedor. Antes de habilitarlo, el responsable debe documentar contrato y roles, uso para entrenamiento, retención, eliminación, subencargados, destinos, transferencias, fundamento lícito, evaluación de impacto cuando corresponda, revisión y vencimiento. El archivo privado `provider-review.json` registra esa evaluación; no contiene claves. Las claves se inyectan exclusivamente en el proceso del servidor. Confirmar también las condiciones del alojamiento y de sus operadores.

Esta documentación distingue textos efectivamente consultados, inferencias de diseño y verificaciones pendientes. No es un dictamen de cumplimiento ni una garantía de ausencia de errores.
