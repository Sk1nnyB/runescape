import argparse
import os

def algorithmFun(data):
	algorithm = ""
	for i in range (0, len(data)):
		if data[i] == ":":
			return(algorithm)
		else:
			algorithm = algorithm + data[i]

def cipherTextFun(data, algorithm):
	cipherText = ""
	trigger = 0
	for i in range (0, len(data)):
		if trigger == 1:
			cipherText = cipherText+ data[i]
		if data[i] == ":":
			trigger = 1

	return(cipherText)

parser = argparse.ArgumentParser()
parser.add_argument("inPath", type=str)
parser.add_argument("outPath", type=str)
args = parser.parse_args()

morseDictionary = { "/":" ", ".-":"a", "-...":"b", "-.-.":"c", "-..":"d", ".":"e", "..-.":"f", "--.":"g", "....":"h", "..":"i", ".---":"j", "-.-":"k", ".-..":"l", "--":"m", "-.":"n", "---":"o", ".--.":"p", "--.-":"q", ".-.":"r", "...":"s", "-":"t", "..-":"u", "...-":"v", ".--":"w", "-..-":"x", "-.--":"y", "--..":"z", ".----":"1", "..---":"2", "...--":"3", "....-":"4", ".....":"5", "-....":"6", "--...":"7", "---..":"8", "----.":"9", "-----":"0", "--..--":", ", ".-.-.-":".", "..--..":"?", "-..-.":"/", "-....-":"-", "-.--.":"(", "-.--.-":")", ".----.":" '", "-.-.--":"!", "---...":":", '.-..-.':'"', "_._._.":";","_...._":"–"}

for file in os.listdir(args.inPath):

	inFile = open(args.inPath + "/" + file, "r")

	data = inFile.readline()
	algorithm = algorithmFun(data)
	cipherText = cipherTextFun(data, algorithm)
	plainText = ""

	if algorithm == "Hex":
		plainText = bytearray.fromhex(cipherText).decode().lower()

	elif algorithm == "Caesar Cipher(+3)":
		for char in cipherText:
			if 64 < ord(char) < 91 or 96 < ord(char) < 123:
				aschar = ord(char) - 3
				if aschar < 65 or 90 < aschar < 97:
					aschar = aschar + 26 
				plainText = plainText + chr(aschar).lower()			
			else:
				plainText = plainText + char.lower()


	elif algorithm == "Morse Code":
		letter = ""
		for char in cipherText:
			if char != " " and char !="":
				letter = letter + char
			else:
				plainText = plainText + morseDictionary[letter]
				letter = ""

		plainText = plainText + morseDictionary[letter]
	
	
	newFile = file
	newFile = newFile.replace(".txt", "_v36373bb.txt")

	outFile = open(args.outPath + "/" + newFile, "w")
	outFile.write(plainText)

	outFile.close()
	inFile.close()



