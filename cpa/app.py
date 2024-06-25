from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# MySQL Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'pass_root'
app.config['MYSQL_DB'] = 'cpa'
app.config['MYSQL_PORT'] = 3307

mysql = MySQL(app)

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
        id_client = request.form['id_client']
        num_compte = request.form['num_compte']
        nom = request.form['nom'] or None
        prenom = request.form['prenom'] or None
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

        daterecp = request.form['date_reception']  # Assuming this is from the session date
        dateenvoi = datetime.now().strftime('%Y-%m-%d')  # Fetch from form if available
        etat = None  # Fetch from form if available
        descriptif = None
        folio = session.get('folio')  # Retrieve folio from session

        # Insert into MySQL
        cur = mysql.connection.cursor()
        cur.execute("""
            INSERT INTO dossier (ID_CLIENT, NUM_COMPTE, NOM, PRENOM, RAISON_SOCIALE, ACTIVITE, ADRESSE, NUMEROTEL, DATE_OUVERTURE, DATE_CLOTURE, CAUSE, NUM_REG_COM, DATE_REG_COM, CODE_AGENCE)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                    (id_client, num_compte, nom, prenom, raison_sociale, activite, adresse, numerotel, date_ouverture, date_cloture, cause, num_reg_com, date_reg_com, code_agence))
        mysql.connection.commit()

        cur.execute("""
            INSERT INTO datetransmis (DATERECP, DATEENVOI, ETAT, DESCRIPTIF, ID_CLIENT, FOLIO)
            VALUES (%s, %s, %s, %s, %s, %s)""",
                    (daterecp, dateenvoi, etat, descriptif, id_client, folio))
        mysql.connection.commit()
        cur.close()

        return 'Successfully submitted dossier form!'
    
    return render_template('secretaire.html')

# Routes for different roles
@app.route('/etude')
def etude():
    return render_template('etude.html')

@app.route('/validation')
def validation():
    return render_template('validation.html')

@app.route('/directeur')
def directeur():
    return render_template('directeur.html')

if __name__ == '__main__':
    app.run(debug=True)
