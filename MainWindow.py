from PyQt4 import QtCore, QtGui
from vtk.qt4.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
#from PyQt4.QtCore import QThread
#from PyQt4.QtCore import QObject, pyqtSignal, pyqtSlot
import display
import vtk


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

        self.CreateSceneMappersAndActors()

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

    def ReReadFile(self):
        self.RemoveActors()
        self.ReadCuvFile()
        self.CreateSceneMappersAndActors()
        self.AddActors()
        self.ReDraw()

    def ResetArrowGlyphScale(self,sc):
        for s in self.scenes:
            s.ResetArrowGlyphScale(sc)

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