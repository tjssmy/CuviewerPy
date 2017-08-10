# CuviewerPy
Python implementation of CuViewer using VTK 

##Description

A Python 3.0 implementation of CuViewer using VTK. The original CuViewer was QT and opengl based 3D viewer. It reads formatted binary files and displays basic geometric entities such as lines, triangles, quadrilaterals, spheres and ellipsoids. The original viewer has quite a lot of functionality, such as grouping entities in scenes, contour plotting, standard views, etc. 

This Python implementation uses VTK and is intended as replacement (I hope) for the somewhat archaic QT version. 

##Current Status:

Basic implementation:

1) Cuviewer File reading/writing
2) VTK rendering of geometry in raw VTK window  
3) Scenes can be toggled on and off
5) Keyboard capture of commands for functionality
4) Contouring is enabled
6) Standard views - perspective and orthogonal views

## use
python3 CuViewerPy.py

##Functionality

Key board commands:
	s: Toggle screen visibility. Command sequence: s <scene number> s
	a: Draw all scenes
	n: Don't draw any scenes
	p: toggle perspective view
	rlfbfud: Standard views
		r: right side
		l: left side
		f: front side
		b: back side
		u: bottom side
		d: top side
	o: Outline polys
	c: Create contours
	i: Print scene info.

##Instalation

Install python3 
Install VTK with python bindings
Make sure cuviewer.py is on PYTHONPATH

###OSX

I used homebrew to install python3 and VTK --with-python3 

###Windows

TBA

###Linux

TBA