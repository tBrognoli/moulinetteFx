import pymysql

class Membres:
    def __init__(self, nom, prenom, groupe):
        self.nom = nom
        self.prenom = prenom
        self.groupe = groupe


db = pymysql.connect("localhost", "root", "", "itstart")

cursor = db.cursor()

with open('membres.csv','r',encoding='utf8') as fichierMb:
    fichierMb = fichierMb.read()


listLignesMb = fichierMb.split("\n")
listMembres = list()

i= 0
while i < len(listLignesMb):
    listInfosMb = listLignesMb[i].split(";")
    listMembres.append(Membres(listInfosMb[0], listInfosMb[1], listInfosMb[2]))
    i+=1

for Membres in listMembres:
    sql = "INSERT INTO student(nom, prenom, groupe)\
        VALUES ('%s', '%s', '%s')" %\
          (Membres.nom, Membres.prenom, Membres.groupe)

    try:
        cursor.execute(sql)
        db.commit()
    except:
        db.rollback()


db.close()