# EcoTech Solutions - Sistema de gestión (consola, MVC + SQLite)

Sistema de gestión interna en Python con arquitectura MVC (modelos, vistas, controladores) y base de datos SQLite.
Esta versión agrega login con contraseñas cifradas, roles, y consulta de servicios externos (clima y tipo de cambio).

## Cómo ejecutarlo

1. Instalar la librería: `pip install -r requirements.txt`
2. Ejecutar desde la carpeta del proyecto: `python main.py`

La primera vez:
- Se crea la base `ecotech.db` y el archivo `.env` con un secreto para cifrar las claves (formato en `.env.example`).
- El programa pide crear el primer administrador (queda como Superadmin).
- **No borres el `.env`** una vez creados usuarios: sin él las contraseñas guardadas dejan de coincidir.

## Roles

- **Administrador**: gestiona empleados, departamentos, proyectos, registros de tiempo e informes, y usa los servicios externos. Solo el **Superadmin** gestiona administradores.
- **Empleado**: ve sus datos, registra sus propias horas, ve sus registros y usa los servicios externos (solo con su propio salario).

## Carpetas

- `models/`: clases del dominio, DAO (acceso a SQLite) y `sesion.py`
- `views/`: menús y formularios de consola
- `controllers/`: lógica de cada módulo, `auth_controller.py` (login) y `servicios_controller.py` (APIs)
- `services/`: consumo de APIs (`cliente_http.py`, `clima_service.py`, `cambio_service.py`) y excepciones propias
- `config/`: base de datos, seguridad (hash de claves), lectura del `.env` y log de errores

Los errores técnicos quedan en `errores.log` y los informes exportados en la carpeta `exportes/`.
