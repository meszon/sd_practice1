###
#   Raul Mesa - Victor Sentis
#   SD 2021
#   Script del servidor
#   File with functions
###

# Counting words function
def countingWords(fileName):
    totalWords = 0
    file = open(fileName, 'r')
    for line in file.readlines():
        if line != "\n":
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
    file = open(fileName, 'r')
    lines = tractarString(file.read()).split(" ")

    freqWord = []
    for word in lines:
        freqWord.append(lines.count(word))
    
    cadena = ""
    for tupla in list(zip(lines,freqWord)):
        cadena = cadena + tupla[0] + ", " + str(tupla[1]) + "; " 

    return cadena
    
