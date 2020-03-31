'''
Yihui Peng
Ze Xuan Ong
Jocelyn Huang
Noah A. Smith
Yifan Xu

Usage: python viterbi.py <HMM_FILE> <TEXT_FILE> <OUTPUT_FILE>

Apart from writing the output to a file, the program also prints
the number of text lines read and processed, and the time taken
for the entire program to run in seconds. This may be useful to
let you know how much time you have to get a coffee in subsequent
iterations.
'''

import math
import sys
import time

from collections import defaultdict

# Magic strings and numbers
HMM_FILE = sys.argv[1]
TEXT_FILE = sys.argv[2]
OUTPUT_FILE = sys.argv[3]
TRANSITION_TAG = "trans"
EMISSION_TAG = "emit"
OOV_WORD = "OOV"         # check that the HMM file uses this same string
INIT_STATE = "init"      # check that the HMM file uses this same string
FINAL_STATE = "final"    # check that the HMM file uses this same string


class Viterbi():
    def __init__(self):
        # transition and emission probabilities. Remember that we're not dealing with smoothing 
        # here. So for the probability of transition and emission of tokens/tags that we haven't 
        # seen in the training set, we ignore thm by setting the probability an impossible value 
        # of 1.0 (1.0 is impossible because we're in log space)
        self.transition = defaultdict(lambda: defaultdict(lambda: 1.0))
        self.emission = defaultdict(lambda: defaultdict(lambda: 1.0))
        # keep track of states to iterate over 
        self.states = set()
        self.POSStates = set()
        # store vocab to check for OOV words
        self.vocab = set()

        # text to run viterbi with
        self.text_file_lines = []
        with open(TEXT_FILE, "r") as f:
            self.text_file_lines = f.readlines()

    def readModel(self):
        # Read HMM transition and emission probabilities
        # Probabilities are converted into LOG SPACE!
        with open(HMM_FILE, "r") as f:
            for line in f:
                line = line.split()

                # Read transition
                # Example line: trans NN NNPS 9.026968067100463e-05
                # Read in states as prev_state -> state
                if line[0] == TRANSITION_TAG:
                    (prev_state, state, trans_prob) = line[1:4]
                    self.transition[prev_state][state] = math.log(float(trans_prob))
                    self.states.add(prev_state)
                    self.states.add(state)

                # Read in states as state -> word
                elif line[0] == EMISSION_TAG:
                    (state, word, emit_prob) = line[1:4]
                    self.emission[state][word] = math.log(float(emit_prob))
                    self.states.add(state)
                    self.vocab.add(word)
        #print(self.states)
        # Keep track of the non-initial and non-final states
        self.POSStates = self.states.copy()
        self.POSStates.remove(INIT_STATE)
        self.POSStates.remove(FINAL_STATE)


    # run Viterbi algorithm and write the output to the output file
    def runViterbi(self):
        result = []
        for line in self.text_file_lines:
            result.append(self.viterbiLine(line))

        # Print output to file
        with open(OUTPUT_FILE, "w") as f:
            for line in result:
                f.write(line)
                f.write("\n")
        #print(f'result {result}\n')
        return result
    # TODO: Implement this

    # run Viterbi algorithm on a line of text 
    # Input: A string representing a sequence of tokens separated by white spaces 
    # Output: A string representing a sequence of POS tags.

    # Things to keep in mind:
    # 1. Probability calculations are done in log space. 
    # 2. Ignore smoothing in this case. For  probabilities of emissions that we haven't seen
    # or  probabilities of transitions that we haven't seen, ignore them. (How to detect them?
    # Remember that values of self.transition and self.emission are default dicts with default 
    # value 1.0!)
    # 3. A word is treated as an OOV word if it has not been seen in the training set. Notice 
    # that an unseen token and an unseen transition/emission are different things. You don't 
    # have to do any additional thing to handle OOV words.
    # 4. There might be cases where your algorithm cannot proceed. (For example, you reach a 
    #     state that for all prevstate, the transition probability prevstate->state is unseen)
    #     Just return an empty string in this case. 
    # 5. You can set up your Viterbi matrix (but we all know it's better to implement it with a 
    #     python dictionary amirite) in many ways. For example, you will want to keep track of 
    #     the best prevstate that leads to the current state in order to backtrack and find the 
    #     best sequence of pos tags. Do you keep track of it in V or do you keep track of it 
    #     separately? Up to you!
    # 6. Don't forget to handle final state!
    # 7. If you are reading this during spring break, mayyyyybe consider taking a break from NLP 
    # for a bit ;)

    def viterbiLine(self, line):
        words = line.split()
        self.Viterbi = defaultdict(lambda: defaultdict(lambda: 1.0))
        self.backpointers = defaultdict(lambda: defaultdict(lambda: 1.0))
        # TODO: Initialize DP matrix for Viterbi here
        '''for each state s from 1 to N do
            viterbi[s,1]←πs ∗ bs(o1)
            backpointer[s,1] ← 0
        '''
        self.states = list(self.states)
        self.POSStates = list(self.POSStates)
        #print(self.states)
        for i in range(len(self.states)):
            #print(self.states)
            curState = self.states[i]
            if words[0] not in self.vocab:
                words[0] = OOV_WORD
            if self.transition[INIT_STATE][curState] > 0:
                continue
            if self.emission[curState][words[0]] > 0:
                continue
            self.Viterbi[curState][0] = self.transition[INIT_STATE][curState] + self.emission[curState][words[0]]
            self.backpointers[curState][0] = curState

        for (t, word) in enumerate(words):
            # replace unseen words as oov
            if word not in self.vocab:
                word = OOV_WORD
            # TODO: Fill up your DP matrix
        #function VITERBI(observations of len T,state-graph of len N) 
            # print(f'transition {self.transition}\n')
            if t ==0: continue
            for i in range(len(self.states)): # cur state
                curStateI = self.states[i]
                curMax = -math.inf
                curMaxState = ""
                for j in range(len(self.states)): # prev state
                    curStateJ = self.states[j]
                    transJI = self.transition[curStateJ][curStateI] #as',s
                    if transJI > 0:
                        '''       print("continue\n")
                            print(f'curStateI {curStateI}\n')
                            print(f'curStateJ {curStateJ}\n')
                        '''
                        continue
                    curEmit = self.emission[curStateI][word]
                    if curEmit > 0:
                        continue
                    if self.Viterbi[curStateJ][t-1] == 1.0:
                        continue
                    curRes = transJI + curEmit + self.Viterbi[curStateJ][t-1]
                    #print(f'curRes {curRes}\n')
                    if curMax < curRes:
                        curMax = curRes
         #               print("ever\n")
                        curMaxState = curStateJ
                if (curMax != -math.inf):
                    self.Viterbi[curStateI][t] = curMax
                    #print(f'curMaxState {curMaxState}\n')
                    self.backpointers[curStateI][t] = curMaxState
        #        bestpath.append(curMax)
        # TODO: Handle best final state
        #print(f'transition {self.transition}\n')
        for j in range(len(self.states)):
            curState = self.states[j]
            if self.transition[curState][FINAL_STATE] > 0:
                continue
            if self.Viterbi[curState][len(words)-1] > 0:
                continue
            self.Viterbi[curState][len(words)] = self.transition[curState][FINAL_STATE] + self.Viterbi[curState][len(words)-1]
        #print(f'viterbi {self.Viterbi}\n')
        #print(f'backpointers {self.backpointers}\n')
        curMax = -math.inf
        curMaxState = ""
        for j in range(len(self.states)):
            curState = self.states[j]
            curRes = self.Viterbi[curState][len(words)]
            if curRes == 1.0:
                continue
            if curMax < curRes:
                curMax = curRes
                if type(curMaxState) != str:
                    print(f'final maxx : {curMaxState}')
                curMaxState = curState
        #print(f'final max : {curMaxState}\n')
        if curMaxState == "":
            return ""
        #self.backpointers[curState][len(word)] = curMaxState 
        # TODO: Backtrack and find the optimal sequence. 
        '''
        bestpathprob = max viterbi[s,T]
        bestpathpointer = argmax viterbi[s,T]
        '''
        '''
        bestpathprob = self.Viterbi[self.states[0]][len(word)-1]
        for j in range(1,len(self.states)):
            curState = self.states[j]
            bestpathprob = max(bestpathprob,self.Viterbi[curState][len(word)])
        #bestpath ← the path starting at state bestpathpointer, that follows backpointer[] to states back in time
        '''
#        print(f'final max : {curMaxState}\n')
        res = [curMaxState]
        #print(f'res : {res}')
        #print(f'backpointers {self.backpointers}\n')
        for j in range(len(words)-1,0,-1):
            if self.backpointers[curMaxState][j]==1.0:
                continue
            #print(f'added {self.backpointers[curMaxState]}\n')
            res.append(self.backpointers[curMaxState][j])
            #print(f'next max : {curMaxState}\n')
            curMaxState = self.backpointers[curMaxState][j]
        #print(f'final max : {curMaxState}\n')
        list.reverse(res)#bestpath, bestpathprob
        '''
        for j in range(len(self.states)):
            curState = self.states[j]
            print(f'backpointers row {j} {self.backpointers[curState]}\n')
        '''
        #print(f'res : {res}\n')
        #print(f'theres : {" ".join(res)}\n')
        #print(f'states {self.states}')
        #print(f'transition {self.transition}')
        return " ".join(res)


if __name__ == "__main__":
    # Mark start time
    t0 = time.time()
    viterbi = Viterbi()
    viterbi.readModel()
    viterbi.runViterbi()
    # Mark end time
    t1 = time.time()
    print("Time taken to run: {}".format(t1 - t0))

