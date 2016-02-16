import time
import pygame
import sys
import os.path
from random import randint

if len(sys.argv) < 2:
	print "Need name of text file on command line which contains song information"
	quit()

if not os.path.exists(sys.argv[1]):
	print "%s does not exist" % sys.argv[1]
	quit()

configfile = open(sys.argv[1], "r")
configlines = configfile.readlines()
configfile.close()

if len(configlines) < 1 or len(configlines[0].split("\t")) < 3:
	print "configuration file does not contain necessary data"
	quit()

songname = configlines[0].split("\t")[0]
beattime = float(configlines[0].split("\t")[1])
starttime = float(configlines[0].split("\t")[2])

turns = 0
count = 0
freq = [0 for i in range(11)]
speakbeat = 8 if len(sys.argv) >= 3 and sys.argv[2] == "2" else 3
justcount = True if len(sys.argv) >= 3 and sys.argv[2] == "count" else False

pygame.init()
pygame.mixer.init()

nums = []
background = pygame.mixer.Sound(songname)
for i in range(0, 11):
	nums.append(pygame.mixer.Sound("audio/" + str(i) + ".aiff"))

channela = background.play()

start = time.time()

while channela.get_busy():
	pygame.time.delay(50)
	if (time.time() - start - beattime*count - starttime + 0.5) >= beattime:
		count = count + 1
		last = time.time()
		if justcount:
			nums[((count-1)%8)+1].play()
		elif ((count-1)%8)+1 == speakbeat:
			randnum = randint(0, 10)
			freq[randnum] = freq[randnum] + 1
			nums[randnum].play()
			if randnum == 9:
				count = count + 2*8
			if randnum in (1, 2, 5, 6, 9):
				turns = turns + 1
			if randnum in (3, 10):
				turns = turns + 2

print "finished with %d turns" % turns
for i in range(11):
	print "number of %ds: %d" % (i, freq[i])
