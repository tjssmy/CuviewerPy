//
//  Util.cpp
//  Atarpp
//
//  Created by tjsOrg on 2017-08-14.
//  Copyright © 2017 Tom Smy. All rights reserved.
//

#include <stdio.h>
#include <stdlib.h>
#include <cmath>

#include "Util.hpp"

FILE *logfile;
int silent;
DEBUG_LEVEL DebugLevel;

void InitLog(string rootName)
{
    char const *logname = (rootName + string(".log")).c_str();
    
    if ((logfile=fopen(logname,"w")) == NULL)
    {
        fprintf(stderr,"could not open log file\n");
        exit(1);
    }

}

FVECTOR_2D::FVECTOR_2D()
{
    x = 0.0;
    y = 0.0;
};

FVECTOR_2D::FVECTOR_2D(float xi, float yi)
{
    x = xi;
    y = yi;
};

FVECTOR_3D::FVECTOR_3D()
{
    x = 0.0;
    y = 0.0;
    z = 0.0;
};

FVECTOR_3D::FVECTOR_3D(float xi, float yi, float zi)
{
    x = xi;
    y = yi;
    z = zi;
};


FVECTOR_3D Vector3Dto3F(VECTOR_3D v){
    FVECTOR_3D f = {float(v.x),float(v.y),float(v.z)};
    return f;
}

FVECTOR_2D Vector2Dto2F(VECTOR_2D v){
    FVECTOR_2D f = {float(v.x),float(v.y)};
    return f;
}

VECTOR_2D::VECTOR_2D(){ x = 0; y = 0;}

VECTOR_2D::VECTOR_2D(double xt, double yt)
{
    x = xt; y = yt;
}

bool VECTOR_2D::InsideReg(VECTOR_2D p0, VECTOR_2D p1)
{
    if (x >= p0.x && x <= p1.x &&
        y >= p0.y && y <= p1.y) return true;
    else return false;
}

VECTOR_2D operator/(VECTOR_2D a, double b){
    VECTOR_2D r; r.x = a.x/b; r.y = a.y/b;;
    return r;
}

VECTOR_2D operator*(VECTOR_2D a, VECTOR_2D b){
    VECTOR_2D r; r.x = a.x*b.x; r.y = a.y*b.y;
    return r;
}

VECTOR_2D operator*(VECTOR_2D a, double b){
    VECTOR_2D r; r.x = a.x*b; r.y = a.y*b;
    return r;
}

VECTOR_2D operator*(double b, VECTOR_2D a){
    VECTOR_2D r; r.x = a.x*b; r.y = a.y*b;
    return r;
}

VECTOR_2D operator+(VECTOR_2D a, VECTOR_2D b){
    VECTOR_2D r; r.x = a.x+b.x; r.y = a.y+b.y;
    return r;
}

VECTOR_2D operator+(VECTOR_2D a, double b){
    VECTOR_2D r; r.x = a.x+b; r.y = a.y+b;
    return r;
}

VECTOR_2D operator+(double b, VECTOR_2D a){
    VECTOR_2D r; r.x = a.x+b; r.y = a.y+b;
    return r;
}

VECTOR_2D operator-(VECTOR_2D a, VECTOR_2D b){
    VECTOR_2D r; r.x = a.x-b.x; r.y = a.y-b.y;
    return r;
}

VECTOR_2D operator-(VECTOR_2D a, double b){
    VECTOR_2D r; r.x = a.x-b; r.y = a.y-b;
    return r;
}

VECTOR_2D operator-(double b, VECTOR_2D a){
    VECTOR_2D r; r.x = b-a.x; r.y = b-a.y;
    return r;
}

double VECTOR_2D::abs(){
    return sqrt(x*x + y*y);
}

double VECTOR_2D::cross(VECTOR_2D b){
    double r;
    r = x*b.y - y*b.x;
    return r;
}

bool VECTOR_2D::operator==(const VECTOR_2D &other) const
{
    if (x == other.x && y == other.y) return true;
    else return false;
}

bool VECTOR_2D::operator!=(const VECTOR_2D &other) const
{
    return !(*this == other);
}

VECTOR_2D AngularComp2D(double phi)
{
    VECTOR_2D comp;
    comp.x = cos(phi);
    comp.y = sin(phi);
    
    return comp;
}

VECTOR_3D::VECTOR_3D(){ x = 0; y = 0; z = 0; }

VECTOR_3D::VECTOR_3D(VECTOR_3D const &v){
    x = v.x;
    y = v.y;
    z = v.z;
}

VECTOR_3D::VECTOR_3D(VECTOR_2D vt, double zt)
{
    x = vt.x;
    y = vt.y;
    z = zt;
}

void VECTOR_3D::operator=(VECTOR_2D b)
{
    x = b.x;
    y = b.y;
    z = 0;
}

VECTOR_3D::VECTOR_3D(double xt, double yt, double zt)
{
    x = xt; y = yt; z = zt;
}

bool VECTOR_3D::InsideReg(VECTOR_3D p0, VECTOR_3D p1)
{
    if (x >= p0.x && x <= p1.x &&
        y >= p0.y && y <= p1.y &&
        z >= p0.z && z <= p1.z) return true;
    else return false;
}

VECTOR_3D operator/(VECTOR_3D a, double b){
    VECTOR_3D r; r.x = a.x/b; r.y = a.y/b; r.z = a.z/b;
    return r;
}

