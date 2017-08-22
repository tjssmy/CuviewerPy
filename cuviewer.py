import numpy as np
import vtk
import math
import sys
# import struct

def tic():
    #Homemade version of matlab tic and toc functions
    import time
    global startTime_for_tictoc
    startTime_for_tictoc = time.time()

def toc():
    import time
    if 'startTime_for_tictoc' in globals():
        print("Elapsed time is " + str(time.time() - startTime_for_tictoc) + " seconds.")
    else:
        print("Toc: start time not set")

# These are the tags used by the Carleton University 3D Viewer 2.0. */ 

# for bit/byte order
DATA_ORDER_CHECK = 1351861536
DATA_NORMAL_ORDER = 1351861536
DATA_MIRROR_ORDER = 549819216

# for version checking
VERSION_STRING = "Carleton University 3D Viewer 2.0 - python"
SHORT_VERSION_STRING = "Carleton University 3D Viewer "
BEGIN_SCENE_LABEL = bytes.fromhex('D1')
END_SCENE_LABEL = bytes.fromhex('D2')

# tags for the sections
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

# tags while in the scene section
SPOINT = bytes.fromhex('00')
SLINE = bytes.fromhex('01')
STRIA = bytes.fromhex('02')
SQUADRI = bytes.fromhex('03')
SSPHERE = bytes.fromhex('04')
SSPHOID = bytes.fromhex('05')
STEXT = bytes.fromhex('06')
SVECTOR = bytes.fromhex('07')

# shape properties in the scene section
SFILL = bytes.fromhex('01')
SOUTLINE = bytes.fromhex('02')
SMULTICOLOR = bytes.fromhex('04')
STRANSPARENT = bytes.fromhex('08')
SNORMALS = bytes.fromhex('10')
SMATERIAL = bytes.fromhex('20')
SUNDEFINED = bytes.fromhex('40')
SPROCESSED = bytes.fromhex('80')

# tags while in the view section
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


def ReadFlags(fid,fdata):
    
    flags = ReadTag(fid, fdata)

    fill = (flags[0] & SFILL[0]) != 0
    out = (flags[0] & SOUTLINE[0]) != 0
    trans = (flags[0] & STRANSPARENT[0]) != 0
    multi = (flags[0] & SMULTICOLOR[0]) != 0

    # print('flags: {}'.format([fill, out, trans, multi]))

    return fill, out, trans, multi


def ReadText(fid):
    pass


def ReadTag(fid, fdata):

    tag = bytes(fdata.data[fdata.pos:fdata.pos + 1])
    fdata.pos = fdata.pos + 1

    # tag = fid.read(1)
    # tag = bytes() + tag

    return tag


def ReadFloats(fid, fdata, t, n, bytesMirrored):

    fls = np.frombuffer(fdata.data, t, n, fdata.pos)

    if t == np.float32:
        fdata.pos = fdata.pos + 4*n
    elif t == np.float64:
        fdata.pos = fdata.pos + 8*n

    if bytesMirrored:
        fls = fls.byteswap()

    # fls = np.fromfile(fid, t, n)
    # if bytesMirrored:
    #     fls = fls.byteswap()

    return fls


def ReadColorAndTrans(fid, fdata,fill, out, multi, trans, n, bytesMirrored):
    
    color = [np.array([0.5, 0.5, 0.5])]
    tr = [0.0]

    if fill or out:
        color[0] = np.multiply(ReadFloats(fid, fdata, np.float32, 3, bytesMirrored), 255.0)
        if trans:
            tr[0] = ReadFloats(fid, fdata, np.float32, 1, bytesMirrored)

        if multi:
            for i in range(1, n):
                color.append(np.multiply(ReadFloats(fid, fdata, np.float32, 3, bytesMirrored), 255.0))
                if trans:
                    tr.append(ReadFloats(fid, fdata, np.float32, 1, bytesMirrored))

    return color, tr


