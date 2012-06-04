from __future__ import division
import numpy as np
cimport numpy as np
cimport cython

@cython.boundscheck(False)
@cython.wraparound(False)
def dot(np.ndarray[double, ndim=1] v1, np.ndarray[double, ndim=1] v2):
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
 