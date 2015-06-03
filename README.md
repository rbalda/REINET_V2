# REINET_V2
Proyecto Red De Innovacion del ecuador V.2.0


##Estructura del Proyecto REINET
La estructura de la aplicacion la crea Django siguiendo el patron MTV(Model Template View), que es bastante similar al patron MVC(Model  View Controller). por lo que cada modelo, template y view estan en archivos de script independientes.

Los templates seran nombrados de acuerdo a la pantalla que vayan representar, con minusculas y si son nombres compuestos se pondra un '_' en lugar de espacio se definira una plantilla base para que el sitio no pierda consistencia, por lo que los desarrolladores tendran que extender de el, para su efecto dejo el siguiente [link](https://docs.djangoproject.com/en/1.8/ref/templates/)

<br/>
###Arbol de ficheros y archivos
**REINET** &emsp;&emsp;&emsp;&emsp;&emsp;&lt;------- Carpeta raíz del proyecto<br />
├── manage.py&emsp;&emsp;&lt;------- Archivo que ejecuta tareas administrativas del proyecto<br />
├── **REINET**&emsp;&emsp;&lt;------- Carpeta que contiene archivos de configuración del proyecto<br />
│&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── settings.py&emsp;&emsp;&lt;------- Archivo que contiene configuración del proyecto<br />
│&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── urls.py&emsp;&emsp;&lt;------- Archivo que contiene las urls de todos los modulos<br />
│&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;└── wsgi.py&emsp;&emsp;&lt;------- Archivo que contiene configuracion para hacer el deploy<br />
├── **templates**&emsp;&emsp;&lt;------- Fichero donde se guardaran las plantillas comunes en el proyecto<br />
├── **static**&emsp;&emsp;&lt;------- Fichero donde se guardaran los archivos staticos ej: JS/CSS/media/img<br />
└── **usuarios**&emsp;&emsp;&lt;------- Fichero que contiene los Modelos, Vistas, Templates y Urls de cada app o modulo.<br />
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── admin.py
&emsp;&emsp;&lt;------- Archivo que registrara los modelos que se pueden agregar usando el admin de django.<br />
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── migrations
&emsp;&emsp;&lt;------- Fichero que contiene las migraciones de la base de datos<br />
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── models.py&emsp;&emsp;&lt;------- Script donde se guardaran los modelos de datos<br />
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── **templates**&emsp;&emsp;&lt;------- Fichero donde se guardaran los templates de la aplicacion o modulo<br />
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;│
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;   ├── Institucion_Sign-up.html&emsp;&emsp;&lt;------- Template definido a nivel de modulo<br />
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;│
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;   ├── profile_usuario.html<br />
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;│
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;   └── sign-up.html<br />
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── tests.py&emsp;&emsp;&lt;------- Script donde se registraran las pruebas unitarias a ser ejecutadas <br />
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── urls.py&emsp;&emsp;&lt;------- Archivo que contiene las url del modulo o app<br />
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;└── views.py&emsp;&emsp;&lt;------- Script donde se registraran las vistas que atenderan la logica del modulo<br />


