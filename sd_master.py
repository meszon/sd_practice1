from xmlrpc.server import SimpleXMLRPCServer
from multiprocessing import Process
import logging
import redis
import os

# Workers
workers = {}
worker_id = 0

# Set up logging
logging.basicConfig(level=logging.INFO)

server = SimpleXMLRPCServer(
    ('localhost', 9000),
    logRequests=True,
)
    
# Create worker
def createWorker():
    global workers
    global worker_id

    proc = Process(target=printProcess, args=(worker_id,))
    proc.start()
    workers[worker_id] = proc
    worker_id += 1

    #return "Create worker"
    return str(proc)

server.register_function(createWorker)

# Print proc example
def printProcess(id):
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

# Word Count
def runWordCount():
    return "Run word count"

# Count Words
server.register_function(runWordCount)

def runCountWords():
    return "Run count words"

server.register_function(runCountWords)



# Start the server
try:
    print('Use Control-C to exit')
    server.serve_forever()
except KeyboardInterrupt:
    print('Exiting')
