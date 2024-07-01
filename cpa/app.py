from flask import Flask, render_template, request, redirect, url_for, session, jsonify, json 
from flask_mysqldb import MySQL
import MySQLdb.cursors
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# MySQL Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'pass_root'
app.config['MYSQL_DB'] = 'db_cpa'
app.config['MYSQL_PORT'] = 3307

mysql = MySQL(app)

# Example mapping function (you should adjust this based on your actual data)
def map_element_id_to_text(element_id):
    element_mappings = {
        '0': 'Un justificatif d\'activité pour les professions libérales (Copie d\'Agrément et Copie d\'Inscription au tableau d\'ordre).',
        '1': 'Copie de la pièce d\'identité biométrique du Gérant/passeport pour les étrangers.',
        '2': 'Copie de la pièce d\'identité biométrique du Gérant/passeport pour les étrangers et la carte de séjour en cour validité.',
        '3': 'Statut initial et ses modificatifs.',
        '4': 'Copie du Registre de commerce et/ou copie de l\'agrément présenté, le cas échéant.',
        '5': 'Carte d\'artisanat pour un artisan.',
        '6': 'Lettre d\'engagement remplie par la relation et spécimen de signature.',
        '7': 'SYRON KYC pour (société, gérants associés) et sa fiche appropriée remplie par la relation (questionnaire).',
        '8': 'FATCA.',
        '9': 'Consultation Fichier clientèle et Interdit chéquier.',
        '10': 'Copie du Numéro d\'Identification Fiscale (NIF) et Numéro d\'Identification Statistiques (NIS) présentés.',
        '11': 'Décision de désignation des personnes habilitées à faire fonctionner le compte (Bac 14)/Procuration notariée pour tiers / BAC 14.',
        '12': 'Consultation Hors périmètre.',
        '13': 'Résidence.',
        '14': 'Avis de la DOPEX ou préalable pour Import/Export et Personnes Étrangères.',
        '15': 'Copie de la pièce d\'identité biométrique du Président et trésorier.',
        '16': 'Copie de l\'agrément de l\'association délivré par l\'autorité compétente et publié dans un journal quotidien.',
        '17': 'Statuts de l\'association et liste des personnes chargées de son administration et ses modificatifs.',
        '18': ' Copie de la piéce d\'identité biométrique du Gérant/passeport pour les étrangers"',
        '19': 'Demande d\'ouverture compte connaissance du client et la convention de compte',
        '20': 'Copie du Registre de commerce et/ou copie de l\'agrément présenté, le cas échéant.',
        '21': 'Carte d\'artisanat pour un artisan.',
        '22': 'Un justificatif d\'activité pour les professions libérales (Copie d\'Agrément et Copie d\'Inscription au tableau d\'ordre ).',
        '23': 'Lettre d\'engagement remplir par la relation et spécimen de signature (CA109)"',
        '24': 'SYRON KYC pour (société, gérants associées) et sa fiche approprie remplir par la relation (questionnaire).',
        '25': 'FATCA',
        '26': 'Consultation Fichier clientèle et Interdit chéquier.',
        '27': 'Décision de désignation des personnes habilitées à faire fonctionner le compte (Bac 14)/Procuration notariée pour tiers / BAC 14.',
        '28': 'Copie du Numéro d\'Identification Fiscale (NIF) et Numéro d\'Identification Statistiques (NIS) présentés.',
        '29': 'Consultation Hors périmètre',
        '30': 'Résidence',
        '31': ' Avis de la DOPEX ou préalable pour Import/Export et Personnes Etranger.',
        '32': 'Contrat de travail , Autorisation de travail pour l\'étranger et carte de séjour en cour de validité.'
        # Add more mappings as needed
    }
    return element_mappings.get(str(element_id), f'{element_id}')  # Return the description or a default message if not found

# Route to render the login form
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle login form submission
@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT folio, mdp, nom, prenom, qualite FROM utilisateur WHERE folio = %s AND mdp = %s", (username, password))
        user = cur.fetchone()
        cur.close()

        if user:
            print(f"User data fetched: {user}")  # Print user data for debugging
            if 'qualite' in user:
                qualite = user['qualite']
                session['folio'] = user['folio']  # Store folio in session
                if qualite == 'Secrétaire':
                    return redirect(url_for('secretaire'))
                elif qualite == 'Charge étude':
                    return redirect(url_for('etude'))
                elif qualite == 'Charge de validation':
                    return redirect(url_for('validation'))
                elif qualite == 'Directeur':
                    return redirect(url_for('directeur'))
                else:
                    print(f"Unknown qualite: {qualite}")  # Debug print for unknown roles
                    return render_template('index.html')
            else:
                print("Qualite not found in user data")  # Print debug message if qualite is missing
                return render_template('index.html')  # Render index.html or handle as needed
        else:
            print("User not found or incorrect password")  # Print debug message for login failure
            return render_template('index.html')  # Render index.html or handle as needed

