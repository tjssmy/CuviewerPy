//
//  main.cpp
//  CuGl++
//
//  Created by tjsOrg on 2018-06-05.
//  Copyright © 2018 Tom Smy. All rights reserved.
//

#include <iostream>
#include "gl.hpp"

int main(int argc, const char * argv[]) {

    CuViewer *cuviewModel  = new CuViewer(string("TestModel.gl"));
    cuviewModel->BeginScene("Geometry");
    
    FVECTOR_3D v1(0,0,0);
    FVECTOR_3D v2(0,1,0);
    FVECTOR_3D v3(0,1,0.5);
    FVECTOR_3D v4(1,0,0);
    
    FVECTOR_3D col[4];
    col[0] = FVECTOR_3D(1,0,0);
    col[1] = FVECTOR_3D(1,1,0);
    col[2] = FVECTOR_3D(1,0,1);
    col[3] = FVECTOR_3D(0,1,1);
    
    cuviewModel->gl_quad(v1,v2,v3,v4,col[0],col[1],col[2],col[3],0,1,1,0);
    
    cuviewModel->EndScene();
    
    cuviewModel->CloseGlFile(0,0,0,string(""));
    
    return 0;
}
