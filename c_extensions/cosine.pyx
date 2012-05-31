from __future__ import division
import numpy as np
import math as m
cimport numpy as np
cimport cython

cdef extern from "math.h":
    double c_sqrt "sqrt"(double)

ctypedef np.float reals #typedef_for easier reading

@cython.boundscheck(False)
@cython.wraparound(False)
cdef inline double dot(np.ndarray[double] v1, np.ndarray[double] v2):
  cdef double result = 0
  cdef int i = 0
  cdef int length = v1.size
  cdef double el1 = 0
  cdef double el2 = 0
  for i in range(length):
    el1 = v1[i]
    el2 = v2[i]
    result += el1*el2
  return result
 
@cython.boundscheck(False)
@cython.wraparound(False)
@cython.cdivision(True)
def distance(np.ndarray[double, ndim = 1] ex1, np.ndarray[double, ndim = 1] ex2):
  cdef double dot12 = dot(ex1, ex2)
  cdef double dot11 = dot(ex1, ex1)
  cdef double dot22 = dot(ex2, ex2)
  cdef double sim = dot12 / (c_sqrt(dot11 * dot22))
  cdef double dist = 1-sim    
  return dist 