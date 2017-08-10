import cuviewer
import sys

if len(sys.argv) != 2:
    print("wrong")
    exit()

input_file = sys.argv[1]

vtkCuv = cuviewer.CreateVtkCuv()
vtkCuv.ReadCuvFile(input_file)
vtkCuv.SetRenderWin()
vtkCuv.renderWindow.Render()
vtkCuv.renderWindowInteractor.Start()

