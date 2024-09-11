



# CRM

## COMO MONTAR EL PROYECTO

Crear un archivo `.env` con las siguientes variables, 

```bash
# postgres environment
POSTGRES_PASSWORD=password # Su contraseña
POSTGRES_USER=postgres
POSTGRES_DB=crm
POSTGRES_PORT=5432
POSTGRES_HOST=crm-db

```

## CONFIGURAR DOCKER

### Iniciar

Realizar el comando `docker compose up`. en caso de error `CTRL + C` y y repetir el comando `docker compose up`.

### Usuario

Con el proyecto armado, realizar el comando `docker container ls` en otra terminal y copiar el `CONTAINER ID`.

Luego, realizar el siguiente comando `docker exec -it <CONTAINER ID COPIADO> sh`.

En la linea de comandos de python realizar el comando `python manage.py createsuperuser` y completar lo que pide.

Al tener el usuario creado, digitar `python manage.py drf_create_token <NOMBRE DE USUARIO CREADO>`. esto dará un token.

El Token que da llevarlo al POSTMAN y agregarlo en `Authorization`. en `Auth Type` escoger `OAuth 2.0`.

En el formulario que aparecerá a la derecha, ingresar el token dado y en `Header Prefix` escribir `Token`

