from xmlrpc.server import SimpleXMLRPCServer
from multiprocessing import Process
import functions
import logging
import time
import redis
import os
import json

###
#   Raul Mesa - Victor Sentis
#   SD 2021
#   Script del servidor
###

# Workers
workers = {}
worker_id = 0

# Task number
taskNumber = 0

# Set up logging
logging.basicConfig(level=logging.INFO)

# Server to sd_client.py
server = SimpleXMLRPCServer(
    ('localhost', 9000),
    logRequests=True,
)

# Redis database connection
r = redis.Redis(host='localhost', port=6379, db=0)
r.flushall

# Create first element in queue
r.rpush('queue:tasks', "")
r.rpush('queue:results', "")
    
# Create worker
def createWorker():
    global workers
    global worker_id

    proc = Process(target=startWorker, args=(worker_id,))
    proc.start()
    workers[worker_id] = proc
    worker_id += 1

    #return "Create worker"
    return str(proc)

server.register_function(createWorker)

# Start worker
def startWorker(id):
    global workers
    while True:
        queue_list = r.lrange('queue:tasks', 1, -1) # Guardar en una lista la queue
        if queue_list:
            # Selecciona una tarea
            task = r.lindex('queue:tasks', 1)   # Get de la posición 1
            r.lrem('queue:tasks', 1, task)      # Eliminar la posición 1 de queue
            task = str(task).replace("b", "").replace("\'", "")
            arrayTask = task.split(";")
            # Tareas con archivos / realizan una de las funciones
            if len(arrayTask) > 2:
                if arrayTask[1] == "Wordcount":
                    result = functions.wordCount(arrayTask[2])
                
                else:
                    result = functions.countingWords(arrayTask[2])

                task = arrayTask[0] + ":" + str(result)
                r.rpushx('queue:results', task)

            # Tareas que unen resultados
            else:
                    # Operamos con la segunda queue
                    queue_result = r.lrange('queue:results', 1, -1)
                    id_task = str(arrayTask[0]) # Id tarea que une 
                    type_task = str(arrayTask[1])
                    i = 0
                    pos = 0
                    while i < len(queue_result):
                        if id_task in str(queue_result[i]): # Obtenemos su posicion en la cola
                            pos = i + 1                     # para borrarla y que otro worker no haga la misma tarea
                            break
                            
                        i = i + 1

                    # Buscamos las tareas que debe unir
                    result_task = r.lindex('queue:results', pos)
                    r.lrem('queue:results', pos, result_task)
                    result_task = str(result_task).replace("b", "").replace("\'", "").split(":")
                    id_pending_tasks = str(result_task[1]).split(";")  # Id de las tareas a unir (sus resultados)
                    id_pending_tasks.remove(id_pending_tasks[-1])
                    acc = 0 # Acumulador
                    
                    # Buscamos los resultados que debe unir
                    list_pos_task_done = [] # Lista con las tareas ya unidas
                    freqWord = []
                    cadena = ""
                    text = ""
                    for t in id_pending_tasks:
                        j = 1
                        pos = 0
                        while j < len(queue_result):
                            if str(t) in str(queue_result[j]):
                                pos = j
                                list_pos_task_done.append(pos)      # Guardamos las posiciones
                                result_pending_task = r.lindex('queue:results', pos)
                                list_pos_task_done.append(result_pending_task)  # Guardamos el resultado
                                result_pending_task = str(result_pending_task).replace("b", "").replace("\'", "").split(":")
                                if type_task == "Countwords":
                                    acc = acc + int(result_pending_task[1])
                                else:
                                    text = text + "".join([i for i in result_pending_task[1] if not i.isdigit()])    #eliminamos los numeros     

                            j = j + 1

                    text = functions.tractarString(text)    #eliminamos , ; y caracteres especiales
                    text = text.replace("\n"," ")           #eliminamos el salto de linea
                    lines = functions.tractarString(text).split("  ") # 2 espacios
                    for word in lines:
                        freqWord.append(lines.count(word))               
                    for tupla in list(zip(lines,freqWord)):
                        if tupla[0] not in cadena:          #mostamos cada palabra solo una vez
                            cadena = cadena + tupla[0] + ", " + str(tupla[1]) + "; " 
                    print(cadena)
                    
                    #eliminamos tareas unidas (ya procesadas)
                    l = 0
                    while l < len(list_pos_task_done):
                        r.lrem('queue:results', list_pos_task_done[l], list_pos_task_done[l+1])
                        l = l + 2



# Delete worker
def deleteWorker():
    global workers
    global worker_id

    worker_id -=1
    proc = workers[worker_id]
    proc.kill()
    print(str(worker_id))

    return "Delete worker"

server.register_function(deleteWorker)

# List worker
def listWorker():
    return "List worker"

server.register_function(listWorker)

# Name files adaptation
def nameFilesArray(nameFiles, typeTask):
    global taskNumber
    nameFiles = nameFiles.replace("[", "")
    nameFiles = nameFiles.replace("]", "")
    arrayFiles = nameFiles.split(",")
    result_tasks = ""

    for i in arrayFiles:
        #print("i: "+ str(i))
        task='task' + str(taskNumber)
        result_tasks = result_tasks + task + ";"
        body=task + ';' + str(typeTask) + ';' + str(i)
        r.rpushx('queue:tasks', body)
        taskNumber+=1
    
    task='task' + str(taskNumber)
    taskNumber+=1
    body=task + ';' + str(typeTask)
    r.rpushx('queue:tasks', body)
    body_tasks = task + ":" + result_tasks
    r.rpushx('queue:results', body_tasks)
 
# Word Count
def runWordCount(nameFiles):
    nameFilesArray(nameFiles, "Wordcount")
    return str(nameFiles)

server.register_function(runWordCount)

# Count Words
def runCountWords(nameFiles):
    nameFilesArray(nameFiles, "Countwords")
    return str(nameFiles)

server.register_function(runCountWords)

# Start the server
try:
    print('Use Control-C to exit')
    server.serve_forever()
except KeyboardInterrupt:
    print('Exiting')
