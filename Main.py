from Arbre import Arbre
from Arbre import Feuille
import random
from tkinter.filedialog import *
from tkinter.messagebox import showinfo

########## PROJET LS4 - GESTIONNAIRE DE MOBILES ##############

#Arbre >>> Mobile
def constructionMobile(l):
    A = Arbre()
    if type(l[0]) is int:
        A.gauche = Feuille(l[0])
    elif type(l[0]) is list:
        A.gauche = constructionMobile(l[0])
        
    if len(l) <= 1:
        return A.gauche
    
    if type(l[1]) is int:
        A.droit = Feuille(l[1])
    elif type(l[1]) is list:
        A.droit = constructionMobile(l[1])
    A.equilibre()

    return A


#Liste de poids >>> Arbre
def constructionArbre(l):
    A = Arbre()
    if len(l) == 0:
        showinfo("Erreur", "Le fichier est vide")
        return A
    elif len(l) == 1:
        A = Feuille(l[0])
        return A
    A.gauche = Feuille(l[0])
    A.droit = Feuille(l[1])
    
    for i in range(2, len(l)):
        A = A.constructionArbre(l[i])
    A.equilibre()
    
    return A

#Affiche le mobile sur l'ardoise
def affiche():
    global ardoise
    global mobile
    ardoise.delete("all")
    largeurArdoise = ardoise.winfo_width()
    longueurArdoise = ardoise.winfo_height()
    
    mobile.placerArbre()
    echelle = min(largeurArdoise // mobile.largeur(), longueurArdoise // mobile.longueur())
    
    afficheArbre(mobile, largeurArdoise//2, 0, mobile.maximum())
    ardoise.scale("all", largeurArdoise//2, 0, echelle, echelle)
    ardoise.update()


#Dessine les sous arbres du mobiles
def afficheArbre(A, x, y, hauteur):
    global ardoise
    ardoise.create_rectangle(x, y, x, y + hauteur)
    
    if type(A) is Arbre:
        ardoise.create_rectangle(x + A.gauche.position.x, y + hauteur + A.gauche.position.y, x + A.droit.position.x, y + hauteur + A.droit.position.y)
        afficheArbre(A.gauche, x + A.gauche.position.x, y + A.gauche.position.y + hauteur, hauteur)
        afficheArbre(A.droit, x + A.droit.position.x, y + A.droit.position.y + hauteur, hauteur)
    else:
        ardoise.create_oval(x - A.valeur/2 + A.valeur/60, y + hauteur - A.valeur/2 - A.valeur/60, x + A.valeur/2 - A.valeur/60 , y + hauteur + A.valeur/2 + A.valeur/60, fill=colorie(A.valeur))
        ardoise.create_text(x, y + hauteur-1, fill='black', anchor='center', text=str(A))

#Construit le mobile selon le mode choisit
def choixConstruction(a):
    global mobile
    l = mobile.listeElement()
    if mobile != None:
        x = {0: constructionArbre(l), 1: constructionArbreT(l), 2:constructionArbreLong(l)}
        mobile = x[a]
        
        affiche()


#Fichier >>> Mobile
def lectureFichier(fichier=None):
    global mobile
    global Etat
    if fichier == None:
        fichier = askopenfilename()
    lecture_fichier = open(fichier, "r")
    lignes = lecture_fichier.readlines()
    lecture_fichier.close()
    
    #Fichier vide
    if len(lignes) == 0:
        showinfo("Echec", "Le fichier est vide")
        return
    
    #Arbre
    if len(lignes) == 1:
        l = eval(lignes[0])
        mobile = constructionMobile(l)
    
    #Liste de poids
    else:
        l = []
        for i in lignes:
            j = i[:-1]
            if len(j) > 0: l.append(int(j))
        mobile = constructionArbre(l)
    
    #Changement d'etat et affichage du mobile
    Etat.set("Mobile charge")
    affiche()


#Sauvegarde l'arbre du mobile
def sauvegarderMobile():
    global mobile
    global Etat

    fichier = asksaveasfilename()
    ecriture_fichier = open(fichier, "w")
    ecriture_fichier.write(str(mobile))
    ecriture_fichier.close()

    Etat.set("L'arbre du mobile a ete sauvegarde")

#Sauvegarde de la liste des poids du mobile
def sauvegarderLDP():
    global mobile
    fichier = asksaveasfilename()
    ecriture_fichier = open(fichier, "w")
    l = mobile.listeElement()
    for i in l:
        ecriture_fichier.write(str(i)+"\n")
    ecriture_fichier.write("\n")
    ecriture_fichier.close()
    
    Etat.set("La liste de poids du mobile a ete sauvegarde")


#Construit un arbre triee
def constructionArbreT(l):
    l.sort()
    return constructionArbre(l)


#Construit un arbre le plus long possible
def constructionArbreLong(l):
    A = Arbre()
    if len(l) == 1:
        A = Feuille(l[0])
        return A
    else:
        A.droit = Feuille(l[0])
        A.gauche = Feuille(l[1])
    
    for i in range(2,len(l)):
        tmp = Arbre()
        tmp.gauche = Feuille(l[i])
        tmp.droit = A
        A = tmp
    A.equilibre()

    return A

#Colorie les feuilles
def colorie(x):
    pal=['purple','cyan','maroon','green','red','orange','yellow', 'HotPink', 'pink', 'Tomato','blue', 'OrangeRed', 'RoyalBlue', 'Gold', 'Khaki', 'Fushsia' ]
    return pal[(x%16)]

#Messages a recuperer
def messages(x):
    if x == 1:
        txt = "Vous etes sur une representation de mobiles!\n";
        txt += "Pour commencer cliquer sur Fichier -> Charger , pour charger un nouveau mobile ou bien cliquer sur Mobile et en choisr un\n";
        txt += "Vous pourrez ensuite le sauvegarder en tant qu'arbre ou bien sous la forme d'une liste de poids\n"; 
        showinfo("A Propos", txt)

    if x == 2:
        txt = "Bonjour :)\n" + "Vous etes sur une representation de mobiles!\n";
        txt += "Ce programme a ete realise Amadou SY\n";
        txt += "\n Amusez vous bien :D"; 
        showinfo("A Propos", txt)

    if x == 3:
        txt = "Bienvenu \n" + "Vous etes sur une representation de mobiles!\n\n";
        txt += "Pour commencer vous devez charger un mobile depuis le menu fichier.\n";
        txt += "Vous pouvez egalement charger un mobile depuis le menu Mobiles\n";
        return txt
    
#### FENETRE ####
fenetre = Tk()
fenetre.geometry("700x600")

#### MENU ####
barreMenu = Menu(fenetre)

mFichier = Menu(barreMenu)
mFichier.add_command(label="Charger un mobile",command=lectureFichier)
mFichier.add_command(label="Sauvegarder le mobile",command=sauvegarderMobile)
mFichier.add_command(label="Sauvegarder la liste de poids",command=sauvegarderLDP)
mFichier.add_command(label="Fermer le mobile",command=lambda:ardoise.delete("all"))
mFichier.add_command(label="Quitter",command=fenetre.destroy)
barreMenu.add_cascade(label="Fichier",menu=mFichier)

mEdition = Menu(barreMenu)
mEdition.add_command(label="Construction classique",command=lambda:choixConstruction(0))
mEdition.add_command(label="Construction triee",command=lambda:choixConstruction(1))
mEdition.add_command(label="Construction long",command=lambda:choixConstruction(2))
mEdition.add_command(label="Effacer l'ardoise",command=lambda:ardoise.delete("all"))
barreMenu.add_cascade(label="Edition",menu=mEdition)
  

mMobiles = Menu(barreMenu)
mMobiles.add_command(label="Mobile A", command=lambda:lectureFichier('./Mobiles/MobileA'))
mMobiles.add_command(label="Mobile B", command=lambda:lectureFichier('./Mobiles/MobileB'))
mMobiles.add_command(label="Mobile C", command=lambda:lectureFichier('./Mobiles/MobileC'))
mMobiles.add_command(label="Mobile D", command=lambda:lectureFichier('./Mobiles/MobileD'))
mMobiles.add_command(label='MOBILE ALEATOIRE', command= lambda: lectureFichier('./Mobiles/Mobile'+random.choice(['A','B','C','D'])))
barreMenu.add_cascade(label="Mobiles",menu=mMobiles)

mAide = Menu(barreMenu)
mAide.add_command(label="Guide",command=lambda:messages(1))
mAide.add_command(label="A Propos",command=lambda:messages(2))
barreMenu.add_cascade(label="Aide",menu=mAide)

fenetre.config(menu=barreMenu)

#### BARRE D'ETAT ####
Etat = StringVar()
BarreEtat = Label(fenetre, textvariable=Etat , anchor=E)
Etat.set("Veuillez charger un mobile")
BarreEtat.pack(side=BOTTOM, fill=X)    

#### ZONE DE DESSIN ####
ardoise = Canvas(fenetre, background="white")
ardoise.pack(side=TOP, fill=BOTH, expand=12)
ardoise.update()
ardoise.create_text(300, 250, fill='black', anchor='center', text=str(messages(3)))


fenetre.mainloop()

