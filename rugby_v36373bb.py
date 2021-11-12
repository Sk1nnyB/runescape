import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument("inPath", type=str)
parser.add_argument("outPath", type=str)
args = parser.parse_args()

for file in os.listdir(args.inPath):

	inFile = open(args.inPath + "/" + file, "r")

	lines = inFile.readlines()
	team1 = 0
	team2 = 0

	for line in lines:
		input = line
		for i in range(0, len(line), 3):
			if input[i+1] == "1":
				if input[i+2] == "t":
					team1 = team1 + 5
				if input[i+2] == "c":
					team1 = team1 +  2
				if input[i+2] == "p":
					team1 = team1 +  3
				if input[i+2] == "d":
					team1 = team1 +  3
			elif input[i+1] == "2":
				if input[i+2] == "t":
					team2 = team2 + 5
				if input[i+2] == "c":
					team2 = team2 + 2
				if input[i+2] == "p":
					team2 = team2 + 3
				if input[i+2] == "d":
					team2 = team2 + 3
		

	winner = ""
	result = team1 - team2

	if result > 0:
		winner = "Team 1"
	elif 0 > result:
		winner = "Team 2"
	else:
		winner = "Draw"

	newFile = file
	newFile = newFile.replace(".txt", "_v36373bb.txt")

	outFile = open(args.outPath + "/" + newFile, "w")

	outFile.write(str(team1) + ":" + str(team2))

	outFile.close()
	inFile.close()