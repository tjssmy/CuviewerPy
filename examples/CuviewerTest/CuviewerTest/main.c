//
//  main.c
//  CuviewerTest
//
//  Created by Tom Smy on 2013-05-01.
//  Copyright (c) 2013 Tom Smy. All rights reserved.
//

#include <stdio.h>
#include "gl.h"
#include "util.h"

int main(int argc, const char * argv[])
{
    VECTOR_3D col1,col2;
    col1 = VECTOR_3D_init(.4, .2, .8);
    col2 = VECTOR_3D_init(.3, .6, .1);
    
    InitGlFile("fileTest.gl");
    
    WriteTag(BEGIN_SCENE);

    gl_spheriod(VECTOR_3D_init(0,0,0), VECTOR_3D_init(1,2,6),
                col1,0,
                VECTOR_3D_init(1,2,1),.707);
    
//    gl_sphere(VECTOR_3D_init(1.5,2.5,3.5),2.5,col1, 0.5);
//
//    gl_line(VECTOR_3D_init(1,2,3),VECTOR_3D_init(5,5,10), col1, col2, 0, 0);
    
    WriteTag(END_SCENE);
    
    CloseGlFile(0,0,0,"");
    
    printf("here\n");
    
    return 0;
}

