from xmlrpc.server import SimpleXMLRPCServer
from multiprocessing import Process
import functions
import logging
import redis
import os

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

# Print proc example
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
    task='task'+str(taskNumber)+'-'+str(typeTask)
    taskNumber+=1
    print(str(task))
    
    nameFiles = nameFiles.replace("[", "")
    nameFiles = nameFiles.replace("]", "")

    if "," in nameFiles:
        arrayFiles = nameFiles.split(",")
        print(str(arrayFiles))
        #r.set(str(task), list(arrayFiles))
    else:
        print(str(nameFiles))
        #r.set(str(task), str(nameFiles))
    

# Word Count
def runWordCount(nameFiles):
    nameFilesArray(nameFiles, "W")
    return str(nameFiles)

# Count Words
server.register_function(runWordCount)

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
