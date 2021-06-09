1. Decisiones de diseño

Como primera decisión de diseño acordamos utilizar xml-rpc frente al grpc, debido a su
simplicidad.
Posteriormente dividimos el proyecto en tres ficheros:
- functions.py: dónde alojamos las funciones principales CountingWords y WordCount.
- sd_client.py: fichero de comunicación con el master. Es el encargado de comunicar la
creación, eliminación o listado de los workers y de enviar las tareas a realizar.
- sd_master.py: fichero de comunicación con redis. Es el encargado de crear, eliminar o
listar los workers y de añadir/eliminar tareas de la cola redis.

functions.py:
En el archivo de funciones alojamos, a parte de las funciones principales, una función auxiliar
que nos permite eliminar signos de puntuación para su posterior tratamiento en el
WordCount.
También utilizamos la librería request para poder acceder al contenido del fichero alojado en
el servidor.

sd_client.py:
En el archivo del cliente utilizamos las librerías xmlrpc.client y sys. Concretamente el
xmlrpc.client lo utilizamos para enviar la tarea a realizar al servidor y la librería sys para
captar los parámetros que introduce el usuario en la línea de comandos.
Comunicamos al servidor, mediante condicionales, la función a ejecutar según la tarea
introducida por el usuario.

sd_master.py:
En el archivo del master utilizamos las siguientes librerías:
- SimpleXMLRPCServer (xmlrpc.server): comunicación con el cliente.
- Process (multiprocessing): creación de workers.
- Functions: llamada a WordCount y CountingWords.
- Logging: registro de errores.
- Redis: gestión de las tareas y colas.
En dicho archivo almacenamos los workers en una lista global con un contador que
utilizamos como identificador. También iniciamos el servidor xml-rpc indefinidamente
mediante serve_forever( ).

Dentro de Redis hemos definido dos colas, una para las diferentes tareas a procesar
(queue:tasks) y otra que nos permite unir los diferentes resultados de las tareas procesadas
(queue:results). Ambas colas son inicializadas con un elemento vacío para solucionar el
problema a la hora de añadir las tareas a las colas.
Para la creación de las tareas que serán añadidas a la cola de Redis hemos decidido utilizar
una función donde recibimos el/los nombre/s del fichero/s y el tipo de programa a ejecutar.
Dentro de dicha función creamos una entrada en la cola queue:tasks, que se trata de una tupla
con el/los fichero/s a tratar y el programa a ejecutar. Por último, creamos una tarea adicional
donde en lugar de adjuntar el programa a ejecutar añadimos las tareas que deberá consultar el
worker en la cola de resultados (queue:results) para unificar todos los resultados en uno. En el
caso de tener un solo fichero en la tarea, el programa sigue el mismo diseño que al tener más
ficheros para tratar, es decir, si solamente se recibe un fichero también se creará la tarea
adicional.
Para la eliminación de los workers únicamente detenemos el último worker creado y
disminuimos el contador global.
Para la creación de los workers utilizamos la librería multiprocessing. Una vez creados los
workers automáticamente son iniciados y pasan a un bucle infinito donde leen
periódicamente la cola de redis (queue:tasks) esperando una tarea a realizar. Cuando leen una
tarea la retiran de la cola y la procesan. El resultado de la tarea es almacenado en otra cola
encargada de unificar los diferentes resultados (queue:results). Cada worker está capacitado
para realizar el procesamiento de una tarea y la unificación de los resultados obtenidos por
diversos workers, esto último es posible ya que añadimos la tarea adicional que contiene el
conjunto de tareas a consultar.

2. Juegos de pruebas

Hemos creado unos archivos simples para las pruebas. Estos contienen:
- fichero1: hola que tal
- fichero2: hola que hace usted

Prueba creando el worker primero:
● Creamos un worker.
● Ejecutamos countword con fichero1 y fichero2 por separado.
Resultados: 3 y 4 ✔️
● Ejecutamos wordcount con fichero1 y fichero2 por separado.
Resultados: hola, 1; que, 1; tal, 1; y hola, 1; que, 1; hace, 1; usted, 1; ✔️
● Ejecutamos countword con ambos archivos en la llamada.
Resultado: 7 ✔️
● Ejecutamos wordcount con ambos archivos en la llamada.
Resultado: hola, 2; que, 2; tal, 1; hace, 1; usted, 1; ✔️

Prueba creando las tareas primero:
● Ejecutamos countword con fichero1 y fichero2 por separado.
● Ejecutamos wordcount con fichero1 y fichero2 por separado.
● Ejecutamos countword con ambos archivos en la llamada.
● Ejecutamos wordcount con ambos archivos en la llamada.
● Creamos un worker.
Resultados: 3 y 4 ✔️
Resultados: hola, 1; que, 1; tal, 1; y hola, 1; que, 1; hace, 1; usted, 1; ✔️
Resultado: 7 ✔️
Resultado: hola, 2; que, 2; tal, 1; hace, 1; usted, 1; ✔️
Prueba con varios workers:
● Creamos dos workers.
● Ejecutamos countword con fichero1 una vez.
Resultado 1: 6
Resultado 2: 3 ✔️
Resultado 3: 3 ✔️
● Ejecutamos wordcount con fichero1 una vez.
Resultado 1: hola, 2; que, 2; tal, 2; hola, 2; que, 2; tal, 2;
Resultado 2: hola, 1; que, 1; tal, 1; ✔️
Resultado 3: hola, 1; que, 1; tal, 1; ✔️
● Ejecutamos countword con fichero1 dos veces.
Resultado: 6 ✔️
Resultado: 6 ✔️
Resultado: 6 ✔️
● Ejecutamos wordcount con fichero1 dos veces.
Resultado 1: hola, 2; que, 2; tal, 2; ✔️
Resultado 2: hola, 2; que, 2; tal, 2; ✔️
Resultado 3: hola, 2; que, 2; tal, 2; ✔
