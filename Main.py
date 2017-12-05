# -*- coding: utf-8 -*-
from Fonctions import *
import shutil
import os
import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import pymysql

class Membres:
    def __init__(self, nom, prenom, groupe):
        self.nom = nom
        self.prenom = prenom
        self.groupe = groupe

#Connecte la BDD et crée une liste de Membres
db = pymysql.connect("localhost", "root", "", "itstart")
cursor = db.cursor()
sql = "SELECT * FROM student"
listMembres = list()
try:
    cursor.execute(sql)
    results = cursor.fetchall()
    for row in results:
        listMembres.append(Membres(row[1], row[2], row[3]))
except:
    print("Error")
db.close()

def ObtenirListN_P(groupe, sep):
    listN_P = list()
    for Membres in listMembres:
        if Membres.groupe == groupe:
            listN_P.append(str(Membres.nom) + sep + Membres.prenom)
    return listN_P

nom7zip = ""
groupe =""
date = str(datetime.date.today())
replay = 0
while replay != "stop":
    os.system("cls")
    path = input("Chemin du dossier contenant les fichiers à envoyer : ")
    try:
        listFichiers = os.listdir(path)
    except:
        print("Erreur, le chemin du dossier est introuvable")
        continue
    trier = input("Passer le dossier à la moulinette (oui/non) : ")

    while trier == "oui":
        print("     NE MARCHE QUE SI LE RENDU COMMENCE PAR 'Nom Prenom'")
        groupeIT = input("Votre groupe (A ou B) : ")

        if groupeIT != "A" and groupeIT != "B":
            print("Votre groupe doit être 'A' ou 'B' !")
            continue
        if groupeIT =="A":
            groupe = "ITSTARTA"
        if groupeIT == "B":
            groupe = "ITSTARTB"

        sep = input("Séparateur entre 'Nom' et 'Prenom' : ")
        if sep == "-":
            print("Erreur, ne pas utiliser '-' comme séparateur, à cause des noms composés")


        nbExt = input("Nombre de type de fichiers possible (ex doc, docx) : ")
        try:
            nbExt = int(nbExt)
        except:
            print("Le nombre de type de fichiers possible doit être... UN NOMBRE...")
            continue

        extensions = list()
        i = 0
        while i < nbExt:
            extensions.append(input("Extension " + str(i+1) + " : "))
            i +=1

        try:
            os.mkdir(path + "\\PasBon")
        except:
            b=1
        try:
            listFichiers.remove("PasBon")
        except:
            b=0
        try:
            os.mkdir(path + "\\Contrôles" + date)
        except:
            b=0
        try:
            listFichiers.remove("Contrôles" + date)
        except:
            b=1

        resume = "      Erreur d'envois\n"
        listPoub = list()
        i =0
        listFichiersSplit = list()
        while i < len(listFichiers):
            listFichiersSplit = listFichiers[i].split(".")
            if listFichiersSplit[1] not in extensions:
                try:
                    shutil.move(path + "\\"+listFichiers[i], path+"\\PasBon")
                    resume += listFichiers[i] + " Erreur type de fichier\n"
                    listPoub.append(listFichiers[i])
                except:
                    b=1

            i+=1

        if len(listPoub) > 0:
            for valeur in listPoub:
                for typeExt in extensions:
                    try:
                        listFichiers.remove(valeur)
                    except:
                        b=0

        i = 0
        while i < len(listFichiers):
            for typeExt in extensions:
                try:
                    listFichiers[i] = listFichiers[i].replace("."+typeExt, "")
                except:
                    b=1
            i+=1

        fin = input("Nom du fichier apres 'Nom" + sep + "Prenom' : ")

        listPoub1 = list()

        for fichier in listFichiers:
            if fichier[-len(fin):] != fin:
                for typeExt in extensions:
                    try:
                        shutil.move(path + "\\" + fichier + "." + typeExt, path + "\\PasBon")
                        resume += fichier + " Erreur Fin de nom du fichier\n"
                        listPoub1.append(fichier)
                    except:
                        b=2

        if len(listPoub1) > 0:
            for valeur in listPoub1:
                listFichiers.remove(valeur)

        i=0
        while i < len(listFichiers):
            listFichiers[i] = listFichiers[i].replace(fin, "")
            i+=1

        listN_P = ObtenirListN_P(groupe, sep)
        listPoub2 = list()
        for fichier in listFichiers:
            if fichier in listN_P:
                for typeExt in extensions:
                    try:
                        shutil.move(path + "\\" + fichier + fin + "." + typeExt, path + "\\Contrôles"+date)
                    except:
                        b=0
            else:
                for typeExt in extensions:
                    try:
                        shutil.move(path + "\\" + fichier + fin + "." + typeExt, path + "\\PasBon")
                        resume += fichier + " Erreur Nom_Prenom\n"
                        listPoub2.append(fichier)
                    except:
                        b=1


        if len(listPoub2) > 0:
            for valeur in listPoub2:
                listFichiers.remove(valeur)

        resume += "\n       Manque les devoirs de :\n"
        for N_P in listN_P:
            if N_P not in listFichiers:
                resume += N_P + "\n"
        print("\n")

        with open(path + "\\resulat.txt", "a") as fichier:
                fichier.write(resume)

        print(resume)
        trier = "non"

    zipper = input("Voulez vous Zip le dossier (oui/non)")
    while zipper =="oui":
        nom7zip = input("Nom du 7zip : ")

        try:
            cmd = "7zg a -t7z " + "\"" + path+"\\"+nom7zip+"\" " + "\""+path+"\\"+"Contrôles"+date+"\\"+"\""
            print(nom7zip+".7z" + " à bien été créer !")
        except:
            print("Erreur lors du zippage")

        os.system(cmd)
        print()
        zipper = "non"

    envoisMail = input("Envoyer le mail (oui/non) : ")
    while envoisMail == "oui":
        if groupe == "":
            groupe = input("Votre groupe de classe ('A'/'B': ")
        myMail = input("Votre adresse gMail : ")
        mdp = input("Votre mdp : ")
        prenomDest = input("Prenom du destinataire : ")
        mailTo = input("Mail du destinataire ('Fx' pour lui envoyer à son adresse IMIE): ")
        if mailTo == "Fx":
            mailTo = "****************"
        objectMail = input("Objet du mail : ")
        print("Voici le contenu du mail : ")
        textMail = "Bonjour " + prenomDest +", \n\nLes contrôles du "+date+" sont en pièce jointe. \nBonne soirée.\n\nCordialement,\nLes "+ groupe
        print(textMail)
        modifMail = input("Souhaitez vous modifier le contenu de ce mail ?(oui/non) : ")
        i =0
        while modifMail== "oui":
            i+=1
            print("Taper le contenu de votre mail dans un fichier texte")
            pathMailTxt = input("Le chemin complet de votre fichier texte(ex : C:Prog\\Documents\\mail"+prenomDest+".txt) : ")
            try:
                with open(pathMailTxt, 'r') as textMail:
                    textMail = textMail.read()
            except:
                print("Erreur, fichier introuvable")
                continue

            print("Voici le contenu de votre mail : ")
            print(textMail)

            modifMail = input("Reproposer ('oui'/'non') : ")

        if nom7zip == "":
            nom7zip = input("Nom du .7z (doit être dans le dossier donné au début) : ")
        nom7zip += ".7z"

        try:
            fromaddr = myMail
            toaddr = mailTo
            msg = MIMEMultipart()
            msg['From'] = fromaddr
            msg['To'] = toaddr
            msg['Subject'] = objectMail
            body = textMail
            msg.attach(MIMEText(body, 'plain'))
            filename = nom7zip
            attachment = open(path + "\\" + nom7zip, "rb")

            part = MIMEBase('application', 'octet-stream')
            part.set_payload((attachment).read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', "attachment; filename= %s" % filename)

            msg.attach(part)

            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(fromaddr, mdp)
            text = msg.as_string()
            server.sendmail(fromaddr, toaddr, text)
            server.quit()
        except:
            print("Erreur lors de l'envois du mail")

        envoisMail = input("Taper 'Oui' pour renvoyer, 'Non' pour quitter")

    replay = input("Taper 'stop' pour arrêter le programme : ")
