# These are the tags used by the Carleton University 3D Viewer 2.0. */

# For bit/byte order
DATA_ORDER_CHECK = 1351861536
DATA_NORMAL_ORDER = 1351861536
DATA_MIRROR_ORDER = 549819216

# For version checking
VERSION_STRING = "Carleton University 3D Viewer 2.0 - python"
SHORT_VERSION_STRING = "Carleton University 3D Viewer "
BEGIN_SCENE_LABEL = bytes.fromhex('D1')
END_SCENE_LABEL = bytes.fromhex('D2')

# Tags for the sections
BEGIN_DATA = bytes.fromhex('C0')
BEGIN_VERSION = bytes.fromhex('C4')
BEGIN_IMG_SET = bytes.fromhex('C5')
BEGIN_MOV_SET = bytes.fromhex('C6')
BEGIN_SCENE = bytes.fromhex('C8')
USER_INTERACT = bytes.fromhex('C9')
BEGIN_VIEW = bytes.fromhex('CC')
RESET_VIEW = bytes.fromhex('CD')
GRAB_IMAGE = bytes.fromhex('CE')
GRAB_FRAME = bytes.fromhex('CF')

END_DATA_STAY = bytes.fromhex('A0')
END_DATA_EXIT = bytes.fromhex('A1')
END_VERSION = bytes.fromhex('A4')
END_IMG_SET = bytes.fromhex('A5')
END_MOV_SET = bytes.fromhex('A6')
END_SCENE = bytes.fromhex('A8')
END_VIEW = bytes.fromhex('AC')

# Tags while in the scene section
SPOINT = bytes.fromhex('00')
MULTIPLE_SPOINT = bytes.fromhex('08')
SLINE = bytes.fromhex('01')
MULTIPLE_SLINE = bytes.fromhex('09')
STRIA = bytes.fromhex('02')
MULTIPLE_STRIA = bytes.fromhex('10')
SQUADRI = bytes.fromhex('03')
MULTIPLE_SQUADRI = bytes.fromhex('11')
SSPHERE = bytes.fromhex('04')
SSPHOID = bytes.fromhex('05')
STEXT = bytes.fromhex('06')
SVECTOR = bytes.fromhex('07')

# Shape properties in the scene section
SFILL = bytes.fromhex('01')
SOUTLINE = bytes.fromhex('02')
SMULTICOLOR = bytes.fromhex('04')
STRANSPARENT = bytes.fromhex('08')
SNORMALS = bytes.fromhex('10')
SMATERIAL = bytes.fromhex('20')
SUNDEFINED = bytes.fromhex('40')
SPROCESSED = bytes.fromhex('80')

# Tags while in the view section
VCAM_TRANS = bytes.fromhex('00')
VCAM_ROTATE = bytes.fromhex('01')
VCAM_ORBIT = bytes.fromhex('02')
VOUTLINE_CLR = bytes.fromhex('03')
VPRESET_VIEW = bytes.fromhex('04')

VVIEW_MODE = bytes.fromhex('10')
VFOV = bytes.fromhex('11')
VCLIP_PLANE = bytes.fromhex('12')
VLINE_WIDTH = bytes.fromhex('13')
VSHADING = bytes.fromhex('14')
VBIN_PAL_SEL = bytes.fromhex('15')
VBIN_PAL_MAP = bytes.fromhex('16')

VLIGHTING = bytes.fromhex('20')
VLIGHT = bytes.fromhex('21')
VAMB_LIGHT = bytes.fromhex('22')
VDIFF_LIGHT = bytes.fromhex('23')
VBG_LIGHT = bytes.fromhex('24')
VGAMMA = bytes.fromhex('25')

VWIREFRAME = bytes.fromhex('30')
VOUTLINES = bytes.fromhex('31')
VTWO_SIDED = bytes.fromhex('32')
VTRANSPARENT = bytes.fromhex('33')
VBIN_PAL = bytes.fromhex('34')
VANTIALIAS = bytes.fromhex('35')

VRELATIVE = bytes.fromhex('00')
VABSOLUTE = bytes.fromhex('01')

VORHTO = bytes.fromhex('00')
VPERSPECTIVE = bytes.fromhex('01')

VFLAT = bytes.fromhex('00')
VSMOOTH = bytes.fromhex('01')

VOFF = bytes.fromhex('00')
VON = bytes.fromhex('01')