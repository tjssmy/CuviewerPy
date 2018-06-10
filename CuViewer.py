#!/usr/local/bin/python3

import numpy as np
import vtk
import math
import sys
import re
import ReadGLFile as r
import Constants as c
import MainWindow



def tic():
    # Homemade version of matlab tic and toc functions
    import time
    global startTime_for_tictoc
    startTime_for_tictoc = time.time()


def toc():
    import time
    if 'startTime_for_tictoc' in globals():
        print("Elapsed time is {0:8f} seconds.".format(float(str(time.time() - startTime_for_tictoc))))
    else:
        print("Toc: start time not set")


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
        self.sphereSource = vtk.vtkSphereSource()
        self.sphereSource.SetCenter(pos[0], pos[1], pos[2])
        self.sphereSource.SetRadius(rad[0])
        # Make the surface smooth.
        self.sphereSource.SetPhiResolution(100)
        self.sphereSource.SetThetaResolution(100)


class Spheroid(object):

    def __init__(self, pos, rad, color, tr, fill, out):
    # def __init__(self, pos, rad, axis, rot, color, tr, fill, out):
        self.spheroidSource = vtk.vtkParametricEllipsoid()
        self.spheroidSource.SetXRadius(rad[0])
        self.spheroidSource.SetYRadius(rad[1])
        self.spheroidSource.SetZRadius(rad[1])        
        self.position = pos


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
        self.number = 0

        self.points = vtk.vtkPoints()
        self.vecPoints = vtk.vtkPoints()

        self.temps = vtk.vtkFloatArray()
        self.temps.SetNumberOfComponents(1)
        self.temps.SetName("Temps")

        self.colors = vtk.vtkUnsignedCharArray()
        self.colors.SetNumberOfComponents(3)
        self.colors.SetName("Colors")

        self.verts = vtk.vtkCellArray()
        self.lines = vtk.vtkCellArray()
        self.polys = vtk.vtkCellArray()
        self.i =0

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

    def AddVtkVector(self, fdata, bytesMirrored):
        pos = r.ReadFloats(fdata, np.float32, 3, bytesMirrored)
        vec = r.ReadFloats(fdata, np.float32, 3, bytesMirrored)
        vecMag = [math.sqrt(vec[0]*vec[0] + vec[1]*vec[1] + vec[2]*vec[2])]

        self.vecPoints.InsertNextPoint(pos)
        self.vectors.InsertNextTuple(vec)
        self.vectorMags.InsertNextTuple(vecMag)
        
    def GetVtkPoly(self, fdata, n, bytesMirrored, shape_type):
        geo = []
        pid = []

        fill, out, trans, multi = r.ReadFlags(fdata)

        for i in range(0, n):            
            geo.append(r.ReadFloats(fdata, np.float32, 3, bytesMirrored))

        color, tr = r.ReadColorAndTrans(fdata, fill, out, multi, trans, n, bytesMirrored)

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

        if shape_type == 'P':
            return pid[0]
            
        elif shape_type == 'L':
            line = vtk.vtkLine()
            line.GetPointIds().SetId(0, pid[0])
            line.GetPointIds().SetId(1, pid[1])
            return line

        elif shape_type == 'T':
            tri = vtk.vtkTriangle()
            tri.GetPointIds().SetId(0, pid[0])
            tri.GetPointIds().SetId(1, pid[1])
            tri.GetPointIds().SetId(2, pid[2])
            return tri

        elif shape_type == 'Q':
            quad = vtk.vtkQuad()
            quad.GetPointIds().SetId(0, pid[0])
            quad.GetPointIds().SetId(1, pid[1])
            quad.GetPointIds().SetId(2, pid[2])
            quad.GetPointIds().SetId(3, pid[3])
            return quad

    def GetVtkPoints(self, fdata, n, no_of_points, bytesMirrored):
        geo = []
        pid = []

        fill, out, trans, multi = r.ReadFlags(fdata)

        for i in range(0, n*no_of_points):
            geo.append(r.ReadFloats(fdata, np.float32, 3, bytesMirrored))
            pid.append(self.points.InsertNextPoint(geo[i]))
            color, tr = r.ReadColorAndTrans(fdata, fill, out, multi, trans, n, bytesMirrored)
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

        return pid
        
    def GetVtkPolys(self, fdata, n, no_of_lines, bytesMirrored):
        
        #Read flags
        fill, out, trans, multi = r.ReadFlags(fdata)
        pid = []
        for i in range(0, no_of_lines):
            #Read Points
            for j in range (0, n):
                pid.append(self.points.InsertNextPoint(r.ReadFloats(fdata, np.float32, 3, bytesMirrored)))
        
            #Read Colors
            color = []
            tr = []
        
            if multi:
                x = n
            else:
                x = 1			 
    
            for j in range (0, x):
                if fill or out:
                    color.append(np.multiply(r.ReadFloats(fdata, np.float32, 3, bytesMirrored), 255.0))
                else:
                    color.append(np.array([0.5, 0.5, 0.5]))
                if trans:
                    tr.append(r.ReadFloats(fdata, np.float32, 1, bytesMirrored))
                else:
                    tr.append(0.0)
            
                t = [color[j][0]]
                self.temps.InsertNextTypedTuple(t)
                col = tuple(color[j])
                self.colors.InsertNextTypedTuple(col)
        return pid

    def GetVtkSphere(self, fdata, bytesMirrored):
        fill, out, trans, multi = r.ReadFlags(fdata)
        multi = False

        pos = r.ReadFloats(fdata, np.float32, 3, bytesMirrored)
        rad = r.ReadFloats(fdata, np.float32, 1, bytesMirrored)

        color, tr = r.ReadColorAndTrans(fdata, fill,out,multi,trans,0, bytesMirrored)

        return Sphere(pos, rad, color, tr, fill, out)

    def GetVtkSpheroid(self, fdata, bytesMirrored):
        fill, out, trans, multi = r.ReadFlags(fdata)
        multi = False

        pos = r.ReadFloats(fdata, np.float32, 3, bytesMirrored)
        rad = r.ReadFloats(fdata, np.float32, 3, bytesMirrored)
        #axis = ReadFloats(fdata, np.float32, 3, bytesMirrored)
        #rot = ReadFloats(fdata, np.float32, 1, bytesMirrored)

        color, tr = r.ReadColorAndTrans(fdata, fill, out, multi, trans, 0, bytesMirrored)

        #return Spheroid(pos, rad, axis, rot, color, tr, fill, out)
        return Spheroid(pos, rad, color, tr, fill, out)
   
    def ReadScene(self, fdata, n, bytesMirrored):

        self.n = n
        
        tag = r.ReadTag(fdata)

        if tag == c.BEGIN_SCENE_LABEL:
            tag = r.ReadTag(fdata)
            label = bytes()
            while tag != c.END_SCENE_LABEL:
                label = label + tag
                tag = r.ReadTag(fdata)

            self.label = label.decode('ascii')
            self.number = int(re.search(r"\d+", self.label).group(0))
            tag = r.ReadTag(fdata)

        if tag != c.END_SCENE:
            print('Reading Scene: \'{}\' {} ... '.format(self.label,n), end='');
            sys.stdout.flush()
            tic()
            
            options = {
                c.SPOINT:           lambda fdata, bytesMirrored: self.InsertSPOINT(fdata, bytesMirrored),
                c.MULTIPLE_SPOINT:  lambda fdata, bytesMirrored: self.InsertMULTIPLESPOINT(fdata, bytesMirrored),
                c.SLINE:            lambda fdata, bytesMirrored: self.InsertSLINE(fdata, bytesMirrored),
                c.MULTIPLE_SLINE:   lambda fdata, bytesMirrored: self.InsertMULTIPLESLINE(fdata, bytesMirrored),
                c.STRIA:            lambda fdata, bytesMirrored: self.InsertSTRIA(fdata, bytesMirrored),
                c.MULTIPLE_STRIA:   lambda fdata, bytesMirrored: self.InsertMULTIPLESTRIA(fdata, bytesMirrored),
                c.SQUADRI:          lambda fdata, bytesMirrored: self.InsertSQUADRI(fdata, bytesMirrored),
                c.MULTIPLE_SQUADRI: lambda fdata, bytesMirrored: self.InsertMULTIPLESQUADRI(fdata, bytesMirrored),
                c.SSPHERE:          lambda fdata, bytesMirrored: self.InsertSSPHERE(fdata, bytesMirrored),
                c.SSPHOID:          lambda fdata, bytesMirrored: self.InsertSSPHOID(fdata, bytesMirrored),
                c.STEXT:            lambda fdata, bytesMirrored: self.InsertSTEXT(fdata, bytesMirrored),
                c.SVECTOR:          lambda fdata, bytesMirrored: self.InsertSVECTOR(fdata, bytesMirrored)
            }

            while tag != c.END_SCENE:
                options[tag](fdata, bytesMirrored)
                tag = r.ReadTag(fdata)
                
            toc()
            self.vtkSurfPolyData.SetPoints(self.points)
            self.vtkSurfPolyData.SetVerts(self.verts)
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
            print('done. ', end='\n')

        tag = r.ReadTag(fdata)
        return tag
        
    def InsertSPOINT(self, fdata, bytesMirrored):
        self.verts.InsertNextCell(1)
        self.verts.InsertCellPoint(self.GetVtkPoly(fdata, 1, bytesMirrored, 'P'))
            
    def InsertMULTIPLESPOINT(self, fdata, bytesMirrored):
        pid = self.GetVtkPoints(fdata, 1, self.number, bytesMirrored)
        for i in range(len(pid)):
            self.verts.InsertNextCell(1)
            self.verts.InsertCellPoint(pid[i])
        
    def InsertSLINE(self, fdata, bytesMirrored):
        self.lines.InsertNextCell(self.GetVtkPoly(fdata, 2, bytesMirrored, 'L'))
        
    def InsertMULTIPLESLINE(self, fdata, bytesMirrored):
        pid  = self.GetVtkPolys(fdata, 2, self.number, bytesMirrored)
        line = vtk.vtkLine()
        for i in range(0, len(pid), 2):
            line.GetPointIds().SetId(0, pid[i])
            line.GetPointIds().SetId(1, pid[i+1])
            self.lines.InsertNextCell(line)
        
    def InsertSTRIA(self, fdata, bytesMirrored):
        self.polys.InsertNextCell(self.GetVtkPoly(fdata, 3, bytesMirrored, 'T'))
        return
        
    def InsertMULTIPLESTRIA(self, fdata, bytesMirrored):
        pid  = self.GetVtkPolys(fdata, 3, self.number, bytesMirrored)
        tri = vtk.vtkTriangle()
        for i in range(0, len(pid), 3):
            tri.GetPointIds().SetId(0, pid[i])
            tri.GetPointIds().SetId(1, pid[i+1])
            tri.GetPointIds().SetId(2, pid[i+2])
            self.polys.InsertNextCell(tri)
        
    def InsertSQUADRI(self, fdata, bytesMirrored):
        self.polys.InsertNextCell(self.GetVtkPoly(fdata, 4, bytesMirrored, 'Q'))
    
    def InsertMULTIPLESQUADRI(self, fdata, bytesMirrored):
        pid  = self.GetVtkPolys(fdata, 4, self.number, bytesMirrored)
        quad = vtk.vtkQuad()
        for i in range(0, len(pid), 4):
            quad.GetPointIds().SetId(0, pid[i])
            quad.GetPointIds().SetId(1, pid[i+1])
            quad.GetPointIds().SetId(2, pid[i+2])
            quad.GetPointIds().SetId(3, pid[i+3])
            self.polys.InsertNextCell(quad)
        
    def InsertSSPHERE(self, fdata, bytesMirrored):
        self.spheres.append(self.GetVtkSphere(fdata, bytesMirrored))

    def InsertSSPHOID(self, fdata, bytesMirrored):
        self.spheroids.append(self.GetVtkSpheroid(fdata, bytesMirrored))

    def InsertSTEXT(self, fdata, bytesMirrored):
        self.texts.append(r.ReadText(fdata,bytesMirrored,'T'))
        return
        
    def InsertSVECTOR(self, fdata, bytesMirrored):
        self.AddVtkVector(fdata, bytesMirrored)

    def CreateArrowsGlyphs(self):

        # Source for the glyph filter
        self.arrow = vtk.vtkArrowSource()
        self.arrow.SetTipResolution(16)
        self.arrow.SetTipLength(0.3)
        self.arrow.SetTipRadius(0.1)

        self.glyph = vtk.vtkGlyph3D()
        self.glyph.SetSourceConnection(self.arrow.GetOutputPort())
        self.glyph.AddInputData(self.vtkVectPolyData)
        self.glyph.SetVectorModeToUseVector()
        self.glyph.SetScaleFactor(1)
        # glyph.SetColorModeToColorByScalar()

        self.glyph.SetScaleModeToScaleByVector()
        self.glyph.OrientOn()
        self.glyph.Update()

    def ResetArrowGlyphScale(self, sc):
        self.glyph.SetScaleFactor(self.glyph.GetScaleFactor()*sc)

    def CreateVtkMapperActor(self):

        self.surfMapper = vtk.vtkPolyDataMapper()

        self.surfMapper.SetInputData(self.vtkSurfPolyData)
        self.surfActor = vtk.vtkActor()
        self.surfActor.SetMapper(self.surfMapper)
        self.surfActor.GetProperty().SetLineWidth(2.0)
        self.surfActor.GetProperty().SetPointSize(8.0)

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
        self.edgeActor.GetProperty().SetLineWidth(2.0)

        self.edgeActor.VisibilityOff()

        # Source for the glyph filter
        self.CreateArrowsGlyphs()

        self.glyphMapper = vtk.vtkPolyDataMapper()
        self.glyphMapper.SetInputConnection(self.glyph.GetOutputPort())
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
        
        # Sphere Source
        self.sphereMapper = list()
        self.sphereActor = list()
        for i in range(0, len(self.spheres)):
            self.sphereMapper.append(vtk.vtkPolyDataMapper())
            self.sphereMapper[i].SetInputConnection(self.spheres[i].sphereSource.GetOutputPort())
            self.sphereActor.append(vtk.vtkActor())
            self.sphereActor[i].SetMapper(self.sphereMapper[i])
        
        # Spheroid Source
        self.spheroidMapper = list()
        self.spheroidActor = list()
        parametricFunctionSources = list()
        for i in range(0, len(self.spheroids)):
            parametricFunctionSources.append(vtk.vtkParametricFunctionSource())
            parametricFunctionSources[i].SetParametricFunction(self.spheroids[i].spheroidSource)
            parametricFunctionSources[i].SetUResolution(51)
            parametricFunctionSources[i].SetVResolution(51)
            parametricFunctionSources[i].SetWResolution(51)
            parametricFunctionSources[i].Update()
            
            # Transform to current position
            aTransform = vtk.vtkTransform()
            aTransform.Translate(self.spheroids[i].position[0], self.spheroids[i].position[1], self.spheroids[i].position[2])
            transFilter = vtk.vtkTransformFilter()
            transFilter.SetInputConnection(parametricFunctionSources[i].GetOutputPort())
            transFilter.SetTransform(aTransform)
            
            self.spheroidMapper.append(vtk.vtkPolyDataMapper())
            self.spheroidMapper[i].SetInputConnection(transFilter.GetOutputPort())
            self.spheroidActor.append(vtk.vtkActor())
            self.spheroidActor[i].SetMapper(self.spheroidMapper[i])


