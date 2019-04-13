import csv, models
from flask import (
    Flask, render_template, request, redirect, url_for, jsonify, flash, session, g
)
import functools
from sqlalchemy import func
from models import Anime, User
from werkzeug import check_password_hash, generate_password_hash

app = models.app
models.initdb()
db = models.db
app.secret_key = 'info2606'

animelist = Anime.query.with_entities(Anime.name).all()

@app.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif User.query.filter_by(username=username).first() is not None:
            error = "User is already registered."

        print(error)

        if error is None:
            hashedPw = generate_password_hash(password)
            db.session.add(User(username, hashedPw))
            db.session.commit()
            return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None
        user = User.query.filter_by(username=username).first()

        if user is None:
            error = 'Incorrect username.'
            print(username)
        elif not check_password_hash(user.password, password):
            error = 'Incorrect password.'
            print(password)

        if error is None:
            session.clear()
            session['user_id'] = user.id
            return redirect(url_for('home'))

        print(error)

    return render_template('login.html')

@app.before_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = User.query.filter_by(id=user_id).first().username

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('login'))

        return view(**kwargs)

    return wrapped_view

@app.route('/')
@app.route('/home')
def home():
    return render_template("index.html", animelist=animelist)

@app.route('/<result>', methods=['GET'])
def details(result):
    return render_template("index.html", animelist=animelist, anime=Anime.query.filter_by(name = result).first())

@app.route('/addnew', methods=['GET', 'POST'])
@login_required
def addNewAnime():
    if request.method == "POST":
        animeid = request.form['animeid']
        animename = request.form['animename']
        animegenre = request.form['animegenre']
        animetype = request.form['animetype']
        animenumepisodes = request.form['animenumepisodes']
        animerating = request.form['animerating']
        animemembers = request.form['animemembers']

        if not animeid: success = "ID missing"
        elif not animename: success = "Name missing"
        elif not animegenre: success = "Genre missing"
        elif not animetype: success = "Type missing"
        elif not animenumepisodes: success = "Episodes missing"
        elif not animerating: success = "Rating missing"
        elif not animemembers: success = "Members missing"
        else: success=True
        
        if success==True:
            newAnime = Anime(animeid, animename, animegenre, animetype, animenumepisodes, animerating, animemembers)
            db.session.add(newAnime)
            db.session.commit()
        return render_template("addNew.html", success=success)
    else:
        return render_template("addNew.html")

@app.route('/search', methods=['GET', 'POST'])
def searchAnime():
    if request.method == 'POST':
        animename = request.form['animename']
        anime = Anime.query.filter(func.lower(Anime.name) == func.lower(animename)).first()
        return render_template("search.html", anime=anime)
    else:
        return render_template("search.html")

@app.route('/update', methods=['GET', 'POST'])
@login_required
def updateAnime():
    if request.method == "POST":
        error = None
        animeid = request.form['animeid']
        animename = request.form['animename']
        animegenre = request.form['animegenre']
        animetype = request.form['animetype']
        animenumepisodes = request.form['animenumepisodes']
        animerating = request.form['animerating']
        animemembers = request.form['animemembers']

        anime = Anime.query.filter(func.lower(Anime.name) == func.lower(animename)).first()
        if anime is None: error = "Anime does not exist"
        if not animeid: error = "ID missing"
        elif not animename: error = "Name missing"
        elif not animegenre: error = "Genre missing"
        elif not animetype: error = "Type missing"
        elif not animenumepisodes: error = "Episodes missing"
        elif not animerating: error = "Rating missing"
        elif not animemembers: error = "Members missing"
        
        if error is None:
            anime.id = animeid
            anime.name = animename
            anime.genre = animegenre
            anime.showType = animetype
            anime.episodes = animenumepisodes
            anime.rating = animerating
            anime.members = animemembers
            db.session.commit()
        else:
            flash(error)
    
    return render_template("update.html")

@app.route('/delete', methods=['GET', 'POST'])
def deleteAnime():
    if request.method == 'POST':
        animename = request.form['animename']
        anime = Anime.query.filter(func.lower(Anime.name) == func.lower(animename)).first()
        db.session.delete(anime)
        db.session.commit()
        flash("Successfully deleted")
        return render_template("delete.html")
    else:
        return render_template("delete.html")

#animeid animename animegenre animetype animenumepisodes animerating animemembers
#animeid, animename, animegenre, animetype, animenumepisodes, animerating, animemembers
#"animeid", "animename", "animegenre", "animetype", "animenumepisodes", "animerating", "animemembers"
#[animeid], [animename], [animegenre], [animetype], [animenumepisodes], [animerating], [animemembers]