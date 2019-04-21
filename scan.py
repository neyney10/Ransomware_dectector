import enchant

DEBUG = False
THRESHOLD = 90 # 90% valid english words
dictionary = enchant.Dict("en_US") 


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
def is_ascii(text):
    try:
        text.decode('ascii')
    except UnicodeDecodeError:
        return False
    else:
        return True

# https://stackoverflow.com/questions/3788870/how-to-check-if-a-word-is-an-english-word-with-python
# library: https://pypi.org/project/pyenchant/
def scan_file(filepath):
    amount_of_words = 0.0
    amount_of_matched_words = 0.0
    amount_of_unmatched_words = 0.0
    f = open(filepath,'r') # file to open.

    line = f.readline()
    while line:
        words = line.split(' ')
        for word in words:
            if len(word) <= 1:
                continue
            
            amount_of_words += 1

            if not is_ascii(word):
                raise NotAsciiError(filepath)

            if dictionary.check(word):
                #English Word
                amount_of_matched_words +=1
                if DEBUG:
                    print "A WORD HELL YEAH!!!! word: "+word
            else:
                #Not an English Word
                amount_of_unmatched_words += 1
                if DEBUG:
                    print "DAFAQ IS THIS SHIT??? word: "+word

        line = f.readline()

    f.close()

    valid_percent = (amount_of_matched_words/amount_of_words)*100
    if valid_percent < THRESHOLD:
        raise BelowThresholdError(filepath)

    if DEBUG:
        print "Summary: "+`amount_of_matched_words`+"/"+`amount_of_words`+" checked! which is " + str(valid_percent)+"%."