class CuvFileData(object):
    def __init__(self,file):
        self.pos = 0

        try:
            self.data = np.fromfile(file, 'int8')
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

        self.fdata = CuvFileData(self.file)
        self.fid = 0

        if not self.ReadInitGLFile():
            self.err = 1

        if not self.ReadScenes():
            self.err = 1

        if not self.ReadEndGLFile():
            self.err = 1

        print('Done')

    def ReadInitGLFile(self):
        check = r.ReadUint(self.fdata, np.uint32, 1, False)

        if check == c.DATA_NORMAL_ORDER:
            self.bytesMirrored = False
        elif check == c.DATA_MIRROR_ORDER:
            self.bytesMirrored = True
        else:
            return False

        if r.ReadTag(self.fdata) != c.BEGIN_DATA:
            return False

        if r.ReadTag(self.fdata) == c.BEGIN_VERSION:
            tag = r.ReadTag(self.fdata)
            version = bytes()

            while tag != c.END_VERSION:
                version = version + tag
                tag = r.ReadTag(self.fdata)

            self.version = version.decode('ascii')

        else:
            return False

        return True

    def ReadEndGLFile(self):
        if r.ReadTag(self.fdata) == c.VPRESET_VIEW:
            self.view = r.ReadTag(self.fdata)

        while r.ReadTag(self.fdata) != c.END_VIEW: # ignore view settings for now
            pass

        if r.ReadTag(self.fdata) != c.END_DATA_STAY:
            return False

        return True

    def ReadScenes(self):
        tag = r.ReadTag(self.fdata)
        if tag != c.BEGIN_SCENE:
            return False

        nScene = 1
        self.scenes = []
        while tag == c.BEGIN_SCENE:

            scene = Scene()
            self.scenes.append(scene)
            tag = scene.ReadScene(self.fdata, nScene, self.bytesMirrored)
            nScene = nScene + 1
            print('Read scenes and visualize')

        if tag != c.BEGIN_VIEW:
            return False
        else:
            return True

    def SetRenderWin(self):
        self.window = MainWindow.MainWindow(self.scenes)