class Poly(object):

    def __init__(self, poly, color, tr, fill, out, multi,type):
        self.poly = poly
        self.pid = []
        self.type = ''
        self.color = color
        self.tr = tr
        self.fill = fill
        self.out = out
        self.multi = multi
        self.type = type

    def addVtkData(self, vpoly, c):

        for p in self.poly:
            vpoly.points.InsertNextPoint(p)
            self.pid.append(c)
            if not self.multi:
                vpoly.colors.InsertNextTypedTuple(self.color[0])

        if self.multi:
            for l in self.color:
                vpoly.colors.InsertNextTypedTuple(l)

        if self.type == 'P':
            pass
        elif self.type == 'L':
            geo = vtk.vtkLine()
            geo.InsertNextPoint(self.pid[0])
            geo.InsertNextPoint(self.pid[1])
        elif self.type == 'T':
            geo = vtk.vtkTriangle()
            geo.InsertNextPoint(self.pid[0])
            geo.InsertNextPoint(self.pid[1])
            geo.InsertNextPoint(self.pid[2])
        elif self.type == 'Q':
            geo = vtk.vtkQuad()
            geo.InsertNextPoint(self.pid[0])
            geo.InsertNextPoint(self.pid[1])
            geo.InsertNextPoint(self.pid[2])
            geo.InsertNextPoint(self.pid[3])

        self.geos.InsertNextCell(geo)

        return c


class Sphere(object):

    def __init__(self, pos, rad, color, tr, fill, out):
        self.pos = pos
        self.rad = rad
        self.color = color
        self.tr = tr
        self.fill = fill
        self.out = out


def ReadSphere(fid, fdata, bytesMirrored):

     fill, out, trans, multi = ReadFlags(fid, fdata)
     multi = False

     pos = ReadFloats(fid, fdata, np.float32, 3, bytesMirrored)
     rad = ReadFloats(fid, fdata, np.float32, 1, bytesMirrored)

     color, tr = ReadColorAndTrans(fid, fdata, fill,out,multi,trans,0, bytesMirrored)

     return Sphere(pos, rad, color, tr, fill, out)


class Spheroid(object):

    def __init__(self, pos, rad, axis, rot, color, tr, fill, out):
        self.pos = pos
        self.rad = rad
        self.axis = axis
        self.rot = rot
        self.color = color
        self.tr = tr
        self.fill = fill
        self.out = out


def ReadSpheriod(fid, fdata, bytesMirrored):

    fill, out, trans, multi = ReadFlags(fid, fdata)
    multi = False

    pos = ReadFloats(fid, fdata, np.float32, 3, bytesMirrored)
    rad = ReadFloats(fid, fdata, np.float32, 1, bytesMirrored)
    axis = ReadFloats(fid, fdata, np.float32, 3, bytesMirrored)
    rot = ReadFloats(fid, fdata, np.float32, 1, bytesMirrored)

    color, tr = ReadColorAndTrans(fid, fdata, fill, out,multi,trans,0, bytesMirrored)

    return Spheroid(pos, rad, axis, rot, color, tr, fill, out)


class Text(object):

    def __init__(self, pos, rad, color, tr):
        self.pos = pos
        self.rad = rad
        self.color = color
        self.tr = tr


def MakeBands(dR, numberOfBands, nearestInteger):
    """
    Divide a range into bands
    :param: dR - [min, max] the range that is to be covered by the bands.
    :param: numberOfBands - the number of bands, a positive integer.
    :param: nearestInteger - if True then [floor(min), ceil(max)] is used.
    :return: A List consisting of [min, midpoint, max] for each band.
    """
    bands = list()
    if (dR[1] < dR[0]) or (numberOfBands <= 0):
        return bands
    x = list(dR)
    if nearestInteger:
        x[0] = math.floor(x[0])
        x[1] = math.ceil(x[1])
    dx = (x[1] - x[0]) / float(numberOfBands)
    b = [x[0], x[0] + dx / 2.0, x[0] + dx]
    i = 0
    while i < numberOfBands:
        bands.append(b)
        b = [b[0] + dx, b[1] + dx, b[2] + dx]
        i += 1
    return bands


def MakeLUT():
    """
    Make a lookup table using vtkColorSeries.
    :return: An indexed lookup table.
    """
    # Make the lookup table.
    colorSeries = vtk.vtkColorSeries()
    # Select a color scheme.
    # colorSeriesEnum = colorSeries.BREWER_DIVERGING_BROWN_BLUE_GREEN_9
    #colorSeriesEnum = colorSeries.BREWER_DIVERGING_SPECTRAL_10
    # colorSeriesEnum = colorSeries.BREWER_DIVERGING_SPECTRAL_3
    # colorSeriesEnum = colorSeries.BREWER_DIVERGING_PURPLE_ORANGE_9
    # colorSeriesEnum = colorSeries.BREWER_SEQUENTIAL_BLUE_PURPLE_9
    # colorSeriesEnum = colorSeries.BREWER_SEQUENTIAL_BLUE_GREEN_9
    # colorSeriesEnum = colorSeries.BREWER_QUALITATIVE_SET3
    colorSeriesEnum = colorSeries.BREWER_SEQUENTIAL_BLUE_PURPLE_9
    colorSeries.SetColorScheme(colorSeriesEnum)
    lut = vtk.vtkLookupTable()
    colorSeries.BuildLookupTable(lut)
    lut.SetNanColor(0, 0, 0, 1)
    return lut


