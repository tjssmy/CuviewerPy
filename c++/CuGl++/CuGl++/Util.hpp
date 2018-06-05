//
//  Util.hpp
//  Atarpp
//
//  Created by tjsOrg on 2017-08-14.
//  Copyright © 2017 Tom Smy. All rights reserved.
//

/*! \file */

#ifndef Util_hpp
#define Util_hpp

#include <vector>
#include <algorithm>

#include <string>

#include <stdio.h>
#include <cstdlib>

//#include "boost/format.hpp"
//#include "Constants.h"

using namespace std;

extern FILE *logfile; /*!< Used to print log messages mirroring them to the log file and standard out. To write to this use the log_msg macro */
extern int silent; /*!<  Shuts all log output off */

typedef enum _DEBUG_LEVEL {
    DEBUG_OFF, DEBUG_ON, DEBUG_ON2
} DEBUG_LEVEL;

extern DEBUG_LEVEL DebugLevel;

void InitLog(string rootName);

void err_msg(int a, const char *b,...);
void log_msg(const char *b,...);
void debug_msg(int d,const char *b,...);
void warn_msg(const char *b, ...);


class VECTOR_2D {
public:
    double x,y;
    VECTOR_2D();
    VECTOR_2D(double xt, double yt);
    double abs();
    double cross(VECTOR_2D b);
    bool InsideReg(VECTOR_2D p0, VECTOR_2D p1);
    bool operator==(const VECTOR_2D &other) const;
    bool operator!=(const VECTOR_2D &other) const;
};

class VECTOR_3D {
public:
    double x,y,z;
    VECTOR_3D();
    VECTOR_3D(VECTOR_3D const & v);
    VECTOR_3D(double xt, double yt, double zt);
    VECTOR_3D(VECTOR_2D vt, double zt);
    double abs();
    double xyabs();
    VECTOR_3D cross(VECTOR_3D b);
    bool InsideReg(VECTOR_3D p0, VECTOR_3D p1);
    void operator=(VECTOR_2D a);
    bool operator==(const VECTOR_3D &other) const;
    bool operator!=(const VECTOR_3D &other) const;
};

VECTOR_2D operator+(VECTOR_2D a, VECTOR_2D b);
VECTOR_2D operator-(VECTOR_2D a, VECTOR_2D b);
VECTOR_2D operator*(VECTOR_2D a, VECTOR_2D b);

VECTOR_2D operator*(VECTOR_2D a, double b);
VECTOR_2D operator/(VECTOR_2D a, double b);
VECTOR_2D operator*(double b, VECTOR_2D a);
VECTOR_2D operator/(double b, VECTOR_2D a);

VECTOR_2D operator+(VECTOR_2D a, double b);
VECTOR_2D operator-(VECTOR_2D a, double b);
VECTOR_2D operator+(double b, VECTOR_2D a);
VECTOR_2D operator-(double b, VECTOR_2D a);

VECTOR_2D operator+(VECTOR_2D a, VECTOR_2D b);
VECTOR_2D operator-(VECTOR_2D a, VECTOR_2D b);
VECTOR_2D operator*(VECTOR_2D a, VECTOR_2D b);

VECTOR_2D operator*(VECTOR_2D a, double b);
VECTOR_2D operator/(VECTOR_2D a, double b);
VECTOR_2D operator*(double b, VECTOR_2D a);
VECTOR_2D operator/(double b, VECTOR_2D a);

VECTOR_2D operator+(VECTOR_2D a, double b);
VECTOR_2D operator-(VECTOR_2D a, double b);
VECTOR_2D operator+(double b, VECTOR_2D a);
VECTOR_2D operator-(double b, VECTOR_2D a);

VECTOR_2D AngularComp2D(double phi);

VECTOR_3D operator+(VECTOR_3D a, VECTOR_3D b);
VECTOR_3D operator-(VECTOR_3D a, VECTOR_3D b);
VECTOR_3D operator*(VECTOR_3D a, VECTOR_3D b);

VECTOR_3D operator*(VECTOR_3D a, double b);
VECTOR_3D operator/(VECTOR_3D a, double b);
VECTOR_3D operator*(double b, VECTOR_3D a);
VECTOR_3D operator/(double b, VECTOR_3D a);

VECTOR_3D operator+(VECTOR_3D a, double b);
VECTOR_3D operator-(VECTOR_3D a, double b);
VECTOR_3D operator+(double b, VECTOR_3D a);
VECTOR_3D operator-(double b, VECTOR_3D a);

VECTOR_3D operator+(VECTOR_3D a, VECTOR_3D b);
VECTOR_3D operator-(VECTOR_3D a, VECTOR_3D b);
VECTOR_3D operator*(VECTOR_3D a, VECTOR_3D b);

VECTOR_3D operator*(VECTOR_3D a, double b);
VECTOR_3D operator/(VECTOR_3D a, double b);
VECTOR_3D operator*(double b, VECTOR_3D a);
VECTOR_3D operator/(double b, VECTOR_3D a);

VECTOR_3D operator+(VECTOR_3D a, double b);
VECTOR_3D operator-(VECTOR_3D a, double b);
VECTOR_3D operator+(double b, VECTOR_3D a);
VECTOR_3D operator-(double b, VECTOR_3D a);

#define Zero3DV VECTOR_3D(0,0,0)
#define Zero2DV VECTOR_2D(0,0)

#define Nan3DV VECTOR_3D(nan(""),nan(""),nan(""))
#define Nan2DV VECTOR_3D(nan(""),nan(""))

class FVECTOR_2D {
public:
    float x,y;
    FVECTOR_2D();
    FVECTOR_2D(float x, float y);
};

class FVECTOR_3D {
public:
    float x,y,z;
    FVECTOR_3D();
    FVECTOR_3D(float x, float y, float z);
};

typedef struct triple_struct
{
    int i;
    int j;
    int k;
} TRIPLE_3D;

FVECTOR_3D Vector3Dto3F(VECTOR_3D v);

//template <typename T>
//const bool Contains( vector<T>& Vec, const T& Element );
template <typename T>
const bool Contains( vector<T>& Vec, const T& Element )
{
    if (find(Vec.begin(), Vec.end(), Element) != Vec.end())
        return true;
    
    return false;
}

#endif /* Util_hpp */
