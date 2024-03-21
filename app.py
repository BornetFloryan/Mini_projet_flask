#! /usr/bin/python
# -*- coding:utf-8 -*-
import pymysql.cursors
import os
from datetime import datetime
from flask import Flask, request, render_template, redirect, flash, g, session

app = Flask(__name__)
app.secret_key = 'une cle(token) : grain de sel(any random string)'

def get_db():
    if 'db' not in g:
        g.db = pymysql.connect(
            host="localhost",  # à modifier
            user="root",  # à modifier
            password="root",  # à modifier
            database="BDD_fbornet",  # à modifier
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
    return g.db

@app.teardown_appcontext
def teardown_db(exception):
    db = g.pop('db', None)
    if db is not None:
        db.close()


@app.route('/')
def show_accueil():
    return render_template('layout.html')

@app.route('/categorie-depense/show')
def show_categorie_depense():
    mycursor = get_db().cursor()
    sql = '''SELECT * FROM categorie_depense;'''
    mycursor.execute(sql)
    categoriesDepenses = mycursor.fetchall()
    return render_template('categorie_depense/show_categorie_depense.html', categoriesDepenses=categoriesDepenses)

@app.route('/categorie-depense/add', methods=['GET'])
def add_categorie_depense():
    return render_template('categorie_depense/add_categorie_depense.html')

@app.route('/categorie-depense/add', methods=['POST'])
def valid_add_categorie_depense():
    libelle_categorie = request.form.get('libelle_categorie', '')
    mycursor = get_db().cursor()
    tab_insert=(libelle_categorie)
    sql = "INSERT INTO categorie_depense(id_categorie, libelle_categorie) VALUES (NULL, %s);"
    mycursor.execute(sql, tab_insert)
    get_db().commit()
    print(u'categorie ajoutée, libellé :', libelle_categorie)
    message = u'categorie ajoutée , libelle de la catégorie :'+libelle_categorie
    flash(message, 'alert-success')
    return redirect('/categorie-depense/show')

@app.route('/categorie-depense/delete1', methods=['GET'])
def delete_categorie_depense1():
    id_categorie = request.args.get('id_categorie', '')
    mycursor = get_db().cursor()
    sql = '''SELECT * FROM depense WHERE categorie_id = %s;'''
    mycursor.execute(sql, id_categorie)
    depenses = mycursor.fetchall()
    if (str(depenses) != '()'):
        print("Impossible de supprimer cette catégorie car elle possède des dépenses ! | id:", id_categorie)
        message = "Impossible de supprimer cet catégorie car elle possède des dépenses ! | id:" + id_categorie
        flash(message, 'alert-danger')
        return render_template('/categorie_depense/cascade.html', depenses=depenses)
    else:
        sql = '''DELETE FROM categorie_depense WHERE id_categorie=%s;'''
        mycursor.execute(sql, id_categorie)
        get_db().commit()
        print("Une catégorie supprimée ! | id:", id_categorie)
        message = 'Une catégorie supprimée ! | id:' + id_categorie
        flash(message, 'alert-warning')
        return redirect('/categorie-depense/show')

@app.route('/categorie-depense/delete2', methods=['GET'])
def delete_categorie_depense2():
    id_depense = request.args.get('id_depense')
    categorie_id = request.args.get('categorie_id')
    mycursor = get_db().cursor()
    sql_delete = ''' DELETE FROM depense WHERE id_depense = %s '''
    mycursor.execute(sql_delete, id_depense)
    get_db().commit()
    message = 'La dépense a été supprimée ! | id:' + id_depense
    flash(message, 'alert-warning')
    sql_select = ''' SELECT * FROM depense WHERE categorie_id = %s '''
    mycursor.execute(sql_select, categorie_id)
    depenses = mycursor.fetchall()
    if (str(depenses) == '()'):
        return redirect('/categorie-depense/show')
    else:
        return render_template('/categorie_depense/cascade.html', depenses=depenses)

@app.route('/categorie-depense/edit', methods=['GET'])
def edit_categorie_depense():
    id_categorie = request.args.get('id_categorie')
    libelle_categorie = request.args.get('libelle_categorie', '')
    mycursor = get_db().cursor()
    tuple_param = (id_categorie)
    sql = ''' SELECT * FROM categorie_depense WHERE id_categorie = %s;'''
    mycursor.execute(sql, tuple_param)
    categoriesDepense = mycursor.fetchone()

    return render_template('categorie_depense/edit_categorie_depense.html', categoriesDepense=categoriesDepense)

@app.route('/categorie-depense/edit', methods=['POST'])
def valid_edit_categorie_depense():
    id_categorie = request.form.get('id_categorie')
    libelle_categorie = request.form.get('libelle_categorie')
    tab_update = (libelle_categorie, id_categorie)
    mycursor = get_db().cursor()
    sql = ("UPDATE categorie_depense SET libelle_categorie = %s WHERE id_categorie = %s;")
    mycursor.execute(sql, tab_update)
    get_db().commit()

    print(u'categorie de dépense modifiée, id_categorie: ',id_categorie, " libelle_categorie :", libelle_categorie)
    message=u'categorie de dépense modifiée, id_categorie: ' + id_categorie + " libelle_categorie : " + libelle_categorie
    flash(message, 'alert-success')
    return redirect('/categorie-depense/show')

@app.route('/depense/show')
def show_depense():
    mycursor = get_db().cursor()
    sql = '''SELECT * FROM depense 
            JOIN categorie_depense ON categorie_depense.id_categorie = depense.categorie_id;'''
    mycursor.execute(sql)
    depenses = mycursor.fetchall()

    return render_template('depense/show_depense.html', depenses=depenses)

@app.route('/depense/add', methods=['GET'])
def add_depense():
    mycursor = get_db().cursor()
    sql = ''' SELECT id_categorie, libelle_categorie FROM categorie_depense;'''
    mycursor.execute(sql)
    categoriesDepenses = mycursor.fetchall()
    return render_template('depense/add_depense.html', categoriesDepenses=categoriesDepenses)

@app.route('/depense/add', methods=['POST'])
def valid_add_depense():
    id_depense = request.form.get('id_depense')
    destinataire_depense = request.form.get('destinataire_depense', '')
    montant = request.form.get('montant', '')
    description = request.form.get('description', '')
    date_depense = request.form.get('date_depense', '')
    id_categorie = request.form.get('id_categorie', '')
    destinataire = request.form.get('destinataire')
    image = request.form.get('image', '')

    tab_insert = (destinataire_depense, montant, description, date_depense, id_categorie, destinataire, image)
    mycursor = get_db().cursor()
    sql = "INSERT INTO depense(id_depense, destinataire_depense, montant, description, date_depense, categorie_id, destinataire, image) VALUES (NULL, %s, %s, %s, %s, %s, %s, %s);"
    mycursor.execute(sql, tab_insert)
    get_db().commit()

    print(u'Dépense ajoutée , Destinataire de la dépense: ', destinataire_depense, ' - id de la categorie de dépense :', id_categorie, ' - montant:', montant, ' - description:', description, ' - date de la dépense:', date_depense, ' - image:', image)
    message = u'Dépense ajoutée , destinataireDepense:'+destinataire_depense + '- categorieDepense_id :' + id_categorie + ' - montant:' + montant + ' - description:'+  description + ' - date_depense:' + date_depense + ' - image:' + image
    flash(message, 'alert-success')
    return redirect('/depense/show')

@app.route('/depense/delete', methods=['GET'])
def delete_depense():
    id_depense = request.args.get('id_depense')
    tab_delete = [id_depense]
    mycursor = get_db().cursor()
    sql = "DELETE FROM depense WHERE id_depense=%s;"
    mycursor.execute(sql, tab_delete)
    get_db().commit()

    message=u'une dépense supprimée, id_depense : ' + id_depense
    flash(message, 'alert-warning')
    return redirect('/depense/show')

@app.route('/depense/edit', methods=['GET'])
def edit_depense():
    id_depense = request.args.get('id_depense')
    tuple_param = (id_depense)
    mycursor = get_db().cursor()
    sql = '''SELECT DISTINCT categorie_depense.id_categorie, categorie_depense.libelle_categorie
        FROM categorie_depense
        LEFT JOIN depense ON categorie_depense.id_categorie = depense.categorie_id
        ORDER BY categorie_depense.id_categorie;'''
    mycursor.execute(sql)
    categoriesDepenses = mycursor.fetchall()
    sql = '''SELECT * FROM depense WHERE id_depense=%s;'''
    mycursor.execute(sql, tuple_param)
    depense = mycursor.fetchone()

    return render_template('depense/edit_depense.html', depense=depense, categoriesDepenses=categoriesDepenses)

@app.route('/depense/edit', methods=['POST'])
def valid_edit_depense():
    id_depense = request.form.get('id_depense', '')
    destinataire_depense = request.form.get('destinataire_depense', '')
    libelle_categorie = request.form.get('libelle_categorie')
    montant = request.form.get('montant', '')
    description = request.form.get('description', '')
    date_depense = request.form.get('date_depense', '')
    destinataire = request.form.get('destinataire', '')
    image = request.form.get('image', '')

    tab_insert = (destinataire_depense, montant, description, date_depense, libelle_categorie, destinataire, image, id_depense)
    mycursor = get_db().cursor()
    sql = "UPDATE depense SET destinataire_depense = %s, montant = %s, description = %s, date_depense = %s, categorie_id = %s, destinataire = %s, image = %s WHERE id_depense = %s;"
    mycursor.execute(sql, tab_insert)
    get_db().commit()

    print(u'dépense modifiée , destinataireDepense : ', destinataire_depense, ' - categorieDepense_id :', libelle_categorie, ' - montant:', montant, ' - description:', description, ' - date_depense:', date_depense, ' - image:', image)
    message = u'dépense modifiée , destinataireDepense:'+destinataire_depense + '- categorieDepense_id :' + libelle_categorie + ' - montant:' + montant + ' - description:' + description + ' - date_depense:' + date_depense + ' - image:' + image
    flash(message, 'alert-success')
    return redirect('/depense/show')


@app.route('/depense/filtre/show', methods=['GET'])
def show_depense_filtre():
    mycursor = get_db().cursor()
    sql = '''SELECT * FROM categorie_depense;'''
    mycursor.execute(sql)
    categoriesDepenses = mycursor.fetchall()

    sql_filtre = ''' SELECT d.destinataire_depense, d.description, d.image 
                    FROM depense d 
                    WHERE 1=1 '''
    tup_sql_filtre = ()

    if ("filter_word" in session) or ("filter_value_max" in session) or ("filter_value_min" in session) or ("filter_items" in session):
        if session.get("filter_word"):
            if session.get("filter_word").isalpha():
                if len(session.get('filter_word')) < 2:
                    flash(u'Votre mot recherché doit être composé de au moins 2 lettre', 'alert-warning')
                    return redirect("/depense/filtre/suppr")
                sql_filtre += "AND d.destinataire_depense LIKE %s "
                tup_sql_filtre += (f"%{session.get('filter_word')}%",)
            else:
                flash(u'Votre mot recherché doit uniquement être composé de lettres', 'alert-warning')
                return redirect("/depense/filtre/suppr")
            
        if session.get("filter_value_max") and session.get("filter_value_min"):
            if not isinstance(session.get("filter_value_max"), (int, float)) or not isinstance(session.get("filter_value_min"), (int, float)):
                flash(u'min et max doivent être des numériques', 'alert-warning')
                return redirect("/depense/filtre/suppr")

            if session.get("filter_value_min") > session.get("filter_value_max"):
                flash(u'min < max', 'alert-warning')
                return redirect("/depense/filtre/suppr")
            
            sql_filtre += "AND d.montant BETWEEN %s AND %s "
            tup_sql_filtre += (session.get("filter_value_min"), session.get("filter_value_max"))
        else:
            if session.get("filter_value_min"):
                sql_filtre += "AND d.montant >= %s "
                tup_sql_filtre += (session.get("filter_value_min"),)

            if session.get("filter_value_max"):
                sql_filtre += "AND d.montant <= %s "
                tup_sql_filtre += (session.get("filter_value_max"),)
        
        if session.get("filter_items"):
            temp = session.get("filter_items")
            for i in range(len(temp)):
                if i == 0:
                    sql_filtre += "AND d.categorie_id = %s "
                else:
                    sql_filtre += "OR d.categorie_id = %s "
                tup_sql_filtre += (temp[i],)
        
        mycursor.execute(sql_filtre, tup_sql_filtre)
        depenses = mycursor.fetchall()
    else:
        sql = ''' SELECT d.destinataire_depense, d.description, d.image 
                    FROM depense d '''
        mycursor.execute(sql)
        depenses = mycursor.fetchall()

    return render_template('depense/front_depense_filtre_show.html', categoriesDepenses=categoriesDepenses, depenses=depenses)

@app.route('/depense/filtre/show', methods=['POST'])
def valid_depense_filtre():
    filter_word = request.form.get('filter_word', None)
    filter_value_min = request.form.get('filter_value_min', None)
    filter_value_max = request.form.get('filter_value_max', None)
    filter_items = request.form.getlist('filter_items')

    depense_suppr_filtre()

    if filter_word:
        session["filter_word"] = str(filter_word)

    if filter_value_min:
        session["filter_value_min"] = int(filter_value_min)

    if filter_value_max:
        session["filter_value_max"] = int(filter_value_max)

    if filter_items:
        session["filter_items"] = [int(elt) for elt in filter_items]

    sql_filtre = ''' SELECT d.destinataire_depense, d.description, d.image 
                    FROM depense d 
                    WHERE 1=1 '''
    tup_sql_filtre = ()

    if ("filter_word" in session) or ("filter_value_max" in session) or ("filter_value_min" in session) or ("filter_items" in session):
        if session.get("filter_word"):
            if session.get("filter_word").isalpha():
                if len(session.get('filter_word')) < 2:
                    flash(u'Votre mot recherché doit être composé de au moins 2 lettres', 'alert-warning')
                    return redirect("/depense/filtre/suppr")
                sql_filtre += "AND d.destinataire_depense LIKE %s "
                tup_sql_filtre += (f"%{session.get('filter_word')}%",)
            else:
                flash(u'Votre mot recherché doit uniquement être composé de lettres', 'alert-warning')
                return redirect("/depense/filtre/suppr")
            
        if session.get("filter_value_max") and session.get("filter_value_min"):
            if not isinstance(session.get("filter_value_max"), (int, float)) or not isinstance(session.get("filter_value_min"), (int, float)):
                flash(u'min et max doivent être des numériques', 'alert-warning')
                return redirect("/depense/filtre/suppr")

            if session.get("filter_value_min") > session.get("filter_value_max"):
                flash(u'min < max', 'alert-warning')
                return redirect("/depense/filtre/suppr")
            
            sql_filtre += "AND d.montant BETWEEN %s AND %s "
            tup_sql_filtre += (session.get("filter_value_min"), session.get("filter_value_max"))
        else:
            if session.get("filter_value_min"):
                sql_filtre += "AND d.montant >= %s "
                tup_sql_filtre += (session.get("filter_value_min"),)

            if session.get("filter_value_max"):
                sql_filtre += "AND d.montant <= %s "
                tup_sql_filtre += (session.get("filter_value_max"),)
        
        if session.get("filter_items"):
            temp = session.get("filter_items")
            for i in range(len(temp)):
                if i == 0:
                    sql_filtre += "AND d.categorie_id = %s "
                else:
                    sql_filtre += "OR d.categorie_id = %s "
                tup_sql_filtre += (temp[i],)


    mycursor = get_db().cursor()
    sql = '''SELECT * FROM categorie_depense;'''
    mycursor.execute(sql)
    categoriesDepenses = mycursor.fetchall()

    mycursor.execute(sql_filtre, tup_sql_filtre)
    depenses = mycursor.fetchall()

    return render_template('depense/front_depense_filtre_show.html', depenses=depenses, categoriesDepenses=categoriesDepenses)

@app.route('/depense/filtre/suppr')
def depense_suppr_filtre():
    session.pop('filter_word', None)
    session.pop('filter_value_min', None)
    session.pop('filter_value_max', None)
    session.pop('filter_items', None)
    return redirect('/depense/filtre/show')

@app.route('/depense/etat')
def depense_etat():
    print('''affichage de l'état''')
    mycursor = get_db().cursor()
    sql = ''' SELECT COUNT(DISTINCT id_depense) AS dep, SUM(montant) AS prix
                FROM depense;'''
    mycursor.execute(sql)
    depenses = mycursor.fetchone()

    mycursor2 = get_db().cursor()
    sql = '''SELECT id_categorie, libelle_categorie, COUNT(DISTINCT depense.id_depense) AS dep_i, SUM(depense.montant) AS prix_i
            FROM categorie_depense
            LEFT JOIN depense ON categorie_depense.id_categorie = depense.categorie_id
            GROUP BY id_categorie, libelle_categorie;'''
    mycursor2.execute(sql)
    categorie_depenses = mycursor2.fetchall()

    return render_template('depense/etat_depense.html', depenses=depenses, categorie_depenses=categorie_depenses)

if __name__ == '__main__':
    app.run(debug=True, port=5000)