class Scene(object):

    def __init__(self):
        self.label = 'N/A'

        self.points = vtk.vtkPoints()
        self.vecPoints = vtk.vtkPoints()

        self.temps = vtk.vtkFloatArray()
        self.temps.SetNumberOfComponents(1)
        self.temps.SetName("Temps")

        self.colors = vtk.vtkUnsignedCharArray()
        self.colors.SetNumberOfComponents(3)
        self.colors.SetName("Colors")

        self.lines = vtk.vtkCellArray()
        self.polys = vtk.vtkCellArray()

        self.vectors = vtk.vtkDoubleArray()
        self.vectors.SetNumberOfComponents(3)
        self.vectors.SetName('vectors')

        self.vectorMags = vtk.vtkDoubleArray()
        self.vectorMags.SetNumberOfComponents(1)
        self.vectorMags.SetName('vecMag')

        self.spheres = []
        self.spheroids = []

        self.texts = []

        self.vtkSurfPolyData = vtk.vtkPolyData()
        self.vtkContPolyData = vtk.vtkPolyData()
        self.vtkEdgePolyData = vtk.vtkPolyData()
        self.vtkVectPolyData = vtk.vtkPolyData()

        self.visible = True

    def AddVtkVector(self, fid, fdata, bytesMirrored):
        pos = ReadFloats(fid, fdata, np.float32, 3, bytesMirrored)
        vec = ReadFloats(fid, fdata, np.float32, 3, bytesMirrored)
        vecMag = [math.sqrt(vec[0]*vec[0] + vec[1]*vec[1] + vec[2]*vec[2])]

        self.vecPoints.InsertNextPoint(pos)
        self.vectors.InsertNextTuple(vec)
        self.vectorMags.InsertNextTuple(vecMag)

    def GetVtkPoly(self, fid, fdata, n, bytesMirrored, type):

        geo = []
        pid = []

        fill, out, trans, multi = ReadFlags(fid, fdata)

        for i in range(0, n):
            geo.append(ReadFloats(fid, fdata, np.float32, 3, bytesMirrored))

        color, tr = ReadColorAndTrans(fid, fdata, fill, out, multi, trans, n, bytesMirrored)

        for i in range(0, n):
            pid.append(self.points.InsertNextPoint(geo[i]))
            if multi:
                t = [color[i][0]]
                self.temps.InsertNextTypedTuple(t)
                col = tuple(color[i])
                self.colors.InsertNextTypedTuple(col)

            else:
                t = [color[0][0]]
                self.temps.InsertNextTypedTuple(t)
                col = tuple(color[0])
                self.colors.InsertNextTypedTuple(col)

        if type == 'L':
            line = vtk.vtkLine()
            line.GetPointIds().SetId(0, pid[0])
            line.GetPointIds().SetId(1, pid[1])
            return line

        elif type == 'T':
            tri = vtk.vtkTriangle()
            tri.GetPointIds().SetId(0, pid[0])
            tri.GetPointIds().SetId(1, pid[1])
            tri.GetPointIds().SetId(2, pid[2])
            return tri

        elif type == 'Q':
            quad = vtk.vtkQuad()
            quad.GetPointIds().SetId(0, pid[0])
            quad.GetPointIds().SetId(1, pid[1])
            quad.GetPointIds().SetId(2, pid[2])
            quad.GetPointIds().SetId(3, pid[3])
            return quad

    def ReadScene(self, fid, fdata, n, bytesMirrored):

        self.n = n

        tag = ReadTag(fid, fdata)

        if tag == BEGIN_SCENE_LABEL:
            tag = ReadTag(fid, fdata)
            label = bytes()
            while tag != END_SCENE_LABEL:
                label = label + tag
                tag = ReadTag(fid,fdata)

            self.label = label.decode('ascii')
            tag = ReadTag(fid, fdata)

        if tag != END_SCENE:

            print('Reading Scene: \'{}\' {} ... '.format(self.label,n), end='');
            sys.stdout.flush()
            tic()

            while tag != END_SCENE:

                if tag == SPOINT:
                    # self.points.InsertNextPoint(self.GetVtkPoly(fid, fdata, 1, bytesMirrored, 'P'))
                    pass
                elif tag == SLINE:
                    self.lines.InsertNextCell(self.GetVtkPoly(fid, fdata, 2, bytesMirrored, 'L'))
                elif tag == STRIA:
                    self.polys.InsertNextCell(self.GetVtkPoly(fid, fdata, 3, bytesMirrored, 'T'))
                elif tag == SQUADRI:
                    self.polys.InsertNextCell(self.GetVtkPoly(fid, fdata, 4, bytesMirrored, 'Q'))
                elif tag == SSPHERE:
                    self.spheres.append(ReadSphere(fid, fdata, bytesMirrored))
                elif tag == SSPHOID:
                    self.spheroids.append(ReadSpheriod(fid, fdata, bytesMirrored))
                elif tag == STEXT:
                    # self.texts.append(ReadText(fid, fdata,bytesMirrored,'T'))
                    pass
                elif tag == SVECTOR:
                    self.AddVtkVector(fid, fdata, bytesMirrored)

                tag = ReadTag(fid, fdata)

            self.vtkSurfPolyData.SetPoints(self.points)
            self.vtkSurfPolyData.SetLines(self.lines)
            self.vtkSurfPolyData.SetPolys(self.polys)
            self.vtkSurfPolyData.GetPointData().SetScalars(self.colors)

            self.vtkVectPolyData.SetPoints(self.vecPoints)
            self.vtkVectPolyData.GetPointData().SetVectors(self.vectors)
            self.vtkVectPolyData.GetPointData().SetScalars(self.vectorMags)

            self.vtkEdgePolyData.SetPoints(self.points)
            self.vtkEdgePolyData.SetPolys(self.polys)

            self.vtkContPolyData.SetPoints(self.points)
            self.vtkContPolyData.SetPolys(self.polys)
            self.vtkContPolyData.GetPointData().SetScalars(self.temps)
            print('done. ', end='')
            toc()

        tag = ReadTag(fid, fdata)
        return tag

    def CreateVtkMapperActor(self):

        self.surfMapper = vtk.vtkPolyDataMapper()

        self.surfMapper.SetInputData(self.vtkSurfPolyData)
        self.surfActor = vtk.vtkActor()
        self.surfActor.SetMapper(self.surfMapper)

        self.contMapper = vtk.vtkPolyDataMapper()
        scalarRange = self.vtkContPolyData.GetScalarRange()
        if scalarRange[0] > scalarRange[1]:
            scalarRange = (0, 1)

        self.contMapper.SetScalarRange(scalarRange)

        lut = MakeLUT()
        # lut.SetNumberOfTableValues(20)
        numberOfBands = lut.GetNumberOfTableValues()
        bands = MakeBands(scalarRange, numberOfBands, False)

        lut.SetTableRange(scalarRange)

        # We will use the midpoint of the band as the label.
        labels = []
        for i in range(numberOfBands):
            labels.append('{:4.2f}'.format(bands[i][1]))

        # Annotate
        values = vtk.vtkVariantArray()
        for i in range(len(labels)):
            values.InsertNextValue(vtk.vtkVariant(labels[i]))
        for i in range(values.GetNumberOfTuples()):
            lut.SetAnnotation(i, values.GetValue(i).ToString())

        # Create the contour bands.
        bcf = vtk.vtkBandedPolyDataContourFilter()
        bcf.SetInputData(self.vtkContPolyData)
        # Use either the minimum or maximum value for each band.
        for i in range(0, numberOfBands):
            bcf.SetValue(i, bands[i][2])
        # We will use an indexed lookup table.
        bcf.SetScalarModeToIndex()
        bcf.GenerateContourEdgesOn()

        self.contMapper.SetInputConnection(bcf.GetOutputPort())
        self.contMapper.SetScalarRange(scalarRange)
        self.contMapper.SetLookupTable(lut)
        self.contMapper.SetScalarModeToUseCellData()

        self.contActor = vtk.vtkActor()
        self.contActor.SetMapper(self.contMapper)
        self.contActor.VisibilityOff()

        self.edgeMapper = vtk.vtkPolyDataMapper()
        self.edgeMapper.SetInputData(self.vtkEdgePolyData)
        self.edgeActor = vtk.vtkActor()
        self.edgeActor.SetMapper(self.edgeMapper)
        self.edgeActor.GetProperty().SetRepresentationToWireframe()
        self.edgeActor.GetProperty().SetColor([0, 0, 0])

        self.edgeActor.VisibilityOff()

        # Source for the glyph filter
        arrow = vtk.vtkArrowSource()
        arrow.SetTipResolution(16)
        arrow.SetTipLength(0.3)
        arrow.SetTipRadius(0.1)

        glyph = vtk.vtkGlyph3D()
        glyph.SetSourceConnection(arrow.GetOutputPort())
        glyph.AddInputData(self.vtkVectPolyData)
        glyph.SetVectorModeToUseVector()
        glyph.SetScaleFactor(1)
        # glyph.SetColorModeToColorByScalar()

        glyph.SetScaleModeToScaleByVector()
        glyph.OrientOn()
        glyph.Update()

        self.glyphMapper = vtk.vtkPolyDataMapper()
        self.glyphMapper.SetInputConnection(glyph.GetOutputPort())
        self.glyphMapper.SetScalarModeToUsePointFieldData()
        # self.glyphMapper.SetColorModeToMapScalars()
        self.glyphMapper.ScalarVisibilityOn()
        # self.glyphMapper.SelectColorArray('vecMag')
        # Colour by scalars.
        # scalarRange = polydata.GetScalerRange()
        # glyphMapper.SetScalarRange(scalarRange)

        self.glyphActor = vtk.vtkActor()
        self.glyphActor.GetProperty().SetColor(0.3, 0.3, 0.0)
        self.glyphActor.SetMapper(self.glyphMapper)

