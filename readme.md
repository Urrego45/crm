



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

### Postman

Link de postman https://www.postman.com/lunar-satellite-896921/workspace/prueba-crm/collection/23247546-33d4b65f-dabd-4a30-ac90-d0795b0c06d9?action=share&creator=23247546

Rutas:
api/cve/sincronizar/ => Sincronizar los datos de la API con la aplicacion.

api/cve/vulnerabilidad/ => Consultar las vulnerabilidades registradas.

api/cve/descripcion/ => Consultar las descripciones de las vulnerabilidades registradas.

api/cve/metrica/ => Consultar las metricas de las vulnerabilidades registradas.

api/cve/dato-metrica/ => Contultar los datos de lass metricas registrradas.

api/cve/solucion-vulnerabilidad/ => Consultar las soluciones de las vulnerabilidades. ademas de crear las soluciones `{'vulnerabilidad': <uuid vulnerabilidad>}`.

api/cve/vulnerabilidad-sin-soluciones/ => Consulta todas las vulnerabilidades sin solucion.

api/cve/vulnerabilidad-severidad/ => Cuenta por cada severidad y devuelve una suma.
