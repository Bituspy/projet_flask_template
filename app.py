from flask import Flask, render_template, request, redirect, url_for, flash, session
import mysql.connector

app = Flask(__name__)
app.secret_key = 'fsDE2LTTOE1dWhHMBAjqKqsYP47VQBaP'


def get_db_connection():
    conn = mysql.connector.connect(
        host='localhost',
        port=3306,
        user='root',
        password='',
        database='utilisateurs_db'
    )
    return conn


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        utilisateur = request.form['utilisateur']
        motdepasse = request.form['motdepasse']
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM utilisateurs WHERE utilisateur = %s AND motdepasse = %s', (utilisateur, motdepasse))
        user = cursor.fetchone()
        conn.close()

        if user:
            session['utilisateur'] = utilisateur
            return redirect(url_for('liste_employes'))
        else:
            flash('Nom d\'utilisateur ou mot de passe incorrect', 'danger')

    return render_template('login.html')


@app.route('/employes')
def liste_employes():
    if 'utilisateur' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM employes')
    employes = cursor.fetchall()
    conn.close()
    return render_template('employes.html', employes=employes)


@app.route('/ajouter_employe', methods=['GET', 'POST'])
def ajouter_employe():
    if 'utilisateur' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        role = request.form['role']
        phone = request.form['phone']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO employes (firstname, lastname, email, role, phone) VALUES (%s, %s, %s, %s, %s)',
            (firstname, lastname, email, role, phone)
        )
        conn.commit()
        conn.close()
        flash('Employé ajouté avec succès', 'success')
        return redirect(url_for('liste_employes'))

    return render_template('ajouter_employe.html')


@app.route('/modifier_employe/<int:matricule>', methods=['GET', 'POST'])
def modifier_employe(matricule):
    if 'utilisateur' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM employes WHERE matricule = %s', (matricule,))
    employe = cursor.fetchone()

    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        role = request.form['role']
        phone = request.form['phone']

        cursor.execute(
            'UPDATE employes SET firstname = %s, lastname = %s, email = %s, role = %s, phone = %s WHERE matricule = %s',
            (firstname, lastname, email, role, phone, matricule)
        )
        conn.commit()
        conn.close()
        flash('Employé modifié avec succès', 'success')
        return redirect(url_for('liste_employes'))

    conn.close()
    return render_template('modifier_employe.html', employe=employe)


@app.route('/supprimer_employe/<int:matricule>')
def supprimer_employe(matricule):
    if 'utilisateur' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM employes WHERE matricule = %s', (matricule,))
    conn.commit()
    conn.close()
    flash('Employé supprimé avec succès', 'success')
    return redirect(url_for('liste_employes'))


@app.route('/logout')
def logout():
    session.pop('utilisateur', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
