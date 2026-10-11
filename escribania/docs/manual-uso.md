# EscribanIA
Tu criterio. Una asistencia que se puede revisar.

Manual de uso adaptado del manual v0.3 aportado por la usuaria. Edición: 11 de octubre de 2026. Colores y estilo de la web. El original se conserva como referencia histórica; este manual describe las funciones actuales.

## Disponible ahora
Prueba sin autenticador, carga local de DOCX y TXT, controles de texto y dígito verificador, lectura de márgenes por sección, huellas SHA-256 y descarga de revisión TXT. En el espacio con cuenta: fichas, propuestas revisables, Word con cambios y registro cifrado del servidor.

## Pendiente de configurar o validar
IA real, perfil técnico oficial de papel notarial y operación segura con documentos reales. El acceso con Supabase requiere variables del servidor, correo confirmado y autenticador. La revisión humana no garantiza ausencia de errores.

## Antes de empezar
Usá documentos ficticios para las pruebas. Los controles no certifican validez jurídica, identidad ni normativa vigente. Una sustitución reversible de nombres y cédulas es seudonimización; no convierte automáticamente el documento en anónimo.

## Abrir y entrar
Abrí https://escriban-a-vanessakisler.onrender.com/demo y elegí «Entrar a prueba sin autenticador» desde el inicio. Funciona en un navegador moderno de PC o iPhone; no necesita instalación. La actualización debe estar desplegada en Render. En «Crear usuario con Supabase», el formulario se habilita cuando la conexión está configurada. Creá tu contraseña, confirmá el correo y vinculá el autenticador siguiendo la clave privada de la app; no uses ni compartas la contraseña de iCloud.

## Qué recibís
La web para revisar, el código fuente, plantillas de compraventa privada con certificación y protocolización, y este manual. Los ejemplos no constituyen instrumentos autorizados. El registro de la prueba y el registro del servidor tienen alcances distintos.
---PAGE---
# 01 / REVISIÓN DOCUMENTAL
Tu primera revisión

## 1. Cargar el documento
En la prueba, elegí DOCX o TXT UTF-8 de hasta 8 MB. El archivo se lee en tu navegador y no se sube al servidor ni a una IA. DOC requiere guardar una copia DOCX en Word. PDF e imágenes requieren conversión u OCR fuera de esta prueba. El archivo original permanece intacto.

## 2. Revisar el texto extraído
Cotejá el texto de trabajo con el original. DOCX: se extrae texto principal, tablas, encabezados y pies, sin reconstruir páginas. Cambios controlados, campos, imágenes, notas, comentarios y elementos complejos pueden quedar parcial o totalmente fuera; las advertencias deben revisarse en Word. No hay OCR. TXT no permite verificar márgenes o secciones.

## 3. Revisar el formato notarial
Se muestran los márgenes encontrados por sección como datos del archivo; no se declaran correctos según la ley. El texto original publicado del art. 39 de la Acordada 7.533 establece para papel liso respetar los márgenes del rayado y los límites citados de 25 líneas por carilla, 55 caracteres por línea y 8 mm mínimos entre líneas. No ofrece cuatro medidas en cm: no se presume 4/1/4/2. Se requiere perfil técnico único validado, anverso/reverso y prueba física; la extracción no verifica renglones impresos. Falta completar el cotejo de modificaciones vigentes.

## 4. Validar el archivo cargado
Pulsá «Validar archivo cargado». Se señalan campos entre corchetes, posibles palabras repetidas y números con formato posible de cédula. Se verifica su dígito cuando corresponde, sin acreditar identidad ni corregirlo automáticamente. Cada señal muestra el fragmento y su alcance; revisar contexto, alternativas y evidencia. Máximo 200 señales visibles; puede haber otras sin mostrar.

## 5. Revisar y descargar
Podés descargar la revisión TXT con huellas de archivo y texto, advertencias, señales y texto extraído. Es editable y puede contener datos personales: protegela. Al quitar el archivo, cargar otro o cerrar la página, se pierde esta revisión local. No exporta Word corregido desde la prueba. La aplicación con cuenta admite DOCX hasta 10 MB y exporta cambios aceptados como revisiones Word; revisar fidelidad y marcas antes de imprimir.

## Nombres: cambios propuestos, no adivinados
El ejemplo fijo permite previsualizar, aceptar, rechazar y deshacer MAYÚSCULAS de nombres completos conservando tildes y Ñ. No aplica esas fichas ficticias al archivo que cargues. En el espacio con cuenta, usar fichas cotejadas por la escribana; la IA no puede modificar sus nombres o cédulas verificados. Comparar menciones y resolver discrepancias antes del cierre.
---PAGE---
# 02 / HUMILDAD ALGORÍTMICA
De una señal a una decisión

