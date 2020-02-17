#str_testVar = "UR'URBLF2B2UR'B'DL'DB'LF2B'U" # Length = 27
#ls_testVar = ["U", "R'", "U", "R", "B", "L", "F2", "B2", "U", "R'", "B'", "D", "L'", "D", "B'", "L", "F2", "B'"]

import random # Testing purposes

def returnParsedStr(str_Mixup):
    ls_Mixup = []
    for i in range(len(str_Mixup)):
        if (i >= len(str_Mixup)) or ((str_Mixup[i] == "'") or (str_Mixup[i] == "2")): continue
        #print("Index " + str(i) + ": " + str_Mixup[i])
        if (i < (len(str_Mixup) - 1)) and ((str_Mixup[i + 1] == "'") or (str_Mixup[i + 1] == "2")):
            ls_Mixup.append(str_Mixup[i] + str_Mixup[i + 1])
        else:
            ls_Mixup.append(str_Mixup[i])
    return ls_Mixup

'''
def tb_parser(movesMax, iterations):
    def runBench(moves):
        def generateBench(moves):
            def outputFace():
                return random.choice(["U", "R", "F", "D", "L", "B"])
            def outputParam():
                return random.choice(["'", "2", ""])
            ls_movesBench = []
            for i in range(moves):
                ls_movesBench.append(str(outputFace() + outputParam()))
            return ls_movesBench
        ls_movesBench = generateBench(moves)
        str_movesBench = ''.join(ls_movesBench)
        ls_parsed = returnParsedStr(str_movesBench)
        if ls_parsed != ls_movesBench:
            return False
        else:
            return True
    itr_bench = []
    for k in range(iterations):
        itr_bench.append(runBench(movesMax))
    if False in itr_bench:
        print("Failure detected")
    return itr_bench
'''

#print(tb_parser(200000, 20))