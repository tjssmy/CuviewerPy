'''
This module can be used to write a GL file that can then be read by CuViewerPy.py
The methods here can be used to write teh various tags for the GL file.
'''

import numpy as np
import Constants as c


def WriteGLTag(fid, tag):
    fid.write(tag)


def WriteGLCheck(fid):
    ch = np.int32(c.DATA_ORDER_CHECK)
    np.array([ch]).tofile(fid)


def WriteGLString(fid,str):
    strBA = bytearray(str,'utf8')
    fid.write(strBA)


def WriteInitGLFile(file):
    fid = open(file,'wb')

    WriteGLCheck(fid)
    WriteGLTag(fid, c.BEGIN_DATA)
    WriteGLTag(fid, c.BEGIN_VERSION)
    WriteGLString(fid, c.VERSION_STRING)
    WriteGLTag(fid, c.END_VERSION)

    return fid


def WriteSceneBegin(fid,label):
    WriteGLTag(fid, c.BEGIN_SCENE)
    if label != '':
        WriteGLTag(fid, c.BEGIN_SCENE_LABEL)
        WriteGLString(fid,label)
        WriteGLTag(fid, c.END_SCENE_LABEL)


def WriteSceneEnd(fid):
    WriteGLTag(fid, c.END_SCENE)


def WriteCloseGLFile(fid):
    WriteGLTag(fid, c.BEGIN_VIEW);
    WriteGLTag(fid, c.VPRESET_VIEW);
    WriteGLTag(fid, bytes([0]));
    WriteGLTag(fid, c.END_VIEW);
    WriteGLTag(fid, c.END_DATA_STAY);
    fid.close()


def WriteGLFloats(fid, vec):
    for f in vec:
        v = np.float32(f)
        np.array([v]).tofile(fid)


def WriteGLColorAndTrans(fid,color,trans):
    WriteGLFloats(fid, color)
    if trans != 0.0:
        WriteGLFloats(fid, trans)


def Write_GL_points_position(fid, p1):
    WriteGLFloats(fid, p1)


def Write_GL_points_color(fid, color):
    WriteGLFloats(fid, color)


def Write_GL_point(fid, p1, color, trans):
    WriteGLTag(fid, c.SPOINT)

    flags = c.SFILL
    WriteGLTag(fid, flags)

    WriteGLFloats(fid, p1)
    WriteGLFloats(fid, color)

    # if flags[0] & STRANSPARENT[0]:
    #     WriteGLFloats(fid, trans)


def write_GL_lines_position(fid, p1, p2):
    WriteGLFloats(fid, p1)
    WriteGLFloats(fid, p2)


def write_GL_lines_color(fid, c1, c2, flags):
    WriteGLFloats(fid, c1)

    if flags[0] & c.SMULTICOLOR[0]:
        WriteGLFloats(fid, c2)

    if flags[0] & c.STRANSPARENT[0]:
        WriteGLFloats(fid, flags[0])
        WriteGLFloats(fid, flags[0])


def Write_GL_line(fid, p1, p2, color, color2, trans, multi):
    WriteGLTag(fid,c.SLINE)

    flags = c.SOUTLINE
    if trans != 0.0:
        flags = bytes([flags[0] | c.STRANSPARENT[0]])
    if multi:
        flags = bytes([flags[0] | c.SMULTICOLOR[0]])

    WriteGLTag(fid, flags)

    WriteGLFloats(fid, p1)
    WriteGLFloats(fid, p2)

    WriteGLFloats(fid, color)

    if flags[0] & c.SMULTICOLOR[0]:
        WriteGLFloats(fid, color2)

    if flags[0] & c.STRANSPARENT[0]:
        WriteGLFloats(fid, trans)


def write_GL_triangles_position(fid, p1, p2, p3):
    WriteGLFloats(fid, p1)
    WriteGLFloats(fid, p2)
    WriteGLFloats(fid, p3)


