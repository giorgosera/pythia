from __future__ import division
import numpy as np
cimport numpy as np
cimport cython
import nltk
from libcpp.vector cimport vector

ctypedef np.float reals #typedef_for easier readding

@cython.boundscheck(False)
@cython.wraparound(False)
def distance(np.ndarray v1, np.ndarray v2):
	cdef vector[int] indices1
	cdef vector[int] indices2
	
	cdef int length = v1.size
	
	cdef int i = 0
	for element in v1:
		if element == 1: indices1.push_back(i)
		i += 1
	
	cdef int j = 0
	for element in v2:
		if element == 1: indices2.push_back(j)
		j += 1
	
	cdef int intersection = 0
	for i in range(length):
		for j in range(length):
			if indices1[i] == indices2[j]: intersection += 1 
	cdef int union = length + length
	cdef double dist = (union -  intersection)/union
	return dist