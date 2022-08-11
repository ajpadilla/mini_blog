## Descarga e instalación del proyecto

Para descargar el proyecto puedes clonar el repositorio:

    git clone https://github.com/j2logo/tutorial-flask.git
    
> Cada una de las lecciones se corresponde con una hoja del repositorio.
> El nombre de las hojas es "leccionXX".

Si quieres descargar una lección en concreto, ejecuta el siguiente comando git:

    git checkout tags/<leccionXX> -b <nombre-de-tu-rama>

Por ejemplo:

    git checkout tags/leccion1 -b leccion1

### Variables de entorno

Para que el miniblog funcione debes crear las siguientes variables de entorno:

#### Linux/Mac

    export FLASK_APP="entrypoint"
    export FLASK_ENV="development"
    export APP_SETTINGS_MODULE="config.local"

#### Windows

    set "FLASK_APP=entrypoint"
    set "FLASK_ENV=development"
    set "APP_SETTINGS_MODULE=config.local"
    
> Mi recomendación para las pruebas es que añadas esas variables en el fichero "activate" o "activate.bat"
> si estás usando virtualenv
 
### Instalación de dependencias

En el proyecto se distribuye un fichero (requirements.txt) con todas las dependencias. Para instalarlas
basta con ejectuar:

    pip install -r requirements.txt

## Ejecución con el servidor que trae Flask

Una vez que hayas descargado el proyecto, creado las variables de entorno e instalado las dependencias,
puedes arrancar el proyecto ejecutando:

    flask run
