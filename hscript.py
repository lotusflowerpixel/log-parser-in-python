import operator
filename = "SSH.log"
file = open(filename, "r")

ipDict = {}
getUser = []
pamArr = []
users = []
ipArray = []
counter = 0
for line in file: # parse each line
    invUsr = line.find('Invalid user ') # grab an invalid user line
    addAttempt = line.find('PAM ') # this returns an index, grab additional attempts
    if (invUsr != -1) and (invUsr not in getUser): # get the attempts
        getUser.append(line[invUsr:]) # showing the unique users
        for arr in getUser:
            splitUp = arr.split(None, 5)
            if splitUp[2] not in users:
                users.append(splitUp[2])
                ipArray.append(splitUp[4]) # prints the ip addresses
                ipAdr0 = splitUp[4]
                if ipAdr0 in ipDict:
                    ipDict[ipAdr0] += 1
                else:
                    ipDict[ipAdr0] = 1
                counter += 1
    elif (addAttempt != -1): # -1 would mean "PAM" was not found in the line
        pamArr.append(line[addAttempt:]) # adding "PAM" and everything after


for arr2 in pamArr: # the unchecked PAM lines
    pamDigit = arr2.split(None, 11) # split the PAM lines
    if pamDigit[1].isdigit(): # check if there is a digit
        attacker = pamDigit[10] # the ip address, with a = in front
        fakeIP = attacker.find('=') # find where it starts
        ipAdr = attacker[fakeIP+1:]
        if ipAdr in ipDict:
            ipDict[ipAdr] += int(pamDigit[1])
        else:
            ipDict[ipAdr] = int(pamDigit[1])
print counter
print ipDict
print max(ipDict.iteritems(), key=operator.itemgetter(1))[0]
