#coding: latin1

# This is abandoned. I chose another way.


# based on a snippet from David Mertz's article
# "Developing a Full-Text Indexer in Python"
# http://www-106.ibm.com/developerworks/xml/library/l-pyind.html
# http://gnosis.cx/publish/programming/charming_python_15.html


"""
- copied only TextSplitter
- renamed splitter() to split() (because a method name should be averb...)

- TextSplitter does *only* filetype "text/plain". I plan to write one
  subclass for each filetype. Class attribute mimetype.

"""
import string


## xalphas = {
##     "cp1252" : "ÄöÖüÜßàâéêèîôûùëçáõÕä",    
##     "cp850" : "".join(map(chr,[ 142, 148, 153, 129, 154, 225,
##                                 133, 131, 130, 136, 138, 140,
##                                 147, 150, 151, 137, 135, 160,
##                                 228, 229, 132]))
##     # this list was generated using tests/etc/7.py
##     }

#-- "Split plain text into words" utility function
class TextSplitter:
    
    mimetype = "text/plain"
    
    def __init__(self,coding):
        self.coding = coding

        for i in range(127,256):
            print i, ":", repr(chr(i).decode(coding))
            
        x = [chr(i).decode(coding) for i in range(127,256)]
        self.xalphas = "".join([ch.encode(coding) for ch in x
                                if ch.isalpha()])
        
##         self.xalphas = "".join(map(chr,[i for i in range(127,256)
##                                 if chr(i).decode(coding).isalpha()]))
        
        prenum  = string.join(map(chr, range(0,48)), '')
        num2cap = string.join(map(chr, range(58,65)), '')
        cap2low = string.join(map(chr, range(91,97)), '')
        
        postlow = string.join(map(chr, range(123,256)), '')


        
        nonword = prenum + num2cap + cap2low + postlow
        
        self.word_only = string.maketrans(nonword, " "*len(nonword))
        
        self.nondigits = string.join(
            map(chr, range(0,48)) + map(chr, range(58,255)), '')
        
        self.alpha = string.join(
            map(chr, range(65,91)) +
            map(chr, range(97,123)), '')
        
        self.ident = string.join(map(chr, range(256)), '')

    def split(self, text, casesensitive=0):
        """Split text/plain string into a list of words"""

        # Speedup trick: attributes into local scope
        word_only = self.word_only
        ident = self.ident
        alpha = self.alpha
        nondigits = self.nondigits
        # 1.52: translate = string.translate

        # Let's adjust case if not case-sensitive
        if not casesensitive: text = text.upper()

        # Split the raw text
        allwords = text.split()

        # Finally, let's skip some words not worth indexing
        words = []
        for word in allwords:

            # Identify common patterns in non-word data (binary, UU/MIME, etc)
            num_nonalpha = len(word.translate(ident, alpha))
            numdigits    = len(word.translate(ident, nondigits))

            if numdigits > len(word)-2:         # almost all digits
                if numdigits > 5:               # too many digits is gibberish
                    continue                    # a moderate number is year/zipcode/etc
            elif num_nonalpha*3 > len(word):    # too much scattered nonalpha = gibberish
                continue

            
            word = word.translate(word_only)    # Let's strip funny byte values
            subwords = word.split()             # maybe embedded non-alphanumeric
            for subword in subwords:            # ...so we might have subwords
                if len(subword) <= 2: continue  # too short a subword
                words.append(subword)
        return words

 