VECTOR_3D operator*(VECTOR_3D a, VECTOR_3D b){
    VECTOR_3D r; r.x = a.x*b.x; r.y = a.y*b.y; r.z = a.z*b.z;
    return r;
}

VECTOR_3D operator*(VECTOR_3D a, double b){
    VECTOR_3D r; r.x = a.x*b; r.y = a.y*b; r.z = a.z*b;
    return r;
}

VECTOR_3D operator*(double b, VECTOR_3D a){
    VECTOR_3D r; r.x = a.x*b; r.y = a.y*b; r.z = a.z*b;
    return r;
}


VECTOR_3D operator+(VECTOR_3D a, VECTOR_3D b){
    VECTOR_3D r; r.x = a.x+b.x; r.y = a.y+b.y; r.z = a.z+b.z;
    return r;
}

VECTOR_3D operator+(VECTOR_3D a, double b){
    VECTOR_3D r; r.x = a.x+b; r.y = a.y+b; r.z = a.z+b;
    return r;
}

VECTOR_3D operator+(double b, VECTOR_3D a){
    VECTOR_3D r; r.x = a.x+b; r.y = a.y+b; r.z = a.z+b;
    return r;
}

VECTOR_3D operator-(VECTOR_3D a, VECTOR_3D b){
    VECTOR_3D r; r.x = a.x-b.x; r.y = a.y-b.y; r.z = a.z-b.z;
    return r;
}

VECTOR_3D operator-(VECTOR_3D a, double b){
    VECTOR_3D r; r.x = a.x-b; r.y = a.y-b; r.z = a.z-b;
    return r;
}

VECTOR_3D operator-(double b, VECTOR_3D a){
    VECTOR_3D r; r.x = b-a.x; r.y = b-a.y; r.z = b-a.z;
    return r;
}


double VECTOR_3D::abs(){
    return sqrt(x*x + y*y +z*z);
}

double VECTOR_3D::xyabs(){
    return sqrt(x*x + y*y);
}



VECTOR_3D VECTOR_3D::cross(VECTOR_3D b){
    VECTOR_3D r;
    r.x = y*b.z - z*b.y;
    r.y = z*b.x - x*b.z;
    r.z = x*b.y - y*b.x;
    return r;
}

bool VECTOR_3D::operator==(const VECTOR_3D &other) const
{
    if (x == other.x && y == other.y && z == other.z) return true;
    else return false;
}

bool VECTOR_3D::operator!=(const VECTOR_3D &other) const
{
    return !(*this == other);
}

void err_msg(int a,         /*!< Exit code */
             const char *b, /*!< Format string (c-type) */
        ...)                /*!< Variable number of arguments*/

{
    
    /** Used to log warning messages to both stderr and the log file. Mirrors a standard *C* fprintf, using a variable number of arguments and a format string. The error code is then used for a call to exit().
     
     Input Parameters:
     */

    va_list argptr;
    va_start(argptr, b);
    vfprintf(stderr, b, argptr);
    va_end(argptr);
    fflush(stderr);
    
    if (logfile!=NULL){
        va_list argptr;
        va_start(argptr, b);
        vfprintf(logfile, b, argptr);
        va_end(argptr);
        fflush(logfile);
        fflush(logfile); exit(a);
    }
}


void warn_msg(const char *b,/*!<  Format string (c-type) */
              ...)          /*!< Variable number of arguments*/
{
    /** Used to log messages to both stderr and the log file. Mirrors a standard *C* fprintf, using a variable number of arguments and a format string.
     */

    if (!silent) {
        va_list argptr;
        va_start(argptr, b);
        vfprintf(stdout, b, argptr);
        va_end(argptr);
        fflush(stdout);
    }
    if (logfile!=NULL) {
        va_list argptr;
        va_start(argptr, b);
        vfprintf(logfile, b, argptr);
        va_end(argptr);
        fflush(logfile);
    }
}

void log_msg(const char *b, /*!< Format string (c-type) */
             ...)           /*!< Variable number of arguments*/
{
    /** Used to log messages to both stdout and the log file. Mirrors a standard *C* fprintf, using a variable number of arguments and a format string.
     */

    if (!silent )
    {
        va_list argptr;
        va_start(argptr, b);
        vfprintf(stdout, b, argptr);
        va_end(argptr);
        fflush(stdout);
        if (logfile!=NULL){
            va_start(argptr, b);
            vfprintf(logfile, b, argptr);
            va_end(argptr);
            fflush(logfile);
        }
    }
}


void debug_msg(int d,        /*!< debug level to output for */
               const char *b,/*!< Format string (c-type) */
               ...          /*!< Variable number of arguments*/ )
{
    /** Used to log debug messages to both stderr and the log file. Mirrors a standard *C* fprintf, using a variable number of arguments and a format string. Checks that DebugLevel is greater then the input parameter d prior to pringint.
     */

    if (!silent && DebugLevel >= d){
        va_list argptr;
        va_start(argptr, b);
        vfprintf(stdout, b, argptr);
        va_end(argptr);
        fflush(stdout);
    }
    if (logfile!=NULL && DebugLevel >= d){
        va_list argptr;
        va_start(argptr, b);
        vfprintf(logfile, b, argptr);
        va_end(argptr);
        fflush(stdout);
        
    }
}
