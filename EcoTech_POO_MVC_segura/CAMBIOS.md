# Qué se cambió y por qué

Este archivo resume los cambios hechos al proyecto original, agrupados por tema, para poder explicarlos.

## 1. Contraseñas (seguridad)
- Antes: la contraseña se guardaba y se comparaba en texto plano.
- Ahora: `config/seguridad.py` guarda solo un hash PBKDF2-SHA256 con una sal distinta por usuario y un secreto (pepper) que viene del `.env`. La comparación usa `hmac.compare_digest`.
- `models/usuario.py`: la clase ya no guarda la contraseña; tiene `setContrasena` (valida y calcula el hash), `verificarContrasena` y `iniciarSesion` usa el hash.
- `config/database.py`: las tablas `empleado` y `administrador` tienen `clave_hash` y `sal`. Si la base es antigua, `_migrar_claves` convierte las claves existentes y borra la columna en texto plano.
- Los DAO de empleado y administrador guardan y leen esos dos campos.
- Política: mínimo 8 caracteres, con mayúscula, minúscula y número. Las vistas piden la clave con `getpass` (no se ve al escribir).

## 2. Login y roles
- `controllers/auth_controller.py`: el sistema pide correo y clave antes de mostrar menús. Mensaje igual si falla el correo o la clave, y bloqueo de 60 segundos tras 3 intentos fallidos. Si no hay administradores, se crea el primero.
- `controllers/main_controller.py` + `views/main_view.py`: menú distinto para administrador y empleado. Solo el Superadmin gestiona administradores. El empleado solo ve y registra lo suyo.
- `models/sesion.py`: la sesión se cierra a los 5 minutos de inactividad y limita las consultas a APIs (10 por sesión, 2 segundos entre cada una).

## 3. Servicios externos (APIs)
- `services/cliente_http.py`: todas las solicitudes con `requests`, timeout de 10 s, hasta 3 intentos para errores 429 y 5xx, y revisión del código HTTP.
- `services/clima_service.py` (Open-Meteo): temperatura, estado del tiempo, humedad y viento de una ciudad, con una recomendación para visitas a terreno.
- `services/cambio_service.py` (ExchangeRate-API): convierte el salario de un empleado (se asume en CLP) a otra moneda.
- Los datos se verifican (tipos y rangos) y las entradas del usuario (ciudad, moneda) se validan antes de enviarlas (`services/validaciones.py`).
- `controllers/servicios_controller.py` y `views/servicios_view.py`: integran todo al sistema y guardan cada consulta en la tabla `consulta_externa` (`models/consulta_externa_dao.py`). El administrador puede ver el historial.

## 4. Errores y registro
- `services/excepciones.py`: jerarquía de excepciones propias (`ErrorServicio` y sus hijas) con un mensaje para el usuario y un detalle técnico aparte.
- `config/errores.py`: el detalle técnico va a `errores.log`; el usuario ve un mensaje simple.
- Los DAO ya no atrapan `Exception` ni muestran el error de Python: atrapan `sqlite3.Error`, `ValueError` y `TypeError`.

## 5. Otros
- `models/informe.py`: el tipo de informe ahora debe estar en `TIPOS_PERMITIDOS` (antes cualquier texto servía y se usaba para armar el nombre del archivo, lo que permitía escribir fuera de la carpeta). Los informes se exportan a la carpeta `exportes/`.
- `config/entorno.py`: lee el `.env`; `.gitignore` excluye `.env`, `*.db`, `*.log` y `exportes/`.
- `config/database.py`: la base se crea junto al proyecto, sin depender de desde dónde se ejecute.

## Pendiente
El documento de uso de IA de la evaluación no está incluido: lo escribe quien entrega el trabajo, con lo que realmente hizo.
