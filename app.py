#DÉBUGÉ AVEC CLAUDE AI (m'a aidé avec les joins plus particulièrement)

import os
from flask import Flask, render_template,request, redirect, url_for
import mysql.connector
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

db = mysql.connector.connect(user = os.getenv("DB_USER"),
                             host = os.getenv("DB_HOST"),
                             port = int(os.getenv("DB_PORT")),
                             database = os.getenv("DB_NAME"),
                             password = os.getenv("DB_PASSWORD"))


@app.route('/')

def index():
    """
    Retourne la page d'accueil
    """
    return render_template('index.html')

@app.route('/commande')
def afficher_commande():
    """
    Retourne la page de prise de commande
    """
    return render_template('commande.html')

@app.route('/liste_commandes')
def afficher_liste_commandes():
    """
    Affiche la liste de commande avec le statut en attente de livraison et les classe en ordre de prise de commande
    Retourne: La liste de commande
    """
    requete ="""
            SELECT c.id, c.date_de_commande, c.adresse, cl.nom, 
            cl.numero_de_telephone, cr.nom AS croute, s.nom AS sauce,
                   GROUP_CONCAT(g.nom SEPARATOR ', ') AS garnitures
            FROM commandes c
            JOIN clients cl ON cl.id = c.id_client
            JOIN pizzas p ON p.id_commande = c.id
            JOIN croutes cr ON cr.id = p.id_croute
            JOIN sauces s ON s.id = p.id_sauce
            JOIN pizzas_garnitures pg ON pg.id_pizza = p.id
            JOIN garnitures g ON g.id = pg.id_garniture
            WHERE c.statut = %(statut)s
            GROUP BY c.id, c.date_de_commande, c.adresse, cl.nom,
                     cl.numero_de_telephone, cr.nom, s.nom
            ORDER BY c.date_de_commande
        """
    parametres = {"statut": "en attente de livraison"}

    curseur = db.cursor(dictionary = True)
    try:
        curseur.execute(requete, parametres)
        data = curseur.fetchall()
        return render_template('liste_commandes.html', data=data)
        curseur.close()
    except mysql.connector.Error as erreur:
        return render_template('erreur.html', erreur=erreur.msg)

@app.route('/resume', methods=['POST'])
def resume_commande():
    """
    Reprend les données soumisent et fait la vérification des données avant des soumettre. Permet aussi de revenir modifier
    Retourne: Au résumé de la commande
    """
    nom_complet = request.form['nom_complet']
    telephone = request.form['telephone']
    adresse = request.form['adresse']
    id_croute = request.form['croute_id']
    id_sauce = request.form['sauce_id']
    garnitures = request.form.getlist('garnitures')

    if len(garnitures)< 1 or len(garnitures)> 4:
        return render_template('erreur.html', erreur=f"Un choix de 1 et maximum 4 garnitures est imposé")

    curseur = db.cursor(dictionary=True)

    try:

        curseur.execute("SELECT nom FROM croutes WHERE id = %(id_croute)s", {"id_croute":id_croute})
        croute = curseur.fetchone()

        curseur.execute("SELECT nom FROM sauces WHERE id = %(id_sauce)s", {"id_sauce": id_sauce})
        sauce = curseur.fetchone()

        nom_garnitures = []
        for id_garniture in garnitures:
            curseur.execute("SELECT nom FROM garnitures WHERE id = %(id_garniture)s", {"id_garniture":id_garniture})
            garniture = curseur.fetchone()
            nom_garnitures.append(garniture["nom"])
        curseur.close()

    except mysql.connector.Error as erreur:
        return render_template('erreur.html', erreur=erreur.msg)

    return render_template('resume_commande.html', nom=nom_complet, telephone=telephone,
                           adresse=adresse, croute_id=id_croute, croute=croute["nom"],
                           sauce_id=id_sauce, sauce=sauce["nom"], id_garnitures=garnitures,
                           nom_garnitures=nom_garnitures)

@app.route('/confirme', methods=['POST'])
def soumettre_commande():
    """
    Soummet la commande
    Retourne: Retourne à l'accueil
    """
    nom_complet = request.form['nom_complet']
    telephone = request.form['telephone']
    adresse = request.form['adresse']
    id_croute = request.form['croute_id']
    id_sauce = request.form['sauce_id']
    garnitures = request.form.getlist('garnitures')


    if len(garnitures)< 1 or len(garnitures)> 4:
        return render_template('erreur.html', erreur=f"Un choix de 1 et maximum 4 garnitures est imposé")

    
    curseur = db.cursor(dictionary=True)

    try:

        curseur.execute(
            """SELECT id FROM clients WHERE nom = %(nom)s AND numero_de_telephone = %(telephone)s""",{"nom":nom_complet, "telephone":telephone})
            
        client = curseur.fetchone()
        if client:
            id_client = client["id"]
        else:
            curseur.execute("INSERT INTO clients(nom, numero_de_telephone) VALUES (%(nom)s, %(telephone)s)", {"nom":nom_complet,"telephone": telephone})
            id_client = curseur.lastrowid

        curseur.execute("INSERT INTO commandes (id_client, adresse) VALUES (%(id_client)s, %(adresse)s)", {"id_client":id_client,"adresse": adresse})
        id_commande = curseur.lastrowid

        curseur.execute("INSERT INTO pizzas (id_croute, id_sauce, id_commande) VALUES (%(id_croute)s, %(id_sauce)s, %(id_commande)s)", {"id_croute":id_croute,"id_sauce": id_sauce, "id_commande" :id_commande})
        id_pizza = curseur.lastrowid

        for id_garniture in garnitures:
            curseur.execute( "INSERT INTO pizzas_garnitures (id_pizza, id_garniture) VALUES (%(id_pizza)s, %(id_garniture)s)", {"id_pizza" :id_pizza, "id_garniture": id_garniture})

        db.commit()
        curseur.close()
        return redirect(url_for('index'))
    
    except mysql.connector.Error as erreur:
        db.rollback()
        return render_template('erreur.html', erreur=erreur.msg)
    
@app.route('/livrer/<int:id_commande>',  methods=['POST'])
def completer_livraison(id_commande):
    """
    Permet de completer une livraison
    Paramètre; id de la commande
    Retourne la liste de la commande qui est updatée
    """
    requete = "UPDATE commandes SET statut = %(statut)s WHERE id = %(id)s"
    parametres = {"statut": "livrée", "id": id_commande}

    curseur = db.cursor(dictionary=True)
    try:
        curseur.execute(requete, parametres)
        db.commit()
        curseur.close()
        return redirect(url_for('afficher_liste_commandes'))
    except mysql.connector.Error as erreur:
        db.rollback()
        return render_template('erreur.html', erreur=erreur.msg)

    
if __name__ == '__main__':
    app.run(debug=True)
