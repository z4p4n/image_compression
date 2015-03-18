#!/usr/bin/python3.4

# Compresseur
# -> Décomposition de l'image par YUV
# -> Suppression des 4 premiers bits des deux octets U et V representant la chrominance
#
# z4p4n, NexMat

import sys
from img_compute import *
from D2 import *

if __name__ == '__main__':

	# Lecture des parametres
	try:
		mode = sys.argv[1]
		img_name = sys.argv[2]
	except:
		print ("Usage: ...")
		exit ()

	(width, height), Y, U, V = read_image(img_name);

	# On enleve l'extension
	img_name = '.'.join(img_name.split('.')[:-1])

	# Suppression des 4 premiers bits des deux octets U et V
	if mode == "-c" :

		for i in range (width * height) :
			Y[i], U[i], V[i] = YUV_to_byte (Y[i], U[i], V[i])

		# Ecrase les 4 premier bits de poids faible
		for i in range (width * height) :
			U[i] &= 0xF8
			V[i] &= 0xF8

		for i in range (width * height) :
			Y[i], U[i], V[i] = byte_to_YUV (Y[i], U[i], V[i])

		create_image (img_name + "_precompressed", width, height, Y, U, V)

	# Option separation des Y, U et V
	elif mode == "-s":
		emptymat = [0 for i in range(len(Y))];

		# Creation des trois images
		create_image("YUV" + img_name + "_Y", width, height, Y, emptymat, emptymat)
		create_image("YUV" + img_name + "_U", width, height, emptymat, U, emptymat)
		create_image("YUV" + img_name + "_V", width, height, emptymat, emptymat, V)

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
