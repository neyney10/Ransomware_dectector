import enchant # (pip install PyEnchant) | library: https://pypi.org/project/pyenchant/


## GLOBAL VARIBALES ##
DEBUG = False
THRESHOLD               = 90  # 90% valid english words
amount_of_words         = 0.0 # reset every call
amount_of_matched_words = 0.0 # reset every call
filepath                = ''  # reset every call
dictionary              = enchant.Dict("en_US")


# see: https://stackoverflow.com/questions/1319615/proper-way-to-declare-custom-exceptions-in-modern-python
class NotAsciiError(Exception):
    def __init__(self, filename):
        # Call the base class constructor with the parameters it needs
        super(NotAsciiError, self).__init__("In file: [" + filename + "] The text contains non-ascii characters!")
        self.filename = filename

class BelowThresholdError(Exception):
    def __init__(self, filename):
        # Call the base class constructor with the parameters it needs
        super(BelowThresholdError, self).__init__("In file: [" + filename + "] The amount of matched english words in the text is below the given threshold!")
        self.filename = filename

# see: https://www.tutorialspoint.com/How-to-check-if-a-string-in-Python-is-in-ASCII

# checks if the string contains only ascii characters.
## Input : text as string.
## Output: True, if contains only ascii characters.
##         False, otherwise.
def is_ascii(text):
    try:
        text.decode('ascii')
    except UnicodeDecodeError:
        return False
    else:
        return True

# Scan a single line of string for encrypted text.
# Raises exceptions: "NotAsciiError" as the line contains non-ascii character.
## Input : line as string.
## Output: None.
def scan_line(line):
    words = line.split(' ')
    for word in words:
        if len(word) <= 1:
            continue

        scan_word(word)
        
# Scan a single word of string for encrypted text.
# Raises exceptions: "NotAsciiError" as the line contains non-ascii character.
## Input : word as string.
## Output: None.
def scan_word(word):
    global amount_of_words, amount_of_matched_words
    amount_of_words += 1

    if not is_ascii(word):
        global filepath
        raise NotAsciiError(filepath)

    if dictionary.check(word):
        #English Word
        amount_of_matched_words +=1
        if DEBUG:
            print "A WORD HELL YEAH!!!! word: "+word
        else:
            #Not an English Word
            if DEBUG:
                print "DAFAQ IS THIS SHIT??? word: "+word

# Scan a text file for encrypted text.
# Raises exceptions: "NotAsciiError" as the line contains non-ascii character.
#                    "BelowThresholdError" as many words are detected to be non-english.
## Input : fp - filepath as string.
## Output: None.
### https://stackoverflow.com/questions/3788870/how-to-check-if-a-word-is-an-english-word-with-python
def scan_file(fp):
    global amount_of_words, amount_of_matched_words, filepath
    amount_of_words = 0.0
    amount_of_matched_words = 0.0
    filepath = fp

    f = open(filepath,'r') # file to open.

    line = f.readline()
    while line:
        scan_line(line)
        line = f.readline()

    f.close()

    valid_percent = (amount_of_matched_words/amount_of_words)*100
    if valid_percent < THRESHOLD:
        raise BelowThresholdError(filepath)
        
    if DEBUG: 
        print "Summary: "+`amount_of_matched_words`+"/"+`amount_of_words`+" checked! which is " + str(valid_percent)+"%."