def write_GL_triangles_color(fid, c1, c2, c3, flags):
    WriteGLFloats(fid, c1)

    if flags[0] & c.SMULTICOLOR[0]:
        WriteGLFloats(fid, c2)
        WriteGLFloats(fid, c3)
        
    if flags[0] & c.STRANSPARENT[0]:
        WriteGLFloats(fid, flags[0])
        WriteGLFloats(fid, flags[0])
        WriteGLFloats(fid, flags[0])


def Write_GL_tri(fid, p1, p2, p3, color, color2, color3, trans, multi, out):
    WriteGLTag(fid,c.STRIA)

    flags = c.SFILL
    if trans != 0.0:
        flags =  bytes([flags[0] | c.STRANSPARENT[0]])
    if multi:
        flags =  bytes([flags[0] | c.SMULTICOLOR[0]])
    if out:
        flags =  bytes([flags[0] | c.SOUTLINE[0]])

    WriteGLTag(fid, flags)

    WriteGLFloats(fid, p1)
    WriteGLFloats(fid, p2)
    WriteGLFloats(fid, p3)

    WriteGLColorAndTrans(fid, color, trans)

    if flags[0] & c.SMULTICOLOR[0]:
        WriteGLColorAndTrans(fid, color2, trans)
        WriteGLColorAndTrans(fid, color3, trans)


def write_GL_quad_position(fid, p1, p2, p3, p4):
    WriteGLFloats(fid, p1)
    WriteGLFloats(fid, p2)
    WriteGLFloats(fid, p3)
    WriteGLFloats(fid, p4)


def write_GL_quad_color(fid, c1, c2, c3, c4, flags):
    WriteGLFloats(fid, c1)

    if flags[0] & c.SMULTICOLOR[0]:
        WriteGLFloats(fid, c2)
        WriteGLFloats(fid, c3)
        WriteGLFloats(fid, c4)
        
    if flags[0] & c.STRANSPARENT[0]:
        WriteGLFloats(fid, flags[0])
        WriteGLFloats(fid, flags[0])
        WriteGLFloats(fid, flags[0])
        WriteGLFloats(fid, flags[0])


def Write_GL_quad(fid, p1, p2, p3, p4,  color, color2, color3, color4, trans, multi, out):
    WriteGLTag(fid, c.SQUADRI)

    flags = c.SFILL
    if trans != 0.0:
        flags =  bytes([flags[0] | c.STRANSPARENT[0]])
    if multi:
        flags =  bytes([flags[0] | c.SMULTICOLOR[0]])
    if out:
        flags =  bytes([flags[0] | c.SOUTLINE[0]])

    WriteGLTag(fid, flags)

    WriteGLFloats(fid, p1)
    WriteGLFloats(fid, p2)
    WriteGLFloats(fid, p3)
    WriteGLFloats(fid, p4)

    WriteGLColorAndTrans(fid, color, trans)

    if flags[0] & c.SMULTICOLOR[0]:
        WriteGLColorAndTrans(fid, color2, trans)
        WriteGLColorAndTrans(fid, color3, trans)
        WriteGLColorAndTrans(fid, color4, trans)


def Write_GL_vector(fid, p0, vec):
    WriteGLTag(fid, c.SVECTOR)
    WriteGLFloats(fid, p0)
    WriteGLFloats(fid, vec)


def Write_GL_sphere(fid, p1, r1, color, trans):
    WriteGLTag(fid, c.SSPHERE)

    flags = c.SFILL
    WriteGLTag(fid, flags)
    
    WriteGLFloats(fid, p1)
    WriteGLFloats(fid, r1)
    WriteGLFloats(fid, color)


def Write_GL_spheroid(fid, p1, r1, color, trans):
    WriteGLTag(fid, c.SSPHOID)

    flags = c.SFILL
    WriteGLTag(fid, flags)
    
    WriteGLFloats(fid, p1)
    WriteGLFloats(fid, r1)
    WriteGLFloats(fid, color)
