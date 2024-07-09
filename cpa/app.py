from flask import Flask, render_template, request, redirect, url_for, session, jsonify, send_file
from flask_mysqldb import MySQL
import MySQLdb.cursors
from datetime import datetime
import pandas as pd
from io import BytesIO

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
    
@app.route('/download_excel', methods=['GET'])
def download_excel():
    try:
        cur = mysql.connect.cursor()
        cur.execute("""
            SELECT d.num_compte, d.nom, d.prenom, dt.daterecp, dt.dateenvoi, dt.etat, dt.descriptif, dt.folio
            FROM datetransmis dt
            INNER JOIN dossier d ON d.id_client = dt.id_client
        """)
        dossiers = cur.fetchall()
        cur.close()

        # Create a DataFrame from the fetched data
        df = pd.DataFrame(dossiers, columns=['Numéro de Compte', 'Nom', 'Prénom', 'Date de Réception', 'Date d\'Envoi', 'État', 'Descriptif', 'Folio'])

        # Save the DataFrame to an Excel file
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Dossiers')
        output.seek(0)

        return send_file(output, download_name='dossiers.xlsx', as_attachment=True)

    except Exception as e:
        print(f"Error generating Excel file: {e}")
        return 'An error occurred while generating the Excel file.', 500
    
@app.route('/envoiversag', methods=['GET', 'POST'])
def envoiversagence():
    return render_template('envoiversag.html')
@app.route('/to_agence', methods=['POST'])
def to_agence():
    date_envoi = request.form['date_envoi']
    num_compte = request.form['num_compte']
    agence = request.form['agence']
    print(agence)
    
    try:
        cursor = mysql.connect.cursor()

        # Query to get id_client based on num_compte
        cursor.execute("SELECT id_client FROM dossier WHERE num_compte=%s;", (num_compte,))
        result = cursor.fetchone()
        
        if result is None:
            print("No id_client found for the given num_compte")
            return render_template('envoiversag.html')  # Handle this case appropriately
        
        id_client = result[0]
        print(id_client)

        folio = session.get('folio')  # Ensure folio is retrieved from session

        if not folio:
            print("Folio not found in session")
            return render_template('envoiversag.html')  # Handle this case appropriately

        # Insert into datetransmis
        insert_query = """
        INSERT INTO datetransmis (descriptif, id_client, folio, date_agence) 
        VALUES (%s, %s, %s, %s)
        """
        cursor.execute(insert_query, (agence, id_client, folio, date_envoi))
        mysql.connect.commit()

    except Exception as e:
        print(f"An error occurred: {e}")
        mysql.connect.rollback()
        return render_template('envoiversag.html')  # Handle this case appropriately

    finally:
        cursor.close()
        mysql.connect.close()

    return render_template('envoiversag.html')  # Redirect to a success page or another route



@app.route('/directeur', methods=['GET'])
def directeur():
    cur = mysql.connect.cursor()

    # Query to get dossier details
    query = """
    SELECT d.id_client, d.num_compte, dt.daterecp, dt.dateenvoi, dt.etat, dt.folio
    FROM dossier d
    LEFT JOIN datetransmis dt ON d.id_client = dt.id_client
    """
    cur.execute(query)
    dossiers = cur.fetchall()
    cur.close()


    # Print fetched data to debug
    print("Fetched Dossiers:", dossiers)

    if dossiers:
        dossier_details = [{
            'id_client': dossier[0],
            'num_compte': dossier[1],
            'daterecp': dossier[2],
            'dateenvoi': dossier[3],
            'etat': dossier[4],
            'folio': dossier[5]
        } for dossier in dossiers]
        return jsonify(dossier_details)
    else:
        return jsonify([]), 404

@app.route('/directeur_page', methods=['GET'])
def directeur_page():
    return render_template('directeur.html')

if __name__ == '__main__':
    app.run(debug=True)



