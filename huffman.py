# huffman inflate and deflate
import pickle

def getprefcode (freq) :
# Pour obtenir la liste des priorités

	# Création de la liste des priorités
	prior = [[val, 1, car, [], []] for car, val in freq.items ()]

	# On créer notre arbre glouton
	while len (prior) > 1 :
		min1 = min (prior)
		del prior[prior.index (min1)]
		min2 = min (prior)
		del prior [prior.index (min2)]
		prior.append ([min2[0] + min1[0], min2[1] + min1[1], '', min2, min1])

	return prior[0]


def getdico (prefcode) :
# Pour obtenir la nouvelle norme

	dico = {}


def aux_getdico (code, val) :

	if code[2] != '' :
		dico.update ({val:code[2]})

	val1 = val + '0'
	val2 = val + '1'

	if code[3] != [] :
		aux_getdico (code[3], val1)
	if code[4] != [] :
		aux_getdico (code[4], val2)

	aux_getdico (prefcode, '')
	return dico


def getfreq (content) :
# Pour obtenir la 'frequence' des lettres

	freq = {}
	lencont = len(content)

	# On récupère les caractères ainsi que leur nombre
	for car in content : 
		if freq.get (car) != None :
			freq[car] += 1
		else :
			freq.update ({car:1})
		
	return freq


def compress (dico, content) :

	# On créer un dictionnaire inversé
	dicorev = {e:i for i, e in dico.items ()}

	c = ''

	for i in content : 
		c += dicorev[i]
	
	return c


def inflate (dico, c) :

	content = []

	while len(c) > 0 :
		
		count = 1
		while dico.get (c[0:count]) == None :
			count += 1

		content.append(dico.get(c[0:count]))
		c = c[count:]

	return content


def comp_file(filename):

	# On ouvre le fichier à compresser
	fd = open (filename, "rb")
	
	# On recupere son contenu
	content = fd.read()
	fd.close()
	
	cont2 = []
	for i in range(len(content)):
		cont2.append(int(content[i]))
	content = [i for i in cont2]
	
	# On recupere la frequence des caracteres
	freq = getfreq(content)
	
	print("dico:::::::::::::::: ", freq)
	
	# Creation du code des prefixes
	prefcode = getprefcode(freq)
	
	# Creation du dictionnaire
	dico = getdico(prefcode)
	
	# Compression du contenu
	c = compress(dico, content)
	
	with open(filename[0:len(filename) - 3] + 'wvl', 'wb') as fd:
		pickle.dump(dico, fd, protocol=None)
		for i in range(0, len(c), 8):
			fd.write(int(c[i:i+8], 2).to_bytes(1, "big"))


def decomp_file(filename):

    c = ''
    with open(filename, 'rb') as fd:
        dico = pickle.load(fd)
        content = fd.read()
        for i in range(len(content)):
            #print(bin(content[i])[2:].zfill(8))
            c += bin(content[i])[2:].zfill(8)

	
    #print(dico)
    #print(c)

    # Decompression du contenu
    d = inflate(dico, c)
    
    print(d)
    #fd = open(filename[0:len(filename) - 3] + 'rle2', 'wb')
    #fd.write(d)
    #fd.close()


if __name__ == "__main__" :

    comp_file("ile_de_la_cite2_D2_E0_P_5.rle")
    #decomp_file("ile_de_la_cite2_D2_E0_P_5.wvl")

