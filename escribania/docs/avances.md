# Avances reales — EscribanIA 0.4

11 de octubre de 2026. Implementación sobre el repositorio existente `hnmfhknn4k-pixel/Escriban-a-vanessakisler`; no se creó un repositorio nuevo. Base recibida: ZIP corregido v0.3, código adicional y dos copias iguales del manual v0.3. Procedencia y huellas en `reference-v03/attachments-manifest.json`.

## Completado y comprobado

- Servidor web y UI adaptable; cuentas con contraseña y TOTP, sesiones, CSRF y permisos por expediente.
- Fichas cotejadas, nombres completos en mayúsculas con tildes/Ñ, formato y dígito verificador de cédulas, cotejo determinista y bloqueo por discrepancias. Correcciones de datos desde la ficha se proponen y requieren aceptación; nunca se alteran las fichas por el modelo.
- Original cifrado y conservado; importación DOCX, análisis de texto/tablas/encabezados/pies y advertencias de elementos no procesados; exportación de cambios aceptados como revisiones Word. Aprobación sobre el mismo archivo y huella corroborados, no una regeneración posterior.
- Seudonimización local y reinserción determinista; adaptador Anthropic basado en v0.3, revisión de proveedor y envío explícito requerido; respuestas estructuradas y fragmentos literales validados, sin hechos generados ni citas inventadas aceptadas.
- Registro cifrado con cadena HMAC, identidad de cuenta autenticada, eventos de cambios y decisiones, huellas de original/texto/final, reglas y prompt, reapertura e impugnación interna. Sin prueba de fecha, firma personal ni protección independiente contra administrador.
- Perfil notarial único para todos los expedientes; sin medidas normativas supuestas ni edición de márgenes por usuario. Validación de impresión exigida. Consulta oficial y alcance en `fuentes.md`.
- Manual PDF actualizado de doce páginas, reproducible desde documentación versionada.

## Validación ejecutada

60 pruebas `unittest` completadas y aprobadas con dependencias fijadas. Incluyen mayúsculas Unicode, CI válida/inválida, seudonimización y reinserción, referencias desconocidas, citas falsas, respuesta que se atribuye hechos, fragmentos inventados, discrepancias, nombre separado en runs, corrección desde ficha, cambios aceptados/rechazados/deshechos, campos pendientes, bloqueo sin perfil, cierre y reapertura con perfil de laboratorio, impresión declarada y huella, conservación Word, cifrado, permisos, alteraciones y rollback del estado, MFA y CSRF. Los valores de dimensiones del test son ficticios: nunca se instalaron como perfil legal.

## Conjunto privado de compraventa, certificación y protocolización

Integrado por solicitud expresa un borrador conjunto basado en los tres modelos, con 77 campos/avisos distintos, referencias comunes y huellas individuales de las fuentes. La certificación no presupone firmas en presencia, conocimiento personal, capacidad ni SOA; el acta no presupone poder ni primera protocolización. Los originales permanecen fuera del repositorio. La cita general al art. 291 de la Ley 18.362 se sustituyó por el art. 89 vigente de la Ley 16.871 para la protocolización de la compraventa; la representación queda condicionada a evidencia real.

Consulta efectiva de nueve fuentes oficiales: IMPO y ficha del trámite DGR en gub.uy. Se identificó el Manual de Automotores 2025 mediante el buscador oficial, pero su descarga y el portal DGR devolvieron bloqueo 403 del proxy. No se afirman lectura del manual, examen de resoluciones ni aprobación DGR del modelo. Informe en `compraventa-automotor.md` y evidencia de consulta con URL/huellas; sin firma ni sellado de tiempo.

Tres pruebas adicionales aprobadas de conjunto documental, adaptaciones, procedencia, descarga y bloqueo; 60 en total. Chromium móvil/escritorio también verificó apertura del conjunto tras reconocimiento y texto de protocolización. Manual actualizado: doce páginas. No se publicó una URL web, habilitó IA ni creó un issue en Linear.