class StructureInteractorStyle(vtk.vtkInteractorStyleTrackballCamera):

    def __init__(self, vtkCuv):
        self.vtkCuv = vtkCuv
        self.AddObserver("LeftButtonPressEvent", self.leftButtonPressEvent)
        self.AddObserver("MouseMoveEvent", self.mouseMoveEvent)
        self.AddObserver("LeftButtonReleaseEvent", self.leftButtonReleaseEvent)
        self.AddObserver("KeyPressEvent", self.keyPressEvent)

        self.ScenePress = False
        self.SceneTxt = ''

    def leftButtonPressEvent(self, obj, event):
        self.mouse_motion = 0
        self.OnLeftButtonDown()
        return

    def mouseMoveEvent(self, obj, event):
        self.mouse_motion = 1
        self.OnMouseMove()
        return

    def leftButtonReleaseEvent(self, obj, event):
        ren = obj.GetCurrentRenderer()
        iren = ren.GetRenderWindow().GetInteractor()
        if self.mouse_motion == 0:
            pos = iren.GetEventPosition()
            iren.GetPicker().Pick(pos[0], pos[1], 0, ren)
        self.OnLeftButtonUp()
        return

    def keyPressEvent(self, obj, event):
        vtkCuv = obj.vtkCuv
        sym = vtkCuv.renderWindowInteractor.GetKeySym()

        if self.ScenePress:
            if sym in "t":
                self.ScenePress = False
                n = int(self.SceneTxt) - 1
                vtkCuv.SceneToggleVis(n)
                self.SceneTxt = ''
                vtkCuv.ReDraw()

            elif sym in "1234567890":
                self.SceneTxt = self.SceneTxt + sym
            else:
                print('bad scene number')
                self.ScenePress = False
        elif sym in "t":
            self.ScenePress = True
        elif sym in "R":
            vtkCuv.ReReadFile()
        elif sym in "a":
            vtkCuv.SceneVis(True)
            vtkCuv.ReDraw()
        elif sym in "n":
            vtkCuv.SceneVis(False)
            vtkCuv.ReDraw()
        elif sym in "i":
            vtkCuv.PrintSceneInfo()
        elif sym in "p":
            vtkCuv.TogglePersp()
            vtkCuv.ReDraw()
        elif sym in "rlfbudv":
            vtkCuv.SetView(sym)
        elif sym in "o":
            if vtkCuv.EdgeDraw:
                vtkCuv.EdgeDraw = False
            else:
                vtkCuv.EdgeDraw = True
            vtkCuv.ReDraw()
        elif sym in "c":
            if vtkCuv.ContDraw:
                vtkCuv.ContDraw = False
                vtkCuv.Lighting = True
            else:
                vtkCuv.ContDraw = True
                vtkCuv.Lighting = False
            vtkCuv.ReDraw()
        elif sym in "L":
            if vtkCuv.Lighting:
                vtkCuv.Lighting = False
            else:
                vtkCuv.Lighting = True
            vtkCuv.ReDraw()
        elif sym in "V":
            if vtkCuv.VectDraw:
                vtkCuv.VectDraw = False
            else:
                vtkCuv.VectDraw = True
            vtkCuv.ReDraw()
        elif sym in "h":
            vtkCuv.ShowHelp()

        self.OnKeyPress()


