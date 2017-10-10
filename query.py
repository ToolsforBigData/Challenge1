import regex as re
import numpy as np
import time 

##############################
#---------FUNTIONS-----------#
##############################

# Writes out the result to a text file.
def hms_string(sec_elapsed):
    h = int(sec_elapsed / (60 * 60))
    m = int((sec_elapsed % (60 * 60)) / 60)
    s = sec_elapsed % 60
    if sec_elapsed < 1:
        return "{:>04.5f} sec".format(sec_elapsed)
    else:
        return "{}:{:>02}:{:>05.2f}".format(h, m, s)

#---------------------
def generateQuery(query):
    '''
    Splits up the query strings into words and allowed characters between
    
    :param str query: The query string
    :return list[words, allowed characters] 
    '''
    query = query.replace('[',']')
    query = query.split(']')
    
    query_words = []
    query_len = []
    
    for i in range(len(query)):

        if i % 2:
            nums = query[i].split(',')
            nums= [int(num) for num in nums]
            query_len.append(nums)
        else:
            query_words.append(query[i])
            
    return query_words,query_len

#--------------------------------------#

def generateReg(words,between):
    '''
    Generates the regex used to find largest query. 
    
    :param list words: The list of the words in right order
    :param list between: The allowed characters between the words
    :return str: the regex string, e.g. (word1)(.{0,10})(word2)(.{0,20})(word3)
    '''
    streng = '('+words[0]+')'
    for i in range(1,len(words)):
        streng = streng + '(.{' + str(between[i-1][0]) +',' +str(between[i-1][1])+'})'
        streng = streng + '(' + words[i] + ')'
    pattern = re.compile(streng)

    return pattern

#--------------------------------------#
def findpos(sentence,word):
    '''
    Finds all position of the specific word in the sentence.
    
    :param string sentence: String to search through.
    :param string word: The word to be find in the variable sentence.
    return list: All index of the word. e.g. 'cat in a hat cat' -> word:cat [0,13] 
    '''
    pos = []   
    counter = 0

    # Finds all position of the word in the sentence.
    # Iterates until end of the sentence.            
    while True:
        try:
            if pos:
                pos.append(sentence.index(word,pos[counter]+1))
                counter = counter + 1
            else:
                pos.append(sentence.index(word,0))
        except ValueError:
            break
    return pos

#--------------------------------------#

def find_subpattern(thesentence,word,Space):
    '''
    Finds all unique sentences based on the word list and the allowed space between them.
    
    :param string thesentence: The sentence to search for patterns.
    :param list word: List contains words to search for.
    :param list Space: The allowed distance between word.
    return word_ok: Allowable position of words.
    '''
    # See the report to see a example of the find_subpattern function works
    
    # Create a list containing list of position of the word in string thesentence 
    word_list = []
    for i,val in enumerate(word):
        word_list.append(findpos(thesentence,val))
      
    word_list[0] = word_list[0][0]
    # Create all possibil combination of the position list.
    # e.g. [[1,2],[3,4]] -> [[1,3],[1,4],[2,3],[2,4]].
    allPos = [list(x) for x in np.array(np.meshgrid(*word_list)).T.reshape(-1,len(word_list))]

    # Now loop through every combination of the position and see if they make sens
    # or if the pattern fulfills the distance requriements 
    word_ok = []
    for word_comb in allPos:
        status = True
        for i in range(len(word_comb)-1):
            # Check first if the order of words in the all possibil combination
            # is correct.
            # Next if statement is to check if the distance requriements are fulfilled.
            if status and word_comb[i] > word_comb[i+1]:
                status = False
            elif status and ( (abs(word_comb[i+1] - word_comb[i]) - len(word[i]) < Space[i][0]) or (abs(word_comb[i+1] - word_comb[i]) - len(word[i]) > Space[i][1])):
                status = False
        if status: #If everything was ok! the add to the list
            word_ok.append((word_comb[0],word_comb[len(word_comb)-1]))
    return set(word_ok)
 

#--------Choosing file and path-------#
# Easiest is to create a file or use the files you used to test the code
dirpath = 'data/' #Change your path
filename = 'cathat' #Change the filename
Rfile = dirpath + filename


#--------Choosing Query-------#
#Change the query to something as 'text[number,number]text'
querystring = 'cat[1,30]in[1,10]hat'

#Trim the query string into words and between
words,between = generateQuery(querystring)
#Create the regex
regex = generateReg(words,between)

##--------Write out the result-------#
out = open(''+ querystring, 'w+')

#------Start timing here-------#
t0 = time.time()
counter = 0 # Counting matches
all_matches = []
#Open file and read line by line
with open(Rfile,encoding="utf8") as f:
    for line in f:
        subsentence = []
        #Check if the target words exist in article 
        if all(map(lambda w: w in line, words)):      
            #Iterate with regex 
            for m in re.finditer(regex,line,overlapped=True):
                #The query match
                found = m.group(0)
                F = found
                check_subpattern = False
                #Check if the is a submatch in the match
                for word in words:
                    found = found.replace(word,'',1)
                    if word in found:
                        check_subpattern = True
                        break
                # Find the submatches inside the line
                if check_subpattern:
                    for i in find_subpattern(F,words,between):
                        subsentence.append(F[i[0]:i[-1]+len(words[-1])])
                else:
                    subsentence.append(F)
        else:
            continue
        for i in subsentence:
            counter = counter + 1
            print(i)
            all_matches.append(i)
                    
t1 = time.time()
elapsed_time = t1 - t0
print("Elapsed time: {}".format(hms_string(elapsed_time)))
print("Number of matches found: " + str(counter))

#------------Printing out for peergrade, not for timing----------------#
out.write("Elapsed time: {}".format(hms_string(elapsed_time)))
out.write('\n')
out.write("Number of matches found: " + str(counter))
out.write('\n')
for match in all_matches:
    out.write(match+'\n')

out.close()