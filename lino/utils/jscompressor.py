# {{{ http://code.activestate.com/recipes/496882/ (r8)
'''
http://code.activestate.com/recipes/496882/
Author: Michael Palmer 13 Jul 2006
a regex-based JavaScript code compression kludge
'''
from __future__ import division
from __future__ import print_function
from builtins import range
from builtins import object
from past.utils import old_div
import re


class JSCompressor(object):

    def __init__(self, compressionLevel=2, measureCompression=False):
        '''
        compressionLevel:
        0 - no compression, script returned unchanged. For debugging only -
            try if you suspect that compression compromises your script
        1 - Strip comments and empty lines, don't change line breaks and indentation (code remains readable)
        2 - Additionally strip insignificant whitespace (code will become quite unreadable)

        measureCompression: append a comment stating the extent of compression
        '''
        self.compressionLevel = compressionLevel
        self.measureCompression = measureCompression

    # a bunch of regexes used in compression
    # first, exempt string and regex literals from compression by transient
    # substitution

    findLiterals = re.compile(r'''
        (\'.*?(?<=[^\\])\')             |       # single-quoted strings
        (\".*?(?<=[^\\])\")             |       # double-quoted strings
        ((?<![\*\/])\/(?![\/\*]).*?(?<![\\])\/) # JS regexes, trying hard not to be tripped up by comments
        ''', re.VERBOSE)

    # literals are temporarily replaced by numbered placeholders

    literalMarker = '@_@%d@_@'                  # temporary replacement
    # put the string literals back in
    backSubst = re.compile('@_@(\d+)@_@')

    # /* ... */ comments on single line
    mlc1 = re.compile(r'(\/\*.*?\*\/)')
    mlc = re.compile(r'(\/\*.*?\*\/)', re.DOTALL)  # real multiline comments
    slc = re.compile('\/\/.*')                  # remove single line comments

    # collapse successive non-leading white space characters into one
    collapseWs = re.compile('(?<=\S)[ \t]+')

    squeeze = re.compile('''
        \s+(?=[\}\]\)\:\&\|\=\;\,\.\+])   |     # remove whitespace preceding control characters
        (?<=[\{\[\(\:\&\|\=\;\,\.\+])\s+  |     # ... or following such
        [ \t]+(?=\W)                      |     # remove spaces or tabs preceding non-word characters
        (?<=\W)[ \t]+                           # ... or following such
        '''
                         , re.VERBOSE | re.DOTALL)

    def compress(self, script):
        '''
        perform compression and return compressed script
        '''
        if self.compressionLevel == 0:
            return script

        lengthBefore = len(script)

        # first, substitute string literals by placeholders to prevent the
        # regexes messing with them
        literals = []

        def insertMarker(mo):
            l = mo.group()
            literals.append(l)
            return self.literalMarker % (len(literals) - 1)

        script = self.findLiterals.sub(insertMarker, script)

        # now, to the literal-stripped carcass, apply some kludgy regexes for
        # deflation...
        script = self.slc.sub('', script)       # strip single line comments
        # replace /* .. */ comments on single lines by space
        script = self.mlc1.sub(' ', script)
        # replace real multiline comments by newlines
        script = self.mlc.sub('\n', script)

        # remove empty lines and trailing whitespace
        script = '\n'.join([l.rstrip()
                           for l in script.splitlines() if l.strip()])

        # squeeze out any dispensible whitespace
        if self.compressionLevel == 2:
            script = self.squeeze.sub('', script)
        # only collapse multiple whitespace characters
        elif self.compressionLevel == 1:
            script = self.collapseWs.sub(' ', script)

        # now back-substitute the string and regex literals
        def backsub(mo):
            return literals[int(mo.group(1))]

        script = self.backSubst.sub(backsub, script)

        if self.measureCompression:
            lengthAfter = float(len(script))
            squeezedBy = int(100 * (1 - old_div(lengthAfter, lengthBefore)))
            script += '\n// squeezed out %s%%\n' % squeezedBy

        return script


if __name__ == '__main__':
    script = '''


    /* this is a totally useless multiline comment, containing a silly "quoted string",
       surrounded by several superfluous line breaks
     */


    // and this is an equally important single line comment

    sth = "this string contains 'quotes', a /regex/ and a // comment yet it will survive compression";

    function wurst(){           // this is a great function
        var hans = 33;
    }

    sthelse = 'and another useless string';

    function hans(){            // another function
        var   bill   =   66;    // successive spaces will be collapsed into one;
        var bob = 77            // this line break will be preserved b/c of lacking semicolon
        var george = 88;
    }
    '''

    for x in range(1, 3):
        print('\ncompression level', x, ':\n--------------')
        c = JSCompressor(compressionLevel=x, measureCompression=True)
        cpr = c.compress(script)
        print(cpr)
        print('length', len(cpr))
# end of http://code.activestate.com/recipes/496882/ }}}
