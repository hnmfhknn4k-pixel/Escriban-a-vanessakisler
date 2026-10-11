# Acceso con Supabase

La app permite crear una cuenta habilitada, confirmar el correo, iniciar con contraseña y completar TOTP antes de abrir expedientes. Supabase gestiona la autenticación; los expedientes y el registro cifrados permanecen en el servidor de EscribanIA. No se migró la base a Supabase ni se configuraron tablas, Storage o RLS allí.

En el inicio, **Entrar a prueba sin autenticador** abre una demostración pública con datos ficticios y sin acceso a expedientes, documentos del usuario ni IA externa. **Crear usuario con Supabase** lleva al formulario de cuenta; si no está configurado, el formulario permanece visible con aviso y controles deshabilitados. La demostración no crea una sesión ni una cuenta y no sustituye la autenticación del entorno de trabajo.

## Configuración del servidor

En Render → servicio → Environment, agregar `SUPABASE_URL` (HTTPS del proyecto), `SUPABASE_PUBLISHABLE_KEY` (clave pública que comienza con sb_publishable_) y `ESCRIBANIA_ALLOWED_EMAILS` (correos habilitados separados por comas). Guardar y redesplegar la rama `codex/escribania-v04`. Ninguno de estos valores se incorpora al repositorio ni se entrega al navegador. No se requiere service_role ni clave secreta de Supabase para el flujo implementado.

En Supabase → Authentication: habilitar proveedor Email, confirmación de correo y factor TOTP. En URL Configuration, configurar Site URL y redirección permitida con la URL HTTPS real de EscribanIA. Verificar el servicio de correo y sus límites; si no llega la confirmación revisar entregas y configuración SMTP. No se afirma haber modificado estas opciones del proyecto.

Los registros desde la app están restringidos por la lista del servidor. Revisar también la política de altas del proyecto Supabase: una lista en EscribanIA no impide por sí sola crear cuentas directamente por la API del proveedor, aunque esas cuentas no pueden entrar a EscribanIA si no están habilitadas.

## Ingreso

Crear mi cuenta → confirmar el correo → ingresar con correo y contraseña → añadir en una app de autenticación la clave TOTP privada presentada → introducir el código de seis dígitos → abrir la mesa de trabajo. No compartir contraseña, clave TOTP ni códigos por chat. La clave pública del proyecto no es la clave TOTP personal.

La preautenticación dura diez minutos, no permite acceder a expedientes y requiere cookie HttpOnly y CSRF para completar el factor. El servidor corrobora con Supabase la identidad y nivel aal2 antes de crear una sesión de treinta minutos. Los tokens del proveedor no se exponen al navegador ni se almacenan como claves del expediente. La sesión existente vence a los treinta minutos; revocación instantánea y administración de recuperación de MFA requieren operación adicional. No hay recuperación automática ni cambio de factores por la app.

La identidad de revisión se registra como `supabase:<UUID>`; no acredita habilitación profesional ni la identidad de un compareciente. Las cuentas locales preexistentes no se fusionan automáticamente y el alta de permisos para cuentas externas requiere revisión administrativa: no se migraron propietarios o ACL.

Antes de documentos reales: revisar contrato, región, transferencias, conservación y seguridad de Supabase y Render. Configurar almacenamiento persistente de base y claves de EscribanIA; autenticar con Supabase no hace persistentes los expedientes de un contenedor efímero. El flujo está probado con transporte simulado; la configuración real y un ingreso exitoso aún deben comprobarse.
