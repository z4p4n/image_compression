#!/usr/bin/python3.4

# Image compression by wavelets
# D2: Haar wavelet
# z4p4n, NexMat

import numpy as np

#d2_1_inv = np.linalg.inv(d2_1);
#d2_2_inv = np.linalg.inv(d2_2);
#d2_3_inv = np.linalg.inv(d2_3);
#d2_4_inv = np.linalg.inv(d2_4);

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

def transfoD2_light(vect, matrix):
	res = np.dot(np.array(vect), matrix)
	return np.array(res).reshape(-1,).tolist()

def transformationD2(vect):
	vect = np.dot(vect, matrixD2(len(vect)));
	S = vect[0:len(vect)//2];
	D = vect[len(vect)//2:];

	return (S, D)

def compressionD2(vect):
	vect_tmp = vect;
	D_tab = [];

	while True:
		S, D = transformationD2(vect_tmp);
		D_tab += [D];
		if len(S) == 1:
			break;
		vect_tmp = S;

	return S, D_tab;

def compressionD2_inverse(S, D_tab):
	vect_tmp = np.array(S);
	for i in range(len(D_tab) - 1, -1, -1):
		S, D = transformationD2(vect_tmp);
		D_tab += [];
		if len(S) == 1:
			break;
		vect_tmp = S;

	return S, D_tab;

def transformationD2_inverse(vect):
	D2_inv = np.linalg.inv(matrixD2(len(vect)));
	vect = np.dot(vect, );
	S = vect[0:len(vect)//2];
	D = vect[len(vect)//2:];

	return (S, D)

if __name__ == '__main__':

	#print(matrixD2(2))
	#print(matrixD2(4))
	#print(matrixD2(6))
	#print(matrixD2(8))
	#rint(matrixD2(16))

	#S4, D1, D2, D3, D4 = transformationD2(vect);
	mat = matrixD2_light(16)
	vect = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 11, 11, 30, 30,  100]);
	print (np.dot (vect, mat))
	#S, D_tab = compressionD2(vect);
	#print(S, D_tab);
	#transformation_inverse(S4, D1, D2, D3, D4);
