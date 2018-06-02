'''
This module can be used to read a GL file
The methods here can be used to read the various tags/flags/data from the GL file.
'''

import numpy as np
import Constants as c


def ReadFlags(fdata):
    flags = ReadTag(fdata)

    fill = (flags[0] & c.SFILL[0]) != 0
    out = (flags[0] & c.SOUTLINE[0]) != 0
    trans = (flags[0] & c.STRANSPARENT[0]) != 0
    multi = (flags[0] & c.SMULTICOLOR[0]) != 0

    return fill, out, trans, multi


def ReadText(fdata,bytesMirrored,text ='T'):
    pass


def ReadTag(fdata):
    tag = fdata.data[fdata.pos].tobytes()
    fdata.pos = fdata.pos + 1

    return tag
 
 
def ReadFloats(fdata, dataType, n, bytesMirrored):
    if dataType == np.float32 and bytesMirrored:
        fls = np.frombuffer(fdata.data[fdata.pos : fdata.pos+(n*4)].tobytes(), dataType, n).byteswap()
        fdata.pos = fdata.pos + 4*n
    elif dataType == np.float64 and bytesMirrored:
        fls = np.frombuffer(fdata.data[fdata.pos : fdata.pos+(n*8)].tobytes(), dataType, n).byteswap()
        fdata.pos = fdata.pos + 8*n
    elif dataType == np.float32 and not bytesMirrored:
        fls = np.frombuffer(fdata.data[fdata.pos : fdata.pos+(n*4)].tobytes(), dataType, n)
        fdata.pos = fdata.pos + 4*n
    elif dataType == np.float64 and not bytesMirrored:
        fls = np.frombuffer(fdata.data[fdata.pos : fdata.pos+(n*8)].tobytes(), dataType, n)
        fdata.pos = fdata.pos + 8*n

    return fls
    

def ReadUint(fdata, dataType, n, bytesMirrored):
    if dataType == np.uint32 and bytesMirrored:
        fls = np.frombuffer(fdata.data[fdata.pos : fdata.pos+(n*4)].tobytes(), dataType, n).byteswap()
        fdata.pos = fdata.pos + 4*n
    elif dataType == np.uint32 and not bytesMirrored:
        fls = np.frombuffer(fdata.data[fdata.pos : fdata.pos+(n*4)].tobytes(), dataType, n)
        fdata.pos = fdata.pos + 4*n

    return fls[0]


def ReadColorAndTrans(fdata, fill, out, multi, trans, n, bytesMirrored):    
    color = []
    tr = []
    
    if multi:
        x = n
    else:
        x = 1			 

    for j in range (0, x):
        if fill or out:
            color.append(np.multiply(ReadFloats(fdata, np.float32, 3, bytesMirrored), 255.0))
        else:
            color.append(np.array([0.5, 0.5, 0.5]))
        if trans:
            tr.append(ReadFloats(fdata, np.float32, 1, bytesMirrored))
        else:
            tr.append(0.0)
    return color, tr
