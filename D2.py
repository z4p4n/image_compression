#!/usr/bin/python3.4

# Image compression by wavelets
# D2: Haar wavelet
# z4p4n, NexMat

import numpy as np

#d2_1_inv = np.linalg.inv(d2_1);
#d2_2_inv = np.linalg.inv(d2_2);
#d2_3_inv = np.linalg.inv(d2_3);
#d2_4_inv = np.linalg.inv(d2_4);

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
        D_tab += [[i for i in D]];
        if len(S) == 1:
            break;
        vect_tmp = S;

    return S, D_tab;


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
            
if __name__ == '__main__':

    #print(matrixD2(2))
    #print(matrixD2(4))
    #print(matrixD2(6))
    #print(matrixD2(8))
    #print(matrixD2(16))

    #S4, D1, D2, D3, D4 = transformationD2(vect);
    vect = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 11, 11, 30, 30,  100]);
    S, D_tab = compressionD2(vect);
    print(S, D_tab);

    #transformation_inverse(S4, D1, D2, D3, D4);
