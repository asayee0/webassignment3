import csv, models
from flask import Flask, render_template, request, redirect, url_for
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

@app.route('/addnew')
def loadAddNewTemplate():
    return render_template("addNew.html")

@app.route('/addnew/request', methods=['POST'])
def addnew():
    animeid = request.form['animeid']
    animename = request.form['animename']
    animegenre = request.form['animegenre']
    animetype = request.form['animetype']
    animenumepisodes = request.form['animenumepisodes']
    animerating = request.form['animerating']
    animemembers = request.form['animemembers']

    with open('anime.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerow([animeid, animename, animegenre, animetype, animenumepisodes, animerating, animemembers])

    return redirect(url_for('home'))

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