/***********************************************************************/
LES UPDATES RAM HNAAAAAAA !!!!!!!!!!!!!!!!!!!!
@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        try:
            conn = mysql.connect()
            cur = conn.cursor()
            cur.execute("SELECT folio, mdp, nom, prenom, qualite FROM utilisateur WHERE folio = %s AND mdp = %s", (username, password))
            user = cur.fetchone()  # Fetch one row

            if user:  # Check if user exists
                print(f"User data fetched: {user}")  # Debug print for user data
                qualite = user[4]  # Accessing qualite from tuple
                session['folio'] = user[0]  # Store folio in session
                if qualite == 'Secrétaire':
                    return render_template('secretaire.html', user=user)  # Pass user to template
                elif qualite == 'Charge étude':
                    return render_template('etude.html', user=user)
                elif qualite == 'Charge de validation':
                    return render_template('validation.html', user=user)
                elif qualite == 'Directeur':
                    return render_template('directeur.html', user=user)
                else:
                    print(f"Unknown qualite: {qualite}")  # Debug print for unknown roles
                    return render_template('index.html')
            else:
                print("User not found or incorrect password")  # Print debug message for login failure
                return render_template('index.html')  # Render index.html or handle as needed

        except Exception as e:
            print(f"Error executing MySQL query: {e}")
            return render_template('index.html')
        finally:
            cur.close()  # Close cursor
            conn.close()  # Close connection

        
@app.route('/get_agences')
def get_agences():
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        query = "SELECT Code, intitule FROM agence;"
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        if result:
            data = [{'code': row[0], 'intitule': row[1]} for row in result]
            return json.dumps(data)
        else:
            return json.dumps([])
    except Exception as e:
        print(f"Error fetching agences: {e}")
        return json.dumps([])


