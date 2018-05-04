#!/usr/local/bin/python3

import cuviewer
import sys
import argparse

def main(input_file):
	vtkCuv = cuviewer.CreateVtkCuv()
	vtkCuv.ReadCuvFile(input_file)
	vtkCuv.SetRenderWin()
	vtkCuv.renderWindow.Render()
	vtkCuv.renderWindowInteractor.Start()

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('-f', 
						'--file',
						action = 'store',
						dest='input_file',
						help = 'file to visualize')
	args = parser.parse_args()
	if args.input_file is None:
		print("Please provide an input file!")
	else:
		main(args.input_file)
