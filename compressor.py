#!/usr/bin/python3.4

# Compresseur
# -> Décomposition de l'image par YUV
# -> Suppression des 4 premiers bits des deux octets U et V representant la chrominance
#
# z4p4n, NexMat

import numpy as np
import getopt, sys
from img_compute import *
from D2 import *

def divide (X, Y, Z, width, height, img_name, deflate, yuv) :

	i = 2
	# On divise l'image tant qu'on peut
	while (width > 16 and height > 16) :
		print ("[+] Divide image per " + str (i))
		i += 1
		(X, Y, Z, width, height) = divide_img (X, Y, Z, width, height, img_name + "_" + str(i), deflate, yuv)

def divide_img (X, Y, Z, width, height, img_name, deflate, yuv) :

	# Pour le moment on fait facile modulo 16 bits TODO
	new_width  = width  - width % 16
	new_height = height - height % 16

	# Creation de la matrice D2
	matrix = matrixD2_light(16)

	# On divise l'image dans le sens de la largeur avec D2
	Xres = [[] for i in range (height)]
	Yres = [[] for i in range (height)]
	Zres = [[] for i in range (height)]

	print ("[+] Apply D2 on image - horizontaly")
	for j in range (height) :
		for i in range (0, new_width, 16) :

			Xres[j].extend (transfoD2_light (X[j][i:i+16], matrix))
			Yres[j].extend (transfoD2_light (Y[j][i:i+16], matrix))
			Zres[j].extend (transfoD2_light (Z[j][i:i+16], matrix))
		if j % 100 == 0 : print ("[!] processing... " + str (j) + "/" + str(height) + "  ")

	new_width = new_width // 2
	# On divise l'image dans le sens de la hauteur avec D2
	print ("[+] Apply D2 on image - verticaly")
	Xres2 = [[0 for i in range (new_width)] for j in range (new_height//2)]
	Yres2 = [[0 for i in range (new_width)] for j in range (new_height//2)]
	Zres2 = [[0 for i in range (new_width)] for j in range (new_height//2)]

	for i in range (new_width) :
		for j in range (0, new_height, 16) :

			s = transfoD2_light ([Xres[j+k][i] for k in range (0, 16)], matrix)
			for k in range (8): Xres2[j//2+k][i] = s[k]
			s = transfoD2_light ([Yres[j+k][i] for k in range (0, 16)], matrix)
			for k in range (8): Yres2[j//2+k][i] = s[k]
			s = transfoD2_light ([Zres[j+k][i] for k in range (0, 16)], matrix)
			for k in range (8): Zres2[j//2+k][i] = s[k]

		if i % 100 == 0 : print ("[!] processing... " + str (i) + "/" + str(new_width) + "  ")

	new_height = new_height // 2
	print ("[+] Create new image " + str(new_width) + "x" + str(new_height))
	create_image ("Divide/" + img_name + "_div", new_width, new_height, Xres2, Yres2, Zres2, yuv)

	return (Xres2, Yres2, Zres2, new_width, new_height)

def cutfirstbit (Y, U, V, width, height, n, img_name):

	print ("[+] convert YUV to byte")
	for i in range (width) :
		for j in range (height) :
			Y[i][j], U[i][j], V[i][j] = YUV_to_byte (Y[i][j], U[i][j], V[i][j])

	# Ecrase les n premier bits de poids faible
	print ("[+] erase " + n + " first bit(s)")
	for i in range (width * height) :
		U[i] &= (0xFF >> n) << n
		V[i] &= (0xFF >> n) << n

	print ("[+] convert byte to YUV")
	for i in range (width) :
		for j in range (height) :
			Y[i][j], U[i][j], V[i][j] = byte_to_YUV (Y[i][j], U[i][j], V[i][j])

	print ("[+] Create cuted image")
	create_image (img_name + "_cut" + str (n) + "bit", width, height, Y, U, V, True)

def splitYUV (Y, U, V, width, height, img_name):

	print ("[+] Create empty matrix")
	emptymat = [[0 for i in range(width)] for j in range (height)];

	# Creation des trois images
	print ("[+] Create Y version")
	create_image("YUV/" + img_name + "_Y", width, height, Y, emptymat, emptymat, True)
	print ("[+] Create U version")
	create_image("YUV/" + img_name + "_U", width, height, emptymat, U, emptymat, True)
	print ("[+] Create V version")
	create_image("YUV/" + img_name + "_V", width, height, emptymat, emptymat, V, True)

def usage ():
	print ("Usage: TODO")

if __name__ == '__main__':

	# Recuperation des parametres
	try:
		opts, args = getopt.getopt(sys.argv[1:], "df:hyc:s", ["help", "d2"])
	except getopt.GetoptError as err:
		print (str(err))
		usage ()
		sys.exit (2)

	yuv = False
	cut = 0
	mode = ''
	img_name = ''
	deflate = 'd2'

	# lecture des parametres
	for o, a in opts:

		# Lecture en mode YUV
		if o == "-y":
			yuv = True

		# Permet d'afficher l'aide
		elif o in ("-h", "--help"):
			usage()
			sys.exit(1)

		# Mode de coupure des n derniers bits
		elif o == "-c":
			mode = "c"
			yuv = True
			cut = int (a)

		# Projection de YUV en 3 images
		elif o == "-s":
			mode = "s"
			yuv = True

		# Selectionne le nom du fichier
		elif o == "-f":
			img_name = a

		# Methode de compression :
		elif o == "--d2":
			deflate = 'd2'

		# Division de l'image
		elif o == "-d":
			mode = "d"

	# Si il n'y a pas de fichier a lire ou pas d'option tout simplement
	if img_name == '' or mode == '':
		usage()
		sys.exit(2)

	# lecture de l'image
	(width, height), X, Y, Z = read_image(img_name, yuv);
	print ("[+] Read image : " + img_name +" "+str(width)+"x"+str(height))

	# On enleve l'extension du nom de l'image
	img_name = '.'.join(img_name.split('.')[:-1])

	# Suppression des X premiers bits des deux chromatiques
	if mode == "c" :
		cutfirstbit (X, Y, Z, width, height, cut, img_name)

	# Option separation des Y, U et V
	elif mode == "s":
		splitYUV (X, Y, Z, width, height, img_name)

	elif mode == "d":
		divide (X, Y, Z, width, height, img_name, deflate, yuv)
		
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
