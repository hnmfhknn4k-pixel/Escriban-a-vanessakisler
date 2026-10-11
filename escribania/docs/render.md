# Despliegue Docker en Render

El error `failed to read dockerfile: open Dockerfile: no such file or directory` indica que Render seleccionó Docker sin encontrar el archivo en la ruta configurada. El repositorio ahora incluye `Dockerfile` en la raíz, en la rama `codex/escribania-v04`.

En Settings del servicio, usar rama `codex/escribania-v04`, Root Directory vacío, Dockerfile Path `./Dockerfile` y Docker Command vacío para respetar el comando de la imagen. Ejecutar Manual Deploy → Deploy latest commit. No cambiar el sitio original de la rama main.

El contenedor usa Python 3.12, dependencias fijadas, usuario sin privilegios y un worker. Escucha en `0.0.0.0` y el `PORT` asignado por Render; usa `RENDER_EXTERNAL_URL` como origen HTTPS de producción, salvo un origen configurado expresamente. Un dominio personalizado requiere ajustar `ESCRIBANIA_ORIGIN` al dominio efectivamente usado. Health Check Path: `/api/status`.

Un despliegue exitoso permite cargar la pantalla de acceso; no crea cuentas, activa IA ni valida controles del alojamiento. La cuenta requiere alta privada con `manage.py create-user` y TOTP. No publicar credenciales ni incorporar una cuenta de prueba fija en el código.

El almacenamiento `/app/runtime` debe conservar base y claves juntas. Sin disco persistente, un redespliegue puede perder cuentas y expedientes; usar únicamente datos ficticios mientras se define almacenamiento y operación. No contratar un plan pago automáticamente. Antes de documentos reales se requiere verificar seguridad, condiciones del proveedor, backups, conservación y demás controles descritos en el manual.