# Route to render secretaire.html and handle form submission
@app.route('/secretaire', methods=['GET', 'POST'])
def secretaire():
    if request.method == 'POST':
        # Fetch form data
        id_client = request.form['id_client'] or None
        num_compte = request.form['num_compte'] or None
        nom = request.form['nom'] or None
        prenom = request.form['prenom'] or None
        raison_sociale = request.form['raison_sociale'] or None
        activite = request.form['activite'] or None
        adresse = request.form['adresse'] or None
        numerotel = request.form['numerotel'] or None
        date_ouverture = request.form['date_ouverture'] or None
        date_cloture = request.form['date_cloture'] or None
        cause = request.form['cause'] or None
        num_reg_com = request.form['num_reg_com'] or None
        date_reg_com = request.form['date_reg_com'] or None
        code_agence = request.form['code_agence'] 

        # Assuming this is from the session date
        daterecp = request.form['date_reception']  
        # Fetch from form if available
        dateenvoi = datetime.now().strftime('%Y-%m-%d')  
        # Fetch from form if available
        etat = None  
        # Fetch from form if available
        descriptif = None
        folio = session.get('folio')  # Retrieve folio from session

        try:
            # Insert into MySQL
            cur = mysql.connection.cursor()

            # Insert into dossier table
            cur.execute("""
                INSERT INTO dossier (ID_CLIENT, NUM_COMPTE, NOM, PRENOM, RAISON_SOCIALE, ACTIVITE, ADRESSE, NUMEROTEL, DATE_OUVERTURE, DATE_CLOTURE, CAUSE, NUM_REG_COM, DATE_REG_COM, CODE_AGENCE)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                        (id_client, num_compte, nom, prenom, raison_sociale, activite, adresse, numerotel, date_ouverture, date_cloture, cause, num_reg_com, date_reg_com, code_agence))
            mysql.connection.commit()

            # Insert into datetransmis table
            cur.execute("""
                INSERT INTO datetransmis (DATERECP, DATEENVOI, ETAT, DESCRIPTIF, ID_CLIENT, FOLIO)
                VALUES (%s, %s, %s, %s, %s, %s)""",
                        (daterecp, dateenvoi, etat, descriptif, id_client, folio))
            mysql.connection.commit()

            cur.close()
            return 'Successfully submitted dossier form!'
        
        except Exception as e:
            # Handle exceptions (e.g., database errors)
            print(f"Error submitting dossier form: {str(e)}")
            return 'An error occurred while processing the form. Please try again later.', 500

    # Handle GET request (render form)
    return render_template('secretaire.html')

@app.route('/etude', methods=['GET', 'POST'])
def etude():
    if request.method == 'POST':
        cur = mysql.connection.cursor()

        # Fetch id_client and other form data
        num_compte = request.form.get('id_client')
        datereception = request.form.get('datereception')
        conformity = request.form.get('conformity')
        folio = session.get('folio')
        dateenvoi = datetime.now().strftime('%Y-%m-%d') 

        cur.execute("SELECT id_client FROM dossier WHERE num_compte=%s;", (num_compte,))
        result = cur.fetchone()
        if result:
            id_client = result[0]
        else:
            # Handle the case where no matching id_client is found
            print(f"No id_client found for num_compte: {num_compte}")
            return 'No matching client found.', 400

        # Collect elements marked as 'nexistepas'
        elements = []
        for i in range(0, 33):  # Adjust the range based on your form's element count
            key_element = f'element{i}'
            if request.form.get(key_element) == 'nexistepas':
                elements.append((id_client, i))  # Include id_client and element number
        
        autre_texte = None
        
        if request.form.get('other') == 'autre':
            autre_texte = request.form.get('autreTexte')
            elements.append((id_client, autre_texte))
        
        try:
            # Insert into docs table
            sql = "INSERT INTO docs (id_client, element) VALUES (%s, %s)"
            for element in elements:
                cur.execute(sql, element)  # Execute query with each element tuple
                mysql.connection.commit()

            cur.execute("""
                INSERT INTO datetransmis (DATERECP, DATEENVOI, ETAT, DESCRIPTIF, ID_CLIENT, FOLIO)
                VALUES (%s, %s, %s, %s, %s, %s)""",
                        (datereception, dateenvoi, conformity, autre_texte, id_client, folio))
            mysql.connection.commit()

            cur.close()
            return render_template('etude.html')
        
        except Exception as e:
            # Handle exceptions (e.g., database errors)
            print(f"Error submitting etude form: {str(e)}")
            return 'An error occurred while processing the form. Please try again later.', 500

    # Handle GET request (render form)
    return render_template('etude.html')

@app.route('/today_dossiers')
def today_dossiers():
    try:
        cur = mysql.connection.cursor()
        cur.execute("""
            SELECT d.num_compte, d.nom, d.prenom, dt.daterecp, dt.dateenvoi, dt.folio, dt.etat, dt.descriptif
            FROM dossier d, datetransmis dt
            where d.id_client = dt.id_client
            and DATE(dt.daterecp) = CURDATE() OR DATE(dt.dateenvoi) = CURDATE()
        """)
        dossiers = cur.fetchall()
        cur.close()

        # Convert data to a list of dictionaries for JSON serialization
        dossiers_list = [{'num_compte': row[0], 'nom': row[1], 'prenom': row[2], 'date_reception': row[3], 'date_envoi': row[4], 'folio': row[5], 'etat': row[6], 'descriptif': row[7]} for row in dossiers]

        return jsonify(dossiers_list)

    except Exception as e:
        print(f"Error fetching today's dossiers: {e}")
        return jsonify([])

    
@app.route('/get_agences')
def get_agences():
    try:
        
        cursor = mysql.connection.cursor()
        query = "SELECT Code, intitule FROM agence;"
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        
        if result:
            data = [{'code': row[0], 'intitule': row[1]} for row in result]
            return jsonify(data)
        else:
            return jsonify([])
    except Exception as e:
        print(f"Error fetching agences: {e}")
        return jsonify([])

@app.route('/validation')
def validation():
    try:
        cur = mysql.connection.cursor()
        cur.execute("""
 SELECT d.num_compte, dt.etat, dt.descriptif, dt.folio, GROUP_CONCAT(e.element) AS elements
            FROM datetransmis dt
            INNER JOIN dossier d ON d.id_client = dt.id_client
            LEFT JOIN docs e ON e.id_client = d.id_client
            WHERE dt.etat IN ('conforme', 'nonconforme')
              AND d.num_compte NOT IN (
                  SELECT DISTINCT d2.num_compte
                  FROM datetransmis dt2
                  INNER JOIN dossier d2 ON d2.id_client = dt2.id_client
                  WHERE dt2.etat = 'valide'
              )
            GROUP BY d.num_compte, dt.etat, dt.descriptif, dt.folio
        """)
        dossiers = cur.fetchall()
        cur.close()

        dossiers_list = []
        for row in dossiers:
            dossier = {
                'num_compte': row[0],
                'etat': row[1],
                'descriptif': row[2],
                'folio': row[3],
                'elements': [map_element_id_to_text(element_id) for element_id in row[4].split(',')] if row[4] else []  # Map element IDs to descriptions
            }
            dossiers_list.append(dossier)

        return render_template('validation.html', dossiers=dossiers_list)

    except Exception as e:
        print(f"Error fetching dossiers: {e}")
        return 'An error occurred while processing the request.'

@app.route('/validate', methods=['POST'])
def validate_dossier():
    try:
        cur = mysql.connection.cursor()
        datereception=request.form.get('datereception')
        folio = session.get('folio')
        dateenvoi = datetime.now().strftime('%Y-%m-%d') 
        num_compte = request.form.get('num_compte')
        cur.execute("SELECT id_client FROM dossier WHERE num_compte=%s;", (num_compte,))
        id_client = cur.fetchone()[0]

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO datetransmis (DATERECP, DATEENVOI, ETAT, DESCRIPTIF, ID_CLIENT, FOLIO) VALUES (%s, %s, 'valide', 'NULL', %s, %s)", (datereception, dateenvoi, id_client,folio,))
        mysql.connection.commit()
        cur.close()

        return redirect(url_for('validation'))  # Redirect to validation page after insertion

    except Exception as e:
        print(f"Error validating dossier: {e}")
        return 'An error occurred while processing the validation.'
    
@app.route('/directeur')
def directeur():
    return render_template('directeur.html')

if __name__ == '__main__':
    app.run(debug=True)




# ani nkhdam b flaskext   chofi page etude hadik autre makantch tmchi tsma sagamtha 
# @app.route('/etude', methods=['GET', 'POST'])
# def ch_etude():
#     if request.method == 'POST':
#         cur = mysql.connection.cursor()

#         # Récupération de id_client et autres données du formulaire
#         num_comp = request.form.get('num_com')
#         cur.execute("SELECT idclient , datereception FROM dossier WHERE num_compte=%s;", (num_comp,))
#         row = cur.fetchone()

#         if row is None:
#             cur.close()
#             return 'Aucun client trouvé avec l\'identifiant fourni.', 404
        
#         id_client = row['idclient']
#         datereception = row['datereception']
        
#         # Collecte des éléments marqués comme 'nexistepas'
#         elements = []
#         for i in range(0, 33):  # Ajustez la plage en fonction du nombre d'éléments dans votre formulaire
#             key_element = f'element{i}'
#             if request.form.get(key_element) == 'nexistepas':
#                 elements.append((id_client, i))  # Inclure id_client et le numéro d'élément
        
#         # Déterminer quel textarea utiliser en fonction de la sélection de l'utilisateur
#         personne_type = request.form.get('personne')
#         autre_texte = None
        
#         if personne_type == 'morale':
#             autre_texte = request.form.get('autreTexteMorale')
#         elif personne_type == 'physique':
#             autre_texte = request.form.get('autreTextePhysique')
        
#         if autre_texte:
#             elements.append((id_client, autre_texte))
        
#         try:
#             # Insérer dans la table docs
#             sql = "INSERT INTO docs (idclient, element) VALUES (%s, %s)"
#             for element in elements:
#                 cur.execute(sql, element)  # Exécuter la requête avec chaque tuple d'élément
#                 mysql.connection.commit()

#             # Insérer dans la table datetransmis
#             cur.execute("""
#                 INSERT INTO datetransmis (DATERECP, DATEENVOI, ETAT, DESCRIPTIF, IDCLIENT, FOLIO)
#                 VALUES (%s, %s, %s, %s, %s, %s)""",
#                         (datereception, datetime.now().strftime('%Y-%m-%d'), request.form.get('conformity'), autre_texte, id_client, session.get('folio')))
#             mysql.connection.commit()

#             cur.close()
#             return render_template('etude.html', num_com=num_comp, datereception=datereception)
        
#         except Exception as e:
#             # Gérer les exceptions (par exemple, les erreurs de base de données)
#             print(f"Erreur lors de la soumission du formulaire d'étude : {str(e)}")
#             return 'Une erreur est survenue lors du traitement du formulaire. Veuillez réessayer plus tard.', 500

#     # Gérer la requête GET (afficher le formulaire)
#     return render_template('etude.html')

# *******************************************************
# @app.route('/today_dossiers')
# def today_dossiers():
#     try:
#         cur = mysql.connect().cursor()
#         cur.execute("""
#             SELECT d.num_compte, d.nom, d.prenom, dt.daterecp, dt.dateenvoi
#             FROM dossier d
#             JOIN datetransmis dt ON d.idclient = dt.idclient
#             WHERE DATE(dt.daterecp) = CURDATE() OR DATE(dt.dateenvoi) = CURDATE()
#         """)
#         dossiers = cur.fetchall()
#         cur.close()
        
#         # Convert data to a list of dictionaries for JSON serialization
#         dossiers_list = [{'num_compte': row[0], 'nom': row[1], 'prenom': row[2], 'date_reception': row[3], 'date_envoi': row[4]} for row in dossiers]
        
#         return jsonify(dossiers_list)
    
#     except Exception as e:
#         print(f"Error fetching today's dossiers: {e}")
#         return jsonify([])
#         #NESRIIIINIE ANA HNA NI NKHDAM B flaskext DONC NTI VERIFIER 9BL#
# ****************************************************************************
# @app.route('/validation')
# def validation():
#     return render_template('validation.html')

# @app.route('/directeur')
# def directeur():
#     return render_template('directeur.html')

# if __name__ == '__main__':
#     app.run(debug=True)
