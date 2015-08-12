from datetime import datetime

from draftmim.core import db
from draftmim import app

class Conference(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Conference %r>' % self.name

class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=True)
    
    def __init__(self, name):
        self.name = name
 
    def __repr__(self):
        return '<Team %r>' % self.name

class ConferenceTeam(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    team_id = db.Column(db.Integer, db.ForeignKey('teams.id'),)
    team = db.relationship('Team', backref=db.backref('teams', lazy='dynamic'))
    conference_id = db.Column(db.Integer, db.ForeignKey('conferences.id'),)
    conference = db.relationship('Conference', backref=db.backref('conferences', lazy='dynamic'))

    def __init__(self, team, conference):
        self.team = team
        self.conference = conference

    def __repr__(self):
        return '<ConferenceTeam %r-%r>' % (self.team.name, self.conference.name,)

class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    team_id = db.Column(db.Integer, db.ForeignKey('teams.id'),)
    team = db.relationship('Team', backref=db.backref('teams', lazy='dynamic'))
    number = db.Column(db.Integer, nullable=True)
    position = db.Column(db.String(10), nullable=True)
    height_ft = db.Column(db.Integer)
    height_in = db.Column(db.Integer)
    year_class = db.Column(db.String(5), nullable=True)
    hometown = db.Column(db.String(50), nullable=True)

    def __init__(self, name, team, number, position, height_ft, height_in, year_class, hometown):
        self.name = name
        self.team = team
        self.number = number
        self.position = position
        self.height_ft = height_ft
        self.height_in = height_in
        self.year_class = year_class
        self.hometown = hometown

    def __repr__(self):
        return '<Player %r>' % (self.name,)

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    home_team_id = db.Column(db.Integer, db.ForeignKey('teams.id'),)
    home_team = db.relationship('Team', backref=db.backref('teams', lazy='dynamic'))
    away_team_id = db.Column(db.Integer, db.ForeignKey('teams.id'),)
    away_team = db.relationship('Team', backref=db.backref('teams', lazy='dynamic'))
    game_time = db.Column(db.DateTime, nullable=True)

    def __init__(self, home_team, away_team, game_time=None):
        self.home_team = home_team
        self.away_team = away_team
        self.game_time = game_time

    def __repr__(self):
        return '<Game %r vs. %r>' % (self.away_team.name, self.home_team.name,)
    

# models for which we want to create API endpoints
app.config['API_MODELS'] = {'player': Player}

# models for which we want to create CRUD-style URL endpoints,
# and pass the routing onto our AngularJS application
app.config['CRUD_URL_MODELS'] = {'player': Player}
