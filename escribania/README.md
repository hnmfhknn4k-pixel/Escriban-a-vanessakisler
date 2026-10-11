# EscribanIA 0.4

Implementación web de asistencia notarial para Uruguay, basada en los flujos, controles de texto y contrato de observaciones del ZIP `EscribanIA_corregida_v03.zip`. Los componentes de referencia y su procedencia están en `reference-v03`. El servidor Python sustituye el registro efímero del navegador y la ruta IA que enviaba texto sin seudonimizar. El sitio original de Vanessa Kisler se conserva en la raíz del repositorio.

## Ejecutar

Requiere Python 3.12 y Node 24 solo para comprobar JavaScript y los controles históricos.

```bash
cd /workspace/Escriban-a-vanessakisler/escribania
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.lock
.venv/bin/python manage.py create-user --user escribana
.venv/bin/python -m uvicorn app:app --host 127.0.0.1 --port 8001 --no-access-log
```

El alta pide contraseña en terminal y entrega el secreto para un autenticador TOTP (30 segundos, seis dígitos). Ese secreto es privado: no subirlo a Git ni compartirlo por chat. La clave de cifrado y la base se generan en `runtime/`, ignorado por Git; `ESCRIBANIA_DATA` permite otra ruta. Si se usan rutas distintas, configurarlas tanto en `manage.py` como en el servidor. Cada tarea cloud ya está aislada: usar el checkout existente, sin crear worktrees salvo petición expresa.

## Flujo

Importar DOCX → cotejar fichas → ver propuestas → aceptar/rechazar/deshacer con evidencia → analizar → registrar consulta oficial y decisiones → corroborar integralmente → revisar impresión → aprobar con fundamento. Cambiar texto, ficha o fuente invalida la corroboración anterior. Reabrir y cuestionar el sistema vuelve a bloquear el cierre.

Los borradores base son plantillas deterministas con campos pendientes, sin cláusulas jurídicas inventadas. La consulta normativa permite registrar fuentes oficiales efectivamente consultadas por el revisor; no hay buscador jurídico automático. La viabilidad aparece como indeterminada hasta valorar antecedentes, capacidad, legitimación, representación, restricciones y reglas del acto concreto.

En **Plantillas revisables** está **Compraventa de automotor**, derivada del modelo DOC aportado por la usuaria. Se muestran las 14 adaptaciones antes/después y se exige reconocer la revisión pendiente antes de crear un expediente propio. Tiene 49 campos/avisos pendientes distintos y no presume identidad, pago total, cargas, tradición ni situación tributaria. El documento original convertido se entrega por separado, sin alterarlo. Ver `docs/plantillas.md` para el alcance y las comprobaciones realizadas.

Word: máximo 10 MB y 40 MB descomprimidos; original cifrado y conservado; cambios aceptados exportados como `w:del`/`w:ins`; estilos y partes no modificadas conservados. La versión aprobada conserva la evidencia de cambios y debe revisarse en Word antes de imprimir, teniendo en cuenta la vista de marcas. No todas las variantes de OOXML se editan: revisar advertencias. No se promete fidelidad visual perfecta.

## Perfil único de papel notarial

No hay márgenes editables por expediente. El art. 39 publicado por IMPO fija los límites citados en `docs/fuentes.md`, pero no las cuatro medidas en cm. No se instala un perfil supuesto. El administrador puede instalar una plantilla técnica respaldada y probada para anverso/reverso:

```bash
.venv/bin/python manage.py install-profile --file /ruta/controlada/perfil-validado.json
```

Debe contener medidas en milímetros `w,h,top,bottom,left,right,header,footer,gutter`, `source` oficial, `authority`, `normative_version`, `evidence`, `reviewer`, `validated_at`, `print_test` y `duplex_validated: true`. No se entrega un ejemplo con números que puedan confundirse con normativa. Reiniciar el servidor y repetir el análisis de expedientes abiertos. Mientras falta la plantilla se permite descargar borradores con el formato original y se bloquea la aprobación final.

## IA

Adaptador Anthropic preparado; conexión real no validada. API key únicamente en variable del servidor `ANTHROPIC_API_KEY`; modelo en `ANTHROPIC_MODEL`. Además requiere `runtime/provider-review.json` con `approved:true`, `contract`, `training`, `retention`, `subprocessors`, `international_transfers`, `legal_basis`, `reviewer`, `reviewed_at` y `expires_at` ISO con zona horaria. Son referencias de evaluación documentada, no afirmaciones automáticas de cumplimiento. Las cadenas deben describir evidencia real; no usar valores de prueba en producción.

La pestaña Protección genera una previsualización local con referencias reversibles. Se exige revisión de identificadores indirectos, ausencia de coincidencias residuales, huella de esa versión y autorización de envío. El servidor sustituye antes de enviar y reinserta después de validar; no envía original, fichas ni tabla de correspondencia. Las respuestas se clasifican como inferencias o indeterminables, sin aprobación ni cambio de Word automáticos. Las pruebas usan transporte simulado y no acreditan una conexión o las condiciones del proveedor.

## iPhone y despliegue

La interfaz es adaptable y se probó en Chromium con viewport móvil 390×844, no en Safari de un iPhone físico. Para abrirla desde iPhone hace falta una dirección HTTPS de un servidor publicado; no basta un HTML en Archivos ni un enlace localhost de este entorno. La app no se publicó y no se creó un nuevo repositorio.

En alojamiento elegido por el responsable: montar almacenamiento privado persistente, mantener un solo worker, desplegar el servicio detrás de un proxy HTTPS, configurar `ESCRIBANIA_MODE=production` y `ESCRIBANIA_ORIGIN=https://dominio-real`, y no exponer el puerto interno. Configurar backups, claves separadas, controles del administrador, retención, logs mínimos y evaluar firma/fechado/anclaje externo del registro según `docs/seguridad.md`. La aplicación rechaza modo producción sin origen HTTPS, pero configurar la variable no aporta un certificado TLS por sí mismo. Un reinicio cierra sesiones. No hay cuentas ni claves de producción en el código.

## Validar

```bash
.venv/bin/python -m unittest discover -s tests -v
node --check web/app.js
node reference-v03/checks/core.mjs
.venv/bin/python scripts/manual.py
.venv/bin/python manage.py verify-audit
```

Prueba de navegador opcional: `PYTHONPATH=. python3 tests/browser_smoke.py`, con Playwright, Chromium y servidor de desarrollo activo; usar solo datos ficticios y almacenamiento de pruebas en `/tmp/escribania-dev`.

Ver manual PDF en `docs/manual.pdf`, fuentes en `docs/fuentes.md`, seguridad y responsabilidades en `docs/seguridad.md` y resultados reales en `docs/avances.md`. No garantiza ausencia de errores ni cumplimiento jurídico integral.
