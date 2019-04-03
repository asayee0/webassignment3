from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/anime.db'
db = SQLAlchemy(app)

def initdb():
    app.app_context().push()
    db.init_app(app)
    db.create_all()
    return app

class Anime(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    genre = db.Column(db.String(120), nullable=False)
    showType = db.Column(db.String(20), nullable=False)
    episodes = db.Column(db.Integer, nullable=False)
    rating = db.Column(db.String, nullable=False)
    members = db.Column(db.Integer, nullable=False)

    def __init__(self, id, name, genre, showType, episodes, rating, members):
        self.name = name
        self.genre = genre
        self.showType = showType
        self.episodes = episodes
        self.rating = rating
        self.members = members

    def __repr__(self):
        return ('<Name %r> <Genre %r>' % (self.name, self.genre))