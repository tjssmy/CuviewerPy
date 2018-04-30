#!/usr/bin/env python

import math

import vtk
import numpy as np

# Available surfaces are:
SURFACE_TYPE = {"TORUS", "PARAMETRIC_HILLS", "PARAMETRIC_TORUS"}


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


def MakeStrip(nx,ny):

    x = np.linspace(0, 100, nx)
    y = np.linspace(0, 10, ny)

    points = vtk.vtkPoints()

    polys = vtk.vtkCellArray()
    lines = vtk.vtkCellArray()

    temps = vtk.vtkFloatArray()
    temps.SetNumberOfComponents(1)
    temps.SetName("Temps")

    for j in range(0, ny - 1):
        for i in range(0, nx - 1):
            p1 = [x[i], y[j], 0]
            p2 = [x[i], y[j + 1], 0]
            p3 = [x[i + 1], y[j + 1], 0]
            p4 = [x[i + 1], y[j], 0]

            temps.InsertNextTypedTuple([x[i]])
            temps.InsertNextTypedTuple([x[i]])
            temps.InsertNextTypedTuple([x[i + 1]])
            temps.InsertNextTypedTuple([x[i + 1]])

            pid1 = points.InsertNextPoint(p1)
            pid2 = points.InsertNextPoint(p2)
            pid3 = points.InsertNextPoint(p3)
            pid4 = points.InsertNextPoint(p4)

            quad = vtk.vtkQuad()
            quad.GetPointIds().SetId(0, pid1)
            quad.GetPointIds().SetId(1, pid2)
            quad.GetPointIds().SetId(2, pid3)
            quad.GetPointIds().SetId(3, pid4)

            line1 = vtk.vtkLine()
            line1.GetPointIds().SetId(0, pid1)
            line1.GetPointIds().SetId(1, pid2)

            line2 = vtk.vtkLine()
            line2.GetPointIds().SetId(0, pid2)
            line2.GetPointIds().SetId(1, pid3)

            line3 = vtk.vtkLine()
            line3.GetPointIds().SetId(0, pid3)
            line3.GetPointIds().SetId(1, pid4)

            line4 = vtk.vtkLine()
            line4.GetPointIds().SetId(0, pid4)
            line4.GetPointIds().SetId(1, pid1)

            polys.InsertNextCell(quad)

            lines.InsertNextCell(line1)
            lines.InsertNextCell(line2)
            lines.InsertNextCell(line3)
            lines.InsertNextCell(line4)

    # Create a polydata object
    geodata = vtk.vtkPolyData()
    linedata = vtk.vtkPolyData()

    # Set the points and vertices we created as the geometry and topology of the polydata
    geodata.SetPoints(points)
    geodata.SetPolys(polys)
    geodata.GetPointData().SetScalars(temps)

    linedata.SetPoints(points)
    linedata.SetLines(lines)

    return geodata, linedata, temps

def DisplaySurface(st):
    """
    Make and display the surface.
    :param: st - the surface to display.
    :return The vtkRenderWindowInteractor.
    """
    surface = st.upper()
    if not (surface in SURFACE_TYPE):
        print(st, "is not a surface.")
        iren = vtk.vtkRenderWindowInteractor()
        return iren
    # ------------------------------------------------------------
    # Create the surface, lookup tables, contour filter etc.
    # ------------------------------------------------------------
    # src = vtk.vtkPolyData()
    # src = Clipper(MakeParametricHills(), 0.5, 0.5, 0.0)
    # src = MakeParametricHills()
    src, linesrc, temps = MakeStrip(1001,101)

    # Here we are assuming that the active scalars are the curvatures.
    src.GetPointData().SetActiveScalars('Temps')
    scalarRange = src.GetScalarRange()

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
    bcf.SetInputData(src)
    # Use either the minimum or maximum value for each band.
    for i in range(0, numberOfBands):
        bcf.SetValue(i, bands[i][2])
    # We will use an indexed lookup table.
    bcf.SetScalarModeToIndex()
    bcf.GenerateContourEdgesOn()

    # ------------------------------------------------------------
    # Create the mappers and actors
    # ------------------------------------------------------------
    srcMapper = vtk.vtkPolyDataMapper()
    srcMapper.SetInputConnection(bcf.GetOutputPort())
    srcMapper.SetScalarRange(scalarRange)
    srcMapper.SetLookupTable(lut)
    srcMapper.SetScalarModeToUseCellData()

    srcActor = vtk.vtkActor()
    srcActor.SetMapper(srcMapper)

    lineMapper = vtk.vtkPolyDataMapper()
    lineMapper.SetInputData(linesrc)
    lineActor = vtk.vtkActor()
    lineActor.SetMapper(lineMapper)
    lineActor.GetProperty().SetColor(0, 0, 1)

    # Create contour edges
    edgeMapper = vtk.vtkPolyDataMapper()
    edgeMapper.SetInputData(bcf.GetContourEdgesOutput())
    edgeMapper.SetResolveCoincidentTopologyToPolygonOffset()

    edgeActor = vtk.vtkActor()
    edgeActor.SetMapper(edgeMapper)
    edgeActor.GetProperty().SetColor(0, 0, 0)




    # ------------------------------------------------------------
    # Create the RenderWindow, Renderer and Interactor
    # ------------------------------------------------------------
    ren = vtk.vtkRenderer()
    renWin = vtk.vtkRenderWindow()
    iren = vtk.vtkRenderWindowInteractor()

    renWin.AddRenderer(ren)
    iren.SetRenderWindow(renWin)

    # add actors
    ren.AddViewProp(srcActor)
    ren.AddViewProp(edgeActor)
    # ren.AddViewProp(lineActor)

    ren.SetBackground(0.7, 0.8, 1.0)
    renWin.SetSize(800, 800)
    renWin.Render()

    ren.GetActiveCamera().Zoom(1.5)

    return iren


if __name__ == '__main__':
    # iren = vtk.vtkRenderWindowInteractor()
    # iren = DisplaySurface("TORUS")
    # iren = DisplaySurface("PARAMETRIC_TORUS")
    iren = DisplaySurface("PARAMETRIC_HILLS")
    iren.Render()
    iren.Start()
# WritePNG(iren.GetRenderWindow().GetRenderers().GetFirstRenderer(),
#               "CurvatureBandsWithGlyphs.png")