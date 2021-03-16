from xmlrpc.server import SimpleXMLRPCServer
from multiprocessing import Process
import functions
import logging
import redis
import os
import json


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

    print(str(id))

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
    for i in arrayFiles:
        print("i: "+ str(i))
        task='task' + str(taskNumber)
        body=task + ';' + str(typeTask) + ';P;' + str(i)
        r.set (str(task), str(body))
        r.rpush('queue:pending', json.dumps(task))
        taskNumber+=1
    
    task='task' + str(taskNumber)
    body=task + ';' + str(typeTask) + ';R'
    r.set (str(task), str(body))
    taskNumber+=1
    r.rpush('queue:results', json.dumps(task))
    result = r.blpop(['queue:tasks'], 30)
    print(str(result))
 
 

# Word Count
def runWordCount(nameFiles):
    nameFilesArray(nameFiles, "W")
    return str(nameFiles)

server.register_function(runWordCount)

# Count Words
def runCountWords(nameFiles):
    nameFilesArray(nameFiles, "C")
    return str(nameFiles)

server.register_function(runCountWords)

# Start the server
try:
    print('Use Control-C to exit')
    server.serve_forever()
except KeyboardInterrupt:
    print('Exiting')
