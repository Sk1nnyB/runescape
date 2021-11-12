import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument("wordFile", type=argparse.FileType("r"))
parser.add_argument("inPath", type=str)
parser.add_argument("outPath", type=str)
args = parser.parse_args()

words = args.wordFile.read().splitlines()

args.wordFile.close()

punctuationList = ["?", "!", ",", ":", ";", "-", "{", "}", "[", "]", '"', "'", "(", ")", "."]

for file in os.listdir(args.inPath):

	inFile = open(args.inPath + "/" + file, "r")
	
	upper = 0
	punctuation = 0
	numbers = 0
	correct = 0
	incorrect = 0

	lines = inFile.readlines()
		
	for line in lines:
		newLine = ""
		for i in range(0, len(line)):
			char = line[i]
			if char.islower() or (char == " "):
				newLine = newLine + char
			elif char.isupper():
				upper = upper + 1
				newLine = newLine + char.lower()
			elif char.isnumeric():
				numbers = numbers + 1
			elif (char == ".") and ((i+1) != len(line)):
				if line[i+ 1] != ".":
					punctuation = punctuation + 1 
			elif char not in punctuationList:
				pass
			else: 
				punctuation = punctuation + 1

		newLine = newLine.split()

		for word in newLine:
			if word in words:
				correct = correct + 1
			else:
				incorrect = incorrect + 1

	wordsTot = incorrect + correct

	newFile = file
	newFile = newFile.replace(".txt", "_v36373bb.txt")

	outFile = open(args.outPath + "/" + newFile, "w")
	outFile.write("v36373bb\n")
	outFile.write("Formatting ###################" + "\n")
	outFile.write("Number of upper case words changed: " + str(upper) + "\n")
	outFile.write("Number of punctuations removed: " + str(punctuation) + "\n")
	outFile.write("Number of numbers removed: " + str(numbers) + "\n")
	outFile.write("Spellchecking ###################\n")
	outFile.write("Number of words: " + str(wordsTot) + "\n")
	outFile.write("Number of correct words: " + str(correct) + "\n")
	outFile.write("Number of incorrect words: " + str(incorrect) + "\n")

	outFile.close()
	inFile.close()
