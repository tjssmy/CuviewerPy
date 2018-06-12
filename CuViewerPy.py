#!/usr/local/bin/python3

import CuViewer
import sys
import argparse
from PyQt4 import QtGui
import MainWindow


def main():
    #vtkCuv = CuViewer.CreateVtkCuv()
    #vtkCuv.ReadCuvFile(input_file)
    app = QtGui.QApplication(sys.argv)
    window = MainWindow.MainWindow()
    #vtkCuv.SetRenderWin()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f',
                        '--file',
                        action='store',
                        dest='input_file',
                        help='file to visualize')
    args = parser.parse_args()
    if args.input_file is None:
        #print("Please provide an input file!")
        main()
    #else:
        #main(args.input_file)