class cuvFileData(object):

    def __init__(self,file):
        self.pos = 0

        try:
            fid = open(file, 'rb')

            self.data = fid.read()
            fid.close()
        except IOError:
            print("Could not read file: {}".format(file))
            exit()

class CreateVtkCuv(object):

    def __init__(self):
        self.version = ''
        self.err = 0
        self.scenes = []
        self.view = bytes.fromhex('00')
        self.bytesMirrored = False
        self.SurfDraw = True
        self.EdgeDraw = False
        self.ContDraw = False
        self.VectDraw = True
        self.Lighting = True

    def ReadCuvFile(self, file=None):

        print('Reading file ... ')

        if file is not None:
            self.file = file

        self.fdata = cuvFileData(self.file)

        # self.fid = open(self.file, 'rb')
        self.fid = 0

        if not self.ReadInitGLFile():
            self.err = 1

        if not self.ReadScenes():
            self.err = 1

        if not self.ReadEndGLFile():
            self.err = 1

        print('Done')

    def ReadInitGLFile(self):

        # check = np.fromfile(self.fid,np.uint32, 1)

        check = np.frombuffer(self.fdata.data, np.uint32, 1, self.fdata.pos)

        self.fdata.pos = self.fdata.pos + 4

        if check == DATA_NORMAL_ORDER:
            self.bytesMirrored = False
        elif check == DATA_MIRROR_ORDER:
            self.bytesMirrored = True
        else:
            return False

        if ReadTag(self.fid, self.fdata) != BEGIN_DATA:
            return False

        if ReadTag(self.fid, self.fdata) == BEGIN_VERSION:
            tag = ReadTag(self.fid, self.fdata)
            version = bytes()

            while tag != END_VERSION:
                version = version + tag
                tag = ReadTag(self.fid, self.fdata)

            self.version = version.decode('ascii')

        else:
            return False

        return True

    def ReadEndGLFile(self):

        if ReadTag(self.fid, self.fdata) == VPRESET_VIEW:
            self.view = ReadTag(self.fid, self.fdata)

        while ReadTag(self.fid, self.fdata) != END_VIEW: # ignore view settings for now
            pass

        if ReadTag(self.fid, self.fdata) != END_DATA_STAY:
            return False

        return True

    def ReadScenes(self):

        tag = ReadTag(self.fid, self.fdata)
        if tag != BEGIN_SCENE:
            return False

        nScene = 1
        self.scenes = []
        while tag == BEGIN_SCENE:

            scene = Scene()
            self.scenes.append(scene)
            tag = scene.ReadScene(self.fid, self.fdata, nScene, self.bytesMirrored)
            nScene = nScene + 1

        if tag != BEGIN_VIEW:
            return False
        else:
            return True

    def CreateSceneMappersAndActors(self):

        for s in self.scenes:
            s.CreateVtkMapperActor()

    def AddActors(self):
        for s in self.scenes:
            self.renderer.AddActor(s.surfActor)
            self.renderer.AddActor(s.edgeActor)
            self.renderer.AddActor(s.contActor)
            self.renderer.AddActor(s.glyphActor)

    def RemoveActors(self):
        for s in self.scenes:
            self.renderer.RemoveActor(s.surfActor)
            self.renderer.RemoveActor(s.edgeActor)
            self.renderer.RemoveActor(s.contActor)
            self.renderer.RemoveActor(s.glyphActor)

    def SetRenderWin(self):

        self.CreateSceneMappersAndActors()

        self.renderer = vtk.vtkRenderer()
        self.renderWindow = vtk.vtkRenderWindow()
        self.renderWindow.AddRenderer(self.renderer)

        WIDTH = 940
        HEIGHT = 680
        self.renderWindow.SetSize(WIDTH, HEIGHT)

        self.renderWindowInteractor = vtk.vtkRenderWindowInteractor()
        self.renderWindowInteractor.SetRenderWindow(self.renderWindow)
        self.renderer.SetBackground(.9, .9, .9)

        self.AddActors()

        style = StructureInteractorStyle(self)
        self.renderWindowInteractor.SetInteractorStyle(style)

        self.PrintSceneInfo()

        self.camera = self.renderer.GetActiveCamera()
        self.renderer.ResetCamera()
        self.SetView('v')


    def SetView(self,view):

        npos = self.camera.GetPosition()
        foc = self.camera.GetFocalPoint()
        nview = self.camera.GetViewUp()

        if view == 'r':
            npos = (foc[0]-1, foc[1], foc[2])
            nview = (0, 0, 1)
        elif view == 'l':
            npos = (foc[0]+1, foc[1], foc[2])
            nview = (0, 0, 1)
        elif view == 'f':
            npos = (foc[0], foc[1]-1, foc[2])
            nview = (0, 0, 1)
        elif view == 'b':
            npos = (foc[0], foc[1]+1, foc[2])
            nview = (0, 0, 1)
        elif view == 'u':
            npos = (foc[0], foc[1], foc[2]-1.0)
            nview = (0, -1, 0)
        elif view == 'd':
            npos = (foc[0], foc[1], foc[2] + 1.0)
            nview = (0, 1, 0)
        elif view == 'v':
            npos = (foc[0]+1, foc[1]-1, foc[2] + 1.0)
            nview = (0, 0, 1)

        self.camera.OrthogonalizeViewUp()
        if view in 'rlfbud':
            self.camera.ParallelProjectionOn()

        self.camera.SetPosition(npos)
        self.camera.SetViewUp(nview)
        self.renderer.ResetCamera()

        self.ReDraw()


    def ReReadFile(self):
        
        self.RemoveActors()
        self.ReadCuvFile()
        self.CreateSceneMappersAndActors()
        self.AddActors()
        self.ReDraw()

    def ReDraw(self):

        for s in self.scenes:

            if not s.visible:
                s.surfActor.VisibilityOff()
                s.contActor.VisibilityOff()
                s.edgeActor.VisibilityOff()
                s.glyphActor.VisibilityOff()
            else:

                if self.SurfDraw:
                    s.surfActor.VisibilityOn()
                    s.contActor.VisibilityOff()
                else:
                    s.surfActor.VisibilityOff()
                    s.contActor.VisibilityOn()

                if self.ContDraw:
                    s.surfActor.VisibilityOff()
                    s.contActor.VisibilityOn()
                else:
                    s.surfActor.VisibilityOn()
                    s.contActor.VisibilityOff()

                if self.EdgeDraw:
                    s.edgeActor.VisibilityOn()
                else:
                    s.edgeActor.VisibilityOff()

                if self.VectDraw:
                    s.glyphActor.VisibilityOn()
                else:
                    s.glyphActor.VisibilityOff()

                if self.Lighting:
                    s.surfActor.GetProperty().LightingOn()
                    s.contActor.GetProperty().LightingOn()
                    s.glyphActor.GetProperty().LightingOn()
                else:
                    s.surfActor.GetProperty().LightingOff()
                    s.contActor.GetProperty().LightingOff()
                    s.glyphActor.GetProperty().LightingOff()

        self.renderWindow.Render()
        # self.PrintSceneInfo()

    def SceneVis(self,vis):
        for s in self.scenes:
            s.visible = vis

    def TogglePersp(self):
        if self.camera.GetParallelProjection():
            self.camera.ParallelProjectionOff()
        else:
            self.camera.ParallelProjectionOn()

    def SceneToggleVis(self,n):

        if n < 0 or n >= len(self.scenes):
            print('Bad Scene number')
            return

        self.scenes[n].visible = not self.scenes[n].visible

        if self.scenes[n].visible:
            print('Scene {} on'.format(n+1))
        else:
            print('Scene {} off'.format(n+1))

    def PrintSceneInfo(self):
        print('\nScenes: ')

        for s in self.scenes:

            print ('\t Scene \'{}\' {} Vis: {} [e {} s {} c {} v {}] Entities: Lines {} Polys {} vecs {}'.format(
                s.label, s.n, s.visible, s.edgeActor.GetVisibility(),
                s.surfActor.GetVisibility(),
                s.contActor.GetVisibility(),
                s.glyphActor.GetVisibility(),
                s.vtkSurfPolyData.GetNumberOfLines(),
                s.vtkSurfPolyData.GetNumberOfPolys(),
                s.vtkVectPolyData.GetNumberOfVerts()))


    def ShowHelp(self):
        print('\nKey board commands:')
        print('\ts: Toggle screen visibility. Command sequence: s <scene number> s')
        print('\ta: Draw all scenes')
        print('\tn: Don\'t draw any scenes')
        print('\tp: toggle perspective view')
        print('\trlfbfud: Standard views')
        print('\t\tr: right side')
        print('\t\tl: left side')
        print('\t\tf: front side')
        print('\t\tb: back side')
        print('\t\tu: bottom side')
        print('\t\td: top side')
        print('\to: Outline polys')
        print('\tc: Create contours')
        print('\ti: Print scene info.')
        print('\th: This message')
        print('\tR: Reread and render file')


