import csv, models
from flask import Flask, render_template, request, redirect, url_for
from models import Anime

app = models.app
models.initdb()
db = models.db

animelist = None
""" with open('anime.csv', 'r', encoding = 'utf-8') as f:
    reader = csv.reader(f)
    animelist = list(reader)
 """
""" animelist = Anime.query.all()
animelist = list(map(lambda x: x.toDict(), animelist))
response = jsonify(animelist) """

@app.route('/')
@app.route('/home')
def home():
    print (type(Anime.query.with_entities(Anime.name).all()))
    #return "working"
    return render_template("index.html", animelist=Anime.query.with_entities(Anime.name).all())

@app.route('/addnew')
def loadAddNewTemplate():
    return render_template("addnew.html")

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
        
    return render_template("searchresult.html", anime=anime)

""" @app.route('displaySingleAnime')
def displaySingleAnime():
    anime = 
    return render_template("singleAnimeResult", anime=anime) """

#animeid animename animegenre animetype animenumepisodes animerating animemembers
#animeid, animename, animegenre, animetype, animenumepisodes, animerating, animemembers
#"animeid", "animename", "animegenre", "animetype", "animenumepisodes", "animerating", "animemembers"
#[animeid], [animename], [animegenre], [animetype], [animenumepisodes], [animerating], [animemembers]