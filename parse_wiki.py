from lxml import etree
from xml.sax.saxutils import escape
import re

#------------------CHOOSE WHICH ARTICLE TYPES YOU WANT-------------------------
# 1: only the cat article from Wikipedia
# 2: All articles that start with the letter 'a' from Wikipedia
# 3: All articles from Wikipedia
case = 1

if case == 1:
	new_filename = 'wiki_cats'
elif case ==2:
	new_filename = 'wiki_only_a'
elif case ==3:
	new_filename = 'wiki_all'
else:
	print('wrong case choosen')

#To escape special characters
chardic = {"\"": "&quot;", "<": "&lt;",  ">": "&gt;"}

#------------------CHOOSE FILEPATH FOR READ AND WRITE--------------------------
dirpath = 'data/'
filename = 'wiki_big'
#-------------------------------PARSER-----------------------------------------
# Destination and filename
xmlFile = dirpath+filename

# Open the file to write lines in.
out = open(dirpath + new_filename, 'w+')

# Define the Taggers, I know it is ugly but I mean...
titleTagger = '{http://www.mediawiki.org/xml/export-0.10/}title'
textTagger = '{http://www.mediawiki.org/xml/export-0.10/}text'
redirectTagger = '{http://www.mediawiki.org/xml/export-0.10/}redirect'
nsTagger = '{http://www.mediawiki.org/xml/export-0.10/}ns'

# Get the iterparse ready, and set tag flag.
context = etree.iterparse(xmlFile, events=('end',), tag=(titleTagger, textTagger, redirectTagger, nsTagger))

for event, elem in context:
    if elem.tag == titleTagger:
        # Set the temporary variable as the title of the article
        temp = elem.text.lower()

    elif elem.tag == redirectTagger:
        # Set the temporary varialbe as a string to dentify it from title tag
        temp = 'Redirect Title'

    elif elem.tag == nsTagger:
        #Only take pages with namespace  == 0
        if elem.text == '0':
            nsBool = True
        else:
            nsBool = False
            
    if elem.tag == textTagger and nsBool == True:

        if case == 1 and temp == 'cat':
            # Replace new line with space and change to lower case, write to file.    
            temptext = re.sub(r'\n+',' ',str(escape(elem.text,chardic)))
            out.write(temptext.lower()+"\n")

            #Break because we don't want to iterate through all.
            break

        elif case == 2 and temp[0] == 'a': #Only take title that start with a
            # Replace new line with space and change to lower case, write to file.
            temptext = re.sub(r'\n+',' ',str(escape(elem.text, chardic)))
            out.write(temptext.lower()+"\n") 
    
        elif case == 3 and temp != 'Redirect Title': #If redirect don't write 
            # Replace new line with space and change to lower case, write to file.
            temptext = re.sub(r'\n+',' ',str(escape(elem.text, chardic)))
            out.write(temptext.lower()+"\n")
        
    # It's safe to call clear() here because no descendants will be accessed
    elem.clear()
    # Also eliminate now-empty references from the root node to the tag
    while elem.getprevious() is not None:
        del elem.getparent()[0]

#Close the file
out.close()
