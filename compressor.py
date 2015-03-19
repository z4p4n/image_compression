#!/usr/bin/python3.4

# Compresseur
# -> Décomposition de l'image par YUV
# -> Suppression des 4 premiers bits des deux octets U et V representant la chrominance
#
# z4p4n, NexMat

import getopt, sys
from img_compute import *
from D2 import *

def cutfirstbit (Y, U, V, width, height, n, img_name):

	for i in range (width * height) :
		Y[i], U[i], V[i] = YUV_to_byte (Y[i], U[i], V[i])

	# Ecrase les n premier bits de poids faible
	for i in range (width * height) :
		U[i] &= (0xFF >> n) << n
		V[i] &= (0xFF >> n) << n

	for i in range (width * height) :
		Y[i], U[i], V[i] = byte_to_YUV (Y[i], U[i], V[i])

	create_image (img_name + "_cut" + str (n) + "bit", width, height, Y, U, V, True)

def splitYUV (Y, U, V, width, height, img_name):

	emptymat = [0 for i in range(len(Y))];

	# Creation des trois images
	create_image("YUV/" + img_name + "_Y", width, height, Y, emptymat, emptymat, True)
	create_image("YUV/" + img_name + "_U", width, height, emptymat, U, emptymat, True)
	create_image("YUV/" + img_name + "_V", width, height, emptymat, emptymat, V, True)

def usage ():
	print ("Usage: TODO")

if __name__ == '__main__':

	# Recuperation des parametres
	try:
		opts, args = getopt.getopt(sys.argv[1:], "f:hyc:s", ["help"])
	except getopt.GetoptError as err:
		print (str(err))
		usage ()
		sys.exit (2)

	yuv = False
	cut = 0
	mode = ''
	img_name = ''

	# lecture des parametres
	for o, a in opts:

		if o == "-y":
			yuv = True

		elif o in ("-h", "--help"):
			usage()
			sys.exit(1)

		elif o == "-c":
			mode = "c"
			yuv = True
			cut = int (a)

		elif o == "-s":
			mode = "s"
			yuv = True

		elif o == "-f":
			img_name = a

	# Si il n'y a pas de fichier a lire ou pas d'option tout simplement
	if img_name == '' or mode == '':
		usage()
		sys.exit(2)

	# lecture de l'image
	(width, height), X, Y, Z = read_image(img_name, yuv);

	# On enleve l'extension du nom de l'image
	img_name = '.'.join(img_name.split('.')[:-1])

	# Suppression des X premiers bits des deux chromatiques
	if mode == "c" :
		cutfirstbit (X, Y, Z, width, height, cut, img_name)

	# Option separation des Y, U et V
	elif mode == "s":
		splitYUV (X, Y, Z, width, height, img_name)

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
