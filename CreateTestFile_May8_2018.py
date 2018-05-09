import numpy as np
import cuviewer
import WriteGLFile as w
import random

def write_points_scene(fid):
    w.WriteSceneBegin(fid, '100000 Points')
    w.WriteGLTag(fid, cuviewer.SPOINTMANY)
    w.WriteGLTag(fid, cuviewer.SFILL)

    for x in range(100000):
        p1 = [random.random(), random.random(),  random.random()]
        w.Write_GL_points_position(fid, p1)
        color = [1, 0, 0]
        w.Write_GL_points_color(fid, color)
    
    #for x in range(10000):
        #color = [1, 0, 0]
        #cuviewer.Write_GL_points_color(fid, color)

    w.WriteSceneEnd(fid)
    w.WriteCloseGLFile(fid)
    
def visualize(output_file):
    # Read and View
    vtkCuv = cuviewer.CreateVtkCuv()
    vtkCuv.ReadCuvFile(output_file)
    vtkCuv.SetRenderWin()
    vtkCuv.renderWindow.Render()
    vtkCuv.renderWindowInteractor.Start()
    
def main():
    # Create gl file
    output_file = 'Points.gl'
    fid = w.WriteInitGLFile(output_file)
    
    # Write some points in the GL file
    write_points_scene(fid)
    
    #Visualize the file just written
    visualize(output_file)


if __name__ == '__main__':
	main()
