#!/usr/bin/python3.4

# Compresseur
# -> Suppression des 4 premiers bits des deux octets U et V representant la chrominance
#
# z4p4n, NexMat

import sys
from PIL import Image

if __name__ == '__main__':

    # Lecture des parametres
    try:
        mode = sys.argv[1]
        img_name = sys.argv[2]
    except:
        print ("Usage: ...")
        exit ()

    (width, height), Y, U, V = read_image(img_name);


    # Suppression des 4 premiers bits des deux octets U et V
    if mode == "-c" :

	for i in range (width * height) :
            U[i] &= 0xF0
            V[i] &= 0xF0

	create_image (img_name, width, height, Y, U, V)

    #(width, height), Y, U, V = read_image ("imagerouge.bmp")
    
    # On garde la plus grande valeur sans le reste % 16
    #size = width * height - (width * height % 16);
    #vect = np.array(Y[0:16], float);

    #S4, D1, D2, D3, D4 = transformationD2(vect);
    #transformation_inverse(S4, D1, D2, D3, D4);
    #for i in range (size / 16) :
    #    vect = np.array(Y[i*16:i*16+16], float)

    #vect = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 11, 11, 30, 30,  100]);
    #transformationD2(vect);
    #vect2 = transformationD2(vect);
    #vect1 = transformation_inverse(vect2);
    #prine);
    #print("vect2 >>>", vect2);
    #print("re vect1 >>>", vect1);
