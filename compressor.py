#!/usr/bin/python3.4

# Compresseur
# -> Décomposition de l'image par YUV
# -> Suppression des 4 premiers bits des deux octets U et V representant la chrominance
#
# z4p4n, NexMat

import math
import numpy as np
import getopt, sys
from img_compute import *
from D2 import *

def inflate_vert (XS, YS, ZS, XD, YD, ZD, width, height, matrix) :

	X = [[0 for i in range (width * 2)] for j in range (height * 2)]
	Y = [[0 for i in range (width * 2)] for j in range (height * 2)]
	Z = [[0 for i in range (width * 2)] for j in range (height * 2)]

	for i in range (width) :
		for j in range (0, height, 8) :
			S = [XS[j+k][i] for k in range (8)]
			D = [XD[j+k][i] for k in range (8)]
			S.extend (D)
			S, D = transfoD2 (S, matrix)
			S.extend (D)
			for k in range (16): 
				X[j*2+k][i] = S[k]
			S = [YS[j+k][i] for k in range (8)]
			D = [YD[j+k][i] for k in range (8)]
			S.extend (D)
			S, D = transfoD2 (S, matrix)
			S.extend (D)
			for k in range (16): 
				Y[j*2+k][i] = S[k]
			S = [ZS[j+k][i] for k in range (8)]
			D = [ZD[j+k][i] for k in range (8)]
			S.extend (D)
			S, D = transfoD2 (S, matrix)
			S.extend (D)
			for k in range (16): 
				Z[j*2+k][i] = S[k]

	return (X, Y, Z, width, height * 2)
			
