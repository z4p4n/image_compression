#!/usr/bin/python3.4

# Image compression by wavelets
# DN: Any wavelet
# z4p4n, NexMat

import numpy as np
import math

def matrixDN_inv (matrix):
	return np.linalg.inv(matrix);

def matrixDN(N, size):
	if N == 4: return matrixD4(size);
	elif N == 2: return matrixD2(size);
	else: return None

def matrixDN_light(N, size):
	if N == 4: return matrixD4_light(size);
	elif N == 2: return matrixD2_light(size);
	else: return None

def matrixD4_light(size):
	# Creation de la matrice des ondelettes de Daubechies

	if size < 4:
		return None;

	h0 = (1 + math.sqrt(3)) / (4 * math.sqrt(2))
	h1 = (3 + math.sqrt(3)) / (4 * math.sqrt(2))
	h2 = (3 - math.sqrt(3)) / (4 * math.sqrt(2))
	h3 = (1 - math.sqrt(3)) / (4 * math.sqrt(2))

	matrix = []
	for i in range(size):
		line = [0 for i in range(size)]
		for j in range(size):
			if j == (i * 2) % size :
				line[j] = h0
			elif j == (i * 2 + 1) % size:
				line[j] = h1
			elif j == (i * 2 + 2) % size:
				line[j % size] = h2
			elif j == (i * 2 + 3) % size:
				line[j % size] = h3
			else:
				line[j] = 0
		matrix.append(line)

	matrix = np.array(matrix, float)
	return np.transpose(matrix, axes = None)
	return matrix

def matrixD4(size):
	# Creation de la matrice des ondelettes de Daubechies

	if size < 4:
		return None;

	h0 = (1 + math.sqrt(3)) / (4 * math.sqrt(2))
	h1 = (3 + math.sqrt(3)) / (4 * math.sqrt(2))
	h2 = (3 - math.sqrt(3)) / (4 * math.sqrt(2))
	h3 = (1 - math.sqrt(3)) / (4 * math.sqrt(2))
	g0 =  h3
	g1 = -h2
	g2 =  h1
	g3 = -h0

	#h0, h3 = h3, h0
	#h1, h2 = h2, h1
	#g0 = -h3
	#g1 = h2
	#g2 = -h1
	#g3 = h0

	matrix = []
	for i in range(size//2):
		line = [0 for i in range(size)]
		for j in range(size):
			if j == (i * 2) % size :
				line[j] = h0
			elif j == (i * 2 + 1) % size:
				line[j] = h1
			elif j == (i * 2 + 2) % size:
				line[j % size] = h2
			elif j == (i * 2 + 3) % size:
				line[j % size] = h3
			else:
				line[j] = 0
		matrix.append(line)

	for i in range(size//2, size):
		line = [0 for i in range(size)]
		for j in range(size):
			if j == (i * 2) % size :
				line[j] = g0
			elif j == (i * 2 + 1) % size:
				line[j] = g1
			elif j == (i * 2 + 2) % size:
				line[j % size] = g2
			elif j == (i * 2 + 3) % size:
				line[j % size] = g3
			else:
				line[j] = 0
		matrix.append(line)


	matrix = np.array(matrix, float)
	return np.transpose(matrix)

def matrixD2_light (size):
	# Creation de la matrice des ondelettes de Haar allegee

	matrix = []
	for i in range (size):
		line = []
		for j in range (size//2):
			if j < size/2 and i//2 == j:
				line.append(1/2)
			else :
				line.append(0)
		matrix.append (line)

	return np.array (matrix, float)


def matrixD2 (size):
	# Creation de la matrice des ondelettes de Haar

	matrix = []
	for i in range (size):
		line = []
		for j in range (size):
			if j < size/2 and i//2 == j:
				line.append(1/2)
			elif j >= size/2 and (i%2 == 0) and (i//2 == j-size/2) :
				line.append(1/2)
			elif j >= size/2 and (i%2 == 1) and (i//2 == j-size/2) :
				line.append(-1/2)
			else :
				line.append(0)
		matrix.append (line)

	return np.array (matrix, float)

def transfoDN_light(vect, matrix):
	res = np.dot(np.array(vect), matrix)
	return np.array(res).reshape(-1,).tolist()

def transfoDN(vect, matrix):
	vect = np.dot(vect, matrix);
	S = np.array(vect[0:len(vect)//2]).reshape(-1,).tolist()
	D = np.array(vect[len(vect)//2:]).reshape(-1,).tolist()
	return (S, D)


if __name__ == '__main__':

	mat = matrixD4(16)
	for i in mat:
		for j in i:
			print(j, end = " ")
		print()
	#vect = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]);
	#vect = np.array([4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]); 
	#vect = np.array([20 * i for i in range(16)], float)
	#mat = matrixD4(16)
	#vect2 = np.dot(vect, mat)
	#print(vect2)
	#mat_inv = np.linalg.inv(mat)
	#print(np.dot(vect2, mat_inv))
	#mat = matrixD4(16)
	#print(mat)
