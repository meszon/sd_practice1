import xmlrpc.client
import sys
###
#   Raul Mesa - Victor Sentis
#   SD 2021
#   Script del cliente
#   Ejemplo llamada: python3 client.py job run-wordcount [fitxer1, fitxer2]
#   python3 sd_client.py worker create/delete
#   redis-server 
#   redis-cli
###

proxy = xmlrpc.client.ServerProxy('http://localhost:9000')

arguments = sys.argv

if "worker" in arguments:
        if arguments[2] in "create":
            print(proxy.createWorker())

        if arguments[2] in "delete":
            print(proxy.deleteWorker())

        if arguments[2] in "list":
            print(proxy.listWorker())


if "job" in arguments:
        if arguments[2] in "run-wordcount":
            nameFiles = arguments[3]
            print(proxy.runWordCount(nameFiles))

        if arguments[2] in "run-countwords":
            nameFiles = arguments[3]
            print(proxy.runCountWords(nameFiles))           

