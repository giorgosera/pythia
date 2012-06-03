import numpy as np
cimport numpy as np
cimport cython
  
@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
def resize(np.ndarray[double, ndim=1] old_center, term_dict, new, old):
  cdef int length = len(new)
  cdef np.ndarray[double, ndim=1] new_center = np.zeros([length])
  cdef list new_vector = length*[None]

  cdef int new_index, old_index = 0
  cdef unicode term
  cdef double old_value 
  for i in xrange(length):
    term = new[i]
    if term in old: 
      old_index = term_dict[term]
      old_value = old_center[old_index]
      new_center[new_index] = old_value
      new_vector[new_index] = term
    else:
      new_vector[new_index] = term
    new_index += 1      
  return new_center, new_vector