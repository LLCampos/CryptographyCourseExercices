import urllib2
import sys
from binascii import unhexlify, hexlify


TARGET = 'http://crypto-class.appspot.com/po?er='


def split_every_n_chars(string, n):
    return [string[i: i + n] for i in range(0, len(string), n)]


class PaddingOracle(object):
    def query(self, q):
        target = TARGET + urllib2.quote(q)    # Create query URL
        req = urllib2.Request(target)         # Send HTTP request to server
        try:
            urllib2.urlopen(req)          # Wait for response
        except urllib2.HTTPError, e:
            print "We got: %d" % e.code       # Print response code
            if e.code == 404:
                return True  # good padding
            return False  # bad padding


cyphertext = 'f20bdba6ff29eed7b046d1df9fb7000058b1ffb4210a580f748b4ac714c001bd4a61044426fb515dad3f21f18aa577c0bdf302936266926ff37dbf7035d5eeb4'
blocks = split_every_n_chars(cyphertext, 32)

if __name__ == "__main__":
    po = PaddingOracle()
    po.query(sys.argv[1])       # Issue HTTP query with the given argument
