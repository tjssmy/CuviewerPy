#!/usr/local/bin/python3

import numpy as np
import vtk
import math
import sys
import re
import ReadGLFile as r
import Constants as c
import display

from PyQt4 import QtCore, QtGui
from vtk.qt4.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
#from PyQt4.QtCore import QThread
#from PyQt4.QtCore import QObject, pyqtSignal, pyqtSlot


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


class StructureInteractorStyle(vtk.vtkInteractorStyleTrackballCamera):

    def __init__(self, vtkCuv):
        self.vtkCuv = vtkCuv
        self.AddObserver("LeftButtonPressEvent", self.leftButtonPressEvent)
        self.AddObserver("MouseMoveEvent", self.mouseMoveEvent)
        self.AddObserver("LeftButtonReleaseEvent", self.leftButtonReleaseEvent)
        self.AddObserver("KeyPressEvent", self.keyPressEvent)

        self.ScenePress = False
        self.SceneTxt = ''
        self.SceneTxt1 = ''

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
                if self.SceneTxt1 is "":
                    n0 = -1
                else:
                    n0 = int(self.SceneTxt1) - 1

                if self.SceneTxt is "":
                    n1 = -1
                else:
                    n1 = int(self.SceneTxt) - 1

                vtkCuv.SceneToggleVis(n0, n1)
                self.SceneTxt = ''
                vtkCuv.ReDraw()

            elif sym in "1234567890":
                self.SceneTxt = self.SceneTxt + sym
            elif sym == 'minus':
                self.SceneTxt1 = self.SceneTxt
                self.SceneTxt = ""
            else:
                print('bad scene number')
                self.ScenePress = False
        elif sym in "t":
            self.SceneTxt1 = ''
            self.SceneTxt = ''
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
        elif sym == 'minus':
            vtkCuv.ResetArrowGlyphScale(0.9)
            vtkCuv.ReDraw()
        elif sym == 'plus':
            vtkCuv.ResetArrowGlyphScale(1.1)
            vtkCuv.ReDraw()
        elif sym in "V":
            if vtkCuv.VectDraw:
                vtkCuv.VectDraw = False
            else:
                vtkCuv.VectDraw = True
            vtkCuv.ReDraw()
        elif sym in "L":
            if vtkCuv.Lighting:
                vtkCuv.Lighting = False
            else:
                vtkCuv.Lighting = True
            vtkCuv.ReDraw()
        elif sym in "h":
            vtkCuv.ShowHelp()

        self.OnKeyPress()


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

    def CreateSceneMappersAndActors(self):
        for s in self.scenes:
            s.CreateVtkMapperActor()

    def AddActors(self):
        for s in self.scenes:
            self.renderer.AddActor(s.surfActor)
            self.renderer.AddActor(s.edgeActor)
            self.renderer.AddActor(s.contActor)
            self.renderer.AddActor(s.glyphActor)
            for i in range(0, len(s.sphereActor)):
                self.renderer.AddActor(s.sphereActor[i])
            for i in range(0, len(s.spheroidActor)):
                self.renderer.AddActor(s.spheroidActor[i])

    def RemoveActors(self):
        for s in self.scenes:
            self.renderer.RemoveActor(s.surfActor)
            self.renderer.RemoveActor(s.edgeActor)
            self.renderer.RemoveActor(s.contActor)
            self.renderer.RemoveActor(s.glyphActor)
            for i in range(0, len(s.sphereActor)):
                self.renderer.RemoveActor(s.sphereActor)
            for i in range(0, len(s.spheroidActor)):
                self.renderer.RemoveActor(s.spheroidActor[i])

    def SetRenderWin(self):
        self.CreateSceneMappersAndActors()

        self.window = MainWindow(self.scenes)

        #self.renderer = vtk.vtkRenderer()
        #self.renderWindow = vtk.vtkRenderWindow()
        #self.renderWindow.AddRenderer(self.renderer)

        #WIDTH = 940
        #HEIGHT = 680
        #self.renderWindow.SetSize(WIDTH, HEIGHT)

        #self.renderWindowInteractor = vtk.vtkRenderWindowInteractor()
        #self.renderWindowInteractor.SetRenderWindow(self.renderWindow)
        #self.renderer.SetBackground(.9, .9, .9)

        #self.AddActors()


        #style = StructureInteractorStyle(self)
        #self.renderWindowInteractor.SetInteractorStyle(style)

        #self.PrintSceneInfo()

        #self.camera = self.renderer.GetActiveCamera()
        #self.renderer.ResetCamera()
        #self.SetView('v')

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

    def ResetArrowGlyphScale(self,sc):
        for s in self.scenes:
            s.ResetArrowGlyphScale(sc)

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

    def SceneToggleVis(self, n0, n1):
        if n1 == -1:
            n1 = n0

        if n0 == -1:
            n0 = n1

        if n0 == -1 and n1 == -1:
            print('Bad Scene number(s)')
            return

        if n0 < 0 or n0 >= len(self.scenes) or n1 < 0 or n1 >= len(self.scenes):
            print('Bad Scene number')
            return

        for n in range(n0, n1+1):
            self.scenes[n].visible = not self.scenes[n].visible

            if self.scenes[n].visible:
                print('Scene {} on'.format(n+1))
            else:
                print('Scene {} off'.format(n+1))

    def PrintSceneInfo(self):
        print('\nScenes: ')

        for s in self.scenes:

            print ('\t {:>3} \t{:>40} \tVis: {} [e {} s {} c {} v {}] Entities: Lines {} Polys {:>6} vecs {}'.format(
                s.n, s.label, s.visible, s.edgeActor.GetVisibility(),
                s.surfActor.GetVisibility(),
                s.contActor.GetVisibility(),
                s.glyphActor.GetVisibility(),
                s.vtkSurfPolyData.GetNumberOfLines(),
                s.vtkSurfPolyData.GetNumberOfPolys(),
                s.vtkVectPolyData.GetNumberOfVerts()))

    def ShowHelp(self):
        print('\nKey board commands:')
        print('\tt: Toggle screen visibility.')
        print('\t\t1) Command sequence single scene: t <scene number> t')
        print('\t\t2) Command sequence scene range: t <scene number> - <scene number t')
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
        print('\tR: Reread and render file')
        print('\tL: Toggle lighting on/off')
        print('\tV: Toggle vectors on/off')
        print('\t+: Increase vectors size')
        print('\t-: Increase vectors size')
        print('\th: This message')