def WriteGLTag(fid, tag):
    fid.write(tag)

def WriteGLCheck(fid):
    ch = np.int32(DATA_ORDER_CHECK)
    np.array([ch]).tofile(fid)

def WriteGLString(fid,str):
    strBA = bytearray(str,'utf8')
    fid.write(strBA)

def WriteInitGLFile(file):

    fid = open(file,'wb')

    WriteGLCheck(fid)
    WriteGLTag(fid, BEGIN_DATA)
    WriteGLTag(fid, BEGIN_VERSION)
    WriteGLString(fid, VERSION_STRING)
    WriteGLTag(fid, END_VERSION)

    return fid

def WriteSceneBegin(fid,label):

    WriteGLTag(fid, BEGIN_SCENE)
    if label != '':
        WriteGLTag(fid, BEGIN_SCENE_LABEL)
        WriteGLString(fid,label)
        WriteGLTag(fid, END_SCENE_LABEL)

def WriteSceneEnd(fid):

    WriteGLTag(fid, END_SCENE)

def WriteCloseGLFile(fid):

    WriteGLTag(fid, BEGIN_VIEW);

    WriteGLTag(fid, VPRESET_VIEW);
    WriteGLTag(fid, bytes([0]));
    WriteGLTag(fid, END_VIEW);
    WriteGLTag(fid, END_DATA_STAY);
    fid.close()

