import sys
import json
import math

nonterDict = dict()
unrDict = dict()
binDict = dict()
wordDict = dict()

def doCount(CountFile):
	fp = open(CountFile,"r")
	for line in fp:
		line = line.strip()
		cfline = line.split(' ')
		if cfline[1] == 'NONTERMINAL':
			nonterDict[cfline[2]] = int(cfline[0])
		elif cfline[1] == 'UNARYRULE':
			unrDict[(cfline[2],cfline[3])] = float(cfline[0])/nonterDict[cfline[2]]
			wordDict[cfline[3]] = 1
		elif cfline[1] == 'BINARYRULE':
			binDict[(cfline[2],cfline[3],cfline[4])] = float(cfline[0])/nonterDict[cfline[2]]
		else:
			print 'There must be something wrong'
			return
	fp.close()

def loopBp(pai,bp,i,j,X,words):
	array = list()
	if i == j:
		array.append(X)
		array.append(words[i])
		return array
	left = loopBp(pai,bp,i,bp[(i,j,X)][3],bp[(i,j,X)][1],words)
	right = loopBp(pai,bp,bp[(i,j,X)][3]+1,j,bp[(i,j,X)][2],words)
	array.append(X)
	array.append(left)
	array.append(right)
	return array


def parseAndOutput(line):
	words = line.split(' ')
	pai = dict()
	bp = dict()
	n = len(words)
	for i in range(0,n):
		x = words[i]
		if words[i] not in wordDict.keys():
			x = '_RARE_'
		for X in nonterDict.keys():
			if (X,x) in unrDict.keys():
				pai[(i,i,X)] = unrDict[(X,x)]
			else:
				pai[(i,i,X)] = 0

	for l in range(1,n):
		for i in range(0,n-l):
			j = i + l
			for X in nonterDict.keys():
				pai[(i,j,X)] = 0
			for key in binDict.keys():
				X = key[0]
				for s in range(i,j):
					if pai[(i,j,X)] < binDict[key] * pai[(i,s,key[1])] * pai[(s+1,j,key[2])]:
						pai[(i,j,X)] = binDict[key] * pai[(i,s,key[1])] * pai[(s+1,j,key[2])]
						bp[(i,j,X)] = (key[0],key[1],key[2],s)
	TX = 'S'
	if pai[(0,n-1,'S')] == 0:
		tmax = 0
		for X in nonterDict.keys():
			if (0,n-1,X) in pai.keys():
				if pai[(0,n-1,X)] > tmax:
					tmax = pai[(0,n-1,X)]
					TX = X

	ret = loopBp(pai,bp,0,n-1,TX,words)
	return json.dumps(ret)

if __name__ == '__main__':
	CountFile = "cfg.counts"
	TestFile = "parse_dev.dat"
	OutputFile = "parse_result.dat"
	
	doCount(CountFile)
	fp = open(TestFile,"r")
	wp = open(OutputFile,"w")
	for line in fp:
		line = line.strip()
		wrJson = parseAndOutput(line)
		wp.write(wrJson)
		wp.write('\n')
	fp.close()
	wp.close()
