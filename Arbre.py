##### CLASSE ARBRE #####

class Arbre:
	
	#Initialise l'arbre
    def __init__(self):
		#Valeur de l'arbre
        self.valeur = 0
		#Fils gauche
        self.gauche = None
		#Fils droit
        self.droit = None
		#Position de l'arbre
        self.position = Position()

    
    def __str__(self):
        return "["+str(self.gauche)+","+str(self.droit)+"]"

    def __len__(self):
        return len(self.gauche) + len(self.droit)

    
    def poid(self):
        return self.gauche.poid() + self.droit.poid()
    
    #Emplacement du sous arbre gauche
    def equilibre(self):
        if type(self.gauche) is Arbre:
            self.gauche.equilibre()
        if type(self.droit) is Arbre:
            self.droit.equilibre()
        self.valeur = self.droit.poid() / (self.gauche.poid()+self.droit.poid())

    #Feuille la plus lourde de l'arbre
    def maximum(self):
        if self.gauche.maximum() > self.droit.maximum():
            return self.gauche.maximum()
        else:
            return self.droit.maximum()
        
    #Liste des feuille de l'arbre
    def listeElement(self):
        l = self.gauche.listeElement()
        l.extend(self.droit.listeElement())
        return l
    
    #Largeur du noeud
    def largeurArbre(self):
        g = 0
        d = 0
        if type(self.gauche) is Feuille:
            g = self.gauche.valeur
        else:
            g = self.gauche.largeurArbre()

        if type(self.droit) is Feuille:
            d = self.droit.valeur
        else:
            d = self.droit.largeurArbre()

        return g+d
    
    #Place les arbres
    def placerArbre(self):
        largeur = self.largeurArbre()//2
        self.gauche.position.x = -largeur*self.valeur
        self.gauche.position.y = 0
        self.droit.position.x = self.gauche.position.x + largeur
        self.droit.position.y = 0
        
        if type(self.gauche) is not Feuille:
            self.gauche.placerArbre()
        
        if type(self.droit) is not Feuille:
            self.droit.placerArbre()
            
    #Largeur de l'arbre pour le dessin
    def largeur(self):
        g = self.gauche.largeurGauche() + self.gauche.position.x
        d = self.droit.largeurDroit() + self.droit.position.x
        return - g + d

    def largeurGauche(self):
        return self.gauche.position.x + self.gauche.largeurGauche()

    def largeurDroit(self):
        return self.droit.position.x + self.droit.largeurDroit()

    #Longueur de l'arbre pour le dessin
    def longueur(self):
        hauteur = self.maximum()
        return self.longueurRec(hauteur)

    def longueurRec(self, hauteur):
        d = self.droit.position.y + self.droit.longueurRec(hauteur)
        g = self.gauche.position.y + self.gauche.longueurRec(hauteur)
        return hauteur + max(d,g)

    #Profondeur de l'arbre   
    def hauteur(self):
        if self.gauche.hauteur() > self.droit.hauteur():
            return self.gauche.hauteur()+1
        return self.droit.hauteur()+1

    #Construit le mobile
    def constructionArbre(self, v):
        poidG = self.gauche.poid()
        poidD = self.droit.poid()
        if v >= (poidG+poidD):
            A = Arbre()
            A.gauche = self
            A.droit = Feuille(v)
            return A
        if poidG == poidD:
            if self.gauche.hauteur() > self.droit.hauteur():
                self.droit = self.droit.constructionArbre(v)
            else:
                self.gauche = self.gauche.constructionArbre(v)
        elif poidG > poidD :
            self.droit = self.droit.constructionArbre(v)
        else:
            self.gauche = self.gauche.constructionArbre(v)
        return self


###### CLASSE FEUILLE #####

class Feuille(Arbre):
    
    def __init__(self, v):
        self.valeur = v
        self.position = Position()
    
    def __str__(self):
        return str(self.valeur)
    
    def __len__(self):
        return 1

    
    def poid(self):
        return self.valeur
    
    def maximum(self):
        return self.valeur
    
    def listeElement(self):
        return [self.valeur]
    
    def largeurGauche(self):
        return -self.valeur//2
    
    def largeurDroit(self):
        return self.valeur//2
    
    def longueur(self):
        hauteur = self.maximum()
        return self.longeurRec(hauteur)

    def longueurRec(self, hauteur):
            return hauteur + self.valeur//2
            
    def hauteur(self):
        return 1

    def constructionArbre(self, v):
        p = Arbre()
        p.gauche = self
        p.droit = Feuille(v)
        return p


class Position:
    def __init__(self):
        self.x = 0
        self.y = 0
