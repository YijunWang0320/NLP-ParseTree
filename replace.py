import json
import sys

wordCount = dict()
def doCount(tree):
	if len(tree) == 2:
		if wordCount.has_key(tree[1]):
			wordCount[tree[1]] = wordCount[tree[1]] + 1
		else:
			wordCount[tree[1]] = 1
	else:
		doCount(tree[1])
		doCount(tree[2])

def doReplace(tree):
	if len(tree) == 2:
		if wordCount.has_key(tree[1]) and wordCount[tree[1]] < 5:
			tree[1] = "_RARE_"
	else:
		doReplace(tree[1])
		doReplace(tree[2])


if __name__ == '__main__':
	'''
		The InputFileName is up to you, since there are two trainning files
		parse_train.dat / parse_train_vert.dat
	'''
	if len(sys.argv) != 2:
		print 'Not enough parameters or too much parameters'
		sys.exit()
	
	InputFileName = sys.argv[1]
	OutputFileName = "parse_train_replaced.dat"
	fp = open(InputFileName,"r")

	for line in fp:
		tree = json.loads(line)
		doCount(tree)

	fp.close()
	fp = open(InputFileName,"r")
	wp = open(OutputFileName,"w")
	for line in fp:
		line = line.strip();
		tree = json.loads(line)
		doReplace(tree)
		wp.write(json.dumps(tree))
		wp.write('\n')

	wp.close()
