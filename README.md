# Recom-Proyect
## Correr la página en Windows
Primero, se deben instalar todos los [módulos especificados](#Requerimientos) con ```py -m pip install x```. Luego, abrir la Command Line de la computadora y dirigirse a la dirección donde fueron instalados y descomprimidos los archivos del repositorio. Por último, definir una environment variable dentro del entorno del sistema con ```set FLASK_APP=datingapp```, para luego correr la aplicación con ```flask run```.
<br>Alternativamente, se puede acceder al entorno virtual definido dentro de los archivos para evitar instalar todos los módulos en el sistema. Para utilizar el entorno virtual, dirigirse a la dirección donde fue descomprimido el programa para actualizar las direcciones del intérprete de python y del venv en sí en *pyvenv.fg*, *activate*, *activate.bat* y *activate.ps1*. Una vez hecho esto, correr el archivo *activate.ps1* en el cmd para activar el entorno. Por último, definir FLASK_APP como se mencionó anteriormente y correr la aplicación con ```flask run```. 
<br><br>Para acceder a la aplicación, dirigirse a http://127.0.0.1:5000 dentro del navegador.
## Requerimientos:
  * Python == 3.10.4
  * Jinja2 == 3.1.2
  * Flask == 2.1.3
  * WTForms   == 3.0.0
  * Neo4j == 4.4.5
  * Py2neo == 2021.1
  * Flask-WTF == 1.0.1
  * Passlib   == 1.7.4
