# Modelo de seguridad y responsabilidades

## Controles implementados

Contraseña con scrypt y sal individual; TOTP de seis dígitos; sesión HttpOnly, SameSite estricto y duración de 30 minutos; control de origen y CSRF; límite de intentos por usuario e IP; permisos por expediente; TLS obligatorio en configuración de producción; CSP sin scripts inline, eval ni recursos externos. La identidad autenticada es una cuenta provisionada por el administrador, no una certificación de habilitación profesional. Vincular la cuenta a una persona y verificar credenciales profesionales es responsabilidad operativa.

Originales, texto, fichas, decisiones y registros sensibles se guardan cifrados con Fernet (cifrado autenticado). Las claves locales están en un archivo con permisos 0600, fuera del código versionado. La seguridad en producción exige separar claves del almacenamiento, KMS/HSM, backups cifrados, gestión de recuperación, revocación, monitoreo y control del administrador. El cifrado local no protege de un proceso o administrador que ya dispone de las claves. Identificadores técnicos de usuario, expediente y ACL no están cifrados; no introducir nombres personales como usuario.

No hay logs de documentos ni del cuerpo de las solicitudes. Iniciar Uvicorn con `--no-access-log`; configurar también proxy y alojamiento para que no registren cuerpos, cookies, cabeceras de autenticación o nombres de archivos. El original puede contener metadatos personales; no se envía al modelo.

## Auditoría

Eventos cifrados y encadenados por HMAC-SHA256; triggers bloquean UPDATE y DELETE normales. Estado del expediente vinculado al último evento mediante hash del contenido, para detectar cambios o restauraciones inconsistentes. La UI presenta un historial; no ofrece un JSON editable como prueba. Las horas son declaradas por el servidor y la cuenta es autenticada, sin firma personal.

Límites: quien controla claves y base puede reconstruir la cadena; eliminar el final o restaurar todo el conjunto junto con sus claves puede pasar la verificación local. Para auditoría resistente al administrador se requieren anclajes periódicos fuera del sistema, almacenamiento WORM con retención apropiada y auditor independiente. Para atribución y fecha, evaluar firma del revisor y fechado electrónico con prestador acreditado. Estas integraciones no se implementaron ni se simulan. Ver `fuentes.md`.

## Conservación y eliminación

El expediente recibe una fecha de revisión a 30 días, sin borrado automático. No es un plazo legal para protocolos u otros instrumentos. El responsable debe adoptar plazos diferenciados por finalidad, tipo documental, obligaciones de conservación y defensa de derechos, con bases y excepciones documentadas. El botón elimina el expediente y ACL de la aplicación; los eventos se conservan cifrados para revisión. No elimina físicamente páginas libres de SQLite, backups ni toda la información histórica. Antes de datos reales hay que definir y operar eliminación segura, retención de auditoría y copias, y ejercer los derechos de titulares mediante un canal identificado. No se declara borrado integral.

## Funciones

- Escribana/revisor: cotejar originales, revisar todas las menciones y asociaciones de identidad, corroborar hallazgos, fuentes y formato impreso y fundamentar decisiones; no delega su juicio al modelo.
- Responsable del tratamiento: legitimación, información, minimización, conservación, derechos, selección de proveedor, contratos, evaluación de impacto e incidentes.
- Administrador: alta y vinculación de cuentas, MFA, permisos, recuperación, claves, perfil normativo único, despliegue y protección de logs.
- Proveedor de software/IA y encargados: obligaciones técnicas, contractuales y legales que correspondan. La revisión humana no elimina toda su responsabilidad.
- Auditor competente: revisar controles, corpus de pruebas, errores, cambios de reglas/modelos y protección independiente del registro.

La aplicación permite cuestionar una observación y un posible defecto del sistema, registrar fundamento y evidencia, reabrir y corregir. No sustituye canales institucionales ni atribuye automáticamente conductas o intenciones a personas. No hay evaluación de crédito, solvencia ni perfilado decisorio automatizado.

## Límites documentales

Se analizan texto principal, tablas, encabezados y pies. Las identidades separadas en runs se comparan sobre texto recompuesto. Se señalan campos Word, notas, comentarios, dibujos, objetos, macros, vínculos externos, cuadros, controles de contenido, saltos y cambios preexistentes; su presencia impide la aprobación final en esta versión. El paquete conserva las partes originales, pero la edición de runs complejos puede rechazarse. La búsqueda automática no identifica todas las variantes de nombres, documentos extranjeros o personas no estructuradas: el cotejo humano integral se exige antes del cierre. No se declara preservación visual perfecta ni validación automática de la impresión.

El adaptador no cambia fichas. Sustituye datos por referencias; reinserta de forma determinista; rechaza referencias desconocidas, respuestas incompletas, citas normativas no verificables y fragmentos ausentes del texto. Las observaciones nunca se aplican automáticamente al Word. Domicilios y otros identificadores indirectos requieren revisión explícita; la detección por patrones no garantiza que no queden datos identificatorios.