class MainWindow(QtGui.QMainWindow, display.Ui_MainWindow):

    def __init__(self, scenes):
        ##
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
        ##
        super(self.__class__, self).__init__()
        self.setupUi(self)

        self.scenes = scenes

        self.vl = QtGui.QVBoxLayout()
        self.vtkWidget = QVTKRenderWindowInteractor(self.frame)
        self.vl.addWidget(self.vtkWidget)
        self.frame.setLayout(self.vl)

        self.renderer = vtk.vtkRenderer()
        self.renderWindowInteractor = vtk.vtkRenderWindowInteractor()
        self.renderer.SetBackground(.9, .9, .9)

        self.AddActors()

        style = StructureInteractorStyle(self)
        self.renderWindowInteractor.SetInteractorStyle(style)

        self.PrintSceneInfo()


        self.vtkWidget.GetRenderWindow().AddRenderer(self.renderer)
        self.vtkWidget.GetRenderWindow().Render()
        self.vtkWidget.Initialize()


        self.camera = self.renderer.GetActiveCamera()
        self.renderer.ResetCamera()
        self.SetView('v')


    def CreateSceneMappersAndActors(self, scenes):
        for s in scenes:
            s.CreateVtkMapperActor()

    def AddActors(self):
        for s in self.scenes:
            self.renderer.AddActor(s.surfActor)
            self.renderer.AddActor(s.edgeActor)
            self.renderer.AddActor(s.contActor)
            self.renderer.AddActor(s.glyphActor)
            for i in range(0, len(s.sphereActor)):
                self.renderer.AddActor(s.sphereActor[i])
            for i in range(0, len(s.spheroidActor)):
                self.renderer.AddActor(s.spheroidActor[i])

    def PrintSceneInfo(self):
        print('\nScenes: ')

        for s in self.scenes:

            print ('\t {:>3} \t{:>40} \tVis: {} [e {} s {} c {} v {}] Entities: Lines {} Polys {:>6} vecs {}'.format(
                s.n, s.label, s.visible, s.edgeActor.GetVisibility(),
                s.surfActor.GetVisibility(),
                s.contActor.GetVisibility(),
                s.glyphActor.GetVisibility(),
                s.vtkSurfPolyData.GetNumberOfLines(),
                s.vtkSurfPolyData.GetNumberOfPolys(),
                s.vtkVectPolyData.GetNumberOfVerts()))

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

        #self.renderWindow.Render()
        self.vtkWidget.GetRenderWindow().Render()
        # self.PrintSceneInfo()