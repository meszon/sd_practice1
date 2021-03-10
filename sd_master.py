from xmlrpc.server import SimpleXMLRPCServer
import logging
import os

# Set up logging
logging.basicConfig(level=logging.INFO)

server = SimpleXMLRPCServer(
    ('localhost', 9000),
    logRequests=True,
)

def createWorker():
    return "Create worker"

server.register_function(createWorker)

def deleteWorker():
    return "Delete worker"

server.register_function(deleteWorker)

def listWorker():
    return "List worker"

server.register_function(listWorker)

def runWordCount():
    return "Run word count"

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