def WriteGLFloats(fid, vec):

    for f in vec:
        v = np.float32(f)
        np.array([v]).tofile(fid)

def WriteGLColorAndTrans(fid,color,trans):
    WriteGLFloats(fid, color)
    if trans != 0.0:
        WriteGLFloats(fid, trans)

def Write_GL_line(fid, p1, p2, color, color2, trans, multi):

    WriteGLTag(fid,SLINE)

    flags = SOUTLINE
    if trans != 0.0:
        flags = bytes([flags[0] | STRANSPARENT[0]])
    if multi:
        flags = bytes([flags[0] | SMULTICOLOR[0]])

    WriteGLTag(fid, flags)

    WriteGLFloats(fid, p1)
    WriteGLFloats(fid, p2)

    WriteGLFloats(fid, color)

    if flags[0] & SMULTICOLOR[0]:
        WriteGLFloats(fid, color2)

    if flags[0] & STRANSPARENT[0]:
        WriteGLFloats(fid, trans)

def Write_GL_tri(fid, p1, p2, p3, color, color2, color3, trans, multi, out):

    WriteGLTag(fid,STRIA)

    flags = SFILL
    if trans != 0.0:
        flags =  bytes([flags[0] | STRANSPARENT[0]])
    if multi:
        flags =  bytes([flags[0] | SMULTICOLOR[0]])
    if out:
        flags =  bytes([flags[0] | SOUTLINE[0]])

    WriteGLTag(fid, flags)

    WriteGLFloats(fid, p1)
    WriteGLFloats(fid, p2)
    WriteGLFloats(fid, p3)

    WriteGLColorAndTrans(fid, color, trans)

    if flags[0] & SMULTICOLOR[0]:
        WriteGLColorAndTrans(fid, color2, trans)
        WriteGLColorAndTrans(fid, color3, trans)

def Write_GL_quad(fid, p1, p2, p3, p4,  color, color2, color3, color4, trans, multi, out):

    WriteGLTag(fid, SQUADRI)

    flags = SFILL
    if trans != 0.0:
        flags =  bytes([flags[0] | STRANSPARENT[0]])
    if multi:
        flags =  bytes([flags[0] | SMULTICOLOR[0]])
    if out:
        flags =  bytes([flags[0] | SOUTLINE[0]])

    WriteGLTag(fid, flags)

    WriteGLFloats(fid, p1)
    WriteGLFloats(fid, p2)
    WriteGLFloats(fid, p3)
    WriteGLFloats(fid, p4)

    WriteGLColorAndTrans(fid, color, trans)

    if flags[0] & SMULTICOLOR[0]:
        WriteGLColorAndTrans(fid, color2, trans)
        WriteGLColorAndTrans(fid, color3, trans)
        WriteGLColorAndTrans(fid, color4, trans)


def Write_GL_vector(fid, p0, vec):

    WriteGLTag(fid, SVECTOR)
    WriteGLFloats(fid, p0)
    WriteGLFloats(fid, vec)

