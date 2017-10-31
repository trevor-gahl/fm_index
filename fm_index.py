import os
from os.path import join, abspath, isfile
from os.path import isdir, exists, basename
import time
import sys
import index_build
import tarfile

class Burrows():
    delimiter = '#'
    def transform(self, s):

        assert self.delimiter not in s, "Input string cannot contain null character (%s)" % self.EOS

        # add end of text marker
        s += self.delimiter

        # table of suffixes
        rotations = [ s[i:] for i in range(len(s))]

        # sort the suffixes
        rotations.sort()

        # get the length of ordered suffixes
        k = len(rotations)

        r = [0]*k
        for i in xrange(k):
            l = len(rotations[i])
            if l == k:
                r[i] = self.delimiter
            else:
                r[i] = s[-l-1]
        r = ''.join(r)
        return r

def calc_first_occ(s):
    """ calculate the first occurance of a letter in sorted string s """
    # s - is the bwt transformed string
    A = {} # letter count
    for i, c in enumerate(s):
        if A.get(c):
            A[c] += 1
        else:
            A[c] = 1

    # sort the letters
    letters = sorted(A.keys())

    # first index of letter
    occ = {}

    index = 0
    for c in letters:
        occ[c] = index
        index += A[c]
    del index, A
    print("\nOCC Array")
    print(occ)
    print("\n")
    return occ



    '''
    test_string = 'accatgactttaggacctg'

    output = Burrows.transform(test_string)

    occ = calc_first_occ(output)

    print(output)
    print(occ)
    '''
def main():
    '''
    if not len(sys.argv) in [3]:
        print 'Usage: '
        print '  %s index search_string' % sys.argv[0]
    else:
        print("unable to load")
        if not isfile(sys.argv[1]):
            print "Index file doesn't exist"
    '''
    inp = open(sys.argv[1])

    # read input
    data = inp.read()

    # create index
    idx = index_build.index(data)
    c = idx.count(sys.argv[2])
    m = idx.search(sys.argv[2])

    print("Number of matches found: %s \n" % str(c))
    print("Index locations of matches: %s \n" % str(m))

if __name__ == '__main__':
    main()
