import requests
###
#   Raul Mesa - Victor Sentis
#   SD 2021
#   Script del servidor
#   File with functions
#   Install requests: python3 -m pip install requests
#   Call server: python3 -m http.server
###

# Counting words function
def countingWords(fileName):
    totalWords = 0
    file = requests.get(fileName)
    file = file.text.splitlines()
    #file = open(fileName, 'r')
    #for line in file.readlines():
    for line in file:
        #if line != "\n":
        totalWords = totalWords + len(line.split(" "))
        
    return totalWords

def tractarString(fileTxt):
    fileTxt = fileTxt.replace("\n","")
    fileTxt = fileTxt.replace(",","")
    fileTxt = fileTxt.replace(".","")
    fileTxt = fileTxt.replace(";","")
    fileTxt = fileTxt.replace("(","")
    fileTxt = fileTxt.replace(")","")
    fileTxt = fileTxt.replace("\"","")
    fileTxt = fileTxt.replace("?","")
    fileTxt = fileTxt.replace("¿","")
    fileTxt = fileTxt.replace("!","")
    fileTxt = fileTxt.replace("¡","")
    fileTxt = fileTxt.lower()
    return fileTxt

# Word count function
def wordCount(fileName):

    file = requests.get(fileName)
    #file = open(fileName, 'r')
    #lines = tractarString(file.read()).split(" ")
    lines = tractarString(file.text).split(" ")

    freqWord = []
    for word in lines:
        freqWord.append(lines.count(word))
    
    cadena = ""
    for tupla in list(zip(lines,freqWord)):
        cadena = cadena + tupla[0] + ", " + str(tupla[1]) + "; " 
    print(cadena)

    return cadena
    
