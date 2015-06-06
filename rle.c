#define BLOCKSIZE 1024 
// taille d'un bloc a lire
#define DECOMPSIZE 130100
// le meme decompresse. Au pire, 127 fois plus gros... 
#define COMPSIZE 1040
// et ici taille pour un bloc compresse. Au pire on rajoute un octet tous les 128...
#include <stdio.h>
// printf
#include <stdlib.h>
// exit
#include <unistd.h>
// read write close
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
//open
#include <err.h>
// err 
 #include <string.h>
// strcmp

void RLEdecompress(int in, int out)
{
  /* on suppose que in et out sont des fichiers ouverts */
  
  char bufin[BLOCKSIZE]; // buffer pour lecture
  char bufout[DECOMPSIZE]; // buffer pour ecriture
  int lus; // nombre d'octets lus par read
  int pin, pout; // pointeurs dans bufin et bufout
  int x,y; // comme dans l'enoncee
  int i; // indice de boucle

  while(1) {
    lus = read(in, bufin, BLOCKSIZE);
    if(lus == -1)
      err(1, "erreur read");
    if(lus == 0) // EOF
      return; 
    pin=pout=0;
    do {
      x = bufin[pin++];
      if(x>=0)	{
	if(lus == pin)
	  // zut y est sur le bloc de 1024 suivant !
	  {
	    if(lus == 1) // ben y'a pas de bloc suivant !
	      {
		fprintf(stderr,"erreur decodage. Format invalide ?\n");
		return;
	      }
	    lseek(in, -1, SEEK_CUR);
	    // dans ce cas on recule de 1 octet
	    break;
	    // et on recommence au bloc suivant
	  }
	y = bufin[pin++];
	for(i=0;i<=x;i++) // ecrire x+1 fois
	  bufout[pout++]=y;
      }
      else {
	if(lus - pin < -x)
	  {
	    // zut, le bloc heterogene a decoder continue sur le read suivant ! 
	    if(pin == 1) // on avait deja fait un lseek pour reculer c'est pas normal
	      {
		fprintf(stderr,"erreur decodage. Format invalide ?\n");
		return;
	      }
	    lseek(in, - ( 1 + lus - pin), SEEK_CUR);
	    // dans ce cas on recule de 1 + lus - pin octets pour relire x
	    break;
	    // et on recommence
	  }
	// on decompresse le bloc homogene
	for(i=0;i< -x; i++)
	  bufout[pout++]=bufin[pin++];
      }
    } while(pin<lus); // arret sur le dernier bloc
    
    if(write(out, bufout, pout) == -1)
      err(1, "erreur write");
  }
}  
  


void RLEcompress(int in, int out)
{
  /* on suppose que in et out sont des fichiers ouverts */
  
  char bufin[BLOCKSIZE]; // buffer pour lecture
  char bufout[COMPSIZE]; // buffer pour ecriture
  int lus; // nombre d'octets lus par read
  int pin, pout; // pointeurs dans bufin et bufout
  int x,y; // comme dans l'enoncee
  int i; // indice de boucle
  while(1){
    lus = read(in, bufin, BLOCKSIZE);
    if(lus == -1)
      err(1, "erreur read");
    if(lus == 0) // EOF
      return; 
    pin=pout=0;
    do {
      // on cherche si on fait un bloc homogene ou heterogene
      if(pin + 3 < lus && 
	 bufin[pin] == bufin[pin+1] &&  
	 bufin[pin+1] == bufin[pin+2])
	// bloc homogene commence
	{
	  x = 1;
	  y = bufin[pin++];
	  while(pin < lus && x < 127 && bufin[pin]==y)
	    {
	      x++;
	      pin++;
	    }	
	  bufout[pout++]=(char)(x-1);
	  bufout[pout++]=(char)y;
	}
      else // bloc homogene. On va jusqu'a 3 caracteres repetes
	{
	  x = 0;
	  while(pin+x < lus 
		&& x < 127 
		&& ! ( pin +x+ 3 < lus 
		       && bufin[pin+x] == bufin[pin+x+1] 
		       && bufin[pin+x+1] == bufin[pin+x+2]))
	    {
	      x++;
	    }
	  if(x==0)
	    break; // fin du bloc, on n'ecrit rien
	  bufout[pout++]=(char)(-x);
	  for(i=0;i<x;i++)
	    bufout[pout++]=(char)bufin[pin++];
	}
      if(lus > 129 && lus - pin <129)
	{
	  /* oh oh, on risque un chevauchement de bloc car il est
	     possible que le bloc suivant à compresser chevauche la
	     limite de bloc */
	  lseek(in, pin - lus, SEEK_CUR);
	  // dans ce cas on recule de lus - pin octets
	  break;
	  // et on recommence
	}
    }while(pin<lus); // arret sur le dernier bloc
    
    if(write(out, bufout, pout) == -1)
      err(1, "erreur write");
  }  
}


int main(int argc, char **argv) {
  int in, out; // fichiers
  
  if(argc != 4 || ! ( (strcmp(argv[1],"-c")==0) || (strcmp(argv[1],"-d")==0) ) )
    {
      printf("Usage : %s [-c|-d] file file\n", argv[0]);
      return 1;
    }
  
  if( (in = open(argv[2], O_RDONLY))==-1)
    err(1,"erreur d'ouverture %s", argv[2]);
  if( (out = open(argv[3], O_WRONLY | O_TRUNC | O_CREAT, 0660))==-1)
    err(1,"erreur d'ouverture %s", argv[3]);
  
  if(argv[1][1] == 'c')
    RLEcompress(in,out);
  else // donc d
    RLEdecompress(in,out);
  
  close(in); 
  close(out);
  return 0;
}
