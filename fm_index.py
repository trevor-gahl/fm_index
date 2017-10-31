import os
from os.path import join, abspath, isfile, isdir, exists, basename
import time
import sys
import index_build
import tarfile

class Burrows():
    def transform(self, s):
        delimiter = '#'
        assert delimiter not in s, "Input string cannot contain null character (%s)" % self.EOS

        # add end of text marker
        s += delimiter

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
                r[i] = delimiter
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

    return occ



    '''
    test_string = 'accatgactttaggacctg'

    output = Burrows.transform(test_string)

    occ = calc_first_occ(output)

    print(output)
    print(occ)
    '''
def main():
        print("test")
        if not len(sys.argv) in [4]:
            print 'Usage: '
            print '  %s index search_string' % sys.argv[0]
        else:
            print("unable to load")
            if not isfile(sys.argv[1]):
                print "Index file doesn't exist"

            idx = index_build.load(sys.argv[1])

            print("file loaded")
            c = idx.count(sys.argv[2])


            m = idx.search(sys.argv[2])

            print(str(c))

            print(str(m))
            fmindex.save(sys.argv[3], idx)
if __name__ == '__main__':
    main()
