# EscribanIA v0.3

Prototipo privado de asistencia notarial. Lectura local de .docx/.txt, controles de texto, márgenes por sección, propuesta explícita de mayúsculas y registro descargable de revisión.

## Alcance

Los controles locales no acreditan validez jurídica. La extracción Word procesa texto principal y tablas; no reconstruye la maquetación ni revisa íntegramente cuadros, notas, encabezados, pies, comentarios o cambios controlados. Se aplica un perfil normativo fijo del artículo 39 de la Acordada 7533. Las medidas de los márgenes en cm requieren especificación técnica validada del papel rayado: no se inventan ni se dejan como preferencias. Las reglas de 25 líneas, 55 caracteres y 8 mm se muestran automáticamente, pero el texto extraído no permite verificar su cumplimiento en la impresión.

El registro incluye SHA-256 del archivo, SHA-256 del texto, fecha declarada por el navegador, perfil usado, resultados y acciones de revisión. Vive en memoria, se pierde al recargar y es editable al exportar. No tiene identidad verificada, firma digital ni sello de tiempo confiable.

## IA

Las rutas están preparadas para Anthropic. Configurar ANTHROPIC_API_KEY y ANTHROPIC_MODEL como secretos del servidor. No incluir claves en frontend ni Git. Sin esas variables, el estado y los módulos muestran conexión pendiente. Las solicitudes exigen sesión ChatGPT y consentimiento expreso. El proveedor recibe el texto enviado; consultas incluyen el historial reciente. Revisar condiciones, retención y tratamiento antes del uso profesional. No hay almacenamiento de documentos del lado servidor ni logs de contenido en el código.

La API limita entradas, no trunca silenciosamente, verifica esquemas JSON y rechaza respuestas incompletas. Las observaciones deben citar fragmentos presentes en el texto y declarar inferencia/no_determinable. Esa correspondencia no acredita corrección jurídica. No hay búsqueda normativa ni auditoría independiente.

Aceptar/descartar exige nombre declarado, evidencia adicional, fundamento y contraargumento; las decisiones pueden reabrirse. Para un servicio productivo hacen falta identidad vinculada, persistencia íntegra, controles de acceso por expediente, auditoría independiente, pruebas con corpus, métricas de errores y mecanismos institucionales de revisión.

## Desarrollo

Instalar dependencias con el helper Sites y construir con scripts/build-site.mjs. Verificar TypeScript con `node node_modules/typescript/bin/tsc --noEmit`.
