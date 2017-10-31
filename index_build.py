import pickle
import fm_index

bw  = fm_index.Burrows()


def save(filename, idx):
    f = open(filename, 'w')
    pickle.dump(idx,f)

def load(filename):
    #f = open(filename)
    idx = pickle.load(open(filename))
    return idx

def index(data):
    return fmIndex(data)

class fmIndex(object):
    def __init__(self, data):
        self.data = bw.transform(data)
        self.offset = {}
        self._build(data)

    def _build(self, data):
        """ build the index """
        self.occ = fm_index.calc_first_occ(self.data)

    def _occ(self, qc):
        """ get the first occurance of letter qc in left-column"""
        c = self.occ.get(qc)
        if c == None:
            return 0
        return c

    def _count(self, idx, qc):
        """ count the occurances of letter qc (rank of qc) upto position idx """
        if not qc in self.occ.keys(): return 0
        c = 0
        for i in xrange(idx):
            if self.data[i] == qc:
                c += 1
        return c

    def _lf(self, idx, qc):
        """ get the nearset lf mapping for letter qc at position idx """
        o = self._occ(qc)
        c = self._count(idx, qc)
        return o + c

    def _walk(self, idx):
        """ find the offset in position idx of transformed string
            from the beginning """

        # walk to the beginning using lf mapping
        # this is same as inverse of burrow wheeler transformation
        # from arbitrary location
        r = 0
        i = idx
        while self.data[i] != bw.delimiter:
            if self.offset.get(i):
                # we have cached the location and can use it
                r += self.offset[i]
                break
            r += 1
            i = self._lf(i, self.data[i])

        # save the offset of some idx for faster searches
        if not self.offset.get(idx):
            self.offset[i] = r
        return r

    def bounds(self, q):
        """ find the first and last suffix positions for query q """
        top = 0
        bot = len(self.data)
        for i, qc in enumerate(q[::-1]):
            top = self._lf(top, qc)
            bot = self._lf(bot, qc)
            if top == bot: return (-1,-1)
        return (top,bot)

    def search(self, q):
        """ search the positions of query q """

        # find the suffixes for the query
        top, bot = self.bounds(q)
        matches = []
        # find the location of the suffixes
        # by walking the reverse text from that position
        # with lf mapping
        for i in range(top, bot):
            pos = self._walk(i)
            matches.append(pos)
        return sorted(matches)

    def count(self, q):
        """ count occurances of q in the index """
        top, bot = self.bounds(q)
        return bot - top

    def getOriginal(self):
        return bwi.inverse(self.data)

    def RLE(self):
        output = []
        last = ''
        k = 0
        for i in range(len(self.data)):
            ch = self.data[i]
            if ch == last:
                k += 1
            else:
                if k > 0:
                    output.append((last, k))
                last = ch
                k = 1
        output.append((last, k))
        return output
