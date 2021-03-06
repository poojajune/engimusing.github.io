#!/usr/bin/python

"""
Original Code:
  Summary: XMODEM protocol implementation.
  Home-page: https://github.com/tehmaze/xmodem
  Author: Wijnand Modderman, Jeff Quast
  License: MIT

Stripped down and modified for this bootloader by Joe George 2015-2016
"""

import sys
from oPkt import asmPkt
from oPkt import verify
from tty import checkAck

packet_size   = 128
debug = 0

def debugPrint(s):
    if s.inWaiting() > 0:
        print s.read()
    return

def sendPackets(s, filename):

    stream = file(filename, 'rb')
    sequence = 1

    data = stream.read(packet_size)
    if not data:
        print "Error: Empty Compiled Script File"
        return False 

    errcnt = 0
    fullcrc = 0
    
    print
    
    while 1:
        pkt = asmPkt(data, sequence)
        fullcrc = verify(data, fullcrc)

        for ch in pkt:
            s.write(ch)
            if debug: sys.stdout.write(hex(ord(ch))+' ')
        if debug:
            print
            print

        if debug: debugPrint(s)

        if checkAck(s) == True:
            if debug:
                print "checkAck -> True"
                print " %r" % sequence
            else:
                sys.stdout.write('.')
                sys.stdout.flush()
            sequence = (sequence + 1) % 0x100  # increment sequence number
            if debug: print sequence
            data = stream.read(packet_size)
            if not data:
                print
                # print "CRC:" + hex(fullcrc) # don't print crc since it doesn't match anything that can be calculated by the bootloader
                return True
        else:
            print
            print "Packet %r Failed to Upload" % sequence
            errcnt += 1
            if errcnt > 0:
                sys.stdout.flush()
                return False

        continue

    print 
    return True

if __name__ == "__main__":
    import sys
    from sys import argv
    script, filename = argv
    debug = 1
    sendPackets(filename)


    fullcrc = calc_crc(data)
    print hex(fullcrc)


