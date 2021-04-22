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
    
    for line in file:
        totalWords = totalWords + len(line.split(" "))
        
    return totalWords

def tractarString(fileTxt):
    fileTxt = fileTxt.replace("\n"," ")
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
    fileTxt = fileTxt.replace(":","")
    fileTxt = fileTxt.lower()
    return fileTxt

# Word count function
def wordCount(fileName):

    file = requests.get(fileName)
    lines = tractarString(file.text).split(" ")

    freqWord = []
    for word in lines:
        freqWord.append(lines.count(word))
    
    cadena = ""
    for tupla in list(zip(lines,freqWord)):
        if tupla[0] != " ":
            cadena = cadena + tupla[0] + ", " + str(tupla[1]) + "; " 

    return cadena
    
