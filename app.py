import csv, models, auth
from flask import (
    Blueprint, Flask, render_template, request, redirect, url_for, jsonify, flash
)
from sqlalchemy import func
from models import Anime, User

app = models.app
models.initdb()
db = models.db
app.secret_key = 'info2606'

app.register_blueprint(auth.bp)

animelist = Anime.query.with_entities(Anime.name).all()

@app.route('/')
@app.route('/home')
def home():
    return render_template("index.html", animelist=animelist)

@app.route('/<result>', methods=['GET'])
def details(result):
    return render_template("index.html", animelist=animelist, anime=Anime.query.filter_by(name = result).first())

@app.route('/addnew', methods=['GET', 'POST'])
@auth.login_required
def addNewAnime():
    if request.method == "POST":
        error = None
        animeid = request.form['animeid']
        animename = request.form['animename']
        animegenre = request.form['animegenre']
        animetype = request.form['animetype']
        animenumepisodes = request.form['animenumepisodes']
        animerating = request.form['animerating']
        animemembers = request.form['animemembers']

        if not animeid: error = "ID missing"
        elif not animename: error = "Name missing"
        elif not animegenre: error = "Genre missing"
        elif not animetype: error = "Type missing"
        elif not animenumepisodes: error = "Episodes missing"
        elif not animerating: error = "Rating missing"
        elif not animemembers: error = "Members missing"

        flash(error)
        
        if error is None:
            newAnime = Anime(animeid, animename, animegenre, animetype, animenumepisodes, animerating, animemembers)
            db.session.add(newAnime)
            db.session.commit()
            
    return render_template("addNew.html")

@app.route('/search', methods=['GET', 'POST'])
def searchAnime():
    if request.method == 'POST':
        animename = request.form['animename']
        anime = Anime.query.filter(func.lower(Anime.name) == func.lower(animename)).first()
        if anime is not None:
            return redirect(url_for("details", result=anime.name))
    return render_template("search.html")

@app.route('/update/<name>', methods=['GET', 'POST'])
@auth.login_required
def updateAnime(name):
    anime = Anime.query.filter(func.lower(Anime.name) == func.lower(name)).first()
    if request.method == "POST":
        error = None
    
        animeid = request.form['animeid']
        animename = request.form['animename']
        animegenre = request.form['animegenre']
        animetype = request.form['animetype']
        animenumepisodes = request.form['animenumepisodes']
        animerating = request.form['animerating']
        animemembers = request.form['animemembers']

        anime = Anime.query.filter_by(id=animeid).first()

        if anime is None: 
            error = "Anime does not exist"
            print("Anime does not exist")
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
            
        
        flash(error)
        return redirect(url_for('details', result=animename))
    
    return render_template("update.html", anime=anime)

@app.route('/delete', methods=['GET', 'POST'])
@auth.login_required
def deleteAnime():
    if request.method == 'POST':
        animename = request.form['animename']
        anime = Anime.query.filter(func.lower(Anime.name) == func.lower(animename)).first()
        db.session.delete(anime)
        db.session.commit()
        
        
    return render_template("delete.html")

@app.route('/delete/<name>', methods=['GET', 'POST'])
@auth.login_required
def deleteAnimeHome(name):
    animename = name
    anime = Anime.query.filter(func.lower(Anime.name) == func.lower(animename)).first()
    db.session.delete(anime)
    db.session.commit()
    
    return redirect(url_for('home'))

#animeid animename animegenre animetype animenumepisodes animerating animemembers
#animeid, animename, animegenre, animetype, animenumepisodes, animerating, animemembers
#"animeid", "animename", "animegenre", "animetype", "animenumepisodes", "animerating", "animemembers"
#[animeid], [animename], [animegenre], [animetype], [animenumepisodes], [animerating], [animemembers]