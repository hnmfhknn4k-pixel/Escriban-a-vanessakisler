# Avances reales — EscribanIA 0.4

11 de octubre de 2026. Implementación sobre el repositorio existente `hnmfhknn4k-pixel/Escriban-a-vanessakisler`; no se creó un repositorio nuevo. Base recibida: ZIP corregido v0.3, código adicional y dos copias iguales del manual v0.3. Procedencia y huellas en `reference-v03/attachments-manifest.json`.

## Completado y comprobado

- Servidor web y UI adaptable; cuentas con contraseña y TOTP, sesiones, CSRF y permisos por expediente.
- Fichas cotejadas, nombres completos en mayúsculas con tildes/Ñ, formato y dígito verificador de cédulas, cotejo determinista y bloqueo por discrepancias. Correcciones de datos desde la ficha se proponen y requieren aceptación; nunca se alteran las fichas por el modelo.
- Original cifrado y conservado; importación DOCX, análisis de texto/tablas/encabezados/pies y advertencias de elementos no procesados; exportación de cambios aceptados como revisiones Word. Aprobación sobre el mismo archivo y huella corroborados, no una regeneración posterior.
- Seudonimización local y reinserción determinista; adaptador Anthropic basado en v0.3, revisión de proveedor y envío explícito requerido; respuestas estructuradas y fragmentos literales validados, sin hechos generados ni citas inventadas aceptadas.
- Registro cifrado con cadena HMAC, identidad de cuenta autenticada, eventos de cambios y decisiones, huellas de original/texto/final, reglas y prompt, reapertura e impugnación interna. Sin prueba de fecha, firma personal ni protección independiente contra administrador.
- Perfil notarial único para todos los expedientes; sin medidas normativas supuestas ni edición de márgenes por usuario. Validación de impresión exigida. Consulta oficial y alcance en `fuentes.md`.
- Manual PDF actualizado de siete páginas, reproducible desde documentación versionada.

## Validación ejecutada

47 pruebas `unittest` completadas y aprobadas en un venv limpio con dependencias fijadas. Incluyen mayúsculas Unicode, CI válida/inválida, seudonimización y reinserción, referencias desconocidas, citas falsas, respuesta que se atribuye hechos, fragmentos inventados, discrepancias, nombre separado en runs, corrección desde ficha, cambios aceptados/rechazados/deshechos, campos pendientes, bloqueo sin perfil, cierre y reapertura con perfil de laboratorio, impresión declarada y huella, conservación Word, cifrado, permisos, alteraciones y rollback del estado, MFA y CSRF. Los valores de dimensiones del test son ficticios: nunca se instalaron como perfil legal.

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
