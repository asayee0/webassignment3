import csv, models
from flask import Flask, render_template, request, redirect, url_for, jsonify
from models import Anime

app = models.app
models.initdb()
db = models.db

animelist = Anime.query.with_entities(Anime.name).all()

@app.route('/')
@app.route('/home')
def home():
    return render_template("index.html", animelist=animelist)

@app.route('/<result>', methods=['GET'])
def details(result):
    return render_template("index.html", animelist=animelist, anime=Anime.query.filter_by(name = result).first())

@app.route('/addnew', methods=['GET', 'POST'])
def loadAddNewTemplate():
    return render_template("addNew.html")

@app.route('/addnew/request', methods=['GET', 'POST'])
def addnew():
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

@app.route('/search')
def loadSearchTemplate():
    print (animelist == None)
    return render_template("search.html")

@app.route('/search/request', methods=['GET', 'POST'])
def searchAnime():
    anime = request.form['animename']
    for a in animelist:
        if a[1] == anime:
            anime = a
            break
    print(anime)
        
    return render_template("searchResult.html", anime=anime)

#animeid animename animegenre animetype animenumepisodes animerating animemembers
#animeid, animename, animegenre, animetype, animenumepisodes, animerating, animemembers
#"animeid", "animename", "animegenre", "animetype", "animenumepisodes", "animerating", "animemembers"
#[animeid], [animename], [animegenre], [animetype], [animenumepisodes], [animerating], [animemembers]