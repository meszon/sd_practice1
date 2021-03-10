import xmlrpc.client
import sys

proxy = xmlrpc.client.ServerProxy('http://localhost:9000')
#print(proxy.command('file1.txt, file2.txt'))

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
            print(proxy.runWordCount())

        if arguments[2] in "run-countwords":
            print(proxy.runCountWords())           