Pasaron los controles históricos v0.3 de texto y extracción ZIP y `node --check web/app.js`. Instalación repetible validada; versiones directas y transitivas fijadas en `requirements.lock`.

Prueba funcional con Chromium y viewport móvil 390×844 y escritorio: login con TOTP, importación de DOCX ficticio, alta de ficha, análisis, previsualización seudonimizada, auditoría, bloqueo de cierre, descarga Word y logout. No hubo errores de JavaScript ni desbordamiento horizontal. No se probó Safari en un iPhone físico. El PDF se generó y se comprobó extracción de contenido.

## Pendiente, sin resultados simulados

- IA real: no hay clave/modelo configurados ni evaluación contractual aprobada. Transporte simulado en pruebas; no se enviaron documentos al proveedor real.
- Márgenes y dimensiones exactas: falta especificación técnica oficial del papel notarial, corroboración de modificaciones aplicables y prueba física de anverso/reverso. Se consultó texto original publicado del art. 39; la ruta consolidada de acceso restringido no se trató como norma verificada.
- Publicación web HTTPS: no realizada. Se requiere dominio/alojamiento y controles operativos. La publicación del entorno cloud es una operación distinta de publicar la app en Internet.
- Firma, fechado y anclaje externo/WORM: evaluados en documentación; no implementados ni certificados. El registro local no se llama inalterable.
- Conservación legal y borrado integral de auditoría/backups: requieren política y operación externas; el botón de eliminación realiza borrado lógico del expediente.
- Linear: sin herramientas/conector disponibles en esta sesión; no se creó ningún issue. Este documento conserva el avance local para registrar resultados efectivos cuando exista acceso.
- GitHub: lectura y simulación de escritura aceptadas. GitHub API/GraphQL respondió Forbidden, por lo que no se pudo abrir un PR con `gh`; la rama `codex/escribania-v04` se envió efectivamente mediante Git y se comprobó el seguimiento remoto. No se afirma creación ni publicación web a partir de acceso de lectura.

Configuración cloud guardada: instalación con lock, pruebas e instrucciones de arranque; requerimientos de secreto `ANTHROPIC_API_KEY` y variable `ANTHROPIC_MODEL`; destinos oficiales IMPO/URCDP y `api.anthropic.com`. Guardar el borrador no configura los valores, no habilita la IA y no publica la app.


## Integración del modelo de automotor

El archivo `MODELO CV AUTOMOTOR.doc` se convirtió localmente a DOCX sin modificar el original. Coincidencia textual comprobada contra exportación directa del DOC a TXT, normalizando espacios y saltos. Se conserva la copia convertida por separado de la plantilla preparada; ninguna de esas comprobaciones certifica maquetación idéntica o validez jurídica.

La plantilla del catálogo incluye 14 adaptaciones visibles y 49 campos/avisos pendientes distintos; reemplaza fechas, precio, circunstancias de entrega, identidades y declaraciones que no deben presumirse en otro acto. Un reconocimiento explícito precede la creación de un expediente propio y registra versión y procedencia. Se mantiene el bloqueo de aprobación por campos pendientes y por perfil normativo no validado. Los márgenes heredados 4/1/4/2 cm no se presentan como exigencia normativa.

Se añadieron y aprobaron 10 pruebas de plantilla, rutas autenticadas, reconocimiento previo, descarga exacta y creación bloqueada por pendientes (57 en total). La prueba móvil/escritorio también comprobó adaptaciones visibles, habilitación tras reconocimiento, apertura del expediente y descarga DOCX. Se corrigió una advertencia de tabulación que confundía configuración de tabuladores con caracteres de tabulación; los caracteres de tabulación reales siguen generando advertencia. El manual actualizado tiene diez páginas. No se habilitó IA, no se publicó una nueva URL web ni se creó un issue de Linear.
