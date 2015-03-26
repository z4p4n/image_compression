#!/usr/bin/python3.4

# Compresseur
# -> Décomposition de l'image par YUV
# -> Suppression des 4 premiers bits des deux octets U et V representants la chrominance
#
# z4p4n, NexMat

# Importations
import math
import numpy as np
import getopt, sys
from img_compute import *
from DN import *

def inflate_vert (XS, YS, ZS, XD, YD, ZD, width, height, matrix) :

	X = [[0 for i in range (width)] for j in range (height * 2)]
	Y = [[0 for i in range (width)] for j in range (height * 2)]
	Z = [[0 for i in range (width)] for j in range (height * 2)]

	for i in range (width) :
		for j in range (0, height, 8) :
			S = [XS[j+k][i] for k in range (8)]
			D = [XD[j+k][i] for k in range (8)]
			S.extend (D)
			S, D = transfoDN (S, matrix)
			S.extend (D)
			for k in range (16): 
				X[j*2+k][i] = S[k]
			S = [YS[j+k][i] for k in range (8)]
			D = [YD[j+k][i] for k in range (8)]
			S.extend (D)
			S, D = transfoDN (S, matrix)
			S.extend (D)
			for k in range (16): 
				Y[j*2+k][i] = S[k]
			S = [ZS[j+k][i] for k in range (8)]
			D = [ZD[j+k][i] for k in range (8)]
			S.extend (D)
			S, D = transfoDN (S, matrix)
			S.extend (D)
			for k in range (16): 
				Z[j*2+k][i] = S[k]
		if i % 100 == 0 : print ("    processing... " + str (i) + "/" + str(width) + "  ")

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

			(S, D) = transfoDN ([X[j+k][i] for k in range (0, 16)], matrix)
			for k in range (8): 
				XresS[j//2+k][i] = S[k]
				XresD[j//2+k][i] = D[k]
			(S, D) = transfoDN ([Y[j+k][i] for k in range (0, 16)], matrix)
			for k in range (8): 
				YresS[j//2+k][i] = S[k]
				YresD[j//2+k][i] = D[k]
			(S, D) = transfoDN ([Z[j+k][i] for k in range (0, 16)], matrix)
			for k in range (8): 
				ZresS[j//2+k][i] = S[k]
				ZresD[j//2+k][i] = D[k]
		if i % 100 == 0 : print ("    processing... " + str (i) + "/" + str(width) + "  ")

	return (XresS, YresS, ZresS, XresD, YresD, ZresD)


def compression_img (X, Y, Z, width, height, img_name, deflate, yuv, depth, err) :
# On renvoie les donnees a compression

	# Compteur de compression
	counter = 0

	print ("\n{ Deflate image }")

	# Enregistrement des donnees de compression
	data = []

	# Compression de l'image
	for i in range(depth):
		print ("\n{Round " + str (i) + "}")
		X, Y, Z, img_diff, width, height, gain = compression (X, Y, Z, width, height, img_name, deflate, yuv, err)

		# Sauvegarde du nombre de pixels compressees
		counter += gain

		data.append([img_diff, (width, height)])

	# Decompression de l'image
	for i in range (depth - 1, -1, -1):

		X, Y, Z, width, height = decompression (X, Y, Z, data[i][0], data[i][1], img_name, deflate, yuv, err)

		print ("[+] Create new image " + str(width) + "x" + str(height))
		format = ''
		if (yuv == True) : format = 'yuv' 
		else : format = 'rgb'
		create_image ("" + img_name + "_D" + str(deflate) + "_E" + str(error) + "_P_" + str(depth + 1) + "." + str(i) + "_" + format, width, height, X, Y, Z, yuv)

	print ("\n[?] Compressed pixels : " + str (counter))

def compression (X, Y, Z, width, height, img_name, deflate, yuv, err) :

	# Pour le moment on fait facile modulo 16 bits TODO
	new_width  = width  - width % 16
	new_height = height - height % 16

	# Creation de la matrice avec la methode deflate
	matrix = matrixDN(deflate, 16)

	# On divise l'image dans le sens de la largeur avec la methode deflate
	XS = [[] for i in range (height)]
	YS = [[] for i in range (height)]
	ZS = [[] for i in range (height)]
	XD = [[] for i in range (height)]
	YD = [[] for i in range (height)]
	ZD = [[] for i in range (height)]

	print ("[+] Apply D" + str(deflate) + " on image - horizontally")
	for j in range (height) :
		for i in range (0, new_width, 16) :

			(S, D) = transfoDN (X[j][i:i+16], matrix)
			XS[j].extend (S)
			XD[j].extend (D)
			(S, D) = transfoDN (Y[j][i:i+16], matrix)
			YS[j].extend (S)
			YD[j].extend (D)
			(S, D) = transfoDN (Z[j][i:i+16], matrix)
			ZS[j].extend (S)
			ZD[j].extend (D)
		if j % 100 == 0 : print ("    processing... " + str (j) + "/" + str(height) + "  ")

	new_width = new_width // 2
	# On divise l'image dans le sens de la hauteur avec  la methode deflate
	print ("[+] Apply D" + str(deflate) + " on image - vertically - Average")
	(XSS, YSS, ZSS, XSD, YSD, ZSD) = compression_vert (XS, YS, ZS, new_width, new_height, matrix)
	print ("[+] Apply D" + str(deflate) + " on image - vertically - Difference") 
	(XDS, YDS, ZDS, XDD, YDD, ZDD) = compression_vert (XD, YD, ZD, new_width, new_height, matrix)

	new_height = new_height // 2

	# Filtrage des differences
	counter = 0
	print ("[+] Filter difference with " + str (error) + " error")
	if deflate == 2:
		for i in range (new_width) :
			for j in range (new_height) :
				if math.fabs(XSD[j][i]) <= error and yuv == False:
					XSD[j][i] = 0
					counter += 1
				if math.fabs(YSD[j][i]) <= error :
					YSD[j][i] = 0
					counter += 1
				if math.fabs(ZSD[j][i]) <= error :
					ZSD[j][i] = 0
					counter += 1
				if math.fabs(XDD[j][i]) <= error and yuv == False:
					XDD[j][i] = 0
					counter += 1
				if math.fabs(YDD[j][i]) <= error :
					YDD[j][i] = 0
					counter += 1
				if math.fabs(ZDD[j][i]) <= error :
					ZDD[j][i] = 0
					counter += 1
	elif deflate == 4:
		for i in range (new_width) :
			for j in range (new_height) :

				#if math.fabs(XSD[j][i]) <= error :
				#	XSD[j][i] = 0
				#	counter += 1
				#if math.fabs(YSD[j][i]) <= error :
				#	YSD[j][i] = 0
				#	counter += 1
				#if math.fabs(ZSD[j][i]) <= error :
				#	ZSD[j][i] = 0
				#	counter += 1
				if math.fabs(XDD[j][i]) <= error :
					XDD[j][i] = 0
					counter += 1
				if math.fabs(YDD[j][i]) <= error :
					YDD[j][i] = 0
					counter += 1
				if math.fabs(ZDD[j][i]) <= error :
					ZDD[j][i] = 0
					counter += 1

	print ("[?] Number of filtered value " + str (counter))

	img_diff = (XSD, YSD, ZSD, XDS, YDS, ZDS, XDD, YDD, ZDD)
	return XSS, YSS, ZSS, img_diff, new_width, new_height, counter


def decompression (XSS, YSS, ZSS, img_diff, size, img_name, deflate, yuv, err) :

	# Extraction des donnees
	XSD, YSD, ZSD, XDS, YDS, ZDS, XDD, YDD, ZDD = img_diff
	new_width, new_height = size

	# Creation de la matrice avec la methode deflate TODO
	matrix = matrixDN(deflate, 16)

	# Reconstruction de l'image
	print ("\n{ Rebuild image }")
	matrix = matrixDN_inv (matrix)

	# Reconstruction verticale
	print ("[+] Inflate vertically - Average")
	(XS, YS, ZS, w, h) = inflate_vert (XSS, YSS, ZSS, XSD, YSD, ZSD, new_width, new_height, matrix) 
	print ("[+] Inflate vertically - Difference")
	(XD, YD, ZD, w, h) = inflate_vert (XDS, YDS, ZDS, XDD, YDD, ZDD, new_width, new_height, matrix) 

	#print ("[+] Create new image " + str(w) + "x" + str(h))
	#create_image ("" + img_name + "_D" + str(deflate) + "tmp_" + str(error), w, h, XS, YS, ZS, yuv)

	print ("[+] Inflate horizontally")
	# Reconstruction horizontale
	X = [[0 for i in range (w * 2)] for j in range (h)]
	Y = [[0 for i in range (w * 2)] for j in range (h)]
	Z = [[0 for i in range (w * 2)] for j in range (h)]

	for j in range (h) :
		for i in range (0, w, 8) :
			S = XS[j][i:i+8]
			D = XD[j][i:i+8]
			S.extend (D)
			S, D = transfoDN (S, matrix)
			S.extend (D)
			for k in range (16): 
				X[j][i*2 + k] = S[k]
			S = YS[j][i:i+8]
			D = YD[j][i:i+8]
			S.extend (D)
			S, D = transfoDN (S, matrix)
			S.extend (D)
			for k in range (16): 
				Y[j][i*2 + k] = S[k]
			S = ZS[j][i:i+8]
			D = ZD[j][i:i+8]
			S.extend (D)
			S, D = transfoDN (S, matrix)
			S.extend (D)
			for k in range (16): 
				Z[j][i*2 + k] = S[k]
		if j % 100 == 0 : print ("    processing... " + str (j) + "/" + str(height) + "  ")

	return (X, Y, Z, w * 2, h)


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
	matrix = matrixDN_light(deflate, 16)

	# On divise l'image dans le sens de la largeur avec la methode deflate
	Xres = [[] for i in range (height)]
	Yres = [[] for i in range (height)]
	Zres = [[] for i in range (height)]

	print ("[+] Apply D" + str(deflate) + " on image - horizontally")
	for j in range (height) :
		for i in range (0, new_width, 16) :

			Xres[j].extend (transfoDN_light (X[j][i:i+16], matrix))
			Yres[j].extend (transfoDN_light (Y[j][i:i+16], matrix))
			Zres[j].extend (transfoDN_light (Z[j][i:i+16], matrix))
		if j % 100 == 0 : print ("    processing... " + str (j) + "/" + str(height) + "  ")

	new_width = new_width // 2
	# On divise l'image dans le sens de la hauteur avec la methode deflate
	print ("[+] Apply D" + str(deflate) + " on image - vertically")
	Xres2 = [[0 for i in range (new_width)] for j in range (new_height//2)]
	Yres2 = [[0 for i in range (new_width)] for j in range (new_height//2)]
	Zres2 = [[0 for i in range (new_width)] for j in range (new_height//2)]

	for i in range (new_width) :
		for j in range (0, new_height, 16) :

			s = transfoDN_light ([Xres[j+k][i] for k in range (0, 16)], matrix)
			for k in range (8): Xres2[j//2+k][i] = s[k]
			s = transfoDN_light ([Yres[j+k][i] for k in range (0, 16)], matrix)
			for k in range (8): Yres2[j//2+k][i] = s[k]
			s = transfoDN_light ([Zres[j+k][i] for k in range (0, 16)], matrix)
			for k in range (8): Zres2[j//2+k][i] = s[k]

		if i % 100 == 0 : print ("    processing... " + str (i) + "/" + str(new_width) + "  ")

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
	print("Usage: python3 compressor.py [df:hyc:se:]")


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
	depth = 0
	img_name = ''
	deflate = 2

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
			depth = int (a)

		# Methode de compression 
		elif o == "--d2":
			deflate = 2

		elif o == "--d4":
			deflate = 4

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
		compression_img (X, Y, Z, width, height, img_name, deflate, yuv, depth, error)

