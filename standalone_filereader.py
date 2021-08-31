import struct
import os
import shutil
import time
import glob
from datetime import datetime


def filereader(filepath):

    counter = 0
    while counter < 10:
        bytelist = []
        try:
            with open(filepath, "rb") as datafile:
                bytelist = datafile.read()
            datafile.close()
        except PermissionError:
            print('Permission Error')
        except FileNotFoundError:
            print('File not Found')
        if len(bytelist) > 500:
            counter = 10
        else:
            time.sleep(0.01)
            counter += 1
    #print("File %s  length %ibytes" % (filepath, len(bytelist)))


    filetype = str(bytelist[205:216], 'cp1250')
    #print('File Type =%s' % filetype)
    c0 = str(bytelist[317:326], 'cp1250')
    c1 = str(bytelist[350:359], 'cp1250')
    c2 = str(bytelist[383:392], 'cp1250')
    c3 = str(bytelist[416:425], 'cp1250')
    c4 = str(bytelist[449:458], 'cp1250')

    #print('channels', c0, c1, c2, c3, c4)

    sampletime = datetime(1900 + bytelist[13], bytelist[12], bytelist[11],
                          bytelist[10], bytelist[9], bytelist[8])
    print('Sample time = %s' % sampletime)
    if (time.time() - datetime.timestamp(sampletime)) > 5:
        filepath = 'Off Line'


    if len(bytelist) > 500:
        pos = 488
        e0 = struct.unpack('f', bytearray(bytelist[pos + 0:pos + 4]))[0]
        e1 = struct.unpack('f', bytearray(bytelist[pos + 4:pos + 8]))[0]
        e2 = struct.unpack('f', bytearray(bytelist[pos + 8:pos + 12]))[0]
        e3 = struct.unpack('f', bytearray(bytelist[pos + 12:pos + 16]))[0]
        e4 = struct.unpack('f', bytearray(bytelist[pos + 16:pos + 20]))[0]

        #print('data', e0, e1, e2, e3, e4)
        return os.path.basename(filepath), sampletime, c0, c1, c2, c3, c4, e0, e1, e2, e3, e4
    else:
        return 'Off line', datetime.now(), '', '', '', '', '', 0, 0, 0, 0, 0


def getfilelist(filepath):
    filelist = glob.glob1(filepath, "pymscyc0*.mdc")
    return filelist


def createfiles(filepath):
    sourcefile = filepath+'pymscyc.mdc'
    for i in range(1000):
        destfile = '%spymscyc%04d-%s.mdc' % (filepath, i, datetime.strftime( datetime.now(),"%H-%M-%S-%f"))
        print(destfile)
        time.sleep(0.1)
        shutil.copy(sourcefile, destfile)


datapath = 'C:\\QS422\\DAT\\'
# x = filereader("C:\\QS422\\DAT\\pymscyc.mdc")
# createfiles(datapath)
x = getfilelist(datapath)
for file in x:
    filereader(datapath + file)