def compression_vert (X, Y, Z, width, height, matrix) :

	XresS = [[0 for i in range (width)] for j in range (height//2)]
	YresS = [[0 for i in range (width)] for j in range (height//2)]
	ZresS = [[0 for i in range (width)] for j in range (height//2)]
	XresD = [[0 for i in range (width)] for j in range (height//2)]
	YresD = [[0 for i in range (width)] for j in range (height//2)]
	ZresD = [[0 for i in range (width)] for j in range (height//2)]

	for i in range (width) :
		for j in range (0, height, 16) :

			(S, D) = transfoD2 ([X[j+k][i] for k in range (0, 16)], matrix)
			for k in range (8): 
				XresS[j//2+k][i] = S[k]
				XresD[j//2+k][i] = S[k]
			(S, D) = transfoD2 ([Y[j+k][i] for k in range (0, 16)], matrix)
			for k in range (8): 
				YresS[j//2+k][i] = S[k]
				YresD[j//2+k][i] = S[k]
			(S, D) = transfoD2 ([Z[j+k][i] for k in range (0, 16)], matrix)
			for k in range (8): 
				ZresS[j//2+k][i] = S[k]
				ZresD[j//2+k][i] = S[k]
		if i % 100 == 0 : print ("[!] processing... " + str (i) + "/" + str(width) + "  ")

	return (XresS, YresS, ZresS, XresD, YresD, ZresD)


def compression (X, Y, Z, width, height, img_name, deflate, yuv, degre, err) :

	# Pour le moment on fait facile modulo 16 bits TODO
	new_width  = width  - width % 16
	new_height = height - height % 16

	# Creation de la matrice avec la methode deflate TODO
	matrix = matrixD2(16)

	# On divise l'image dans le sens de la largeur avec la methode deflate
	XresS = [[] for i in range (height)]
	YresS = [[] for i in range (height)]
	ZresS = [[] for i in range (height)]
	XresD = [[] for i in range (height)]
	YresD = [[] for i in range (height)]
	ZresD = [[] for i in range (height)]

	print ("[+] Apply D2 on image - horizontaly")
	for j in range (height) :
		for i in range (0, new_width, 16) :

			(S, D) = transfoD2 (X[j][i:i+16], matrix)
			XresS[j].extend (S)
			XresD[j].extend (D)
			(S, D) = transfoD2 (Y[j][i:i+16], matrix)
			YresS[j].extend (S)
			YresD[j].extend (D)
			(S, D) = transfoD2 (Z[j][i:i+16], matrix)
			ZresS[j].extend (S)
			ZresD[j].extend (D)
		if j % 100 == 0 : print ("[!] processing... " + str (j) + "/" + str(height) + "  ")

	new_width = new_width // 2
	# On divise l'image dans le sens de la hauteur avec  la methode deflate
	print ("[+] Apply D2 on image - verticaly - Average")
	(XSres2S, YSres2S, ZSres2S, XSres2D, YSres2D, ZSres2D) = compression_vert (XresS, YresS, ZresS, new_width, new_height, matrix)
	print ("[+] Apply D2 on image - horizontaly - Difference") 
	(XDres2S, YDres2S, ZDres2S, XDres2D, YDres2D, ZDres2D) = compression_vert (XresD, YresD, ZresD, new_width, new_height, matrix)

	new_height = new_height // 2

	# Filtrage des differences
	counter = 0
	print ("[+] Filter difference with " + str (error) + " error")
	for i in range (new_width) :
		for j in range (new_height) :
			if math.fabs(XSres2D[j][i]) <= error :
				XSres2D[j][i] = 0
				counter += 1
			if math.fabs(YSres2D[j][i]) <= error :
				YSres2D[j][i] = 0
				counter += 1
			if math.fabs(ZSres2D[j][i]) <= error :
				ZSres2D[j][i] = 0
				counter += 1
			if math.fabs(XSres2D[j][i]) <= error :
				XDres2D[j][i] = 0
				counter += 1
			if math.fabs(YSres2D[j][i]) <= error :
				YDres2D[j][i] = 0
				counter += 1
			if math.fabs(ZSres2D[j][i]) <= error :
				ZDres2D[j][i] = 0
				counter += 1

	print ("[?] Number of filtered value " + str (counter))

	# Reconstruction de l'image
	print ("[+] Rebuild image")
	matrix = matrixDN_inv (matrix)

	# Reconstruction verticale
	print ("[+] Inflate verticaly - Average")
	(XfinS, YfinS, ZfinS, w, h) = inflate_vert (XSres2S, YSres2S, ZSres2S, XSres2D, YSres2D, ZSres2D, new_width, new_height, matrix) 
	print ("[+] Inflate verticaly - Difference")
	(XfinD, YfinD, ZfinD, w, h) = inflate_vert (XDres2S, YDres2S, ZDres2S, XDres2D, YDres2D, ZDres2D, new_width, new_height, matrix) 

	print ("[+] Create new image " + str(w) + "x" + str(h))
	create_image ("" + img_name + "_D2tmp", w, h, XfinS, YfinS, ZfinS, yuv)

	# Reconstruction horizontale
	X = [[0 for i in range (w * 2)] for j in range (h)]
	Y = [[0 for i in range (w * 2)] for j in range (h)]
	Z = [[0 for i in range (w * 2)] for j in range (h)]

	for j in range (h) :
		for i in range (0, w, 8) :
			S = XfinS[j][i:i+8]
			D = XfinD[j][i:i+8]
			S.extend (D)
			S, D = transfoD2 (S, matrix)
			S.extend (D)
			for k in range (16): 
				X[j][i*2 + k] = S[k]
			S = YfinS[j][i:i+8]
			D = YfinD[j][i:i+8]
			S.extend (D)
			S, D = transfoD2 (S, matrix)
			S.extend (D)
			for k in range (16): 
				Y[j][i*2 + k] = S[k]
			S = ZfinS[j][i:i+8]
			D = ZfinD[j][i:i+8]
			S.extend (D)
			S, D = transfoD2 (S, matrix)
			S.extend (D)
			for k in range (16): 
				Z[j][i*2 + k] = S[k]
		if j % 100 == 0 : print ("[!] processing... " + str (j) + "/" + str(height) + "  ")

	print ("[+] Create new image " + str(w * 2) + "x" + str(h))
	create_image ("" + img_name + "_D2", w * 2, h, X, Y, Z, yuv)

	#return (Xres2, Yres2, Zres2, new_width, new_height)
	
def divide (X, Y, Z, width, height, img_name, deflate, yuv) :

	i = 2
	# On divise l'image tant qu'on peut
	while (width > 16 and height > 16) :
		print ("[+] Divide image per " + str (i))
		(X, Y, Z, width, height) = divide_img (X, Y, Z, width, height, img_name + "_" + str(i), deflate, yuv)
		i += 1

def divide_img (X, Y, Z, width, height, img_name, deflate, yuv) :

	# Pour le moment on fait facile modulo 16 bits TODO
	new_width  = width  - width % 16
	new_height = height - height % 16

	# Creation de la matrice avec la methode deflate TODO
	matrix = matrixD2_light(16)

	# On divise l'image dans le sens de la largeur avec la methode deflate
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
	# On divise l'image dans le sens de la hauteur avec  la methode deflate
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
		opts, args = getopt.getopt(sys.argv[1:], "df:hyc:se:", ["help", "d2", "d4"])
	except getopt.GetoptError as err:
		print (str(err))
		usage ()
		sys.exit (2)

	yuv = False
	cut = 0
	error = 0
	mode = ''
	degre = 0
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
		elif o == "-b":
			mode = "b"
			yuv = True
			cut = int (a)

		# Projection de YUV en 3 images
		elif o == "-s":
			mode = "s"
			yuv = True

		# Selectionne le nom du fichier
		elif o == "-f":
			img_name = a

		# Compression du fichier
		elif o == "-c":
			mode = "c"
			degre = int (a)

		# Methode de compression 
		elif o == "--d2":
			deflate = 'd2'

		elif o == "--d4":
			deflate = 'd4'

		# Niveau d'erreur
		elif o == "-e":
			error = int (a)

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
	if mode == "b" :
		cutfirstbit (X, Y, Z, width, height, cut, img_name)

	# Option separation des Y, U et V
	elif mode == "s":
		splitYUV (X, Y, Z, width, height, img_name)

	elif mode == "d":
		divide (X, Y, Z, width, height, img_name, deflate, yuv)

	elif mode == "c":
		compression (X, Y, Z, width, height, img_name, deflate, yuv, degre, error)
		
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
