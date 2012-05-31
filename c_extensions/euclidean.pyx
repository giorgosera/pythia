from __future__ import division
import numpy as np
cimport numpy as np
cimport cython

cdef extern from "math.h":
    double c_sqrt "sqrt"(double)
 
@cython.boundscheck(False)
@cython.wraparound(False)
@cython.cdivision(True)
def distance(np.ndarray[double, ndim = 1] ex1, np.ndarray[double, ndim = 1] ex2):
  cdef int length = ex1.size
  
  cdef double sum = 0
  cdef double el1 = 0
  cdef double el2 = 0
  for i in range(length):
    el1 = ex1[i]
    el2 = ex2[i]
    sum += (el1-el2)*(el1-el2)

  cdef double dist = c_sqrt(sum)
  return dist 