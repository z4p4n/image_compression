#!/usr/bin/python3.4

# Image compression by wavelets
# D2: Haar wavelet
# z4p4n, NexMat

import numpy as np

d2_1 = np.array([
	[1/2, 0, 0, 0, 0, 0, 0, 0, 1/2, 0, 0, 0, 0, 0, 0, 0 ],
	[1/2, 0, 0, 0, 0, 0, 0, 0, -1/2, 0, 0, 0, 0, 0, 0, 0],
	[0, 1/2, 0, 0, 0, 0, 0, 0, 0, 1/2, 0, 0, 0, 0, 0, 0 ],
	[0, 1/2, 0, 0, 0, 0, 0, 0, 0, -1/2, 0, 0, 0, 0, 0, 0],
	[0, 0, 1/2, 0, 0, 0, 0, 0, 0, 0, 1/2, 0, 0, 0, 0, 0 ],
	[0, 0, 1/2, 0, 0, 0, 0, 0, 0, 0, -1/2, 0, 0, 0, 0, 0],
	[0, 0, 0, 1/2, 0, 0, 0, 0, 0, 0, 0, 1/2, 0, 0, 0, 0 ],
	[0, 0, 0, 1/2, 0, 0, 0, 0, 0, 0, 0, -1/2, 0, 0, 0, 0],
	[0, 0, 0, 0, 1/2, 0, 0, 0, 0, 0, 0, 0, 1/2, 0, 0, 0 ],
	[0, 0, 0, 0, 1/2, 0, 0, 0, 0, 0, 0, 0, -1/2, 0, 0, 0],
	[0, 0, 0, 0, 0, 1/2, 0, 0, 0, 0, 0, 0, 0, 1/2, 0, 0 ],
	[0, 0, 0, 0, 0, 1/2, 0, 0, 0, 0, 0, 0, 0, -1/2, 0, 0],
	[0, 0, 0, 0, 0, 0, 1/2, 0, 0, 0, 0, 0, 0, 0, 1/2, 0 ],
	[0, 0, 0, 0, 0, 0, 1/2, 0, 0, 0, 0, 0, 0, 0, -1/2, 0],
	[0, 0, 0, 0, 0, 0, 0, 1/2, 0, 0, 0, 0, 0, 0, 0, 1/2 ],
	[0, 0, 0, 0, 0, 0, 0, 1/2, 0, 0, 0, 0, 0, 0, 0, -1/2]], float);

vect = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 11, 11, 30, 30,  100]);

d2_2 = np.array([
    [1/2, 0, 0, 0, 1/2, 0, 0, 0 ],
    [1/2, 0, 0, 0, -1/2, 0, 0, 0],
    [0, 1/2, 0, 0, 0, 1/2, 0, 0 ],
    [0, 1/2, 0, 0, 0, -1/2, 0, 0],
    [0, 0, 1/2, 0, 0, 0, 1/2, 0 ],
    [0, 0, 1/2, 0, 0, 0, -1/2, 0],
    [0, 0, 0, 1/2, 0, 0, 0, 1/2 ],
    [0, 0, 0, 1/2, 0, 0, 0, -1/2]], float);

d2_3 = np.array([
    [1/2, 0, 1/2, 0 ],
    [1/2, 0, -1/2, 0],
    [0, 1/2, 0, 1/2 ],
    [0, 1/2, 0, -1/2]], float);

d2_4 = np.array([
    [1/2, 1/2 ],
    [1/2, -1/2]], float);

d2_1_inv = np.linalg.inv(d2_1);
d2_2_inv = np.linalg.inv(d2_2);
d2_3_inv = np.linalg.inv(d2_3);
d2_4_inv = np.linalg.inv(d2_4);


def transformationD2(vect):
    print("vect : ", vect);
    vect = np.dot(vect, d2_1);
    print("vect2: ", vect);
    S1 = vect[0:8];
    D1 = vect[8:];

    vect = np.dot(S1, d2_2);
    print("vect3: ", vect);
    S2 = vect[0:4];
    D2 = vect[4:];

    vect = np.dot(S2, d2_3);
    print("vect4: ", vect);
    S3 = vect[0:2];
    D3 = vect[2:];

    vect = np.dot(S3, d2_4);
    print("vect5: ", vect);
    S4 = vect[0:1];
    D4 = vect[1:];

    return (S4, D1, D2, D3, D4)

def transformation_inverse(S4, D1, D2, D3, D4):
    SD4 = np.concatenate((S4, D4), axis = 0);
    print("SD4: ", SD4);
    vect = np.dot(SD4, d2_4_inv);
    print("vect4: ", vect);

    SD3 = np.concatenate((vect, D3), axis = 0);
    print("SD3: ", SD3);
    vect = np.dot(SD3, d2_3_inv);
    print("vect3: ", vect);

    SD2 = np.concatenate((vect, D2), axis = 0);
    print("SD2: ", SD2);
    vect = np.dot(SD2, d2_2_inv);
    print("vect2: ", vect);

    SD1 = np.concatenate((vect, D1), axis = 0);
    print("SD1: ", SD1);
    vect = np.dot(SD1, d2_1_inv);
    print("vect1: ", vect);

def RGB_to_YUV():
    matrice = np.array(
            [ 0.299  ,  0.587  , 0.114   ],
            [-0.14713, -0.28886, 0.436   ],
            [ 0.299  , -0.51498, -0.10001]);

def YUV_to_RGB():
    matrice = np.array(
            [ 1,  0      ,  1.13983],
            [ 1, -0.39465, -0.58060],
            [ 1,  2.03211,  0      ]);
            