## Comprobado en el texto
Hecho mecánico con alcance limitado, como un campo entre corchetes o un dígito incompatible si el número es una cédula. No equivale a identidad, intención, viabilidad ni validez jurídica. La prueba no inventa resultados de IA.

## Inferencia
Interpretación que necesita corroboración y criterio profesional. No afirmar datos de partes, pago, tradición, cargas o antecedentes sin evidencia. Las observaciones de IA, cuando se habilite el proveedor, requieren fragmento literal verificable, fundamento, alternativas, incertidumbre y evidencia que cambiaría el criterio.

## No se puede determinar
Falta información, fuente o capacidad de verificación. Identificar qué hace falta y conservar el estado pendiente. La ausencia de señales en controles limitados no demuestra ausencia de errores.

## Flujo de revisión humana
Detección → fundamento → revisión humana → corroboración → decisión fundada → posibilidad de revisión. En el espacio con cuenta, aceptar o rechazar requiere evidencia y motivo; se puede cuestionar, reabrir y corregir. Un nombre declarado no prueba identidad ni habilitación profesional. El acceso autenticado con Supabase registra el UUID de la cuenta y exige segundo factor; la prueba pública no identifica revisor.

## Tres conceptos diferentes
Trazabilidad permite reconstruir eventos y versiones. Explicabilidad permite comprender fundamento y límites; una cita no revela por sí sola las causas internas del modelo. Auditabilidad permite que un tercero competente examine funcionamiento y controles; falta auditoría independiente y anclaje externo del registro.

## Responsabilidad e impugnación
Cuestionar una observación o un defecto del sistema dentro de la app no equivale a un recurso institucional o judicial. La asignación de responsabilidades y el valor probatorio requieren análisis del marco y el caso. La revisión humana no elimina automáticamente la responsabilidad del proveedor. No presentar propuestas de investigación como recursos jurídicos vigentes.
---PAGE---
# 03 / PRIVACIDAD Y REGISTROS
Qué conservar y qué proteger

## Qué identifica la revisión
La prueba calcula SHA-256 del archivo original y del texto extraído: representan contenidos diferentes. La descarga TXT registra señales, advertencias, texto y fecha del dispositivo. El historial del ejemplo fijo es ilustrativo. No hay cuenta, firma ni registro protegido en ese modo.

## Qué no acredita
Una huella aislada o un informe editable no prueban autoría ni fecha. En el servidor, el original y eventos se cifran y se protege una cadena HMAC; un administrador con claves puede reconstruirla y el truncado requiere anclaje independiente para detectarse. No se la llama inalterable ni firma personal. Firma avanzada, sellado de tiempo y conservación independiente deben evaluarse según el uso.

## Datos y secreto profesional
La carga y validación de la prueba son locales, sin llamadas a API para el contenido. No se siguen relaciones externas del Word. Quitá el archivo o cerrá la página para retirar la vista. Un informe descargado puede ser sensible. En el espacio autenticado los expedientes se guardan en el servidor: requiere almacenamiento persistente, permisos, claves protegidas, backups y políticas justificadas de conservación y eliminación. Supabase gestiona acceso; no se migraron expedientes allí. Antes de datos reales revisar también Render, Supabase, contratos, región y transferencias.

## Conexión a IA
El adaptador existe; no hay conexión real aprobada ni buscador normativo automático. Se requieren ANTHROPIC_API_KEY y ANTHROPIC_MODEL solo en el servidor y evaluación documentada del proveedor: entrenamiento, retención, subencargados, ubicación, transferencias y roles. Revisar sustitución reversible e identificadores indirectos antes de cualquier envío; reinsertar por programación. No enviar documentos completos por defecto ni llamar anonimización a referencias reversibles.

## Si algo falla
No abre Word: verificar DOCX válido, límite de 8 MB y navegador; conservar el original. DOC, PDF e imágenes requieren conversión. Si se alcanzan límites de descompresión o tiempo, dividir o revisar fuera de la prueba. Registro Supabase deshabilitado: completar configuración en Render y opciones de Authentication del proyecto. No llega el correo: revisar correo, entregas y configuración del proveedor. IA pendiente: es el estado real; los controles locales siguen disponibles. Cerrar o recargar: se pierde la prueba local; descargar antes si corresponde.

## Validación y límites de esta entrega
Pruebas relevantes usan documentos ficticios; se comprueban extracción, límites, controles de identidad, mayúsculas, cambios, reinserción y trazabilidad según el modo. La interfaz se prueba en Chromium móvil y escritorio; no acredita prueba en Safari físico, aceptación DGR o cumplimiento integral. Las actualizaciones deben desplegarse en Render para aparecer en la web. Fuentes y detalles operativos en la documentación del proyecto.
