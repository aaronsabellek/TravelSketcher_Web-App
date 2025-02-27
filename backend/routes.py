from flask import request, render_template, redirect, url_for, flash, jsonify
from flask_login import LoginManager, login_required, current_user, login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

from models import User, Destination, Activity
from app import app, db, login_manager


# Benutzer laden
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def home():
    return "Backend ist aktiv!"  # oder eine andere Antwort


@app.route('/dashboard')
@login_required
def dashboard():
    destinations = Destination.query.filter_by(user_id=current_user.id).order_by(Destination.position).all()
    return render_template('dashboard.html', destinations=destinations)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':

        username = request.form['username']
        email = request.form['email']  # E-Mail hinzufügen
        password = request.form['password']

        # Überprüfen, ob der Benutzername oder die E-Mail bereits existieren
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return 'Benutzername bereits vergeben!'

        existing_email = User.query.filter_by(email=email).first()
        if existing_email:
            return 'E-Mail bereits registriert!'

        # Check pw for digit
        if not any(i.isdigit() for i in password):
            flash("Password must contain at least one number", "warning")
            return redirect("/register")

          # Check pw for letter
        elif not any(i.isalpha() for i in password):
            flash("Password must contain at least one letter", "warning")
            return redirect("/register")

          # Check pw for special character
        elif not any(not i.isalnum() for i in password):
            flash("Password must contain at least one special character", "warning")
            return redirect("/register")

        # Passwort verschlüsseln
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(username=username, email=email, password=hashed_password)

        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:  # Wenn der Benutzer bereits eingeloggt ist
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)  # Hier wird der Benutzer eingeloggt
            return redirect(url_for('dashboard'))  # Nach erfolgreichem Login zur Dashboard-Seite umleiten

        flash('Login fehlgeschlagen. Überprüfe deinen Benutzernamen und dein Passwort.', 'danger')
        return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()  # Benutzer ausloggen
    flash("Erfolgreich abgemeldet.", "success")
    return redirect(url_for('home'))

@app.route('/add_destination', methods=['GET', 'POST'])
@login_required
def add_destination():
    if request.method == 'POST':
        title = request.form['title']
        country = request.form['country']
        img_link = request.form['img_link']
        duration = request.form['duration']
        tags = request.form['tags']
        status= request.form['status']
        months = request.form['month']
        accomodation_link = request.form['accomodation_link']
        accomodation_price = request.form['accomodation_price']
        accomodation_text = request.form['accomodation_text']
        trip_duration = request.form['trip_duration']
        trip_price = request.form['trip_price']
        trip_text = request.form['trip_text']
        free_text = request.form['free_text']

        # Set position number
        highest_position = db.session.query(db.func.max(Destination.position)).filter_by(user_id=current_user.id).scalar()
        new_position = (highest_position + 1) if highest_position is not None else 1


        new_destination = Destination(  name=name,
                                        title=title,
                                        country=country,
                                        img_link=img_link,
                                        duration=duration,
                                        tags=tags,
                                        status=status,
                                        months=months,
                                        accomodation_link=accomodation_link,
                                        accomodation_price=accomodation_price,
                                        accomodation_text=accomodation_text,
                                        trip_duration=trip_duration,
                                        trip_price=trip_price,
                                        trip_text=trip_text,
                                        free_text=free_text,
                                        position=new_position,
                                        user_id=current_user.id)
        db.session.add(new_destination)
        db.session.commit()

        return redirect(url_for('dashboard'))

    return render_template('add_destination.html')

@app.route('/reorder_destinations', methods=['POST'])
@login_required
def reorder_destinations():
    """
    Erwartet eine JSON-Liste mit Destination-IDs in der gewünschten Reihenfolge.
    Aktualisiert die Positionen entsprechend.
    """
    data = request.get_json()
    new_order = data.get('new_order')  # Erwartet eine Liste mit Destination-IDs in neuer Reihenfolge

    if not new_order:
        return jsonify({'error': 'Invalid data'}), 400

    # Reiseziele in neuer Reihenfolge aktualisieren
    for index, destination_id in enumerate(new_order, start=1):
        destination = Destination.query.filter_by(id=destination_id, user_id=current_user.id).first()
        if destination:
            destination.position = index

    db.session.commit()
    return jsonify({'success': True})

@app.route('/add_activity', methods=['POST'])
def add_activity():
    data = request.get_json()

    title = data.get('title')
    country = data.get('country')
    duration = data.get('duration')
    price = data.get('price')
    activity_text = data.get('activity_text')
    number = data.get('number')
    status = data.get('status')
    web_link = data.get('web_link')
    img_link = data.get('img_link')
    tags = data.get('tags')
    trip_duration = data.get('trip_duration')
    trip_price = data.get('trip_price')
    trip_text = data.get('trip_text')
    free_text = data.get('free_text')

    destination_id = data.get('destination_id')

    # Überprüfen, ob die Destination existiert
    destination = Destination.query.get(destination_id)
    if not destination:
        return jsonify({'error': 'Destination not found'}), 404

    new_activity = Activity(title=title,
                            country=country,
                            duration=duration,
                            price=price,
                            activity_text=activity_text,
                            number=number,
                            status=status,
                            web_link=web_link,
                            img_link=img_link,
                            tags=tags,
                            trip_duration=trip_duration,
                            trip_price=trip_price,
                            trip_text=trip_text,
                            free_text=free_text,
                            destination_id=destination_id)
    db.session.add(new_activity)
    db.session.commit()

    return jsonify({'message': 'Activity added successfully!', 'activity': {
        'id': new_activity.id,
        'name': new_activity.name,
        'description': new_activity.description,
        'destination_id': new_activity.destination_id
    }})

@app.route('/get_activities/<int:destination_id>', methods=['GET'])
def get_activities(destination_id):
    destination = Destination.query.get(destination_id)
    if not destination:
        return jsonify({'error': 'Destination not found'}), 404

    activities = Activity.query.filter_by(destination_id=destination_id).all()
    activities_list = [{'id': act.id, 'name': act.name, 'description': act.description} for act in activities]

    return jsonify({'destination': destination.name, 'activities': activities_list})