@app.route('/secretaire', methods=['GET', 'POST'])
def secretaire():
    if request.method == 'POST':
        # Handle form submission
        try:
            conn = mysql.connect()
            cur = conn.cursor()

            # Extract form data
            id_client = request.form['id_client']
            num_compte = request.form['num_compte']
            nom = request.form['nom'] or None
            prenom = request.form['prenom'] or None
            agence_id = request.form['agence']
            raison_sociale = request.form['raison_sociale'] or None
            activite = request.form['activite'] or None
            adresse = request.form['adresse']
            numerotel = request.form['numerotel']
            date_ouverture = request.form['date_ouverture']
            date_cloture = request.form['date_cloture'] or None
            cause = request.form['cause'] or None
            num_reg_com = request.form['num_reg_com']
            date_reg_com = request.form['date_reg_com']
            code_agence = request.form['code_agence']
            daterecp = request.form['date_reception']

            dateenvoi = datetime.now().strftime('%Y-%m-%d')
            etat = None
            descriptif = None
            folio = session.get('folio')

            # Insert into dossier table
            cur.execute("""
                INSERT INTO dossier (id_client, raison_sociale, nom, prenom, num_compte, agence, ACTIVITE, date_ouverture, DATE_CLOTURE, adresse, NUMEROTEL, CAUSE, NUM_REG_COM, DATE_REG_COM, CODE_AGENCE)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                        (id_client, raison_sociale, nom, prenom, num_compte, agence_id, activite, date_ouverture, date_cloture, adresse, numerotel, cause, num_reg_com, date_reg_com, code_agence))

            # Insert into datetransmis table
            cur.execute("""
                INSERT INTO datetransmis (DATERECP, DATEENVOI, ETAT, DESCRIPTIF, FOLIO, id_client)
                VALUES (%s, %s, %s, %s, %s, %s)""",
                        (daterecp, dateenvoi, etat, descriptif, folio, id_client))

            conn.commit()
            cur.close()

            return redirect(url_for('secretaire'))

        except Exception as e:
            print(f"Error submitting dossier form: {e}")
            return 'An error occurred while submitting the dossier form.'

    else:
        # Fetch the user's details from the database
        folio = session.get('folio')
        try:
            conn = mysql.connect()
            cur = conn.cursor()
            cur.execute("SELECT nom, prenom, mdp FROM utilisateur WHERE folio = %s AND qualite = 'Secrétaire'", (folio,))
            user = cur.fetchone()
            cur.close()
        except Exception as e:
            print(f"Error fetching user details: {e}")
            user = None

        return render_template('secretaire.html', user=user)

@app.route('/enversag')
def envversagence(): 
    return render_template('envoiversag.html')
   
@app.route('/envoiversag', methods=['GET', 'POST'])
def envoiversagence():
    folio = session.get('folio')
    user_info = None
    try:
        conn = mysql.connect()
        cur = conn.cursor()
        cur.execute("SELECT nom, prenom, mdp FROM utilisateur WHERE folio = %s AND qualite = 'Secrétaire'", (folio,))
        user_info = cur.fetchone()
        cur.close()
    except Exception as e:
        print(f"Error fetching user details: {e}")
    finally:
        conn.close()  # Always close the connection
    
    print(user_info)  # Check what data is retrieved from the database
    
    return render_template('envoiversag.html', user_info=user_info)

@app.route('/to_agence', methods=['POST'])
def to_agence():
    date_envoi = request.form['date_envoi']
    num_compte = request.form['num_compte']
    agence = request.form['agence']
    
    conn = mysql.connect()
    cursor = conn.cursor()

    # Query to get id_client based on num_compte
    query = "SELECT id_client FROM dossier WHERE num_compte = %s"
    cursor.execute(query, (num_compte,))
    result = cursor.fetchone()

    if result:
        id_client = result[0]
        folio = session.get('folio')  # Ensure folio is retrieved from session

        if folio is None:
            cursor.close()
            conn.close()
            return "Folio is missing from session", 400

        # Insert into datetransmis
        insert_query = "INSERT INTO datetransmis (dateenvoi, id_client, nom_agence, folio) VALUES (%s, %s, %s, %s)"
        cursor.execute(insert_query, (date_envoi, id_client, agence, folio))
        conn.commit()

        # Fetch user info again to keep displaying it
        user_info = None
        try:
            cur = conn.cursor()
            cur.execute("SELECT nom, prenom, mdp FROM utilisateur WHERE folio = %s AND qualite = 'Secrétaire'", (folio,))
            user_info = cur.fetchone()
            cur.close()
        except Exception as e:
            print(f"Error fetching user details: {e}")

        cursor.close()
        conn.close()

        return render_template('envoiversag.html', user_info=user_info)  # Render the template with user_info
    else:
        cursor.close()
        conn.close()
        return "Num compte not found", 404  # Return an error if num_compte not found
    @app.route('/get_dossier_details', methods=['POST'])
def get_dossier_details():
    try:
        num_compte = request.form['num_compte']
        
        conn = mysql.connect()
        cursor = conn.cursor()

        # Query to get dossier details with conditionally displaying elements
        dossier_query = """
        SELECT 
            d.num_compte, 
            dt.daterecp, 
            dt.dateenvoi, 
            dt.etat, 
            dt.descriptif, 
            dt.folio, 
            d.agence, 
            d.nom, 
            d.prenom, 
            CASE 
                WHEN dt.etat = 'conforme' THEN NULL
                ELSE doc.element
            END AS element_display
        FROM dossier d
        LEFT JOIN datetransmis dt ON d.id_client = dt.id_client
        LEFT JOIN docs doc ON d.id_client = doc.id_client
        WHERE d.num_compte = %s
          AND dt.folio = (SELECT folio FROM utilisateur WHERE qualite = 'Charge Étude')
        ORDER BY dt.daterecp ASC
        """
        cursor.execute(dossier_query, (num_compte,))
        dossiers = cursor.fetchall()
        cursor.close()

        if dossiers:
            dossier_details = [{
                'num_compte': dossier[0],
                'daterecp': dossier[1],
                'dateenvoi': dossier[2],
                'etat': dossier[3],
                'descriptif': dossier[4],
                'folio': dossier[5],
                'agence': dossier[6],
                'nom': dossier[7],
                'prenom': dossier[8],
                'element_display': map_element_id_to_text(dossier[9])
            } for dossier in dossiers]

            return render_template('validation.html', dossiers=dossier_details)
        
        else:
            return render_template('validation.html', error='Numéro de compte non trouvé ou pas de dossier pour Charge Étude.')

    except Exception as e:
        print(f"Error retrieving dossier details: {e}")
        return render_template('validation.html', error='Une erreur est survenue lors de la récupération des détails du dossier.')

    finally:
        conn.close()

    return redirect(url_for('validation'))       

@app.route('/directeur', methods=['GET'])
def directeur():
    conn = mysql.connect()
    cursor = conn.cursor()

    query_base = """
        SELECT d.id_client, d.num_compte, dt.daterecp, dt.dateenvoi, dt.etat, dt.folio
        FROM dossier d
        LEFT JOIN datetransmis dt ON d.id_client = dt.id_client
    """
    cursor.execute(query_base)
    dossiers = cursor.fetchall()
    cursor.close()
    conn.close()

    if dossiers:
        dossier_details = [{
            'id_client': dossier[0],
            'num_compte': dossier[1],
            'daterecp': dossier[2],
            'dateenvoi': dossier[3],
            'etat': dossier[4],
            'folio': dossier[5]
        } for dossier in dossiers]
        return jsonify(dossier_details)
    else:
        return jsonify([]), 404

@app.route('/directeur_filtrage', methods=['GET'])
def directeur_filtrage():
    num_compte = request.args.get('num_compte')
    filter_type = request.args.get('filter_type')
    conn = mysql.connect()
    cursor = conn.cursor()
    
    query_base = """
        SELECT d.id_client, d.num_compte, dt.daterecp, dt.dateenvoi, dt.etat, dt.folio
        FROM dossier d
        LEFT JOIN datetransmis dt ON d.id_client = dt.id_client
    """
    query_filters = []
    params = []

    if num_compte:
        query_filters.append("d.num_compte = %s")
        params.append(num_compte)

    if filter_type == 'recu_non_traite':
        query_filters.append("dt.daterecp IS NOT NULL AND (dt.etat IS NULL OR dt.etat = '')")
    elif filter_type == 'traite_envoye':
        query_filters.append("dt.daterecp IS NULL AND dt.etat IS NULL")
    elif filter_type == 'traite_non_envoye':
         query_filters.append("""
            dt.etat IN ('Conforme', 'nonconforme', 'validé') 
            AND dt.folio IN (
                SELECT folio FROM utilisateur 
                WHERE qualite IN ('charge étude', 'Charge de validation')
            )
        """)

    if query_filters:
        query = f"{query_base} WHERE {' AND '.join(query_filters)}"
    else:
        query = query_base

    cursor.execute(query, params)
    dossiers = cursor.fetchall()
    cursor.close()
    conn.close()

    if dossiers:
        dossier_details = [{
            'id_client': dossier[0],
            'num_compte': dossier[1],
            'daterecp': dossier[2],
            'dateenvoi': dossier[3],
            'etat': dossier[4],
            'folio': dossier[5]
        } for dossier in dossiers]
        return jsonify(dossier_details)
    else:
        return jsonify([]), 404

@app.route('/get_dossier_details/<id_client>', methods=['GET'])
def get_dossier_details_by_id(id_client):
    try:
        conn = mysql.connect()
        cursor = conn.cursor()

        # Query to get missing elements and descriptif based on id_client
        query = """
        SELECT DISTINCT doc.element, COALESCE(dt.descriptif, 'No description available') as descriptif
        FROM docs doc
        LEFT JOIN datetransmis dt ON doc.id_client = dt.id_client
        WHERE doc.id_client = %s AND dt.etat = 'nonconforme'
        """
        cursor.execute(query, (id_client,))
        result = cursor.fetchall()
        cursor.close()
        conn.close()

        print(f"Result from database: {result}")  # Debug statement

        if result:
            missing_elements = list(set([map_element_id_to_text(row[0]) for row in result]))
            descriptif = next((row[1] for row in result if row[1] is not None), 'No description available')
            return jsonify({'missing_elements': missing_elements, 'descriptif': descriptif})
        else:
            return jsonify({'missing_elements': [], 'descriptif': 'No details available'}), 404

    except Exception as e:
        print(f"Error retrieving dossier details: {e}")
        return jsonify({'error': 'An error occurred while retrieving dossier details'}), 500

@app.route('/directeur_page', methods=['GET'])
def directeur_page():
    return render_template('directeur.html')
 

if __name__ == '__main__':
    app.run(debug=True)
 
